# Changelog + Last-updated Footer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a build-time "Last updated" timestamp to the footer of every page; add a new `/changelog/` section with the four most recent releases backfilled; link Changelog from the footer + from the "A note on dated claims" section.

**Architecture:** One feature branch (`changelog`) off `main`, one atomic commit. Reuses the existing `Section` parser + per-chapter rendering pipeline (no new infrastructure). New build-script placeholder `{{DATE_MODIFIED_HUMAN}}` runs in parallel with the existing ISO `{{DATE_MODIFIED}}`. Template footer split: `.footer-copy` gets the date stamp; `.footer-contact` gets the Changelog nav link (parallel to email/LinkedIn/ai-leaders.ro).

**Tech Stack:** Python 3.12 + `markdown` for the build. Vanilla HTML/CSS template. Playwright + Python `http.server` for verification (existing `build/tests/verify_seo_pass.js` extended in-place).

**Spec:** `docs/superpowers/specs/2026-05-27-changelog-and-last-updated-design.md` — read first; every task assumes its decisions.

**Branch:** `changelog`. Do NOT push to main during execution.

---

## File map

**Modify:**
- `source/Ship_It_With_AI.md` — insert new `## Changelog {#changelog}` section between Acknowledgments and About-the-author (back-matter housekeeping group); append new paragraph to "A note on dated claims" with the maintenance promise + changelog link.
- `build/build_spa.py` — new `{{DATE_MODIFIED_HUMAN}}` substitution; `SECTION_SLUGS` entry for changelog; parser regex + boundary regex update; TOC slot; reading-time suppression for `kind="changelog"`.
- `build/spa_template.html` — `.footer-copy` gets "Last updated" stamp; `.footer-contact` gets Changelog link.
- `build/tests/verify_seo_pass.js` — new assertions for the changelog page, footer date, footer link, dated-claims paragraph, hash redirect.

**Do NOT modify:**
- `.github/workflows/static.yml` — CI rebuilds + deploys; no changes needed.
- `.gitignore`, `build/static/*`, `build/cover_to_webp.py`, `build/tests/lib/build_and_serve.js` — unaffected.

---

## Workflow conventions

After every change, the rebuild + verify cycle is:

```bash
python3 build/build_spa.py
node build/tests/verify_seo_pass.js
```

Until Task 9 (verify assertions) lands, use plain `grep` against built `_site/` files for spot checks.

The source + build-script + template changes are inter-dependent (build fails between intermediate states). Implement Tasks 2-8 in any order locally, but only run the full build + verify after all source/build changes are in place. Single commit at the end (Task 10).

---

## Task 1: Create the feature branch

**Files:** none

- [ ] **Step 1: Confirm main is up to date**

```bash
git checkout main
git status
```

Expected: `nothing to commit, working tree clean` on `main`.

- [ ] **Step 2: Create and switch to the branch**

```bash
git checkout -b changelog
git status
```

Expected: `nothing to commit, working tree clean` on `changelog`.

---

## Task 2: Add `{{DATE_MODIFIED_HUMAN}}` substitution

**Why:** Existing `{{DATE_MODIFIED}}` renders ISO `YYYY-MM-DD` for JSON-LD. The footer wants human-readable `Month DD, YYYY` so the date isn't a wall of digits in user-facing copy.

**Files:**
- Modify: `build/build_spa.py` — wherever `{{DATE_MODIFIED}}` is currently substituted

- [ ] **Step 1: Locate the existing substitution**

```bash
grep -n "DATE_MODIFIED" build/build_spa.py
```

Expected: at least one place where `template.replace("{{DATE_MODIFIED}}", ...)` runs (added during the SEO pass). Note the line numbers.

- [ ] **Step 2: Add the parallel substitution**

In `build/build_spa.py`, alongside the existing `{{DATE_MODIFIED}}` substitution, add the human-readable variant. Concretely, find the line that looks like:

```python
template = template.replace("{{DATE_MODIFIED}}", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
```

Add immediately below (using the same `datetime.now(timezone.utc)` instant for consistency — extract to a local variable if it's not already):

```python
_now_utc = datetime.now(timezone.utc)
template = template.replace("{{DATE_MODIFIED}}", _now_utc.strftime("%Y-%m-%d"))
template = template.replace("{{DATE_MODIFIED_HUMAN}}", _now_utc.strftime("%B %d, %Y"))
```

(Replace any single-line existing substitution with the two-line block. If the existing call is inside a helper function that runs multiple times per build, ensure both placeholders use the SAME instant — same `_now_utc` variable.)

- [ ] **Step 3: Rebuild and confirm the placeholder is recognized**

```bash
python3 build/build_spa.py 2>&1 | tail -3
```

Expected: build completes. The new placeholder is harmless even though the template doesn't reference it yet — `.replace()` is a no-op on absent placeholders.

- [ ] **Step 4: Verify via a temporary test substitution**

```bash
python3 -c "
from datetime import datetime, timezone
print(datetime.now(timezone.utc).strftime('%B %d, %Y'))
"
```

Expected: a string like `May 27, 2026` (zero-padded day on Linux).

- [ ] **Step 5: Commit (deferred — bundled into Task 10's commit)**

---

## Task 3: Footer template updates

**Why:** The "Last updated" stamp goes in `.footer-copy`; the Changelog link goes in `.footer-contact` (parallel to other nav links). Two coordinated template edits.

**Files:**
- Modify: `build/spa_template.html` — `.footer-contact` block (~line 2040) and `.footer-copy` line (~line 2047)

- [ ] **Step 1: Locate the footer block**

```bash
grep -n "footer-contact\|footer-copy\|<footer class=\"article-footer\">" build/spa_template.html | head -10
```

Expected: the `<footer class="article-footer">` block around line 2039 with `.footer-contact` div (lines ~2040-2046) and `.footer-copy` `<p>` (line ~2047).

- [ ] **Step 2: Read the current footer block**

```bash
sed -n '2039,2050p' build/spa_template.html
```

Note the existing markup structure.

- [ ] **Step 3: Add Changelog link to `.footer-contact`**

Find the closing `</div>` of `.footer-contact`. Immediately before the closing tag, insert:

```html
        <span class="footer-sep">·</span>
        <a href="/changelog/">Changelog</a>
```

(The `<span class="footer-sep">` separator matches the existing pattern between email/LinkedIn/ai-leaders.ro entries.)

After the edit, the full `.footer-contact` should read (line breaks preserved for readability):

```html
        <div class="footer-contact">
          <a href="mailto:info@ship-it-with.ai">info@ship-it-with.ai</a>
          <span class="footer-sep">·</span>
          <a href="https://www.linkedin.com/in/mihaicvasnievschi/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
          <span class="footer-sep">·</span>
          <a href="https://ai-leaders.ro" target="_blank" rel="noopener noreferrer">ai-leaders.ro</a>
          <span class="footer-sep">·</span>
          <a href="/changelog/">Changelog</a>
        </div>
```

- [ ] **Step 4: Add Last-updated stamp to `.footer-copy`**

Find the `<p class="footer-copy">` line. Replace:

```html
<p class="footer-copy">© 2026 {{AUTHOR}} · Bucharest · All rights reserved</p>
```

with:

```html
<p class="footer-copy">© 2026 {{AUTHOR}} · Last updated {{DATE_MODIFIED_HUMAN}} · Bucharest · All rights reserved</p>
```

- [ ] **Step 5: Rebuild + spot-check the footer**

```bash
python3 build/build_spa.py
grep "Last updated" _site/index.html | head -3
grep 'href="/changelog/"' _site/index.html | head -3
```

Expected: the landing page renders `Last updated <Month DD, YYYY>` and contains a `Changelog` link in `.footer-contact`. The `/changelog/` link will 404 until Tasks 4-8 land — that's fine for this intermediate state.

- [ ] **Step 6: Commit (deferred — bundled into Task 10's commit)**

---

## Task 4: Section parser + SECTION_SLUGS + boundary regex for changelog

**Why:** The new `## Changelog {#changelog}` source heading needs to be parsed into a `Section` object with the right kind and slug. The parser, SECTION_SLUGS table, and boundary regex must all agree.

**Files:**
- Modify: `build/build_spa.py` — `SECTION_SLUGS` dict, parser heading-pattern table, `_NEXT_BOUNDARY_RE` (or whatever the parser uses to detect section boundaries during body collection)

- [ ] **Step 1: Locate `SECTION_SLUGS`**

```bash
grep -n "SECTION_SLUGS\|\"About the author\":" build/build_spa.py | head -10
```

Find the dict and the existing About-the-author entry — the changelog entry goes immediately AFTER it (matching the source-markdown order: About → Changelog → Appendices).

- [ ] **Step 2: Add the SECTION_SLUGS entry**

Find the existing entry:

```python
    ("about", "About the author"):                                  "about-the-author",
```

Add immediately below:

```python
    ("changelog", "Changelog"):                                     "changelog",
```

- [ ] **Step 3: Update the `SectionKind` Literal type**

```bash
grep -n "SectionKind = Literal" build/build_spa.py
```

Find the line:

```python
SectionKind = Literal["foreword", "prologue", "chapter", "closing",
                      "acknowledgments", "about", "appendix"]
```

Add `"changelog"` to the literal union:

```python
SectionKind = Literal["foreword", "prologue", "chapter", "closing",
                      "acknowledgments", "about", "changelog", "appendix"]
```

(Order in the literal doesn't affect behavior, but keeping it in document order helps readability.)

- [ ] **Step 4: Add the parser's heading-pattern detection**

```bash
grep -n "_ABOUT_RE\|_APPENDIX_RE\|^_.*_RE = re\.compile" build/build_spa.py | head -10
```

Find the existing `_ABOUT_RE` and `_APPENDIX_RE` definitions. Add a new regex for the changelog heading immediately after `_ABOUT_RE`:

```python
_CHANGELOG_RE = re.compile(r"^## Changelog\b.*$")
```

- [ ] **Step 5: Wire `_CHANGELOG_RE` into the parser state machine**

```bash
grep -n "_ABOUT_RE.match\|_APPENDIX_RE.match\|if _ABOUT_RE\|if _APPENDIX_RE" build/build_spa.py | head -5
```

Find the section of the parser where `_ABOUT_RE` is handled (probably inside `parse_sections()`). It should look like:

```python
        if _ABOUT_RE.match(line):
            flush()
            cur_meta = ("about", "About the author")
            cur_title = "About the author"
            i += 1
            continue
```

Immediately AFTER this block, add the changelog branch:

```python
        if _CHANGELOG_RE.match(line):
            flush()
            cur_meta = ("changelog", "Changelog")
            cur_title = "Changelog"
            i += 1
            continue
```

- [ ] **Step 6: Update `_NEXT_BOUNDARY_RE` if it exists**

```bash
grep -n "_NEXT_BOUNDARY_RE\|## About the author\|## Acknowledgments" build/build_spa.py | head -10
```

If a `_NEXT_BOUNDARY_RE` exists (used to detect section boundaries in body collection or reading-time computation), it likely lists patterns like `^## Chapter|^# Part|^## Closing|^## Acknowledgments|^## About the author|^## Appendix`. Add `## Changelog\b` to the alternation:

```python
_NEXT_BOUNDARY_RE = re.compile(
    r"(?m)^(?:## Chapter \d+\b|# Part [IVX]+\b|# Closing\b|## Appendix [A-Z]\.|## About the author\b|## Acknowledgments\b|## Changelog\b)"
)
```

(If the existing regex has slightly different shape, preserve its structure and just add the `## Changelog\b` branch.)

- [ ] **Step 7: Verify the parser change doesn't break the existing build**

```bash
python3 build/build_spa.py 2>&1 | tail -5
```

Expected: build FAILS with `RuntimeError: parse_sections produced N sections, expected N+1 (per SECTION_SLUGS table)` (or similar count-mismatch error). The SECTION_SLUGS now has an entry for changelog but the source markdown doesn't have the `## Changelog` heading yet. **This expected failure is the proof the parser is reading the new map correctly.** Task 7 (adding the source markdown) resolves the mismatch.

- [ ] **Step 8: Commit (deferred — bundled into Task 10's commit)**

---

## Task 5: TOC slot for changelog

**Why:** The TOC builder has explicit slots for Foreword/Prologue/Parts/Chapters/Closing/Acknowledgments/About/Appendices. Changelog needs its own slot between About and Appendices.

**Files:**
- Modify: `build/build_spa.py` — `build_toc()` function

- [ ] **Step 1: Locate the TOC builder + the About-the-author slot**

```bash
grep -n "about-the-author\|build_toc\|About the author" build/build_spa.py | head -10
```

Find the TOC builder block that emits the About-the-author entry. It likely looks like:

```python
    # About the author (sits between Closing and Appendices).
    sections.append('<div class="toc-section">')
    sections.append('<div class="toc-section-title"><a href="/about-the-author/">About the author</a></div>')
    sections.append("</div>")
```

(Or with in-page anchor URL if the page uses `read` mode — there may be a mode parameter; preserve it.)

- [ ] **Step 2: Add the Changelog slot**

Immediately AFTER the About-the-author TOC block, insert:

```python
    # Changelog (sits between About and Appendices).
    sections.append('<div class="toc-section">')
    sections.append('<div class="toc-section-title"><a href="/changelog/">Changelog</a></div>')
    sections.append("</div>")
```

If the builder uses a `mode` parameter (e.g., `'in-page'` / `'transition'` / `'chapter-url'`), match the existing pattern — use the same URL-style helper the About entry uses. For example:

```python
    sections.append(f'<div class="toc-section-title">{_href_helper("changelog", "Changelog")}</div>')
```

(Use whichever pattern the surrounding code uses; mirror the About row exactly, swapping `about-the-author`/`About the author` for `changelog`/`Changelog`.)

- [ ] **Step 3: Verify (after Task 7 lands)**

The TOC change doesn't render until the changelog Section exists. Defer verification to the post-Task-7 rebuild.

- [ ] **Step 4: Commit (deferred — bundled into Task 10's commit)**

---

## Task 6: Suppress reading-time badge on changelog kind

**Why:** A ~150-word changelog page renders as "1 min read" which feels confused. Suppress the badge for `kind="changelog"` specifically.

**Files:**
- Modify: `build/build_spa.py` — wherever the per-chapter `<p class="reading-time">` is emitted

- [ ] **Step 1: Locate the reading-time emission**

```bash
grep -n "reading-time\|reading_time_min\|min read" build/build_spa.py | head -10
```

Find the line(s) that emit the reading-time badge. Likely inside `chapter_template_body()` or similar. Look for something like:

```python
    reading_time = (
        f'<p class="reading-time">{section.reading_time_min} min read</p>'
        if section.reading_time_min else ''
    )
```

- [ ] **Step 2: Add the changelog suppression**

Update the conditional to also skip for the changelog kind:

```python
    reading_time = (
        f'<p class="reading-time">{section.reading_time_min} min read</p>'
        if section.reading_time_min and section.kind != "changelog" else ''
    )
```

- [ ] **Step 3: Verify (after Task 7 lands)**

The reading-time suppression doesn't render until the changelog Section exists. Defer verification.

- [ ] **Step 4: Commit (deferred — bundled into Task 10's commit)**

---

## Task 7: Source markdown — Changelog section

**Why:** Add the new section that the build script (after Tasks 4-6) is expecting.

**Files:**
- Modify: `source/Ship_It_With_AI.md` — insert new section between Acknowledgments and About-the-author

- [ ] **Step 1: Locate the insertion point**

```bash
grep -n "^## Acknowledgments\|^## About the author" source/Ship_It_With_AI.md
```

Find the line numbers. The Changelog section goes between Acknowledgments and About-the-author — find the last line of the Acknowledgments section (typically a `---` separator), and the new section goes BEFORE the `## About the author` heading.

Wait — re-read the spec: the order is Acknowledgments → **Changelog** → About-the-author? Or Acknowledgments → About-the-author → **Changelog** → Appendix A?

The spec's resolved decision #6 says: "between About-the-author and Appendix A (housekeeping sequence)". So the order is:

Closing → Acknowledgments → About-the-author → **Changelog** → Appendix A → Appendix B → Appendix C

The Changelog inserts AFTER `## About the author`'s section ends, BEFORE `## Appendix A.`.

- [ ] **Step 2: Find the end of the About section**

```bash
grep -n "^## About the author\|^## Appendix A" source/Ship_It_With_AI.md
```

Find both line numbers. The Changelog inserts between them. The About section's body ends just before the `## Appendix A` heading. Look for the `---` separator at the end of About (or just insert before `## Appendix A` with a blank line).

- [ ] **Step 3: Insert the Changelog section**

Insert this block immediately before `## Appendix A. Cost Economics` (preserving any blank line / separator structure that the source uses between sections):

```markdown
## Changelog {#changelog}

This page tracks meaningful updates to the manual. Smaller copy-edits and SEO tweaks are not enumerated; the build's last-modified date is in the footer.

### 2026-05-27 — Memory primitive + open-set framing

Memory promoted to a named primitive across the book; Chapter 1 retitled "The primitives" and the structural argument rewritten as "named primitives + the recursive primitive (subagents)". The closed "six primitives" count dropped throughout in favor of open-set framing. New Memory section covers two halves - manually defined memory (AGENTS.md/CLAUDE.md, agent-agnostic) and the auto-memory system (Auto Memory, Auto Dream - currently Claude-Code-led). Diagram updated. Chapter 6 gains a one-paragraph framing intro anchoring AGENTS.md as the team-shareable memory layer. Three new Appendix C entries source the Memory claims.

### 2026-05-27 — SEO pass: per-chapter URLs

Split the all-in-one SPA into 20 indexable URLs: landing (`/`) + each section as its own page (`/foreword/`, `/chapter-1-primitives/`, ... `/appendix-c-sources/`) + `/read/` for the single-page reading mode. Each chapter page now has unique title, meta description, canonical URL, `TechArticle` + `BreadcrumbList` JSON-LD, and prev/next nav. Hero gained a control-thesis dek and a three-button CTA row. Schema upgraded from `Article` to `Book` + `Organization` + `FAQPage`. Cross-section anchor rewriting, AGENTS.md de-linking, hash-redirect shim for old `/#chapter-N` bookmarks. Built-in 404 page, `llms.txt` for AI answer engines, `cover.webp`.

### 2026-05-26 — Feedback-pass polish

External-reviewer pass: TOC chapter-to-part mismatch fixed, figure numbering dropped (web-manual style), new Source-note and Artifact callout components with light + dark variants, foreword bio trimmed to four sentences and full version moved to a new About-the-author section, hero gained a control-thesis dek, AGENTS.md links collapsed to at most one per chapter, per-section `¶` copy-link anchors, callout stack tightening.

### 2026-05-26 — First public version

Manual published at ship-it-with.ai. Ten chapters across three parts (Architecture, Method, Reality), three appendices, plus foreword, prologue, closing.

---

```

(The trailing `---` and blank line match the source's existing section-separator pattern.)

- [ ] **Step 4: Rebuild and verify the build succeeds**

```bash
python3 build/build_spa.py 2>&1 | tail -10
```

Expected: build completes. Output mentions `Wrote _site/changelog/index.html` (or similar — the per-section render loop emits each section). Section count matches `SECTION_SLUGS` size now that Task 4's mismatch is resolved.

- [ ] **Step 5: Spot-check the rendered page**

```bash
ls _site/changelog/index.html
grep -c "2026-05-27 — Memory primitive\|2026-05-26 — First public version" _site/changelog/index.html
```

Expected: file exists; the grep finds at least 2 hits (both dated entries present).

- [ ] **Step 6: Commit (deferred — bundled into Task 10's commit)**

---

## Task 8: Source markdown — "A note on dated claims" paragraph

**Why:** Add the maintenance promise + changelog link to the existing front-matter section.

**Files:**
- Modify: `source/Ship_It_With_AI.md` — `## A note on dated claims` section (~line 151)

- [ ] **Step 1: Locate the section + its closing**

```bash
grep -n "^## A note on dated claims\|^## Scope and limits" source/Ship_It_With_AI.md
```

Find both lines. The "A note on dated claims" section ends just before `## Scope and limits`. The section body has its own `---` separator at the very end.

Read the section to find the exact end:

```bash
sed -n '151,170p' source/Ship_It_With_AI.md
```

Identify the last paragraph and the trailing `---`.

- [ ] **Step 2: Insert the new paragraph**

Insert a new blank line + paragraph immediately BEFORE the trailing `---` of the section. The new content:

```markdown
I do my best to keep the manual current and maintain a [changelog](/changelog/) of meaningful updates.
```

It must be its own paragraph (not appended to the existing final paragraph). Concretely, the section's final lines should look like (before edit):

```
... If a new primitive emerges, the list grows.

---
```

After edit:

```
... If a new primitive emerges, the list grows.

I do my best to keep the manual current and maintain a [changelog](/changelog/) of meaningful updates.

---
```

- [ ] **Step 3: Rebuild + spot-check**

```bash
python3 build/build_spa.py
grep "I do my best to keep the manual current" _site/foreword/index.html | head -2
grep 'href="/changelog/"' _site/foreword/index.html | head -2
```

Expected: the rendered foreword (which contains the front-matter sections including "A note on dated claims") includes the new paragraph + link.

- [ ] **Step 4: Commit (deferred — bundled into Task 10's commit)**

---

## Task 9: Verify script assertions

**Files:**
- Modify: `build/tests/verify_seo_pass.js` — add a new assertion block for the changelog feature

- [ ] **Step 1: Locate the assertion structure**

```bash
grep -n "Memory primitive\|chapter-6 framing intro\|appendix-c has all 3 new" build/tests/verify_seo_pass.js | head -5
```

The existing verify has assertion blocks numbered (per the SEO + memory passes). Add new assertions after the existing ones.

- [ ] **Step 2: Add the Changelog feature assertion block**

Inside the verify script's main run block, after the last existing assertion (likely the Appendix C entries assertion from the Memory pass), add:

```javascript
// ===== Changelog + Last-updated footer assertions =====

// 10. /changelog/ page exists, returns 200, has correct H1
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  const resp = await page.goto(`${baseUrl}/changelog/`);
  if (!resp || resp.status() !== 200) fail(`/changelog/ status ${resp && resp.status()}`);
  const h1Count = await page.locator('h1').count();
  if (h1Count !== 1) fail(`/changelog/ has ${h1Count} <h1>, expected 1`);
  const h1Text = (await page.locator('h1').first().textContent() || '').trim();
  if (h1Text !== 'Changelog') fail(`/changelog/ H1 = "${h1Text}", expected "Changelog"`);
  if (resp && resp.status() === 200 && h1Count === 1 && h1Text === 'Changelog') {
    ok('/changelog/ exists, returns 200, H1 = "Changelog"');
  }
  await ctx.close();
}

// 11. Changelog page has all four initial entries
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/changelog/`);
  const body = (await page.locator('main').textContent() || '');
  const required = [
    '2026-05-27 — Memory primitive + open-set framing',
    '2026-05-27 — SEO pass: per-chapter URLs',
    '2026-05-26 — Feedback-pass polish',
    '2026-05-26 — First public version',
  ];
  let allPresent = true;
  for (const entry of required) {
    if (!body.includes(entry)) {
      fail(`/changelog/ missing entry "${entry}"`);
      allPresent = false;
    }
  }
  if (allPresent) ok('/changelog/ contains all 4 initial entries');
  await ctx.close();
}

// 12. Changelog page has NO reading-time badge (suppressed per spec)
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/changelog/`);
  const readingTimeCount = await page.locator('.reading-time').count();
  if (readingTimeCount !== 0) fail(`/changelog/ has ${readingTimeCount} .reading-time elements, expected 0 (suppressed)`);
  else ok('/changelog/ reading-time badge suppressed');
  await ctx.close();
}

// 13. Changelog prev/next nav targets
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/changelog/`);
  const prev = await page.locator('.chapter-prev').first().getAttribute('href');
  const next = await page.locator('.chapter-next').first().getAttribute('href');
  if (prev !== '/about-the-author/') fail(`/changelog/ prev = "${prev}", expected "/about-the-author/"`);
  if (next !== '/appendix-a-cost-economics/') fail(`/changelog/ next = "${next}", expected "/appendix-a-cost-economics/"`);
  if (prev === '/about-the-author/' && next === '/appendix-a-cost-economics/') {
    ok('/changelog/ prev → /about-the-author/, next → /appendix-a-cost-economics/');
  }
  await ctx.close();
}

// 14. Sitemap includes /changelog/
{
  const sitemap = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
  if (!sitemap.includes('<loc>https://ship-it-with.ai/changelog/</loc>')) {
    fail('sitemap missing /changelog/');
  } else ok('sitemap includes /changelog/');
  // Sitemap should now have 21 URLs total (was 20)
  const urlCount = (sitemap.match(/<url>/g) || []).length;
  if (urlCount !== 21) fail(`sitemap has ${urlCount} URLs, expected 21`);
  else ok('sitemap has 21 URLs (was 20)');
}

// 15. Footer "Last updated" stamp on landing + chapter page
{
  const dateRegex = /Last updated [A-Z][a-z]+ \d{1,2}, \d{4}/;
  for (const path_ of ['/', '/chapter-1-primitives/']) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const page = await ctx.newPage();
    await page.goto(`${baseUrl}${path_}`);
    const footerText = (await page.locator('.footer-copy').first().textContent() || '');
    if (!dateRegex.test(footerText)) fail(`footer at ${path_} missing "Last updated <date>" — got: "${footerText}"`);
    else ok(`footer at ${path_} has "Last updated <date>"`);
    await ctx.close();
  }
}

// 16. Footer Changelog link present
{
  for (const path_ of ['/', '/chapter-1-primitives/']) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const page = await ctx.newPage();
    await page.goto(`${baseUrl}${path_}`);
    const linkCount = await page.locator('.footer-contact a[href="/changelog/"]').count();
    if (linkCount < 1) fail(`footer at ${path_} missing Changelog link in .footer-contact`);
    else ok(`footer at ${path_} has Changelog link`);
    await ctx.close();
  }
}

// 17. "A note on dated claims" carries the maintenance promise + link
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/foreword/`);
  const body = (await page.locator('main').textContent() || '');
  if (!body.includes('I do my best to keep the manual current and maintain a')) {
    fail('/foreword/ missing maintenance promise sentence');
  } else {
    const linkCount = await page.locator('a[href="/changelog/"]').count();
    if (linkCount < 1) fail('/foreword/ maintenance sentence missing /changelog/ link');
    else ok('/foreword/ has maintenance promise + /changelog/ link');
  }
  await ctx.close();
}

// 18. Hash-redirect: /#changelog → /changelog/
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/#changelog`);
  await page.waitForURL(/\/changelog\//, { timeout: 2000 }).catch(() => {});
  const url = page.url();
  if (!url.includes('/changelog/') || url.includes('/#changelog')) {
    fail(`hash-redirect /#changelog landed at ${url}`);
  } else ok('hash-redirect /#changelog → /changelog/');
  await ctx.close();
}
```

- [ ] **Step 3: Run verify**

```bash
node build/tests/verify_seo_pass.js 2>&1 | tail -40
```

Expected: `Verification PASSED.` with 9 new `OK:` lines for the changelog assertions.

- [ ] **Step 4: Commit (deferred — bundled into Task 10's commit)**

---

## Task 10: Final verify + commit + PR

**Files:** none new

- [ ] **Step 1: Clean run**

```bash
rm -rf _site build/tests/screenshots/seo-pass
node build/tests/verify_seo_pass.js 2>&1 | tail -40
```

Expected: `Verification PASSED.` with all existing + 9 new changelog assertions OK.

- [ ] **Step 2: Manual walk**

```bash
python3 -m http.server -d _site 8765 > /dev/null 2>&1 &
sleep 1
```

In a browser, open + spot-check:

- `http://localhost:8765/` — footer shows "Last updated <Month DD, YYYY>" in the copyright row and a "Changelog" link in the contact row
- `http://localhost:8765/changelog/` — H1 "Changelog", four dated entries, NO "1 min read" badge, prev nav → About-the-author, next nav → Appendix A
- `http://localhost:8765/foreword/` — "A note on dated claims" section ends with the maintenance promise + changelog link
- `http://localhost:8765/#changelog` — should redirect to `/changelog/`

Kill server: `pkill -f "http.server -d _site 8765"`.

- [ ] **Step 3: Commit**

```bash
git status
git add source/Ship_It_With_AI.md build/build_spa.py build/spa_template.html build/tests/verify_seo_pass.js
git commit -m "feat: changelog page + last-updated footer

Adds /changelog/ section with the four most recent releases backfilled
(Memory primitive, SEO pass, Feedback pass, First public version).
Footer carries a build-time 'Last updated <Month DD, YYYY>' stamp in
the copyright row; Changelog nav link joins email/LinkedIn/ai-leaders.ro
in .footer-contact. 'A note on dated claims' section gains a one-paragraph
maintenance promise + link. Reading-time badge suppressed on the changelog
page. Verify script extended with 9 assertions: page existence + content,
prev/next nav, sitemap inclusion (21 URLs), footer date regex + link
presence, dated-claims paragraph, hash-redirect."
```

- [ ] **Step 4: Push and prepare PR**

```bash
git push -u origin changelog
```

If `gh pr create` works for your account, run:

```bash
gh pr create --title "Changelog page + last-updated footer" --body "$(cat <<'EOF'
## Summary

- New /changelog/ section with four recent releases backfilled (Memory primitive, SEO pass, Feedback pass, First public version)
- Footer "Last updated <Month DD, YYYY>" stamp on every page, auto-stamped at build time via new {{DATE_MODIFIED_HUMAN}} placeholder
- Changelog nav link in .footer-contact (parallel to email/LinkedIn/ai-leaders.ro), not in copyright row
- "A note on dated claims" front-matter section gains a maintenance promise + link to /changelog/
- Reading-time badge suppressed on the changelog page (~150 words; "1 min read" reads as confused)
- Sitemap now 21 URLs (was 20)

## Spec & plan
- Spec: `docs/superpowers/specs/2026-05-27-changelog-and-last-updated-design.md`
- Plan: `docs/superpowers/plans/2026-05-27-changelog-and-last-updated.md`

## Test plan
- [x] `node build/tests/verify_seo_pass.js` passes (existing + 9 new assertions)
- [x] Manual walk: /, /changelog/, /foreword/, /#changelog (hash-redirect)
- [ ] Reviewer eyeballs the four initial changelog entries
- [ ] CI rebuilds and deploys on merge
EOF
)"
```

If `gh pr create` is blocked (org account permissions): open the PR via:

`https://github.com/ro-ai-labs/ship-it-with-ai/compare/main...changelog`

CI rebuilds and deploys on merge.

---

## Self-review (run by the engineer before opening the PR)

**Spec coverage:**
- [x] Footer "Last updated" stamp → Tasks 2 + 3
- [x] Changelog link in `.footer-contact` → Task 3
- [x] New /changelog/ page → Tasks 4 + 5 + 7
- [x] Reading-time suppressed on changelog → Task 6
- [x] "A note on dated claims" maintenance paragraph → Task 8
- [x] Four initial changelog entries → Task 7
- [x] Hash-redirect map updated → automatic via SECTION_SLUGS (Task 4)
- [x] Sitemap includes new URL → automatic via SECTION_SLUGS (Task 4)
- [x] Verify assertions (page existence, entries, reading-time, prev/next, sitemap, footer date, footer link, dated-claims, hash-redirect) → Task 9

**Files touched (verify no orphans):**
- `source/Ship_It_With_AI.md` — Tasks 7, 8
- `build/build_spa.py` — Tasks 2, 4, 5, 6
- `build/spa_template.html` — Task 3
- `build/tests/verify_seo_pass.js` — Task 9
