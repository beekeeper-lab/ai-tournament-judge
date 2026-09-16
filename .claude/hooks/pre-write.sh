#!/usr/bin/env bash
# PreToolUse on Edit|Write|MultiEdit|NotebookEdit.
#
# Blocks three specific mistakes:
#   1. Writing event or framework artifacts while on main.
#   2. Editing an active event's frozen contracts (rubric version, weights,
#      personas, bracket policy) after judging has begun.
#   3. Writing into an event's public/ directory by hand, which bypasses the
#      publication gate.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
read_input

path="$(hook_field tool_input.file_path)"
[ -z "$path" ] && exit 0

case "$path" in
  "$REPO_ROOT"/*) relative="${path#"$REPO_ROOT"/}" ;;
  /*) exit 0 ;;                       # outside the repository; not ours to police
  *) relative="$path" ;;
esac

branch="$(current_branch)"
if [ "$branch" = "main" ]; then
  case "$relative" in
    events/*|framework/*|schemas/*|atj/*|.claude/*)
      block "refusing to modify $relative on main. Create a feature branch first:
  git switch -c feature/<name>
This is the repository's own working rule, not a Claude Code restriction." ;;
  esac
fi

case "$relative" in
  events/*/public/*)
    block "public artifacts are generated and gated, not hand-edited.
Generate the artifact, then run:
  python3 -m atj validate publication $relative --event-dir events/<event>
A public artifact must carry an approving official and its source artifacts." ;;
esac

case "$relative" in
  framework/rubrics/*|framework/personas.md)
    active=""
    shopt -s nullglob
    for event in "$REPO_ROOT"/events/*/status.md; do
      name="$(basename "$(dirname "$event")")"
      [ "$name" = "_template" ] && continue
      stage="$(grep -m1 '^current_stage:' "$event" 2>/dev/null | awk '{print $2}')"
      case "$stage" in
        configuration|complete|"") ;;
        *) active="$active $name($stage)" ;;
      esac
    done
    if [ -n "$active" ]; then
      block "refusing to edit $relative while judging is under way for:$active
An active event's rubric, weights, personas and bracket policy are frozen.
Create a new version and migrate or restart explicitly instead."
    fi
    ;;
esac
exit 0
