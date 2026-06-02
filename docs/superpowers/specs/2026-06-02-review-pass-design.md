# Review Pass (Editorial + SEO/Build) — Design

**Date:** 2026-06-02
**Author:** Mihai (via Claude Code)
**Status:** Draft v2 — reviewer-panel findings applied; pending user review
**Basis:** 8-agent two-team review of 2026-06-02 (4 book editors + 4 SEO/Pages devs). Findings in memory `ship-it-with-ai-review-2026-06`.
**Reviewed:** 4-reviewer spec panel of 2026-06-02 (developmental, copy/accuracy, SEO/GEO, perf/build) — corrections folded in; see "Reviewer panel — applied findings" at the end.

---

## Goal

Apply the findings of the 2026-06-02 review panel to both surfaces of *Ship It With AI* in a single coordinated pass: the manuscript (`source/Ship_It_With_AI.md`) and the generated GitHub Pages site (`build/build_spa.py` + `build/spa_template.html` → `_site/`). Both surfaces graded B+ ("strong, one or two decisions from excellent"); the defects are concentrated and mostly cheap. This pass closes them.

User chose **one combined spec**, **maximal editorial depth**, and the authorial directions recorded below. Organized as seven workstreams (A–G) grouped by surface and risk, implemented in dependency order (build hardening → site/template → manuscript content → re-verify).

## Why now

The book is published live at `ship-it-with.ai` and is explicitly built to be discovered and cited by AI answer engines. Two classes of defect undercut that goal: (1) credibility errors a skeptical senior engineer catches on a spot-check (a fabricated citation author, a wrong canonical repo URL, case-note tables that contradict their own prose), and (2) a duplicate-content / not-answer-ready site posture leaving rankings and citations on the table. Both fixable now, before the book is promoted further.

## Resolved decisions

### Authorial (user-decided in brainstorming)

1. **Foreword spine — reconcile both, explicitly.** Durability ("a way of thinking that survives the tools") = *why it matters*; control ("agentic delivery is a control problem") = *how the book is organized*. Name the relationship crisply so the two stop competing. The control mapping **already exists in the manuscript at `:129`** ("Architecture is the control of capability… Method… workflow… Reality… adoption") — this pass *revises that sentence* to label the division of labor, not adds a second statement of it. Thread the control names into the three Part dividers and the Closing; durability keeps the epigraph and emotional close.
2. **Primary reader — the staff+/tech-lead champion** who runs the practice *and* must sell it upward. Reframe leadership-facing material (Ch.3, Ch.8, Ch.10, Appendix A) as "what you hand your manager / what you need from them." Sharpen the Foreword audience paragraph and "How to read."
3. **Editorial depth — maximal.** Corrections + Foreword/reader reframe + Ch.8/Ch.9 surgery + testing-depth and war-story expansion + all P2 editorial polish.
4. **GEO content — add question-headings + visible FAQ.** Touches manuscript (question-shaped sub-headings, **anchored**) and build (visible FAQ rendering + per-chapter mirrors).

### Default decisions (Claude-proposed)

5. **`/read/` → `noindex, follow`** (not self-canonical); drop `/read/` from `sitemap.xml`. **Requires** editing the test suite: `build/tests/verify_seo_pass.js:299` asserts exactly 21 sitemap URLs → change to **20**, and add a "/read/ carries `noindex`" assertion. `follow` is kept so the page isn't a crawl dead-end (note: `/read/` only links chapters via in-page `#fragments`, so it routes little equity regardless).
6. **Number style:** spell out zero–nine; numerals for 10+ and all percentages/statistics, body and apparatus; declare in "A note on dated claims." *Borderline authorial — shifts the spelled-out voice on stats. Author sign-off required.*
7. **Dashes:** keep spaced-hyphen ` - ` house style; normalize only the stray em-dashes. **Exempt** the Changelog `### DATE — TITLE` header convention (6 of the 8 em-dashes are these deliberate headers); only `:2021` and `:2436` are prose strays. Declare the house style in "A note on dated claims."
8. **AGENTS.md links:** one link per **chapter/appendix unit** (the `SECTION_SLUGS` page units the build already parses), first occurrence only, rest bare; never inside a code fence. This auto-satisfies the Changelog "at most one per chapter" claim.
9. **Perf JS externalization (revised per panel):** externalize the **search index only** (`/search-index.json`, fetched on first overlay open). **Keep the app JS inline** — externalizing it trades zero-RTT first paint for no first-visit benefit on a mostly-single-page site. Keep critical CSS inline.

## Non-goals

- No page URL/slug changes. Existing section slugs survive. (Question-headings use in-page anchors only — no new page slugs.)
- No UI/theme redesign. Only the FOUC fix, `<picture>`, touch-target sizing, and the visible-FAQ block change rendered output.
- No chapter retitling.
- No wholesale voice rewrite. Authorial additions ship as in-voice sketches the author revises.
- No dismantling of Ch.3's five-layer narrative.
- No workshop-repo changes.

## Constraints

- The verify suite must pass after every workstream. **Note:** `npm run verify` runs `verify_feedback_pass.js` (landing page only, rebuilds); the script that actually serves and asserts against `_site/` is `verify_seo_pass.js` (unwired). This pass wires and uses the latter (see G1).
- "AGENTS.md", "opencode" (lowercase), "Permissions / Sandbox" (spaces around `/`) — canonical forms; do not regress.
- No Claude attribution in commits/PRs (user preference; matches git history).
- The build's section model (`SECTION_SLUGS`, `parse_sections`, `CHAPTER_SPLIT_RE`) is anchor/slug load-bearing; it fails loud (`RuntimeError`) on unknown/duplicate page-level headings, so a `## Chapter`-level change breaks the build rather than shipping silently. `###`-level changes do not touch it. Heading work (C7/D4/F1) stays behind the verify suite.

---

## Design

Format per item: **[ID] Title** — `location` — current → change. Authorial items carry an in-voice sketch the author revises.

### Workstream A — Manuscript: credibility & correctness (mechanical)

- **[A1] Appendix C citation fixes** — `source/Ship_It_With_AI.md`
  - `:2347` "Eve Cailey" → **Martin Paul Eve** (`eve.gd` is his). **Open question (panel):** the eve.gd post (2026-04-19) is about **`.env` auto-load/exfiltration**, but `:2347` attaches the citation to the **permission-parser-bypass class** (`open()`/`fs.readFile` evading deny rules) — a *different* claim. Either find the correct source for the parser-bypass claim, or repoint the Eve citation to the `.env` class (note `:2333` already cites Knostic for `.env`). Fixing only the name leaves a source↔claim mismatch.
  - `:2384` opencode repo `opencode-ai/opencode` → **`github.com/sst/opencode`** (the canonical SST/Anomaly project; `opencode-ai/opencode` is an unrelated Go project). Propagate to implied references at `:412`, `:510`.
  - `:2319`/`:2321` CVE-2025-59536: clarify "disclosed & patched Oct 2025 (Claude Code v1.0.111); Check Point writeup Feb 2026." (Manuscript already says "patched in v1.0.111," so this is a clarity improvement, not an error correction.)
  - `:786`/`:2289` METR (optional): name models — "Cursor Pro with Claude 3.5/3.7 Sonnet." Figures (19% / 24% / 43-point) correct; keep.

- **[A2] Case-note table reconciliation** — exactly two boxed case-note "Agent time" tables exist (`:447`, `:1288`); both have the prose-contradiction; the tables are the drifted slot, prose is canonical.
  - `:447` two-agent demo: `~8 minutes` → `~4 min wall clock (two panes in parallel)` (matches `:416` "four minutes thirteen seconds", `:518`).
  - `:1288–1290` banking case: `~25 minutes` → "fifteen/eighteen minutes" (`:1237`,`:1267`); `3 of 47 modules` → "two modules" (`:1275`); "**wire transfer subsystem**" → "**customer onboarding** domain" (`:1261`,`:1265`). (The book defines "Wire" as inter-bank at `:1108`, so "wire transfer" is a genuine cross-case bleed.)

- **[A3] Prologue appositive fix** — `:201` "PocketOS's production database, all the customer reservations… was wiped." *Not* a subject–verb error (subject "database" is singular, so "was" is correct); the defect is the **comma-fenced appositive reading as a false plural** + missing serial "and." Recast with em-dashes isolating the appositive: "PocketOS's production database — all the customer reservations, payment records, and vehicle inventory — was wiped." (Highest-visibility sentence in the book.)

- **[A4] Anchor-incident precision** —
  - DataTalks.Club `:531`/`:2303`/`:2305`: the apparatus states the **wrong mechanism as fact** ("duplicate resources collided") and "recovery took weeks." Correct (not merely hedge) to: "ran `terraform destroy` against a **stale state file**; **~24h partial recovery** (AWS restored ~1.94M rows from snapshot)." Also fix the date: reporting says **late February 2026**, not "March 2026" (`:531`,`:2303`).
  - PocketOS date `:199`: **leave as-is.** "April 24, 2026" is correct and uniform across sources — do **not** soften (would remove accurate precision). *(Reversed from v1.)*

### Workstream B — Manuscript: consistency sweeps (mechanical)

- **[B1] AGENTS.md de-linking** — **92 bare + 21 linked = 113 total** (v1's "113 bare" was wrong). Apply decision #8. There are **no** linked `[AGENTS.md]` inside code fences today (in-fence occurrences are already bare) — so this is a forward-looking rule, not a defect to fix. Reconcile the Changelog claim at **`:2031`** ("collapsed to at most one per chapter"; a second, vaguer mention sits at `:2029` — keep both consistent).

- **[B2] Number style** — apply decision #6. Body spells stats ("nineteen percent" `:786`; "forty-one percent" `:1850`) vs apparatus numerals (`:186`,`:2286`). Normalize %/stats to numerals body-and-apparatus; declare in "A note on dated claims" (`:151–155`). *(Author sign-off — see decision #6.)*

- **[B3] "Opencode" → "opencode"** — `:412,:420,:422,:424,:426,:430,:468` (7 sentence-initial auto-caps, all in Ch.2). Rewrite each so "opencode" is not sentence-initial.

- **[B4] Hyphenation** — pick **"post-mortem"** (match Anthropic usage `:2309`) over "postmortem" (`:57`); collapse "operating-system level" → "OS-level" at `:426`, `:551`, `:608` (dominant form, 11×). **Drop the "six-phase" item** — `:828`/`:832` are already correct ("six phases" as a noun is open; "six-phase loop" attributive is hyphenated). *(Reversed from v1.)*

- **[B5] Dash normalization** — apply decision #7: normalize only the two prose strays (`:2021`, `:2436`); **leave the six `### DATE — TITLE` Changelog headers** (`:2011`,`:2015`,`:2019`,`:2023`,`:2027`,`:2031`) — they're a deliberate pattern. Declare the house style in "A note on dated claims."

### Workstream C — Manuscript: structure & argument (authorial — in-voice sketches)

- **[C1] Foreword reconcile-both spine** — **revise `:129`** (the existing control-mapping sentence) to name the division of labor; lightly set it up at `:119–125`. Make durability=why / control=how a labeled relationship, not two competitors.
  > *Sketch (author revises, as a revision of `:129`):* "Two things are true about what follows. The **why** is durability — tools churn quarterly, and a practice pinned to this month's tool dies with it; what survives is a way of thinking. The **how** is control: this book is organized as three controls you take back in order — Architecture is the control of **capability**, Method the control of **workflow**, Reality the control of **adoption**. Durability is why you should care; control is how the book is built."
  - Retitle the three Part dividers to name their control (`:225`/`:739`/`:1341` — pure-prose epigraphs, not slugged headings, so safe).
  - **Closing — split the instruction:** name the three-control recap at `:1924–1928` (the "invariant" recap); add the loop-closing beat *beside the durability close* at `:1950`/`:1970–1972` (the epigraph reprise).

- **[C2] Primary-reader commitment + leadership reframe** — Foreword `:55/:99`, "How to read" `:135–147`, leadership chapters Ch.3/8/10/App-A, grassroots arc `:1728/:1732`. (App-A already ends pointing at Ch.10's procurement conversation `:2071`; the reframe describes what these sections already do.)
  > *Sketch (author revises):* "This manual is written for one reader: the senior engineer — staff, principal, tech lead — who will run this practice on a real team and then defend it upward. You do the work in Parts I–II; you need Part III to win the argument with the people who sign off."
  - One-line orienting note on leadership sections ("what to hand your manager / what you'll need"). Sharpen "How to read" to one primary path + optional detours, not four co-equal tracks.

- **[C3] "Highest-leverage" dedup** — reserve the superlative for the architecture review (`:1217`,`:1319`, both Ch.7). Downgrade Research at `:876` to "highest leverage *within the loop*." (Closing `:1954` says "lowest-cost test," not the literal phrase — the conflict is conceptual; handle by not letting Research own the superlative.)

- **[C4] Ch.8 reproportion** — `:1345–1597` (longest chapter). Cut worked examples 4–6 (`:1550–1568`, already flagged "briefer" at `:1550`) to a compact table; keep the spine (eight signals → traffic light → signal-6 weighting `:1544`). Reclaim ~600–800 words.

- **[C5] Ch.9 rebalance** — `:1598–1722`. Relocate pattern 5 ("governance for AI-selling companies," `:1655–1667`) to Ch.10/sidebar — it's audience-segment advice, not a brownfield operating pattern. **Removing it drops the "default" tier from five to four**, so this REQUIRES rewriting the count language at **`:1603`** ("The first five are the default…"), **`:1671`** ("Five patterns. Worktrees. Champions…"), and **`:1707`** ("The final three are maturity patterns") to "**four default + three maturity = seven**." Keep the tier split (it's real and explicit) — just re-count it.

- **[C6] Testing depth + war-story diversification** — *new authored content; specify for the plan:*
  - "Trusting agent-written tests" treatment → home in **Ch.5 Verify** (`:928–941`) or **Ch.8**; ~250–400 words; builds out the characterization caveat (`:1383`), kill-signal-1 (`:1371`), the "test was wrong" beat (`:982`). Cover test-quality, coverage gaming, backend verification depth.
  - **Two** failure stories that break the "Team A freestyles / Team B disciplines / B wins" shape (`:792`,`:804`, both currently in Ch.4): a *discipline that backfired* (→ Ch.9 patterns or a Ch.4 sidebar, to avoid stacking a third vignette in Ch.4) and an *adoption that succeeded without the full loop* (the case conceded at `:171`). ~150–250 words each. **Acceptance:** neither uses the A/B-symmetry structure.
  - *In-voice sketches drafted in the plan; author owns final voice.*

- **[C7] Front-matter resequencing** — `:135–192`. Move "How to read," "A note on dated claims," "Cases used" toward a back-matter reference cluster (or compress hard); land the Prologue within ~1,200 words. **Build-risk:** these sections carry `{#…}` slugs and participate in `parse_sections`. If a move would change a slug (Non-goal), **fall back to compress-in-place.** Behind the verify suite.

- **[C8] P2 editorial polish** — corrected counts: thin "is real" (**×16**, not 11) by ~⅓ toward the specific consequence; vary the closest "compound/compounding" pairs (×13); break the longest anaphoric "The agent…" runs (`:1141–1143`,`:1375`,`:1449–1451`). **Drop the "Said plainly" item** — it appears only twice (`:299`,`:379`, both Part I); it's not a tic. **"Try it yourself" consistency:** present in Ch.2 (`:506`), Ch.4 (`:711`), Ch.7 (twice — `:1189`,`:1317`), Ch.8 (`:1582`); missing from Ch.1,3,5,6,9,10; Ch.7 has a duplicate. Decide one rule (every chapter with a runnable exercise) and apply — including de-duplicating Ch.7 — rather than spot-adding two.

### Workstream D — Site: indexing & crawl

- **[D1] `/read/` noindex** — emit `<meta name="robots" content="noindex, follow">` on `/read/` via the existing `head_extra` hook (precedent: 404 at `build_spa.py:2115`); exclude `/read/` from `sitemap.xml`. (See decision #5 for the required `verify_seo_pass.js` edits.)
- **[D2] FAQPage de-dup** — keep `FAQPage` JSON-LD on landing only; drop from `/read/` (moot once noindexed). Per-chapter FAQ schema added in F2.
- **[D3] `/read/` social URLs** — `_site/read/index.html:17,:32` og:url/twitter:url `→ /` → real `https://ship-it-with.ai/read/`.
- **[D4] Section-page heading hierarchy — scope per-chapter.** Not all section pages are flat (Ch.1 already has real `<h2>/<h3 id>` because its subheads use `### … {#anchor}`). The pathology hits chapters whose bodies lack anchored subheads (Ch.6, Ch.10). Two causes: (a) the chapter-title `<h2 id="chapter-N">` is consumed by `CHAPTER_SPLIT_RE` (`:732–770`) so it isn't the visible secondary heading; (b) bodies lack `##/###`. Fix = **manuscript anchored subheads** (same mechanism as F1) for the affected chapters, **plus** demote the keyboard-overlay UI `<h2 id="kbdOverlayTitle">` (`spa_template.html:1949`) to a non-heading element. `Section.h2_subsections` (`:77`) is declared-but-unused dead code — TOC subsection surfacing is **out of scope** (don't assume it exists).
- **[D5] og:type — per-mode placeholder.** `spa_template.html:14` is a hardcoded literal `content="article"` shared by ALL pages, **not** a placeholder. Introduce `{{OG_TYPE}}` and substitute by `SITE_MODE` (already known per page): `website` for landing, `article` for chapters and `/read/`. A naive literal edit would wrongly flip all 19 chapter pages.

### Workstream E — Site: performance

- **[E1] Dark-mode FOUC** — theme init runs at body-end (`spa_template.html:2123`; `</head>` at `:1998`). Add a synchronous head snippet (idempotent with the existing body-end logic; CSP-safe — no CSP in repo) **after `{{HEAD_EXTRA}}` (`:36`), before `<style>` (`:38`)**: `<script>try{var t=localStorage.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>`.
- **[E2] Cover image** — `_site/index.html:1975` serves only `cover.jpg` (206 KB); `cover.webp` (139 KB) built but unreferenced; 1200×630 in a ≤720px column. Wrap in `<picture>`; **generate a 720px variant** — extend `cover_to_webp.py` (currently hardcodes 1200×630 at `:19`,`:40` and writes to **repo root** `:18`) to also emit `cover-720.webp` **into `build/static/`** so `copy_static()` deploys it. Keep `loading="lazy"` + explicit dimensions. **Leave og:image/twitter:image as `cover.jpg`** (`spa_template.html:20,30`) — JPEG is the safe social-card format; do not swap to webp.
- **[E3] Externalize the search index only** (decision #9, revised). Move the ~17 KB `searchIndex` JSON to `/search-index.json`, fetched on first overlay open (reuse the `/deferred.css` preload machinery, `build_spa.py:1333`). **Keep the ~28 KB app JS and critical CSS inline.**
- **[E4] Touch targets** — `.topbar-btn` (~36–38px; `spa_template.html:204–227`, `padding:6px 12px`) → `min-height:44px` under `@media (max-width:720px)`.

### Workstream F — Site: answer-engine readiness (GEO)

- **[F1] Question-shaped headings — anchored form mandatory.** The renderer omits markdown's `toc` extension (`build_spa.py:1147–1152`), so a bare `### Q?` gets **no id** — invisible to anchors/TOC/`¶`. Use the explicit attr_list form the Foreword/Ch.1 already use (e.g. `:289 ### Permissions / Sandbox {#permissions-sandbox}`): `### What is AGENTS.md? {#what-is-agents-md}`. Add ~8–10 across chapters: Ch.1 primitive, Ch.5 six-phase loop, Ch.6 AGENTS.md + AGENTS.md-vs-CLAUDE.md, Ch.8 "when not to," Ch.10 rollout, App-A cost; plus production-ready / MCP / vibe-coding where they fit. In-voice phrasing, not keyword-stuffed.
- **[F2] Visible FAQ + per-chapter mirror — single source of truth.** Define one Python data structure (`FAQ_ENTRIES = [{q, a, home_slug}]`) in `build_spa.py` that emits **both** the visible landing `<section>` (`<h2>`+`<h3>`) **and** every `FAQPage` JSON-LD block, so landing, visible copy, and per-chapter schema cannot drift. Mirror relevant Q&As onto their home chapter (AGENTS.md→Ch.6, cost→App-A, rollout→Ch.10) with a per-page `FAQPage`. Expand 4→~8 (add: agentic-vs-vibe-coding, MCP, six-phase loop, production-ready/safe). FAQ answer copy is authored content (in-voice).
- **[F3] llms.txt enrichment** — one-line description after each link (llmstxt.org convention) + a `## Author` section (name + LinkedIn). `llms-full.txt` is exemplary — leave it.
- **[F4] AI-corpus discoverability** — add `<link rel="alternate" type="text/markdown" href="https://ship-it-with.ai/llms-full.txt" title="Full text (Markdown)">` (+ one for `llms.txt`) to the template `<head>`; sitewide footer link. **`/read/` stays linked in `llms.txt`** intentionally (llms.txt is an LLM affordance, not a crawl directive) despite the `noindex` — note this so the two surfaces are consistently reasoned.
- **[F5] keywords meta** — `spa_template.html:9`: trim to 4–5 durable head terms (or drop; near-zero ranking weight).
- **[F6] Chapter share framing** — chapter og/twitter description defaults to the "control problem, not a tooling problem" thesis dek when none is punchy; eyeball `cover.jpg` social-card legibility.

### Workstream G — Site: build & deploy hardening

- **[G1] CI gate — wire the RIGHT verifier.** `npm run verify` → `verify_feedback_pass.js`, which **rebuilds and checks the repo-root landing page only — it never serves `_site/`.** The script that serves `_site/` and asserts `404.html`/`sitemap.xml`/`/read/`/size-floors is **`verify_seo_pass.js`** (`buildAndServe('_site')`, `:148–297`), currently **unwired**. Actions:
  - Add `"verify:site": "node tests/verify_seo_pass.js"` to `build/package.json`, with a **no-rebuild mode** (env flag) so it tests the bytes CI just built rather than rebuilding.
  - In `.github/workflows/static.yml`, between "Build SPA" (`:37`) and "Setup Pages" (`:39`): assert `_site/{index.html,.nojekyll,CNAME,404.html,sitemap.xml}` exist, `index.html` > ~50 KB, and the directory count matches (see below); then run `npm ci && npx playwright install --with-deps chromium && npm run verify:site`. Fail the job on any failure.
  - **Directory-count constant:** `_site/` has **21 subdirs = 19 sections + `read/` + 1 redirect stub (`chapter-1-six-primitives/`)**. Drive the assertion from G4's `len(sections) == 19` single source, not a hand-counted literal.
  - **Playwright in CI:** pin `playwright` exactly (currently `^1.60.0`, `package.json:11`) and cache `~/.cache/ms-playwright` keyed on that version; note the ~30–90s `--with-deps` download/network cost.
- **[G2] Pin the build dependency** — replace `pip install markdown` (`static.yml:34`) with `build/requirements.txt` (`markdown==3.10.2` + `--hash=sha256:…`) and `pip install --require-hashes -r build/requirements.txt`; add `setup-python` `cache: pip`. (`markdown==3.10.2` has **no runtime deps**, so a single hash satisfies `--require-hashes`.)
- **[G3] Build determinism** — `build_spa.py:1618, :1832, :2363–2365` use `datetime.now(timezone.utc)` for sitemap `lastmod` / JSON-LD `dateModified` / footer. Derive from the source's last git-commit date with a `SOURCE_DATE_EPOCH` override and `os.stat(SOURCE).st_mtime` fallback. **Required:** set `fetch-depth: 0` in `actions/checkout` (`static.yml:26`) — the default shallow clone makes `git log` return the CI commit time, not the content's true edit date.
- **[G4] Build hygiene** — `build_spa.py:18` wrap `import markdown` in a friendly `ImportError` guard; `:2399` replace the stale "18 total" comment with `assert len(sections) == EXPECTED` (currently emits 19) — the single source of truth for G1's count.

---

## Sequencing / build order

1. **G (build hardening) first** — pin deps, determinism, the section-count assert, and wire `verify:site` as the local safety net (the CI-gate step lands here too).
2. **D, E, F-build (template/generator)** — SEO/perf/GEO changes in `spa_template.html` + `build_spa.py`. Rebuild + `verify:site` after each.
3. **A, B, C, F1 (manuscript)** — corrections, sweeps, structural surgery, anchored question-headings. Rebuild + verify; confirm slugs/anchors survive (C7/D4/F1).
4. **F2 (visible FAQ)** — depends on both Q&A copy and the `FAQ_ENTRIES` generator change; after 2+3 settle.
5. **Full re-verify** — `verify:site` + the `test_*.js` suite + a manual `_site/` spot-check (`/read/` noindex + absent from sitemap; FAQ renders; question-headings anchored & present; head theme-init present; cover `<picture>`).

## Verification

- Per-workstream: `python3 build/build_spa.py` (exit 0; fail-loud parser) then `npm run verify:site` (the `_site/`-serving asserter — newly wired in G1).
- **Edits to existing tests:** `verify_seo_pass.js:299` sitemap count 21 → 20; add `/read/ robots=noindex` assertion. Keep the existing "/read/ canonical=/ + #chapter anchors" block (still valid).
- New assertions: landing renders a visible FAQ `<section>`; chosen question-headings appear **with ids** in per-section HTML; `<head>` theme-init present; `requirements.txt` is the install source; `og:type=website` on landing and `article` on a sampled chapter.
- A1 credibility items get a human/second-model spot-check of corrected citations before commit (esp. the open A1 eve.gd claim↔source question).

## Risks & open questions

- **C7 + D4 + F1 touch the heading/anchor model.** Mitigation: fail-loud build + `verify:site`; compress-in-place fallback for C7.
- **B2 number-style (decision #6)** shifts the spelled-out voice on statistics — author sign-off.
- **A1 eve.gd citation** attaches a `.env` source to a parser-bypass claim — resolve before committing A1.
- **C6** is net-new prose needing the most author involvement; sketches only in the plan.

---

## Reviewer panel — applied findings (2026-06-02)

Four reviewers (developmental, copy/accuracy, SEO/GEO, perf/build) verified this spec against the manuscript, `build_spa.py`, `_site/`, the test suite, and the web. All four: **"yes-with-fixes."** Verifications and corrections folded into v2:

**Confirmed correct (kept):** A1 citations (Martin Paul Eve, `sst/opencode`, CVE timeline — all web-verified); A2 reconcile targets (prose is canonical); A4 DataTalks mechanism (stale state + `destroy` + ~24h); D1 `/read/` duplicate content (byte-identical text confirmed) and `noindex` path (`head_extra` precedent); E1/E2 premises; G3/G4 cite sites; G2 (no transitive deps).

**P0 corrections (would have broken/misled implementation):**
1. C1 — revise existing `:129` mapping, don't add (else printed twice).
2. F1/D4 — bare `###` get no id (no `toc` ext); mandate anchored `{#slug}` form.
3. D5 — og:type is a shared template literal; needs `{{OG_TYPE}}` per-mode placeholder.
4. Decision #5 — must edit `verify_seo_pass.js:299` (21→20); v1 only "added."
5. G1 — `npm run verify` is landing-only and never touches `_site/`; wire `verify_seo_pass.js` + no-rebuild mode.
6. E2 — no 720px downscale tool exists; specify extending `cover_to_webp.py` → `build/static/`.
7. A4/B4 — PocketOS date (April 24) and `:828/:832` "six-phase" are **already correct**; removed from scope (v1 would have degraded correct text).

**Decision flipped:** #9 — externalize search index only; keep app JS inline (panel evidence: gzip already covers the repeated payload; externalizing app JS loses zero-RTT first paint for no first-visit gain).

**P1/P2 corrections:** B1 count (92 bare, not 113); decision #8 "section" defined as `SECTION_SLUGS` units; A3 relabelled (appositive, not S/V agreement); A4 DataTalks date (late Feb, not March) + correct-don't-hedge; C5 count-sentence edits (`:1603`/`:1671`/`:1707`); C6 placements + word budgets + acceptance; C8 counts ("is real" ×16; "Said plainly" dropped; real "Try it yourself" distribution + Ch.7 dup); B4 `:551` added, B5 Changelog-header em-dashes exempted; D1 `follow` rationale softened; F2 single `FAQ_ENTRIES`; F4 `/read/`-in-llms.txt reconciled; G1 dir-count (19/21) tied to G4; G3 `fetch-depth: 0`; E1 insertion anchor named; Changelog ref `:2029`→`:2031`.
