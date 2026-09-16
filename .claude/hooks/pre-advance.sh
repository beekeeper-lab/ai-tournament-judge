#!/usr/bin/env bash
# PreToolUse on Bash: refuse a stage advance whose audit gate has not passed,
# and refuse obviously unsafe execution of submission code on the host.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
read_input

command="$(hook_field tool_input.command)"
[ -z "$command" ] && exit 0

# Running a submission directly on the host is the thing the execution-safety
# policy exists to prevent.
case "$command" in
  *workspaces/*npm\ *|*workspaces/*yarn\ *|*workspaces/*pnpm\ *|*workspaces/*python\ *|*workspaces/*./*)
    block "that runs submission code on the host. Submissions execute only through
  python3 -m atj sandbox run ...
which refuses to start unless container isolation is verified. If isolation is
unavailable, record executable evidence as unavailable and score affected
criteria NE." ;;
esac

case "$command" in
  *"atj event advance"*|*"event advance"*)
    event_dir="$(printf '%s' "$command" | grep -oE 'events/[A-Za-z0-9._-]+' | head -n1)"
    [ -z "$event_dir" ] && exit 0
    [ -d "$REPO_ROOT/$event_dir" ] || exit 0
    if ! status="$(atj event status "$REPO_ROOT/$event_dir")"; then
      warn "could not read $event_dir status; allowing and leaving the check to atj itself"
      exit 0
    fi
    if printf '%s' "$status" | grep -q 'blocked:'; then
      reason="$(printf '%s' "$status" | grep -m1 'blocked:')"
      block "the stage gate for $event_dir has not passed.
  $reason
Run the stage audit, record the result with \`atj event gate\`, then advance.
Advancing past a failed audit is what the gate exists to prevent." 
    fi
    ;;
esac
exit 0
