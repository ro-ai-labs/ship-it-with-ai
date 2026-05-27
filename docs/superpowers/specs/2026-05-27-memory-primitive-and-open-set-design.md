# Memory primitive + open-set reframing — Design Spec

A retroactive update to the manual to (a) add **Memory** as a named primitive, (b) drop the closed "six" count for an open-set framing, and (c) reframe Chapter 1's structural argument from "five local + one recursive" to "named primitives + the recursive primitive". Driven by the parallel workshop spec dated 2026-05-27 that promoted Memory across the workshop chain; the book was explicitly out of scope of that spec and is the target of this one.

The conceptual cut the book contributes (beyond the workshop's four-layer enumeration): Memory has **two categorical halves** — manually defined memory (agent-agnostic, mature, converged across the major coding agents) and the auto-memory system (Claude-Code-specific today, emerging across other agents). This cleaner cut maps onto the book's existing agent-agnostic primitive-status test.

## Scope

In scope (this pass):

- **Chapter 1 restructure.** Rename `Six primitives` → `The primitives`. Rewrite the load-bearing "five local + one recursive" argument. Add a Memory section between MCP and Subagents structured around the two categorical halves. Update the diagram. Rename slug `/chapter-1-six-primitives/` → `/chapter-1-primitives/` with a JS redirect stub at the old URL.
- **Book-wide cross-reference sweep.** Every count-anchored phrasing (~25 lines across Foreword, Chapter 1, Chapter 2, Chapter 5, Closing, Appendix C, TOC) gets rewritten so the book is internally consistent after a single commit.
- **Chapter 6 framing intro.** One opening paragraph that anchors AGENTS.md as the manually defined memory layer of the new Memory primitive. Rest of chapter unchanged. Slug unchanged. The "Six things go in AGENTS.md" structure stays (it's about AGENTS.md content, orthogonal to primitive count).
- **Appendix C new entries** for the load-bearing Memory claims (cross-vendor AGENTS.md support; Claude Code Auto Memory; Auto Dream announcement 2026-05-06).
- **Verification** — extend `build/tests/verify_seo_pass.js` with assertions for the new slug, the redirect stub, the renamed TOC entry, the diagram update, and the "no `six primitives` anywhere in body" sweep.

Out of scope (separate concerns):

- Reframing Chapter 6 around all four memory layers. Three of the four (Auto Memory, Session Memory, Auto Dream) aren't team infrastructure; the chapter title would apply to 25% of content. AGENTS.md remains the chapter's subject; Memory primitive context comes from Chapter 1.
- A dedicated "Boundary primitives" section (hooks / LSPs / observability). The book's existing agent-agnostic primitive-status test correctly classifies hooks as control layers (Chapter 3) and LSPs as implementation details. Open-set framing is communicated by one acknowledgment line, not a section. Line 349's current claim ("hooks, telemetry are not additional primitives, they are control layers") stays.
- Session Memory as a separate layer. It collapses to "session memory = context window" — one-sentence mention in Chapter 1's Memory section.
- The "six-phase loop" naming in Chapter 5. Different "six" (methodology, intentionally counted). Lines 187, 794, 938 — leave alone.

## Sequencing — one PR, two atomic commits

**Commit 1 — Chapter 1 restructure + book-wide sweep + slug + diagram + verify.**
Touches: `source/Ship_It_With_AI.md` (TOC + Foreword + Chapter 1 + Chapter 2 + Chapter 5 + Closing + Appendix C labels), `build/build_spa.py` (`SECTION_SLUGS`, `diagram_primitives`, JS redirect stub, hash-redirect map), `build/tests/verify_seo_pass.js` (new + updated assertions). After this commit, the book is internally consistent: every "primitives" reference is open-set; Memory is named everywhere; the Chapter 1 H1 is `The primitives`; the old `/chapter-1-six-primitives/` URL redirects to `/chapter-1-primitives/`. Chapter 6 still doesn't mention the Memory primitive frame — fixed in Commit 2.

**Commit 2 — Chapter 6 framing intro + Appendix C new entries + final verify.**
Touches: `source/Ship_It_With_AI.md` (Chapter 6 one-paragraph intro + Appendix C new entries), `build/tests/verify_seo_pass.js` (final assertions for Appendix C entries). After this commit, Chapter 6 connects to the Memory primitive named in Chapter 1, the new claims are sourced per the book's discipline.

Each commit is independently deployable. The two-commit structure exists for review granularity, not because Commit 1 leaves the book in a broken state.

## Architecture

The Memory primitive in the book is structured around two categorical halves, mapped to the existing agent-agnostic primitive-status test:

| Half | Status | What it is | Where it goes |
|---|---|---|---|
| **Manually defined memory** | Agent-agnostic; converged across Codex, Cursor, Copilot, Gemini, Aider, Claude Code | AGENTS.md / CLAUDE.md — always-loaded, team-shareable, user/team-authored | Chapter 1 Memory section names it; Chapter 6 covers it in depth |
| **Auto-memory system** | Claude-Code-specific today; emerging in other agents | Auto Memory (Claude-written learned patterns); Auto Dream (background consolidation, announced 2026-05-06) | Chapter 1 Memory section covers it with explicit "currently Claude-Code-specific" framing |

Session Memory from the workshop's four-layer model collapses to "session memory = context window" — a single sentence in the Memory section, not its own layer.

The structural argument in Chapter 1 rewrites from:

> Five of them are the agent's local capabilities. The sixth is the composition mechanism that makes the agent recursive.

to:

> Most are local capabilities of the agent. One — subagents — is the composition mechanism that makes the agent recursive: it can spawn constrained instances of itself.

The local/recursive distinction stays; the count goes. The "named primitives are an open set" framing is acknowledged in the chapter open and in the diagram caption, without naming specific boundary candidates (which the existing line 349 already characterizes as control layers).

## Content designs

### Commit 1 — Chapter 1 + cross-references

#### Chapter 1 H1, slug, TOC entry

- Heading: `## Chapter 1` + `## The primitives` (currently `## Six primitives`).
- TOC entry on line 26: `1. Six primitives` → `1. The primitives`.
- Slug in `SECTION_SLUGS`: `("chapter", "Six primitives")` → `("chapter", "The primitives")` (key change), value `"chapter-1-six-primitives"` → `"chapter-1-primitives"`.
- Legacy slug alias in `build_anchor_index` (`chapter-1` → `chapter-1-primitives`) updated.

#### Chapter 1 opening rewrite — lines 228-238

Current (lines 228-238):

> ## Six primitives
>
> Open the source code or documentation of most production-grade coding agents - Codex CLI in Rust, opencode in TypeScript, the public-source parts of Claude Code, the agents shipped by half a dozen smaller vendors - and you see the same architecture emerging: six primitives wrapped by a harness. The implementations differ. The anatomy converges. Different names sometimes, different file layouts always, but the same six conceptual building blocks. Five of them are the agent's local capabilities. The sixth is the composition mechanism that makes the agent recursive: it can spawn constrained instances of itself.
>
> ...
>
> That is the anatomy. Every interesting question about a coding agent - what it can do, what it cannot do, how to control it, what to compare it to - reduces to one or more of these six primitives. When a new agent arrives, your first question is: how does this one handle the six primitives? When you are deciding whether to let an agent touch a particular codebase, your second question is: which of the six primitives is the relevant control point for this risk? When you are buying tooling, your third question is: which of the six primitives does this tooling improve, and at what cost?
>
> ...
>
> Six primitives.

Proposed rewrite (user revises during diff review):

> ## The primitives
>
> Open the source code or documentation of most production-grade coding agents - Codex CLI in Rust, opencode in TypeScript, the public-source parts of Claude Code, the agents shipped by half a dozen smaller vendors - and you see the same architecture emerging: a small set of primitives wrapped by a harness. The implementations differ. The anatomy converges. Different names sometimes, different file layouts always, but the same conceptual building blocks. Most are local capabilities of the agent. One - subagents - is the composition mechanism that makes the agent recursive: it can spawn constrained instances of itself.
>
> ...
>
> That is the anatomy. Every interesting question about a coding agent - what it can do, what it cannot do, how to control it, what to compare it to - reduces to one or more of these primitives. When a new agent arrives, your first question is: how does this one handle each primitive? When you are deciding whether to let an agent touch a particular codebase, your second question is: which primitive is the relevant control point for this risk? When you are buying tooling, your third question is: which primitive does this tooling improve, and at what cost?
>
> ...
>
> Context window. Tools. Skills. Plugins. MCP. Memory. Subagents. Plus the harness as the runtime that organizes them. That is the list today. The set is open; expect it to grow. Memory was missing eighteen months ago and converged across the major agents within a six-month window. The next one will appear when the convergence appears, not before.

Notes on the rewrite:

- The open-set acknowledgment is positioned AFTER the named list (per reader-experience review: a learner can't evaluate "the set is open" before they know what the set IS).
- The closing list is opened by the list itself, not by a category label. "Named primitives." was rejected by three reviewers as a rhetorical regression vs. "Six primitives.".
- The expand-clause ("Memory was missing... the next one will appear when the convergence appears, not before") substitutes for the dropped count as the chapter's parting wisdom — replaces a number with a test.

#### Chapter 1 Memory section (new)

Insert between the MCP section (~line 322) and the Subagents section (~line 325). Two structural subsections matching the two-category split:

**Memory (sketch — user revises voice)**

> Memory is the most recent primitive to go universal. Eighteen months ago it was implicit: the agent loaded a prompt, did some work, and the next session started clean. Today Memory has two halves - one fully converged across the major agents, one led by Claude Code with the others on the path.
>
> **Manually defined memory** is the layer the team writes. The convergence is real: Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider ecosystem all read AGENTS.md from the repository root at session start. Claude Code reads CLAUDE.md, which can import AGENTS.md to share the same content with other agents. The file is committed to source control, reviewed in pull requests, owned by the team. It is the place forbidden patterns, mistake-journal entries, build commands, and domain glossaries live. Chapter 6 covers what goes in this file in detail and why it matters.
>
> **The auto-memory system** is what the agent writes for itself. Claude Code is the early-mover; other agents are converging on similar mechanisms but had not shipped equivalents at publication. It has two visible surfaces: Auto Memory is the layer where Claude saves learned patterns across sessions - build commands it figured out, debugging insights it confirmed, code-style preferences it inferred - without the user explicitly writing them down. Auto Dream is the background-consolidation layer Anthropic unveiled at Code with Claude SF on 2026-05-06: a scheduled process that reviews recent sessions and the memory store, identifies recurring mistakes and convergent workflows, and writes consolidated notes back into long-term memory. The agent gets better at your codebase between runs.
>
> A note on what is *not* memory in this taxonomy: session memory (the conversation history plus tool results inside a single session) is just the context window. It is memory in the everyday sense but not a separate primitive - it is the primitive named first.
>
> Manually defined memory passes the convergence test today. The auto-memory system is on the path - Claude Code is first; others are following. This manual treats them as one primitive because the structural role is identical, with the caveat that the second half is an early-mover signal, not yet a convergence.

Notes on this rewrite:

- Drops spec-author phrases ("crossed the agent-agnostic threshold", "two categorical halves", "structurally distinct mechanisms") in favor of plain prose.
- Names the asymmetry explicitly (per argument-coherence review): manually defined passes the test; auto-memory is "early-mover signal, not yet a convergence". Honest scoping, not smoothing.
- Fixes the Claim 5 imprecision (per technical review): Claude Code reads CLAUDE.md, not AGENTS.md - the interop is via `@AGENTS.md` import. Body copy and Appendix C now agree.
- Auto Dream attribution corrected (per technical review): unveiled at Code with Claude SF, 2026-05-06 (the Managed Agents announcement); the Claude Code surface was an earlier quieter rollout. Appendix C carries the longer caveat.
- Marketing-deck phrase ("self-improvement between runs without manual retraining") replaced with a concrete, in-voice line ("the agent gets better at your codebase between runs").
- All-caps NOT → italics (manual uses italics for emphasis, not caps).
- Self-justifying final paragraph (the "primitive-status test for Memory" block) folded into the second-half opener, since the asymmetry naming now does that work in-line.

#### Chapter 1 subagents section — rewrite line 327

Current line 327:

> What makes subagents structurally distinct from the other five primitives is that they are recursive. A subagent is another instance of the five primitives - it has its own context window, its own tools, its own skills, plugins, MCP - bounded to a smaller task and isolated from the orchestrator's context.

Proposed rewrite:

> What makes subagents structurally distinct from the other primitives is that they are recursive. A subagent is another instance of the primitives - it has its own context window, its own tools, its own skills, plugins, MCP, memory - bounded to a smaller task and isolated from the orchestrator's context.

#### Chapter 1 harness section — rewrite lines 339-355

Current line 339: `One more piece organizes all six.` → `One more piece organizes them all.`

Current line 341: `The six primitives all live inside the harness.` → `The primitives all live inside the harness.`

Current line 345: `The middleware *is* the harness, *is* the six primitives, *is* what you are buying when you adopt an agent.` → `The middleware *is* the harness, *is* the primitives, *is* what you are buying when you adopt an agent.`

Current line 349 (the boundary-primitives contradiction concern — leave the existing claim intact):

> A note on vocabulary. The six primitives are capability primitives: what the agent uses to know, act, extend, integrate, and delegate. The governance mechanisms in Chapter 3 - permissions, sandboxing, hooks, telemetry - are not additional primitives. They are control layers around the primitives, especially around tools and subagents.

Proposed minimal rewrite:

> A note on vocabulary. The primitives named here are capability primitives: what the agent uses to know, act, extend, integrate, remember, and delegate. The governance mechanisms in Chapter 3 - permissions, sandboxing, hooks, telemetry - are not additional primitives. They are control layers around the primitives, especially around tools and subagents.

Closing line 353: `Six primitives. Context window. Tools. Skills. Plugins. MCP. Subagents. Plus the harness as the runtime that organizes them.` → handled in opening-rewrite section above (final paragraph of the rewritten opening).

#### Chapter 1 diagram update

Current `diagram_primitives()` (`build/build_spa.py:27-42`) emits a 2×3 grid of 6 cells with abstract icons (◉ ⚙ ✦ ▣ ↔ ⟲). Caption ends "...Subagents are the recursive primitive: each subagent is itself an instance of the other five."

New approach (synthesizes both reviewer recommendations):
- **Keep the grid** for the 6 named local primitives (per reader review: grids feel like architecture; lists feel like enumeration; readers expect a primitives diagram to look like a diagram).
- **Subagents lives below the grid in its own bottom row spanning full width**, with a small divider above it (per argument review: the original 2×3 grid muddied recursion by putting subagents in a cell alongside the others — separating subagents visually makes recursion visible).
- Memory occupies the 6th cell of the grid (the slot subagents used to fill). Memory carries two small sub-bullets inside the cell: "manually defined" and "auto-memory system" — communicates the two halves without expanding cell count.

Caption updated:

> Figure: The primitives and the harness that runs them. Memory is the most recent primitive to converge across the major agents. Subagents sit below the line because they are the recursive primitive: each subagent is itself an instance of the others.

Implementation in `build/build_spa.py`:

```python
def diagram_primitives() -> str:
    return """<figure class="diagram diagram-primitives">
  <div class="harness">
    <div class="harness-label">THE HARNESS</div>
    <div class="primitives-grid">
      <div class="primitive"><div class="primitive-icon">◉</div><div class="primitive-name">context window</div></div>
      <div class="primitive"><div class="primitive-icon">⚙</div><div class="primitive-name">tools</div></div>
      <div class="primitive"><div class="primitive-icon">✦</div><div class="primitive-name">skills</div></div>
      <div class="primitive"><div class="primitive-icon">▣</div><div class="primitive-name">plugins</div></div>
      <div class="primitive"><div class="primitive-icon">↔</div><div class="primitive-name">MCP</div></div>
      <div class="primitive primitive-memory">
        <div class="primitive-icon">▤</div>
        <div class="primitive-name">memory</div>
        <div class="primitive-sublist">
          <span class="primitive-sub">manually defined</span>
          <span class="primitive-sub">auto-memory system</span>
        </div>
      </div>
    </div>
    <div class="primitives-divider" aria-hidden="true"></div>
    <div class="primitives-recursive">
      <div class="primitive primitive-recursive"><div class="primitive-icon">⟲</div><div class="primitive-name">subagents</div><div class="primitive-note">the agent, recursively</div></div>
    </div>
    <div class="harness-foot">the agent loop binds them together;<br/>subagents spawn constrained child instances of the agent itself</div>
  </div>
  <figcaption>Figure: The primitives and the harness that runs them. Memory is the most recent primitive to converge across the major agents. Subagents sit below the line because they are the recursive primitive: each subagent is itself an instance of the others.</figcaption>
</figure>"""
```

CSS changes in `build/spa_template.html`:
- `.primitives-grid` rule stays (existing 2×3 layout); Memory cell uses the same shape as the others.
- New `.primitives-divider` rule — a thin horizontal rule across the harness's width, just below the grid, to make the local-vs-recursive split visible.
- New `.primitives-recursive` rule (full-width row below the divider; subagents cell visually emphasized — slightly larger, perhaps a different border treatment to telegraph "structurally distinct").
- New `.primitive-sublist` + `.primitive-sub` (small subordinate labels inside the Memory cell — 11px uppercase, light color, two short lines).

#### Cross-reference sweep — exact line edits

Every sweep target identified by the audit. Bulk find-replace where safe; manual rewrite where the structural argument depends on phrasing.

| Line | Current | Proposed |
|---|---|---|
| 26 (TOC) | `1. Six primitives` | `1. The primitives` |
| 161 (Foreword) | `If a future agent ships without something that maps to one of the six primitives, I missed an invariant that I thought was structural.` | `The primitives are an open set. Memory was missing from the original list eighteen months ago; the major agents converged on it within a six-month window. If a future agent ships without a mechanism that maps to one of the primitives, I missed an invariant I thought was structural. If a new primitive emerges, the list grows.` |
| 287 (Chapter 1, existing tech debt picked up per technical review) | `the always-loaded primitive has converged on two names: the vendor-neutral [AGENTS.md](https://agents.md/), supported by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider ecosystem; and CLAUDE.md, the Claude Code-specific variant. Both are markdown files at the project root, both load at session start, both serve the same role.` | Fix the "same file, vendor-specific variant" imprecision (per technical review): `the always-loaded primitive has converged on two filenames: the vendor-neutral [AGENTS.md](https://agents.md/), supported by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider ecosystem; and CLAUDE.md, which Claude Code reads natively. The two are interoperable - Claude Code can import AGENTS.md into CLAUDE.md so the team's content lives in one place across vendors. Both load at session start, both serve the same role.` |
| 187 | `wire priority feature... all six phases of the loop` | unchanged (different "six" — methodology) |
| 228 | `## Six primitives` | `## The primitives` |
| 230 | `the same six conceptual building blocks. Five of them are the agent's local capabilities. The sixth...` | `the same conceptual building blocks. Most are local capabilities of the agent. One - subagents - is the composition mechanism that makes the agent recursive...` (see full rewrite above) |
| 236 (3 occurrences in one paragraph) | `these six primitives... handle the six primitives... which of the six primitives... which of the six primitives` | `these primitives... handle each primitive... which primitive... which primitive` |
| 238 | `Six primitives.` | (paragraph rewritten — handled in opening) |
| 259 (figure caption) | `Figure: The six primitives and the harness that runs them. Subagents are the recursive primitive: each subagent is itself an instance of the other five.` | `Figure: The primitives and the harness that runs them. Memory is the most recent primitive to converge across the major agents. Subagents are the recursive primitive: each subagent is itself an instance of the others.` |
| 327 (2 occurrences) | `What makes subagents structurally distinct from the other five primitives... A subagent is another instance of the five primitives - it has its own context window, its own tools, its own skills, plugins, MCP -` | `What makes subagents structurally distinct from the other primitives... A subagent is another instance of the primitives - it has its own context window, its own tools, its own skills, plugins, MCP, memory -` |
| 339 | `organizes all six` | `organizes them all` |
| 341 | `The six primitives all live inside the harness.` | `The primitives all live inside the harness.` |
| 345 | `is the six primitives, is what you are buying` | `is the primitives, is what you are buying` |
| 349 | `The six primitives are capability primitives: what the agent uses to know, act, extend, integrate, and delegate.` | `The primitives named here are capability primitives: what the agent uses to know, act, extend, integrate, remember, and delegate.` |
| 353 | `Six primitives. Context window. Tools. Skills. Plugins. MCP. Subagents. Plus the harness as the runtime that organizes them.` | `Context window. Tools. Skills. Plugins. MCP. Memory. Subagents. Plus the harness as the runtime that organizes them. That is the list today. The set is open; expect it to grow.` (list-led opener per argument review; the period after each primitive does the percussive work the count used to do) |
| 354 (Ch 1 evaluation questions) | `How big is the context window and how does the agent manage it under pressure? What tools are available and how are they constrained? How are skills implemented - always-loaded, or dispatched on detection? Is there a plugin marketplace and is it growing? Does it speak MCP, and how good is the MCP integration? How does it expose subagents - and is parallel dispatch a first-class operation or an afterthought?` | Split the Memory question into two (per argument review: a single Memory question is "two questions in a trench coat with an 'if there is one' escape hatch"). Memory inserted in primitive order: `How big is the context window and how does the agent manage it under pressure? What tools are available and how are they constrained? How are skills implemented - always-loaded, or dispatched on detection? Is there a plugin marketplace and is it growing? Does it speak MCP, and how good is the MCP integration? Does it read a team-shared memory file at session start? Does it maintain any agent-written learned memory across sessions? How does it expose subagents - and is parallel dispatch a first-class operation or an afterthought?` |
| 357 | `Six questions. They tell you almost everything you need to know to compare the new agent to the one you are using today.` | `Eight questions today; more tomorrow. They tell you almost everything you need to know to compare the new agent to the one you are using today.` (keep a dated count per editorial + reader-experience: the count is the memorization scaffold a teacher uses; "today" signals it will grow) |
| 406 (Ch 2 case note title) | `**Case note: the two-agent demo, six primitives observable in both.**` | `**Case note: the two-agent demo, the primitives observable in both.**` |
| 411 | `the six primitives were not Claude-Code-specific marketing` | `the primitives were not Claude-Code-specific marketing` |
| 412 | `agent identifies the six primitives in each codebase` | `agent identifies the primitives in each codebase` |
| 415 | `Same six primitives present in both codebases` | `Same primitives present in both codebases` |
| 428 | `The harness is the six primitives plus the way they are organized` | `The harness is the primitives plus the way they are organized` |
| 446-447 (Ch 2 inspection sequence) | `You open its repository. You locate context assembly. You locate the tool registry. You locate skills loading. You locate plugin extension. You check for MCP support. You locate subagent dispatch. You locate the permission gate. You locate the sandbox - all wrapped by the harness's agent loop.` | Add the memory inspection point in primitive order: `You open its repository. You locate context assembly. You locate the tool registry. You locate skills loading. You locate plugin extension. You check for MCP support. You locate the memory layer (AGENTS.md or equivalent; any auto-memory surface the vendor exposes). You locate subagent dispatch. You locate the permission gate. You locate the sandbox - all wrapped by the harness's agent loop.` |
| 449 (Ch 2 inspection summary) | `Eight inspection points: context assembly, tool registry, skills loading, plugin extension, MCP support, subagent dispatch, permission gate, sandbox - all wrapped by the harness's agent loop.` | Keep a count (per reader review: counts are the operational scaffold). Bump to 9 with the memory layer added: `Nine inspection points: context assembly, tool registry, skills loading, plugin extension, MCP support, memory layer, subagent dispatch, permission gate, sandbox - all wrapped by the harness's agent loop.` Note: Chapter 2's "Source-inspection checklist" artifact mentions "eight inspection points" too — also bumps to nine in the artifact callout (around line 473). |
| 480 (Ship-this-week) | `Walk this codebase and name the six primitives - context window, tools, skills, plugins, MCP, subagents.` | `Walk this codebase and name the primitives - context window, tools, skills, plugins, MCP, memory, subagents.` |
| 484 | `The six primitives, the diagnostic, and what the diagnostic tells you about governance will be.` | `The primitives, the diagnostic, and what the diagnostic tells you about governance will be.` |
| 794, 858, 938 | "all six phases" / "sixth primitive from Chapter 1" | line 858: `sixth primitive from Chapter 1 - subagents - earns its keep` → `recursive primitive from Chapter 1 - subagents - earns its keep`. Lines 794, 938 unchanged (six-phase loop). |
| 1882 (Closing) | `The six primitives - context window, tools, skills, plugins, MCP, subagents - plus the harness... When you evaluate a new agent, you walk down the list, ask the six questions, and you have your answer.` | `The primitives - context window, tools, skills, plugins, MCP, memory, subagents - plus the harness... When you evaluate a new agent, you walk down the list, ask the question for each primitive, and you have your answer. The list is open; new primitives will appear as the major agents converge on new mechanisms.` (drops "ask the questions one primitive at a time" — prepositional pile-up flagged by editorial) |
| 2311 (Appendix C) | `Source-organized around the same six primitives this manual identifies in Codex CLI and Claude Code.` | `Source-organized around the same primitives this manual identifies in Codex CLI and Claude Code.` |
| Appendix C entry labels (lines 2285, 2292, 2299, 2306, 2313, 2334, 2343-2344 — verify exact list during implementation) | `Chapter 1 (Six primitives)` | `Chapter 1 (The primitives)` |

#### Chapter 1 slug rename + JS redirect stub

In `build/build_spa.py`:
- `SECTION_SLUGS[("chapter", "Six primitives")]` → `SECTION_SLUGS[("chapter", "The primitives")]` (key + value both change)
- `build_anchor_index` legacy alias `index["chapter-1"] = "chapter-1-six-primitives"` → `index["chapter-1"] = "chapter-1-primitives"`
- `render_hash_redirect_js` map: `'#chapter-1': '/chapter-1-six-primitives/'` → `'#chapter-1': '/chapter-1-primitives/'`

Reuse the existing redirect-stub pattern. After per-chapter pages are rendered, emit a small `_site/chapter-1-six-primitives/index.html` containing:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Moved — The primitives</title>
  <link rel="canonical" href="https://ship-it-with.ai/chapter-1-primitives/">
  <meta http-equiv="refresh" content="0; url=/chapter-1-primitives/">
  <meta name="robots" content="noindex, follow">
  <script>location.replace('/chapter-1-primitives/');</script>
</head>
<body>
  <p>This page has moved to <a href="/chapter-1-primitives/">/chapter-1-primitives/</a>.</p>
</body>
</html>
```

Implementation in `build/build_spa.py`: new `render_redirect_stub(old_slug, new_slug)` function called from `main()` after per-chapter rendering. Exclude the old slug from `sitemap.xml` (so Google sees only the new URL as canonical).

### Commit 2 — Chapter 6 intro + Appendix C

#### Chapter 6 opening paragraph (new — prepend to chapter body)

Insert as the very first paragraph of Chapter 6, before the existing opening anecdote:

> AGENTS.md is the manually defined layer of the Memory primitive named in Chapter 1. It is the team-shareable surface - the layer the team authors, reviews, and owns in source control, as infrastructure the team owns. The auto-memory system (Auto Memory, Auto Dream) is per-developer and largely automatic; this chapter focuses on the layer the team explicitly owns, because that is where team-level discipline lives. What follows is six things that go in AGENTS.md, the 200-line budget rule, and the failure modes you see in practice.

The "six things go in AGENTS.md" structure stays. The bridging clause ("six things that go in AGENTS.md") makes the relationship explicit: the chapter's six things are about content of the file, not primitives.

#### Appendix C new entries

Three new entries using the existing Appendix C structure. Insert in the existing category groupings (likely under "Standards and conventions" / "Vendor documentation"):

```markdown
### AGENTS.md as cross-vendor standard

**Claim:** AGENTS.md is read at session start by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider open-source coding-agent ecosystem (20+ vendors listed at agents.md as of 2026-05). Claude Code reads CLAUDE.md, which can import AGENTS.md to share the same content with other agents. The convergence puts AGENTS.md in the manually defined memory layer of the Memory primitive named in Chapter 1.

**Source:** [agents.md](https://agents.md/) (the open standard's site), plus vendor documentation for each agent listed.

**Where used:** Chapter 1 (The primitives, Memory section) and Chapter 6 (AGENTS.md as team infrastructure).

**Caveat:** The exact filename and load semantics vary by vendor - Claude Code reads CLAUDE.md (importable from AGENTS.md via `@AGENTS.md` or symlink); Cursor reads AGENTS.md plus `.cursorrules`. Convergence is on the structural role - user-written, always-loaded, team-shareable - not on byte-identical file format.

### Claude Code Auto Memory

**Claim:** Claude Code maintains an auto-memory layer in which Claude writes notes for itself across sessions - build commands it figured out, debugging insights it confirmed, code-style preferences it inferred - distinct from the user-written CLAUDE.md. Requires Claude Code v2.1.59+; on by default; per-repo storage.

**Source:** [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).

**Where used:** Chapter 1 (The primitives, Memory section).

**Caveat:** Auto memory is Claude-Code-specific at the time of writing. Other coding agents are converging on similar mechanisms but had not shipped an equivalent at publication date.

### Auto Dream (Anthropic background memory consolidation)

**Claim:** Anthropic publicly unveiled Dreaming as part of Claude Managed Agents at Code with Claude SF on 2026-05-06 - a scheduled background process that reviews recent sessions and the memory store, identifies recurring mistakes and convergent workflows, and writes consolidated notes back into long-term memory. The Claude Code surface (`Auto Dream`, accessible via `/dream`) shipped earlier as a research preview gated behind developer access and was documented in March 2026.

**Source:** Code with Claude SF announcement, 2026-05-06; [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).

**Where used:** Chapter 1 (The primitives, Memory section).

**Caveat:** Auto Dream is Claude-Code-specific at publication date. The structural role is what this manual indexes, not the vendor.
```

## Verification

Extend `build/tests/verify_seo_pass.js` with new assertions, all gated on a fresh build:

**Commit 1 assertions:**
- `_site/chapter-1-primitives/index.html` exists, returns 200, `<h1>` text is `The primitives`.
- `_site/chapter-1-six-primitives/index.html` exists (redirect stub), contains `meta http-equiv="refresh"` AND `link rel="canonical" href="https://ship-it-with.ai/chapter-1-primitives/"`.
- `_site/sitemap.xml` lists `/chapter-1-primitives/` and does NOT list `/chapter-1-six-primitives/`.
- `_site/chapter-1-primitives/index.html` body contains the substring `Memory` and `auto-memory system`.
- The diagram caption no longer contains `six primitives` or `other five`.
- Global content sweep — multiple patterns must all return `0` in `_site/read/index.html` and any chapter page:
  - `grep -c "six primitives\|sixth primitive\|the other five\|five primitives\|five capabilities\|six conceptual"` → 0
  - `grep -c "Six questions\|Eight inspection points"` → 0
  - Exception: "six-phase loop" / "all six phases" matches are explicitly allowed (Chapter 5 methodology, intentionally counted; verify by separately counting `six-phase\|six phases` and confirming those account for all remaining `six` mentions).
- Positive markers (must each appear at least once in `_site/read/index.html`):
  - `Eight questions today` (the new operational rubric count on line 357)
  - `Nine inspection points` (the new operational count on line 449)
  - `manually defined layer of the Memory primitive` (the Chapter 6 intro bridging clause)
  - `auto-memory system` (the Memory section second-half label)
  - `early-mover signal, not yet a convergence` (the asymmetry-naming clause)
  - `Auto Dream` AND `Code with Claude SF` (Appendix C attribution)
  - `which can import AGENTS.md to share the same content with other agents` (the Claim 5 fix in both line 287 and the Memory section)
- Landing hash-redirect map: `/#chapter-1` redirects to `/chapter-1-primitives/`.
- Chapter 1 `<title>` is `The primitives — Agentic Coding Field Manual`.
- TOC entry on landing has `Chapter 1 — The primitives` (not `Six primitives`).
- Chapter 1 sidebar TOC marker on `/chapter-1-primitives/` page has `class="toc-current"`.

**Commit 2 assertions:**
- Chapter 6 first paragraph contains `manually defined layer of the Memory primitive`.
- Appendix C contains the three new entry headings (`AGENTS.md as cross-vendor standard`, `Claude Code Auto Memory`, `Auto Dream`).
- Each new Appendix C entry has Claim / Source / Where used / Caveat structure (per the existing pattern).
- No `six primitives` references remain anywhere in `_site/read/index.html` or any chapter page.

All assertions run from the existing `build/tests/verify_seo_pass.js` harness; no new infrastructure needed.

## Build pipeline changes (`build/build_spa.py`)

- `SECTION_SLUGS`: key + value update for Chapter 1.
- `diagram_primitives()`: rewrite per the diagram spec above (grid stays for 6 named primitives; subagents row separated below a divider; Memory cell carries two sub-bullets).
- `build_anchor_index`: legacy alias update for `chapter-1`.
- `render_hash_redirect_js`: target URL update for `#chapter-1`.
- New `render_redirect_stub(old_slug, new_slug)` function — called from `main()` after per-chapter rendering. Emits a small HTML file with `meta refresh` + `link rel=canonical` + JS `location.replace`.
- `render_sitemap`: exclude any old-slug URLs (Chapter 1's old slug doesn't get added to sitemap).

CSS changes in `build/spa_template.html` for the diagram update: `.primitives-grid` keeps its existing layout; new `.primitives-divider` (thin horizontal rule across the harness, just below the grid); new `.primitives-recursive` (full-width row below the divider, subagents cell visually emphasized); new `.primitive-sublist` + `.primitive-sub` (small subordinate labels inside the Memory cell). Goes in the "critical" CSS region (above-the-fold for Chapter 1).

## Error handling

- **`SECTION_SLUGS` rename** — verified at parser load (existing duplicate-slug check still catches collisions). If the new slug is somehow already taken, the build fails loudly.
- **Old-slug redirect stub** — if `render_redirect_stub` fails to write, the build raises; the verify script's "old-slug returns redirect" assertion catches a silent miss.
- **Cross-reference sweep** — the verify script's `grep -c "six primitives"` assertion catches any line the implementer missed.

## Out of scope (explicit)

- Restructuring Chapter 6 around all four memory layers. AGENTS.md remains the chapter subject.
- Dedicated "Boundary primitives" section (hooks/LSPs/observability). Line 349's existing claim stands; open-set framing is communicated by Foreword, chapter open, and diagram caption.
- Session Memory as a separate primitive layer. Collapses to "session memory = context window".
- Rewriting the "Six things go in AGENTS.md" structure inside Chapter 6.
- Per-chapter page redirect for Chapter 6 (slug unchanged).
- The "six-phase loop" naming in Chapter 5 (lines 187, 794, 938 — different concept).
- Any reference to specific search-engine behavior or Google Search Console.

## Reviewer feedback applied (post-revision)

This spec went through a four-reviewer round (editorial voice, technical accuracy, structural argument, reader experience). All findings have been folded into the spec above. Summary of changes:

**From editorial voice review:**
- Foreword 161 redrafted to keep the original's confident "I missed an invariant" cadence (was: spec-author prose with "the test for primitive status is convergence, not count").
- Chapter 1 opening: trimmed "magic number" slangy phrasing; removed the doubled beat ("the set will continue to evolve. The test ... is convergence").
- Memory section: dropped "crossed the agent-agnostic threshold" (jargon); "two categorical halves" → "two halves" (spec-author phrase out of book copy); cut the self-justifying primitive-status paragraph (folded into the second-half opener); replaced "self-improvement between runs without manual retraining" (marketing-deck line) with "the agent gets better at your codebase between runs"; all-caps NOT → italics.
- Closing 1882: dropped "ask the questions one primitive at a time" (prepositional pile-up).
- Chapter 6 intro: "load-bearing infrastructure" → "as infrastructure the team owns".
- Appendix C: dropped quoted adjective-lists ("convergent property is 'user-written, always-loaded, team-shareable'") for plain prose; removed marketing-deck duplicate.

**From technical accuracy review:**
- Claim 5 (CLAUDE.md vs AGENTS.md "same file") corrected throughout. Body copy now: "Claude Code reads CLAUDE.md, which can import AGENTS.md to share the same content with other agents." Pre-existing imprecision in published line 287 added to the sweep table.
- Auto Dream attribution corrected: unveiled at Code with Claude SF, 2026-05-06 for Managed Agents; the Claude Code surface (`Auto Dream` / `/dream`) was an earlier quieter rollout documented in March 2026.
- Auto Memory caveat tightened: added v2.1.59+, on-by-default, per-repo storage details from `code.claude.com/docs/en/memory`.

**From structural argument review:**
- Memory's two-half framing now explicitly names the asymmetry: "Manually defined memory passes the convergence test today. The auto-memory system is on the path - Claude Code is first; others are following. ... an early-mover signal, not yet a convergence." Honest scoping rather than smoothing.
- Closing drumbeat (line 353): "Named primitives." rejected as rhetorical regression; replaced with list-led opener ("Context window. Tools. Skills. Plugins. MCP. Memory. Subagents. ... That is the list today. The set is open; expect it to grow."). The period after each primitive carries the percussive work the count used to do.
- Evaluation Memory question (line 354) split into two: "Does it read a team-shared memory file at session start? Does it maintain any agent-written learned memory across sessions?" Breaks one-question-per-primitive symmetry but preserves operational clarity.

**From reader-experience review:**
- Open-set acknowledgment moved AFTER the named list in Chapter 1 opening (was: paragraph 2, before the reader knew what a primitive IS). Now lives in the closing paragraph and in the Foreword.
- Operational counts kept and updated rather than dropped: "Eight questions today; more tomorrow" (line 357); "Nine inspection points" (line 449). Counts are the memorization scaffold a teacher uses; the "today" temporal hedge signals openness without dropping the count entirely.
- Chapter 2 artifact "Source-inspection checklist. The eight inspection points from this chapter" also bumps to nine.
- Diagram: keep the 2×3 grid for the 6 named local primitives (Reader: grids feel like architecture, lists like enumeration), but separate subagents as a full-width bottom row below a divider (Argument: original grid muddied recursion by putting subagents alongside the others). Synthesizes both reviewer recommendations.

## Open items for user review

1. **The Foreword 161, Chapter 1 opening, Memory section, Closing 1882, and Chapter 6 intro sketches** — all reflect reviewer feedback. The author reviews voice/cadence during diff review.
2. **Diagram visual** — synthesizes both reviewer views (grid + separated subagents row). The Memory icon `▤` is open (alternatives: `☰`, `▥`, or any other glyph that reads as "layered storage"). User confirms.
3. **Appendix C wording** — particularly the Auto Memory / Auto Dream caveats (both Claude-Code-specific today). User confirms the convergence-vs-early-mover framing.

## Resolved decisions (defaults applied — flag in review if you want to change)

1. **Chapter 1 H1**: `The primitives` (short, matches workshop deck framing).
2. **Chapter 1 slug**: `/chapter-1-primitives/` with JS+meta-refresh redirect stub at the old `/chapter-1-six-primitives/` URL.
3. **Chapter 6 stays AGENTS.md-focused.** Slug unchanged. One new opening paragraph anchors AGENTS.md as the manually defined memory layer of the Memory primitive.
4. **Memory structured around two halves**: manually defined memory (agent-agnostic, passes the convergence test) and auto-memory system (Claude-Code-specific today, named as early-mover signal). Asymmetry named explicitly per argument-coherence review.
5. **Session Memory collapses** to "session memory = context window" — one-sentence mention, not a separate layer.
6. **No Boundary primitives section.** Line 349's existing claim stands. Open-set framing communicated via Foreword + chapter-close paragraph + diagram caption.
7. **Structural argument rewrite**: "most primitives are local; one - subagents - is the recursive primitive" replaces "five local + one recursive". The local/recursive distinction stays; the count goes.
8. **Two atomic commits**, not three. Each commit leaves the book internally consistent.
9. **Diagram**: keep the 2×3 grid for the 6 named local primitives; subagents lives below the grid in a full-width row separated by a thin divider. Memory cell carries two sub-bullets ("manually defined" / "auto-memory system"). Synthesizes reader (grid) + argument (subagents-separated) feedback.
10. **Appendix C new entries**: three (AGENTS.md cross-vendor standard, Auto Memory, Auto Dream). Use the existing claim/source/where-used/caveat structure. Auto Dream attribution: Code with Claude SF (Managed Agents) + earlier quiet Claude Code rollout (March 2026).
11. **The "six-phase loop"** in Chapter 5 stays. Different "six" (methodology, intentionally counted).
12. **The "Six things go in AGENTS.md"** structure in Chapter 6 stays. Orthogonal to primitive count.
13. **Operational counts**: chapter TITLE drops the count ("The primitives", not "Six primitives"). Operational rubrics keep counts with a "today" temporal hedge ("Eight questions today; more tomorrow", "Nine inspection points") — counts are the memorization scaffold; the temporal hedge honors the open-set framing.
14. **Closing drumbeat**: list-led opener, not a category label. The period after each primitive carries the percussive work the count used to do.
15. **Claim 5 fix scope**: pre-existing imprecision on line 287 of the published manual ("CLAUDE.md, the Claude Code-specific variant") is picked up in the same sweep, since the spec's new wording would otherwise contradict it.
