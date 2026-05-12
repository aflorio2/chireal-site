# Project Guide

## CV Workflow

The CV is **single-sourced**: one YAML file drives both the website page and a print-ready PDF.

### Key files

| File | Role |
|---|---|
| `_data/cv.yaml` | Single source of truth for all CV content |
| `_members/adrien-florio.md` | Web CV (Liquid loops over `cv.yaml`) |
| `_layouts/cv-pdf.html` | PDF-specific layout (self-contained HTML+CSS) |
| `cv-pdf.md` | Jekyll page that uses the PDF layout (builds to `_site/cv-pdf.html`) |
| `scripts/build-cv-pdf.sh` | Builds the site then prints the PDF via headless Chrome |

### How to modify the CV

Edit `_data/cv.yaml`. Both the web page and the PDF are generated from this file. Do not edit `_members/adrien-florio.md` or `_layouts/cv-pdf.html` for content changes -- only for layout/styling changes.

### How to compile the PDF

```bash
./scripts/build-cv-pdf.sh          # outputs cv.pdf in the repo root
./scripts/build-cv-pdf.sh out.pdf  # custom output path
```

The script:
1. Runs `bundle exec jekyll build` to generate `_site/cv-pdf.html`
2. Uses headless Chrome/Chromium to print that page to a PDF

Requirements: Ruby + Bundler (for Jekyll), and Chrome or Chromium installed.

## i18n (EN/DE)

The site supports a German version alongside English, using a **mirror-tree** convention.

### Conventions

- Default language is English. A page declares itself German by adding `lang: de` to its front matter.
- DE nav pages live under `/de/` (e.g. `de/index.md` → `/de/`, `de/research/index.md` → `/de/research/`). The existing CV mirror uses a hyphen-suffix URL (`adrien-florio-de.html`); that convention is kept in place for member CVs only.
- A page may set `alt_lang_url:` in its front matter to point to the same content in the other language. The header EN|DE switcher prefers this; otherwise it falls back to `/` or `/de/`.
- UI chrome strings live in `_data/i18n.yaml` under `en:` and `de:` blocks. In any include/layout, look them up via `{% assign t = site.data.i18n[page.lang | default: 'en'] %}` and reference `{{ t.key }}`.
- A page or YAML entry that should never be translated can set `translate: false`. (Honored by the lint and the weekly translation routine, both added in later phases.)

### Header nav

The nav loop in `_includes/header.html` shows only pages whose `lang` matches the current page (EN pages with no `lang:` count as English). The EN|DE switcher is appended after the nav links.
