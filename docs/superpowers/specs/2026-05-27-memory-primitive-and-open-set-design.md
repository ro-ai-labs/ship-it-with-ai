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
> The set is not closed at a magic number. Memory is the most recent primitive to converge across the major agents - eighteen months ago it was implicit in context window; today AGENTS.md (and CLAUDE.md, the Claude Code-specific filename) is a standard the major agents read at session start, and Claude Code has shipped an auto-memory system around it. The set will continue to evolve. The test for what counts as a primitive is not a count; it is convergence across the major agents.
>
> ...
>
> That is the anatomy. Every interesting question about a coding agent - what it can do, what it cannot do, how to control it, what to compare it to - reduces to one or more of these primitives. When a new agent arrives, your first question is: how does this one handle each primitive? When you are deciding whether to let an agent touch a particular codebase, your second question is: which primitive is the relevant control point for this risk? When you are buying tooling, your third question is: which primitive does this tooling improve, and at what cost?
>
> ...
>
> Named primitives. Context window. Tools. Skills. Plugins. MCP. Memory. Subagents. Plus the harness as the runtime that organizes them. An open set, not a closed list.

#### Chapter 1 Memory section (new)

Insert between the MCP section (~line 322) and the Subagents section (~line 325). Two structural subsections matching the two-category split:

**Memory (sketch — user revises voice)**

> Memory is the primitive that crossed the agent-agnostic threshold most recently. Eighteen months ago it was implicit: the agent loaded a prompt, did some work, and the next session started clean. Today the major agents converge on two structurally distinct mechanisms: manually defined memory and an auto-memory system.
>
> **Manually defined memory** is the layer the team writes. The convergence is real: Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider ecosystem all read AGENTS.md from the repository root at session start; Claude Code reads CLAUDE.md (same file, Claude Code-specific filename) at the same moment. The file is committed to source control, reviewed in pull requests, owned by the team. It is the place forbidden patterns, mistake-journal entries, build commands, and domain glossaries live. Chapter 6 covers what goes in this file in detail and why it matters.
>
> **The auto-memory system** is what the agent writes for itself. Currently Claude-Code-specific (other agents are converging on similar mechanisms), it has two visible surfaces: Auto Memory is the layer where Claude saves learned patterns across sessions — build commands it figured out, debugging insights it confirmed, code-style preferences it inferred — without the user explicitly writing them down. Auto Dream is the background-consolidation layer Anthropic announced in May 2026: a scheduled process that reviews recent sessions and the memory store, identifies recurring mistakes and convergent workflows, and writes consolidated notes back into long-term memory. Self-improvement between runs without manual retraining.
>
> A note on what is NOT memory in this taxonomy: session memory (the conversation history plus tool results inside a single session) is just the context window. It is memory in the everyday sense but not a separate primitive — it is the primitive named first.
>
> The primitive-status test for Memory: AGENTS.md / CLAUDE.md pass cleanly (cross-vendor convergence). The auto-memory system passes the test on Claude Code today and is on the path to passing it across the wider ecosystem; this manual treats it as part of the same primitive because the structural role is identical even when implementation varies.

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

New approach: drop the 2×3 grid; vertical list with subagents visually separated as the structurally distinct recursive primitive. Memory shown with two sub-bullets (manually defined / auto-memory system) without expanding the cell count proper. Caption updated:

> Figure: The primitives and the harness that runs them. Memory is the most recent primitive to converge across the major agents. Subagents are the recursive primitive: each subagent is itself an instance of the others.

Implementation in `build/build_spa.py`:

```python
def diagram_primitives() -> str:
    return """<figure class="diagram diagram-primitives">
  <div class="harness">
    <div class="harness-label">THE HARNESS</div>
    <div class="primitives-list">
      <div class="primitive"><div class="primitive-icon">◉</div><div class="primitive-name">context window</div></div>
      <div class="primitive"><div class="primitive-icon">⚙</div><div class="primitive-name">tools</div></div>
      <div class="primitive"><div class="primitive-icon">✦</div><div class="primitive-name">skills</div></div>
      <div class="primitive"><div class="primitive-icon">▣</div><div class="primitive-name">plugins</div></div>
      <div class="primitive"><div class="primitive-icon">↔</div><div class="primitive-name">MCP</div></div>
      <div class="primitive primitive-memory">
        <div class="primitive-icon">▤</div>
        <div class="primitive-name">memory</div>
        <div class="primitive-sublist">
          <span class="primitive-sub">manually defined (AGENTS.md, CLAUDE.md)</span>
          <span class="primitive-sub">auto-memory system (Auto Memory, Auto Dream)</span>
        </div>
      </div>
    </div>
    <div class="primitives-recursive">
      <div class="primitive primitive-recursive"><div class="primitive-icon">⟲</div><div class="primitive-name">subagents</div><div class="primitive-note">the agent, recursively</div></div>
    </div>
    <div class="harness-foot">the agent loop binds them together;<br/>subagents spawn constrained child instances of the agent itself</div>
  </div>
  <figcaption>Figure: The primitives and the harness that runs them. Memory is the most recent primitive to converge across the major agents. Subagents are the recursive primitive: each subagent is itself an instance of the others.</figcaption>
</figure>"""
```

CSS changes in `build/spa_template.html`:
- Replace `.primitives-grid` rule with `.primitives-list` (vertical flex with gap)
- Add `.primitives-recursive` rule (visually separated below the main list — small divider, subagents in its own emphasized row)
- Add `.primitive-sublist` + `.primitive-sub` (small subordinate labels under Memory)

#### Cross-reference sweep — exact line edits

Every sweep target identified by the audit. Bulk find-replace where safe; manual rewrite where the structural argument depends on phrasing.

| Line | Current | Proposed |
|---|---|---|
| 26 (TOC) | `1. Six primitives` | `1. The primitives` |
| 161 (Foreword) | `If a future agent ships without something that maps to one of the six primitives, I missed an invariant that I thought was structural.` | `The primitives are an open set, not a closed list. I expect new ones to emerge as the major agents converge on new mechanisms - Memory is the most recent example, missing from the original list eighteen months ago and shipped across the major agents within a six-month window. The test for primitive status is convergence, not count.` |
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
| 353 | `Six primitives. Context window. Tools. Skills. Plugins. MCP. Subagents. Plus the harness as the runtime that organizes them.` | `Named primitives. Context window. Tools. Skills. Plugins. MCP. Memory. Subagents. Plus the harness as the runtime that organizes them. An open set, not a closed list.` |
| 354 (Ch 1 evaluation questions) | `How big is the context window and how does the agent manage it under pressure? What tools are available and how are they constrained? How are skills implemented - always-loaded, or dispatched on detection? Is there a plugin marketplace and is it growing? Does it speak MCP, and how good is the MCP integration? How does it expose subagents - and is parallel dispatch a first-class operation or an afterthought?` | Add a Memory question in primitive order (between MCP and subagents): `How big is the context window and how does the agent manage it under pressure? What tools are available and how are they constrained? How are skills implemented - always-loaded, or dispatched on detection? Is there a plugin marketplace and is it growing? Does it speak MCP, and how good is the MCP integration? How does it handle memory - both the user-written AGENTS.md surface and the auto-memory system if there is one? How does it expose subagents - and is parallel dispatch a first-class operation or an afterthought?` |
| 357 | `Six questions. They tell you almost everything you need to know to compare the new agent to the one you are using today.` | `These questions tell you almost everything you need to know to compare the new agent to the one you are using today. The list will grow as the primitives do.` |
| 406 (Ch 2 case note title) | `**Case note: the two-agent demo, six primitives observable in both.**` | `**Case note: the two-agent demo, the primitives observable in both.**` |
| 411 | `the six primitives were not Claude-Code-specific marketing` | `the primitives were not Claude-Code-specific marketing` |
| 412 | `agent identifies the six primitives in each codebase` | `agent identifies the primitives in each codebase` |
| 415 | `Same six primitives present in both codebases` | `Same primitives present in both codebases` |
| 428 | `The harness is the six primitives plus the way they are organized` | `The harness is the primitives plus the way they are organized` |
| 446-447 (Ch 2 inspection sequence) | `You open its repository. You locate context assembly. You locate the tool registry. You locate skills loading. You locate plugin extension. You check for MCP support. You locate subagent dispatch. You locate the permission gate. You locate the sandbox - all wrapped by the harness's agent loop.` | Add the memory inspection point in primitive order: `You open its repository. You locate context assembly. You locate the tool registry. You locate skills loading. You locate plugin extension. You check for MCP support. You locate the memory layer (AGENTS.md or equivalent; any auto-memory surface the vendor exposes). You locate subagent dispatch. You locate the permission gate. You locate the sandbox - all wrapped by the harness's agent loop.` |
| 449 (Ch 2 inspection summary) | `Eight inspection points: context assembly, tool registry, skills loading, plugin extension, MCP support, subagent dispatch, permission gate, sandbox - all wrapped by the harness's agent loop.` | Drop the count, add memory: `The inspection points: context assembly, tool registry, skills loading, plugin extension, MCP support, memory layer, subagent dispatch, permission gate, sandbox - all wrapped by the harness's agent loop.` |
| 480 (Ship-this-week) | `Walk this codebase and name the six primitives - context window, tools, skills, plugins, MCP, subagents.` | `Walk this codebase and name the primitives - context window, tools, skills, plugins, MCP, memory, subagents.` |
| 484 | `The six primitives, the diagnostic, and what the diagnostic tells you about governance will be.` | `The primitives, the diagnostic, and what the diagnostic tells you about governance will be.` |
| 794, 858, 938 | "all six phases" / "sixth primitive from Chapter 1" | line 858: `sixth primitive from Chapter 1 - subagents - earns its keep` → `recursive primitive from Chapter 1 - subagents - earns its keep`. Lines 794, 938 unchanged (six-phase loop). |
| 1882 (Closing) | `The six primitives - context window, tools, skills, plugins, MCP, subagents - plus the harness... When you evaluate a new agent, you walk down the list, ask the six questions, and you have your answer.` | `The primitives - context window, tools, skills, plugins, MCP, memory, subagents - plus the harness... When you evaluate a new agent, you walk down the list, ask the questions one primitive at a time, and you have your answer. The set is open; expect new primitives to emerge as the major agents converge on new mechanisms.` |
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

> AGENTS.md is the manually defined layer of the Memory primitive named in Chapter 1. It is the team-shareable surface - the layer the team authors, reviews, owns in source control, and treats as load-bearing infrastructure. The auto-memory system (Auto Memory, Auto Dream) is per-developer and largely automatic; this chapter focuses on the layer the team explicitly owns, because that is where team-level discipline lives. What follows is six things that go in AGENTS.md, the 200-line budget rule, and the failure modes you see in practice.

The "six things go in AGENTS.md" structure stays. The bridging clause ("six things that go in AGENTS.md") makes the relationship explicit: the chapter's six things are about content of the file, not primitives.

#### Appendix C new entries

Three new entries using the existing Appendix C structure. Insert in the existing category groupings (likely under "Standards and conventions" / "Vendor documentation"):

```markdown
### AGENTS.md as cross-vendor standard

**Claim:** AGENTS.md is read at session start by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider open-source coding-agent ecosystem. Claude Code reads CLAUDE.md (same file, vendor-specific filename) at the same moment. The convergence puts AGENTS.md in the manually defined memory layer of the Memory primitive named in Chapter 1.

**Source:** [agents.md](https://agents.md/) (the open standard's site), plus vendor documentation for each agent listed.

**Where used:** Chapter 1 (The primitives, Memory section) and Chapter 6 (AGENTS.md as team infrastructure).

**Caveat:** The exact filename and load semantics vary by vendor (e.g., Claude Code reads CLAUDE.md plus files in `.claude/rules/`; Cursor reads AGENTS.md plus `.cursorrules`); the convergent property is "user-written, always-loaded, team-shareable", not byte-identical file format.

### Claude Code Auto Memory

**Claim:** Claude Code maintains an auto-memory layer in which Claude writes notes for itself across sessions - build commands it figured out, debugging insights it confirmed, code-style preferences it inferred - distinct from the user-written CLAUDE.md.

**Source:** [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).

**Where used:** Chapter 1 (The primitives, Memory section).

**Caveat:** Auto Memory is Claude-Code-specific at the time of writing. Other coding agents are converging on similar mechanisms but had not shipped an equivalent at publication date.

### Auto Dream (Anthropic background memory consolidation)

**Claim:** Anthropic announced Auto Dream on 2026-05-06 - a scheduled background process that reviews recent sessions and the memory store, identifies recurring mistakes and convergent workflows, and writes consolidated notes back into long-term memory. Self-improvement between runs without manual retraining.

**Source:** Anthropic announcement, 2026-05-06; [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).

**Where used:** Chapter 1 (The primitives, Memory section).

**Caveat:** Auto Dream is Claude-Code-specific at publication date. The framing in this manual is that it is a structural feature of the auto-memory system, regardless of which vendor ships it first.
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
- `diagram_primitives()`: full rewrite per the diagram spec above.
- `build_anchor_index`: legacy alias update for `chapter-1`.
- `render_hash_redirect_js`: target URL update for `#chapter-1`.
- New `render_redirect_stub(old_slug, new_slug)` function — called from `main()` after per-chapter rendering. Emits a small HTML file with `meta refresh` + `link rel=canonical` + JS `location.replace`.
- `render_sitemap`: exclude any old-slug URLs (Chapter 1's old slug doesn't get added to sitemap).

CSS changes in `build/spa_template.html` for the new diagram layout: replace `.primitives-grid` with `.primitives-list` (vertical flex); add `.primitives-recursive` for visual separation of the subagents row; add `.primitive-sublist` / `.primitive-sub` for the Memory two-sub-bullet display. Goes in the "critical" CSS region (above-the-fold for Chapter 1).

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

## Open items for user review

1. **Memory section copy (Chapter 1).** Sketched in this spec. User revises voice/length during diff review.
2. **Foreword line 161 rewrite.** Sketched (epistemological shift from "I claim the count is structural" to "convergence is the test"). User confirms tone fits the Foreword's voice.
3. **Closing line 1882 rewrite.** Sketched. User confirms.
4. **Chapter 6 opening paragraph.** Sketched. User confirms voice.
5. **Diagram visual.** Going with option (c) — drop the grid, vertical list with subagents called out. Memory shown with two sub-bullets. User confirms visual direction (especially the Memory icon `▤` — could also use `☰` or another glyph).
6. **Appendix C three new entries.** Drafted from the workshop spec + the Anthropic announcement. User confirms the convergence claim wording (especially for Auto Memory / Auto Dream, which are Claude-Code-specific today).

## Resolved decisions (defaults applied — flag in review if you want to change)

1. **Chapter 1 H1**: `The primitives` (short, matches workshop deck framing).
2. **Chapter 1 slug**: `/chapter-1-primitives/` with JS+meta-refresh redirect stub at the old `/chapter-1-six-primitives/` URL.
3. **Chapter 6 stays AGENTS.md-focused.** Slug unchanged. One new opening paragraph anchors AGENTS.md as the manually defined memory layer of the Memory primitive.
4. **Memory structured around two categorical halves**: manually defined memory (agent-agnostic) and auto-memory system (Claude-Code-specific today).
5. **Session Memory collapses** to "session memory = context window" — one-sentence mention, not a separate layer.
6. **No Boundary primitives section.** Line 349's existing claim stands. Open-set framing communicated via Foreword + chapter open + diagram caption.
7. **Structural argument rewrite**: "named primitives + the recursive primitive (subagents)" replaces "five local + one recursive". The local/recursive distinction stays; the count goes.
8. **Two atomic commits**, not three. Each commit leaves the book internally consistent.
9. **Diagram**: vertical list (drop the 2×3 grid). Subagents visually separated as the recursive primitive. Memory carries two sub-bullets.
10. **Appendix C new entries**: three (AGENTS.md cross-vendor standard, Auto Memory, Auto Dream). Use the existing claim/source/where-used/caveat structure.
11. **The "six-phase loop"** in Chapter 5 stays. Different "six" (methodology, intentionally counted).
12. **The "Six things go in AGENTS.md"** structure in Chapter 6 stays. Orthogonal to primitive count.
