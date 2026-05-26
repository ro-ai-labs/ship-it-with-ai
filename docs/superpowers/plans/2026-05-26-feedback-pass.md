# Feedback-pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Polish the live ship-it-with.ai site per external reviewer feedback — fix the TOC/figure bugs, add two new callout components (Source note, Artifact), trim the foreword bio, add a top CTA row, and harden the About-the-author surface — verifying everything across desktop / tablet / mobile in light + dark mode.

**Architecture:** Three tiered commits in one branch. Commit 1 is mechanical (TOC map, figure numbering, copy sweep). Commit 2 is visual additions (callouts, hero changes, CTAs, polish). Commit 3 is structural (bio trim, About section, AGENTS.md de-linking, copy-link anchors). A Playwright verification script runs after each commit; the final run gates the PR.

**Tech Stack:** Python 3.12 + `markdown` package for the build script. Vanilla HTML/CSS/JS template. Playwright (chromium) for verification. GitHub Pages for hosting via `.github/workflows/static.yml`.

**Spec:** `docs/superpowers/specs/2026-05-26-feedback-pass-design.md` (read this first — every task assumes its decisions).

**Branch:** Work on a feature branch (e.g., `feedback-pass`) so the PR groups all three commits.

---

## File map

**Create**
- `build/tests/verify_feedback_pass.js` — Playwright verification script
- `build/tests/lib/build_and_open.js` — small helper that runs the build and returns a `file://` URL (DRY across the verify script)
- `build/tests/screenshots/feedback-pass/` — output directory for verification screenshots (auto-created on first run)

**Modify**
- `source/Ship_It_With_AI.md` — figure captions, book→manual sweep, foreword bio trim, new About section
- `build/build_spa.py` — TOC chapter-to-part map, figure-caption regex, source-note + artifact-box transforms, AGENTS.md de-linker, anchor-link injector, About-section TOC integration
- `build/spa_template.html` — new CSS vars, source-note/artifact-box styles, mobile + print rules, hero dek, CTA row, anchor-link styles and JS

**Do NOT modify**
- `.github/workflows/static.yml` — CI rebuilds index.html; no changes needed for this pass
- `index.html`, `cover.jpg`, `robots.txt`, `sitemap.xml`, `CNAME`, `.nojekyll` — all served as-is

---

## Workflow conventions

After every code change in this plan: **run the build, then run the verification script.** That's:

```bash
python3 build/build_spa.py && node build/tests/verify_feedback_pass.js
```

Until Task 4 lands, the verification script doesn't exist yet — for Tasks 1-3 use plain `grep` or `python3 build/build_spa.py` then `grep` the generated `index.html`.

---

# COMMIT 1 — Mechanical fixes

## Task 1: Create the feature branch

**Files:** none

- [ ] **Step 1: Create and switch to the branch**

```bash
git checkout -b feedback-pass
```

- [ ] **Step 2: Verify clean working tree**

```bash
git status
```

Expected: `nothing to commit, working tree clean` on `feedback-pass`.

---

## Task 2: Fix the TOC chapter-to-part map

**Why:** TOC currently places Ch 4 under Part I, Ch 8 under Part II, and references a non-existent Ch 11. The body markdown is correct; only the hardcoded build-script map is wrong.

**Files:**
- Modify: `build/build_spa.py:648-660`

- [ ] **Step 1: Write a failing grep assertion**

Build the current `index.html` first, then assert the bug exists:

```bash
python3 build/build_spa.py
# Confirm the bug: Chapter 4 link should be inside Part II's section, not Part I's.
python3 -c "
import re
html = open('index.html').read()
parts = re.findall(r'(<div class=\"toc-section\">.*?</div></div>)', html, re.S)
part_i = [p for p in parts if 'Part I -' in p][0]
assert 'chapter-4' not in part_i, 'BUG STILL PRESENT: chapter-4 in Part I'
"
```

Expected (before fix): `AssertionError: BUG STILL PRESENT: chapter-4 in Part I`.

- [ ] **Step 2: Apply the fix**

Edit `build/build_spa.py:648-660`:

```python
    chapter_to_part = {
        "chapter-1": "part-i",
        "chapter-2": "part-i",
        "chapter-3": "part-i",
        "chapter-4": "part-ii",
        "chapter-5": "part-ii",
        "chapter-6": "part-ii",
        "chapter-7": "part-ii",
        "chapter-8": "part-iii",
        "chapter-9": "part-iii",
        "chapter-10": "part-iii",
    }
```

(Drop the stale `"chapter-11"` entry.)

- [ ] **Step 3: Rebuild and re-run the assertion**

```bash
python3 build/build_spa.py
python3 -c "
import re
html = open('index.html').read()
parts = re.findall(r'(<div class=\"toc-section\">.*?</div></div>)', html, re.S)
part_i = [p for p in parts if 'Part I -' in p][0]
part_ii = [p for p in parts if 'Part II -' in p][0]
part_iii = [p for p in parts if 'Part III -' in p][0]
assert 'chapter-4' not in part_i and 'chapter-4' in part_ii, 'chapter-4 placement'
assert 'chapter-8' not in part_ii and 'chapter-8' in part_iii, 'chapter-8 placement'
assert 'chapter-11' not in (part_i + part_ii + part_iii), 'stale chapter-11 reference'
print('OK')
"
```

Expected: `OK`.

- [ ] **Step 4: Commit**

```bash
git add build/build_spa.py
git commit -m "fix: TOC chapter-to-part map (off-by-one + stale ch-11)"
```

---

## Task 3: Drop figure numbering — diagram functions

**Why:** Reviewer's recommendation: a web manual doesn't need academic figure numbering. Currently Ch 1 has "Figure 2.1", Ch 5 has "Figure 6.1", etc. — leftover from earlier chapter numbering.

**Files:**
- Modify: `build/build_spa.py` — the five `diagram_*()` functions at lines ~22-146

- [ ] **Step 1: List current captions to know what's changing**

```bash
grep -n "Figure [0-9]" build/build_spa.py
```

Expected: five lines, one per diagram function.

- [ ] **Step 2: Apply the rewrite**

Edit each `<figcaption>` in `build/build_spa.py`:

- `diagram_primitives` (~line 40): change `<figcaption>Figure 2.1. The six primitives and the harness that runs them. Subagents are the recursive primitive: each subagent is itself an instance of the other five.</figcaption>` to `<figcaption>Figure: The six primitives and the harness that runs them. Subagents are the recursive primitive: each subagent is itself an instance of the other five.</figcaption>`.
- `diagram_layers` (~line 61): `Figure 4.1.` → `Figure:` (drop the leading number+period).
- `diagram_loop` (~line 79): `Figure 6.1.` → `Figure:`.
- `diagram_traffic` (~line 105): `Figure 9.1.` → `Figure:`.
- `diagram_arc` (~line 145): `Figure 11.1.` → `Figure:`.

The text content after the prefix stays unchanged.

- [ ] **Step 3: Rebuild and assert no numbered figures remain in those captions**

```bash
python3 build/build_spa.py
grep -c 'Figure 2.1\|Figure 4.1\|Figure 6.1\|Figure 9.1\|Figure 11.1' index.html
```

Expected: `0`.

- [ ] **Step 4: Commit** (deferred — combined with Task 4 since they're the same concern)

---

## Task 4: Drop figure numbering — markdown captions + regex

**Why:** The markdown source has `*Figure N.N. ...*` captions that get parsed by a regex at `build/build_spa.py:166`. Both source captions and the regex need updating.

**Files:**
- Modify: `source/Ship_It_With_AI.md` — 5 figure caption lines
- Modify: `build/build_spa.py:163-167` — `FIGURE_RE` regex

- [ ] **Step 1: List the current source captions**

```bash
grep -n '^\*Figure [0-9]' source/Ship_It_With_AI.md
```

Expected: 5 lines (around 270, 557, 837, 1477, 1761).

- [ ] **Step 2: Strip the number from each markdown caption**

In `source/Ship_It_With_AI.md`, edit each `*Figure N.N. <text>*` line to `*Figure: <text>*`:

- L270: `*Figure 2.1. The six primitives ...` → `*Figure: The six primitives ...`
- L557: `*Figure 4.1. The five governance ...` → `*Figure: The five governance ...`
- L837: `*Figure 6.1. The six-phase loop. ...` → `*Figure: The six-phase loop. ...`
- L1477: `*Figure 9.1. The kill signals ...` → `*Figure: The kill signals ...`
- L1761: `*Figure 11.1. The 90-day adoption arc. ...` → `*Figure: The 90-day adoption arc. ...`

- [ ] **Step 3: Update the FIGURE_RE regex**

Edit `build/build_spa.py:163-167`. Current:

```python
FIGURE_RE = re.compile(
    r"```\n(?P<body>.*?)\n```\s*\n+\*Figure\s+(?P<fid>\d+\.\d+)\.[^*]*\*\s*\n",
    re.DOTALL,
)
```

Replace with (accepts both old `N.N.` and new no-number captions; the `fid` group is no longer used and is dropped):

```python
FIGURE_RE = re.compile(
    r"```\n(?P<body>.*?)\n```\s*\n+\*Figure(?:\s+\d+\.\d+)?[:.][^*]*\*\s*\n",
    re.DOTALL,
)
```

Verify the regex is still referenced correctly — check the function `replace_figures` that uses `FIGURE_RE`:

```bash
grep -n "FIGURE_RE\|fid" build/build_spa.py
```

If any code references `m.group("fid")`, remove or rewrite it (figure id is no longer captured). The likely call site is in `replace_figures` near line 170-180.

- [ ] **Step 4: Rebuild, assert numbers are gone everywhere**

```bash
python3 build/build_spa.py
grep -c 'Figure [0-9]\+\.[0-9]' index.html
```

Expected: `0`.

- [ ] **Step 5: Commit**

```bash
git add build/build_spa.py source/Ship_It_With_AI.md
git commit -m "fix: drop figure numbering (web-manual style: 'Figure: ...')"
```

---

## Task 5: Book → manual sweep + printer phrase

**Why:** Reviewer flagged the "printer finished" phrase as a print-era artifact, plus general "book" mentions where the artifact is meant to be a web manual.

**Files:**
- Modify: `source/Ship_It_With_AI.md`

- [ ] **Step 1: Inventory all "book" mentions**

```bash
grep -n -w -i "book\|books" source/Ship_It_With_AI.md
```

Read each occurrence in context. Categorize:
- **Keep:** citations / titles of referenced print books (if any), the idiom "open book", references to other people's books.
- **Replace:** any sentence where "book" refers to *this* artifact (should be "manual").

- [ ] **Step 2: Replace the printer-era sentence**

Find the sentence in `source/Ship_It_With_AI.md` (likely in the Foreword or "Scope and limits") containing "before the printer finished" and replace with: *"If this were a tool guide, it would be stale before publication."*

```bash
grep -n "printer finished" source/Ship_It_With_AI.md
```

- [ ] **Step 3: Replace remaining self-referential "book" → "manual"**

For each location identified in Step 1 as "Replace", edit the sentence. Be careful: replace only when the word refers to this artifact. The existing front-matter already uses "manual" in most headings (`How to read this manual`, etc.), so the body should follow suit.

- [ ] **Step 4: Re-grep to verify**

```bash
grep -n -w -i "book\|books" source/Ship_It_With_AI.md
```

Every remaining occurrence should be intentional (citations, idioms, other people's books). No occurrence refers to *this* artifact as a "book".

- [ ] **Step 5: Rebuild and spot-check**

```bash
python3 build/build_spa.py
```

Open `index.html` in a browser. Read the Foreword and "Scope and limits" sections. Confirm no jarring "book" mentions.

- [ ] **Step 6: Commit**

```bash
git add source/Ship_It_With_AI.md
git commit -m "edit: book → manual sweep, drop print-era phrasing"
```

---

# COMMIT 2 — New visual components

## Task 6: Add CSS variables for new callouts

**Why:** The existing template defines every color as a `--color-*` CSS var with light + dark pairs. New components should follow suit.

**Files:**
- Modify: `build/spa_template.html` — `:root` block (~line 71-93) and `[data-theme="dark"]` block (~line 105-122)

- [ ] **Step 1: Add light-theme variables**

In `build/spa_template.html`, find the `:root` block (search for `--color-quote-border:`). Add at the end of the var list, before the closing `}`:

```css
      --color-source-bg: #f1f4f8;
      --color-source-border: #cbd5e1;
      --color-source-text: #475569;
      --color-source-label-bg: #475569;
      --color-artifact-bg: #faf8f3;
      --color-artifact-accent: #475569;
      --color-artifact-icon: #475569;
```

- [ ] **Step 2: Add dark-theme variables**

Find `[data-theme="dark"] {` block. Add at the end of its var list, before the closing `}`:

```css
      --color-source-bg: #1e293b;
      --color-source-border: #334155;
      --color-source-text: #cbd5e1;
      --color-source-label-bg: #94a3b8;
      --color-artifact-bg: #232629;
      --color-artifact-accent: #94a3b8;
      --color-artifact-icon: #94a3b8;
```

- [ ] **Step 3: Build (CSS only — no behavior change yet)**

```bash
python3 build/build_spa.py
grep -c "color-source-bg\|color-artifact-bg" index.html
```

Expected: `>= 2` (each var appears in both `:root` and `[data-theme]` blocks).

- [ ] **Step 4: Commit** (deferred — bundled with Task 7 and onward into commit 2)

---

## Task 7: Build the Playwright verification scaffold

**Why:** Subsequent tasks rely on a verify script for TDD-style assertions and screenshots. Build the skeleton now.

**Files:**
- Create: `build/tests/lib/build_and_open.js`
- Create: `build/tests/verify_feedback_pass.js`

- [ ] **Step 1: Confirm Playwright is installed**

```bash
ls build/package.json
node -e "console.log(require.resolve('playwright'))" 2>&1 || echo "playwright not installed"
```

If "not installed": from the repo root, run `cd build && npm install playwright && npx playwright install chromium`. Then `cd ..` back to repo root.

- [ ] **Step 2: Create the helper (uses execFileSync — no shell, no injection vector)**

Create `build/tests/lib/build_and_open.js`:

```javascript
// Run the python build via execFileSync (arg-array form: no shell, no injection),
// then return a file:// URL for the generated index.html.
const { execFileSync } = require('child_process');
const path = require('path');

function buildAndUrl() {
  const repoRoot = path.resolve(__dirname, '..', '..', '..');
  execFileSync('python3', ['build/build_spa.py'], { cwd: repoRoot, stdio: 'inherit' });
  return 'file://' + path.join(repoRoot, 'index.html');
}

module.exports = { buildAndUrl };
```

- [ ] **Step 3: Create the verify script skeleton**

Create `build/tests/verify_feedback_pass.js`:

```javascript
// Verification for the 2026-05-26 feedback pass.
// Runs the build, then opens the generated index.html across viewports + themes,
// asserts feature presence, and saves screenshots.

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { buildAndUrl } = require('./lib/build_and_open');

const VIEWPORTS = [
  { name: 'mobile',  width: 375,  height: 812 },
  { name: 'tablet',  width: 768,  height: 1024 },
  { name: 'desktop', width: 1280, height: 800 },
];

const THEMES = ['light', 'dark'];

const SHOTS_DIR = path.resolve(__dirname, 'screenshots', 'feedback-pass');

async function setTheme(page, theme) {
  await page.evaluate((t) => {
    localStorage.setItem('theme', t);
    document.documentElement.setAttribute('data-theme', t);
  }, theme);
  await page.waitForTimeout(150);
}

function fail(msg) {
  console.error('FAIL:', msg);
  process.exitCode = 1;
}

function ok(msg) {
  console.log('OK:', msg);
}

async function main() {
  fs.mkdirSync(SHOTS_DIR, { recursive: true });
  const url = buildAndUrl();
  const browser = await chromium.launch();

  for (const vp of VIEWPORTS) {
    for (const theme of THEMES) {
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
      const page = await ctx.newPage();
      await page.goto(url);
      await setTheme(page, theme);

      // ---- Assertions added in later tasks; the skeleton just opens the page. ----

      await page.screenshot({
        path: path.join(SHOTS_DIR, `hero_${vp.name}_${theme}.png`),
        fullPage: false,
      });
      ok(`hero screenshot saved: ${vp.name}/${theme}`);

      await ctx.close();
    }
  }

  await browser.close();
  if (process.exitCode) {
    console.error('\nVerification FAILED — see above.');
  } else {
    console.log('\nVerification PASSED.');
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
```

- [ ] **Step 4: Run the skeleton**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: builds, opens 6 viewport×theme combinations, saves 6 hero screenshots to `build/tests/screenshots/feedback-pass/`, prints `Verification PASSED.`.

- [ ] **Step 5: Spot-check screenshots**

```bash
ls build/tests/screenshots/feedback-pass/
```

Expected: `hero_mobile_light.png`, `hero_mobile_dark.png`, `hero_tablet_light.png`, `hero_tablet_dark.png`, `hero_desktop_light.png`, `hero_desktop_dark.png`.

Open one or two visually to confirm the dark/light theme is applying.

- [ ] **Step 6: Commit** (deferred — bundled into commit 2)

---

## Task 8: Source-note callout — CSS + build-script wrap

**Why:** The ~5 `*Source note. <body>*` italic paragraphs in chapters need a distinct styled component (decision: Option B with sandstone, revised by designer to cool blue-gray to avoid case-note collision).

**Files:**
- Modify: `build/spa_template.html` — add `.source-note` CSS
- Modify: `build/build_spa.py` — add `transform_source_notes()` and call it in the pipeline

- [ ] **Step 1: Add `.source-note` CSS to the template**

In `build/spa_template.html`, add this block right after the existing `.case-note` rules (search for `.case-note-label`, find the end of the case-note block around line ~730). Add:

```css
    /* Source notes — inline annotations pointing to Appendix C. */
    .source-note {
      background: var(--color-source-bg);
      border: 1px solid var(--color-source-border);
      border-radius: var(--radius-lg);
      padding: 14px 18px;
      margin: 24px 0;
    }
    .source-note-label {
      display: inline-block;
      background: var(--color-source-label-bg);
      color: white;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      padding: 3px 9px;
      border-radius: 4px;
      margin-bottom: 8px;
    }
    .source-note p {
      margin: 0;
      font-style: italic;
      font-size: 15px;
      line-height: 1.55;
      color: var(--color-source-text);
    }
```

Also add a mobile padding rule (search `@media (max-width`) — find the appropriate block and add `.source-note` to the existing padding rule so it gets the tighter 16×18 padding on mobile. If no rule currently tightens callout padding on mobile, add:

```css
    @media (max-width: 480px) {
      .action-box, .try-box, .case-note, .source-note, .artifact-box {
        padding: 16px 18px;
      }
    }
```

(Add `.artifact-box` here too — it lands in Task 9 and the rule belongs together.)

- [ ] **Step 2: Add an inline pipeline assertion for source-notes**

In `build/tests/verify_feedback_pass.js`, replace the comment `// ---- Assertions added in later tasks; ... ----` with the following — these will be supplemented in subsequent tasks:

```javascript
      // Assertion: Source-note callouts present in body.
      if (vp.name === 'desktop' && theme === 'light') {
        const sourceCount = await page.locator('aside.source-note').count();
        if (sourceCount < 3) fail(`expected >= 3 .source-note elements, got ${sourceCount}`);
        else ok(`source-note count: ${sourceCount}`);

        const note = page.locator('aside.source-note').first();
        if (await note.count()) {
          await note.scrollIntoViewIfNeeded();
          await page.waitForTimeout(150);
          await note.screenshot({ path: path.join(SHOTS_DIR, 'source-note_desktop_light.png') });
        }
      }
      if (vp.name === 'desktop' && theme === 'dark') {
        const note = page.locator('aside.source-note').first();
        if (await note.count()) {
          await note.scrollIntoViewIfNeeded();
          await page.waitForTimeout(150);
          await note.screenshot({ path: path.join(SHOTS_DIR, 'source-note_desktop_dark.png') });
        }
      }
```

- [ ] **Step 3: Run — should FAIL because the wrapper isn't built yet**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: `FAIL: expected >= 3 .source-note elements, got 0` and `Verification FAILED`.

- [ ] **Step 4: Implement `transform_source_notes()` in the build script**

Edit `build/build_spa.py`. Add this function near the other post-processing helpers (e.g., after `transform_source_cards` around line 380):

```python
SOURCE_NOTE_RE = re.compile(
    r'<p><em>Source note\.\s*(?P<body>.*?)</em></p>',
    re.DOTALL,
)


def transform_source_notes(html: str) -> str:
    """Wrap inline `*Source note. ...*` italic paragraphs as styled callouts."""
    def repl(m):
        body = m.group("body").strip()
        return (
            '<aside class="source-note">'
            '<span class="source-note-label">Source</span>'
            f'<p>{body}</p>'
            '</aside>'
        )
    return SOURCE_NOTE_RE.sub(repl, html)
```

Then find the main build pipeline (search for `transform_source_cards(` and similar calls; this is in the `main` function around line ~855-870). Insert the new transform call in the pipeline order specified in the spec (after markdown→html, before action/try wrapping). Locate the line that calls `transform_source_cards(html_after_md)` or similar and add this call before action-box wrapping:

```python
    html = transform_source_notes(html)
```

Place it where it can see the rendered HTML but before the action/try wrap step.

- [ ] **Step 5: Rebuild and re-run**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: `OK: source-note count: 5` (or similar — there are ~5 in source). `Verification PASSED.`

- [ ] **Step 6: Spot-check the screenshots**

Open `build/tests/screenshots/feedback-pass/source-note_desktop_light.png` and `source-note_desktop_dark.png`. The callouts should show:
- Light: cool blue-gray background, slate "SOURCE" badge, italic body.
- Dark: dark slate background, lighter slate badge, light body text.

- [ ] **Step 7: Commit** (deferred — bundled into commit 2)

---

## Task 9: Artifact-box callout — CSS + SVG icon + build-script wrap

**Why:** The 10 `**Artifact: TITLE.** body` paragraphs (one per chapter) need a card-style component. Designer recommendation: warm-neutral tint, 3px left slate border, inline SVG clipboard icon.

**Files:**
- Modify: `build/spa_template.html` — add `.artifact-box` CSS
- Modify: `build/build_spa.py` — add `transform_artifacts()` and call it in the pipeline

- [ ] **Step 1: Add `.artifact-box` CSS**

In `build/spa_template.html`, immediately after the `.source-note` block from Task 8:

```css
    /* Artifact boxes — chapter-ending deliverables. */
    .artifact-box {
      background: var(--color-artifact-bg);
      border: 1px solid var(--color-border-strong);
      border-left: 3px solid var(--color-artifact-accent);
      border-radius: var(--radius-lg);
      padding: 24px 28px;
      margin: 40px 0;
      box-shadow: var(--shadow-sm);
    }
    .artifact-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 10px;
    }
    .artifact-icon {
      width: 16px;
      height: 16px;
      stroke: var(--color-artifact-icon);
      stroke-width: 1.5;
      fill: none;
    }
    .artifact-label {
      display: inline-block;
      background: var(--color-artifact-accent);
      color: white;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      padding: 3px 9px;
      border-radius: 4px;
    }
    .artifact-title {
      font-weight: 600;
      font-size: 17px;
      margin: 0 0 8px 0;
      letter-spacing: -0.01em;
    }
    .artifact-box p {
      margin-bottom: 12px;
      font-size: 16px;
    }
    .artifact-box p:last-child { margin-bottom: 0; }
```

- [ ] **Step 2: Add an artifact-box assertion to the verify script**

In `build/tests/verify_feedback_pass.js`, add inside the existing per-viewport loop (after the source-note assertion):

```javascript
      // Assertion: Artifact-box wrapping — should match the 10 chapters.
      if (vp.name === 'desktop' && theme === 'light') {
        const artifactCount = await page.locator('aside.artifact-box').count();
        if (artifactCount < 10) fail(`expected >= 10 .artifact-box elements, got ${artifactCount}`);
        else ok(`artifact-box count: ${artifactCount}`);

        const firstArtifact = page.locator('aside.artifact-box').first();
        const hasIcon = await firstArtifact.locator('svg.artifact-icon').count();
        const hasLabel = await firstArtifact.locator('.artifact-label').count();
        const hasTitle = await firstArtifact.locator('.artifact-title').count();
        if (!hasIcon)  fail('first artifact-box missing svg.artifact-icon');
        if (!hasLabel) fail('first artifact-box missing .artifact-label');
        if (!hasTitle) fail('first artifact-box missing .artifact-title');

        await firstArtifact.scrollIntoViewIfNeeded();
        await page.waitForTimeout(150);
        await firstArtifact.screenshot({ path: path.join(SHOTS_DIR, 'artifact_desktop_light.png') });
      }
      if (vp.name === 'desktop' && theme === 'dark') {
        const firstArtifact = page.locator('aside.artifact-box').first();
        if (await firstArtifact.count()) {
          await firstArtifact.scrollIntoViewIfNeeded();
          await page.waitForTimeout(150);
          await firstArtifact.screenshot({ path: path.join(SHOTS_DIR, 'artifact_desktop_dark.png') });
        }
      }
```

- [ ] **Step 3: Run — should FAIL**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: `FAIL: expected >= 10 .artifact-box elements, got 0`.

- [ ] **Step 4: Implement `transform_artifacts()` in build script**

In `build/build_spa.py`, add this constant and function next to `transform_source_notes` from Task 8:

```python
CLIPBOARD_SVG = (
    '<svg class="artifact-icon" viewBox="0 0 16 16" aria-hidden="true">'
    '<rect x="3" y="2" width="10" height="13" rx="1.5"></rect>'
    '<rect x="5.5" y="0.75" width="5" height="2.5" rx="0.5"></rect>'
    '<line x1="5" y1="6.5" x2="11" y2="6.5"></line>'
    '<line x1="5" y1="9" x2="11" y2="9"></line>'
    '<line x1="5" y1="11.5" x2="9" y2="11.5"></line>'
    '</svg>'
)

ARTIFACT_RE = re.compile(
    r'<p><strong>Artifact:\s*(?P<title>[^<]+?)\.</strong>\s*(?P<body>.*?)</p>',
    re.DOTALL,
)


def transform_artifacts(html: str) -> str:
    """Wrap **Artifact: TITLE.** body paragraphs into styled cards."""
    def repl(m):
        title = m.group("title").strip()
        body = m.group("body").strip()
        return (
            '<aside class="artifact-box">'
            '<div class="artifact-header">'
            f'{CLIPBOARD_SVG}'
            '<span class="artifact-label">Artifact</span>'
            '</div>'
            f'<h4 class="artifact-title">{title}</h4>'
            f'<p>{body}</p>'
            '</aside>'
        )
    return ARTIFACT_RE.sub(repl, html)
```

Then add the call to the pipeline in `main`, immediately after the `transform_source_notes(html)` call from Task 8:

```python
    html = transform_artifacts(html)
```

- [ ] **Step 5: Rebuild and re-run**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: `OK: artifact-box count: 10`. `Verification PASSED.`.

- [ ] **Step 6: Spot-check screenshots**

Open `artifact_desktop_light.png` and `artifact_desktop_dark.png`. Light should show a warm-tinted card with a 3px slate left border, the clipboard SVG, "ARTIFACT" badge, bold title, then body text. Dark uses surface-elevated background and lighter slate accent.

- [ ] **Step 7: Commit** (deferred — bundled into commit 2)

---

## Task 10: Chapter-end stack tightening

**Why:** Trailing `<hr/>` separators in the existing wrappers break CSS `+` sibling selectors. Drop the trailing `<hr/>` from the existing action/try wraps so adjacent callouts become true siblings.

**Files:**
- Modify: `build/build_spa.py` — action/try wrap regexes (lines ~821-834)
- Modify: `build/spa_template.html` — sibling-margin CSS

- [ ] **Step 1: Drop the trailing `<hr/>` from action/try wraps**

In `build/build_spa.py`, find the action-box wrap (around line 821):

```python
    html_text = re.sub(
        r'<div class="action-marker"><p><strong>Ship this week\.</strong></p>(.*?)<hr ?/?>',
        r'<aside class="action-box"><div class="action-label">Ship this week</div>\1</aside><hr/>',
        html_text,
        flags=re.DOTALL,
    )
```

Change the replacement to NOT re-emit the trailing `<hr/>`:

```python
    html_text = re.sub(
        r'<div class="action-marker"><p><strong>Ship this week\.</strong></p>(.*?)<hr ?/?>',
        r'<aside class="action-box"><div class="action-label">Ship this week</div>\1</aside>',
        html_text,
        flags=re.DOTALL,
    )
```

Similarly for the try-box wrap (around line 833): drop the `<hr/>` from the replacement.

- [ ] **Step 2: Add the sibling-margin CSS**

In `build/spa_template.html`, find the `.try-box li { … }` rule (~line 683). After it, add:

```css
    /* Chapter-end stack tightening: when callouts sit adjacent, reduce top margin. */
    .artifact-box + .action-box,
    .artifact-box + .try-box,
    .action-box + .try-box {
      margin-top: 24px;
    }
```

- [ ] **Step 3: Add an assertion**

In `build/tests/verify_feedback_pass.js`, add a check that the chapter-end stack has no `<hr>` between siblings:

```javascript
      // Chapter-end stack: no <hr> between artifact-box and the following action/try boxes.
      if (vp.name === 'desktop' && theme === 'light') {
        const stackHasHr = await page.evaluate(() => {
          const artifacts = document.querySelectorAll('aside.artifact-box');
          for (const a of artifacts) {
            let n = a.nextElementSibling;
            while (n && n.tagName === 'HR') return true;
            if (n && (n.classList.contains('action-box') || n.classList.contains('try-box'))) continue;
          }
          return false;
        });
        if (stackHasHr) fail('found <hr> between artifact-box and next callout');
        else ok('chapter-end stack has no <hr> between siblings');

        const ch3End = page.locator('aside.artifact-box').nth(2);
        await ch3End.scrollIntoViewIfNeeded();
        await page.waitForTimeout(150);
        await page.screenshot({
          path: path.join(SHOTS_DIR, 'ch3-end_desktop_light.png'),
          fullPage: false,
        });
      }
```

- [ ] **Step 4: Rebuild and run**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: assertions pass. Open `ch3-end_desktop_light.png` to spot-check the visual stack tightness.

- [ ] **Step 5: Commit** (deferred — bundled into commit 2)

---

## Task 11: Appendix C source-card polish

**Files:**
- Modify: `build/spa_template.html` — `.source-grid dd.source-claim` and `.source-card` hover

- [ ] **Step 1: Find the existing source-card rules**

```bash
grep -n "source-grid dd.source-claim\|source-card:hover" build/spa_template.html
```

- [ ] **Step 2: Apply polish**

Change `font-weight: 500` to `font-weight: 600` on `.source-grid dd.source-claim` (around line 800).

Add a `transition: box-shadow 0.15s ease` to the base `.source-card` rule (around line 734).

Verify on mobile that the 4px category-colored left border is visible — read `.source-card[data-cat="..."]` rules (~line 766-770). They use `border-left-color` which only works if there IS a left border. Add `border-left-width: 4px` to the base `.source-card` rule if not already present.

- [ ] **Step 3: Rebuild and visually check at 375px**

Add to the verify script (inside the per-viewport loop):

```javascript
      if (vp.name === 'mobile' && theme === 'light') {
        await page.locator('article.source-card').first().scrollIntoViewIfNeeded();
        await page.waitForTimeout(150);
        await page.locator('article.source-card').first().screenshot({
          path: path.join(SHOTS_DIR, 'source-card_mobile_light.png'),
        });
      }
```

```bash
node build/tests/verify_feedback_pass.js
```

Spot-check `source-card_mobile_light.png` — the colored left border should be visible.

- [ ] **Step 4: Commit** (deferred — bundled into commit 2)

---

## Task 12: Hero control-thesis dek

**Files:**
- Modify: `build/spa_template.html` — `.article-header` block + `.article-dek` CSS

- [ ] **Step 1: Insert the dek in `.article-header`**

In `build/spa_template.html`, find lines 1772-1776:

```html
    <main class="article" id="top">
      <header class="article-header">
        <h1 class="article-title">{{TITLE}}</h1>
        <p class="article-subtitle">{{SUBTITLE}}</p>
        <div class="article-author"><a href="#contact">{{AUTHOR}}</a></div>
      </header>
```

Insert the dek between subtitle and author:

```html
    <main class="article" id="top">
      <header class="article-header">
        <h1 class="article-title">{{TITLE}}</h1>
        <p class="article-subtitle">{{SUBTITLE}}</p>
        <p class="article-dek">Agentic software delivery is not a tooling problem. It is a control problem: control the context, control the actions, control the verification, control the adoption surface.</p>
        <div class="article-author"><a href="#contact">{{AUTHOR}}</a></div>
      </header>
```

- [ ] **Step 2: Add CSS for `.article-dek`**

Find the `.article-subtitle` rule (~line 422). After it, add:

```css
    .article-dek {
      font-size: 18px;
      font-weight: 400;
      color: var(--color-text-soft);
      max-width: 640px;
      margin: 20px auto 28px;
      text-align: center;
      line-height: 1.5;
    }
    @media (max-width: 480px) {
      .article-dek { font-size: 16px; margin: 16px auto 22px; }
    }
```

- [ ] **Step 3: Assertion in verify script**

```javascript
      // Hero dek: present in article-header with the control-thesis text.
      if (theme === 'light' && vp.name === 'desktop') {
        const dek = await page.locator('header.article-header .article-dek').textContent();
        if (!dek || !/control problem/i.test(dek)) {
          fail(`hero dek missing or doesn't contain "control problem": ${JSON.stringify(dek)}`);
        } else ok('hero dek present');
      }
```

- [ ] **Step 4: Rebuild and run**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: assertion passes. Open `hero_desktop_light.png` and `hero_mobile_light.png` — the dek should sit between the subtitle and the author byline.

- [ ] **Step 5: Commit** (deferred — bundled into commit 2)

---

## Task 13: Top CTA row

**Files:**
- Modify: `build/spa_template.html` — `.article-header` (CTA nav) + CSS

- [ ] **Step 1: Insert the CTA nav into the hero**

Right after the `.article-author` div in `.article-header`, add:

```html
        <nav class="hero-cta" aria-label="Quick start">
          <a class="cta-primary" href="#chapter-7">Start with the architecture review</a>
          <a class="cta-secondary" href="#appendix-b">Download the templates</a>
          <a class="cta-secondary" href="mailto:info@ship-it-with.ai?subject=Agentic%20delivery%20assessment">Book an assessment</a>
        </nav>
```

- [ ] **Step 2: Add CSS for `.hero-cta` + buttons**

After the `.article-dek` rule from Task 12:

```css
    .hero-cta {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      justify-content: center;
      align-items: center;
      margin: 24px auto 0;
      max-width: 720px;
    }
    .hero-cta a {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-family: inherit;
      font-size: 15px;
      font-weight: 600;
      letter-spacing: 0.01em;
      text-decoration: none;
      padding: 12px 20px;
      border-radius: 6px;
      transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
    }
    .cta-primary {
      background: var(--color-accent);
      color: white;
      border: 1.5px solid var(--color-accent);
    }
    .cta-primary:hover { background: #b45309; border-color: #b45309; }
    .cta-secondary {
      background: transparent;
      color: var(--color-accent);
      border: 1.5px solid var(--color-accent);
    }
    .cta-secondary:hover { background: var(--color-accent-soft); }
    .hero-cta a:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }
    @media (max-width: 640px) {
      .hero-cta { flex-direction: column; align-items: stretch; }
      .hero-cta a { width: 100%; }
    }
    @media (prefers-reduced-motion: reduce) {
      .hero-cta a { transition: none; }
    }
```

- [ ] **Step 3: Assertion in verify script**

```javascript
      // Hero CTA row: three buttons in the hero with correct targets.
      if (theme === 'light' && vp.name === 'desktop') {
        const ctas = await page.locator('nav.hero-cta a').all();
        if (ctas.length !== 3) fail(`expected 3 hero CTAs, got ${ctas.length}`);
        const hrefs = await Promise.all(ctas.map(c => c.getAttribute('href')));
        const expected = ['#chapter-7', '#appendix-b', /^mailto:info@ship-it-with\.ai\?subject=/];
        for (let i = 0; i < 3; i++) {
          const h = hrefs[i] || '';
          const want = expected[i];
          const ok_ = (want instanceof RegExp) ? want.test(h) : h === want;
          if (!ok_) fail(`hero CTA ${i} href: got ${h}, want ${want}`);
        }
        if (process.exitCode !== 1) ok('hero CTA row: 3 correct targets');
      }

      // Mobile CTA stack: buttons full-width.
      if (theme === 'light' && vp.name === 'mobile') {
        const firstCta = page.locator('nav.hero-cta a').first();
        const box = await firstCta.boundingBox();
        if (box && box.width < vp.width * 0.7) fail(`mobile CTA not stacked full-width: ${box.width}px on ${vp.width}px viewport`);
        else ok('mobile CTAs stacked');
      }
```

- [ ] **Step 4: Rebuild and run**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: all CTA assertions pass. Open `hero_desktop_light.png` and `hero_mobile_light.png` to spot-check.

- [ ] **Step 5: Commit** (deferred — bundled into commit 2)

---

## Task 14: Print stylesheet — extend for new callouts

**Files:**
- Modify: `build/spa_template.html` — `@media print` block (~line 1721)

- [ ] **Step 1: Find and extend the print rule**

```bash
grep -n "@media print" build/spa_template.html
```

Find the line: `.action-box, .try-box, .case-note, figure.diagram { break-inside: avoid; box-shadow: none; }`. Change to:

```css
      .action-box, .try-box, .case-note, .artifact-box, .source-note, figure.diagram { break-inside: avoid; box-shadow: none; }
```

- [ ] **Step 2: Rebuild — no test (print stylesheet is hard to assert)**

```bash
python3 build/build_spa.py
grep -c "\.artifact-box, \.source-note" index.html
```

Expected: `>= 1`.

- [ ] **Step 3: Commit COMMIT 2**

All changes for commit 2 are now in place. Stage and commit:

```bash
git status
git add build/spa_template.html build/build_spa.py build/tests/verify_feedback_pass.js build/tests/lib/build_and_open.js index.html
git commit -m "feat: source-note + artifact-box callouts, hero dek + CTA row, Appendix C polish

Adds two new styled callout components (.source-note, .artifact-box) with
build-script wrappers that match the existing markdown patterns. Hero gains a
control-thesis dek and a 3-button CTA row (architecture review, templates,
assessment). Chapter-end stack tightened by dropping trailing <hr/> from the
existing wrappers and using CSS sibling selectors. Print stylesheet extended
for the new components. Mobile-first padding and dark-mode variants for all
new components. Adds build/tests/verify_feedback_pass.js for screenshot-based
verification across desktop / tablet / mobile in both themes."
```

---

# COMMIT 3 — Content & structure

## Task 15: Foreword bio trim

**Files:**
- Modify: `source/Ship_It_With_AI.md` — replace the body of `### Where I am coming from {#where-i-am-coming-from}`

- [ ] **Step 1: Locate the section**

The heading is at `source/Ship_It_With_AI.md:99`. Body spans lines 100-115. The `<a id="contact"></a>` anchor is on line 113.

- [ ] **Step 2: Replace the body**

Replace lines 100-115 with this 4-sentence version. **Important:** do NOT keep the `<a id="contact"></a>` here — it moves to the new About section in Task 16.

```markdown
### Where I am coming from {#where-i-am-coming-from}

I have been writing software professionally since 2000 and building AI systems for more than a decade. I have used every generation of coding assistant, from early IDE intelligence to Copilot to current coding agents, and I have spent the last eighteen months watching production teams adopt agentic workflows well and badly. This manual is the result of the patterns that survived repeated use across real teams.

[Full background: About the author.](#about-the-author)

---
```

(The trailing `---` is the section separator that was already there; preserve it.)

- [ ] **Step 3: Rebuild**

```bash
python3 build/build_spa.py
```

- [ ] **Step 4: Spot-check**

```bash
grep -A 6 "Where I am coming from" index.html | head -20
```

The rendered subsection should show 3 short paragraphs (2 substantive + the link).

- [ ] **Step 5: Commit** (deferred — bundled into commit 3)

---

## Task 16: Add the About-the-author section + move the contact anchor

**Files:**
- Modify: `source/Ship_It_With_AI.md` — insert new section after `## Acknowledgments`, before `## Appendix A.`
- Modify: `build/build_spa.py` — TOC builder to include About in the index

- [ ] **Step 1: Locate the insertion point**

```bash
grep -n "^## Acknowledgments\|^## Appendix A" source/Ship_It_With_AI.md
```

The new section goes between them.

- [ ] **Step 2: Insert the About section**

Insert this BLOCK right after the Acknowledgments section ends and before `## Appendix A. Cost Economics`. The section combines the full bio (the original ~7 paragraphs from the foreword) plus the contact paragraph. Copy the original bio paragraphs from Task 15's "before" state — they're the long version (lines 100-112 of the pre-trim source).

```markdown
## About the author {#about-the-author}

The shape of a manual depends on the shape of the writer, and you deserve to know whether the writer's experience is the kind of experience that maps to your situation.

I first met a computer in my parents' office around 1984, when I was six - a mainframe room with a raised floor, Space Invaders running on a terminal, and an introduction to BASIC. I wrote my first programs in BASIC in 1989. Borland Pascal in DOS followed in 1993, then Visual Basic, the first real IDE I used and the first language I sold software in as a teenager. My professional career started in 2000 as IT Manager for a manufacturing company. In 2001 I moved into software engineering proper, joining a startup that built multicasting software for satellite operators running DVB. When the startup lost its investors and pivoted to outsourcing, I switched from C++ to .NET, and spent the next two decades, through 2023, delivering for customers across industries on Visual Studio.NET and its descendants. I am, by training and inclination, an engineer first and a consultant second; the consulting work is the secondary outgrowth of doing engineering with teams who want help.

My interest in machine learning started around 2013. The first serious deep dive came in late 2015, when I ported DarkNet and YOLO onto an XR headset; that is when I started building AI applications professionally. In 2023 I joined a company building the first neuromorphic SoC, working on the nano-ML end of the field. On the assisted-coding side, I have used every generation: Whole Tomato's Visual Assist (the first intelligent coding assistant I ever installed), the early JetBrains tooling in the .NET world, the first releases of Copilot, and LLMs for coding since the day ChatGPT first shipped. I have not built my own coding agent. I have used most of the ones that ship now, and I have watched a lot of teams use them.

The manual draws on this trajectory. The methodology I describe has been refined across dozens of engagements with teams of varying sizes, in varying industries, in varying states of agentic readiness. The frames I share are the ones that have held up across the engagements; the ones that did not hold up have been retired. This is not the first set of frames I wrote about agentic delivery. It is the third or fourth iteration. The earlier iterations were wrong in interesting ways. This one is, I hope, less wrong.

I am not neutral about the topic. I think agentic software delivery is the most consequential shift in our field since the introduction of high-level programming languages. I also think the way most teams are currently adopting it is doing them more harm than good. Both of those things can be true. The point of the manual is to help you adopt in a way that captures the upside without the harm. The frameworks are how.

That trajectory - four decades of writing code, twenty-five of them professional, more than a decade building AI systems, every generation of coding assistant in between - is the trajectory the manual is written from. Calibrate your expectations accordingly.

<a id="contact"></a>
*Contact: [info@ship-it-with.ai](mailto:info@ship-it-with.ai) for technical conversations or tailored workshops, in-person or online, shaped to your team's codebase and constraints. Find me on [LinkedIn](https://www.linkedin.com/in/mihaicvasnievschi/). For executive and non-technical leadership audiences, the sister practice at [ai-leaders.ro](https://ai-leaders.ro) covers the adoption side without the engineering depth.*

---
```

- [ ] **Step 3: Verify the existing TOC-related regex handles `## About the author`**

The `BREAK_RE` at `build/build_spa.py:403` looks like:

```python
r"(?m)^(?:## Chapter \d+\b|# Part [IVX]+\b|# Closing\b|## Appendix [A-Z]\.)"
```

`## About the author` matches none of these. Add it:

```python
r"(?m)^(?:## Chapter \d+\b|# Part [IVX]+\b|# Closing\b|## Appendix [A-Z]\.|## About the author\b)"
```

- [ ] **Step 4: Add About to the TOC builder**

Find `build_toc()` in `build/build_spa.py` (~line 641). After the "Closing" block and before the "Appendices" block, add an explicit About entry:

```python
    # About the author (sits between Closing and Appendices).
    sections.append('<div class="toc-section">')
    sections.append('<div class="toc-section-title"><a href="#about-the-author">About the author</a></div>')
    sections.append("</div>")
```

- [ ] **Step 5: Rebuild and verify the About section is present**

```bash
python3 build/build_spa.py
grep -c "id=\"about-the-author\"" index.html
grep -c "href=\"#about-the-author\"" index.html
```

Expected: each `>= 1` (the section heading once, the TOC link + the foreword link).

- [ ] **Step 6: Add a Playwright assertion**

In `build/tests/verify_feedback_pass.js`, add:

```javascript
      // About-the-author section: heading + #contact anchor present.
      if (theme === 'light' && vp.name === 'desktop') {
        const about = page.locator('#about-the-author');
        if (await about.count() !== 1) fail('#about-the-author heading missing');
        else ok('#about-the-author present');

        const contact = page.locator('#contact');
        if (await contact.count() !== 1) fail('#contact anchor missing (should be inside About)');
        else ok('#contact anchor present in About');

        const aboutLink = page.locator('#where-i-am-coming-from ~ p a[href="#about-the-author"]');
        if (await aboutLink.count() < 1) fail('foreword "About the author" link missing');
        else ok('foreword links to About');
      }
```

- [ ] **Step 7: Run**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: all About assertions pass.

- [ ] **Step 8: Commit** (deferred — bundled into commit 3)

---

## Task 17: AGENTS.md de-linking

**Why:** Reviewer flagged repeated `[AGENTS.md](https://agents.md/)` links as noisy. Keep first occurrence per chapter; unwrap the rest.

**Files:**
- Modify: `build/build_spa.py` — add `delink_repeated_agents_md(html)` post-processor and call it in the pipeline

- [ ] **Step 1: Inspect current AGENTS.md link density**

```bash
python3 build/build_spa.py
grep -c 'href="https://agents.md/"' index.html
```

Note the count.

- [ ] **Step 2: Implement the de-linker**

In `build/build_spa.py`, add this function near the other transforms:

```python
AGENTS_LINK_RE = re.compile(r'<a href="https://agents\.md/?"[^>]*>AGENTS\.md</a>')
CHAPTER_SPLIT_RE = re.compile(r'(<h2 id="chapter-\d+"[^>]*>)')


def delink_repeated_agents_md(html: str) -> str:
    """Keep only the first AGENTS.md link per chapter; unwrap subsequent ones."""
    parts = CHAPTER_SPLIT_RE.split(html)
    out = [parts[0]]
    i = 1
    while i < len(parts):
        h2 = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        seen = {"flag": False}

        def keep_first(m):
            if seen["flag"]:
                return "AGENTS.md"
            seen["flag"] = True
            return m.group(0)

        new_body = AGENTS_LINK_RE.sub(keep_first, body)
        out.extend([h2, new_body])
        i += 2

    return "".join(out)
```

Add the call in the pipeline (in `main`) after the existing transforms and before TOC build:

```python
    html = delink_repeated_agents_md(html)
```

- [ ] **Step 3: Verify the count dropped**

```bash
python3 build/build_spa.py
grep -c 'href="https://agents.md/"' index.html
```

Expected: at most 1 per chapter that mentions AGENTS.md (Ch 6 will likely have 1, plus the appendix B.2 reference if present). Should be significantly fewer than before.

- [ ] **Step 4: Add a Playwright assertion**

In `build/tests/verify_feedback_pass.js`:

```javascript
      // AGENTS.md de-linking: per chapter, at most one link.
      if (theme === 'light' && vp.name === 'desktop') {
        const tooMany = await page.evaluate(() => {
          const chapters = Array.from(document.querySelectorAll('h2[id^="chapter-"]'));
          for (let i = 0; i < chapters.length; i++) {
            const start = chapters[i];
            const end = chapters[i + 1] || null;
            const links = [];
            let n = start.nextElementSibling;
            while (n && n !== end) {
              if (n.querySelectorAll) {
                n.querySelectorAll('a[href^="https://agents.md"]').forEach(a => links.push(a));
              }
              n = n.nextElementSibling;
            }
            if (links.length > 1) return { chapter: start.id, count: links.length };
          }
          return null;
        });
        if (tooMany) fail(`chapter ${tooMany.chapter} has ${tooMany.count} AGENTS.md links (max 1)`);
        else ok('AGENTS.md links: <= 1 per chapter');
      }
```

- [ ] **Step 5: Run**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: assertion passes.

- [ ] **Step 6: Commit** (deferred — bundled into commit 3)

---

## Task 18: Per-section copy-link anchors

**Why:** Reviewer asked for per-section copy-link anchors on every artifact, plus heading anchors. Spec scope: every `h2`/`h3` in chapter bodies + every `.artifact-box`.

**Files:**
- Modify: `build/build_spa.py` — add `inject_anchor_links(html)` post-processor and ensure each `.artifact-box` gets an `id`
- Modify: `build/spa_template.html` — `.anchor-link` CSS + clipboard JS in the script block

- [ ] **Step 1: Add `id` to each artifact-box during the wrap**

Update `transform_artifacts` in `build/build_spa.py` (added in Task 9). Add a counter to the function so each artifact gets a unique id:

```python
def transform_artifacts(html: str) -> str:
    counter = {"n": 0}

    def repl(m):
        counter["n"] += 1
        slug = f"artifact-{counter['n']}"
        title = m.group("title").strip()
        body = m.group("body").strip()
        return (
            f'<aside class="artifact-box" id="{slug}">'
            '<div class="artifact-header">'
            f'{CLIPBOARD_SVG}'
            '<span class="artifact-label">Artifact</span>'
            '</div>'
            f'<h4 class="artifact-title">{title}</h4>'
            f'<p>{body}</p>'
            '</aside>'
        )
    return ARTIFACT_RE.sub(repl, html)
```

- [ ] **Step 2: Add the anchor-link injector**

In `build/build_spa.py`, add:

```python
HEADING_RE = re.compile(
    r'<(?P<tag>h2|h3) id="(?P<id>[^"]+)"(?P<attrs>[^>]*)>(?P<inner>.*?)</(?P=tag)>',
    re.DOTALL,
)
ARTIFACT_HEADER_RE = re.compile(
    r'(<aside class="artifact-box" id="(?P<aid>artifact-\d+)">\s*<div class="artifact-header">)',
    re.DOTALL,
)
SKIP_IDS = {'top', 'contact', 'about-the-author'}


def inject_anchor_links(html: str) -> str:
    """Add `<a class="anchor-link" href="#id">¶</a>` to h2/h3 and artifact-boxes.

    Preserves existing markdown {#anchor} ids (the markdown extension already set them).
    Skips ids in SKIP_IDS to avoid noise on the byline target and the About heading.
    """
    def head_repl(m):
        hid = m.group('id')
        if hid in SKIP_IDS:
            return m.group(0)
        tag = m.group('tag')
        attrs = m.group('attrs')
        inner = m.group('inner')
        anchor = f'<a class="anchor-link" href="#{hid}" aria-label="Copy link to section" tabindex="0">¶</a>'
        return f'<{tag} id="{hid}"{attrs}>{inner}{anchor}</{tag}>'

    html = HEADING_RE.sub(head_repl, html)

    def art_repl(m):
        aid = m.group('aid')
        anchor = f'<a class="anchor-link" href="#{aid}" aria-label="Copy link to artifact" tabindex="0">¶</a>'
        return m.group(1) + anchor

    html = ARTIFACT_HEADER_RE.sub(art_repl, html)
    return html
```

Add the call to the pipeline AFTER `transform_artifacts` and before TOC build:

```python
    html = inject_anchor_links(html)
```

- [ ] **Step 3: Add `.anchor-link` CSS**

In `build/spa_template.html`, add (near the existing `.chapter-heading` rules, or with the new components):

```css
    /* Per-section anchor links. Visible on hover (desktop) / always (touch). */
    .anchor-link {
      display: inline-block;
      margin-left: 8px;
      opacity: 0;
      color: var(--color-text-muted);
      text-decoration: none;
      font-size: 0.85em;
      vertical-align: baseline;
      transition: opacity 0.15s ease, color 0.15s ease;
    }
    h2:hover .anchor-link,
    h3:hover .anchor-link,
    aside.artifact-box:hover .anchor-link,
    .anchor-link:focus-visible {
      opacity: 1;
    }
    .anchor-link:hover { color: var(--color-accent); }
    @media (hover: none) {
      .anchor-link { opacity: 0.5; }
    }
    @media (prefers-reduced-motion: reduce) {
      .anchor-link { transition: none; }
    }
    .anchor-toast {
      position: fixed;
      bottom: 32px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--color-text);
      color: var(--color-bg);
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
      z-index: 1000;
    }
    .anchor-toast.show { opacity: 1; }
```

- [ ] **Step 4: Add clipboard JS**

Find the existing `<script>` block (search for `themeToggle`) and add inside its scope:

```javascript
      (function(){
        let toast = null;
        function showToast() {
          if (!toast) {
            toast = document.createElement('div');
            toast.className = 'anchor-toast';
            toast.textContent = 'Link copied';
            document.body.appendChild(toast);
          }
          toast.classList.add('show');
          setTimeout(() => toast.classList.remove('show'), 1400);
        }
        document.addEventListener('click', (e) => {
          const a = e.target.closest('a.anchor-link');
          if (!a) return;
          e.preventDefault();
          const href = a.getAttribute('href');
          const url = window.location.origin + window.location.pathname + href;
          history.replaceState(null, '', href);
          if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(showToast, showToast);
          } else {
            showToast();
          }
        });
      })();
```

- [ ] **Step 5: Add a Playwright assertion**

In `build/tests/verify_feedback_pass.js`:

```javascript
      // Anchor links: at least one on a chapter h2 and one on an artifact-box.
      if (theme === 'light' && vp.name === 'desktop') {
        const headingAnchors = await page.locator('h2[id^="chapter-"] a.anchor-link').count();
        if (headingAnchors < 10) fail(`expected >= 10 anchor links on chapter h2s, got ${headingAnchors}`);
        else ok(`anchor links on chapter h2s: ${headingAnchors}`);

        const artifactAnchors = await page.locator('aside.artifact-box a.anchor-link').count();
        if (artifactAnchors < 10) fail(`expected >= 10 anchor links on artifact-boxes, got ${artifactAnchors}`);
        else ok(`anchor links on artifact-boxes: ${artifactAnchors}`);

        await page.locator('h2[id^="chapter-"] a.anchor-link').first().click();
        await page.waitForTimeout(200);
        const toastVisible = await page.locator('.anchor-toast.show').count();
        if (!toastVisible) fail('anchor-link click did not show toast');
        else ok('anchor-link click shows toast');
      }
```

- [ ] **Step 6: Run**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: all anchor-link assertions pass.

- [ ] **Step 7: Commit** (deferred — bundled into commit 3)

---

## Task 19: Final no-horizontal-overflow + reading-time sanity assertions

**Why:** Catch any layout regressions on mobile and verify reading-time output looks plausible.

**Files:**
- Modify: `build/tests/verify_feedback_pass.js`

- [ ] **Step 1: Add overflow + reading-time assertions**

Inside the per-viewport loop in `build/tests/verify_feedback_pass.js`, add:

```javascript
      // No horizontal scrollbar on any viewport.
      const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
      const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
      if (scrollWidth > clientWidth + 1) {
        fail(`${vp.name}/${theme}: horizontal overflow (scrollWidth ${scrollWidth} > clientWidth ${clientWidth})`);
      } else {
        ok(`${vp.name}/${theme}: no horizontal overflow`);
      }

      // Reading times: every chapter TOC entry should have a non-empty min value.
      if (theme === 'light' && vp.name === 'desktop') {
        const missing = await page.evaluate(() =>
          Array.from(document.querySelectorAll('.toc-list .toc-time'))
            .filter(s => !s.textContent || !/\d+ min/.test(s.textContent)).length
        );
        if (missing > 0) fail(`${missing} chapters have missing/malformed reading-time`);
        else ok('all chapter reading-times present');
      }
```

- [ ] **Step 2: Run**

```bash
node build/tests/verify_feedback_pass.js
```

Expected: all assertions pass; no overflow; reading-times all present.

- [ ] **Step 3: Commit COMMIT 3**

```bash
git status  # Confirm: source/Ship_It_With_AI.md, build/build_spa.py, build/spa_template.html, build/tests/verify_feedback_pass.js, index.html
git add source/Ship_It_With_AI.md build/build_spa.py build/spa_template.html build/tests/verify_feedback_pass.js index.html
git commit -m "feat: trim foreword bio, add About-the-author, de-link AGENTS.md, per-section copy-link anchors

Foreword bio reduces to 4 sentences linking to the new About section that
carries the full background plus the contact paragraph (with the existing
#contact anchor preserved). TOC gets an About-the-author entry between
Closing and Appendices. AGENTS.md links collapse to at most one per chapter.
Every chapter heading and every artifact-box gets a hover-revealed ¶
anchor that copies the absolute URL to the clipboard."
```

---

## Task 20: Final cross-viewport verification + screenshot review

**Why:** Run the full verification one more time end-to-end, review every screenshot, fix any visual regressions before opening the PR.

**Files:** none

- [ ] **Step 1: Clean run**

```bash
rm -rf build/tests/screenshots/feedback-pass
node build/tests/verify_feedback_pass.js
```

Expected: `Verification PASSED.` with no failures.

- [ ] **Step 2: Eyeball every screenshot**

```bash
ls build/tests/screenshots/feedback-pass/
```

You should see (approximately):
- `hero_{mobile,tablet,desktop}_{light,dark}.png` × 6
- `source-note_desktop_{light,dark}.png` × 2
- `artifact_desktop_{light,dark}.png` × 2
- `ch3-end_desktop_light.png`
- `source-card_mobile_light.png`

Open each and verify:
- Hero shows: title → subtitle → dek → author → 3 CTAs in correct stack
- Mobile hero CTAs stack vertically, full-width
- Source-note callouts use cool blue-gray (light) / dark slate (dark) — distinct from sandstone case-notes
- Artifact-boxes use warm-neutral tint with 3px slate left border + clipboard icon
- Ch 3 end stack: artifact → action → try with tightened spacing, no `<hr>` between
- Appendix C source-card on mobile: colored left border visible

- [ ] **Step 3: If any regression is found**

Fix it in the appropriate task's file. Re-run `node build/tests/verify_feedback_pass.js`. If the fix is small, commit as a fix-up commit on the branch.

- [ ] **Step 4: Push the branch and open the PR**

```bash
git push -u origin feedback-pass
gh pr create --title "Feedback-pass polish: TOC + figures + new callouts + hero CTA + bio trim" --body "$(cat <<'EOF'
## Summary
- Three tiered commits implementing the 2026-05-26 feedback pass.
- Commit 1: TOC chapter-to-part map fix, figure numbering dropped, book→manual sweep.
- Commit 2: New `.source-note` and `.artifact-box` callouts, hero control-thesis dek + 3-button CTA row, Appendix C polish, mobile + dark variants.
- Commit 3: Foreword bio trimmed (full version in new About-the-author section), AGENTS.md de-linked, per-section copy-link anchors.
- New `build/tests/verify_feedback_pass.js` validates everything across desktop / tablet / mobile in light + dark.

## Spec
`docs/superpowers/specs/2026-05-26-feedback-pass-design.md`

## Test plan
- [x] Local: `node build/tests/verify_feedback_pass.js` passes
- [x] Visual review of all screenshots in `build/tests/screenshots/feedback-pass/`
- [ ] Reviewer spot-checks the built `index.html` (preview via `python3 -m http.server`)
EOF
)"
```

The CI workflow will rebuild `index.html` from source on merge and deploy to ship-it-with.ai.

---

## Self-review (run by the engineer before opening the PR)

**Spec coverage check:**
- [x] Item 1 TOC mismatch → Task 2
- [x] Item 2 Figure numbering → Tasks 3+4
- [x] Item 3 Title strategy decided no change → no task needed
- [x] Item 4 Workshop pitch out of foreword → Task 15 (removed entirely)
- [x] Item 5 New Source/Artifact callouts → Tasks 8+9
- [x] Item 6 Foreword bio trim + About page → Tasks 15+16
- [x] Item 7 Top CTA row → Task 13
- [x] Item 8 Appendix C polish → Task 11
- [x] Item 9 AGENTS.md de-linking → Task 17
- [x] Item 10 Book→manual sweep → Task 5
- [x] Item 12 Copy-link anchors → Task 18
- [x] Cross-cutting CSS vars → Task 6
- [x] Cross-cutting print stylesheet → Task 14
- [x] Cross-cutting Playwright verification → Tasks 7, 8-19 (assertions accumulated)

**Files touched (verify no orphans):**
- `source/Ship_It_With_AI.md` — Tasks 4, 5, 15, 16
- `build/build_spa.py` — Tasks 2, 4, 8, 9, 16, 17, 18
- `build/spa_template.html` — Tasks 6, 8, 9, 10, 11, 12, 13, 14, 18
- `build/tests/lib/build_and_open.js` — Task 7
- `build/tests/verify_feedback_pass.js` — Tasks 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19
