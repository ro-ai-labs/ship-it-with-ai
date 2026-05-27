# Permissions / Sandbox primitive — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote **Permissions / Sandbox** to a named primitive in the book (3rd slot, after Context window and Tools). Cascade ~13 source edits across Ch.1 / Ch.2 / Ch.3 / Closing / Appendix C / Changelog, rewrite `diagram_primitives()` for the 8-cell layout, and update the verify suite (4 existing assertions + 3 new positive markers + 1 new forbidden phrase).

**Architecture:** Linear cascade. Build-pipeline first (diagram), then source content in roughly file-order (Ch.1 → Ch.2 → Ch.3 → Closing → Appendix C → Changelog), then verify-suite updates, then visual verification, then push.

**Tech Stack:** Markdown edits to `source/Ship_It_With_AI.md`; Python edits to `build/build_spa.py`; JavaScript edits to `build/tests/verify_seo_pass.js`; Playwright for visual checks.

**Spec:** `docs/superpowers/specs/2026-05-27-permissions-sandbox-primitive-design.md`

**Precedent:** `docs/superpowers/plans/2026-05-27-memory-primitive-and-open-set.md` (Memory cascade — same shape).

---

## Conventions

- **Find/replace strings are verbatim** from the current source. Use the Edit tool with `old_string` set EXACTLY as shown.
- **Canonical written form:** `Permissions / Sandbox` (with spaces around `/`).
- **Em-dashes:** match local file style (the source uses ` - ` ASCII more than ` — ` Unicode; keep what's already there).
- **Commits:** plain, no Claude attribution, no `Co-Authored-By`, no "Generated with Claude Code" footer. Subject form `area: short imperative description`.
- **No push** until the final task; intermediate commits are local only.

---

## Task 1: Build — `diagram_primitives()` 8-cell rewrite

**Files:**
- Modify: `build/build_spa.py:314-340` (`diagram_primitives()` function)

**Why first:** independent of source content; verifiable in isolation by rebuilding and viewing `/chapter-1-primitives/`.

- [ ] **Step 1:** Read `build/build_spa.py:314-340` to confirm current state.

- [ ] **Step 2:** Edit `diagram_primitives()` to insert the new cell between `tools` and `skills`. The new cell carries:
  - icon: `⛨`
  - name: `permissions / sandbox`
  - sublist: two `primitive-sub` spans — `decision layer` and `OS enforcement`

  Use the same markup structure as the existing Memory cell (which has the `primitive-sublist` + two `primitive-sub` spans).

- [ ] **Step 3:** Update the `<figcaption>` to add one sentence about P/S being the second primitive whose convergence is partial across vendors (after Memory). Suggested addition: "Permissions / Sandbox sits in the third slot as a primitive whose two halves — the agent-level decision layer and OS-level enforcement — converge on presence but diverge on posture."

- [ ] **Step 4:** Rebuild: `python3 build/build_spa.py`. Confirm no errors.

- [ ] **Step 5:** Commit:
  ```
  build: 8-cell primitives diagram with Permissions / Sandbox in slot 3
  ```

---

## Task 2: Ch.1 — New Permissions / Sandbox section

**Files:**
- Modify: `source/Ship_It_With_AI.md` — insert new section between Tools section (ends ~line 310) and Skills section (starts ~line 312). Confirm exact insertion point by reading the file.

**Why second:** the section content underpins many of the downstream sweep edits.

- [ ] **Step 1:** Read `source/Ship_It_With_AI.md` lines 240-388 to map the Ch.1 structure and confirm the insertion point (between the end of Tools and the start of Skills).

- [ ] **Step 2:** Insert the new section. The heading is exactly:
  ```
  ### Permissions / Sandbox {#permissions-sandbox}
  ```

  The section body uses the in-voice prose sketch from the spec (Section 1) as the starting point. Revise the voice to match the surrounding chapter (short declarative sentences in series, "Said plainly:" reset move, no over-explaining concepts the reader knows). Target length: ~450 words. The two halves must be named in bold: `**The agent-level decision layer**` and `**The OS-level enforcement**`. The section must explicitly:
  - Name PocketOS in the first sentence.
  - Name Claude Code, Codex CLI, opencode, Cursor, Gemini CLI as the agents that ship the decision half.
  - Acknowledge the OS-enforcement posture asymmetry honestly (Codex defaults, Cursor + Gemini first-class, Claude Code opt-in, opencode soft-confinement only).
  - End with the forward-reference to Ch.3 about configuration surfaces.

- [ ] **Step 3:** Verify the section parses correctly by rebuilding (`python3 build/build_spa.py`) and visually confirming the section appears in `_site/chapter-1-primitives/index.html` at the expected location, with the anchor `id="permissions-sandbox"` present.

- [ ] **Step 4:** Commit:
  ```
  content: Ch.1 — new Permissions / Sandbox primitive section
  ```

---

## Task 3: Ch.1 — Vocabulary note rewrite (line 365)

**Files:**
- Modify: `source/Ship_It_With_AI.md:365` (the "A note on vocabulary" paragraph)

- [ ] **Step 1:** Read line 365 in context (lines 363-368).

- [ ] **Step 2:** Replace the existing vocabulary note with the rewrite from spec Section 2. Verbatim target text:

  > A note on vocabulary. The primitives named here are what the agent uses to know, act, gate, extend, integrate, remember, and delegate. The test for primitiveness is convergence: a mechanism is a primitive when every major coding agent ships it as a distinct, configurable bundle, even when the implementations differ substantively. Permissions / Sandbox passes that test on the decision-layer half across all the major agents; the OS-enforcement half is presence-converged but posture-divergent - Codex CLI defaults it on, Cursor and Gemini CLI ship it as a first-class option, Claude Code is opt-in, opencode leaves OS isolation to the operator. Same architectural role; different vendor postures. The Memory primitive has the same shape on its second half (auto-memory consolidation is an early-mover signal across Claude Code, with the others converging). Telemetry has not yet crossed the convergence line and remains a control layer around the primitives. When the next mechanism converges - observability event-push is the candidate to watch - the list will grow again.

  (Note: ASCII hyphens with spaces in place of em-dashes to match local file style.)

- [ ] **Step 3:** Confirm the old phrase `are not additional primitives` no longer exists in the file: `grep -c "are not additional primitives" source/Ship_It_With_AI.md` → expected `0`.

- [ ] **Step 4:** Commit:
  ```
  content: Ch.1 — rewrite vocabulary note (convergence test promotes P/S)
  ```

---

## Task 4: Ch.1 — Primary primitives list update (line 369)

**Files:**
- Modify: `source/Ship_It_With_AI.md:369`

- [ ] **Step 1:** Find the exact current text:
  > Context window. Tools. Skills. Plugins. MCP. Memory. Subagents. Plus the harness as the runtime that organizes them.

- [ ] **Step 2:** Replace with:
  > Context window. Tools. Permissions / Sandbox. Skills. Plugins. MCP. Memory. Subagents. Plus the harness as the runtime that organizes them.

- [ ] **Step 3:** Commit:
  ```
  content: Ch.1 — primary primitives list includes Permissions / Sandbox
  ```

---

## Task 5: Ch.1 — Eight → Nine questions + new P/S question (lines 371-373)

**Files:**
- Modify: `source/Ship_It_With_AI.md:371-373`

- [ ] **Step 1:** Read lines 371-373.

- [ ] **Step 2:** Insert a new question into line 371's enumerated rubric, between the MCP question ("Does it speak MCP, and how good is the MCP integration?") and the memory question ("Does it read a team-shared memory file at session start?"). Suggested wording: "What permission model does it ship - allow/ask/deny rules, auto-mode classifier - and what OS sandbox does it default to?"

- [ ] **Step 3:** Update line 373 from `Eight questions today; more tomorrow.` to `Nine questions today; more tomorrow.`

- [ ] **Step 4:** Commit:
  ```
  content: Ch.1 — add P/S question to evaluation rubric (Eight → Nine)
  ```

---

## Task 6: Ch.1 — Ship-this-week prompt update (line 385)

**Files:**
- Modify: `source/Ship_It_With_AI.md:385`

- [ ] **Step 1:** Read line 385 (the Ship-this-week prompt).

- [ ] **Step 2:** Add a P/S question to the rapid-fire prompt. Suggested placement: between the MCP question ("does this agent speak MCP") and the memory question ("where does the agent read team-shared memory from"). Suggested wording: "what allow/ask/deny model and what sandbox does this agent ship with".

- [ ] **Step 3:** Commit:
  ```
  content: Ch.1 — Ship-this-week prompt includes P/S question
  ```

---

## Task 7: Ch.1 — Subagents recursive definition (line 343)

**Files:**
- Modify: `source/Ship_It_With_AI.md:343`

- [ ] **Step 1:** Find the exact phrase: `A subagent is another instance of the primitives - it has its own context window, its own tools, its own skills, plugins, MCP, memory`

- [ ] **Step 2:** Replace with: `A subagent is another instance of the primitives - it has its own context window, its own tools, its own permissions / sandbox, its own skills, plugins, MCP, memory`

- [ ] **Step 3:** Commit:
  ```
  content: Ch.1 — subagents recursive definition includes permissions / sandbox
  ```

---

## Task 8: Ch.1 — ASCII diagram + figure caption sync (lines 240-261)

**Files:**
- Modify: `source/Ship_It_With_AI.md:240-261` (the ASCII-art diagram block in markdown source — renders verbatim in `/read/` + `_site/llms-full.txt`)

- [ ] **Step 1:** Read lines 235-265 to map the exact ASCII structure.

- [ ] **Step 2:** Insert a row for `permissions / sandbox (decision layer | OS enforcement)` between the `tools` row and the `skills` row. Match the indentation, pipe characters, and width of the existing rows. The Memory row's sublist syntax `memory (manually defined | auto-memory system)` is the template.

- [ ] **Step 3:** Update the source-side figure caption (line 261 area) to add the same one-sentence P/S note added to the HTML caption in Task 1.

- [ ] **Step 4:** Commit:
  ```
  content: Ch.1 — source ASCII diagram + caption include permissions / sandbox
  ```

---

## Task 9: Ch.2 — Inspection points re-count to Eight (lines 464-478)

**Files:**
- Modify: `source/Ship_It_With_AI.md:464-478`

- [ ] **Step 1:** Read lines 460-480.

- [ ] **Step 2:** Replace line 466's "Nine inspection points: ..." sentence with:
  > Eight inspection points: context assembly, tool registry, the Permissions / Sandbox primitive (decision layer + OS sandbox as two halves), skills loading, plugin extension, MCP support, memory layer, subagent dispatch - all wrapped by the harness's agent loop.

- [ ] **Step 3:** Read line 464 — if it also references "nine inspection points" (the lead-in sentence), update to "eight".

- [ ] **Step 4:** Replace line 478's Artifact callout `The nine inspection points from this chapter.` → `The eight inspection points from this chapter.`

- [ ] **Step 5:** Confirm: `grep -c "Nine inspection points\|nine inspection points" source/Ship_It_With_AI.md` → expected `0`.

- [ ] **Step 6:** Commit:
  ```
  content: Ch.2 — recount inspection points to Eight (P/S collapses two halves to one)
  ```

---

## Task 10: Ch.2 — Try-it-yourself prompt (line 496)

**Files:**
- Modify: `source/Ship_It_With_AI.md:496`

- [ ] **Step 1:** Find the exact phrase: `"Walk this codebase and name the primitives - context window, tools, skills, plugins, MCP, memory, subagents.`

- [ ] **Step 2:** Replace with: `"Walk this codebase and name the primitives - context window, tools, permissions / sandbox, skills, plugins, MCP, memory, subagents.`

- [ ] **Step 3:** Commit:
  ```
  content: Ch.2 — Try-it-yourself prompt includes permissions / sandbox
  ```

---

## Task 11: Ch.2 — Sandbox-as-primitive light edit (line 452)

**Files:**
- Modify: `source/Ship_It_With_AI.md:452`

- [ ] **Step 1:** Read line 452 in context (lines 450-456).

- [ ] **Step 2:** Light edit to anchor the existing claim about sandbox being a primitive into the new Ch.1 framing. Current text: `the sandbox is a primitive, and primitives are choices, and the choices a vendor makes about primitives are governance choices.` Proposed rewrite: `the OS-level half of the Permissions / Sandbox primitive named in Chapter 1 is where vendors diverge most, and the choices a vendor makes about primitives are governance choices.` Keep the surrounding flow.

- [ ] **Step 3:** Commit:
  ```
  content: Ch.2 — sandbox-as-primitive passage points to Ch.1 P/S framing
  ```

---

## Task 12: Ch.3 — Framing paragraph

**Files:**
- Modify: `source/Ship_It_With_AI.md` — insert new paragraph after the "least privilege is the spine" passage (line ~543) and BEFORE the "Layer one: permissions" treatment (line 566).

- [ ] **Step 1:** Read lines 540-570 to find the exact insertion point.

- [ ] **Step 2:** Insert the framing paragraph from spec Section 5 (with the Memory parallel sentence already integrated):

  > Three of these five layers - permissions, security hooks, sandbox - are the configuration surfaces of the Permissions / Sandbox primitive named in Chapter 1. The primitive is what every major coding agent ships; the surfaces are how your team configures it for your codebase, your threat model, your compliance posture. Same shape as Memory in Chapter 1: one primitive, multiple configuration surfaces. Memory has one (AGENTS.md / CLAUDE.md); Permissions / Sandbox has more. Secrets handling and telemetry are adjacent governance controls - they belong in this chapter because they catch what the primitive's surfaces miss, but they are not themselves configuration surfaces of the primitive. The five-layer treatment that follows is independent of whether you read the primitive as one bundle or five separate controls; both framings land the same configuration work.

  Add a paragraph separator (blank line) before and after.

- [ ] **Step 3:** Commit:
  ```
  content: Ch.3 — framing paragraph binds 3 of 5 layers to P/S primitive
  ```

---

## Task 13: Ch.3 — PocketOS callout edit (~line 533)

**Files:**
- Modify: `source/Ship_It_With_AI.md` — around line 533 (the existing Ch.3 PocketOS callout)

- [ ] **Step 1:** Read lines 525-540 to find the exact PocketOS sentence/paragraph.

- [ ] **Step 2:** Append a new sentence to that callout: `Permissions / Sandbox would have caught it twice - once at the decision layer if the rule had been there, once at the OS layer regardless.` Find an appropriate insertion point that flows naturally.

- [ ] **Step 3:** Commit:
  ```
  content: Ch.3 — PocketOS callout names P/S primitive explicitly
  ```

---

## Task 14: Closing — Part I summary (line 1902)

**Files:**
- Modify: `source/Ship_It_With_AI.md:1902`

- [ ] **Step 1:** Find the exact phrase: `The primitives - context window, tools, skills, plugins, MCP, memory, subagents - plus the harness that organizes them.`

- [ ] **Step 2:** Replace with: `The primitives - context window, tools, permissions / sandbox, skills, plugins, MCP, memory, subagents - plus the harness that organizes them.`

- [ ] **Step 3:** Commit:
  ```
  content: Closing — Part I summary includes permissions / sandbox
  ```

---

## Task 15: Appendix C — 3 new entries

**Files:**
- Modify: `source/Ship_It_With_AI.md` — Appendix C, "Tool documentation" group

- [ ] **Step 1:** Read the existing Appendix C structure (find with `grep -n "^### Tool documentation\|^## Appendix C" source/Ship_It_With_AI.md`). Identify the format used: claim / source / where-used / caveat.

- [ ] **Step 2:** Add three new entries (paralleling the Memory primitive sources added earlier today):

  1. **Claude Code permissions + sandbox documentation.** Claim: Claude Code ships an Allow/Ask/Deny permission model with deny→ask→allow precedence and an opt-in OS sandbox (Seatbelt on macOS, bubblewrap on Linux). Source: `https://code.claude.com/docs/en/permissions` and `https://code.claude.com/docs/en/sandboxing`. Where used: Ch.1 P/S section + Ch.3 layer-one and layer-two passages. Caveat: opt-in posture; default installation has no sandbox.

  2. **Codex CLI sandbox by default.** Claim: Codex CLI enforces OS-level sandbox by default on Linux (Landlock + seccomp via bwrap) and macOS (Seatbelt); restricted tokens + ACLs on Windows. Source: `https://developers.openai.com/codex/concepts/sandboxing` and `https://developers.openai.com/codex/agent-approvals-security`. Where used: Ch.1 P/S section + Ch.2 side-by-side. Caveat: opt-out posture is configurable.

  3. **opencode permission model + soft confinement.** Claim: opencode ships a permission-prompt model and path/permission validation but does not provide OS-level sandbox isolation; external Docker or microVM is the operator's responsibility. Source: Vercel KB at `https://vercel.com/kb/guide/running-opencode-securely-with-the-vercel-sandbox` (notes opencode's lack of sandbox explicitly). Where used: Ch.1 P/S section + Ch.2 side-by-side. Caveat: the "soft confinement" framing is the book's; opencode's docs do not claim sandbox.

- [ ] **Step 3:** Commit:
  ```
  content: Appendix C — 3 new entries for P/S primitive sources
  ```

---

## Task 16: Changelog entry

**Files:**
- Modify: `source/Ship_It_With_AI.md` — Changelog section (find with `grep -n "## Changelog" source/Ship_It_With_AI.md`)

- [ ] **Step 1:** Read the existing changelog to confirm the format and find the top of the entry list.

- [ ] **Step 2:** Insert a new entry at the top (newest first), dated 2026-05-27. Use the text from spec Section 8:

  > ### 2026-05-27 — Permissions / Sandbox primitive
  >
  > Permissions / Sandbox promoted to a named primitive - the third slot in the inventory, after Context window and Tools. Two halves like Memory: the agent-level decision layer (Allow / Ask / Deny + auto mode) and OS-level enforcement (Seatbelt / bubblewrap / restricted tokens / WSL2). The vocabulary note in Chapter 1 was rewritten to name the convergence test that promoted this primitive while leaving telemetry as a control layer. Chapter 3 gains a framing paragraph binding three of its five layers (permissions, hooks, sandbox) to the new primitive's configuration surfaces; the five-layer defense-in-depth narrative is preserved unchanged. Inspection-points count in Chapter 2 dropped from Nine to Eight (the two halves of P/S collapsed to one). Diagram updated to 8 cells. Three new Appendix C entries source the Claude Code / Codex / opencode implementations.

- [ ] **Step 3:** Commit:
  ```
  content: Changelog — 2026-05-27 P/S primitive entry
  ```

---

## Task 17: Verify suite — apply all assertion updates

**Files:**
- Modify: `build/tests/verify_seo_pass.js`

- [ ] **Step 1:** Search the verify suite for the assertions that need updating:
  - `grep -n "Eight inspection points\|Eight questions today\|Context window. Tools. Skills" build/tests/verify_seo_pass.js`

- [ ] **Step 2:** Apply the following updates per spec Section 9:

  1. **L582 — bump count:** `'Eight questions today'` → `'Nine questions today'`.
  2. **L590 — primitives list:** `'Context window. Tools. Skills. Plugins. MCP. Memory. Subagents.'` → `'Context window. Tools. Permissions / Sandbox. Skills. Plugins. MCP. Memory. Subagents.'`
  3. **L566 — flip Eight inspection points** from forbidden to positive marker (currently in the forbidden-list sweep; move to the positive-marker assertion that runs on `/chapter-2-anatomy-invariant/`).
  4. **L606-610 — sublist count:** tighten the assertion from `sublistCount < 1` to `sublistCount < 2` (locks the invariant that BOTH Memory + P/S cells carry sublists).

- [ ] **Step 3:** Add new forbidden phrase to the sweep: `'are not additional primitives'` (must NOT appear anywhere except possibly in `/changelog/` historical context — exclude `/changelog/` from the sweep using the existing changelog-exclusion mechanism).

- [ ] **Step 4:** Add new positive markers:
  - `'Permissions / Sandbox'` appears in `/chapter-1-primitives/`, `/chapter-2-anatomy-invariant/`, `/chapter-3-governance-in-layers/`.
  - H3 anchor `id="permissions-sandbox"` present in `/chapter-1-primitives/`.
  - Ch.3 framing-paragraph phrase `'configuration surfaces of the Permissions / Sandbox primitive'` appears in `/chapter-3-governance-in-layers/`.

- [ ] **Step 5:** Run the suite:
  ```bash
  cd /home/mihai/ai-labs/ship-it-with-ai
  python3 build/build_spa.py
  (lsof -ti:8774 | xargs -r kill 2>/dev/null; true) && python3 -m http.server -d _site 8774 > /tmp/srv.log 2>&1 &
  sleep 1
  cd build/tests && PORT=8774 node verify_seo_pass.js 2>&1 | tail -10
  lsof -ti:8774 | xargs -r kill 2>/dev/null
  ```
  Expected: `Verification PASSED.`

- [ ] **Step 6:** Commit:
  ```
  test: verify suite — update assertions for P/S primitive
  ```

---

## Task 18: Visual verification — screenshots + CSS fallback if needed

**Files:**
- Modify (if needed): `build/spa_template.html` — the `.diagram-primitives .primitives-grid` CSS rule (line ~1204).

- [ ] **Step 1:** Build + serve:
  ```bash
  cd /home/mihai/ai-labs/ship-it-with-ai
  python3 build/build_spa.py
  (lsof -ti:8775 | xargs -r kill 2>/dev/null; true) && python3 -m http.server -d _site 8775 > /tmp/srv.log 2>&1 &
  sleep 1
  ```

- [ ] **Step 2:** Capture screenshots at 3 viewports using Playwright. Test script (save as `/tmp/diagram-check.js`):

  ```js
  const { chromium } = require('/home/mihai/ai-labs/ship-it-with-ai/build/node_modules/playwright');
  (async () => {
    const browser = await chromium.launch();
    for (const vp of [{w:1280,h:800,n:'desktop'},{w:768,h:1024,n:'tablet'},{w:375,h:812,n:'mobile'}]) {
      const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
      const page = await ctx.newPage();
      await page.goto('http://127.0.0.1:8775/chapter-1-primitives/');
      const fig = page.locator('figure.diagram-primitives');
      await fig.scrollIntoViewIfNeeded();
      await fig.screenshot({ path: `/tmp/ps-diagram-${vp.n}.png` });
      // Count cells, check empty slots
      const info = await page.evaluate(() => {
        const cells = [...document.querySelectorAll('.primitives-grid > .primitive')];
        return cells.map(c => c.querySelector('.primitive-name')?.textContent.trim() || '?');
      });
      console.log(vp.n, 'cells:', info);
      await ctx.close();
    }
    await browser.close();
  })();
  ```

  Run: `node /tmp/diagram-check.js`

- [ ] **Step 3:** Review the 3 screenshots. The acceptance criteria:
  - All 8 named primitives visible (no clipping).
  - No awkward empty cell (an empty grid slot reads as "missing primitive").
  - At mobile width, wrap to a column-stack or 2-col layout is fine.

- [ ] **Step 4:** If the layout looks bad, apply the Section 4 fallback options from the spec, in order:
  1. Tighten `minmax(120px, 1fr)` → `minmax(160px, 1fr)` in `spa_template.html:1206`.
  2. If still bad, add a `@media (min-width: 760px) { .diagram-primitives .primitives-grid { grid-template-columns: repeat(4, 1fr); } }`.
  3. Rebuild + re-screenshot until acceptance criteria are met.

- [ ] **Step 5:** Tear down server: `lsof -ti:8775 | xargs -r kill 2>/dev/null`

- [ ] **Step 6:** If any CSS change was made, commit:
  ```
  style: tighten primitives-grid layout for 8 cells
  ```

  Otherwise no commit needed.

---

## Task 19: Final verify-suite + e2e pass

- [ ] **Step 1:** Build + serve:
  ```bash
  cd /home/mihai/ai-labs/ship-it-with-ai
  python3 build/build_spa.py
  (lsof -ti:8776 | xargs -r kill 2>/dev/null; true) && python3 -m http.server -d _site 8776 > /tmp/srv.log 2>&1 &
  sleep 1
  ```

- [ ] **Step 2:** Run verify suite:
  ```bash
  cd build/tests && PORT=8776 node verify_seo_pass.js 2>&1 | tail -10
  ```
  Expected: `Verification PASSED.`

- [ ] **Step 3:** Run a P/S-specific e2e check. Suggested assertions:
  - `/chapter-1-primitives/` H3 with `id="permissions-sandbox"` exists.
  - `/chapter-1-primitives/` primitives diagram contains 8 cells named correctly in order.
  - `/chapter-1-primitives/` body contains "Permissions / Sandbox" string in at least 3 places (heading, primary list, vocabulary note).
  - `/chapter-2-anatomy-invariant/` body contains "Eight inspection points".
  - `/chapter-3-governance-in-layers/` body contains "configuration surfaces of the Permissions / Sandbox primitive".
  - `/changelog/` body contains "Permissions / Sandbox primitive" entry.
  - `/llms-full.txt` contains "Permissions / Sandbox".

- [ ] **Step 4:** Tear down server.

- [ ] **Step 5:** No commit (tests only validate).

---

## Task 20: Push to main

- [ ] **Step 1:** Confirm `git status` is clean.

- [ ] **Step 2:** Show the user the commit list (all P/S-related commits since the spec was committed) and ask for explicit permission to push:
  ```bash
  git log --oneline main --not origin/main
  ```

- [ ] **Step 3:** Wait for user authorization ("push to main"). If granted, push:
  ```bash
  git push origin main
  ```
