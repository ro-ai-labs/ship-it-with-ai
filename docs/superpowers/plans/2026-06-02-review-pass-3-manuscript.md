# Review Pass — Plan 3: Manuscript (Corrections, Sweeps, Structure, GEO Headings) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply every manuscript-side review finding to `source/Ship_It_With_AI.md` — credibility corrections, consistency sweeps, the Foreword/reader reframe and structural surgery, and anchored question-headings — without breaking the build's section/anchor model.

**Architecture:** One source file (`source/Ship_It_With_AI.md`), edited in eleven tasks grouped by kind. Mechanical fixes (A, B) are exact before/after. Authorial rewrites (C1, C2, C6) ship as **DRAFT sketches the author revises** — the plan provides faithful starting prose and exact insertion points, not final voice. Every task ends by rebuilding and running `verify:site`; several add a content assertion to `build/tests/verify_seo_pass.js` (the repo's established way to test prose — it already greps for phrases like "Eight inspection points"). This is **Plan 3 of 4** (spec Workstreams **A, B, C, F1**; spec: `docs/superpowers/specs/2026-06-02-review-pass-design.md`). It depends on **Plan 1** (`verify:site`).

**Tech Stack:** Markdown source; Python build (`build/build_spa.py`, fail-loud on heading/anchor breakage); Playwright content verifier.

**Conventions:** run from repo root; commit prefixes `content:`/`fix:`; **no Claude attribution**. After every task: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | tail -2; cd ..` must end `Verification PASSED.` (the build raises if any `## Chapter`/slug invariant breaks).

**Author-review gate:** Tasks 7, 8, 10 (C1/C2/C6) contain authored prose. The implementing agent applies the DRAFT, but flags the diff for Mihai's voice pass before the task's commit is considered final. Decision #6 (number style, Task 5) also needs his sign-off.

**Note on a panel drift:** the Changelog "AGENTS.md links collapsed to at most one per chapter" line is at **`:2029`** (verified by direct read), not `:2031` as the spec/panel stated. This plan uses `:2029`.

---

### Task 1: Appendix C citation fixes (A1)

**Files:** Modify `source/Ship_It_With_AI.md` (`:2347`, `:2384`, `:2321`); optional `:2296`.

- [ ] **Step 1: Fix the fabricated author** — `:2347`
Before: `**Source:** [eve.gd](https://eve.gd) (Eve Cailey), public writeup of the architectural class.`
After:
```markdown
**Source:** [Martin Paul Eve](https://eve.gd), public writeup of the permission-parser bypass class.
```
**Author check:** confirm the eve.gd post actually covers the *permission-parser bypass* claim at `:2346` (it is known to cover `.env` auto-loading, which is already cited separately at `:2333` via Knostic). If the parser-bypass writeup is a different/missing source, either cite the correct URL or move this citation to the `.env` class. Do not ship the name fix alone if the source↔claim mismatch stands.

- [ ] **Step 2: Fix the opencode repo URL** — `:2384`
Before: `**Source:** opencode repository ([github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode)); LICENSE and README.`
After:
```markdown
**Source:** opencode repository ([github.com/sst/opencode](https://github.com/sst/opencode)); LICENSE and README.
```

- [ ] **Step 3: Clarify the CVE timeline** — `:2321`
Before: `**Caveat:** Patched in Claude Code v1.0.111. Versions earlier than the patch remain vulnerable; the class survives even after the specific patch.`
After:
```markdown
**Caveat:** Disclosed and patched in Claude Code v1.0.111 (October 2025); the Check Point writeup was published February 2026. Versions earlier than the patch remain vulnerable; the class survives even after the specific patch.
```

- [ ] **Step 4 (optional): name METR models** — only if doing the optional enrichment, in the METR source entry, change "Cursor with Claude" to "Cursor Pro with Claude 3.5/3.7 Sonnet". (Skip if not touching that entry.)

- [ ] **Step 5: Verify + commit**
Run: `grep -n 'sst/opencode' source/Ship_It_With_AI.md && grep -c 'Eve Cailey\|opencode-ai/opencode' source/Ship_It_With_AI.md` → expect the sst line present and the count `0`. Then build+verify (above).
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: fix Appendix C citations (Martin Paul Eve, sst/opencode, CVE timeline)"
```

---

### Task 2: case-note table reconciliations (A2)

The boxed case-note tables contradict their prose. Prose is canonical.

**Files:** Modify `source/Ship_It_With_AI.md` (`:447`, `:1288-1290`).

- [ ] **Step 1: Two-agent demo table** — `:447` `Agent time | ~8 minutes` →
```markdown
| Agent time | ~4 min wall clock (two panes in parallel) |
```
(Matches prose `:416` "four minutes thirteen seconds" and `:518`. Keep the surrounding table rows; edit only the Agent-time value.)

- [ ] **Step 2: Banking case table** — `:1288-1290`. Reconcile to prose (`:1237/1267` "fifteen/eighteen minutes"; `:1275` "two modules"; `:1261/1265` "customer onboarding"):
  - `~25 minutes` → `~15-18 minutes`
  - `3 of 47 modules` → `two modules`
  - `deep domain knowledge of the wire transfer subsystem` → `deep domain knowledge of the customer onboarding domain`

- [ ] **Step 3: Verify + commit**
Run: `grep -n 'wire transfer subsystem\|3 of 47 modules\|~8 minutes\|~25 minutes' source/Ship_It_With_AI.md` → expect **no matches**. Build+verify.
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: reconcile case-note tables with their prose (timings, module count, domain)"
```

---

### Task 3: Prologue + anchor-incident precision (A3 + A4)

**Files:** Modify `source/Ship_It_With_AI.md` (`:201`; `:531`/`:2302`/`:2305`). **Leave the PocketOS date — April 24, 2026 is correct and uniform across sources; do NOT soften it.**

- [ ] **Step 1: Prologue appositive** — `:201`. The false-plural appositive reads as an error (subject "database" is singular, so "was" is correct grammar; the fix is readability). Change:
Before: `PocketOS's production database, all the customer reservations, payment records, vehicle inventory, was wiped.`
After:
```markdown
PocketOS's production database — all the customer reservations, payment records, and vehicle inventory — was wiped.
```

- [ ] **Step 2: DataTalks mechanism + date in Appendix C** — `:2302` and `:2305`. Public reporting is: stale Terraform state file + `terraform destroy` + ~24h partial recovery; the date is late February 2026.
`:2302` before: `In March 2026, Alexey Grigorev at DataTalks.Club lost two and a half years of course infrastructure when Claude Code worked against an incomplete Terraform state file, created duplicate resources where real ones existed, and ran destructive commands when the duplicates collided.`
After:
```markdown
In late February 2026, Alexey Grigorev at DataTalks.Club lost two and a half years of course infrastructure when Claude Code worked against a stale Terraform state file and ran `terraform destroy` against what it read as orphaned resources.
```
`:2305` before: `**Caveat:** Data loss was partial; recovery took weeks. The incident is documented publicly but with less coverage than PocketOS.`
After:
```markdown
**Caveat:** Data loss was partial; AWS restored roughly 1.94M rows from a snapshot within about a day. The incident is documented publicly but with less coverage than PocketOS.
```

- [ ] **Step 3: DataTalks mention in Chapter 3** — `:531` (the in-chapter telling). Align its mechanism to "stale state file / `terraform destroy`" and drop "recovery took weeks" if stated; match the Appendix wording. (Read `:528-535`, edit the mechanism clause to match Step 2; keep the chapter's narrative voice.)

- [ ] **Step 4: Verify + commit**
Run: `grep -n 'recovery took weeks\|created duplicate resources where real ones\|In March 2026, Alexey' source/Ship_It_With_AI.md` → expect **no matches**. Build+verify.
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: fix Prologue appositive; correct DataTalks mechanism/date (stale state, ~24h)"
```

---

### Task 4: AGENTS.md de-linking (B1)

Rule (spec decision #8): **one `[AGENTS.md](https://agents.md/)` link per chapter/appendix unit** (the `SECTION_SLUGS` page units), first occurrence only; the rest bare `AGENTS.md`; never inside a code fence (already true — no in-fence links exist).

**Files:** Modify `source/Ship_It_With_AI.md` (the 21 linked occurrences); verify against the existing test.

- [ ] **Step 1: Inventory the links**
Run: `grep -n '\[AGENTS\.md\](https://agents\.md/)' source/Ship_It_With_AI.md`
Expected: 21 lines. Note which `SECTION_SLUGS` unit each belongs to (front matter = the foreword/prologue/contents region; then per chapter/appendix).

- [ ] **Step 2: Unwrap all but the first per unit**
For each page unit, keep the link on its **first** occurrence and replace every later `[AGENTS.md](https://agents.md/)` in that unit with bare `AGENTS.md`. Front matter occurrences (`:173`, `:184`, the Contents/Scope/Cases region) collapse to a single link in that front-matter unit. (The existing verifier already asserts ≤1 outbound agents.md link **per chapter page** at `verify_seo_pass.js:466-477` — this rule satisfies it.)

- [ ] **Step 3: Reconcile the Changelog claim** — `:2029` says "AGENTS.md links collapsed to at most one per chapter." Leave it (now accurate). If you want a record, add a one-line entry to the current changelog pass — but that belongs to the changelog update at pass end, not here.

- [ ] **Step 4: Verify + commit**
Run: `python3 build/build_spa.py >/dev/null && cd build && SITE_NO_REBUILD=1 npm run verify:site 2>&1 | grep -i 'agents.md de-link'; cd ..`
Expected: `OK: AGENTS.md de-link: every chapter page has <= 1 outbound agents.md link`.
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: enforce one AGENTS.md link per section unit"
```

---

### Task 5: number style — stats as numerals (B2) — AUTHOR SIGN-OFF

Spec decision #6 (borderline authorial): spell out zero–nine; **numerals for 10+ and for all percentages/statistics**, body and apparatus, so the same stat doesn't appear two ways.

**Files:** Modify `source/Ship_It_With_AI.md`; add the rule to "A note on dated claims" (`:151-155`).

- [ ] **Step 1: Confirm with Mihai** that stat-numerals are wanted (it shifts the spelled-out voice, e.g. "nineteen percent" → "19%"). If he prefers to preserve spelled-out prose, the fallback is: keep spelled-out in body, numerals in tables/appendix, and only fix cases where the *same* statistic appears both ways. Proceed per his choice.

- [ ] **Step 2: Convert body statistics to numerals** (primary path). Examples: `:786` "nineteen percent"/"twenty-four percent" → "19%"/"24%"; `:1850` "forty-one percent"/"twenty-eight percent" → "41%"/"28%", "thirteen of the twenty" → "13 of the 20", and similar across the body. Leave spelled-out small counts that are not statistics (e.g. "two reviewers", "six phases"). Sweep with `grep -nE '(percent|points)' source/Ship_It_With_AI.md` and convert the statistical ones.

- [ ] **Step 3: Declare the rule** — append to "A note on dated claims" (`:153`):
```markdown
Number style: statistics and percentages use numerals (19%, 43 points); small non-statistical counts are spelled out.
```

- [ ] **Step 4: Verify + commit**
Run: `grep -n 'nineteen percent\|forty-one percent' source/Ship_It_With_AI.md` → expect **no matches** (primary path). Build+verify.
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: numerals for statistics/percentages; declare the rule"
```

---

### Task 6: lexical consistency (B3 + B4 + B5)

**Files:** Modify `source/Ship_It_With_AI.md`.

- [ ] **Step 1: "Opencode" → "opencode" (B3)** — `:412, :420, :422, :424, :426, :430, :468` (7 sentence-initial caps in Ch.2). Rewrite each so the brand isn't sentence-initial, e.g. "Opencode is written…" → "The opencode build is written…" / "In opencode, …". (Do not just lowercase mid-sentence — fix the sentence so lowercase reads correctly.)

- [ ] **Step 2: Hyphenation (B4)** — pick **post-mortem**: `:57` "postmortems" → "post-mortems" (matches `:2309` "post-mortem"). Collapse "operating-system level" → "OS-level" at `:426`, `:551`, `:608`. **Do NOT touch "six-phase"** — `:828/:832` are already correct.

- [ ] **Step 3: Em-dash strays (B5)** — normalize only the two prose strays (`:2021`, `:2436`) to the spaced-hyphen house style. **Leave the six `### DATE — TITLE` Changelog headers** (`:2011/2015/2019/2023/2027/2031`) — deliberate pattern. Add to "A note on dated claims": `Dashes: the manual uses spaced hyphens ( - ) for parenthetical breaks; em-dashes appear only in dated section headers.`

- [ ] **Step 4: Verify + commit**
Run: `grep -nE '^[^a-z]*Opencode |postmortem|operating-system level' source/Ship_It_With_AI.md` → expect **no matches** (the `Opencode ` sentence-initial check and the two hyphenation items). Build+verify.
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: opencode casing, post-mortem/OS-level hyphenation, dash strays"
```

---

### Task 7: Foreword reconcile-both spine (C1) — DRAFT, AUTHOR REVISES

The control mapping already exists at `:129`; name the durability↔control relationship so they stop competing, add control subtitles to the Part dividers, and close the control loop in the Closing.

**Files:** Modify `source/Ship_It_With_AI.md` (`:129`; Part dividers `:223`, `:739`, `:1341`; Closing `:1924-1928` and near `:1950`).

- [ ] **Step 1: Name the relationship at `:129`** — insert at the start of the existing central-claim paragraph (before "The central claim…"):
> **DRAFT (author revises):** "Two framings run through this manual, and they are not rivals. *Durability* is why it matters — tools churn quarterly, and a practice pinned to this month's tool dies with it. *Control* is how the book is organized. "
Then keep the existing sentences (the three-layer control mapping is already there and stays).

- [ ] **Step 2: Add control subtitles to the three Part dividers** — after each Part heading, add an italic subtitle line:
  - `:223` after `# Part I - Architecture` → `*The control of capability: what the agent can know and do.*`
  - `:739` after `# Part II - Method` → `*The control of workflow: how work is formulated, executed, and verified.*`
  - `:1341` after `# Part III - Reality` → `*The control of adoption: where the method applies and where it must not.*`
  (Pure prose under the heading — no slug, safe for the build.)

- [ ] **Step 3: Close the control loop in the Closing** — the recap at `:1924-1928` already names the three invariants; add one clause tying them back to "control of capability / workflow / adoption," and beside the durability close at `:1950` add a sentence that the three controls are what durability buys. **DRAFT — author revises for voice.**

- [ ] **Step 4: Verify + commit (after author voice pass)**
Run: `grep -n 'control of capability\|control of workflow\|control of adoption' source/Ship_It_With_AI.md` → expect the Part-divider subtitles present. Build+verify.
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: reconcile durability/control framing; control subtitles on Part dividers"
```

---

### Task 8: primary-reader commitment + leadership reframe (C2) — DRAFT, AUTHOR REVISES

Commit the staff+/tech-lead-champion as primary; reframe the four-persona router and tag leadership chapters as "ammunition to hand upward."

**Files:** Modify `source/Ship_It_With_AI.md` (`:55` area / `:135-145`; light notes on Ch.3/8/10/App-A openings).

- [ ] **Step 1: Name the primary reader** — in the Foreword (after `:55` or in the frame section), add:
> **DRAFT (author revises):** "This manual is written for one reader above the others: the senior engineer — staff, principal, tech lead — who will run this practice on a real team and then have to defend it upward. You do the work in Parts I and II; you need Part III to win the argument with the people who sign the budget."

- [ ] **Step 2: Reframe "How to read"** (`:135-147`) — convert the four co-equal personas into one primary path + optional detours. Keep the role pointers, but subordinate them:
> **DRAFT:** "Read it linearly the first time. If you are leading the rollout (staff/tech-lead), that linear read is your path. **Hand upward:** Chapter 3, Chapter 8, Chapter 10, and Appendix A are what you give your manager — risk posture, portfolio classification, rollout, and cost. **Facilitating?** Appendix B is the artifact set."

- [ ] **Step 3: One-line orienting notes** on Ch.3/8/10/App-A openings ("What to hand your manager / what you'll need from them"). **DRAFT — author revises.**

- [ ] **Step 4: Verify + commit (after author voice pass)** — build+verify; the existing maintenance/role assertions still pass.
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: commit primary reader (staff+/champion); reframe leadership chapters as ammunition"
```

---

### Task 9: highest-leverage dedup + Ch.8 trim + Ch.9 rebalance (C3 + C4 + C5)

**Files:** Modify `source/Ship_It_With_AI.md` (`:876`; `:1550-1568`; `:1603/1655-1667/1671/1707`).

- [ ] **Step 1: Highest-leverage dedup (C3)** — `:876`. Reserve the superlative for the architecture review (the Closing elevates it at `:1954`).
Before: `Research is also the phase that, in my experience, has the highest leverage.`
After:
```markdown
Research is also the phase that, in my experience, has the highest leverage within the loop.
```

- [ ] **Step 2: Ch.8 trim (C4)** — `:1550-1568` (examples four–six, already flagged "briefer"). Compress the three to a compact table or two sentences each, preserving their distinct shapes (greenfield green-plus / internal-tool green-leaning / vendor-fork red) and the per-example "lesson." Keep the spine (`:1538-1546`) intact. Target ~600-800 words reclaimed.
> **DRAFT replacement** for `:1550-1568`: a 3-row table — | Project | Signals | Color | Lesson | — one row each for greenfield (0, green-plus, "treat agent involvement as a first-class architectural decision"), internal tool (1, green-leaning, "internal tools are ideal training grounds"), vendor fork (4, red, "the diagnostic sometimes questions whether the codebase should exist"). Author tightens prose.

- [ ] **Step 3: Ch.9 rebalance (C5)** — relocate pattern 5 ("governance for AI-selling companies," `:1655-1667`) to a Ch.10 sidebar or cut to a cross-reference. **Removing it drops the default tier from five to four**, so update the count language in all three places:
  - `:1603` "The first five are the default operating patterns" → "The first four are the default operating patterns"
  - `:1671` "Five patterns. Worktrees. Champions. hookify rules. PR review toolkit. Governance for AI-selling companies." → "Four patterns. Worktrees. Champions. hookify rules. PR review toolkit."
  - `:1707` "The final three are maturity patterns" → keep "three," but verify the surrounding "5 + 3" framing now reads "4 + 3 = seven."

- [ ] **Step 4: Verify + commit**
Run: `grep -n 'highest leverage within the loop\|The first four are the default' source/Ship_It_With_AI.md` → expect both present; `grep -c 'Governance for AI-selling companies' source/Ship_It_With_AI.md` → expect it now appears only in its relocated home. Build+verify.
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: dedup highest-leverage; trim Ch.8 examples; rebalance Ch.9 to seven patterns"
```

---

### Task 10: testing depth + war stories (C6) — DRAFT, NEW CONTENT, AUTHOR REVISES

**Files:** Modify `source/Ship_It_With_AI.md` (new prose in Ch.5 Verify `:928-941` or Ch.8; two failure stories outside Ch.4).

- [ ] **Step 1: "Trusting agent-written tests"** — ~250-400 words after the Verify-phase Playwright passage (`:940`). Build out the seed at `:982` ("the test was wrong - it asserted the old format") and the characterization caveat (`:1383`). Cover: tests can be wrong/gameable; coverage % is not correctness; who reviews the agent's tests; backend verification depth.
> **DRAFT (author revises) opening:** "A green test suite the agent wrote is evidence, not proof. In the worked example above, one of the six tasks shipped a *passing* test that asserted the old log format — green, and wrong. The discipline that catches this is the same one humans need: review the test, not just its color…"

- [ ] **Step 2: Two failure stories that break the A/B-symmetry shape** (`:792/:804` are both Ch.4 "Team A freestyles / Team B disciplines"). Add, outside Ch.4:
  - A *discipline that backfired* (→ Ch.9 patterns or a Ch.4 sidebar) — ~150-250 words.
  - An *adoption that succeeded without the full loop* (the case "Scope and limits" concedes at `:171`) — ~150-250 words, ideally in Ch.10 or Ch.9.
> **DRAFT direction:** make each *specific and surprising*; neither uses the "two adjacent teams, B wins" structure. Author supplies the real anecdotes; the plan reserves the slots and states the acceptance criterion.

- [ ] **Step 3: Verify + commit (after author writes the real prose)** — build+verify.
```bash
git add source/Ship_It_With_AI.md
git commit -m "content: add 'trusting agent-written tests' + two non-symmetric failure stories"
```

---

### Task 11: front-matter resequencing + P2 polish + question-headings (C7 + C8 + F1)

**Files:** Modify `source/Ship_It_With_AI.md`.

- [ ] **Step 1: Front-matter resequencing (C7)** — move "A note on dated claims" (`:151`) and "Cases used in this manual" (`:177`) toward a back-matter reference cluster (near the Appendices), and compress "How to read" (`:135`). **Build-risk:** these carry `{#…}` slugs and are parsed as page units. If a move would change a slug (Non-goal), **compress in place instead.** After moving, run the build — it raises loudly if a `SECTION_SLUGS` unit breaks. If it breaks, revert to compress-in-place.

- [ ] **Step 2: P2 polish (C8)** — thin "is real" (×16) by ~⅓ toward the specific consequence; vary the closest "compound/compounding" pairs (×13); break the longest anaphoric "The agent…" runs (`:1141-1143/1375/1449-1451`). **Drop the "Said plainly" item** (only ×2, both Part I — not a tic). "Try it yourself" consistency: present in Ch.2 (`:506`), Ch.4 (`:711`), Ch.7 (`:1189` and `:1317` — a duplicate), Ch.8 (`:1582`); missing from Ch.1,3,5,6,9,10. Decide one rule (every chapter with a runnable exercise), apply it, and de-duplicate Ch.7.

- [ ] **Step 3: Anchored question-headings (F1)** — add `### Question? {#slug}` headings (the **anchored** form is mandatory — the build omits `toc`, so bare `###` get no id). Place ~8-10 in-voice:
  - Ch.1 `:233` area → `### What is a coding-agent primitive? {#what-is-a-primitive}`
  - Ch.5 (six-phase loop intro) → `### What is the six-phase agentic loop? {#what-is-the-six-phase-loop}`
  - Ch.6 `:1022` (Names and conventions) → `### What is AGENTS.md? {#what-is-agents-md}` and, before the CLAUDE.md contrast, `### AGENTS.md vs CLAUDE.md: what's the difference? {#agents-md-vs-claude-md}`
  - Ch.8 (kill-signals intro) → `### When should you not use AI coding agents? {#when-not-to-use-agents}`
  - Ch.10 (rollout) → `### How do you roll out AI coding agents on a team? {#how-to-roll-out}`
  - Appendix A → `### How much does agentic coding cost? {#how-much-does-it-cost}`
  - plus "Are AI coding agents production-ready?", "What is MCP?", "Agentic coding vs vibe coding?" where they fit.
  Phrasing stays in-voice; match each chapter's heading style (Ch.1 already uses `### … {#…}`; for bold-run-in chapters the question heading precedes the relevant run-in).

- [ ] **Step 4: Assert the anchors render with ids + verify**
Add to `build/tests/verify_seo_pass.js`:
```javascript
    // GEO question-headings render WITH anchor ids (bare ### would have none).
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'chapter-6-agents-md', 'index.html'), 'utf8');
      if (!/id="what-is-agents-md"/.test(html)) fail('Ch.6 question-heading "what-is-agents-md" missing or anchorless');
      else ok('Ch.6 question-heading anchored (#what-is-agents-md)');
    }
```
Run build+verify → `Verification PASSED.`
```bash
git add source/Ship_It_With_AI.md build/tests/verify_seo_pass.js
git commit -m "content: front-matter resequence, prose-tic thinning, anchored GEO question-headings"
```

---

## Self-Review

**Spec coverage:** A1→T1, A2→T2, A3/A4→T3, B1→T4, B2→T5, B3/B4/B5→T6, C1→T7, C2→T8, C3/C4/C5→T9, C6→T10, C7/C8/F1→T11. ✅

**Placeholder scan:** Authorial tasks (7, 8, 10) carry explicit **DRAFT** prose + exact insertion points + an author-review gate — not "write something here." Mechanical tasks are literal before/after. T3 Step 3 and T5 Step 2 are sweeps with the grep that bounds them.

**Consistency:** PocketOS date is *kept* (T3 explicitly says don't soften — matches spec v2's reversal). "six-phase" is *not* touched (T6 says so — matches the panel's "already correct"). The `:2029` changelog line is used (corrected from the panel's `:2031`). F1 mandates the anchored `{#slug}` form everywhere (matches Plan 2's D4 dependency and the build's missing-`toc` reality).

**Build-safety:** Every task rebuilds; the build fails loudly on any `## Chapter`/slug breakage. C7 (the one structural-move risk) has an explicit compress-in-place fallback.

**Author gate:** Tasks 5, 7, 8, 10 flagged for Mihai (number-style decision + three authored-prose tasks). The implementing agent drafts; he revises voice before those commits are final.

---

## Execution Handoff

Plan 3 of 4. After it, **Plan 4** (visible FAQ) wires the question-content into a single `FAQ_ENTRIES` source feeding the visible section + per-chapter `FAQPage` schema.
