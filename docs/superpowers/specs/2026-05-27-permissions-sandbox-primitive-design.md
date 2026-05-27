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

## Resolved decisions (from brainstorming)

1. **Vocabulary note (Ch.1, line 365):** *Rewrite — P/S is the exception (convergence promoted it).* Keep the note; reframe it as a convergence test that P/S now passes while hooks + telemetry do not.

2. **Chapter 3 framing:** *Two-axis — keep all 5 layers; 3 of them are surfaces.* Preserve the existing five-layer defense-in-depth structure. Add a framing paragraph: *"Five layers of defense in depth. Three of them — permissions, hooks, sandbox — are the configuration surfaces of the Permissions / Sandbox primitive named in Chapter 1. Secrets and telemetry are adjacent governance controls."* Existing Artifact, Ship-this-week, and Try-it-yourself callouts continue to reference five layers.

3. **Surfaces decomposition:** in the book, the surfaces are named explicitly only in Chapter 1's primitive description (two halves: agent-level + OS-level) and in Chapter 3's framing paragraph. The book does NOT adopt the workshop's literal "four surfaces" enumeration (defaults / project settings / hooks / sandbox) because Ch.3's existing layer-by-layer treatment is already richer.

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

**Slot:** between Tools (existing Ch.1) and Skills. After "Tools" and before "Skills" in the linear narrative.

**Section heading:** `### Permissions / Sandbox {#permissions-sandbox}`

**Structure:** parallels Memory's two-halves treatment. Approximate length: 400–500 words (Memory is ~620, Tools is ~450; this primitive earns space because it carries the most governance weight).

**Two halves:**

1. **Agent-level decision layer.** What it is: Allow / Ask / Deny + the newer auto mode (classifier-driven per-action decision). Where it lives: agent configuration files + project `.claude/settings.json` (or vendor equivalent). What it does: gates every tool call before execution. Convergence note: every major coding agent (Claude Code, Codex CLI, opencode, Cursor, Gemini CLI) ships this layer — sometimes with different rule syntax, always with the same architectural role.

2. **OS-level enforcement.** What it is: kernel-enforced sandbox. Where it lives: Seatbelt (macOS), bubblewrap with Landlock + seccomp (Linux), restricted tokens with job objects (Windows). What it does: refuses syscalls the agent is not authorized to make, independent of the agent's reasoning. Convergence note: this is where vendors diverge most substantively (Codex enforces by default; Claude Code is opt-in; opencode ships soft confinement only) — the convergence is on *presence*, not on *posture*.

**Key claims to preserve:**
- "Same primitive across the major agents; substantively different implementations."
- The agent-level layer is bypassable by prompt injection; the OS-level layer is not.
- This is the primitive that PocketOS lacked (cross-reference back to the prologue).

**Forward reference:** "Chapter 3 walks the configuration surfaces of this primitive — how each major agent exposes its allow/ask/deny rules, where the OS sandbox is opted-into or opted-out-of, and where the four governance layers sit relative to this primitive's two halves."

### Section 2: The vocabulary note rewrite (Ch.1, ~line 365)

**Current text:**
> "A note on vocabulary. The primitives named here are capability primitives: what the agent uses to know, act, extend, integrate, remember, and delegate. The governance mechanisms in Chapter 3 — permissions, sandboxing, hooks, telemetry — are not additional primitives. They are control layers around the primitives, especially around tools and subagents. When evaluating an agent, inspect both: the capability anatomy and the control surface."

**Rewrite (target):**
> "A note on vocabulary. The primitives named here are what the agent uses to know, act, extend, integrate, remember, gate, and delegate. The test for primitiveness is convergence: a mechanism is a primitive when every major coding agent ships it as a distinct, configurable bundle, even when the implementations differ substantively. Permissions / Sandbox passes that test — Claude Code, Codex CLI, opencode, Cursor, and Gemini CLI all ship a decision layer + an enforcement layer, with different rule syntax and different OS sandbox postures but the same architectural role. Other governance mechanisms in Chapter 3 — security hooks, telemetry — do not yet pass the convergence test as distinct primitives; they remain control layers around the primitives. When the next mechanism converges (background memory consolidation almost crossed the line in 2026; observability event-push is the candidate to watch), the list will grow again."

**Rationale:** introduces the convergence test as the methodological rule (not just an exception). Names hooks + telemetry explicitly so readers know why they stayed in Ch.3. Preserves the "inspect both" idea by implication (the open-set framing already does this work).

### Section 3: The primitives list update

The book has several places that enumerate the primitives. All must update to include P/S as the 3rd primitive.

**Primary list (Ch.1, ~line 369):**
> Current: "Context window. Tools. Skills. Plugins. MCP. Memory. Subagents."
> New:     "Context window. Tools. Permissions / Sandbox. Skills. Plugins. MCP. Memory. Subagents."

**Inspection points (Ch.2, line 466):**

Current text counts nine inspection points: `context assembly, tool registry, skills loading, plugin extension, MCP support, memory layer, subagent dispatch, permission gate, sandbox` — 9 items, "all wrapped by the harness's agent loop."

After collapsing `permission gate` + `sandbox` into one P/S inspection point, the literal count drops to 8 named items. Three options:

1. *Re-count to "Eight inspection points"* — explicit, honest, but loses a small rhetorical anchor.
2. *Keep "Nine inspection points" by counting "the harness's agent loop" as #9* — already in the sentence ("all wrapped by"), promoted from coda to enumerable item. Reads naturally.
3. *Drop the count word ("Inspection points: …")* — sidesteps the question.

**Recommended: option 2** — keep "Nine inspection points" but rewrite to make the harness loop count: "Nine inspection points: context assembly, tool registry, the Permissions / Sandbox primitive (decision layer + OS sandbox), skills loading, plugin extension, MCP support, memory layer, subagent dispatch, and the harness's agent loop that binds them." Same number, same anchor in line 478's Artifact callout, slightly more accurate framing.

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
[ Plugins | MCP | Memory | (subagents below divider) ]
```

Decision: **4×2 grid for the 8 named primitives** (4 columns × 2 rows, 7 cells filled + 1 empty in slot 8 because subagents sit below the divider as the recursive primitive). Memory keeps its sublist (manually defined / auto-memory system). P/S gets its sublist (decision layer / OS enforcement).

*Alternative considered:* 3-column grid with 8 items → ragged last row. The current 4-wide grid carries forward visually; one empty slot is acceptable.

**Icon:** the existing icons are ◉ ⚙ ✦ ▣ ↔ ▤ ⟲. Permissions / Sandbox needs a glyph that connotes gating / boundary. Proposed: **⛨** (shield-like) or **▥** (hatched / barrier). Decision: **⛨** — semantically clearest, doesn't visually clash with existing icons.

**Caption update:** add one sentence about P/S being the second primitive whose convergence is partial across vendors (after Memory).

### Section 5: Chapter 3 — framing paragraph

Insert a new paragraph at the top of Chapter 3, immediately after the existing intro and BEFORE the "Layer one: permissions" treatment. Approximate placement: before line ~543 (the "least privilege is the spine" passage) — actually, after that passage but before the per-layer treatment begins.

**Paragraph text (target):**
> "Three of these five layers — permissions, security hooks, sandbox — are the configuration surfaces of the Permissions / Sandbox primitive named in Chapter 1. The primitive is what every major coding agent ships; the surfaces are how your team configures the primitive for your codebase, your threat model, your compliance posture. Secrets handling and telemetry are adjacent governance controls — they belong in this chapter because they catch what the primitive's surfaces miss, but they are not themselves configuration surfaces of the primitive. The five-layer treatment that follows is independent of whether you read the primitive as one bundle or five separate controls; both framings land the same configuration work."

### Section 6: Appendix C entries

Three new entries in the "Tool documentation" group, paralleling the Memory entries that shipped earlier:

1. **Claude Code permissions + sandbox documentation** — claim: Claude Code ships an allow/ask/deny permission model + opt-in sandbox; source: Anthropic Claude Code docs.
2. **Codex CLI sandbox-by-default on Linux/macOS** — claim: Codex enforces OS-level sandbox by default; source: Codex CLI repo / docs.
3. **opencode permission model + soft confinement** — claim: opencode ships a permission-prompt model + path/permission validation without kernel-level sandbox; source: opencode repo / docs.

Wire each into the existing Appendix C structure (claim / source / where-used / caveat per source, per the book's existing format).

### Section 7: Cross-book sweep targets

Locations that mention "primitives" in ways that need updating:

| Line(s) | Current state | Action |
|---|---|---|
| 165 | "The five-layer model is what I expect to hold" | Reads OK — still 5 layers; add a parenthetical "(three of them are surfaces of the Permissions / Sandbox primitive)" if it flows; otherwise leave |
| 169 | "Memory was missing from the original list…" | Add: "Permissions / Sandbox was named as a control layer in earlier drafts; the convergence test promoted it." |
| 213 | "A sandbox might have blocked the destructive call. Secrets segregation… A security hook…" | Stays. PocketOS callout — no edit needed; the Ch.1 primitive doesn't change the prologue. |
| 365 | Vocabulary note | Full rewrite (Section 2 above) |
| 369 | Primitives list | Add P/S (Section 3) |
| 396, 406, 408, 450, 452, 454 | Ch.2 side-by-side passages on sandbox | Light edit on 452 to anchor "the sandbox is a primitive" → "the OS-level half of the Permissions / Sandbox primitive is the layer where vendors diverge most" |
| 464, 466 | "Nine inspection points" enumeration | Merge "permission gate" + "sandbox" into one inspection point (Section 3) |
| 478 | Artifact callout citing "nine inspection points" | No edit if wording stays at "Nine"; otherwise sync the count |
| 543 | "The governing principle underneath all five layers is least privilege" | No edit — the framing paragraph (Section 5) is inserted before this |
| 685 | Ship-this-week "five governance layers" | No edit |
| 1004 | Ch.6 intro "AGENTS.md is the manually defined layer of the Memory primitive…" | No edit (the AGENTS.md/CLAUDE.md is the memory surface, not a P/S surface) |
| Cases-used-in-this-book front matter | Check whether any case is now relevant to P/S | Likely no edit; PocketOS is already in the cases list |

A grep for `primitive|primitives|permission gate|sandbox` will find any I missed; the sweep is mechanical after the spec is approved.

### Section 8: Changelog entry

Add a new dated entry at the top of `## Changelog`:

> ### 2026-05-27 — Permissions / Sandbox primitive
>
> Permissions / Sandbox promoted to a named primitive — the third slot in the inventory, after Context window and Tools. Two halves like Memory: the agent-level decision layer (Allow / Ask / Deny + auto mode) and OS-level enforcement (Seatbelt / bubblewrap / restricted tokens). The vocabulary note in Chapter 1 was rewritten to name the convergence test that promoted this primitive while leaving hooks + telemetry as control layers. Chapter 3 gains a framing paragraph binding three of its five layers (permissions, hooks, sandbox) to the new primitive's configuration surfaces; the five-layer defense-in-depth narrative is preserved unchanged. Diagram updated to 8 cells. Three new Appendix C entries source the Claude Code / Codex / opencode implementations.

### Section 9: Build + verify

- The build pipeline (`build/build_spa.py`) needs:
  - `diagram_primitives()` rewritten for 8-cell layout
  - SECTION_SLUGS already covers all sections — no new entry needed (P/S is a sub-section of Ch.1, not its own page)
  - `verify_seo_pass.js` assertion that "Permissions / Sandbox" appears in chapter-1 body, in the primitives diagram (h3 anchor present), in the inspection-points enumeration in chapter-2, and in chapter-3's framing paragraph
  - A forbidden-list sweep assertion that the literal phrase "are not additional primitives" no longer appears in the book (was the old vocabulary note's load-bearing line; if it survives, the rewrite didn't land)

- The verify script's existing "changelog excluded from forbidden-list sweep" handling already covers the new changelog entry that quotes the old vocabulary.

## Open questions

1. **Diagram icon for P/S.** Proposed `⛨` (shield). Alternatives: `▥`, `▦`, `⊟`, or no icon.
2. **Verb in the vocabulary note** at line 365 (`know, act, ___, extend, integrate, remember, delegate`): "gate" is the proposal. Alternatives: "guard", "enforce", "constrain".
3. **"Nine inspection points" preservation** — Section 3 recommends keeping the count by promoting the harness loop to the 9th item; alternative is to drop to "Eight" honestly.
4. **Source-note callout in Ch.1.** Memory's sources live only in Appendix C; P/S could match or get its own in-chapter callout. Default: match Memory (Appendix C only).

## File inventory

Touched files (in dependency order):

1. `source/Ship_It_With_AI.md` — content edits (new section, vocabulary rewrite, sweep, Appendix C entries, changelog entry)
2. `build/build_spa.py` — diagram update only (no other build changes needed; the new section parses as a normal H3 inside Ch.1's existing page)
3. `build/tests/verify_seo_pass.js` — new assertions
4. `docs/superpowers/plans/2026-05-27-permissions-sandbox-primitive.md` — to be written next

No template, CSS, or routing changes. No new pages, no new slugs, no redirect stubs.

## Estimated cascade scope

- 1 new section in Ch.1 (~450 words)
- 1 paragraph rewrite (vocabulary note)
- ~5–10 surgical edits across Ch.1, Ch.2, Ch.3 for primitives-list mentions
- 1 framing paragraph in Ch.3
- 3 Appendix C entries
- 1 changelog entry
- 1 diagram function rewrite in `build_spa.py`
- 4–6 new assertions in `verify_seo_pass.js`

Approximate effort: same scale as Memory cascade. ~2 hours subagent-driven execution + review.
