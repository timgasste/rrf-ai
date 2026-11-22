#!/usr/bin/env bash
# Make print/literature-matrix-print.pdf (one A4 landscape page) from
# print/literature-matrix-print.html with a local headless Chromium. Nothing
# loads from the web: the fonts are in assets/fonts. scripts/build.sh copies
# the PDF into downloads/. Set CHROME= to use another Chromium binary.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROME="${CHROME:-$(ls "$HOME"/.local/share/quarto/chrome-headless-shell/*/chrome-headless-shell 2>/dev/null | head -1)}"
[[ -x "$CHROME" ]] || { echo "Stopped: no headless Chromium found. Set CHROME=." >&2; exit 1; }
OUT="$ROOT/print/literature-matrix-print.pdf"
"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --print-to-pdf="$OUT" "file://$ROOT/print/literature-matrix-print.html" 2>/dev/null
pages="$(pdfinfo "$OUT" | awk '/^Pages:/ {print $2}')"
size="$(pdfinfo "$OUT" | awk -F': *' '/^Page size:/ {print $2}')"
echo "Made $OUT: $pages page(s), $size"
[[ "$pages" == 1 ]] || { echo "Stopped: the sheet is not one page." >&2; exit 1; }
