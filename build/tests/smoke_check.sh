#!/usr/bin/env bash
# Structural smoke check for the built _site/ before deploy. Exits non-zero if a
# load-bearing artifact is missing, the landing page is suspiciously small, or
# far too few pages were emitted — any of which means a silently-broken build.
set -euo pipefail

SITE="${1:-_site}"
fail() { echo "SMOKE FAIL: $*" >&2; exit 1; }

for f in index.html .nojekyll CNAME 404.html sitemap.xml robots.txt llms.txt llms-full.txt read/index.html full/index.html search-index.json cover-720.webp favicon.ico favicon.svg; do
  [ -f "$SITE/$f" ] || fail "missing $SITE/$f"
done

size=$(wc -c < "$SITE/index.html")
[ "$size" -ge 51200 ] || fail "index.html only ${size} bytes (< 50 KB) — build likely broken"

# Short edition: 18 sections + /read/ + /full/ (archive) + 9 redirect stubs
# for retired slugs => 29+ sub-page index.html files at depth 2.
pages=$(find "$SITE" -mindepth 2 -maxdepth 2 -name index.html | wc -l)
[ "$pages" -ge 29 ] || fail "only ${pages} sub-page index.html files (< 29) — sections or redirect stubs missing"

# The Romanian edition, when built, mirrors the same page set under /ro/.
if [ -d "$SITE/ro" ]; then
  for f in ro/index.html ro/404.html ro/llms.txt ro/llms-full.txt ro/read/index.html ro/full/index.html ro/search-index.json; do
    [ -f "$SITE/$f" ] || fail "missing $SITE/$f"
  done
  ro_pages=$(find "$SITE/ro" -mindepth 2 -maxdepth 2 -name index.html | wc -l)
  [ "$ro_pages" -ge 28 ] || fail "only ${ro_pages} /ro/ sub-page index.html files (< 28)"
fi

echo "SMOKE OK: ${pages} sub-pages, landing ${size} bytes, all required files present"
