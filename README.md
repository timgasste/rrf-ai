# rrf-ai

The students' page for the AI workshop in Reviewing a Research Field (2FK052), Monday 23 November 2026: four workflows from the easiest to the most advanced, the prompts with copy buttons, the example matrix, the course's AI guidelines, and the slides. Built with Quarto into `docs/`, to be published at <https://timgasste.github.io/rrf-ai/> from `docs/` on `main`.

## Build

```bash
scripts/build.sh
```

The build reads from the lecture folder this repository sits in (found through git, or set `LECTURE=`):

- `prompts.md`: `scripts/check-prompts.py` stops the build unless every prompt in `index.qmd` equals it word for word.
- `demo/`: the example matrix, copied to `downloads/`.
- `print/literature-matrix-print.pdf` (in this repository): the matrix sheet to print, one A4 landscape page. `scripts/make-print.sh` makes it from `print/literature-matrix-print.html` with a local headless Chromium.
- `presentations/output/final-output/` (or `DECK=`): `<deck>-audience.html` becomes `slides/index.html`, and `<deck>.pdf`, if there is one, the slides PDF. Without an export the page says the slides come later.

The page loads nothing from other hosts: Work Sans is served from `assets/fonts/`, and the theme's web font import is switched off in `styles.scss`.

Only audience-facing files belong in this repository.
