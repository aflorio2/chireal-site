#!/usr/bin/env bash
set -euo pipefail

SITE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
OUTPUT="${1:-publications.pdf}"
shift || true

HIGHLIGHT_OVERRIDE=""
HAS_HIGHLIGHT_FLAG=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --highlights) HAS_HIGHLIGHT_FLAG=true; HIGHLIGHT_OVERRIDE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

JEKYLL_CONFIG="_config.yaml"
if $HAS_HIGHLIGHT_FLAG; then
  OVERRIDE_CFG=$(mktemp /tmp/_config_publist_XXXXXX.yaml)
  echo "publist_highlight_ids: \"${HIGHLIGHT_OVERRIDE}\"" > "$OVERRIDE_CFG"
  JEKYLL_CONFIG="_config.yaml,${OVERRIDE_CFG}"
  trap "rm -f '$OVERRIDE_CFG'" EXIT
fi

echo "==> Building Jekyll site..."
cd "$SITE_DIR"
bundle exec jekyll build --quiet --config "$JEKYLL_CONFIG"

echo "==> Generating PDF with Chromium..."
if command -v chromium-browser &>/dev/null; then
  CHROME="chromium-browser"
elif command -v chromium &>/dev/null; then
  CHROME="chromium"
elif command -v google-chrome &>/dev/null; then
  CHROME="google-chrome"
elif [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else
  echo "Error: No Chrome/Chromium found" >&2; exit 1
fi

"$CHROME" --headless --no-sandbox --disable-gpu \
  --print-to-pdf="$OUTPUT" --no-pdf-header-footer \
  "file://${SITE_DIR}/_site/publist-pdf.html"

echo "==> Done: $OUTPUT"
