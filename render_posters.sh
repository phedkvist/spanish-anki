#!/usr/bin/env bash
# Render posters to PDF and PNG, and complain if one no longer fits on A4.
#
#   ./render_posters.sh                  # all of them
#   ./render_posters.sh poster-pasado    # just one (.html optional)
#
# Each page is sized to fill A4 exactly, so a poster that grows spills onto a
# second page. That is what the page count at the end is checking.
set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || { echo "Chrome not found at $CHROME" >&2; exit 1; }

cd "$(dirname "$0")/posters"

if [ $# -gt 0 ]; then
  targets=()
  for arg in "$@"; do targets+=("${arg%.html}.html"); done
else
  targets=(*.html)
fi

status=0
for html in "${targets[@]}"; do
  base="${html%.html}"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --virtual-time-budget=8000 --print-to-pdf="$base.pdf" "$html" 2>/dev/null
  "$CHROME" --headless --disable-gpu --hide-scrollbars \
    --virtual-time-budget=8000 --window-size=794,1123 \
    --force-device-scale-factor=2 --screenshot="$base.png" "$html" 2>/dev/null

  pages=$(python3 -c "
import re,sys
d=open('$base.pdf','rb').read()
print(len(re.findall(rb'/Type\s*/Page[^s]',d)))")

  if [ "$pages" = "1" ]; then
    printf '%-26s ok\n' "$base"
  else
    printf '%-26s SPILLS TO %s PAGES - reduce .verb padding or table line-height\n' "$base" "$pages"
    status=1
  fi
done
exit $status
