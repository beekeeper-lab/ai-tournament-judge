#!/usr/bin/env bash
# SessionStart: report framework health and branch, once, at the top of a session.
# Advisory only. It never blocks.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
read_input

branch="$(current_branch)"
printf 'AI Tournament Judge — framework check\n'
printf '  branch: %s' "$branch"
if [ "$branch" = "main" ]; then
  printf '  ⚠ event work must happen on a feature branch\n'
else
  printf '\n'
fi

if ! check="$(atj release-check)"; then
  printf '  release-check: FAIL\n'
  printf '%s\n' "$check" | sed 's/^/    /' | tail -n 12
else
  printf '  release-check: PASS\n'
fi

shopt -s nullglob
for event in "$REPO_ROOT"/events/*/; do
  name="$(basename "$event")"
  [ "$name" = "_template" ] && continue
  status="$(atj event status "$event" 2>&1 | sed -n '1p;5p' | tr '\n' ' ')"
  printf '  event %s: %s\n' "$name" "${status:-unreadable}"
done
exit 0
