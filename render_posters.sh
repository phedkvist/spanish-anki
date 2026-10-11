#!/usr/bin/env bash
# Render posters to PDF, and complain if one no longer fits on A4.
#
#   ./render_posters.sh                  # all of them
#   ./render_posters.sh poster-pasado    # just one (.html optional)
#
# Sources live in posters/src/*.html; the rendered PDF lands in posters/ next
# to its siblings, which is the folder you actually open to print one.
#
# Each page is sized to fill A4 exactly, so a poster that grows spills onto a
# second page. That is what the page count at the end is checking.
set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || { echo "Chrome not found at $CHROME" >&2; exit 1; }

# A throwaway profile per run. Chrome locks its default user-data-dir, so a
# headless process left over from an earlier render silently blocks this one.
PROFILE="$(mktemp -d)"
trap 'rm -rf "$PROFILE"' EXIT
chrome(){ "$CHROME" --headless --disable-gpu --user-data-dir="$PROFILE" \
                   --no-first-run --no-default-browser-check "$@"; }

cd "$(dirname "$0")/posters"
mkdir -p src

if [ $# -gt 0 ]; then
  targets=()
  for arg in "$@"; do targets+=("src/$(basename "${arg%.html}").html"); done
else
  targets=(src/*.html)
fi

status=0
for html in "${targets[@]}"; do
  base="$(basename "${html%.html}")"

  # a poster declares its own length: one <section class="page"> per A4 sheet,
  # or none at all for the single-page ones
  want=$(grep -c 'class="page"' "$html" || true)
  [ "$want" -eq 0 ] && want=1

  chrome --no-pdf-header-footer \
    --virtual-time-budget=8000 --print-to-pdf="$base.pdf" "$html" 2>/dev/null

  pages=$(python3 -c "
import re,sys
d=open('$base.pdf','rb').read()
print(len(re.findall(rb'/Type\s*/Page[^s]',d)))")

  # the grids are built by JS, so a thrown exception leaves a page that is the
  # right size and completely empty - count what actually rendered
  cells=$(chrome --virtual-time-budget=8000 --dump-dom "$html" 2>/dev/null \
            | { grep -o 'class="verb"' || true; } | wc -l | tr -d ' ')
  builds_grid=$(grep -c 'const V = \[' "$html" || true)

  if [ "$pages" != "$want" ]; then
    printf '%-26s WANTED %s PAGES, GOT %s - reduce .verb padding or table line-height\n' \
      "$base" "$want" "$pages"
    status=1
  elif [ "$builds_grid" -gt 0 ] && [ "$cells" -eq 0 ]; then
    printf '%-26s EMPTY - the page script threw; check the browser console\n' "$base"
    status=1
  else
    printf '%-26s ok  (%s page%s, %s verbs)\n' "$base" "$pages" \
      "$([ "$pages" = 1 ] || echo s)" "$cells"
  fi
done
exit $status
