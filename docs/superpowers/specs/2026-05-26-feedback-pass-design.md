# Feedback-pass polish design — 2026-05-26

A polish pass on the live site (https://ship-it-with.ai) responding to external reviewer feedback. Goal: take the manual from S-minus to S-tier by fixing structural bugs, adding two missing callout components, trimming front-matter, and adding a top CTA row.

The title strategy stays: **Ship It With AI** as the H1 (matching the domain). The reviewer's "Ship It With Agents" rename is explicitly out of scope.

## Scope

In scope (13 items from the feedback):

1. TOC / part mismatch (must-fix)
2. Figure numbering (must-fix)
3. Title strategy — decided, no change (must-fix)
4. Move workshop pitch out of foreword (must-fix)
5. Style Source notes + Artifact callouts as distinct components (must-fix)
6. Shorten "Where I am coming from" in the foreword + new "About the author" section (medium)
7. Top CTA row: architecture review / templates / assessment (medium)
8. Appendix C card polish (medium)
9. AGENTS.md de-linking (medium)
10. Book → manual sweep (medium)
11. (Skipped per user) Rename to "Ship It With Agents"
12. Per-section copy-link anchors on artifacts (low)
13. (Deferred) Downloadable PDF/EPUB

Cross-cutting: Playwright validation across desktop / tablet / mobile, light + dark mode.

## Sequencing — one PR, three tiered commits

Tiered commits allow individual rollback and let work stop at any tier if priorities shift. One PR for review cohesion.

**Commit 1 — Mechanical fixes.** TOC, figures, copy sweep. Pure source/code edits; zero new styling. Lowest risk.

**Commit 2 — New visual components.** Source-note + Artifact callout styles and their build-script wrappers, Appendix C polish, hero control-thesis line, top CTA row, chapter-end stack-margin tightening, dark + mobile variants.

**Commit 3 — Content & structure.** Foreword bio trim, new "About the author" section, AGENTS.md de-linking, copy-link anchors.

**Verification step** (folded into commit 3 or its own commit if regressions are found): Playwright run across viewports, screenshots saved to `build/tests/screenshots/`.

## Architecture

The site is a single-file SPA built by `build/build_spa.py` from `source/Ship_It_With_AI.md` using `build/spa_template.html`. CI rebuilds and stages public files into `_site/` on push to main.

Changes live in three places, each cleanly bounded:

- **`source/Ship_It_With_AI.md`** — content edits, new About section, foreword trim, copy edits, control-thesis text source.
- **`build/spa_template.html`** — new callout CSS (light + dark), hero changes (control-thesis dek, CTA row), stack-margin tightening, mobile breakpoints, copy-link anchor styles.
- **`build/build_spa.py`** — TOC map fix, figure-caption rewrites, source-note + artifact-box wrappers, AGENTS.md de-linker, anchor-link injector.

Verification scripts live in `build/tests/`.

## Component designs

### Commit 1 — Mechanical fixes

#### TOC chapter-to-part map (`build/build_spa.py:648-660`)

Replace the off-by-one hardcoded mapping. The chapter-11 entry is stale and gets dropped.

```python
chapter_to_part = {
    "chapter-1": "part-i", "chapter-2": "part-i", "chapter-3": "part-i",
    "chapter-4": "part-ii", "chapter-5": "part-ii",
    "chapter-6": "part-ii", "chapter-7": "part-ii",
    "chapter-8": "part-iii", "chapter-9": "part-iii", "chapter-10": "part-iii",
}
```

#### Figure numbering

The reviewer recommends dropping numbering for a web manual. Apply in two places:

1. Five hardcoded diagram functions in `build/build_spa.py` (`diagram_primitives`, `diagram_layers`, `diagram_loop`, `diagram_traffic`, `diagram_arc`) — replace `Figure N.N. <text>` with `Figure: <text>` in each `<figcaption>`.
2. The markdown figure-caption regex at `build/build_spa.py:166` — rewrite to accept captions without numbers, and update any captions in `source/Ship_It_With_AI.md` that still use `*Figure X.Y. …*`.

#### Book → manual sweep

Scoped find-and-replace in `source/Ship_It_With_AI.md`. The word "book" appears intentionally in some contexts (titles of referenced works, the phrase "open book"). Approach:

1. List all occurrences.
2. Rewrite the print-era artifacts: the "if I wrote a manual about specific tools, it would be obsolete before the printer finished" sentence becomes *"If this were a tool guide, it would be stale before publication."*
3. Other "book" mentions: keep where intentional (citations, idioms); replace where it refers to the manual itself.

### Commit 2 — New visual components

Both new components incorporate the expert designer's critique: source-note uses a cool blue-gray (not sandstone, to avoid collision with case-notes); artifact-box uses warm-neutral tint (not pure white, which disappears on the warm bg), an SVG clipboard icon (not Unicode), and a 3px left border for "deliverable" weight.

#### `.source-note` — inline body callout

Replaces ~5 `*Source note. <body>*` italic paragraphs in chapters. Less prominent than action/try (an annotation, not a CTA). Cool blue-gray family — separates from sandstone case-notes and reads as "citation/reference".

```html
<aside class="source-note">
  <span class="source-note-label">Source</span>
  <p>METR study published July 2025. The interpretation that workflow discipline is the missing variable is mine, not the study's. Citation in Appendix C.</p>
</aside>
```

CSS (light theme):
- background `#f1f4f8` (cool blue-gray)
- border `1px solid #cbd5e1`
- padding `14px 18px`
- border-radius matches existing callouts
- margin `24px 0` (tighter than the 40px on action/try)
- label badge: slate-filled `#475569`, white text, 11px uppercase letter-spacing 0.12em
- body: italic, 14-15px, color `#475569`

CSS (dark theme):
- background `#1e293b` (cool dark slate, not just darkened sandstone)
- border `#334155`
- label badge: bumped luminance `#94a3b8`
- body: `#cbd5e1`

Build script (`build/build_spa.py`): post-process the rendered HTML to match `<p><em>Source note. (.*?)</em></p>` paragraphs and rewrite them as the `<aside class="source-note">` structure. The literal "Source note." prefix is stripped (it's replaced by the styled badge); the rest of the captured body becomes the inner `<p>`.

#### `.artifact-box` — chapter-ending deliverable

Replaces 10 `**Artifact: <TITLE>.** <body>` bold paragraphs (one per chapter). Card with structural weight — peer of action-box but neutral (deliverable, not CTA).

```html
<aside class="artifact-box">
  <div class="artifact-header">
    <svg class="artifact-icon" viewBox="0 0 16 16" aria-hidden="true">
      <!-- inline clipboard outline -->
    </svg>
    <span class="artifact-label">Artifact</span>
  </div>
  <h4 class="artifact-title">Five-layer governance audit</h4>
  <p>Score each layer for one codebase your team owns: default / configured / enforced / monitored. The audit becomes the baseline for the next quarter's investment.</p>
</aside>
```

CSS (light theme):
- background `#faf8f3` (warm-neutral tint — sits visibly on `--color-bg`)
- border `1px solid var(--color-border-strong)` + 3px left border `#475569` (slate)
- padding `24px 28px`
- border-radius matches existing callouts
- margin `40px 0` (above body), reduced to `24px` when followed by `.action-box` or `.try-box`
- icon: inline SVG, 16px, slate stroke
- label: slate-filled badge, same shape as other labels
- title: 17px semibold with 8px bottom margin

CSS (dark theme):
- background `--color-surface` slightly elevated (lighter than bg) — "card lifts off page"
- left border: lighter slate `#94a3b8`
- icon stroke: `#94a3b8`

Build script: regex-match `<p><strong>Artifact: ([^<]+)\.</strong>(.*?)</p>` and wrap into the structure above. The title is captured between `Artifact:` and the closing period.

#### Chapter-end stack tightening

The existing build script preserves `<hr/>` separators after the action-box and try-box wrappers (`build/build_spa.py:822, 834`). That means siblings are NOT adjacent in the DOM — a CSS `+` selector wouldn't apply. Two options:

1. **Drop the trailing `<hr/>` from the wrappers** when the next sibling is another callout (artifact / action / try). Simpler DOM; `+` selectors work cleanly.
2. **Wrap the chapter-end trio in a `<div class="chapter-coda">`** that the build script emits when it sees the artifact pattern; CSS targets children of `.chapter-coda` for tighter spacing.

Picking option 1 (smaller code change): extend the action-box and try-box wrap regexes to consume the trailing `<hr/>` only when the next non-whitespace HTML node isn't another `<aside>` callout. Then the general-sibling CSS works:

```css
.artifact-box + .action-box,
.artifact-box + .try-box,
.action-box + .try-box {
  margin-top: 24px;
}
```

Optional hairline divider above the trio is **out of scope** for this round — revisit if the stack still feels heavy after viewing the built page.

#### Mobile padding reduction

Under 480px, all four callouts (action, try, artifact, source-note) drop padding to `16px 18px`. Existing case-note already handles this; extend the same media-query block to cover the new components.

#### Appendix C source-card polish

Existing `.source-card` styling stays. Small additions:
- Bump `Claim` row visual weight: existing `font-weight: 500` → `600`.
- Ensure the 4px category left border is visible on mobile (verify in Playwright run).
- Add `transition: box-shadow 0.15s` on hover.

#### Hero control-thesis dek

The actual hero structure in `build/spa_template.html:1772-1776` is `<header class="article-header">` containing title → subtitle → author link. The cover image lives at the END of the article (`.article-cover-end`), not the top.

Insert the dek between `.article-subtitle` and `.article-author`:

```html
<p class="article-subtitle">{{SUBTITLE}}</p>
<p class="article-dek">Agentic software delivery is not a tooling problem. It is a control problem: control the context, control the actions, control the verification, control the adoption surface.</p>
<div class="article-author"><a href="#contact">{{AUTHOR}}</a></div>
```

Styling: 18px regular weight, color `--color-text-soft`, max-width 640px, centered, margin 20px auto 28px. Mobile breakpoint drops to 16px.

#### Top CTA row

Three buttons placed inside `.article-header` after `.article-author`. Internal anchors + mailto (per user decision). The mailto uses `info@ship-it-with.ai` for consistency with the existing footer contact link, and URL-encodes the subject:

```html
<nav class="hero-cta" aria-label="Quick start">
  <a class="cta-primary" href="#chapter-7">Start with the architecture review</a>
  <a class="cta-secondary" href="#appendix-b">Download the templates</a>
  <a class="cta-secondary" href="mailto:info@ship-it-with.ai?subject=Agentic%20delivery%20assessment">Book an assessment</a>
</nav>
```

Styling:
- Primary: filled `--color-accent` background, white text, 12px×20px padding, 6px border-radius
- Secondaries: 1.5px outline `--color-accent`, transparent bg, accent text, same dimensions
- Desktop: horizontal flex with 12px gap, centered
- Mobile (<640px): vertical stack, full-width buttons

The first CTA anchors to `#chapter-7` (the architecture review chapter); the Try-it-yourself anchor inside Ch 7 will get its own id during the copy-link-anchor pass so this can be sharpened in commit 3 if desired.

### Commit 3 — Content & structure

#### Foreword bio trim

Current "Where I am coming from" subsection (~600 words covering BASIC in 1989, Borland, .NET, DarkNet/YOLO, XR, neuromorphic SoC) shortens to 3-4 sentences. The heading itself stays (`### Where I am coming from {#where-i-am-coming-from}`), so the existing hardcoded TOC entry at `build/build_spa.py:677` keeps working without changes. Suggested replacement (user to polish on review):

> I have been writing software professionally since 2000 and building AI systems for more than a decade. I have used every generation of coding assistant, from early IDE intelligence to Copilot to current coding agents, and I have spent the last eighteen months watching production teams adopt agentic workflows well and badly. This manual is the result of the patterns that survived repeated use across real teams. [Full background: About the author.](#about-the-author)

The contact/workshop sentence currently in this subsection is **removed entirely** from the foreword (per the reviewer's point that the footer already carries the same info); the full version moves to the About section.

#### New "About the author" section

Inserted as a top-level `## About the author {#about-the-author}` heading after `## Acknowledgments` and before `## Appendix A.` Contains:
- The full bio (everything currently in "Where I am coming from").
- The contact/workshop sentence.
- Anchor: `#about-the-author`.

The TOC builder (`build/build_spa.py:build_toc`) currently has hardcoded sections for Front Matter / Prologue / Parts / Closing / Appendices, with no "About" slot. Add an explicit entry in the Closing block (or a new "About" block between Closing and Appendices) so the section is reachable from the TOC. The book's `closing` and `appendices` detection in `build/build_spa.py:403` will need a `## About the author` allowance — verify whether the existing regex catches it or needs an extra branch.

#### AGENTS.md de-linking

Build-script post-processor: scan rendered HTML chapter by chapter (using `## Chapter` boundaries). For each chapter, keep the first `<a href="https://agents.md/">AGENTS.md</a>` link; unwrap subsequent ones to plain `AGENTS.md`.

Implementation sketch: after markdown rendering, split on chapter boundaries, walk each chapter's HTML once, track a `seen` flag per chapter.

#### Per-section copy-link anchors

Add `<a class="anchor-link" href="#slug" aria-label="Copy link to section">¶</a>` adjacent to:
- Every `<h2>` and `<h3>` in chapter bodies (skip TOC, hero, foreword subsections that already have ids)
- Every `.artifact-box` (artifacts only, per the reviewer's "every artifact" wording — action and try boxes are excluded to keep visual noise down)

Each artifact-box gains an `id="artifact-<chapter-slug>"` during the wrap step so the anchor can target it.

CSS:
- Default opacity 0
- Parent `:hover .anchor-link { opacity: 1 }` on desktop
- Always visible on touch (`@media (hover: none)`)
- Color `--color-text-muted`, transitions to `--color-accent` on hover

JavaScript: on click, write the absolute URL with hash to clipboard and flash a brief "Copied" tooltip (existing toast infrastructure if any, otherwise a small inline span).

### Cross-cutting implementation notes

These apply across multiple commits — calling them out so they don't get dropped at implementation time.

**CSS variables for new colors.** The existing system defines every color as a `--color-*` CSS var with light + dark pairs. The new callouts should follow suit instead of using inline hex:

```css
:root {
  --color-source-bg: #f1f4f8;
  --color-source-border: #cbd5e1;
  --color-source-text: #475569;
  --color-source-label-bg: #475569;
  --color-artifact-bg: #faf8f3;
  --color-artifact-accent: #475569;
  --color-artifact-icon: #475569;
}
[data-theme="dark"] {
  --color-source-bg: #1e293b;
  --color-source-border: #334155;
  --color-source-text: #cbd5e1;
  --color-source-label-bg: #94a3b8;
  --color-artifact-bg: #232629;  /* surface-elevated, slightly lighter than dark bg */
  --color-artifact-accent: #94a3b8;
  --color-artifact-icon: #94a3b8;
}
```

The component CSS references these vars only.

**Print stylesheet.** The existing `@media print` block at `build/spa_template.html:1721` handles `.action-box, .try-box, .case-note, figure.diagram { break-inside: avoid; box-shadow: none; }`. Extend it to `.artifact-box, .source-note` so the new components print correctly (no cut-off boxes, no shadow rendering issues).

**Markdown `{#anchor}` preservation.** Foreword H3s use `### Heading {#explicit-anchor}` syntax. The anchor-link injector must read the existing `id` attribute (set by the markdown extension) rather than re-slugifying — otherwise it will overwrite or duplicate ids and break existing TOC links.

**Search index.** The build script computes a search index over rendered text (`build/build_spa.py:478, build_search_index`). The wrapped Source-note and Artifact content is still plain text inside the new `<aside>` elements, so the index should pick it up automatically — but verify after the wrap step: open `index.html`, search for "METR" (source note) and "Five-layer governance audit" (artifact title); both must return hits. Also confirm the new About-the-author content is indexed.

**Reading-time recomputation.** `build/build_spa.py` computes per-chapter reading times from word counts. Adding the About section + trimming the foreword changes counts; the build will recompute automatically. No code change needed — just verify the TOC time estimates look sane after the build.

**Accessibility.**
- CTA buttons get visible focus rings (2px outline `--color-accent` with 2px offset). Test with keyboard Tab navigation.
- Anchor-link `¶` symbols get `aria-label="Copy link to section"` (already in the spec) plus `tabindex="0"` so they're keyboard-reachable.
- `@media (prefers-reduced-motion: reduce)` disables the opacity transition on anchor-links and any hover transitions added in this pass.

**Dark mode toggle in Playwright.** The site stores theme in localStorage and applies `data-theme="dark"` to the document. The verification script switches modes via:
```js
await page.evaluate(() => { localStorage.setItem('theme', 'dark'); document.documentElement.setAttribute('data-theme', 'dark'); });
await page.reload();
```
Mirror for light mode. Set this before each screenshot.

**Verify script commits.** The `build/tests/verify_feedback_pass.js` file is created as part of **commit 2** (alongside the new visual components it exercises) so any later commit can re-run it. Commit 3 adds steps for the structural changes (About section, copy-link anchors). The script is run *after* each commit during local development; CI is not modified to run Playwright in this round (deferred).

**Existing Ship-this-week / Try-it-yourself styling.** The reviewer flagged these as visually weak, but they ARE styled in `build/spa_template.html:636-683`. We're not redesigning them in this round — only tightening their stack margins next to the new artifact-box. If they still feel weak after the build, that's a follow-up pass, not part of this spec.

### Playwright verification

New file: `build/tests/verify_feedback_pass.js`. Uses the existing puppeteer setup (currently in `build/tests/`). Runs against the built `index.html` via `file://`.

Viewports:
- 375 × 812 (mobile)
- 768 × 1024 (tablet)
- 1280 × 800 (desktop)

For each viewport, in both light and dark mode:
1. Load page, wait for fonts.
2. Screenshot the hero (verifies CTA row + dek render correctly).
3. Scroll to Ch 3 Governance, screenshot the chapter end (verifies artifact-box + action-box + try-box stack).
4. Scroll to a source-note instance (Ch 4 around the METR paragraph), screenshot.
5. Open Appendix C, screenshot first source-card (verifies polish).
6. Check TOC: assert Part II contains chapters 4-7, Part III contains 8-10.
7. Click an anchor link, verify clipboard write (or skip if clipboard API blocked in headless).
8. Assert no horizontal overflow at 375px.

Output: screenshots into `build/tests/screenshots/feedback-pass/` with viewport+mode in filename. Exit non-zero if any assertion fails.

Run command: `node build/tests/verify_feedback_pass.js` (existing pattern).

## Data flow

```
source/Ship_It_With_AI.md  ─┐
                            ├─► build/build_spa.py ──► index.html ──► (CI staged) ──► _site/ ──► Pages
build/spa_template.html ────┤                                                                   
                            ▼
                   transforms applied in order:
                   1. markdown → html
                   2. figure placeholder injection (no numbering)
                   3. source-note wrapping
                   4. artifact-box wrapping
                   5. action-box / try-box wrapping (existing)
                   6. case-note wrapping (existing)
                   7. AGENTS.md de-linking
                   8. anchor-link injection
                   9. Appendix C source-card transform (existing)
                   10. TOC build (with corrected chapter_to_part map)
                   11. template render (with hero dek + CTA row)
```

## Error handling

- TOC map: if a chapter slug exists in the source but is missing from the map, log a warning and place it under Part I as fallback (so the build doesn't fail silently when new chapters are added).
- Source-note / Artifact regex: if the wrapper doesn't match (e.g., the markdown drifts), log how many were wrapped vs how many `Source note.` / `Artifact:` strings remain in the rendered HTML. Build still completes.
- AGENTS.md de-linker: idempotent; safe to run twice.
- Playwright: fail fast on assertion errors; screenshots from successful steps still saved.

## Testing

Manual: build locally, open `index.html`, spot-check the hero, Ch 3 end, Ch 4 source note, Appendix C, mobile DevTools at 375px.

Automated: `node build/tests/verify_feedback_pass.js` per the spec above. Should pass on all 6 viewport×mode combinations before merge.

## Out of scope

- "Ship It With Agents" title rename
- Separate /about.html route (single SPA section instead)
- External destinations for CTAs (calendar URL, PDF download) — internal anchors + mailto only
- PDF/EPUB generation
- Per-section copy-link anchors on Ship-this-week / Try-it-yourself boxes (artifacts and headings only)
- Optional hairline divider above chapter-end stack (revisit after seeing the built page)

## Resolved decisions (defaults applied — flag in review if you want to change)

1. **Foreword bio wording**: use the reviewer's suggested copy verbatim as the starting point. You can rewrite in your voice during the diff review for commit 3.
2. **CTA first button anchor**: `#chapter-7` (chapter top), not a deeper anchor. Simpler; no dependency on the copy-link-anchor pass landing first.
3. **Hairline divider above chapter-end stack**: deferred (already in out-of-scope).
4. **Mailto address for "Book an assessment"**: `info@ship-it-with.ai` (matches the footer).
5. **`#contact` anchor in author byline**: the anchor exists at `source/Ship_It_With_AI.md:113` (`<a id="contact"></a>`) inside the bio. Since the bio is being trimmed, the anchor must move to the new About-the-author section so the byline link keeps working. No template change needed.
