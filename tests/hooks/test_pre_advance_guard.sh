#!/usr/bin/env bash
# Behavioural tests for the run-on-host guard in pre-advance.sh.
#
# The guard blocked a `git commit` during live-trial-2026 whose message body
# merely discussed a submission. These cases pin both directions: prose about a
# submission passes, actually running one does not.
set -uo pipefail

HOOK="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/.claude/hooks/pre-advance.sh"
pass=0
fail=0

run_hook() {
  # The hook reads a JSON event on stdin and exits non-zero to block.
  python3 -c '
import json, sys
print(json.dumps({"tool_name": "Bash", "tool_input": {"command": sys.argv[1]}}))
' "$1" | bash "$HOOK" >/dev/null 2>&1
}

expect() {
  local want="$1" desc="$2" cmd="$3"
  if run_hook "$cmd"; then got=allow; else got=block; fi
  if [ "$got" = "$want" ]; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    printf 'FAIL  expected %s, got %s: %s\n' "$want" "$got" "$desc"
  fi
}

# --- must still block: actually running submission code on the host ---
expect block "python on a submission path" \
  'python3 workspaces/live-trial-2026/team-ledger/src/fin/cli.py --help'
expect block "pytest inside a checkout" \
  'pytest workspaces/live-trial-2026/team-ledger/tests'
expect block "npm with a prefix flag" \
  'npm --prefix workspaces/live-trial-2026/team-podcast test'
expect block "executing a file in a checkout" \
  './workspaces/live-trial-2026/team-podcast/run.sh'
expect block "cd into a checkout then run" \
  'cd workspaces/live-trial-2026/team-ledger && python3 -m pytest'
expect block "chained after a safe command" \
  'git status && node workspaces/live-trial-2026/team-podcast/server/app.js'

# --- must allow: talking about a submission is not running one ---
expect allow "commit message naming a submission path" \
  'git commit -m "notes: workspaces/live-trial-2026/team-podcast e2e reached stage 7" && python3 -m atj release-check'
expect allow "heredoc writing docs that mention a checkout and a runner" \
  "$(printf 'cat > notes.md <<%sNOTES%s\nRun the suite in workspaces/live-trial-2026/team-podcast\nwith python3 and node.\nNOTES\npython3 -m atj validate reports events/live-trial-2026' "'" "'")"
expect allow "the sanctioned sandbox invocation" \
  'python3 -m atj sandbox run workspaces/live-trial-2026/team-ledger --image img -- sh -c "pytest"'
expect allow "reading a submission file" \
  'grep -rn subprocess workspaces/live-trial-2026/team-ledger/src/fin/'
expect allow "atj commands that mention nothing" \
  'python3 -m atj event status events/live-trial-2026'
expect allow "listing a checkout" \
  'ls workspaces/live-trial-2026/team-podcast'

# --- D23: the gate check reads pre-command state, so order matters ---
# Both committed events are `complete`, so `atj event status` reports them
# blocked and a bare advance is refused. That is the baseline for these cases.
ADV='python3 -m atj event advance events/live-trial-2026'
GATE='python3 -m atj event gate events/live-trial-2026 final-audit-passed passed --audit audits/final.md'
OTHER_GATE='python3 -m atj event gate events/sample-mock-2026 final-audit-passed passed --audit audits/final.md'
PENDING='python3 -m atj event gate events/live-trial-2026 final-audit-passed pending'

expect block "a bare advance of a blocked event" "$ADV"
expect allow "a gate recorded before the advance in the same chain" "$GATE && $ADV"
expect block "a gate recorded after the advance" "$ADV && $GATE"
expect block "a gate for a different event before the advance" "$OTHER_GATE && $ADV"
expect block "a gate set to pending before the advance" "$PENDING && $ADV"

# The gate half read the raw command string long after D6 fixed the execution
# half, so a heredoc that merely wrote the words down was blocked.
expect allow "a heredoc describing an advance" \
  "$(printf 'cat > notes.md <<%sNOTES%s\nThen run %s to finish the event.\nNOTES' "'" "'" "$ADV")"
expect allow "a commit message describing an advance" \
  "git commit -m \"docs: $ADV is the last step\""

printf '\npre-advance guard: %d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
