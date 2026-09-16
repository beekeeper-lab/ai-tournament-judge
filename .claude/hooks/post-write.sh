#!/usr/bin/env bash
# PostToolUse on Edit|Write|MultiEdit: validate what was just written.
# Advisory: it reports problems back to Claude but never reverts anything.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
read_input

path="$(hook_field tool_input.file_path)"
[ -z "$path" ] && exit 0
[ -f "$path" ] || exit 0
case "$path" in *.md) ;; *) exit 0 ;; esac

case "$path" in
  "$REPO_ROOT"/events/*) ;;
  *) exit 0 ;;
esac

relative="${path#"$REPO_ROOT"/}"
event_dir="$REPO_ROOT/$(printf '%s' "$relative" | cut -d/ -f1,2)"
[ "$(basename "$event_dir")" = "_template" ] && exit 0

if ! output="$(atj validate reports "$event_dir")"; then
  printf 'atj-hook: report validation found problems after writing %s\n' "$relative" >&2
  printf '%s\n' "$output" | grep -E 'BLOCKING|MAJOR' | head -n 15 >&2
  printf 'atj-hook: fix these before the stage audit; `atj validate reports %s` shows all of them.\n' "$event_dir" >&2
fi
exit 0
