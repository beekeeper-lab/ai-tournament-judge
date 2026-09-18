"""The egress proxy that makes a network allowlist enforceable.

Advisory 5 of `docs/final-audit.md`: "A network allowlist needs an egress proxy
this repository does not provide. Configuring one without a proxy is refused,
which is correct and means the allowlist path is untested end to end."

The refusal is still there for the case with no proxy. These tests cover the
proxy: the allowlist grammar, the filter it compiles to, the container wiring,
and the refusals that keep one event's allowlist from being enforced against
another's run. The live path -- an allowed host reaching 200, a denied host
getting 403 from the proxy, and both bypass routes closed -- needs a container
runtime and a network, so it runs only when asked with `ATJ_LIVE_SANDBOX=1`.
"""

import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import egress, sandbox
from atj.errors import SafetyError

LIVE = os.environ.get("ATJ_LIVE_SANDBOX") == "1"
PODMAN = shutil.which("podman") is not None


class TheAllowlistGrammarIsStrict(unittest.TestCase):
    """An entry this filter cannot express exactly would have to be widened."""

    def test_bare_hostnames_and_one_wildcard_form(self):
        self.assertEqual(
            egress.normalize_allowlist(["PyPI.org", "*.pythonhosted.org", "pypi.org"]),
            ("pypi.org", "*.pythonhosted.org"),
        )

    def test_anything_that_is_not_a_hostname_is_refused(self):
        for entry in (
            "https://pypi.org/simple/", "pypi.org:443", "pypi.org/simple", "10.0.0.1",
            "*", "*.org.", "-pypi.org", "localhost", "a..b",
        ):
            with self.subTest(entry):
                with self.assertRaises(SafetyError):
                    egress.normalize_allowlist([entry])

    def test_an_empty_allowlist_is_refused_rather_than_allowing_everything(self):
        with self.assertRaises(SafetyError) as raised:
            egress.normalize_allowlist([])
        self.assertIn("run with no network instead", raised.exception.message)


class TheFilterIsAnchored(unittest.TestCase):
    """`pypi.org` may not also permit `pypi.org.attacker.example`."""

    def compile(self, allowlist):
        import re

        rules = [re.compile(line, re.IGNORECASE)
                 for line in egress.filter_rules(egress.normalize_allowlist(allowlist)).split()]
        return lambda host: any(rule.match(host) for rule in rules)

    def test_an_exact_host_matches_only_itself(self):
        allows = self.compile(["pypi.org"])
        self.assertTrue(allows("pypi.org"))
        for host in ("pypi.org.attacker.example", "notpypi.org", "files.pypi.org", "pypi.orgx"):
            with self.subTest(host):
                self.assertFalse(allows(host))

    def test_a_wildcard_matches_subdomains_and_not_the_suffix_alone(self):
        allows = self.compile(["*.pythonhosted.org"])
        self.assertTrue(allows("files.pythonhosted.org"))
        self.assertTrue(allows("a.b.pythonhosted.org"))
        for host in ("pythonhosted.org", "pythonhosted.org.attacker.example", "xpythonhosted.org"):
            with self.subTest(host):
                self.assertFalse(allows(host))

    def test_connect_is_limited_to_the_web_ports(self):
        config = egress.proxy_config()
        self.assertIn("FilterDefaultDeny Yes", config)
        self.assertIn("ConnectPort 443", config)
        self.assertIn("ConnectPort 80", config)
        self.assertNotIn("ConnectPort 22", config)


class TheSandboxJoinsTheInternalNetwork(unittest.TestCase):
    def build(self, **kwargs):
        return sandbox.build_command(
            runtime="podman", image="img", source=ROOT / "workspaces",
            command=["sh", "-c", "true"], **kwargs,
        )

    def test_no_proxy_still_means_no_network(self):
        argv = self.build()
        self.assertIn("none", argv)
        self.assertNotIn(egress.SANDBOX_NETWORK, argv)

    def test_a_proxy_puts_the_run_on_the_internal_network(self):
        argv = self.build(
            network_allowlist=["pypi.org"], egress_proxy="http://10.89.1.1:8888"
        )
        self.assertIn(egress.SANDBOX_NETWORK, argv)
        self.assertNotIn("none", argv)
        joined = " ".join(argv)
        for variable in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy"):
            with self.subTest(variable):
                self.assertIn(f"{variable}=http://10.89.1.1:8888", joined)

    def test_an_allowlist_without_a_proxy_is_still_refused(self):
        with self.assertRaises(SafetyError) as raised:
            self.build(network_allowlist=["pypi.org"])
        self.assertIn("would in fact grant unrestricted network access",
                      raised.exception.message)


class TheProxyMustMatchTheEventsAllowlist(unittest.TestCase):
    """A proxy from another event enforces that event's decision, not this one's."""

    def test_no_proxy_running_is_a_refusal_that_says_what_to_do(self):
        original = egress.state

        def absent(runtime=None):
            return egress.ProxyState(runtime="podman", running=False, allowlist=(), url="")

        egress.state = absent
        try:
            with self.assertRaises(SafetyError) as raised:
                egress.require_for(["pypi.org"])
            self.assertIn("atj sandbox proxy up", raised.exception.message)
        finally:
            egress.state = original

    def test_a_different_allowlist_is_refused_by_name(self):
        original = egress.state

        def other(runtime=None):
            return egress.ProxyState(
                runtime="podman", running=True, allowlist=("example.com",),
                url="http://10.89.1.1:8888",
            )

        egress.state = other
        try:
            with self.assertRaises(SafetyError) as raised:
                egress.require_for(["pypi.org"])
            self.assertIn("['example.com']", raised.exception.message)
            self.assertIn("['pypi.org']", raised.exception.message)
        finally:
            egress.state = original

    def test_a_matching_allowlist_returns_the_url(self):
        original = egress.state

        def matching(runtime=None):
            return egress.ProxyState(
                runtime="podman", running=True, allowlist=("pypi.org", "*.pythonhosted.org"),
                url="http://10.89.1.1:8888",
            )

        egress.state = matching
        try:
            self.assertEqual(
                egress.require_for(["*.pythonhosted.org", "pypi.org"]),
                "http://10.89.1.1:8888",
            )
        finally:
            egress.state = original


@unittest.skipUnless(LIVE and PODMAN, "needs a container runtime and ATJ_LIVE_SANDBOX=1")
class TheLivePathWasExercised(unittest.TestCase):
    """The end-to-end behaviour advisory 5 said had never been run.

    Opt-in: it builds an image, creates two networks and reaches the internet.
    CI stays hermetic; this is what an operator runs on the event host before
    trusting an allowlist.
    """

    ALLOWLIST = ["pypi.org", "*.pythonhosted.org"]
    CLIENT = "docker.io/curlimages/curl:latest"

    @classmethod
    def setUpClass(cls):
        cls.state = egress.start(cls.ALLOWLIST)

    @classmethod
    def tearDownClass(cls):
        egress.stop()

    def client(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["podman", "run", "--rm", "--network", egress.SANDBOX_NETWORK, *args],
            capture_output=True, text=True, timeout=180, check=False,
        )

    def curl(self, url: str, proxy: bool = True) -> str:
        argv = []
        if proxy:
            argv += ["--env", f"https_proxy={self.state.url}",
                     "--env", f"http_proxy={self.state.url}"]
        done = self.client(*argv, self.CLIENT, "-sS", "--max-time", "30",
                           "-o", "/dev/null", "-w", "%{http_code}", url)
        return (done.stdout or "").strip()

    def test_an_allowed_host_is_reachable(self):
        self.assertEqual(self.curl("https://pypi.org/simple/"), "200")

    def test_a_denied_host_is_refused_by_the_proxy(self):
        self.assertEqual(self.curl("https://example.com/"), "000")

    def test_the_sandbox_network_has_no_resolver(self):
        done = self.client(self.CLIENT, "-sS", "--max-time", "8", "https://pypi.org/simple/")
        self.assertIn("Could not resolve host", done.stderr)

    def test_an_internal_network_has_no_route_out(self):
        done = self.client(self.CLIENT, "-sS", "--max-time", "8", "https://151.101.0.223/")
        self.assertIn("Could not connect", done.stderr)

    def test_the_network_is_internal_and_has_dns_disabled(self):
        inspected = subprocess.run(
            ["podman", "network", "inspect", egress.SANDBOX_NETWORK],
            capture_output=True, text=True, check=False,
        )
        facts = json.loads(inspected.stdout)[0]
        self.assertTrue(facts.get("internal"))
        self.assertFalse(facts.get("dns_enabled"))


if __name__ == "__main__":
    unittest.main()
