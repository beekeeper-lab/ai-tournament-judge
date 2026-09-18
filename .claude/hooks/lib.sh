#!/usr/bin/env bash
# Shared helpers for the project-local hooks.
#
# Hooks here are guard rails, not a security boundary. They run in the operator's
# own shell with the operator's own permissions, and anything they check can be
# done another way. They exist to catch the ordinary mistake — editing on main,
# publishing an unapproved artifact, leaving a placeholder in a report — early
# enough to be cheap. The real controls are `atj validate`, `atj
# validate publication`, and the audit gates, which run whether or not a hook did.
#
# Every hook fails OPEN: an internal error warns and allows. A hook that blocked
# on its own bug would be worse than no hook, and its blocking would be mistaken
# for a safety guarantee it cannot provide.

set -uo pipefail

REPO_ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
export REPO_ROOT

# Never let a hook hang a session.
HOOK_TIMEOUT="${ATJ_HOOK_TIMEOUT:-15}"

atj() {
  timeout "$HOOK_TIMEOUT" python3 -m atj --root "$REPO_ROOT" "$@" 2>&1
}

warn() { printf 'atj-hook: %s\n' "$1" >&2; }

# Block the tool call and tell Claude why. Exit code 2 is the documented
# "block and feed stderr back" contract.
block() { printf 'atj-hook BLOCKED: %s\n' "$1" >&2; exit 2; }

current_branch() {
  git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
}

# Read the hook payload once; callers use $HOOK_INPUT.
read_input() {
  HOOK_INPUT="$(cat)"
  export HOOK_INPUT
}

# Pull a field out of the hook JSON without assuming jq is installed.
hook_field() {
  python3 -c '
import json, sys
try:
    payload = json.loads(sys.stdin.read() or "{}")
except json.JSONDecodeError:
    sys.exit(0)
node = payload
for part in sys.argv[1].split("."):
    if isinstance(node, dict):
        node = node.get(part)
    else:
        node = None
        break
print("" if node is None else node)
' "$1" <<<"$HOOK_INPUT" 2>/dev/null || true
}
