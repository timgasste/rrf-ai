#!/usr/bin/env bash
# Build the workshop page: copy the matrix files and the latest deck export (if
# there is one), check that the prompts match the course's prompt file, and
# render into docs/.
#
# The print sheet comes from print/ in this repository (scripts/make-print.sh).
# Sources, both relative to the lecture folder this repo sits in (found through
# git, so the build also works from a worktree):
#   LECTURE/prompts.md, LECTURE/demo/     the prompts and the matrix files
#   LECTURE/presentations/                the deck (override with DECK=...)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMMON="$(git -C "$ROOT" rev-parse --path-format=absolute --git-common-dir)"
LECTURE="${LECTURE:-$(dirname "$(dirname "$COMMON")")}"
DECK="${DECK:-$LECTURE/presentations}"
EXPORT="$DECK/output/final-output"
PDF_NAME="rrf-ai-workshop-slides.pdf"
META=()
mkdir -p "$ROOT/slides" "$ROOT/downloads"

# The matrix files: the page links all three, so the build stops without them.
for f in literature-matrix-template.xlsx literature-matrix-template.csv literature-matrix-criminal-governance.xlsx
do
  if [[ -f "$LECTURE/demo/$f" ]]
  then
    cp "$LECTURE/demo/$f" "$ROOT/downloads/$f"
  elif [[ ! -f "$ROOT/downloads/$f" ]]
  then
    echo "Stopped: no $f in $LECTURE/demo. Set LECTURE= to the lecture folder." >&2
    exit 1
  fi
done

# The matrix sheet to print, made by scripts/make-print.sh from print/.
PRINT="$ROOT/print/literature-matrix-print.pdf"
[[ -f "$PRINT" ]] || { echo "Stopped: no $PRINT. Run scripts/make-print.sh." >&2; exit 1; }
[[ "$PRINT" -ot "$ROOT/print/literature-matrix-print.html" ]] && \
  echo "Warning: the print PDF is older than its HTML. Run scripts/make-print.sh." >&2
cp "$PRINT" "$ROOT/downloads/literature-matrix-print.pdf"

# The prompts must equal prompts.md word for word.
if [[ -f "$LECTURE/prompts.md" ]]
then
  python3 "$ROOT/scripts/check-prompts.py" "$LECTURE/prompts.md" "$ROOT/index.qmd"
else
  echo "Warning: no $LECTURE/prompts.md, so the prompts were not checked." >&2
fi

# The deck's files are named after its DECK_NAME: <deck>-audience.html, and
# <deck>.pdf only after `make export-pdf`. Without an export the page says the
# slides come later. Nothing stale is published: the build stops instead.
AUDIENCE=""
if [[ -d "$EXPORT" ]]
then
  AUDIENCE="$(find "$EXPORT" -maxdepth 1 -name '*-audience.html' | sort)"
fi
if [[ "$AUDIENCE" == *$'\n'* ]]
then
  echo "Stopped: more than one *-audience.html in $EXPORT. Ask Tim which deck the page shows." >&2
  exit 1
fi
if [[ -n "$AUDIENCE" ]]
then
  [[ "$AUDIENCE" -ot "$DECK/presentation.qmd" ]] && \
    echo "Warning: the deck export is older than presentation.qmd. Re-export before publishing." >&2
  cp "$AUDIENCE" "$ROOT/slides/index.html"
  META+=(-M has-slides:true)
  SLIDES_PDF="${AUDIENCE%-audience.html}.pdf"
  if [[ -f "$SLIDES_PDF" ]]
  then
    [[ "$SLIDES_PDF" -ot "$DECK/presentation.qmd" ]] && \
      echo "Warning: $(basename "$SLIDES_PDF") is older than presentation.qmd. Re-export before publishing." >&2
    cp "$SLIDES_PDF" "$ROOT/downloads/$PDF_NAME"
    META+=(-M has-slides-pdf:true)
  else
    rm -f "$ROOT/downloads/$PDF_NAME"
    echo "Note: no $(basename "$SLIDES_PDF") (make export-pdf), so the page offers no slides PDF." >&2
  fi
  python3 "$ROOT/scripts/check-sync.py" "$DECK/presentation.qmd" "$ROOT/index.qmd"
else
  rm -f "$ROOT/slides/index.html" "$ROOT/downloads/$PDF_NAME"
  echo "Note: no deck export in $EXPORT, so the page says the slides come later." >&2
fi

rm -rf "$ROOT/docs"
(cd "$ROOT" && quarto render ${META[@]+"${META[@]}"})
echo "Built: $ROOT/docs/index.html"
