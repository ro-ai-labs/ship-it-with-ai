# SEO pass design — 2026-05-26

A two-part SEO improvement pass on ship-it-with.ai: bake on-page signals around the primary keyword "agentic coding" into the existing template, then evolve the build pipeline from one big SPA into a tree of per-chapter pages plus a preserved single-page reading mode. Goal: take the manual from an unrankable one-URL surface to a ~18-URL topical authority hub positioned as the vendor-neutral methodology reference.

Driven by findings from three parallel SEO research agents (technical audit, keyword/intent, competitive/distribution). The positioning bet, validated by the keyword agent: nobody currently owns the methodology-first, vendor-neutral slot — the SERP is vendor-glossary-dominated (Google Cloud, IBM, Apiiro, Anthropic) plus practitioner blogs. The site has the content; it lacks the surface and the structure.

## Scope

In scope (this pass):
- **Tier 1 — On-page fixes.** Title and H1 carry "agentic coding"; demote stray H1s to H2; rewrite landing dek to lead with the phrase; schema upgrade to `TechArticle` + `Book` + `FAQPage` + `BreadcrumbList` + `Organization`; internal anchor text variation; cover.jpg → cover.webp at 1200×630; dynamic dateModified stamped at build time; custom 404 page; llms.txt; render-blocking CSS split.
- **Tier 2 — Per-chapter URL split.** Generate ~17 per-chapter / per-appendix / per-About URLs from the same source, each with unique title + meta + canonical + breadcrumbs + prev/next nav. Preserve the all-in-one SPA at `/read/` for one-page reading and to keep existing `#anchor` bookmarks working.
- **Build pipeline refactor.** Build script becomes a generator that emits to `_site/` directly; workflow stops staging files manually; `index.html` at the repo root is no longer committed (it's a build artifact).
- **Verification harness** (`build/tests/verify_seo_pass.js`) covering desktop / tablet / mobile in light + dark mode.

Out of scope (separate specs):
- Three Tier 3 standalone landing pages (vs vibe coding, AGENTS.md field guide, 90-day rollout plan).
- Tier 4 outreach drafts (HN post, Simon Willison email, agents.md PR, podcast/conference pitches).
- Postmortem Library microsite.
- Renaming the 4 anchor URL slugs that still contain "book" (`#how-to-read-this-book` etc.) — preserved per earlier feedback-pass decision; doesn't affect new chapter URLs.

## Sequencing — one PR, three tiered commits

Same pattern as the feedback-pass branch: tiered commits in one branch enable individual rollback. One PR for review cohesion.

**Commit 1 — On-page fixes (Tier 1).** Template + script edits on the existing single-`index.html` output: title, H1, dek, schema (Book + Organization + FAQPage), internal anchor text, cover.webp, dynamic dateModified, 404, llms.txt, deferred-CSS extraction. **No URL changes.** Lowest risk; the on-page changes are independent of the URL structure, so the search-engine signals land on the *current* URL and are preserved when Commit 2 splits the template.

> **Coupling note:** the schema block ships on `/index.html` (the current SPA URL) in Commit 1. In Commit 2 the template splits into landing/chapter/read modes and the schema block becomes a parameter of the landing template — same JSON-LD content, served from the same URL (`/`), just generated through the new template plumbing. No re-emission needed; the schema is portable across the refactor.

**Commit 2 — Build refactor + static-file move + workflow update.** Section parser, multi-mode template, generator emits to `_site/` directly. Move static-input files (`robots.txt`, `CNAME`, `.nojekyll`, `cover.jpg`, `cover.webp`) from repo root into `build/static/` *and* update `.github/workflows/static.yml` to remove the staging step *in the same commit* — otherwise CI breaks mid-branch. No new URLs yet — landing + `/read/` (which is the renamed all-in-one mode) only. Validates the pipeline change without changing the URL surface for crawlers.

**Commit 3 — Per-chapter pages (Tier 2).** Emit ~17 chapter pages, breadcrumbs, prev/next nav, sitemap regenerated, cross-section anchor rewriting, hash-redirect shim on landing, byline mode-awareness, AGENTS.md de-linker refactor for chapter mode. The actual organic-ceiling unlock.

**Verification** runs after each commit; full pass after Commit 3.

## Architecture

The site is hosted on GitHub Pages with custom domain `ship-it-with.ai`. Today: one `build/build_spa.py` reads `source/Ship_It_With_AI.md` and `build/spa_template.html` and writes `index.html`. The CI workflow stages `index.html` + 5 static assets into `_site/` and uploads to Pages.

After this pass:

- `build/build_spa.py` becomes a generator that walks the source markdown, parses it into a list of `Section` objects (kind, slug, title, body markdown, reading time, optional parent part), and emits a complete `_site/` tree.
- `build/spa_template.html` factors into shared chrome (head, topbar, sidebar TOC, footer) plus a body slot. The template gains a parameter for "page mode" (`landing` | `chapter` | `read`) that selects the right body shape.
- The CI workflow runs the build and uploads `_site/` directly — no more manual file staging.
- `index.html` at the repo root stops being committed. It was always a build artifact; making that explicit removes the dirty-working-tree confusion that's already bitten the feedback-pass branch.

## Output tree

```
_site/
├── index.html                                  ← landing: H1, dek, CTAs, TOC, footer (~80 KB)
├── 404.html                                    ← branded 404 with link back to TOC
├── llms.txt                                    ← AI-answer-engine preference signals
├── robots.txt                                  ← unchanged from current
├── sitemap.xml                                 ← regenerated to list all URLs
├── cover.jpg                                   ← preserved for backwards compat
├── cover.webp                                  ← new, 1200×630, ≤50 KB
├── CNAME                                       ← unchanged
├── .nojekyll                                   ← unchanged
│
├── foreword/index.html
├── prologue-nine-seconds/index.html
├── chapter-1-six-primitives/index.html
├── chapter-2-the-anatomy-invariant/index.html
├── chapter-3-governance-in-layers/index.html
├── chapter-4-from-generating-code-to-shipping-software/index.html
├── chapter-5-the-six-phase-loop/index.html
├── chapter-6-agents-md-as-team-infrastructure/index.html
├── chapter-7-architecture-review/index.html
├── chapter-8-readiness-kill-signals/index.html
├── chapter-9-patterns-for-brownfield-codebases/index.html
├── chapter-10-adoption-90-days-three-roles/index.html
├── closing/index.html
├── acknowledgments/index.html
├── about-the-author/index.html
├── appendix-a-cost-economics/index.html
├── appendix-b-templates/index.html
├── appendix-c-sources/index.html
│
└── read/index.html                             ← all-in-one SPA preserved (~378 KB)
```

~19 indexable URLs. The `/read/` page preserves every existing `#chapter-N`, `#appendix-b`, `#about-the-author` anchor so inbound bookmarks keep working; the chapter URLs are new and SEO-priority.

## Slug map (explicit, hand-curated)

A pure-derivation rule (`kebab-case(title)`) produces URLs that are too long for chapters with subtitles ("Architecture Review: Documentation and Diagnosis" → `chapter-7-architecture-review-documentation-and-diagnosis`). Slugs are hand-curated truncations of the title's most-searchable noun phrase, with the numeric prefix kept stable. **This table is the canonical source of truth — the parser reads from it.**

| Section (source heading) | Kind | Slug |
|---|---|---|
| `## Foreword - Why this manual` | foreword | `foreword` |
| `## Nine seconds {#nine-seconds}` (under `# Prologue`) | prologue | `prologue-nine-seconds` |
| `## Chapter 1` + `## Six primitives` | chapter | `chapter-1-six-primitives` |
| `## Chapter 2` + `## The anatomy invariant` | chapter | `chapter-2-anatomy-invariant` |
| `## Chapter 3` + `## Governance in layers` | chapter | `chapter-3-governance-in-layers` |
| `## Chapter 4` + `## From generating code to shipping software` | chapter | `chapter-4-from-generating-code-to-shipping-software` |
| `## Chapter 5` + `## The six-phase loop` | chapter | `chapter-5-six-phase-loop` |
| `## Chapter 6` + `## AGENTS.md as team infrastructure` | chapter | `chapter-6-agents-md` |
| `## Chapter 7` + `## Architecture Review: Documentation and Diagnosis` | chapter | `chapter-7-architecture-review` |
| `## Chapter 8` + `## Readiness: The Kill Signals and the Traffic Light` | chapter | `chapter-8-readiness-kill-signals` |
| `## Chapter 9` + `## Patterns for brownfield codebases` | chapter | `chapter-9-brownfield-patterns` |
| `## Chapter 10` + `## Adoption: 90 days, three roles` | chapter | `chapter-10-adoption-90-days` |
| `# Closing - …` | closing | `closing` |
| `## Acknowledgments` | acknowledgments | `acknowledgments` |
| `## About the author {#about-the-author}` | about | `about-the-author` |
| `## Appendix A. Cost Economics` | appendix | `appendix-a-cost-economics` |
| `## Appendix B. Templates` | appendix | `appendix-b-templates` |
| `## Appendix C. …` | appendix | `appendix-c-sources` |

The slug map lives as a Python `dict` constant in `build/build_spa.py` (e.g., `SECTION_SLUGS`). Adding a new section to the manual requires adding a row to this table; the build fails loudly otherwise (per Error Handling).

## Canonical & duplicate-content strategy

The same chapter body appears at two URLs after Commit 3: `/chapter-3-governance-in-layers/` (the SEO-priority page) and inside `/read/` (the all-in-one experience). Without explicit canonicals, Google may pick `/read/` and demote the per-chapter pages — defeating the whole exercise.

**Decisions:**

- **Per-chapter pages** (`/chapter-N-…/`, `/appendix-X-…/`, `/foreword/`, etc.): `<link rel="canonical" href="<self>">`. Each chapter URL is the authoritative location for its content.
- **Landing** (`/`): `<link rel="canonical" href="https://ship-it-with.ai/">` (self).
- **`/read/`**: `<link rel="canonical" href="https://ship-it-with.ai/">` (the landing). This signals to Google that `/read/` is an alternate format of the manual-as-a-whole, not the canonical home of any individual chapter. Google may still index `/read/` (no `noindex`) because users searching for "ship it with ai full text" should still find it, but ranking authority flows to the per-chapter pages.

The `/read/` page also gets a small note in its body ("You're reading in single-page mode. Each chapter has its own page — see the [table of contents](/).") to give users a navigable on-ramp to the chapter URLs.

## Component designs

### Commit 1 — On-page fixes

#### Title and H1

Landing page:
- `<title>Agentic Coding: A Field Manual for Shipping Software With AI Agents</title>` (~66 chars)
- H1 carries both brand and keyword via a two-part structure:
  ```html
  <h1 class="article-title">
    Ship It With AI
    <span class="article-title-keyword">Agentic Coding Field Manual</span>
  </h1>
  ```
  The accessible/indexable text is `Ship It With AI Agentic Coding Field Manual` (Google reads the whole H1). The styled `<span>` renders smaller and visually subordinate so the brand still dominates the eye. Existing `.article-title` rule stays; new `.article-title-keyword` rule sets `display: block; font-size: 0.55em; font-weight: 500; color: var(--color-text-soft); letter-spacing: normal; margin-top: 8px;`.

`/read/` page (all-in-one mode): same H1; the existing Part I/II/III, Prologue, Closing `<h1>` tags get demoted to `<h2>` so the page has one true H1.

Chapter pages: `<title><Chapter Title> — Agentic Coding Field Manual</title>` (e.g. `Six primitives of an AI coding agent — Agentic Coding Field Manual`, ~62 chars). Single `<h1>` equals the chapter title (no brand suffix in H1; the brand lives in the topbar via the persistent "Ship It With AI" anchor).

#### Landing dek (the in-page tagline)

Rewrite from the current control-thesis dek to lead with the primary keyword:

> Agentic coding — letting an AI agent read, write, run, and verify your code — is now a control problem, not a tooling problem. Control the context, the actions, the verification, and the adoption surface. This field manual is the methodology.

Sits between subtitle and the byline+CTA row in the landing hero.

#### Schema upgrade

Landing emits three JSON-LD blocks:

1. **Book** (current `Article` block converted): `@type: Book`, `"@id": "https://ship-it-with.ai/#book"`, `name`, `author` (Person), `bookFormat: "EBook"`, `inLanguage: "en"`, `numberOfPages` (computed at build time: `round(total_word_count / 250)`), `genre: "Technology / Software Engineering"`, `about: ["Agentic coding", "AI software delivery", "AGENTS.md"]`, `dateModified` (build-time).
2. **Organization** with `logo`: `Ship It With AI` as publisher entity; resolves the "publisher must be Organization for rich results" issue the technical audit flagged. `"@id": "https://ship-it-with.ai/#org"`.
3. **FAQPage** with 4 high-intent Q/As drawn from the manual:
   - "What is agentic coding?"
   - "How does agentic coding differ from AI autocomplete and from vibe coding?"
   - "What is AGENTS.md and why does it matter?"
   - "How do you safely roll out AI coding agents in an engineering team?"

Chapter pages emit:
1. **TechArticle** (`@type: TechArticle`): `headline`, `author`, `dateModified` (build-time), `articleSection` (chapter title), `isPartOf: {"@id": "https://ship-it-with.ai/#book"}` referencing the Book by its explicit `@id` (Schema validators require an `@id` link, not just a URL string), `proficiencyLevel: "Expert"`, `dependencies: ["Claude Code", "AGENTS.md", "MCP"]`.
2. **BreadcrumbList**: trail depends on section kind. Chapters get `Home → Part X → Chapter Y`. Appendices get `Home → Appendices → Appendix Y`. Foreword / Prologue / Closing / Acknowledgments / About the author are two-level: `Home → <section title>`.

#### Internal anchor text variation

The TOC currently emits `<span class="toc-num">1</span><span class="toc-text">Six primitives</span>`. Anchor text submitted to the link target is "Six primitives" — too thin. Update to full chapter title in the link's accessible name (the `<a>`'s text content): `Chapter 1 — Six primitives of an AI coding agent`. Apply on both the landing TOC and the sidebar TOC.

#### Cover image

Generate `cover.webp` at exactly 1200×630, target ≤50 KB. The conversion is one-shot — committed to the repo, regenerated only when the source `cover.png` changes. `og:image` and `twitter:image` keep pointing at `cover.jpg` for maximum scraper compatibility (some scrapers still don't speak WebP); the WebP is for browser hero rendering where appropriate. Both files coexist in `build/static/` (after Commit 2's static-file move) and get copied to `_site/` by the build script.

Implementation: add `build/cover_to_webp.py` (Python + Pillow, dev-only one-shot — Pillow is not added to CI). Script reads `build/cover.png`, writes `build/static/cover.webp` at exactly 1200×630. Run manually when the cover changes: `python3 build/cover_to_webp.py`.

#### Dynamic dateModified

`build/build_spa.py` already has access to `datetime`. Replace the hardcoded `2026-05-26` in the JSON-LD with `datetime.utcnow().strftime("%Y-%m-%d")`. Stamps every build with the current date so freshness signals stay accurate.

#### Custom 404 page

`build/build_spa.py` writes `_site/404.html` from a small template snippet. Page chrome matches the site (topbar, dark/light themes); body is a short "Page not found" message, links to the homepage and to the TOC anchor on `/read/`.

#### llms.txt

`build/build_spa.py` writes `_site/llms.txt`. Contents follow the emerging convention (`https://llmstxt.org/`):

```
# Ship It With AI - A Field Manual for Agentic Software Delivery

> A vendor-neutral field manual for shipping software with AI coding agents.
> Covers six primitives, the six-phase loop, AGENTS.md as team infrastructure,
> governance in layers, kill signals, brownfield patterns, and 90-day adoption.

## Docs
- [Foreword](https://ship-it-with.ai/foreword/)
- [Prologue - Nine seconds](https://ship-it-with.ai/prologue-nine-seconds/)
- [Chapter 1 - Six primitives](https://ship-it-with.ai/chapter-1-six-primitives/)
…
- [Chapter 10 - Adoption: 90 days, three roles](https://ship-it-with.ai/chapter-10-adoption-90-days/)
- [Closing](https://ship-it-with.ai/closing/)
- [Appendix A - Cost Economics](https://ship-it-with.ai/appendix-a-cost-economics/)
- [Appendix B - Templates](https://ship-it-with.ai/appendix-b-templates/)
- [Appendix C - Sources](https://ship-it-with.ai/appendix-c-sources/)

## Optional
- [About the author](https://ship-it-with.ai/about-the-author/)
- [Acknowledgments](https://ship-it-with.ai/acknowledgments/)
- [Read as one page](https://ship-it-with.ai/read/)
```

Generated from the same Section list that drives sitemap.xml.

#### Non-critical CSS deferral

The current template inlines ~50 KB of CSS in `<head>`. Most is critical (typography, layout, callouts) but some is non-critical (search modal, kbd help dialog, anchor-toast, dark-mode-only overrides for components not above the fold).

**Correction on technique:** moving inline `<style>` to the end of `<body>` does NOT defer browser parsing — inline styles parse synchronously regardless of position. The only real deferral comes from extracting non-critical CSS to a separate file and async-loading it:

```html
<!-- in <head>, critical CSS only (inlined) -->
<style>{{CRITICAL_CSS}}</style>

<!-- non-critical CSS, async-loaded -->
<link rel="preload" href="/deferred.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/deferred.css"></noscript>
```

Implementation:

- `build/spa_template.html` splits its inline `<style>` into two named regions: `<!-- @region critical-css -->` and `<!-- @region deferred-css -->`. The template author maintains the split manually.
- The build script emits the critical region inline in `<head>` and writes the deferred region to `_site/deferred.css`.
- Both regions ship on every page (landing / chapter / read) — the deferred styles must be present so e.g. clicking search shows a styled modal.

Class allocation:
- **Critical** (in `<head>`): theme vars, typography, hero, topbar, sidebar, body prose, callouts (action/try/case/source/artifact), Appendix C source-cards, anchor-link CSS, mobile breakpoints affecting layout.
- **Deferred** (in `_site/deferred.css`): `.search-*` (the modal is hidden until invoked), `.kbd-*` (same), `.anchor-toast` (lazy-shown after click — initial styles still need to exist so the first toast renders correctly; if there's a flash-of-unstyled-content concern on first click, inline JUST `.anchor-toast` in critical and defer the rest).

### Commit 2 — Build pipeline refactor (no new URLs yet)

#### Section parser

Replace the current ad-hoc chapter/part/appendix extraction in `build/build_spa.py` with a single parser that walks the source markdown and produces a list of typed `Section` records:

```python
@dataclass
class Section:
    kind: Literal["foreword", "prologue", "chapter", "closing",
                  "acknowledgments", "about", "appendix"]
    slug: str                    # from SECTION_SLUGS, e.g. "chapter-1-six-primitives"
    title: str                   # H1 text, e.g. "Six primitives"
    body_md: str                 # raw markdown for the body
    reading_time_min: int | None # computed from word count
    part_slug: str | None        # for chapters only: "part-i" / "part-ii" / "part-iii"
    h2_subsections: list[tuple[str, str]]  # (slug, title) for sidebar nav (foreword + about)
```

Slug source: the `SECTION_SLUGS` table from above. Slugs are stable contract; the source heading text can change without affecting the slug.

##### Parser state machine

The source markdown has 7 distinct heading patterns (verified by reading the current source):

| Pattern (regex on a line) | Marks the start of |
|---|---|
| `^# Part [IVX]+ - .*$` | A Part (just sets current `part_slug` state — no Section emitted) |
| `^## Chapter \d+$` followed on next line by `^## .+$` | A chapter Section. Title = second line. |
| `^## Foreword\b` | Foreword Section |
| `^# Prologue\s*$` | A Prologue container (not a Section — sets state) |
| `^## Nine seconds \{#nine-seconds\}` (or any H2 under the Prologue container) | Prologue Section (kind=prologue) |
| `^# Closing\b` | Closing Section |
| `^## Acknowledgments\b` | Acknowledgments Section |
| `^## About the author\b` | About Section |
| `^## Appendix [A-Z]\.\s` | Appendix Section |

The parser is a single linear pass:

1. Walk source line-by-line tracking three pieces of state: `current_part_slug`, `current_section_buffer`, `current_section_meta`.
2. When a new section-starting heading is matched, emit the previous section (if any) and start buffering.
3. `# Part X` lines update `current_part_slug` but don't end the current chapter buffer (Parts are containers, not Sections).
4. Resolve each section's `slug` via `SECTION_SLUGS` keyed by `(kind, title)` or by recognizable substring.
5. End of file → emit last buffered section.

For chapters specifically, the parser must handle the existing two-line pattern (`## Chapter N` then `## Title`) — both lines are consumed as part of the heading. The current build script's `transform_chapter_headings` (around `build/build_spa.py:185-203`) already collapses these pairs; that logic moves into the parser. Title equals the second line's text.

The `_NEXT_BOUNDARY_RE` regex in the current script does not list `# Prologue` as a boundary — the new parser MUST include it (per the table above).

If any source heading pattern isn't in `SECTION_SLUGS`, raise loudly (per Error Handling).

#### Multi-mode template

`build/spa_template.html` factors into clearly delineated regions via comments:

```html
<!-- @region head -->
…shared head, schema scaffold, fonts…
<!-- @endregion -->

<!-- @region topbar -->
…persistent topbar with toggles + search button…
<!-- @endregion -->

<!-- @region sidebar -->
…TOC sidebar with "you are here" highlight…
<!-- @endregion -->

<!-- @region body -->
{{BODY}}
<!-- @endregion -->

<!-- @region footer -->
…contact + copyright…
<!-- @endregion -->
```

The Python build script reads the template once, splits on these region markers, and composes per-page HTML by inserting the body content (and mode-specific schema, title, etc.) into the right slot.

The body slot is filled differently per page mode:
- `landing`: marketing hero (H1 + dek + CTAs), then the TOC (also visible in the sidebar), then a short "About this manual" blurb, then footer-y outbound links.
- `chapter`: chapter title (H1), reading-time badge, body HTML, prev/next nav at the bottom.
- `read`: the existing all-in-one body (every section concatenated), with Parts/Prologue/Closing demoted from H1 to H2.

#### Output to `_site/`

`build/build_spa.py` writes to `_site/` instead of the repo root. The CI workflow's "Stage public files" step disappears entirely:

```yaml
- name: Build SPA from source
  run: python3 build/build_spa.py

- name: Upload artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: '_site'
```

The build script itself writes everything (`index.html`, `read/index.html`, `robots.txt`, `sitemap.xml`, `CNAME`, `.nojekyll`, `404.html`, `llms.txt`, `cover.jpg`, `cover.webp`) into `_site/`. The static assets (`robots.txt`, etc.) are sourced from a `build/static/` directory that the script copies.

The committed `index.html` at the repo root is deleted in Commit 2. Add `_site/` to `.gitignore`. Local preview workflow becomes: `python3 build/build_spa.py && python3 -m http.server -d _site 8000`.

### Commit 3 — Per-chapter pages

#### Emit per-chapter HTML

For each `Section` from the parser, the build script writes `_site/<slug>/index.html` using the `chapter` template mode. Content:

- `<head>`: unique `<title>`, unique meta description (auto-derived: first ~155 chars of the section body, with the chapter title prepended), canonical = self.
- Topbar + sidebar TOC (sidebar highlights the current chapter).
- H1 = chapter title.
- Body = the rendered chapter content (figures, source-notes, artifact boxes, action boxes, try-it boxes — all the existing transforms apply identically).
- Prev/next nav at the bottom: links to the previous and next Section by document order, with chapter title in the anchor text.
- `BreadcrumbList` JSON-LD: per the per-kind rule above.
- `TechArticle` JSON-LD: `articleSection` set to the chapter title, `isPartOf` referencing the Book on landing.

#### Sitemap regeneration

`build/build_spa.py` writes `_site/sitemap.xml`. Every Section gets an entry with `<loc>`, `<lastmod>` (build time), and the landing page gets its own entry. `/read/` is included so it stays indexable as the all-in-one experience.

#### TOC link rewriting

The TOC on landing and the sidebar TOC on chapter pages link to `/<slug>/` (the per-chapter URL). The TOC on `/read/` keeps using in-page anchors. The TOC builder takes a parameter for which URL style to emit.

Concrete examples of TOC entries that change between modes:

- `read` mode: `<a href="#chapter-3">Governance in layers</a>`
- `chapter` / `landing` mode: `<a href="/chapter-3-governance-in-layers/">Governance in layers</a>`

Same applies to the "About the author" TOC entry added in the feedback pass (currently `#about-the-author` — becomes `/about-the-author/` on landing + chapter pages).

#### Cross-section anchor rewriting

The body markdown contains intra-document references that cross section boundaries — e.g., line 103 of `source/Ship_It_With_AI.md` has `[Full background: About the author.](#about-the-author)` inside the Foreword body. On `/foreword/` the target anchor doesn't exist (it lives on `/about-the-author/`).

Add a new post-render transform, `rewrite_cross_section_anchors(html, current_section, anchor_index)`:

- Build an `anchor_index: dict[str, str]` once during parse: maps every known anchor id (h2/h3 explicit `{#anchor}` ids and computed section ids) to the slug of the section that owns it. Example: `{"about-the-author": "about-the-author", "the-shift-in-context": "foreword", "nine-seconds": "prologue-nine-seconds", "appendix-b": "appendix-b-templates", …}`.
- For each `<a href="#X">` in the body:
  - If `X` is in `current_section`'s own anchors → leave as `#X` (in-page jump works).
  - Else if `X` is in `anchor_index` → rewrite to `<a href="/<owning-slug>/#X">`.
  - Else (unknown) → leave as `#X` and log a warning (the link is already broken; rewriting won't fix it).

On `/read/` (all-in-one mode) this transform is a no-op — every anchor is in-page, no rewriting needed.

The transform runs after `inject_anchor_links` (so the `¶` anchor-link `href`s themselves can also be in-section absolute when needed) and before the final HTML emission.

#### Byline link mode-awareness

The topbar byline `<a href="#contact">{{AUTHOR}}</a>` works on `/read/` (where `#contact` is in-page) but breaks on chapter pages (no `#contact` element). The template renders the byline link differently per page mode:

- `read` mode: `<a href="#contact">{{AUTHOR}}</a>` (unchanged)
- `landing` and `chapter` modes: `<a href="/about-the-author/#contact">{{AUTHOR}}</a>`

Implementation: the template gets a `{{BYLINE_HREF}}` placeholder; the build script substitutes the right value per page.

#### Hash-redirect shim on landing

External bookmarks to the old SPA's anchors (e.g., `https://ship-it-with.ai/#chapter-7`) will land on the new short landing page and silently do nothing — the anchor doesn't exist there. Resolved decision #5 (no JS redirects) was scoped to `/read/`; on the landing page there's no SPA scroll behavior to fight.

Add a small JS shim to the landing template only (~10 lines):

```html
<script>
  // Migrate pre-split bookmarks: /#chapter-N → /chapter-N-slug/
  (function() {
    var hash = location.hash;
    if (!hash) return;
    var REDIRECTS = {
      '#chapter-1':  '/chapter-1-six-primitives/',
      '#chapter-2':  '/chapter-2-anatomy-invariant/',
      '#chapter-3':  '/chapter-3-governance-in-layers/',
      '#chapter-4':  '/chapter-4-from-generating-code-to-shipping-software/',
      '#chapter-5':  '/chapter-5-six-phase-loop/',
      '#chapter-6':  '/chapter-6-agents-md/',
      '#chapter-7':  '/chapter-7-architecture-review/',
      '#chapter-8':  '/chapter-8-readiness-kill-signals/',
      '#chapter-9':  '/chapter-9-brownfield-patterns/',
      '#chapter-10': '/chapter-10-adoption-90-days/',
      '#foreword':   '/foreword/',
      '#nine-seconds':       '/prologue-nine-seconds/',
      '#about-the-author':   '/about-the-author/',
      '#closing':            '/closing/',
      '#acknowledgments':    '/acknowledgments/',
      '#appendix-a':         '/appendix-a-cost-economics/',
      '#appendix-b':         '/appendix-b-templates/',
      '#appendix-c':         '/appendix-c-sources/'
    };
    var target = REDIRECTS[hash];
    if (target) location.replace(target);
  })();
</script>
```

The map is generated from `SECTION_SLUGS` by the build script — never hand-maintained. Placed inline in `<head>` so it runs before any DOM is rendered.

Not added to `/read/` (anchors keep working there) or to chapter pages (no migration concern from those URLs).

#### Search index

The existing search index works against the all-in-one HTML. After the split, two changes:

1. The same index is embedded on landing, every chapter page, and `/read/` — small enough (~30 KB) that duplication is fine.
2. On chapter pages and landing, search result clicks navigate to the chapter URL with the section anchor appended (e.g., `/chapter-3-governance-in-layers/#the-five-layers`). On `/read/`, search results stay as in-page anchors.

The search index JSON gains a `url` field per entry (chapter-page URL); the click handler uses it on landing/chapter pages and ignores it on `/read/`.

The page mode is exposed to JS via a `<script>window.SITE_MODE = '<mode>';</script>` snippet in `<head>` set by the build script per page (one of `'landing' | 'chapter' | 'read'`). The search click handler reads `window.SITE_MODE`:

```js
function onSearchResultClick(entry) {
  if (window.SITE_MODE === 'read') {
    location.hash = entry.id;  // in-page anchor
  } else {
    location.href = entry.url + '#' + entry.id;  // chapter URL + anchor
  }
}
```

#### AGENTS.md de-linker on per-chapter pages

The existing `delink_repeated_agents_md` (around `build/build_spa.py:387`) splits HTML on `<h2 id="chapter-N">` to determine chapter boundaries. On per-chapter pages the chapter heading is an `<h1>` and there's only one chapter per page — the splitter sees the entire body as one chunk, but the semantics are simpler: keep the first AGENTS.md link in the page, plain-text the rest.

Refactor so the function accepts a page mode:

- `read` mode: current behavior (split on `<h2 id="chapter-N">`, keep first per chunk).
- `chapter`, `landing`, `acknowledgments`, etc.: treat the entire body as one chunk and apply `keep_first`.

Each chapter page therefore has at most one AGENTS.md link — same invariant as before, just enforced at a smaller boundary.

#### Sidebar "you are here" highlight on chapter pages

The current scroll-spy on `/read/` (intersection observer on H2s) doesn't apply when only one chapter is visible. On chapter pages, the build script stamps the current section's TOC `<li>` with `class="toc-current"` at render time (no JS needed). Existing `.toc-current` CSS gets a small treatment (heavier weight, accent left-border) if not already present.

On `/read/`, the scroll-spy continues to work as today.

#### Asset path convention

All asset references in the template become root-relative so they resolve from any URL depth. Specifically:

- `<img src="/cover.jpg">` (was: `cover.jpg`) at `build/spa_template.html:1781`
- `<meta property="og:image" content="https://ship-it-with.ai/cover.jpg">` (already absolute — unchanged)
- Any inline SVG `<use href="…">` references (none currently)
- All internal navigation: TOC links to `/chapter-N-…/`, `/read/`, `/`, etc.

The shim `build/static/` directory holds the static-copy files that get copied verbatim to `_site/` root: `CNAME`, `robots.txt`, `.nojekyll`, `cover.jpg`, `cover.webp`. The build script enumerates them by globbing this directory and `shutil.copy`-ing into `_site/`.

#### Prev/next nav

A small footer-region block on chapter pages:

```html
<nav class="chapter-nav" aria-label="Chapter navigation">
  <a class="chapter-prev" href="/<prev-slug>/">← <prev-title></a>
  <a class="chapter-next" href="/<next-slug>/"><next-title> →</a>
</nav>
```

First section has no prev; last has no next.

### Verification harness

New file: `build/tests/verify_seo_pass.js`. Same pattern as the feedback-pass verify script, with one architectural change: **tests run against a local HTTP server, not `file://`**. Root-relative URLs (`/chapter-3-…/`, `/cover.jpg`) don't resolve against `file://` (browser interprets `/` as filesystem root, not `_site/`), so prev/next nav, chapter-to-chapter navigation, and asset loading would silently fail. The harness spins up Python's `http.server` against `_site/` on a free port before running tests, tears it down after.

Concretely, the helper (`build/tests/lib/build_and_open.js` evolves into `build/tests/lib/build_and_serve.js`):

```javascript
const { execFileSync, spawn } = require('child_process');
const path = require('path');
const net = require('net');

async function buildAndServe() {
  const repoRoot = path.resolve(__dirname, '..', '..', '..');
  execFileSync('python3', ['build/build_spa.py'], { cwd: repoRoot, stdio: 'inherit' });

  const port = await freePort();
  const server = spawn('python3', ['-m', 'http.server', '-d', '_site', String(port)],
                       { cwd: repoRoot, stdio: 'pipe' });
  await waitForReady(port);
  const baseUrl = `http://127.0.0.1:${port}`;
  return { baseUrl, stop: () => server.kill() };
}
```

Tests navigate to `${baseUrl}/`, `${baseUrl}/chapter-3-…/`, etc.

Assertions built up across the three commits:

- **Commit 1 assertions** (landing page only):
  - `<title>` contains "Agentic Coding"
  - Exactly one `<h1>` and it contains "Agentic Coding"
  - Landing first paragraph contains the phrase "agentic coding" (case-insensitive)
  - JSON-LD parses; blocks present: `@type: Book` (with `@id`), `@type: Organization` (with `@id`), `@type: FAQPage`
  - `cover.webp` exists in `_site/`, is ≤50 KB, dimensions exactly 1200×630
  - `404.html` exists in `_site/`, has site chrome (topbar present in HTML)
  - `llms.txt` exists in `_site/`
  - `dateModified` in Book schema matches today's date
  - No horizontal overflow on mobile / tablet / desktop
- **Commit 2 assertions**:
  - `_site/index.html` exists, is ≤100 KB (landing is now thin)
  - `_site/read/index.html` exists, contains all 10 chapter anchor IDs (`#chapter-1` through `#chapter-10`)
  - `_site/read/index.html` has exactly one `<h1>` (parts demoted)
  - `_site/read/index.html` has `<link rel="canonical" href="https://ship-it-with.ai/">`
  - `_site/deferred.css` exists, is loaded via `<link rel="preload">` on landing and `/read/`
- **Commit 3 assertions**:
  - `_site/sitemap.xml` lists at least 19 URLs (the 17 sections + landing + `/read/`)
  - Every URL in the sitemap returns 200 from the local HTTP server and has exactly one `<h1>` matching the page title
  - Every chapter page has unique `<title>` + meta description
  - Every chapter page has a `BreadcrumbList` JSON-LD block that parses; first crumb resolves to `/`, last to self
  - Every chapter page has `<link rel="canonical" href="<self>">`
  - Every chapter page has a `TechArticle` block whose `isPartOf` references `https://ship-it-with.ai/#book` by `@id`
  - `/chapter-3-governance-in-layers/` has a prev/next nav with both prev and next links pointing to siblings
  - Clicking a TOC entry on landing navigates to `/<chapter-slug>/` (not `/#chapter-N`)
  - Search index on a chapter page: type a query, click a result, lands on a chapter URL with the expected anchor
  - Hash-redirect shim: navigate to `/#chapter-7`, must end up at `/chapter-7-architecture-review/`
  - Cross-section anchor rewriting: on `/foreword/`, the "About the author" link `href` is `/about-the-author/#about-the-author` (not bare `#about-the-author`)
  - Byline link on `/chapter-3-governance-in-layers/` resolves to `/about-the-author/#contact` (not `#contact`)

All assertions run across 3 viewports (375 mobile, 768 tablet, 1280 desktop) in both light and dark mode where layout-relevant, single-viewport for content-only assertions.

## Data flow

```
source/Ship_It_With_AI.md
        │
        ▼
parse_sections() ── list[Section]   ◄── SECTION_SLUGS table
        │
        ├──► build_anchor_index()    ── dict[anchor_id → owning_slug]
        │
        ├──► render_landing()        ──► _site/index.html
        │      (includes hash-redirect shim, SITE_MODE='landing')
        ├──► render_chapter(s)       ──► _site/<slug>/index.html  (×18)
        │      (SITE_MODE='chapter', cross-section anchors rewritten)
        ├──► render_read_mode()      ──► _site/read/index.html
        │      (SITE_MODE='read', H1s demoted, canonical → /)
        ├──► render_sitemap()        ──► _site/sitemap.xml
        ├──► render_llms_txt()       ──► _site/llms.txt
        ├──► render_404()            ──► _site/404.html
        ├──► render_deferred_css()   ──► _site/deferred.css
        └──► copy_static()           ──► _site/{robots.txt, CNAME, .nojekyll, cover.jpg, cover.webp}
                                          (from build/static/)
```

All emit functions share the rendered-body pipeline:

```
markdown → html
  → replace_diagrams (figures)
  → transform_source_notes
  → transform_artifacts
  → wrap_action_boxes
  → wrap_try_boxes
  → tag_case_notes
  → transform_source_cards
  → delink_repeated_agents_md (mode-aware: read-mode splits on h2, chapter-mode treats body as one chunk)
  → inject_anchor_links
  → rewrite_cross_section_anchors (new — uses anchor_index; no-op on /read/)
```

The same content renders identically across `/read/` and the per-chapter pages.

## Error handling

- **Section parse failures**: if the parser encounters a heading not present in `SECTION_SLUGS`, raise loudly with the unmatched heading text. Builds should fail visibly rather than silently producing a broken site or dropping a section.
- **Slug collisions**: if `SECTION_SLUGS` has duplicate values, raise at script startup. Slugs are URLs and must be unique.
- **Missing static asset**: if `build/static/robots.txt` (or any other static input including `cover.webp`) is missing, raise with the path and the command to regenerate (`python3 build/cover_to_webp.py` for cover.webp).
- **Unknown cross-section anchor**: `rewrite_cross_section_anchors` logs a warning for each `#X` reference not found in `anchor_index` (the link is already broken in source; rewriting won't fix it, but the warning surfaces drift between body content and section anchors).
- **Hash-redirect map drift**: the landing hash-redirect map is generated from `SECTION_SLUGS` at build time, never hand-maintained, so it can't drift.
- **Verification script**: fails fast on assertion errors; screenshots from successful steps still saved for inspection. The local HTTP server is torn down on test exit even on failure (use a `try/finally` in the harness).

## Testing

Manual: `python3 build/build_spa.py`, then `python3 -m http.server -d _site 8000` and walk the site. Check:
- Landing loads and looks like a marketing entry (not a wall of text).
- Clicking a TOC entry navigates to a per-chapter URL.
- Chapter pages have one H1, sidebar TOC highlights the current chapter, prev/next nav works.
- `/read/` still works as the all-in-one experience.
- `/chapter-1-six-primitives/` (and a few others) look correct on mobile DevTools.
- `view-source:/chapter-1-six-primitives/` shows correct title, meta description, JSON-LD schema.

Automated: `node build/tests/verify_seo_pass.js`. Must pass on all viewport×mode combinations before merge.

## Open items for user review

1. **Exact dek wording.** Suggested copy in the design uses "control problem, not a tooling problem" lifted from the existing feedback-pass dek. You may want to refine. (Reasonable default: ship the suggestion, revise during diff review.)
2. **The 4 FAQPage Q/As.** I'll draft from the existing manual; you approve voice. (Default: I draft, you review during diff.)
3. **The 4 anchor URL slugs that still contain "book"** (`#what-agentic-ai-means-in-this-book`, etc.) — these remain on `/read/` as in-page anchors. Per earlier decision, no change in this pass. Flag if you want them renamed alongside the URL split.

## Resolved decisions (defaults applied — flag in review if you want to change)

1. **Per-chapter URL slug style**: descriptive kebab-case with the chapter number prefix (`/chapter-1-six-primitives/` not `/chapter-1/` or `/six-primitives/`). Keyword in URL is a small but real signal; stable numeric prefix keeps ordering legible.
2. **Foreword granularity**: one URL for the whole Foreword, with its 4 H3 subsections as on-page anchors. The H3s aren't strong enough as standalone pages.
3. **Reading mode preserved at `/read/`**: not `/all/`, not `/full/`. The name is intentional — distinguishes "consume as a single document" from "chapter-by-chapter reference".
4. **`index.html` at repo root**: deleted in Commit 2. Build artifacts don't belong in source control.
5. **No redirects from `/#chapter-N` to `/chapter-N-…/`**: GitHub Pages doesn't support server-side redirects, and a JS redirect on `/read/` would fight the legitimate SPA scroll behavior. The `/read/` anchors stay valid; external bookmarks keep working there.
6. **Cover image conversion**: use Python Pillow with WebP support (no system `cwebp` dep). Conversion is a **dev-only, one-shot step** (run when cover changes) via a small `build/cover_to_webp.py` script; the resulting `cover.webp` is committed to the repo and copied to `_site/` like any other static asset. **Pillow is NOT added to the CI install step** — CI just copies the pre-built cover.webp. Document the manual invocation in the script's header (`python3 build/cover_to_webp.py`).
7. **CSS split: manual, with extraction to a real file.** The template author splits the inline `<style>` block into two regions (`<!-- @region critical-css -->` and `<!-- @region deferred-css -->`). The build script keeps `critical-css` inline in `<head>` and emits `deferred-css` to `_site/deferred.css`, loaded async via `<link rel="preload" as="style" onload>`. Scripted detection adds complexity without protecting against the actual failure mode (a developer adds a new rule and doesn't know which slot it belongs in).
8. **Trailing slashes.** All internal links and canonicals use the trailing-slash form (`/chapter-3-…/`, not `/chapter-3-…`). GitHub Pages serves directories with `index.html` at the trailing-slash URL and 301-redirects the no-slash form, so the trailing slash is the canonical surface. The verify script checks every link uses the trailing-slash form.
9. **CI workflow: install step unchanged.** `.github/workflows/static.yml` keeps `pip install markdown` only — Pillow is not needed in CI (cover.webp is pre-built and committed). The workflow does drop the manual file-staging step in Commit 2 (the build now writes directly to `_site/`).
10. **`/read/` canonical points to `/`.** Per the Canonical & duplicate-content strategy section: the all-in-one mode is an alternate format of the manual-as-a-whole, not the canonical home of any individual chapter.
11. **Hash-redirect shim on landing only.** Per the Hash-redirect shim section: not on `/read/` (anchors keep working) or on chapter pages (no migration concern from those URLs).
12. **Page mode signal in JS via `window.SITE_MODE`.** Set inline in `<head>` by the build script per page. Read by the search click handler (and any future mode-dependent JS).
13. **`build/build_spa.py` rename: deferred.** The script generates a tree now, not an SPA, but renaming is a chore for a separate pass — every doc, hook, and CI reference would need updating.
