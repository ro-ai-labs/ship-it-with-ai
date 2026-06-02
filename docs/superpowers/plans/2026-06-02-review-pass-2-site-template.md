# Review Pass — Plan 2: Site & Template (SEO / Perf / GEO) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the generated site's indexing, performance, and answer-engine surfaces by editing the generator (`build/build_spa.py`) and template (`build/spa_template.html`) — without touching the manuscript.

**Architecture:** Nine surgical changes: noindex the duplicate `/read/` page; make `og:type`/`og:url` per-page; kill the dark-mode flash; demote a UI heading out of the SEO outline; size touch targets; serve a smaller responsive cover; externalize the search index; and enrich the AI-discovery surfaces (`llms.txt`, `<head>` markdown links, keywords). This is **Plan 2 of 4** (spec Workstreams **D, E, F-build**; spec: `docs/superpowers/specs/2026-06-02-review-pass-design.md`). It depends on **Plan 1** having wired `npm run verify:site` (the `_site/`-serving verifier). Manuscript anchored question-headings (F1) and the visible FAQ (F2/D2) are Plans 3–4.

**Tech Stack:** Python 3.12 generator, HTML/CSS/vanilla-JS template, Playwright verifier (`build/tests/verify_seo_pass.js`), PIL (`build/cover_to_webp.py`).

**Conventions:** run from repo root; commit prefixes `build:`/`fix:`/`perf:`/`test:`; **no Claude attribution**. After every task: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..` must end `Verification PASSED.`

**Scope notes:** D2 (FAQPage off `/read/`) is mooted by Task 1's noindex and is finished cleanly in Plan 4's FAQ refactor. F6 (chapter og:description) is already satisfied — `render_chapter` sets `PAGE_DESCRIPTION` from `_section_description`, which feeds `og:description` — so no task is needed; only `/read/`'s og:url is wrong (Task 2).

---

### Task 1: noindex `/read/` and drop it from the sitemap (D1)

The full book exists at both `/read/` and the 19 per-section pages — a duplicate-content race. `/read/` stays for humans/bookmarks but leaves the index.

**Files:**
- Modify: `build/build_spa.py` — `render_read` (`:2052`), `render_sitemap` (`:1623`)
- Modify: `build/tests/verify_seo_pass.js` — sitemap asserts (`:299`, `:817`), add a noindex check

- [ ] **Step 1: Write the failing assertions in the verifier**

In `build/tests/verify_seo_pass.js`, change **both** sitemap-count assertions from 21 to 20 (dropping `/read/`):

Line 299 — before: `if (urlCount !== 21) fail(\`sitemap has ${urlCount} URLs, expected 21\`);` / after-text `else ok(\`sitemap has 21 URLs (landing + /read/ + 19 sections)\`);` →
```javascript
      if (urlCount !== 20) fail(`sitemap has ${urlCount} URLs, expected 20`);
      else ok(`sitemap has 20 URLs (landing + 19 sections; /read/ excluded)`);
```
Line 817 (in the changelog block) — before `if (urlCount !== 21) ...` / `else ok('sitemap has 21 URLs (was 20)');` →
```javascript
      if (urlCount !== 20) fail(`sitemap has ${urlCount} URLs, expected 20`);
      else ok('sitemap has 20 URLs (/read/ excluded for noindex)');
```
Then add a new assertion block immediately after the existing `/read/` canonical block (after line 220, the `await ctx.close();` that ends the "/read/ has … chapter anchors" block):
```javascript
    // /read/ is noindex (kept for humans, out of the index to avoid duplicate
    // content vs the 19 per-section pages) and absent from the sitemap.
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'read', 'index.html'), 'utf8');
      const robots = [...html.matchAll(/<meta name="robots" content="([^"]+)"/g)].map(m => m[1]);
      if (!robots.some(r => /noindex/.test(r))) fail(`/read/ missing noindex robots meta (got: ${robots})`);
      else ok('/read/ emits noindex robots meta');
      const sitemap = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
      if (/ship-it-with\.ai\/read\//.test(sitemap)) fail('/read/ still listed in sitemap');
      else ok('/read/ excluded from sitemap');
    }
```

- [ ] **Step 2: Run the verifier to watch it fail**

Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | grep -E 'FAIL|read'; cd ..`
Expected: FAILs — `/read/` has no noindex meta and is still in the sitemap (and the count is 21, not 20).

- [ ] **Step 3: Emit noindex on `/read/`**

`build/build_spa.py`, in `render_read`, change the `HEAD_EXTRA` value (`:2052`):

Before: `"HEAD_EXTRA": "",`
After:
```python
        "HEAD_EXTRA": '<meta name="robots" content="noindex, follow">',
```
(The template's default `index, follow` meta is earlier in `<head>`; a later meta in `{{HEAD_EXTRA}}` overrides it by document order — the same mechanism `render_404` already relies on.)

- [ ] **Step 4: Drop `/read/` from the sitemap**

`build/build_spa.py`, in `render_sitemap` (`:1623`):

Before: `urls = ["https://ship-it-with.ai/", "https://ship-it-with.ai/read/"]`
After:
```python
    # /read/ is noindex (duplicate of the per-section pages) — keep it out of the sitemap.
    urls = ["https://ship-it-with.ai/"]
```

- [ ] **Step 5: Run the verifier — now green**

Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.` (including the new `/read/ emits noindex` and `/read/ excluded from sitemap` lines).

- [ ] **Step 6: Commit**

```bash
git add build/build_spa.py build/tests/verify_seo_pass.js
git commit -m "fix(seo): noindex /read/ and drop it from sitemap (kills duplicate content)"
```

---

### Task 2: per-page `og:type`, and correct `/read/` `og:url` (D5 + D3)

`og:type` is a hardcoded `article` shared by every page; the homepage should be `website`. And `/read/`'s `og:url`/`twitter:url` resolve to `/` (canonical stays `/`, but the share URL should be `/read/`). Introduce two placeholders.

**Files:**
- Modify: `build/spa_template.html` (`:14`, `:17`, `:32`)
- Modify: `build/build_spa.py` — the four render dicts: `render_chapter` (`:1984`), `render_landing` (`:2022`), `render_read` (`:2047`), `render_404` (`:2123`)
- Modify: `build/tests/verify_seo_pass.js` — add og assertions

- [ ] **Step 1: Add the placeholders to the template**

`build/spa_template.html:14`, before: `<meta property="og:type" content="article" />` →
```html
  <meta property="og:type" content="{{OG_TYPE}}" />
```
`build/spa_template.html:17`, before: `<meta property="og:url" content="{{PAGE_URL}}" />` →
```html
  <meta property="og:url" content="{{OG_URL}}" />
```
`build/spa_template.html:32`, before: `<meta name="twitter:url" content="{{PAGE_URL}}" />` →
```html
  <meta name="twitter:url" content="{{OG_URL}}" />
```
(`{{PAGE_URL}}` still drives the canonical at `:12` — unchanged.)

- [ ] **Step 2: Set both keys in all four render dicts**

In each `substitutions` dict, add the two keys next to `"PAGE_URL"`:

`render_chapter` (`build/build_spa.py:1983`, after `"PAGE_URL": page_url,`):
```python
        "OG_TYPE": "article",
        "OG_URL": page_url,
```
`render_landing` (`:2021`, after `"PAGE_URL": "https://ship-it-with.ai/",`):
```python
        "OG_TYPE": "website",
        "OG_URL": "https://ship-it-with.ai/",
```
`render_read` (`:2046`, after `"PAGE_URL": "https://ship-it-with.ai/",  # alternate format of /`):
```python
        "OG_TYPE": "article",
        "OG_URL": "https://ship-it-with.ai/read/",
```
`render_404` (`:2122`, after `"PAGE_URL": "https://ship-it-with.ai/404.html",`):
```python
        "OG_TYPE": "website",
        "OG_URL": "https://ship-it-with.ai/404.html",
```

- [ ] **Step 3: Add assertions to the verifier**

In `build/tests/verify_seo_pass.js`, append inside the file-system assertions area (e.g. after the new `/read/` block from Task 1):
```javascript
    // og:type is website on landing, article on chapters; /read/ og:url is /read/.
    {
      const land = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      if (!/og:type" content="website"/.test(land)) fail('landing og:type should be website');
      else ok('landing og:type=website');
      const ch = fs.readFileSync(path.join(repoRoot, '_site', 'chapter-1-primitives', 'index.html'), 'utf8');
      if (!/og:type" content="article"/.test(ch)) fail('chapter og:type should be article');
      else ok('chapter og:type=article');
      const read = fs.readFileSync(path.join(repoRoot, '_site', 'read', 'index.html'), 'utf8');
      if (!/og:url" content="https:\/\/ship-it-with\.ai\/read\/"/.test(read)) fail('/read/ og:url should be /read/');
      else ok('/read/ og:url=/read/');
      if (!/rel="canonical" href="https:\/\/ship-it-with\.ai\/"/.test(read)) fail('/read/ canonical should stay /');
      else ok('/read/ canonical stays /');
    }
```

- [ ] **Step 4: Build + verify**

Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.` (`render_template_with_placeholders` raises if any render dict missed `OG_TYPE`/`OG_URL`, so a missed call-site fails the build loudly.)

- [ ] **Step 5: Commit**

```bash
git add build/spa_template.html build/build_spa.py build/tests/verify_seo_pass.js
git commit -m "fix(seo): per-page og:type (website/article) and correct /read/ og:url"
```

---

### Task 3: kill the dark-mode flash (E1)

Theme is applied by a script at `</body>`, so dark-preference users see a light→dark flash every load. Set `data-theme` in a tiny blocking head script before the CSS paints.

**Files:**
- Modify: `build/spa_template.html` (insert after `{{HEAD_EXTRA}}` `:36`, before `<style>` `:38`)

- [ ] **Step 1: Insert the head snippet**

After the `{{HEAD_EXTRA}}` line (`:36`) and before `<style>`, add:
```html
  <script>try{var t=localStorage.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t);}catch(e){}</script>
```
(Idempotent with the body-end logic at `:2131`, which recomputes the same value from `localStorage.theme` / `prefers-color-scheme`. The localStorage key is `theme`, matching the body-end code and the verifier's `setTheme`.)

- [ ] **Step 2: Add an assertion**

In `build/tests/verify_seo_pass.js`, add near the other landing checks:
```javascript
    // Head theme-init runs before paint (no dark-mode FOUC). Must appear before <style>.
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      const initIdx = html.indexOf("setAttribute('data-theme'");
      const styleIdx = html.indexOf('<style>');
      if (initIdx === -1 || initIdx > styleIdx) fail('head theme-init missing or after <style> (FOUC)');
      else ok('head theme-init present before <style>');
    }
```

- [ ] **Step 3: Build + verify**

Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.`

- [ ] **Step 4: Commit**

```bash
git add build/spa_template.html build/tests/verify_seo_pass.js
git commit -m "perf: set theme in <head> before paint to remove dark-mode FOUC"
```

---

### Task 4: demote the keyboard-overlay heading out of the SEO outline (D4)

The most prominent secondary heading on section pages is UI chrome (`<h2 id="kbdOverlayTitle">Keyboard shortcuts</h2>`). Make it a non-heading; it still labels the dialog via `aria-labelledby`.

**Files:**
- Modify: `build/spa_template.html:2096`

- [ ] **Step 1: Change the element**

Before: `        <h2 class="kbd-card-title" id="kbdOverlayTitle">Keyboard shortcuts</h2>`
After:
```html
        <p class="kbd-card-title" id="kbdOverlayTitle">Keyboard shortcuts</p>
```
(The `aria-labelledby="kbdOverlayTitle"` on the dialog at `:2092` still resolves; `.kbd-card-title` CSS keeps the visual styling.)

- [ ] **Step 2: Add an assertion**

In `build/tests/verify_seo_pass.js`:
```javascript
    // The keyboard-overlay title is no longer an <h2> (kept out of the SEO outline).
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'chapter-1-primitives', 'index.html'), 'utf8');
      if (/<h2[^>]*id="kbdOverlayTitle"/.test(html)) fail('kbdOverlayTitle is still an <h2>');
      else ok('kbdOverlayTitle demoted out of heading outline');
    }
```

- [ ] **Step 3: Build + verify**

Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.`

- [ ] **Step 4: Commit**

```bash
git add build/spa_template.html build/tests/verify_seo_pass.js
git commit -m "fix(seo): demote keyboard-overlay title from <h2> to labelled <p>"
```

---

### Task 5: size touch targets for mobile (E4)

`.topbar-btn` is ~36px tall; Lighthouse wants ≥44px tap targets on touch.

**Files:**
- Modify: `build/spa_template.html` (after the `.topbar-btn.size-btn .large-a` rule, `:233`)

- [ ] **Step 1: Add a touch-only rule**

After line 233 (`.topbar-btn.size-btn .large-a { font-size: 16px; }`), add:
```css
    @media (max-width: 720px) {
      .topbar-btn { min-height: 44px; min-width: 44px; }
    }
```

- [ ] **Step 2: Build + verify it didn't regress layout**

Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.` (the verifier checks no horizontal overflow at the 375px mobile viewport — confirms the larger targets don't break the topbar).

- [ ] **Step 3: Commit**

```bash
git add build/spa_template.html
git commit -m "fix(a11y): 44px minimum touch targets for topbar buttons on mobile"
```

---

### Task 6: serve a smaller, responsive cover (E2)

The 206 KB JPEG is always shipped; the 139 KB webp is built but unreferenced; the image displays in a ≤720px column. Serve webp with a 720px variant.

**Files:**
- Modify: `build/cover_to_webp.py` (emit both sizes into `build/static/`)
- Modify: `build/build_spa.py:1376` and `:1404` (the two identical `<img>` cover blocks)

- [ ] **Step 1: Make the cover tool emit full + 720px webp into `build/static/`**

In `build/cover_to_webp.py`, replace the output section (`OUTPUT = REPO_ROOT / "cover.webp"` at `:18`, and the single `img.save(...)` at `:41`). New `:18`:
```python
STATIC_DIR = HERE / "static"
```
Replace the save + print (lines 40-44) with:
```python
    base = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    for name, w, h in [("cover.webp", TARGET_W, TARGET_H), ("cover-720.webp", 720, 378)]:
        out = STATIC_DIR / name
        base.resize((w, h), Image.Resampling.LANCZOS).save(out, format="WEBP", quality=82, method=6)
        print(f"wrote {out.relative_to(REPO_ROOT)} ({out.stat().st_size / 1024:.1f} KB, {w}x{h})")
    return 0
```
(720×378 keeps the 1200:630 ratio. Delete the now-unused `OUTPUT` line and the old single save/print.)

- [ ] **Step 2: Generate the assets**

Run: `python3 build/cover_to_webp.py`
Expected: prints `wrote static/cover.webp (...)` and `wrote static/cover-720.webp (...)`. Confirm: `ls build/static/cover*.webp` shows both files.

- [ ] **Step 3: Replace both `<img>` cover blocks with `<picture>`**

In `build/build_spa.py`, both `:1376` and `:1404` are the identical line:
`<img src="/cover.jpg" alt="Ship It With AI - A Manual for Shipping Software with AI Agents, by {AUTHOR}" width="1200" height="630" loading="lazy" decoding="async" />`

Replace **both occurrences** with:
```python
        <picture>
          <source type="image/webp" srcset="/cover-720.webp 720w, /cover.webp 1200w" sizes="(max-width: 760px) 100vw, 720px" />
          <img src="/cover.jpg" alt="Ship It With AI - A Manual for Shipping Software with AI Agents, by {AUTHOR}" width="1200" height="630" loading="lazy" decoding="async" />
        </picture>
```
(Use Edit with `replace_all: true` since the two blocks are byte-identical. `{AUTHOR}` is a `.format` field already present in these strings — keep it.)

- [ ] **Step 4: Build and confirm the variant deploys + markup is right**

Run:
```bash
python3 build/build_spa.py >/dev/null
test -f _site/cover-720.webp && echo "720 DEPLOYED" || echo "720 MISSING — add 'cover-720.webp' to copy_static's file list in build_spa.py"
grep -c '<source type="image/webp"' _site/index.html
```
Expected: `720 DEPLOYED`; grep count `>= 1`. (If `720 MISSING`: `copy_static()` uses an explicit allow-list — add `"cover-720.webp"` next to `"cover.webp"` there, rebuild, recheck.)

- [ ] **Step 5: Add an assertion + verify**

In `build/tests/verify_seo_pass.js`, extend the existing `cover.webp` file check area:
```javascript
    if (!exists('cover-720.webp')) fail('cover-720.webp missing'); else ok('cover-720.webp present');
    {
      const land = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      if (!/<source type="image\/webp" srcset="\/cover-720\.webp/.test(land)) fail('cover <picture>/<source> missing');
      else ok('cover served via <picture> with webp srcset');
    }
```
Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.`

- [ ] **Step 6: Commit**

```bash
git add build/cover_to_webp.py build/static/cover.webp build/static/cover-720.webp build/build_spa.py build/tests/verify_seo_pass.js
git commit -m "perf: serve cover via <picture> with a 720px webp variant"
```

---

### Task 7: externalize the search index, fetch on first open (E3)

The 17 KB search index is inlined into all 22 pages. Move it to a cacheable `/search-index.json`, fetched the first time the user opens search. **Keep the app JS and critical CSS inline** (per spec decision #9).

**Files:**
- Modify: `build/build_spa.py` — write `_site/search-index.json` (near the other `write_text` calls, ~`:2460`); stop inlining (set the `SEARCH_INDEX` substitution to `"[]"` so nothing large is embedded — see note)
- Modify: `build/spa_template.html` — the search-init JS (`:2330-2334`) + the trigger handler
- Modify: `build/tests/verify_seo_pass.js:444-455` (reads the inline index today)

- [ ] **Step 1: Write the index to a file and stop inlining it**

In `build/build_spa.py`, near the other `write_text` calls (after the `sitemap.xml` write, ~`:2460`), add:
```python
    (SITE_DIR / "search-index.json").write_text(search_json)
    print("Wrote _site/search-index.json")
```
Then make the inline index empty so the JSON isn't duplicated into 22 pages: change the `search_index=search_json` passed into the four render calls (`render_landing`, `render_read`, `render_chapter`, `render_404`) to `search_index="[]"`. (Simplest: at the build-orchestration site where `search_json` is computed (`:2346`), keep `search_json` for the file write, and pass the literal `"[]"` to the renderers. Concretely, add `inline_index = "[]"` after `:2346` and replace the `search_index=search_json` arguments in the four render call-sites with `search_index=inline_index`.)

- [ ] **Step 2: Lazy-fetch the index on first search open**

In `build/spa_template.html`, replace the index-init (`:2330-2334`):

Before:
```javascript
        const indexEl = document.getElementById('searchIndex');
        if (!overlay || !input || !results || !indexEl) return;

        let index = [];
        try { index = JSON.parse(indexEl.textContent || '[]'); } catch (err) { index = []; }
```
After:
```javascript
        if (!overlay || !input || !results) return;

        let index = [];
        let indexLoaded = false;
        let indexLoading = null;
        function ensureIndex() {
          if (indexLoaded) return Promise.resolve(index);
          if (!indexLoading) {
            indexLoading = fetch('/search-index.json')
              .then(r => (r.ok ? r.json() : []))
              .then(data => { index = data; indexLoaded = true; return index; })
              .catch(() => { index = []; indexLoaded = true; return index; });
          }
          return indexLoading;
        }
```
Then find the handler that opens the overlay (the `trigger` click / the function that shows `#searchOverlay`) and call `ensureIndex()` at its top so the JSON is fetched on first open. Search the template for where `searchOverlay` is shown (e.g. a `function openSearch()` or `trigger.addEventListener('click', …)` near `:2360+`) and add `ensureIndex();` as its first statement. (The `search(q)` function already returns `[]` when `index` is empty, so an open-then-type before the fetch resolves degrades gracefully; results populate once the input fires after load.)

- [ ] **Step 3: Update the verifier to read the external index**

In `build/tests/verify_seo_pass.js`, replace the search-index block (`:444-455`):

Before (reads inline `<script id="searchIndex">`):
```javascript
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      const m = html.match(/<script id="searchIndex" type="application\/json">(.*?)<\/script>/s);
      if (!m) fail('searchIndex JSON not found in landing');
      else {
        const entries = JSON.parse(m[1]);
        const withUrl = entries.filter(e => e.url).length;
        if (withUrl < entries.length / 2) fail(`search index: only ${withUrl}/${entries.length} entries have url`);
        else ok(`search index: ${withUrl}/${entries.length} entries have url field`);
      }
    }
```
After (reads `/search-index.json`, asserts it is NOT inlined):
```javascript
    {
      if (!exists('search-index.json')) fail('search-index.json not emitted');
      else {
        const entries = JSON.parse(fs.readFileSync(path.join(repoRoot, '_site', 'search-index.json'), 'utf8'));
        const withUrl = entries.filter(e => e.url).length;
        if (withUrl < entries.length / 2) fail(`search index: only ${withUrl}/${entries.length} entries have url`);
        else ok(`search-index.json: ${withUrl}/${entries.length} entries have url field`);
        const land = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
        const inline = (land.match(/<script id="searchIndex" type="application\/json">(.*?)<\/script>/s) || [])[1] || '';
        if (inline.length > 10) fail(`search index still inlined in landing (${inline.length} chars)`);
        else ok('search index not inlined into landing (externalized)');
      }
    }
```

- [ ] **Step 4: Build + verify + smoke the UI manually**

Run: `python3 build/build_spa.py >/dev/null && test -f _site/search-index.json && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.`
Manual smoke (optional but recommended): `cd build && SITE_NO_REBUILD=1 node -e "require('./tests/lib/build_and_serve').buildAndServe('_site').then(async({baseUrl,stop})=>{const {chromium}=require('playwright');const b=await chromium.launch();const p=await b.newContext().then(c=>c.newPage());await p.goto(baseUrl+'/');await p.click('#searchTrigger');await p.fill('#searchInput','primitive');await p.waitForTimeout(500);console.log('results:', await p.locator('.search-result').count());await b.close();stop();})"; cd ..` — Expected: `results:` a number `> 0` (index fetched on open, search works).

- [ ] **Step 5: Commit**

```bash
git add build/build_spa.py build/spa_template.html build/tests/verify_seo_pass.js
git commit -m "perf: externalize search index to /search-index.json, fetch on first open"
```

---

### Task 8: enrich `llms.txt` with descriptions + an Author section (F3)

`llms.txt` lists bare titles; the convention wants a one-line description per link, and an author signal helps answer engines attribute citations.

**Files:**
- Modify: `build/build_spa.py` — `render_llms_txt` (`:2177-2219`), reusing `_section_description`

- [ ] **Step 1: Append a description to each link and add `## Author`**

In `render_llms_txt`, change the two list-builder lines to append the section's existing one-line description, and add an Author block to the returned string.

Replace the `docs_lines.append(...)` (`:2195`) and `optional_lines.append(...)` (`:2200`) bodies:
```python
            docs_lines.append(f"- [{_llms_label(s)}]({base}/{s.slug}/): {_section_description(s)}")
```
```python
            optional_lines.append(f"- [{_llms_label(s)}]({base}/{s.slug}/): {_section_description(s)}")
```
(`_section_description(section)` already exists — it's what `render_chapter` uses for the per-page meta description, so each link gets a real one-liner with no new authoring.)

Then in the returned f-string (`:2206-2219`), add an Author section before the closing `"""`:
```python
## Author
- [Mihai Cvasnievschi](https://www.linkedin.com/in/mihaicvasnievschi/): author; 25+ years shipping software, now focused on agentic delivery.
"""
```

- [ ] **Step 2: Build + assert**

In `build/tests/verify_seo_pass.js`, extend the llms.txt block (near `:172`):
```javascript
    {
      const t = fs.readFileSync(path.join(repoRoot, '_site/llms.txt'), 'utf8');
      if (!/\/\): .+/.test(t)) fail('llms.txt links lack per-link descriptions');
      else ok('llms.txt links carry descriptions');
      if (!/## Author/.test(t)) fail('llms.txt missing ## Author section');
      else ok('llms.txt has ## Author section');
    }
```
Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.`

- [ ] **Step 3: Commit**

```bash
git add build/build_spa.py build/tests/verify_seo_pass.js
git commit -m "feat(geo): add per-link descriptions + Author section to llms.txt"
```

---

### Task 9: discoverable markdown corpus + trimmed keywords (F4 + F5)

Link the clean markdown corpus from `<head>` so answer engines find it, and trim the over-long keywords meta.

**Files:**
- Modify: `build/spa_template.html` (`<head>`, after `:32`; keywords `:9`)

- [ ] **Step 1: Add `rel="alternate"` markdown links to the head**

After the `twitter:url` meta (now `:32`), add:
```html
  <link rel="alternate" type="text/markdown" href="https://ship-it-with.ai/llms-full.txt" title="Ship It With AI — full text (Markdown)" />
  <link rel="alternate" type="text/markdown" href="https://ship-it-with.ai/llms.txt" title="Ship It With AI — URL index (Markdown)" />
```

- [ ] **Step 2: Trim the keywords meta**

`build/spa_template.html:9`, replace the long keywords list with the durable head terms:
```html
  <meta name="keywords" content="agentic coding, AI coding agents, AGENTS.md, AI software delivery, agentic software engineering" />
```

- [ ] **Step 3: Assert + verify**

In `build/tests/verify_seo_pass.js`:
```javascript
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      if (!/rel="alternate" type="text\/markdown" href="https:\/\/ship-it-with\.ai\/llms-full\.txt"/.test(html))
        fail('head missing rel=alternate markdown link to llms-full.txt');
      else ok('head links the markdown corpus (llms-full.txt)');
    }
```
Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.`

- [ ] **Step 4: Commit**

```bash
git add build/spa_template.html build/tests/verify_seo_pass.js
git commit -m "feat(geo): link markdown corpus from <head>; trim keywords meta"
```

---

## Self-Review

**Spec coverage (D, E, F-build):** D1→T1; D2→mooted by T1, finished in Plan 4; D3→T2; D4→T4 (template half; manuscript anchored subheads are Plan 3 F1); D5→T2; E1→T3; E2→T6; E3→T7; E4→T5; F3→T8; F4/F5→T9; F6→already satisfied (noted in header). ✅

**Placeholder scan:** No TBD/TODO. Two tasks contain a located-by-search step by necessity — T7 Step 2 ("find the overlay-open handler and add `ensureIndex()`") and T6 Step 4's conditional `copy_static` allow-list fallback — both give the exact symbol to find, the exact code to add, and a test that fails if it's wrong. Everything else is literal before/after.

**Type/name consistency:** `{{OG_TYPE}}`/`{{OG_URL}}` added to the template and set in all four render dicts (the build's own `render_template_with_placeholders` fails loudly if any dict misses them — belt and suspenders). `ensureIndex`/`index`/`indexLoaded` consistent within T7. `cover-720.webp` spelled identically in the tool, the `<source srcset>`, the deploy check, and the verifier.

**Cross-dependencies captured:** T1 fixes *both* `===21` sitemap asserts (`:299` and `:817`) — the SEO reviewer only found `:299`. T7 updates the verifier's search-index block (`:444`) that reads the now-removed inline JSON. Each task adds its own verifier assertion, so regressions surface at `verify:site` time.

**Out of scope (later plans):** F1 anchored question-headings + the manuscript half of D4 → Plan 3. F2 visible FAQ + per-chapter FAQPage + the clean D2 FAQ removal → Plan 4.

---

## Execution Handoff

This is Plan 2 of 4. It is fully executable on its own once Plan 1 has wired `verify:site`. Plan 3 (manuscript: corrections, sweeps, structure, anchored question-headings) and Plan 4 (visible FAQ) follow.
