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

**Commit 1 — On-page fixes (Tier 1).** Pure template + script edits, no URL changes. Lowest risk; ships ranking signals immediately. Captures most of what the technical audit flagged.

**Commit 2 — Build refactor.** Section parser, multi-mode template, generator emits to `_site/`, workflow update. No new URLs yet — landing + `/read/` (which is the existing SPA) only. Validates the pipeline change without changing the URL surface for crawlers.

**Commit 3 — Per-chapter pages (Tier 2).** Emit ~17 chapter pages, breadcrumbs, prev/next nav, sitemap regenerated. The actual organic-ceiling unlock.

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
├── about-the-author/index.html
├── appendix-a-cost-economics/index.html
├── appendix-b-templates/index.html
├── appendix-c-sources/index.html
│
└── read/index.html                             ← all-in-one SPA preserved (~378 KB)
```

~18 indexable URLs. The `/read/` page preserves every existing `#chapter-N`, `#appendix-b`, `#about-the-author` anchor so inbound bookmarks keep working; the chapter URLs are new and SEO-priority.

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

1. **Book** (current `Article` block converted): `@type: Book`, `name`, `author` (Person), `bookFormat: "EBook"`, `inLanguage: "en"`, `numberOfPages`, `genre: "Technology / Software Engineering"`, `about: ["Agentic coding", "AI software delivery", "AGENTS.md"]`, `dateModified` (build-time).
2. **Organization** with `logo`: `Ship It With AI` as publisher entity; resolves the "publisher must be Organization for rich results" issue the technical audit flagged.
3. **FAQPage** with 4 high-intent Q/As drawn from the manual:
   - "What is agentic coding?"
   - "How does agentic coding differ from AI autocomplete and from vibe coding?"
   - "What is AGENTS.md and why does it matter?"
   - "How do you safely roll out AI coding agents in an engineering team?"

Chapter pages emit:
1. **TechArticle** (`@type: TechArticle`): `headline`, `author`, `dateModified` (build-time), `articleSection` (chapter title), `isPartOf` linking back to the Book on the landing URL, `proficiencyLevel: "Expert"`, `dependencies: ["Claude Code", "AGENTS.md", "MCP"]`.
2. **BreadcrumbList**: trail depends on section kind. Chapters get `Home → Part X → Chapter Y`. Appendices get `Home → Appendices → Appendix Y`. Foreword / Prologue / About the author / Closing are two-level: `Home → <section title>`.

#### Internal anchor text variation

The TOC currently emits `<span class="toc-num">1</span><span class="toc-text">Six primitives</span>`. Anchor text submitted to the link target is "Six primitives" — too thin. Update to full chapter title in the link's accessible name (the `<a>`'s text content): `Chapter 1 — Six primitives of an AI coding agent`. Apply on both the landing TOC and the sidebar TOC.

#### Cover image

Generate `cover.webp` at exactly 1200×630, target ≤50 KB. The conversion is one-shot — committed to the repo, regenerated only when the source `cover.png` changes. `og:image` and `twitter:image` keep pointing at `cover.jpg` for maximum scraper compatibility (some scrapers still don't speak WebP); the WebP is for browser hero rendering where appropriate. Both files coexist.

Implementation: add a `build/cover-to-webp.sh` script (uses `cwebp` or `ImageMagick`) that takes `build/cover.png` and writes `cover.webp` to the repo root. Not auto-run by the build; run on demand when cover changes. Document in the script's header.

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
- [Chapter 1 - Six primitives](https://ship-it-with.ai/chapter-1-six-primitives/)
…
- [Appendix C - Sources](https://ship-it-with.ai/appendix-c-sources/)

## Optional
- [About the author](https://ship-it-with.ai/about-the-author/)
- [Read as one page](https://ship-it-with.ai/read/)
```

Generated from the same Section list that drives sitemap.xml.

#### Render-blocking CSS split

The current template inlines ~50 KB of CSS in `<head>`. Most is critical (typography, layout, callouts) but some is non-critical (search modal, kbd help dialog, anchor-toast, dark-mode-only overrides for components not above the fold). Split:

- Inline in `<head>`: critical above-the-fold CSS (~15-20 KB target).
- Inline at end of body in a `<style>` block: non-critical CSS (search overlay, kbd dialog, dark-mode component overrides, the `.anchor-toast` rule).

Concretely: in `build/spa_template.html`, the existing inline `<style>` becomes two blocks. The build script can split mechanically by recognized class prefixes (`.search-`, `.kbd-`, `.anchor-toast`, etc.), or — simpler — the template author splits manually and the script just renders both slots.

### Commit 2 — Build pipeline refactor (no new URLs yet)

#### Section parser

Replace the current ad-hoc chapter/part/appendix extraction in `build/build_spa.py` with a single parser that walks the source markdown and produces a list of typed `Section` records:

```python
@dataclass
class Section:
    kind: Literal["foreword", "prologue", "chapter", "closing", "about", "appendix"]
    slug: str                    # URL slug, e.g. "chapter-1-six-primitives"
    title: str                   # H1 text, e.g. "Six primitives of an AI coding agent"
    body_md: str                 # raw markdown for the body
    reading_time_min: int | None # computed from word count
    part_slug: str | None        # for chapters: "part-i" etc.
    h2_subsections: list[tuple[str, str]]  # (slug, title) for sidebar nav
```

Slug rule: kebab-case of the chapter heading, with a numeric prefix for chapters/appendices (e.g., `chapter-3-governance-in-layers`, `appendix-b-templates`). Slugs are stable; once a chapter ships, its slug shouldn't change without a redirect plan.

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

#### Search index

The existing search index works against the all-in-one HTML. After the split, two changes:

1. The same index is embedded on landing, every chapter page, and `/read/` — small enough (~30 KB) that duplication is fine.
2. On chapter pages and landing, search result clicks navigate to the chapter URL with the section anchor appended (e.g., `/chapter-3-governance-in-layers/#the-five-layers`). On `/read/`, search results stay as in-page anchors.

The search index JSON gains a `url` field per entry (chapter-page URL); the click handler uses it on landing/chapter pages and ignores it on `/read/`.

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

New file: `build/tests/verify_seo_pass.js`. Same pattern as the feedback-pass verify script. Built up across the three commits:

- **Commit 1 assertions** (run from build time, on the landing page only):
  - `<title>` contains "Agentic Coding"
  - Exactly one `<h1>` and it contains "Agentic Coding"
  - Landing first paragraph contains the phrase "agentic coding" (case-insensitive)
  - JSON-LD parses; `@type: Book`, `@type: Organization`, `@type: FAQPage` all present
  - `cover.webp` exists, is ≤50 KB, dimensions exactly 1200×630
  - `404.html` exists in `_site/`
  - `llms.txt` exists in `_site/`
  - `dateModified` in Book schema matches today's date
  - No horizontal overflow on mobile / tablet / desktop
- **Commit 2 assertions**:
  - `_site/index.html` exists, is ≤100 KB (landing is now thin)
  - `_site/read/index.html` exists, contains all 10 chapter anchor IDs (`#chapter-1` through `#chapter-10`)
  - `_site/read/index.html` has exactly one `<h1>` (parts demoted)
- **Commit 3 assertions**:
  - `_site/sitemap.xml` lists at least 17 URLs
  - Every URL in the sitemap resolves to a 200 (load each via `file://_site/<path>/index.html`) and has exactly one `<h1>` matching the page title
  - Every chapter page has unique `<title>` + meta description
  - Every chapter page has a `BreadcrumbList` JSON-LD block that parses
  - `/chapter-1-six-primitives/` has a prev/next nav with both prev and next links pointing to siblings
  - Clicking a TOC entry on landing navigates to `/<chapter-slug>/` (not `/#chapter-N`)
  - Search index on a chapter page returns chapter-URL results

All assertions run across 3 viewports (375 mobile, 768 tablet, 1280 desktop) in both light and dark mode where layout-relevant, single-viewport for content-only assertions.

## Data flow

```
source/Ship_It_With_AI.md
        │
        ▼
parse_sections() ── list[Section]
        │
        ├──► render_landing()       ──► _site/index.html
        ├──► render_chapter(s)      ──► _site/<slug>/index.html  (×17)
        ├──► render_read_mode()     ──► _site/read/index.html
        ├──► render_sitemap()       ──► _site/sitemap.xml
        ├──► render_llms_txt()      ──► _site/llms.txt
        ├──► render_404()           ──► _site/404.html
        └──► copy_static()          ──► _site/{robots.txt, CNAME, .nojekyll, cover.jpg, cover.webp}
```

All emit functions share the rendered-body pipeline (figures → source-notes → artifacts → action/try boxes → case notes → AGENTS.md de-link → anchor links → source-cards) so the same content renders identically across `/read/` and the per-chapter pages.

## Error handling

- **Section parse failures**: if the source markdown ever changes shape such that the parser can't determine a section's kind/slug/title, raise loudly. Builds should fail visibly rather than silently producing a broken site.
- **Slug collisions**: if two sections produce the same slug, raise. Slugs are URLs and must be unique.
- **Missing static asset**: if `build/static/robots.txt` (or any other static input) is missing, raise.
- **Cover image conversion**: `cover-to-webp.sh` is manual; if `cover.webp` is missing from the repo root, the build raises a clear error with the command to regenerate it.
- **Verification script**: fails fast on assertion errors; screenshots from successful steps still saved for inspection.

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
7. **CSS split: manual.** The template author splits the inline `<style>` block into two regions (`<!-- @region critical-css -->` and `<!-- @region deferred-css -->`); the build script just renders each into the corresponding slot. Scripted detection adds complexity without protecting against the actual failure mode (a developer adds a new rule and doesn't know which slot it belongs in).
