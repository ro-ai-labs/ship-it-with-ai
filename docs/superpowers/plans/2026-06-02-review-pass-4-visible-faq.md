# Review Pass — Plan 4: Visible FAQ + Per-Chapter Schema Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the site "answer-ready": render the existing FAQ as visible, crawlable HTML and mirror each Q&A onto its home chapter as `FAQPage` schema — driven by a single source of truth so the visible copy and every JSON-LD block can never drift.

**Architecture:** Introduce one `FAQ_ENTRIES` list in `build/build_spa.py`; two pure render helpers (`faq_jsonld`, `faq_visible_html`) consume it. The landing page emits both the visible `<section>` and the `FAQPage` JSON-LD from it; each relevant chapter appends a `FAQPage` for the entry that "lives" there; `/read/` stops emitting `FAQPage` (cleanly retiring the duplicate the noindex in Plan 2 only masked). Expand the FAQ from 4 to 8 entries. This is **Plan 4 of 4** (spec items **F2** + the clean half of **D2**; spec: `docs/superpowers/specs/2026-06-02-review-pass-design.md`). It depends on **Plan 1** (`verify:site`) and reuses content themes from **Plan 3** (the four new answers are authored, in-voice).

**Tech Stack:** Python generator (`build/build_spa.py`), JSON-LD, Playwright verifier.

**Conventions:** run from repo root; commit prefix `feat(geo):`; **no Claude attribution**. After each task: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..` ends `Verification PASSED.`

**Author gate:** the four NEW answers in Task 1 are DRAFT prose (faithful to the book's framing) — flag for Mihai's voice pass before final commit. The existing four are lifted verbatim from the current schema.

---

### Task 1: define `FAQ_ENTRIES` + the two render helpers (single source of truth)

**Files:** Modify `build/build_spa.py` — add near the current FAQ literal (`~:1408`, replacing the inline FAQ's role).

- [ ] **Step 1: Add the data structure and helpers**

Add this block (just above `HOMEPAGE_HEAD_SCHEMA` at `:1412`):
```python
# Single source of truth for the FAQ. Each entry renders to (1) the visible
# landing <section>, (2) the landing FAQPage JSON-LD, and (3) — when home_slug
# is set — a FAQPage block on that chapter page. The first four answers are the
# ones previously inlined in HOMEPAGE_HEAD_SCHEMA; the last four are new.
FAQ_ENTRIES: list[dict] = [
    {
        "q": "What is agentic coding?",
        "home_slug": None,
        "a": "Agentic coding is the practice of using AI agents that read, write, run, and verify code largely on their own, with humans in the loop for review and governance rather than for every keystroke. Unlike autocomplete or chat assistants, an agentic system holds a multi-step plan, executes through real tools (filesystem, shell, browser, version control), and surfaces work for verification rather than producing isolated suggestions.",
    },
    {
        "q": "How does agentic coding differ from AI autocomplete and from vibe coding?",
        "home_slug": None,
        "a": "Autocomplete completes the next token under your cursor. Vibe coding accepts whatever the model generates with minimal verification. Agentic coding sits between: the agent plans, edits across files, runs tests, and reports back, but the human controls the context the agent sees, the actions it can take, the verification gates it passes through, and the adoption surface it operates on. The difference is methodological discipline, not model quality.",
    },
    {
        "q": "What is AGENTS.md and why does it matter?",
        "home_slug": "chapter-6-agents-md",
        "a": "AGENTS.md is a plain-Markdown file at the root of a repository that tells coding agents how the project actually works — forbidden patterns, conventions, build commands, where things live, and the mistakes the team has already made. It is the de-facto standard across Claude Code, Codex, Cursor, and Aider for instructing agents at the project level, and is tracked as an open standard at agents.md.",
    },
    {
        "q": "How do you safely roll out AI coding agents in an engineering team?",
        "home_slug": "chapter-10-adoption-90-days",
        "a": "A safe rollout treats agentic delivery as a control problem with five layers of governance: permissions, sandboxing, secrets, security hooks, and telemetry. Pair that with a clear methodology — a six-phase loop covering research, plan, execute, review, verify, ship — and a 90-day adoption arc with three named roles (Champion, Lead, Manager). Skip any of these and adoption produces more harm than benefit.",
    },
    # --- NEW (DRAFT — author revises voice) ---
    {
        "q": "What is the six-phase agentic loop?",
        "home_slug": "chapter-5-six-phase-loop",
        "a": "The six-phase loop is a delivery discipline for agentic work: research (the agent maps the codebase into a durable note), plan (a reviewable file-level task list), execute (constrained subagents make the changes), review (separate spec-compliance and code-quality passes), verify (new tests run, including accessibility-tree UI tests), and ship (a normal pull request your existing process reviews). Most failures route back to plan, not back to research.",
    },
    {
        "q": "How much does agentic coding cost?",
        "home_slug": "appendix-a-cost-economics",
        "a": "Per-seat tool pricing is the small line item; the real cost is total cost of ownership — seats, token/usage, the human review time the loop requires, and the governance setup. The durable way to budget is to match seat tier to actual usage rather than buying uniform tooling, and to compare the loaded cost of agent-assisted delivery against the cost of the work it replaces, not against zero.",
    },
    {
        "q": "What is MCP (Model Context Protocol)?",
        "home_slug": "chapter-1-primitives",
        "a": "MCP, the Model Context Protocol, is a specification that lets a coding agent connect to external tools and data sources — issue trackers, databases, documentation, internal services — through a uniform interface. It is one of the agent primitives: where Tools are the agent's built-in actions, MCP is how the agent reaches capabilities the harness did not ship with.",
    },
    {
        "q": "Are AI coding agents production-ready?",
        "home_slug": "chapter-8-readiness-kill-signals",
        "a": "It depends on the codebase, not the company. Readiness is a per-project question answered by eight kill signals and a green/yellow/red traffic light: a well-tested, documented, decoupled module with a team that can evaluate the output is green; an undocumented, untested, tightly-coupled system whose team cannot verify the result is red. Most companies have a mix, and the mix tells you the order of operations.",
    },
]


def faq_jsonld(entries: list[dict]) -> str:
    """One <script type=ld+json> FAQPage block for the given entries."""
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": e["q"],
             "acceptedAnswer": {"@type": "Answer", "text": e["a"]}}
            for e in entries
        ],
    }
    return ('<script type="application/ld+json">'
            + json.dumps(faq, ensure_ascii=False)
            + '</script>')


def faq_visible_html(entries: list[dict]) -> str:
    """Visible, crawlable FAQ section: real <h2>/<h3> so search + answer engines
    see question→answer adjacency (not just JSON-LD)."""
    items = "\n".join(
        f'        <h3>{html_lib.escape(e["q"])}</h3>\n'
        f'        <p>{html_lib.escape(e["a"])}</p>'
        for e in entries
    )
    return (
        '\n      <section class="article-faq" id="faq" aria-labelledby="faq-heading">\n'
        '        <h2 id="faq-heading">Frequently asked questions</h2>\n'
        f'{items}\n'
        '      </section>\n'
    )
```

- [ ] **Step 2: Confirm it imports/parses**
Run: `python3 -c "import sys; sys.path.insert(0,'build'); import build_spa; print(len(build_spa.FAQ_ENTRIES), 'entries'); print(build_spa.faq_jsonld(build_spa.FAQ_ENTRIES)[:40]); import json; json.loads(build_spa.faq_jsonld(build_spa.FAQ_ENTRIES).split('>',1)[1].rsplit('<',1)[0])" && echo "FAQ JSON-LD parses"`
Expected: `8 entries`, a `<script…` prefix, and `FAQ JSON-LD parses`.

- [ ] **Step 3: Commit**
```bash
git add build/build_spa.py
git commit -m "feat(geo): single-source FAQ_ENTRIES + faq_jsonld/faq_visible_html helpers"
```

---

### Task 2: landing emits FAQ from the new source; `/read/` drops FAQPage (D2)

**Files:** Modify `build/build_spa.py` — `HOMEPAGE_HEAD_SCHEMA` (`:1452-1491`), the schema-build site (`:2366`), `render_read` head_schema.

- [ ] **Step 1: Remove the inline FAQPage from the Book+Org literal**

In `HOMEPAGE_HEAD_SCHEMA`, delete the third `<script type="application/ld+json"> … "@type": "FAQPage" … </script>` block (`:1452-1490`), so the constant ends right after the Organization block's `</script>` followed by the closing `'''`. The literal now holds **Book + Organization only**.

- [ ] **Step 2: Build a with-FAQ landing schema and a no-FAQ read schema**

At the orchestration site (`:2366`, `head_schema = _homepage_head_schema(...)`), replace with:
```python
    book_org_schema = _homepage_head_schema(author, number_of_pages, date_modified)
    head_schema_landing = book_org_schema + "\n  " + faq_jsonld(FAQ_ENTRIES)
    head_schema_read = book_org_schema  # /read/ is noindex + carries no FAQPage
```
Then pass `head_schema=head_schema_landing` to `render_landing(...)` (`:2377` area) and `head_schema=head_schema_read` to `render_read(...)` (`:2392` area). (Update the two call-sites' `head_schema=` argument accordingly.)

- [ ] **Step 3: Add the `/read/`-has-no-FAQ assertion**

In `build/tests/verify_seo_pass.js`, in the `/read/` block, add:
```javascript
      const readLd = [...html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)]
        .map(m => { try { return JSON.parse(m[1])['@type']; } catch { return null; } });
      if (readLd.includes('FAQPage')) fail('/read/ should not carry FAQPage (landing owns it)');
      else ok('/read/ carries no FAQPage');
```
(The existing landing assertion at `:64-70` still requires `FAQPage` on `/` — now satisfied by `faq_jsonld`. The 404 check at `:137` still forbids it there.)

- [ ] **Step 4: Build + verify**
Run the standard build+verify. Expected `Verification PASSED.` — landing still has `Book`/`Organization`/`FAQPage`; `/read/` no longer does.

- [ ] **Step 5: Commit**
```bash
git add build/build_spa.py build/tests/verify_seo_pass.js
git commit -m "feat(geo): drive landing FAQPage from FAQ_ENTRIES; remove it from /read/"
```

---

### Task 3: render the visible FAQ section + per-chapter FAQPage mirror

**Files:** Modify `build/build_spa.py` — `_landing_article_body` (`:1539`), `render_chapter_schema` (`:1875` return).

- [ ] **Step 1: Append the visible FAQ to the landing body**

`build/build_spa.py:1539`, change `_landing_article_body` to append the section:
Before:
```python
    return LANDING_ARTICLE_BODY.format(
        SUBTITLE=html_lib.escape(subtitle),
        AUTHOR=html_lib.escape(author),
        BYLINE_HREF=html_lib.escape(byline_href),
        TOC_HTML=toc_html,
    )
```
After:
```python
    body = LANDING_ARTICLE_BODY.format(
        SUBTITLE=html_lib.escape(subtitle),
        AUTHOR=html_lib.escape(author),
        BYLINE_HREF=html_lib.escape(byline_href),
        TOC_HTML=toc_html,
    )
    return body + faq_visible_html(FAQ_ENTRIES)
```

- [ ] **Step 2: Mirror each chapter's FAQ onto its page schema**

`build/build_spa.py`, in `render_chapter_schema`, change the return (`:1875-1882`) to append a `FAQPage` for entries that live on this page:
```python
    blocks = [
        f'<script type="application/ld+json">{json.dumps(tech_article, ensure_ascii=False)}</script>',
        f'<script type="application/ld+json">{json.dumps(breadcrumb_list, ensure_ascii=False)}</script>',
    ]
    page_faq = [e for e in FAQ_ENTRIES if e["home_slug"] == section.slug]
    if page_faq:
        blocks.append(faq_jsonld(page_faq))
    return "\n  ".join(blocks)
```
(So `chapter-6-agents-md`, `chapter-10-adoption-90-days`, `chapter-5-six-phase-loop`, `appendix-a-cost-economics`, `chapter-1-primitives`, and `chapter-8-readiness-kill-signals` each gain a one-question `FAQPage`.)

- [ ] **Step 3: Optional CSS** — if the FAQ section needs spacing, add a `.article-faq { margin-top: 2rem; }` rule in `build/spa_template.html` near the other article styles. (Skip if the inherited `<section>`/`<h3>` styling already reads cleanly — check the screenshot in Step 4.)

- [ ] **Step 4: Build + visually confirm**
Run: `python3 build/build_spa.py >/dev/null && grep -c 'class="article-faq"' _site/index.html && grep -o 'id="faq-heading"' _site/index.html`
Expected: count `1` and `id="faq-heading"`. Confirm a chapter mirror: `node -e "const fs=require('fs');const h=fs.readFileSync('_site/chapter-6-agents-md/index.html','utf8');const t=[...h.matchAll(/ld\+json\">(.*?)<\/script>/gs)].map(m=>{try{return JSON.parse(m[1])['@type']}catch{return null}});console.log(t)"` → includes `FAQPage`.

- [ ] **Step 5: Commit**
```bash
git add build/build_spa.py build/spa_template.html
git commit -m "feat(geo): visible landing FAQ section + per-chapter FAQPage mirror"
```

---

### Task 4: lock it down with assertions

**Files:** Modify `build/tests/verify_seo_pass.js`.

- [ ] **Step 1: Add the F2 assertions**
```javascript
    // Visible FAQ section on landing (real headings, not just JSON-LD).
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(baseUrl + '/');
      const faqH2 = await page.locator('section.article-faq h2#faq-heading').count();
      const faqH3 = await page.locator('section.article-faq h3').count();
      if (faqH2 !== 1) fail(`landing visible FAQ <h2> count ${faqH2}, expected 1`);
      else ok('landing has a visible FAQ section');
      if (faqH3 < 8) fail(`landing visible FAQ has ${faqH3} questions, expected >= 8`);
      else ok(`landing visible FAQ has ${faqH3} questions`);
      await ctx.close();
    }
    // Per-chapter FAQPage mirror lands on the right pages.
    {
      for (const slug of ['chapter-6-agents-md', 'appendix-a-cost-economics', 'chapter-10-adoption-90-days']) {
        const h = fs.readFileSync(path.join(repoRoot, '_site', slug, 'index.html'), 'utf8');
        const types = [...h.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)]
          .map(m => { try { return JSON.parse(m[1])['@type']; } catch { return null; } });
        if (!types.includes('FAQPage')) fail(`${slug} missing mirrored FAQPage`);
        else ok(`${slug} has mirrored FAQPage`);
      }
    }
```

- [ ] **Step 2: Full verify**
Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..`
Expected: `Verification PASSED.`

- [ ] **Step 3: Commit**
```bash
git add build/tests/verify_seo_pass.js
git commit -m "test(geo): assert visible FAQ + per-chapter FAQPage mirrors"
```

---

## Self-Review

**Spec coverage:** F2 (visible FAQ + per-chapter mirror + per-page FAQPage + expand to 8) → Tasks 1-4. D2 (FAQPage off `/read/`, cleanly) → Task 2. ✅

**Placeholder scan:** No TBD/TODO. The four new answers are complete DRAFT prose (author revises voice — gated). All code blocks are literal.

**Type/name consistency:** `FAQ_ENTRIES`, `faq_jsonld`, `faq_visible_html` defined in Task 1, used in Tasks 2-3; `home_slug` values are real `SECTION_SLUGS` keys (`chapter-6-agents-md`, etc., verified against the build's slug table). `id="faq-heading"`/`class="article-faq"` consistent across renderer (Task 3) and assertions (Task 4). The single-source design means the visible copy and all JSON-LD derive from one list — no drift (the panel's F2 concern).

**Cross-dependency captured:** Task 2 removes the inline FAQPage that the existing landing assertion (`:64`) relies on, and replaces it with `faq_jsonld(FAQ_ENTRIES)` — landing still has `FAQPage`, so that assertion stays green; the `/read/` and 404 forbid-FAQPage checks also stay correct.

---

## Execution Handoff

This completes the four-plan set for the 2026-06-02 review pass (spec: `2026-06-02-review-pass-design.md`). Recommended execution order: **Plan 1 → 2 → 3 → 4** (build harness first; manuscript before the FAQ that references its themes). All four use `npm run verify:site` (wired in Plan 1) as the gate.
