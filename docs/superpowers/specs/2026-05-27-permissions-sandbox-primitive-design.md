# Permissions / Sandbox primitive — Design

**Date:** 2026-05-27
**Author:** Mihai (via Claude Code)
**Status:** Design approved, ready for writing-plans
**Predecessor:** `docs/superpowers/specs/2026-05-27-memory-primitive-and-open-set-design.md` (same cascade pattern)

---

## Goal

Promote **Permissions / Sandbox** to a named primitive in the book, paralleling the Memory promotion that shipped earlier in the day. Slot it as the 3rd primitive (after Context window and Tools, before Skills). Reconcile the existing vocabulary note that explicitly excluded permissions/sandbox from the primitives list. Bind Chapter 3's governance layers to the new primitive without losing the existing five-layer defense-in-depth narrative.

This adapts the workshop-side spec `2026-05-27-theme1-permissions-sandbox-primitive-design.md` (`/mnt/c/Users/xbox1/OneDrive/AI Labs/ClaudeWorkshop/Clients/ITSS/`) into the book. The book's structure is different from the workshop deck, so the adaptation is not a literal port.

## Why now

The workshop's D-1 cascade (workshop is 2026-05-28) decided this primitive promotion. The book has been the lagging surface and needs to align before the workshop ships. The existing book content in Ch.2 (the Codex vs opencode side-by-side sandbox finding) already does the empirical work; this pass surfaces the conceptual upgrade.

## Resolved decisions (from brainstorming + review)

1. **Vocabulary note (Ch.1, line 365):** *Rewrite — P/S is the exception (convergence promoted it).* Keep the note; reframe as a convergence test that P/S now passes. **Hooks come off the "control layers around primitives" list** (the Ch.3 framing paragraph reclassifies hooks as a surface of the P/S primitive — they can't be both). Only telemetry remains as the named example of a control layer that has not yet crossed the convergence line.

2. **Chapter 3 framing:** *Two-axis — keep all 5 layers; 3 of them are surfaces.* Preserve the existing five-layer defense-in-depth structure. Add a framing paragraph binding 3 of the 5 layers (permissions, hooks, sandbox) to the new primitive's surfaces.

3. **Surfaces decomposition:** in the book, the surfaces are named explicitly only in Chapter 1's primitive description (two halves: agent-level + OS-level) and in Chapter 3's framing paragraph. The book does NOT adopt the workshop's literal "four surfaces" enumeration (defaults / project settings / hooks / sandbox) because Ch.3's existing layer-by-layer treatment is already richer.

4. **Convergence claim honesty (resolved in review):** the OS-enforcement half is **presence-converged but posture-divergent** across the major agents — opencode in particular ships the decision half only (soft confinement, no kernel sandbox). The Ch.1 section and the vocabulary-note rewrite must name this asymmetry the same way the Memory section named "the second half is an early-mover signal, not yet a convergence." Don't smooth it over.

5. **Inspection points count (resolved in review, user decided):** re-count Ch.2 line 466 to "**Eight** inspection points" (down from Nine). The harness's agent loop stays as the binder, not as an enumerable item — preserves line 357's existing harness-as-organizer vs primitives-as-components framing. The Memory cascade also bumped a count honestly (six → seven); same discipline applies in the other direction here.

6. **Pedagogical anchor (resolved in review):** carry the workshop's Memory↔P/S parallel into the book: *"Same shape as Memory: one primitive, multiple configuration surfaces. Memory has one (AGENTS.md / CLAUDE.md); Permissions / Sandbox has more."* Lives in the Ch.3 framing paragraph.

7. **Two-halves framing strengthening (resolved in review):** the two halves of P/S are *not* the same control written two ways (which is Memory's structure). They are two different controls with different failure modes that the convergent agents always ship together. The convergent-pairing IS the primitive. Acknowledge this openly in Ch.1 — don't force Memory-style symmetry.

## Non-goals

- Not restructuring Chapter 3's five-layer narrative. The book's strongest section stays.
- Not removing the "Adjacent practices" section in Ch.3.
- Not changing the URL of any existing page. (`/chapter-1-primitives/` and `/chapter-3-governance-in-layers/` keep their slugs.)
- Not retitling Chapter 3 ("Governance in layers" survives — the "layers" word is now load-bearing for the existing defense-in-depth framing).
- Not adding workshop-specific surfaces ("Slide 7 four surfaces", etc.) — that's workshop-side material.
- Not touching the workshop repo (separate update path, owned by Mihai).

## Constraints

- The Memory primitive cascade is the precedent. Match its pattern: named primitive section in Ch.1, diagram update, sweep, Appendix C entries, changelog entry.
- The two-halves framing must parallel Memory's existing two halves (manually defined / auto-memory system).
- "Permissions / Sandbox" with spaces around the `/` is the canonical written form (per workshop convention).
- No Claude attribution in commits or PR descriptions (per user's global preference).

---

## Design

### Section 1: Chapter 1 — new primitive section

**Slot:** between Tools (existing Ch.1) and Skills.

**Section heading:** `### Permissions / Sandbox {#permissions-sandbox}`

**Structure:** parallels Memory's two-halves treatment but acknowledges the structural difference (Memory's halves share a substrate; P/S's halves are two different controls always shipped together). Length: ~450 words (Memory is ~620, Tools is ~450).

#### In-voice prose sketch (user revises voice; matches the Memory spec's precedent)

> Permissions / Sandbox is the primitive that PocketOS lacked. It has two halves, and they are not the same control written two ways — they are two different controls that the convergent agents always ship together, because each one catches what the other misses.
>
> **The agent-level decision layer** is what the agent itself consults before every tool call. Allow / Ask / Deny rules, plus the newer auto-mode classifier that handles routine decisions silently and surfaces the rest. Every major coding agent ships this: Claude Code, Codex CLI, opencode, Cursor, Gemini CLI. The rule syntax differs by vendor; the architectural role does not. This is the layer most teams reach for first; this is also the layer prompt injection can defeat, because prompt injection works by manipulating the agent's reasoning, and the agent's reasoning is what consults the rules.
>
> **The OS-level enforcement** is what runs underneath. The kernel itself refuses syscalls the agent was not authorized to make: Seatbelt on macOS, bubblewrap with Landlock and seccomp on Linux, restricted tokens or WSL2-backed isolation on Windows. The agent cannot reason its way past this layer because the kernel is not listening to the agent's reasoning — it is listening to system calls. Either the syscall is permitted or it is not.
>
> Convergence on this half is real but uneven. Codex CLI enforces OS-level sandbox by default on Linux and macOS. Cursor added kernel-backed sandbox controls in its 2.x line. Gemini CLI ships sandbox profiles. Claude Code is opt-in — the sandbox is available, but most installations skip it. opencode is the partial exception: it ships only the decision half, leaving OS isolation to the operator's own Docker or microVM setup. The convergence is on *presence of both halves as a configurable bundle*, not on *posture* — exactly the asymmetry the Memory primitive has on its second half. Treat that as the honest reading.
>
> Said plainly: the agent-level layer is bypassable by prompt injection. The OS-level layer is not. The two ship together because neither is sufficient alone. **The convergent-pairing is the primitive.**
>
> Chapter 3 walks the configuration surfaces of this primitive — how each major agent exposes its allow/ask/deny rules, where the OS sandbox is opted-into or opted-out-of, and how the chapter's five governance layers map onto the primitive's two halves.

#### Voice anchors for the implementer

- Short declarative sentences in series (compare Ch.1 lines 277-279, 339-341).
- "Said plainly:" reset move (compare line 361).
- Operational concretion where possible — name specific syscall postures, name agents by name, name where the bypass happens.
- No "let me explain what a sandbox is" framing — readers know.
- Bold only the two key terms ("agent-level decision layer", "OS-level enforcement"). Italics for emphasis sparingly.

#### Explicit forward-reference edits (cross-references this section creates)

- **Prologue cross-ref.** PocketOS is named in this section's first sentence. The Prologue ("Nine seconds") needs no edit — the existing line 213 already enumerates "a sandbox might have blocked / secrets segregation / a security hook" which the new primitive name now binds. But Ch.3's PocketOS callout in line 533 should add one phrase: "Permissions / Sandbox would have caught it twice — once at the decision layer if the rule had been there, once at the OS layer regardless."
- **Ch.2 cross-ref.** Line 452 ("the sandbox is a primitive") should be lightly rewritten to "the OS-level half of the Permissions / Sandbox primitive named in Chapter 1 is the layer where vendors diverge most." Captured in Section 7 sweep.

### Section 2: The vocabulary note rewrite (Ch.1, ~line 365)

**Current text:**
> "A note on vocabulary. The primitives named here are capability primitives: what the agent uses to know, act, extend, integrate, remember, and delegate. The governance mechanisms in Chapter 3 — permissions, sandboxing, hooks, telemetry — are not additional primitives. They are control layers around the primitives, especially around tools and subagents. When evaluating an agent, inspect both: the capability anatomy and the control surface."

**Rewrite (target):**
> "A note on vocabulary. The primitives named here are what the agent uses to know, act, gate, extend, integrate, remember, and delegate. The test for primitiveness is convergence: a mechanism is a primitive when every major coding agent ships it as a distinct, configurable bundle, even when the implementations differ substantively. Permissions / Sandbox passes that test on the decision-layer half across all the major agents; the OS-enforcement half is presence-converged but posture-divergent — Codex CLI defaults it on, Cursor and Gemini CLI ship it as a first-class option, Claude Code is opt-in, opencode leaves OS isolation to the operator. Same architectural role; different vendor postures. The Memory primitive has the same shape on its second half (auto-memory consolidation is an early-mover signal across Claude Code, with the others converging). Telemetry has not yet crossed the convergence line and remains a control layer around the primitives. When the next mechanism converges — observability event-push is the candidate to watch — the list will grow again."

**Rationale:** introduces the convergence test as the methodological rule, then names the posture asymmetry honestly (matches Ch.2's existing finding that Codex enforces real kernel sandbox and opencode ships soft confinement only). **Hooks are deliberately not named here as a "control layer"** — the Ch.3 framing paragraph reclassifies hooks as a configuration surface of P/S, and the vocabulary note must not contradict it. Telemetry is the surviving named example of a control layer that has not yet crossed.

### Section 3: The primitives list update

The book has several places that enumerate the primitives. All must update to include P/S as the 3rd primitive.

**Primary list (Ch.1, ~line 369):**
> Current: "Context window. Tools. Skills. Plugins. MCP. Memory. Subagents."
> New:     "Context window. Tools. Permissions / Sandbox. Skills. Plugins. MCP. Memory. Subagents."

**Inspection points (Ch.2, line 466) — DECIDED: Eight:**

Current text counts nine inspection points: `context assembly, tool registry, skills loading, plugin extension, MCP support, memory layer, subagent dispatch, permission gate, sandbox` — 9 items, "all wrapped by the harness's agent loop."

After collapsing `permission gate` + `sandbox` into one P/S inspection point, the literal count drops to 8 named items.

**Decision: re-count to "Eight inspection points"** — explicit, honest. Keeps line 357's existing framing intact (the harness *organizes* the primitives; promoting it to an enumerable would muddle the architecture/components distinction). The Memory cascade also bumped a count honestly in the other direction (six → seven) — same discipline.

**New text:**
> "Eight inspection points: context assembly, tool registry, the Permissions / Sandbox primitive (decision layer + OS sandbox as two halves), skills loading, plugin extension, MCP support, memory layer, subagent dispatch — all wrapped by the harness's agent loop."

**Cascade:**
- Line 478 Artifact callout currently says "**The nine inspection points from this chapter.**" Update to "**The eight inspection points from this chapter.**"
- `build/tests/verify_seo_pass.js` has a forbidden phrase `'Eight inspection points'` (originally added to prevent miscounting). With this decision, **flip from forbidden to positive marker**: `'Eight inspection points'` must now appear in `/chapter-2-anatomy-invariant/`.

**Ch.1 evaluation-rubric questions (Ch.1, lines 371-373):**

L371 enumerates 8 questions ("How big is the context window… How does the agent expose subagents…"). L373 closes with "Eight questions today; more tomorrow." With P/S becoming a primitive, the rubric needs a 9th question.

**New question to insert** (placement: between MCP and memory in the L371 list to match primitive order): "What permission model does it ship — allow/ask/deny rules, auto-mode classifier — and what OS sandbox does it default to?"

**Closing line update:** "Eight questions today" → "Nine questions today."

**Ship-this-week (line 385):** the rapid-fire prompt similarly lists 7 questions ("how large is your context window… how do I dispatch a subagent?"). Add one P/S question: "what allow/ask/deny model and what sandbox does this agent ship with?"

**Other enumerations to sweep:**
- Line 365's "know, act, extend, integrate, remember, and delegate" → "know, act, gate, extend, integrate, remember, and delegate" (add "gate" as the verb for P/S).
- Line 396: the side-by-side prompt that asks Claude Code to "map the agent loop, the tool system, the permission gates, the sandbox primitive, and the plugin model" already references both halves — leave as-is, but the chapter introduction can now point at this as having been an early instance of the convergence (footnote-style).
- Line 478 ("nine inspection points") — see above.
- Line 498: "The primitives are the same in both. The implementation choices are different." — stays.
- Line 169 in the scope-and-limits passage: "If a future agent ships without a mechanism that maps to one of the primitives, I missed an invariant…" — stays (already open-set).

### Section 4: Diagram update

The `diagram_primitives()` function in `build/build_spa.py:314-340` currently emits a 7-cell grid (6 primitives + Memory in slot 6) + divider + subagents row (recursive).

**New layout:** insert Permissions / Sandbox in slot 3 (after Tools, before Skills). The grid grows from 7 named primitives to 8.

```
[ CW | Tools | P/S | Skills ]
[ Plugins | MCP | Memory | (empty — subagents is below divider) ]
```

Decision: **8 named primitives in the responsive auto-fit grid** (existing CSS: `repeat(auto-fit, minmax(120px, 1fr))` at `spa_template.html:1206`). Memory keeps its sublist (manually defined / auto-memory system); P/S gets its sublist (decision layer / OS enforcement). Subagents stays below the divider as the recursive primitive.

**Visual verification required during execution:** capture screenshots at desktop/tablet/mobile after the 8-cell grid lands. The auto-fit math depends on the rendered article column width — at typical desktop widths (~720-820px) with `minmax(120px, 1fr)`, 8 items may wrap as 6+2 (one half-empty row reading as "missing primitive" — voice reviewer's concern) rather than as a clean 4×2. If the wrap is awkward, three fallback options:

1. **Tighten the min-width to force 4-col at desktop:** `minmax(160px, 1fr)` → 8 items render as exactly 4×2 at most desktop widths.
2. **Promote subagents into the main grid as cell 8** + relabel the divider/note to reserve the recursive distinction without geometry. Loses some visual signal.
3. **Hard-code grid-template-columns: repeat(4, 1fr)** at a media-query breakpoint. Most rigid but most predictable.

Recommended fallback order: try option 1 first (smallest CSS change, preserves responsiveness), fall back to option 3 if option 1 still wraps awkwardly. Do not adopt option 2 unless the screenshots show both 1 and 3 failing.

**Icon:** the existing icons are ◉ ⚙ ✦ ▣ ↔ ▤ ⟲. Permissions / Sandbox needs a glyph that connotes gating / boundary. Proposed: **⛨** (shield-like) or **▥** (hatched / barrier). Decision: **⛨** — semantically clearest, doesn't visually clash with existing icons.

**Caption update:** add one sentence about P/S being the second primitive whose convergence is partial across vendors (after Memory).

### Section 5: Chapter 3 — framing paragraph

Insert a new paragraph at the top of Chapter 3, immediately after the existing intro and BEFORE the "Layer one: permissions" treatment. Approximate placement: before line ~543 (the "least privilege is the spine" passage) — actually, after that passage but before the per-layer treatment begins.

**Paragraph text (target):**
> "Three of these five layers — permissions, security hooks, sandbox — are the configuration surfaces of the Permissions / Sandbox primitive named in Chapter 1. The primitive is what every major coding agent ships; the surfaces are how your team configures it for your codebase, your threat model, your compliance posture. Same shape as Memory in Chapter 1: one primitive, multiple configuration surfaces. Memory has one (AGENTS.md / CLAUDE.md); Permissions / Sandbox has more. Secrets handling and telemetry are adjacent governance controls — they belong in this chapter because they catch what the primitive's surfaces miss, but they are not themselves configuration surfaces of the primitive. The five-layer treatment that follows is independent of whether you read the primitive as one bundle or five separate controls; both framings land the same configuration work."

### Section 6: Appendix C entries

Three new entries in the "Tool documentation" group, paralleling the Memory entries that shipped earlier:

1. **Claude Code permissions + sandbox documentation** — claim: Claude Code ships an allow/ask/deny permission model + opt-in sandbox; source: Anthropic Claude Code docs.
2. **Codex CLI sandbox-by-default on Linux/macOS** — claim: Codex enforces OS-level sandbox by default; source: Codex CLI repo / docs.
3. **opencode permission model + soft confinement** — claim: opencode ships a permission-prompt model + path/permission validation without kernel-level sandbox; source: opencode repo / docs.

Wire each into the existing Appendix C structure (claim / source / where-used / caveat per source, per the book's existing format).

### Section 7: Cross-book sweep targets

Reviewer-augmented after structural-sweep review found 7 misses in the original table.

| Line(s) | Current state | Action |
|---|---|---|
| 165 | "The five-layer model is what I expect to hold" | Reads OK; no edit |
| 169 | "Memory was missing from the original list…" | Add: "Permissions / Sandbox was named as a control layer in earlier drafts; the convergence test promoted it." |
| 213 | Prologue PocketOS callout | No edit — Prologue stays |
| **240-258** | **MISS — source-side ASCII diagram** | Add a `permissions / sandbox (decision layer \| OS enforcement)` row to the ASCII grid. Renders verbatim in `/read/` + `llms-full.txt`. |
| **261** | **MISS — source-side figure caption** | Same one-sentence P/S addition as the HTML caption (Section 4) |
| **343** | **MISS — Ch.1 subagents recursive definition** | "A subagent is another instance of the primitives - it has its own context window, its own tools, its own skills, plugins, MCP, memory" → add "permissions / sandbox" in order |
| 365 | Vocabulary note | Full rewrite (Section 2 above) |
| 369 | Primitives list ("Context window. Tools. Skills. Plugins. MCP. Memory. Subagents.") | Insert P/S in position 3: "Context window. Tools. Permissions / Sandbox. Skills. Plugins. MCP. Memory. Subagents." |
| **371-373** | **MISS — "Eight questions today" rubric** | Add a P/S question (between MCP and memory in the list); change "Eight questions today" → "Nine questions today". Captured in Section 3. |
| **385** | **MISS — Ch.1 Ship-this-week rapid-fire prompt** | Add a P/S question to the prompt. Captured in Section 3. |
| 396, 406, 408, 450, 454 | Ch.2 side-by-side passages on sandbox | Light edit only on 452 |
| 452 | "the sandbox is a primitive" | Rewrite to "the OS-level half of the Permissions / Sandbox primitive named in Chapter 1 is the layer where vendors diverge most" |
| **464-466** | "Nine inspection points" enumeration | Decided: re-count to **Eight**, collapse permission gate + sandbox into one P/S inspection point (Section 3 has new text) |
| **478** | Artifact callout "The nine inspection points from this chapter." | Update to "The eight inspection points from this chapter." |
| **496** | **MISS — Ch.2 Try-it-yourself prompt** ("Walk this codebase and name the primitives - context window, tools, skills, plugins, MCP, memory, subagents.") | Insert P/S in order |
| 533 | Ch.3 PocketOS callout | Add: "Permissions / Sandbox would have caught it twice — once at the decision layer if the rule had been there, once at the OS layer regardless." (Captured in Section 1's forward-reference subsection) |
| 543 | "The governing principle underneath all five layers is least privilege" | No edit — framing paragraph (Section 5) is inserted before this |
| 685 | Ship-this-week "five governance layers" | No edit |
| 1004 | Ch.6 intro Memory primitive ref | No edit |
| **1902** | **MISS — Closing Part I summary** ("The primitives - context window, tools, skills, plugins, MCP, memory, subagents - plus the harness that organizes them.") | Insert P/S in order |
| Cases front matter | Check whether PocketOS framing changes | No edit; PocketOS already listed |

The grep `primitive|primitives|permission gate|sandbox` reaches all of these; the implementer should rerun the grep after applying the table to confirm no further misses.

### Section 8: Changelog entry

Add a new dated entry at the top of `## Changelog`:

> ### 2026-05-27 — Permissions / Sandbox primitive
>
> Permissions / Sandbox promoted to a named primitive — the third slot in the inventory, after Context window and Tools. Two halves like Memory: the agent-level decision layer (Allow / Ask / Deny + auto mode) and OS-level enforcement (Seatbelt / bubblewrap / restricted tokens). The vocabulary note in Chapter 1 was rewritten to name the convergence test that promoted this primitive while leaving hooks + telemetry as control layers. Chapter 3 gains a framing paragraph binding three of its five layers (permissions, hooks, sandbox) to the new primitive's configuration surfaces; the five-layer defense-in-depth narrative is preserved unchanged. Diagram updated to 8 cells. Three new Appendix C entries source the Claude Code / Codex / opencode implementations.

### Section 9: Build + verify

**Build pipeline (`build/build_spa.py`):**
- `diagram_primitives()` rewritten for 8-cell layout (Section 4).
- No new `SECTION_SLUGS` entry needed (P/S is an H3 under Ch.1, not its own page).
- No CSS change anticipated; verify by screenshots during execution and apply fallback only if needed (Section 4).
- `H3_ANCHOR_RE` already auto-indexes the new section for search/sidebar — no build wiring needed.

**Verify suite (`build/tests/verify_seo_pass.js`) — explicit updates:**

*Positive markers that must update verbatim (existing assertions will break):*
- L582 marker `'Eight questions today'` → must become `'Nine questions today'` (count bumped to 9, per Section 3).
- L590 marker `'Context window. Tools. Skills. Plugins. MCP. Memory. Subagents.'` → must become `'Context window. Tools. Permissions / Sandbox. Skills. Plugins. MCP. Memory. Subagents.'` (canonical primitive list, per Section 3).
- L566 forbidden phrase `'Eight inspection points'` → **flip to positive marker** (Eight is now the correct count per Section 3).
- L606-610 Memory sublist count assertion (`sublistCount < 1` currently): tighten to `< 2` to lock the invariant that BOTH Memory and P/S cells carry sublists.

*New forbidden phrases (added to the sweep):*
- `'are not additional primitives'` — the load-bearing line of the old vocabulary note. Must not survive the rewrite. The `/changelog/` page is excluded from this sweep (the prior vocabulary may be quoted there historically).

*New positive markers (asserted in the rendered pages):*
- `'Permissions / Sandbox'` appears in `/chapter-1-primitives/`, `/chapter-2-anatomy-invariant/`, `/chapter-3-governance-in-layers/`.
- H3 anchor `id="permissions-sandbox"` present in `/chapter-1-primitives/`.
- Ch.3 framing paragraph phrase `'configuration surfaces of the Permissions / Sandbox primitive'` appears in `/chapter-3-governance-in-layers/`.
- Three new Appendix C entries — at minimum, one positive marker per entry (parallel to lines 647-657 Memory entries).

**Diagram visual verification (manual, during execution):**
- Capture `/chapter-1-primitives/` at desktop / tablet / mobile after the 8-cell rewrite.
- Confirm no orphan empty cell, no awkward wrap.
- Apply Section 4 fallback if visually broken.

## Open questions

All four open questions resolved during the review round (reviewer consensus + user decision on inspection-points split):

1. **Diagram icon `⛨`** — accepted (4/4 reviewer approval; no clash with existing icons).
2. **Verb "gate"** — accepted (already used at lines 396, 464; workshop-consistent).
3. **"Eight" inspection points** — accepted on voice-reviewer argument (line 357 separates harness-as-organizer from primitives-as-components; user confirmed).
4. **Source-note callout in Ch.1** — match Memory (Appendix C only).

## File inventory

Touched files (in dependency order):

1. `source/Ship_It_With_AI.md` — content edits (new section, vocabulary rewrite, sweep, Appendix C entries, changelog entry)
2. `build/build_spa.py` — diagram update only (no other build changes needed; the new section parses as a normal H3 inside Ch.1's existing page)
3. `build/tests/verify_seo_pass.js` — new assertions
4. `docs/superpowers/plans/2026-05-27-permissions-sandbox-primitive.md` — to be written next

No template, CSS, or routing changes. No new pages, no new slugs, no redirect stubs.

## Estimated cascade scope (reviewer-adjusted)

- 1 new section in Ch.1 (~450 words) — implementer revises voice from the in-voice prose sketch in Section 1
- 1 paragraph rewrite (vocabulary note)
- 1 PocketOS callout edit in Ch.3 (~line 533)
- **~13 surgical edits** across Ch.1, Ch.2, Ch.3, and the Closing for primitives-list mentions + count bumps (Section 7 table)
- 1 source-side ASCII diagram update (lines 240-258) + source-side caption update (line 261)
- 1 framing paragraph in Ch.3
- 3 Appendix C entries
- 1 changelog entry
- 1 diagram function rewrite in `build_spa.py` + possible CSS fallback
- **~7 verify-suite updates** (4 existing assertions to flip/update + 3 new positive markers + 1 new forbidden phrase)

Approximate effort: ~1.5× the Memory cascade because of the count-flip cascades (Eight inspection points, Nine questions) and the more aggressive sweep. ~2.5-3 hours subagent-driven execution + review.
