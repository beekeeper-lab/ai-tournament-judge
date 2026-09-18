#!/usr/bin/env bash
# UserPromptSubmit: put the branch and each event's next safe action in context,
# so the model does not have to re-derive them or guess.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
read_input

branch="$(current_branch)"
line="atj: branch=$branch"
[ "$branch" = "main" ] && line="$line (event work must move to a feature branch)"

shopt -s nullglob
for event in "$REPO_ROOT"/events/*/; do
  name="$(basename "$event")"
  [ "$name" = "_template" ] && continue
  stage="$(grep -m1 '^current_stage:' "$event/status.md" 2>/dev/null | awk '{print $2}')"
  next="$(atj event status "$event" 2>/dev/null | grep -m1 '  next:' | sed 's/^ *next: *//')"
  line="$line | $name: stage=${stage:-?}${next:+, next=$next}"
done
printf '%s\n' "$line"
exit 0
