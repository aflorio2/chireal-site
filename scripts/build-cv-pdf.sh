#!/usr/bin/env bash
set -euo pipefail

SITE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT="${1:-cv.pdf}"

echo "==> Building Jekyll site..."
cd "$SITE_DIR"
bundle exec jekyll build --quiet

echo "==> Generating PDF with Chromium..."
chromium-browser --headless --no-sandbox --disable-gpu \
  --print-to-pdf="$OUTPUT" --no-pdf-header-footer \
  "file://${SITE_DIR}/_site/cv-pdf.html"

echo "==> Done: $OUTPUT"
