#!/usr/bin/env bash
# Structural smoke check for the built _site/ before deploy. Exits non-zero if a
# load-bearing artifact is missing, the landing page is suspiciously small, or
# far too few pages were emitted — any of which means a silently-broken build.
set -euo pipefail

SITE="${1:-_site}"
fail() { echo "SMOKE FAIL: $*" >&2; exit 1; }

for f in index.html .nojekyll CNAME 404.html sitemap.xml robots.txt llms.txt llms-full.txt read/index.html search-index.json cover-720.webp favicon.ico favicon.svg; do
  [ -f "$SITE/$f" ] || fail "missing $SITE/$f"
done

size=$(wc -c < "$SITE/index.html")
[ "$size" -ge 51200 ] || fail "index.html only ${size} bytes (< 50 KB) — build likely broken"

# 19 sections + /read/ + redirect stub(s) => 20+ sub-page index.html files.
pages=$(find "$SITE" -mindepth 2 -maxdepth 2 -name index.html | wc -l)
[ "$pages" -ge 20 ] || fail "only ${pages} sub-page index.html files (< 20) — sections missing"

echo "SMOKE OK: ${pages} sub-pages, landing ${size} bytes, all required files present"
