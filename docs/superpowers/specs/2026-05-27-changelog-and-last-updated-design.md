# Changelog + Last-updated footer — Design Spec

Adds a build-time "Last updated" timestamp to the footer of every page, links a new `/changelog/` page from the footer + from the "A note on dated claims" front-matter section, and seeds the changelog with the four recent releases. Lets readers see the manual is maintained without committing the author to a release cadence.

## Scope

In scope:
- **Footer addition**: `Last updated <Month DD, YYYY>` segment + `Changelog` link in the existing `.footer-copy` line. Stamped at build time.
- **New `/changelog/` page** as a top-level section (like `/about-the-author/`). New kind in `SECTION_SLUGS`. Slug `changelog`. Two-level breadcrumb `Home → Changelog`.
- **"A note on dated claims" addition**: one sentence + link to `/changelog/`.
- **Initial changelog content**: four dated entries (Memory primitive, SEO pass, Feedback pass, First public version), reverse-chronological, one short paragraph each.
- **Build/template plumbing**: new `{{DATE_MODIFIED_HUMAN}}` substitution; `SECTION_SLUGS` row; parser boundary regex; TOC slot; hash-redirect map entry; sitemap inclusion.
- **Verify-script assertions**: `/changelog/` returns 200 with H1, all four entry dates present, footer carries the "Last updated" + Changelog link, sitemap has 21 URLs.

Out of scope:
- Per-section "last updated" dates (single build-time stamp covers the whole site).
- Auto-generated changelog from git history (manual entries only; smaller updates intentionally not enumerated).
- RSS / Atom feed of changelog entries (defer; the static page is enough).
- Notification mechanism (email subscribe, etc.) — out of scope.

## Sequencing — one PR, one commit

Small enough for a single commit on branch `changelog`. After merge, CI rebuilds and deploys.

## Architecture

The site is built from `source/Ship_It_With_AI.md` via `build/build_spa.py`, which parses sections into `Section` objects, then emits `_site/<slug>/index.html` per section + landing + `/read/` + sitemap. The changelog slots into this existing pipeline without new infrastructure:

- A new section in the source markdown (`## Changelog {#changelog}`)
- A new `SECTION_SLUGS` entry that the parser recognizes
- A new TOC slot
- A footer-template change that affects every emitted page

The footer date uses the same `datetime.now(timezone.utc)` call that already stamps `{{DATE_MODIFIED}}` (ISO format) for JSON-LD. A new `{{DATE_MODIFIED_HUMAN}}` substitution renders the same instant as `<Month DD, YYYY>` for the user-facing footer.

## Component designs

### 1. Footer change

Two coordinated changes:

**`.footer-copy` (line 2047)** — current:

```html
<p class="footer-copy">© 2026 {{AUTHOR}} · Bucharest · All rights reserved</p>
```

Becomes (adds the "Last updated" stamp; does NOT add the Changelog link here):

```html
<p class="footer-copy">© 2026 {{AUTHOR}} · Last updated {{DATE_MODIFIED_HUMAN}} · Bucharest · All rights reserved</p>
```

**`.footer-contact` (line 2040-2046)** — current row with email + LinkedIn + ai-leaders.ro. Add `Changelog` as a parallel nav link at the end:

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

Rationale: Changelog is semantically a navigation link (parallel to LinkedIn, contact email, sister-site link), not part of the copyright statement. Putting it inside `.footer-contact` reuses the existing `.footer-contact a` styling without a new CSS rule, and avoids the visual oddity of a nav link separated from "All rights reserved" by the same `·` separator the copyright row uses internally.

The footer is shared by every page (landing, chapters, /read/, 404). The redirect stub uses its own minimal HTML and is exempt. On every build, all per-chapter pages get the same stamp.

No new CSS rules needed.

### 2. `{{DATE_MODIFIED_HUMAN}}` substitution

`build/build_spa.py` — wherever `{{DATE_MODIFIED}}` is computed (the SEO pass added this; search for `DATE_MODIFIED`), add a parallel placeholder:

```python
now_utc = datetime.now(timezone.utc)
template = template.replace("{{DATE_MODIFIED}}", now_utc.strftime("%Y-%m-%d"))
template = template.replace("{{DATE_MODIFIED_HUMAN}}", now_utc.strftime("%B %d, %Y"))
```

(`%B %d, %Y` renders e.g. `May 27, 2026`. On Linux it produces zero-padded day; if a non-padded day is preferred, use `%-d` GNU extension or strip the leading zero manually.)

### 3. `/changelog/` page

#### Source markdown

Insert in `source/Ship_It_With_AI.md` between `## Acknowledgments` and `## About the author` (the existing front-of-back-matter sequence is Closing → Acknowledgments → About → Appendices; Changelog goes between About and Appendix A so it groups with the back-matter housekeeping):

```markdown
## Changelog {#changelog}

This page tracks meaningful updates to the manual. Smaller copy-edits and SEO tweaks are not enumerated; the build's last-modified date is in the footer.

### 2026-05-27 — Memory primitive + open-set framing

Memory promoted to a named primitive across the book; Chapter 1 retitled "The primitives" and the structural argument rewritten as "named primitives + the recursive primitive (subagents)". The closed "six primitives" count dropped throughout in favor of open-set framing. New Memory section covers two halves — manually defined memory (AGENTS.md/CLAUDE.md, agent-agnostic) and the auto-memory system (Auto Memory, Auto Dream — currently Claude-Code-led). Diagram updated. Chapter 6 gains a one-paragraph framing intro anchoring AGENTS.md as the team-shareable memory layer. Three new Appendix C entries source the Memory claims.

### 2026-05-27 — SEO pass: per-chapter URLs

Split the all-in-one SPA into 20 indexable URLs: landing (`/`) + each section as its own page (`/foreword/`, `/chapter-1-primitives/`, … `/appendix-c-sources/`) + `/read/` for the single-page reading mode. Each chapter page now has unique title, meta description, canonical URL, `TechArticle` + `BreadcrumbList` JSON-LD, and prev/next nav. Hero gained a control-thesis dek and a three-button CTA row. Schema upgraded from `Article` to `Book` + `Organization` + `FAQPage`. Cross-section anchor rewriting, AGENTS.md de-linking, hash-redirect shim for old `/#chapter-N` bookmarks. Built-in 404 page, `llms.txt` for AI answer engines, `cover.webp`.

### 2026-05-26 — Feedback-pass polish

External-reviewer pass: TOC chapter-to-part mismatch fixed, figure numbering dropped (web-manual style), new Source-note and Artifact callout components with light + dark variants, foreword bio trimmed to four sentences and full version moved to a new About-the-author section, hero gained a control-thesis dek, AGENTS.md links collapsed to at most one per chapter, per-section `¶` copy-link anchors, callout stack tightening.

### 2026-05-26 — First public version

Manual published at ship-it-with.ai. Ten chapters across three parts (Architecture, Method, Reality), three appendices, plus foreword, prologue, closing.

---
```

The trailing `---` matches the source's existing section-separator pattern.

#### Build script plumbing

`build/build_spa.py`:

- `SECTION_SLUGS` gains `("changelog", "Changelog"): "changelog"` between the about entry and the first appendix entry.
- Parser's heading-pattern table gains a row for `^## Changelog\b` → kind `changelog`. The exact regex follows the parser's existing one-line conventions.
- `_NEXT_BOUNDARY_RE` (or whatever the parser uses to detect section boundaries during body collection) adds `## Changelog` alongside the existing about/appendix patterns.
- TOC builder slots the changelog entry. The existing builder has explicit positioning for Closing / About / Appendices — add changelog between About and the appendices group, OR within the "About" / housekeeping section (whichever matches the builder's current structure).
- `build_anchor_index`: the explicit `{#changelog}` anchor in source markdown is picked up by the existing anchor-collection logic; no special case needed.
- `render_hash_redirect_js`: the redirect map is generated from `SECTION_SLUGS`, so `#changelog → /changelog/` lands automatically.
- `render_sitemap`: the new section is picked up; sitemap URL count goes from 20 to 21.

#### Chapter-page rendering

The existing `render_chapter()` (or whatever per-section render function) handles the changelog page with one targeted exception: **suppress the reading-time badge for `kind="changelog"`**. A ~150-word changelog renders as "1 min read" which feels confused (it announces brevity instead of being read).

Concretely in the renderer: where the reading-time `<p class="reading-time">N min read</p>` is emitted, gate on `section.kind != "changelog"`.

The BreadcrumbList for `kind="changelog"` produces the two-level trail `Home → Changelog` (mirrors how About and Foreword work — non-chapter, non-appendix sections get the two-level trail). If the existing breadcrumb logic switches only on `kind in {"chapter", "appendix"}`, the changelog falls through to the two-level default branch — confirm during implementation.

**Prev/next nav on the changelog page**: by the section order (Foreword → Prologue → Ch 1-10 → Closing → Acknowledgments → About → **Changelog** → Appendix A → Appendix B → Appendix C), the changelog's prev is `/about-the-author/`, next is `/appendix-a-cost-economics/`. That's reasonable flow — a reader walking the back-matter encounters About → Changelog → first Appendix in order. No customization needed.

**Note on `/read/` mode**: the changelog content is embedded in `/read/` as a section (the all-in-one mode concatenates everything). Plus the `/read/` footer carries a link to `/changelog/`. Mild redundancy — the footer link points to a per-chapter page that contains the same content the user is already reading. Acceptable; the link still serves users who want to deep-link the changelog or share it.

### 4. "A note on dated claims" addition

`source/Ship_It_With_AI.md` line ~151. Current section content discusses why some claims age fast — the final paragraph ends with the open-set conclusion ("If a new primitive emerges, the list grows."). The maintenance promise is a topic pivot (from "what ages" to "how it's kept fresh"), so it lands as a NEW paragraph, not appended to the existing one.

Insert as its own paragraph at the very end of the section, immediately before the trailing `---` separator:

```
I do my best to keep the manual current and maintain a [changelog](/changelog/) of meaningful updates.
```

The `/changelog/` link uses the new section's URL. The cross-section anchor rewriter (in chapter pages) won't touch this — it only rewrites `#anchor` references, not `/path/` references.

## Verification

Extend `build/tests/verify_seo_pass.js` with new assertions:

- `_site/changelog/index.html` exists and returns 200 from the local HTTP server.
- The page has exactly one `<h1>` and its text is `Changelog`.
- The page contains all four entry-header dates: `2026-05-27 — Memory primitive + open-set framing`, `2026-05-27 — SEO pass: per-chapter URLs`, `2026-05-26 — Feedback-pass polish`, `2026-05-26 — First public version`.
- The page emits BreadcrumbList JSON-LD with `Home → Changelog` (two crumbs).
- The page does NOT contain a `.reading-time` element (per the suppression in the renderer).
- The page's prev nav links to `/about-the-author/`; the next nav links to `/appendix-a-cost-economics/`.
- `_site/changelog/index.html` is listed in the sitemap.
- Sitemap has 21 URLs total (was 20).
- Landing footer (`.footer-copy`) contains text matching the regex `/Last updated [A-Z][a-z]+ \d{1,2}, \d{4}/` (e.g. `Last updated May 27, 2026`). Chapter-1 footer contains the same.
- Landing footer (`.footer-contact`) contains an `<a href="/changelog/">Changelog</a>` link. Same on chapter pages.
- The "A note on dated claims" section on `/foreword/` contains the text `I do my best to keep the manual current and maintain a` AND an `<a href="/changelog/">changelog</a>` link in the same paragraph.
- Hash-redirect map on landing: `/#changelog` lands on `/changelog/`.

## Build pipeline changes

- `build/build_spa.py`: `SECTION_SLUGS` entry, parser heading-pattern row, boundary regex update, TOC slot, `{{DATE_MODIFIED_HUMAN}}` substitution.
- `build/spa_template.html`: `.footer-copy` text update.
- `source/Ship_It_With_AI.md`: new Changelog section + "A note on dated claims" sentence.
- `build/tests/verify_seo_pass.js`: new assertions.

## Error handling

- Parser: if `## Changelog` isn't matched by the new regex, the existing "unknown section in SECTION_SLUGS" runtime error fires loudly (already wired).
- TOC builder: if changelog isn't slotted, the verify script's sitemap-count assertion catches it (count stays at 20 instead of 21).
- Footer: if `{{DATE_MODIFIED_HUMAN}}` isn't substituted, the `render_template_with_placeholders` helper (from the SEO pass) raises on unsubstituted `{{...}}` placeholders.

## Out of scope (explicit)

- Per-section last-updated dates. Single build-time stamp is correct given the build is one artifact per push.
- Auto-generating changelog from git history. Manual entries with editorial selection.
- RSS / Atom feed for changelog. Static page only.
- Subscribe / notification mechanism.
- Linking individual changelog entries to their PRs (could add commit/PR refs later; not now to keep entries terse).

## Open items for user review

1. **The four initial changelog entries** as drafted above — voice and length match the author's preference? Each is one paragraph; the spec leans terse. User revises during diff review if needed.
2. **Day-of-month formatting**: `%B %d, %Y` produces `May 27, 2026` (zero-padded day on Linux; single-digit days like the 7th render as `May 07, 2026`). If non-padded preferred (`May 7, 2026`), switch to `%B %-d, %Y` (GNU extension). Spec uses zero-padded for simplicity.

## Resolved decisions

1. **Date placement**: footer only — one segment inside `.footer-copy`, immediately after the copyright holder.
2. **Changelog as dedicated page**: `/changelog/`. New top-level section.
3. **Initial content**: backfill the three recent passes + first-public-version entry (2026-05-26, verified against `git log --reverse`).
4. **Granularity**: dates only, no commit SHAs or PR links in changelog entries (keep them terse and human-readable).
5. **Update mechanism**: manual editorial — author adds entries on each meaningful release. Smaller copy-edits don't get a changelog row (footer date covers them).
6. **TOC placement of changelog**: between About-the-author and Appendix A (housekeeping sequence).
7. **Breadcrumb shape**: `Home → Changelog` (two-level), matching About/Foreword/Closing.
8. **No RSS feed in this pass.**
9. **Changelog link placement**: inside `.footer-contact` (alongside email + LinkedIn + ai-leaders.ro), NOT in `.footer-copy`. Changelog is semantically a navigation link; placing it in the copyright row with the same `·` separator would visually treat it as another data field. Putting it in `.footer-contact` reuses existing link styling — no new CSS rules needed.
10. **Reading-time badge suppressed on the changelog page** (`kind="changelog"`). A ~150-word page rendered as "1 min read" feels confused.
11. **Prev/next nav on changelog**: prev = `/about-the-author/`, next = `/appendix-a-cost-economics/`. No customization needed; follows the section-order default.
12. **`/read/` page** contains the changelog inline AND a footer link to `/changelog/`. Mild redundancy accepted — the footer link is consistent across pages and serves users who want to deep-link or share the changelog URL.
