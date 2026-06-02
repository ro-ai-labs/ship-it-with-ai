# Review Pass — Plan 1: Build & Deploy Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the GitHub Pages build reproducible and self-guarding so a broken or non-deterministic build can never silently deploy to the live apex domain.

**Architecture:** Five independent changes to the build/deploy pipeline: pin the one build dependency by hash; derive the build date from content (not wall-clock) so rebuilds are byte-identical; harden the generator's failure modes; wire the *real* `_site/`-serving verifier (currently unwired) with a no-rebuild mode; and add a CI gate that smoke-checks the built artifact and runs that verifier before deploy. This is **Plan 1 of 4** for the 2026-06-02 review pass (spec: `docs/superpowers/specs/2026-06-02-review-pass-design.md`, Workstream **G**). It establishes the `verify:site` harness that Plans 2–4 (site/template, manuscript, FAQ) rely on, and has zero authorial/content risk.

**Tech Stack:** Python 3.12 (`build/build_spa.py`, stdlib + `markdown`), Node/Playwright verifier (`build/tests/`), GitHub Actions (`.github/workflows/static.yml`), bash.

**Conventions for this repo:** commit messages use `build:`/`ci:`/`test:` prefixes; **no Claude attribution** in commits. Run all commands from the repo root `/home/mihai/ai-labs/ship-it-with-agents` unless a step says otherwise.

---

## Files

- **Create:** `build/requirements.txt` — single hashed pin for `markdown` (Task 1).
- **Create:** `build/tests/smoke_check.sh` — structural smoke check for `_site/`, reused locally + in CI (Task 5).
- **Modify:** `build/build_spa.py` — add `_content_date()` helper + replace 3 `datetime.now()` sites (Task 2); import guard + `EXPECTED_PAGE_COUNT` + fix stale comment (Task 3).
- **Modify:** `build/tests/lib/build_and_serve.js` — `SITE_NO_REBUILD` env flag (Task 4).
- **Modify:** `build/tests/verify_seo_pass.js` — make the `dateModified` assertion determinism-safe (Task 2).
- **Modify:** `build/package.json` — add `verify:site` script (Task 4).
- **Modify:** `.github/workflows/static.yml` — hashed install + pip cache (Task 1); `fetch-depth: 0` (Task 2); Node setup + Playwright cache + the verify gate step (Task 5).

---

### Task 1: Pin the build dependency by hash

**Files:**
- Create: `build/requirements.txt`
- Modify: `.github/workflows/static.yml` (the "Set up Python" and "Install build dependencies" steps)

- [ ] **Step 1: Write the failing test**

Create the requirements file with the exact pin + hash (computed from `markdown==3.10.2`, the version this repo builds with):

`build/requirements.txt`:
```
# Pinned + hashed so CI builds are reproducible and supply-chain-closed.
# markdown 3.10.2 has no runtime dependencies, so a single hash satisfies
# pip's --require-hashes mode. Regenerate with:
#   pip download markdown==<v> --no-deps -d /tmp/h && pip hash /tmp/h/*.whl
markdown==3.10.2 --hash=sha256:e91464b71ae3ee7afd3017d9f358ef0baf158fd9a298db92f1d4761133824c36
```

- [ ] **Step 2: Run the install to verify the hash resolves**

Run: `pip install --require-hashes -r build/requirements.txt && python3 -c "import markdown; print(markdown.__version__)"`
Expected: install exits 0 (prints "Requirement already satisfied" or installs markdown-3.10.2), then prints `3.10.2`. If the hash were wrong, pip would abort with `THESE PACKAGES DO NOT MATCH THE HASHES`.

- [ ] **Step 3: Point the workflow at the hashed requirements file + enable pip cache**

In `.github/workflows/static.yml`, change the "Set up Python" and "Install build dependencies" steps.

Before:
```yaml
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install build dependencies
        run: pip install markdown
```
After:
```yaml
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: build/requirements.txt

      - name: Install build dependencies
        run: pip install --require-hashes -r build/requirements.txt
```

- [ ] **Step 4: Verify the build still runs with only the pinned dep**

Run: `python3 build/build_spa.py`
Expected: exits 0, prints the usual `Wrote _site/index.html (...)` … `Copied static files from build/static/` lines.

- [ ] **Step 5: Commit**

```bash
git add build/requirements.txt .github/workflows/static.yml
git commit -m "build: pin markdown by hash; reproducible CI install"
```

---

### Task 2: Deterministic build date

The build stamps sitemap `lastmod`, JSON-LD `dateModified`, and the footer from `datetime.now()`, so every build on a new calendar day churns the output and advertises a freshness that didn't happen. Derive the date from content instead. **Note:** `verify_seo_pass.js` currently asserts `dateModified === today` (wall-clock), which this change would break — so this task updates that assertion to stay internally consistent.

**Files:**
- Modify: `build/build_spa.py` (imports near `:14`; new helper after the path constants ~`:30`; call sites `:1618`, `:1832`, `:2363`)
- Modify: `build/tests/verify_seo_pass.js:79-82`
- Modify: `.github/workflows/static.yml` (Checkout step — `fetch-depth: 0`)

- [ ] **Step 1: Write the failing test**

The fix must honor `SOURCE_DATE_EPOCH`. `1700000000` is `2023-11-14` UTC. Today the build ignores the env var, so this check fails.

Run:
```bash
SOURCE_DATE_EPOCH=1700000000 python3 build/build_spa.py >/dev/null && grep -q '<lastmod>2023-11-14</lastmod>' _site/sitemap.xml && echo TESTPASS || echo TESTFAIL
```
Expected now: `TESTFAIL` (sitemap shows the real current date, not 2023-11-14).

- [ ] **Step 2: Add the imports and the helper**

In `build/build_spa.py`, add `os` and `subprocess` to the stdlib imports (the block around `:10-16` that has `import re`, `import sys`, …):
```python
import os
import subprocess
```

Then add this helper immediately after the path constants (`TEMPLATE_PATH = HERE / "spa_template.html"`, ~`:30`):
```python
def _content_date() -> datetime:
    """Deterministic build timestamp for sitemap lastmod / JSON-LD dateModified.

    Resolution order: SOURCE_DATE_EPOCH env override -> the source file's last
    git commit date -> the source file's mtime. Never datetime.now(), so an
    unchanged source rebuilds byte-identically and lastmod reflects the last
    *content* edit rather than when CI happened to run.
    """
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc)
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(SOURCE)],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return datetime.fromisoformat(out).astimezone(timezone.utc)
    except Exception:
        pass
    return datetime.fromtimestamp(SOURCE.stat().st_mtime, tz=timezone.utc)
```

- [ ] **Step 3: Replace the three `datetime.now()` call sites**

`build/build_spa.py:1618` (in `render_sitemap`):
```python
    today = _content_date().strftime("%Y-%m-%d")
```
`build/build_spa.py:1832` (in `render_chapter_schema`):
```python
    today = _content_date().strftime("%Y-%m-%d")
```
`build/build_spa.py:2363` (the landing/read block — replace the `_now_utc` assignment):
```python
    _now_utc = _content_date()
```
(Leave the two following lines `date_modified = _now_utc.strftime(...)` and `date_modified_human = _now_utc.strftime(...)` unchanged.)

- [ ] **Step 4: Make the verifier's dateModified assertion determinism-safe**

In `build/tests/verify_seo_pass.js`, replace lines 79-82:

Before:
```javascript
          // dateModified is today
          const today = new Date().toISOString().slice(0, 10);
          if (book && book.dateModified !== today) fail(`Book.dateModified=${book.dateModified}, expected ${today}`);
          else ok(`Book.dateModified is today`);
```
After:
```javascript
          // dateModified is deterministic (content date) and must match sitemap <lastmod>.
          const sm = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
          const lastmod = (sm.match(/<lastmod>([0-9-]+)<\/lastmod>/) || [])[1];
          if (!book || book.dateModified !== lastmod) fail(`Book.dateModified=${book && book.dateModified}, expected sitemap lastmod ${lastmod}`);
          else ok(`Book.dateModified matches sitemap lastmod (${lastmod})`);
```
(`repoRoot` is declared later at `:147` inside the same `main()`; move the `const repoRoot = path.resolve(__dirname, '..', '..');` declaration up to just below `async function main() {` at `:28`, and delete the duplicate at `:147`, so it's in scope here. Verify with the run in Step 6.)

- [ ] **Step 5: Set `fetch-depth: 0` so CI can read the git date**

`actions/checkout` defaults to a shallow clone, where `git log` returns the CI commit's date, not the content's. In `.github/workflows/static.yml`, change the Checkout step.

Before:
```yaml
      - name: Checkout
        uses: actions/checkout@v4
```
After:
```yaml
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
```

- [ ] **Step 6: Run the determinism test + the verifier**

Run:
```bash
SOURCE_DATE_EPOCH=1700000000 python3 build/build_spa.py >/dev/null && grep -q '<lastmod>2023-11-14</lastmod>' _site/sitemap.xml && echo TESTPASS || echo TESTFAIL
python3 build/build_spa.py >/dev/null && cp _site/sitemap.xml /tmp/sm1 && python3 build/build_spa.py >/dev/null && diff -q /tmp/sm1 _site/sitemap.xml && echo DETERMINISTIC
cd build && node tests/verify_seo_pass.js 2>&1 | tail -3; cd ..
```
Expected: `TESTPASS`; then `DETERMINISTIC` (two consecutive builds produce an identical sitemap); then the verifier ends with `Verification PASSED.` (the `dateModified` line now reads `Book.dateModified matches sitemap lastmod (...)`).

- [ ] **Step 7: Commit**

```bash
git add build/build_spa.py build/tests/verify_seo_pass.js .github/workflows/static.yml
git commit -m "build: derive build date from content (SOURCE_DATE_EPOCH/git/mtime), not now()"
```

---

### Task 3: Build hygiene — import guard, expected-count constant, stale comment

**Files:**
- Modify: `build/build_spa.py` (import `:18`; the per-section comment `:2399`; add a module-level `EXPECTED_PAGE_COUNT`)

- [ ] **Step 1: Add a friendly import guard**

`build/build_spa.py:18` is `import markdown`. Replace it with:
```python
try:
    import markdown
except ImportError:
    sys.exit("build_spa.py: missing dependency. Run: pip install -r build/requirements.txt")
```
(`sys` is already imported.)

- [ ] **Step 2: Add `EXPECTED_PAGE_COUNT` as the single source of truth for the page count**

Immediately after the `SECTION_SLUGS` dict + its dedupe sanity check (the block ending with `_seen.add(_v)`, ~`:62`), add:
```python
# Single source of truth for how many per-section pages the build must emit.
# Used by the build's own print + the CI smoke check.
EXPECTED_PAGE_COUNT = len(SECTION_SLUGS)  # 19 as of this pass
```

- [ ] **Step 3: Fix the stale "18 total" comment and assert the count**

`build/build_spa.py:2399-2401` currently reads:
```python
    # Per-section pages (18 total: foreword, prologue, 10 chapters, closing,
    # acknowledgments, about, 3 appendices). Each gets a "you are here" mark
    # on its sidebar TOC entry.
```
Replace with:
```python
    # Per-section pages (EXPECTED_PAGE_COUNT total). Each gets a "you are here"
    # mark on its sidebar TOC entry.
    assert len(sections) == EXPECTED_PAGE_COUNT, (
        f"emitted {len(sections)} sections, expected {EXPECTED_PAGE_COUNT}")
```

- [ ] **Step 4: Verify the build still succeeds and the count is right**

Run: `python3 build/build_spa.py 2>&1 | grep 'per-section pages'`
Expected: `Wrote 19 per-section pages` (no assertion error).

Run (guard works): `python3 -c "import sys; sys.modules['markdown']=None" 2>/dev/null; echo "guard is a runtime path — exercised only when markdown is absent"`
Expected: informational; the guard fires only on a real missing dep — no separate test needed beyond Step 4 building cleanly.

- [ ] **Step 5: Commit**

```bash
git add build/build_spa.py
git commit -m "build: import guard, EXPECTED_PAGE_COUNT assert, fix stale 18/19 comment"
```

---

### Task 4: Wire the real verifier with a no-rebuild mode

`npm run verify` runs `verify_feedback_pass.js` (landing page only, rebuilds). The script that actually serves and asserts against `_site/` is `verify_seo_pass.js`, but it is **unwired**. Wire it as `verify:site`, and add a `SITE_NO_REBUILD` flag so CI verifies the exact bytes it just built instead of rebuilding.

**Files:**
- Modify: `build/tests/lib/build_and_serve.js:39-41`
- Modify: `build/package.json` (scripts)

- [ ] **Step 1: Write the failing test**

The `_site/` build clears its output dir on every run (`reset_site_dir()` rmtrees `_site/`), so a SENTINEL file surviving a verify run proves it did NOT rebuild. First add the script + a fresh build with a sentinel:

Run:
```bash
python3 build/build_spa.py >/dev/null && touch _site/SENTINEL
cd build && SITE_NO_REBUILD=1 node tests/verify_seo_pass.js >/dev/null 2>&1; cd ..
test -f _site/SENTINEL && echo "NO_REBUILD_OK" || echo "REBUILT (sentinel gone)"
```
Expected now: `REBUILT (sentinel gone)` — `buildAndServe` always rebuilds today, deleting the sentinel.

- [ ] **Step 2: Add the `SITE_NO_REBUILD` guard**

In `build/tests/lib/build_and_serve.js`, change `buildAndServe` (lines 39-41).

Before:
```javascript
async function buildAndServe(serveDir = '.') {
  const repoRoot = path.resolve(__dirname, '..', '..', '..');
  execFileSync('python3', ['build/build_spa.py'], { cwd: repoRoot, stdio: 'inherit' });
```
After:
```javascript
async function buildAndServe(serveDir = '.') {
  const repoRoot = path.resolve(__dirname, '..', '..', '..');
  // CI builds once (the workflow's Build step) then verifies those exact bytes.
  // Set SITE_NO_REBUILD=1 to serve the existing _site/ without rebuilding.
  if (!process.env.SITE_NO_REBUILD) {
    execFileSync('python3', ['build/build_spa.py'], { cwd: repoRoot, stdio: 'inherit' });
  }
```

- [ ] **Step 3: Add the `verify:site` npm script**

In `build/package.json`, change the `scripts` block.

Before:
```json
  "scripts": {
    "verify": "node tests/verify_feedback_pass.js"
  },
```
After:
```json
  "scripts": {
    "verify": "node tests/verify_feedback_pass.js",
    "verify:site": "node tests/verify_seo_pass.js"
  },
```

- [ ] **Step 4: Run the test to verify it now passes**

Run:
```bash
python3 build/build_spa.py >/dev/null && touch _site/SENTINEL
cd build && SITE_NO_REBUILD=1 npm run verify:site >/dev/null 2>&1; cd ..
test -f _site/SENTINEL && echo "NO_REBUILD_OK" || echo "REBUILT (sentinel gone)"
rm -f _site/SENTINEL
```
Expected: `NO_REBUILD_OK`.

Then confirm the full verifier is green when allowed to rebuild:
Run: `cd build && npm run verify:site 2>&1 | tail -2; cd ..`
Expected: ends with `Verification PASSED.`

- [ ] **Step 5: Commit**

```bash
git add build/tests/lib/build_and_serve.js build/package.json
git commit -m "test: wire verify:site (the _site/ asserter) with SITE_NO_REBUILD mode"
```

---

### Task 5: CI build-output gate before deploy

Add a step between "Build SPA from source" and "Setup Pages" that smoke-checks the artifact and runs `verify:site` against it. Today the workflow goes Build → Deploy with nothing in between, so a broken `_site/` ships straight to the apex.

**Files:**
- Create: `build/tests/smoke_check.sh`
- Modify: `.github/workflows/static.yml` (add Node setup, Playwright cache, and the verify gate step)

- [ ] **Step 1: Write the smoke check (the test) and a failing run**

`build/tests/smoke_check.sh`:
```bash
#!/usr/bin/env bash
# Structural smoke check for the built _site/ before deploy. Exits non-zero if a
# load-bearing artifact is missing, the landing page is suspiciously small, or
# far too few pages were emitted — any of which means a silently-broken build.
set -euo pipefail

SITE="${1:-_site}"
fail() { echo "SMOKE FAIL: $*" >&2; exit 1; }

for f in index.html .nojekyll CNAME 404.html sitemap.xml robots.txt llms.txt llms-full.txt read/index.html; do
  [ -f "$SITE/$f" ] || fail "missing $SITE/$f"
done

size=$(wc -c < "$SITE/index.html")
[ "$size" -ge 51200 ] || fail "index.html only ${size} bytes (< 50 KB) — build likely broken"

# 19 sections + /read/ + redirect stub(s) => 20+ sub-page index.html files.
pages=$(find "$SITE" -mindepth 2 -maxdepth 2 -name index.html | wc -l)
[ "$pages" -ge 20 ] || fail "only ${pages} sub-page index.html files (< 20) — sections missing"

echo "SMOKE OK: ${pages} sub-pages, landing ${size} bytes, all required files present"
```

Make it executable and prove it passes on a good build and fails on a broken one:
```bash
chmod +x build/tests/smoke_check.sh
python3 build/build_spa.py >/dev/null && bash build/tests/smoke_check.sh
# Negative control: a missing file must fail the check.
bash build/tests/smoke_check.sh /tmp/nonexistent-site || echo "CORRECTLY FAILED on missing site"
```
Expected: `SMOKE OK: ...` on the real `_site/`, then `CORRECTLY FAILED on missing site`.

- [ ] **Step 2: Add Node setup + Playwright cache + the verify gate to the workflow**

In `.github/workflows/static.yml`, insert these steps **between** the existing "Build SPA from source" step and the "Setup Pages" step.

Before:
```yaml
      - name: Build SPA from source
        run: python3 build/build_spa.py

      - name: Setup Pages
        uses: actions/configure-pages@v5
```
After:
```yaml
      - name: Build SPA from source
        run: python3 build/build_spa.py

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: build/package-lock.json

      - name: Cache Playwright browsers
        uses: actions/cache@v4
        with:
          path: ~/.cache/ms-playwright
          key: playwright-${{ hashFiles('build/package-lock.json') }}

      - name: Verify built site (gate)
        run: |
          bash build/tests/smoke_check.sh _site
          cd build
          npm ci
          npx playwright install --with-deps chromium
          SITE_NO_REBUILD=1 npm run verify:site

      - name: Setup Pages
        uses: actions/configure-pages@v5
```

- [ ] **Step 3: Sanity-check the workflow YAML parses**

Run: `python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/static.yml')); print('YAML OK')"`
Expected: `YAML OK`. (If PyYAML is absent, run `pip install pyyaml` first — dev-only, not added to `requirements.txt`.)

- [ ] **Step 4: Locally simulate the gate against the built site**

Run:
```bash
python3 build/build_spa.py >/dev/null
bash build/tests/smoke_check.sh _site
cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..
```
Expected: `SMOKE OK: ...` then `Verification PASSED.`

- [ ] **Step 5: Commit**

```bash
git add build/tests/smoke_check.sh .github/workflows/static.yml
git commit -m "ci: gate deploy on smoke check + verify:site against the built _site/"
```

---

## Self-Review

**Spec coverage (Workstream G):**
- G1 (CI gate + wire `verify_seo_pass.js` + no-rebuild + dir-count + Playwright cache/pin) → Tasks 4 + 5. ✅ (Playwright version pin: `package.json` already carries `playwright` under devDeps; `npm ci` honors `package-lock.json`. The cache key is the lockfile hash — pinned transitively. If a stricter exact pin is wanted, change `^1.60.0`→`1.60.0` in `build/package.json`; noted, not required.)
- G2 (hashed `requirements.txt` + `--require-hashes` + pip cache) → Task 1. ✅
- G3 (content-derived date + `fetch-depth: 0`) → Task 2, including the verifier-assertion fix the determinism change forces. ✅
- G4 (import guard + section-count assert + stale comment) → Task 3. ✅

**Placeholder scan:** No TBD/TODO. The one external value (the wheel hash) is concrete: `sha256:e91464b71ae3ee7afd3017d9f358ef0baf158fd9a298db92f1d4761133824c36`. Regeneration command is documented in the file comment for future version bumps.

**Type/name consistency:** `_content_date()` defined once (Task 2) and called at all three sites; returns `datetime`, callers use `.strftime(...)`. `EXPECTED_PAGE_COUNT` defined in Task 3, used in the same task's assert + referenced by the smoke check's `>= 20` fan-out heuristic (the smoke check counts files rather than importing the Python constant — intentional, since bash can't read it). `SITE_NO_REBUILD` spelled identically in `build_and_serve.js` and both Task 4/5 runs and the workflow. `verify:site` script name consistent across Task 4 + Task 5 + the workflow.

**Cross-dependency captured:** Task 2 updates `verify_seo_pass.js:79-82` because the content-date change would otherwise break its `dateModified === today` assertion — the kind of break that would only surface at CI time.

**Out of scope (later plans):** the sitemap `=== 21` assertions at `verify_seo_pass.js:299` AND `:817` (two of them) belong to Plan 2's `/read/` noindex change (decision #5) — flagged here so they aren't forgotten: dropping `/read/` makes both `20`.

---

## Execution Handoff

This is Plan 1 of 4 for the review pass. Plans 2–4 (site/template SEO+perf+GEO; manuscript corrections+structure; visible FAQ) will be written next, each in the same TDD style, and each depends on the `verify:site` harness this plan wires.
