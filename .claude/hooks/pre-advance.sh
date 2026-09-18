#!/usr/bin/env bash
# PreToolUse on Bash: refuse a stage advance whose audit gate has not passed,
# and refuse obviously unsafe execution of submission code on the host.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
read_input

command="$(hook_field tool_input.command)"
[ -z "$command" ] && exit 0

# Running a submission directly on the host is the thing the execution-safety
# policy exists to prevent.
#
# Match an actual invocation, not two words that both appear somewhere in the
# command. The old globs were *workspaces/*python\ * and friends, which fire on
# any command string holding a workspaces path followed later by a runner --
# including a `git commit` whose message body merely discusses a submission, and
# including a heredoc writing documentation about one. Both happened during
# live-trial-2026. A guard that cries wolf is a guard people learn to route
# around, which is worse than a narrower guard that means what it says.
#
# Heredoc bodies are stripped first: text on its way into a file is not a
# command. What remains is scanned for a runner adjacent to a submission path,
# for direct execution of one, and for a `cd` into one followed by a runner.
#
# This is a guard rail, not a security boundary. It does not read inside quoted
# strings passed to `bash -c`, and it is not trying to. The real controls are
# atj validate, the publication gate and the audit gates.

scan="$(printf '%s\n' "$command" | awk '
  BEGIN { skip = 0; term = "" }
  skip == 1 {
    stripped = $0
    gsub(/^[ \t]+|[ \t]+$/, "", stripped)
    if (stripped == term) { skip = 0 }
    next
  }
  {
    if (match($0, /<<-?[ \t]*'"'"'?[A-Za-z_][A-Za-z0-9_]*'"'"'?/)) {
      term = substr($0, RSTART, RLENGTH)
      sub(/^<<-?[ \t]*/, "", term)
      gsub(/'"'"'/, "", term)
      skip = 1
    }
    print
  }')"

runners='python3?|node|npm|yarn|pnpm|npx|bash|sh|zsh|ruby|perl|go|cargo|make|pytest|deno|bun'
boundary='(^|[;&|(]|&&|\|\|)[[:space:]]*'

unsafe=0

# A runner invoked on a path inside a submission checkout.
if printf '%s' "$scan" | grep -qE "${boundary}(${runners})([[:space:]]+-[^[:space:]]+)*[[:space:]]+\.?/?workspaces/"; then
  unsafe=1
fi

# Executing a file inside a submission checkout as the command itself.
if printf '%s' "$scan" | grep -qE "${boundary}\.?/workspaces/[^[:space:]]+"; then
  unsafe=1
fi

# cd into a checkout, then run something in the same chain.
if printf '%s' "$scan" | grep -qE "cd[[:space:]]+[^;&|]*workspaces/" \
  && printf '%s' "$scan" | grep -qE "(&&|;|\|\|)[[:space:]]*(${runners})([[:space:]]|$)"; then
  unsafe=1
fi

if [ "$unsafe" = 1 ]; then
  block "that runs submission code on the host. Submissions execute only through
  python3 -m atj sandbox run ...
which refuses to start unless container isolation is verified. If isolation is
unavailable, record executable evidence as unavailable and score affected
criteria NE."
fi

# Match an actual invocation in the command itself, not a phrase in text the
# command is only writing down. This reads $scan, the heredoc-stripped copy, for
# the same reason the execution guard above does: during live-trial-2026 the
# execution half false-positived on prose, D6 fixed that half, and this half kept
# reading the raw string. It then blocked a heredoc that merely contained the
# words, which is the defect twice in one file.
# Matching loosely made this hook block unrelated commands that merely mentioned
# advancing, and pick an event directory out of surrounding text.
advance='(python3?([[:space:]]+-m)?[[:space:]]+)?atj event advance[[:space:]]+\.?/?events/'
if printf '%s' "$scan" | grep -qE "${boundary}${advance}"; then
    # The invocation has to start a command, not sit inside an argument. A
    # `git commit -m "... atj event advance events/x ..."` is a sentence about
    # advancing, and blocking it is the same false positive D6 removed from the
    # execution half of this hook.
    event_dir="$(printf '%s' "$scan" \
      | grep -oE "${boundary}${advance}[A-Za-z0-9._-]+" \
      | head -n1 | grep -oE 'events/[A-Za-z0-9._-]+')"
    [ -z "$event_dir" ] && exit 0

    # D23: this check reads the gate state as it is *before* the command runs,
    # and the command may be the thing that passes the gate. A single chain that
    # records a gate and then advances was blocked on a state its own first half
    # was about to change, which is a false positive of the same family as D6:
    # the guard was reading a string, not a sequence.
    #
    # Split the chain on its sequencing operators and compare positions. When a
    # gate for this same event is passed earlier in the chain than the advance,
    # the pre-command state is not the state the advance will see, so this hook
    # has nothing reliable to say and `atj event advance` -- which re-reads the
    # ledger at execution time and refuses a pending gate itself -- is the
    # authority. Order matters: a gate recorded *after* the advance still blocks.
    sequence="$(printf '%s' "$scan" | sed -E 's/(&&|\|\||;)/\n/g')"
    gate_line="$(printf '%s\n' "$sequence" \
      | grep -nE "atj event gate[[:space:]]+\.?/?${event_dir}[[:space:]]+[A-Za-z0-9-]+[[:space:]]+passed" \
      | head -n1 | cut -d: -f1)"
    advance_line="$(printf '%s\n' "$sequence" \
      | grep -nE "atj event advance[[:space:]]+\.?/?${event_dir}" \
      | head -n1 | cut -d: -f1)"
    if [ -n "$gate_line" ] && [ -n "$advance_line" ] && [ "$gate_line" -lt "$advance_line" ]; then
      warn "this command records a gate for $event_dir before advancing it; \
leaving the decision to \`atj event advance\`, which re-reads the ledger and \
refuses a pending gate on its own"
      exit 0
    fi
    # Resolve against the command's own working directory when it is inside the
    # repository; otherwise this hook has nothing reliable to say.
    if [ -d "$REPO_ROOT/$event_dir" ]; then
      event_dir="$REPO_ROOT/$event_dir"
    else
      exit 0
    fi
    if ! status="$(atj event status "$event_dir")"; then
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
fi
exit 0
