# Memory Primitive + Open-Set Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retroactively add Memory as a named primitive across the book, drop the closed "six" count for an open-set framing, rewrite Chapter 1's structural argument from "five local + one recursive" to "named primitives + the recursive primitive (subagents)", and sweep ~25 cross-book count-anchored references. Chapter 6 gets a one-paragraph framing intro; Appendix C gets three new sourced entries.

**Architecture:** Two atomic commits in one branch (`memory-primitive`), each leaving the book internally consistent. Commit 1 rewrites Chapter 1 + sweeps every count-anchored reference book-wide + renames the chapter slug + emits a JS redirect stub at the old URL. Commit 2 adds Chapter 6's intro paragraph + three Appendix C entries. The existing build pipeline (per-chapter rendering, sitemap, hash-redirect map) accommodates the changes via small targeted edits.

**Tech Stack:** Python 3.12 + `markdown` for the build. Vanilla HTML/CSS in the template. Playwright + Python `http.server` for verification (existing `build/tests/verify_seo_pass.js` extended in-place).

**Spec:** `docs/superpowers/specs/2026-05-27-memory-primitive-and-open-set-design.md` — read this first; every task assumes its decisions.

**Branch:** `memory-primitive`. Do NOT push to main during execution.

---

## File map

**Modify:**
- `source/Ship_It_With_AI.md` — content edits across TOC (line 26), Foreword (line 161), Chapter 1 (lines 228-357), Chapter 2 (lines 406-484, plus artifact at ~473), Chapter 5 (line 858), Closing (line 1882), Appendix C (5-8 cross-ref labels + line 2311 + 3 new entries in Commit 2), Chapter 6 intro paragraph (Commit 2), line 287 (tech-debt Claim 5 fix).
- `build/build_spa.py` — `SECTION_SLUGS` key + value, `diagram_primitives()`, `build_anchor_index` legacy alias, `render_hash_redirect_js` target URL, new `render_redirect_stub()` function, `render_sitemap` exclusion.
- `build/spa_template.html` — three new CSS rules (`.primitives-divider`, `.primitives-recursive`, `.primitive-sublist` + `.primitive-sub`) in the critical CSS region.
- `build/tests/verify_seo_pass.js` — new positive-marker assertions; updated SLUGS list; new redirect-stub assertion.

**Create:**
- (none — all changes land in existing files)

**Do NOT modify:**
- `.github/workflows/static.yml` — CI rebuilds + deploys; no changes needed.
- `.gitignore`, `build/static/*`, `build/tests/lib/build_and_serve.js`, `build/cover_to_webp.py` — unaffected.
- Any chapter content outside the cross-reference sweep (Chapter 3, Chapter 4, Chapter 7-10, About, Acknowledgments, Prologue).

---

## Workflow conventions

After every code or content change in this plan, the rebuild + verify cycle is:

```bash
python3 build/build_spa.py
node build/tests/verify_seo_pass.js
```

Until Task 16 lands (the new verify assertions), use plain `grep` against built `_site/` files to spot-check intermediate state.

The build emits `_site/` from scratch each run; nothing committed at the repo root needs touching except the source and the build script + template.

---

# COMMIT 1 — Chapter 1 + book-wide sweep + diagram + slug + verify

This commit must leave the book internally consistent — every count-anchored reference is swept in one go.

## Task 1: Create the feature branch

**Files:** none

- [ ] **Step 1: Confirm main is up to date**

```bash
git checkout main
git status
```

Expected: clean working tree on `main`.

- [ ] **Step 2: Create and switch to the branch**

```bash
git checkout -b memory-primitive
git status
```

Expected: `nothing to commit, working tree clean` on `memory-primitive`.

---

## Task 2: SECTION_SLUGS + legacy alias + hash-redirect map

**Why:** The slug rename `chapter-1-six-primitives` → `chapter-1-primitives` is the smallest mechanical change and unblocks the per-chapter URL generation, the sitemap entry, and the redirect-stub work later in this commit.

**Files:**
- Modify: `build/build_spa.py` — `SECTION_SLUGS` dict, `build_anchor_index` legacy alias, `render_hash_redirect_js` target URL

- [ ] **Step 1: Locate `SECTION_SLUGS`**

```bash
grep -n "SECTION_SLUGS\|\"Six primitives\"\|\"chapter-1-six-primitives\"" build/build_spa.py
```

Expected: the dict declaration and the chapter-1 entry. Note the line numbers.

- [ ] **Step 2: Update the SECTION_SLUGS entry**

Edit `build/build_spa.py`. Find:

```python
    ("chapter", "Six primitives"):                                  "chapter-1-six-primitives",
```

Change to:

```python
    ("chapter", "The primitives"):                                  "chapter-1-primitives",
```

(Both the key tuple and the value string change.)

- [ ] **Step 3: Update the legacy alias in `build_anchor_index`**

```bash
grep -n "chapter-1-six-primitives\|chapter-1" build/build_spa.py | head -10
```

Find the line in `build_anchor_index` that maps `chapter-1` → the chapter-1 slug. Change `chapter-1-six-primitives` to `chapter-1-primitives` in that mapping.

- [ ] **Step 4: Update the hash-redirect map**

```bash
grep -n "render_hash_redirect_js\|#chapter-1.*chapter-1" build/build_spa.py | head -5
```

Find the line emitting the redirect for `#chapter-1`. Change the target URL from `/chapter-1-six-primitives/` to `/chapter-1-primitives/`.

- [ ] **Step 5: Build — should partially succeed but produce inconsistent state (Chapter 1 heading still says "Six primitives" in source)**

```bash
python3 build/build_spa.py 2>&1 | tail -5
```

Expected: build completes. The `parse_sections` step uses the source heading `## Six primitives` and tries to look it up in `SECTION_SLUGS` — fails because the key changed to `"The primitives"`. Build raises `RuntimeError: unknown section in SECTION_SLUGS: ('chapter', 'Six primitives')`. **This expected failure is the proof the parser is consulting the new map; the source heading update in Task 3 will fix it.**

- [ ] **Step 6: Commit (deferred — bundled into Commit 1)**

---

## Task 3: Chapter 1 heading + TOC line

**Files:**
- Modify: `source/Ship_It_With_AI.md` — line 26 (TOC entry), line 228 (chapter heading)

- [ ] **Step 1: Update the TOC entry**

```bash
grep -n "^1\. Six primitives\|^## Chapter 1\|^## Six primitives" source/Ship_It_With_AI.md
```

Expected: line 26 (TOC), line 227 (`## Chapter 1`), line 228 (`## Six primitives`).

Edit `source/Ship_It_With_AI.md`. Change line 26 from `1. Six primitives` to `1. The primitives`.

- [ ] **Step 2: Update the chapter heading**

Edit line 228. Change `## Six primitives` to `## The primitives`.

- [ ] **Step 3: Rebuild — Task 2's RuntimeError should now resolve**

```bash
python3 build/build_spa.py 2>&1 | tail -5
```

Expected: build completes cleanly; output mentions `Wrote _site/chapter-1-primitives/index.html`.

- [ ] **Step 4: Quick smoke checks**

```bash
ls _site/chapter-1-primitives/index.html
ls _site/chapter-1-six-primitives/index.html 2>&1
```

Expected: first file exists; second does not (the old slug isn't emitted; the redirect stub lands in Task 10).

- [ ] **Step 5: Commit (deferred — bundled into Commit 1)**

---

## Task 4: Chapter 1 opening rewrite (paragraphs around line 230, 236)

**Why:** The structural argument changes from "five local + one recursive = six" to "most local; one recursive (subagents)". The open-set acknowledgment moves AFTER the named list per reader-experience review.

**Files:**
- Modify: `source/Ship_It_With_AI.md` — paragraph at line 230, paragraph at line 236

- [ ] **Step 1: Read the current state of lines 228-260**

```bash
sed -n '228,260p' source/Ship_It_With_AI.md
```

Expected: chapter heading (now updated in Task 3), the multi-sentence paragraph at line 230, then the paragraph at line 236.

- [ ] **Step 2: Replace the line 230 paragraph**

Find this sentence in `source/Ship_It_With_AI.md` (currently line 230):

```
Open the source code or documentation of most production-grade coding agents - Codex CLI in Rust, opencode in TypeScript, the public-source parts of Claude Code, the agents shipped by half a dozen smaller vendors - and you see the same architecture emerging: six primitives wrapped by a harness. The implementations differ. The anatomy converges. Different names sometimes, different file layouts always, but the same six conceptual building blocks. Five of them are the agent's local capabilities. The sixth is the composition mechanism that makes the agent recursive: it can spawn constrained instances of itself.
```

Replace with:

```
Open the source code or documentation of most production-grade coding agents - Codex CLI in Rust, opencode in TypeScript, the public-source parts of Claude Code, the agents shipped by half a dozen smaller vendors - and you see the same architecture emerging: a small set of primitives wrapped by a harness. The implementations differ. The anatomy converges. Different names sometimes, different file layouts always, but the same conceptual building blocks. Most are local capabilities of the agent. One - subagents - is the composition mechanism that makes the agent recursive: it can spawn constrained instances of itself.
```

- [ ] **Step 3: Replace the line 236 paragraph**

Find this sentence (currently line 236):

```
That is the anatomy. Every interesting question about a coding agent - what it can do, what it cannot do, how to control it, what to compare it to - reduces to one or more of these six primitives. When a new agent arrives, your first question is: how does this one handle the six primitives? When you are deciding whether to let an agent touch a particular codebase, your second question is: which of the six primitives is the relevant control point for this risk? When you are buying tooling, your third question is: which of the six primitives does this tooling improve, and at what cost?
```

Replace with:

```
That is the anatomy. Every interesting question about a coding agent - what it can do, what it cannot do, how to control it, what to compare it to - reduces to one or more of these primitives. When a new agent arrives, your first question is: how does this one handle each primitive? When you are deciding whether to let an agent touch a particular codebase, your second question is: which primitive is the relevant control point for this risk? When you are buying tooling, your third question is: which primitive does this tooling improve, and at what cost?
```

- [ ] **Step 4: Remove the standalone `Six primitives.` line**

```bash
grep -n "^Six primitives\.$" source/Ship_It_With_AI.md
```

Expected: line 238 — a one-line paragraph. Delete the entire line (and the blank lines around it that would otherwise leave a double-blank). The new closer lives at line 353; this standalone repeat is no longer needed.

- [ ] **Step 5: Rebuild + spot-check**

```bash
python3 build/build_spa.py
grep -c "six primitives\|six conceptual\|Five of them\|the sixth\|six primitives" _site/chapter-1-primitives/index.html
```

Expected: `0` (no remaining count-anchored phrasings in the chapter 1 opening).

- [ ] **Step 6: Commit (deferred — bundled into Commit 1)**

---

## Task 5: Chapter 1 Memory section (new, ~5 paragraphs)

**Why:** The new primitive needs prose treatment. Two-half structure (manually defined vs auto-memory system), with the asymmetry explicitly named.

**Files:**
- Modify: `source/Ship_It_With_AI.md` — insert after the MCP section, before the Subagents section (~around line 322)

- [ ] **Step 1: Find the insertion point**

```bash
grep -n "^### MCP\|^### Subagents\|^### " source/Ship_It_With_AI.md | head -20
```

Locate the line where the Subagents subsection begins inside Chapter 1. Insertion point is immediately before that line (with a separator blank line).

- [ ] **Step 2: Insert the Memory section**

Insert this content as a new H3 subsection between MCP and Subagents:

```markdown
### Memory

Memory is the most recent primitive to go universal. Eighteen months ago it was implicit: the agent loaded a prompt, did some work, and the next session started clean. Today Memory has two halves - one fully converged across the major agents, one led by Claude Code with the others on the path.

**Manually defined memory** is the layer the team writes. The convergence is real: Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider ecosystem all read [AGENTS.md](https://agents.md/) from the repository root at session start. Claude Code reads CLAUDE.md, which can import AGENTS.md to share the same content with other agents. The file is committed to source control, reviewed in pull requests, owned by the team. It is the place forbidden patterns, mistake-journal entries, build commands, and domain glossaries live. Chapter 6 covers what goes in this file in detail and why it matters.

**The auto-memory system** is what the agent writes for itself. Claude Code is the early-mover; other agents are converging on similar mechanisms but had not shipped equivalents at publication. It has two visible surfaces: Auto Memory is the layer where Claude saves learned patterns across sessions - build commands it figured out, debugging insights it confirmed, code-style preferences it inferred - without the user explicitly writing them down. Auto Dream is the background-consolidation layer Anthropic unveiled at Code with Claude SF on 2026-05-06: a scheduled process that reviews recent sessions and the memory store, identifies recurring mistakes and convergent workflows, and writes consolidated notes back into long-term memory. The agent gets better at your codebase between runs.

A note on what is *not* memory in this taxonomy: session memory (the conversation history plus tool results inside a single session) is just the context window. It is memory in the everyday sense but not a separate primitive - it is the primitive named first.

Manually defined memory passes the convergence test today. The auto-memory system is on the path - Claude Code is first; others are following. This manual treats them as one primitive because the structural role is identical, with the caveat that the second half is an early-mover signal, not yet a convergence.

---

```

(Note: the trailing `---` keeps the source markdown's existing section-separator pattern.)

- [ ] **Step 3: Rebuild and verify the section renders**

```bash
python3 build/build_spa.py
grep -c "manually defined memory\|auto-memory system\|early-mover signal" _site/chapter-1-primitives/index.html
```

Expected: each term appears at least once.

- [ ] **Step 4: Verify the Memory section ID + sidebar link**

```bash
grep "id=\"memory\"" _site/chapter-1-primitives/index.html | head -3
```

Expected: an `<h3 id="memory">` heading.

- [ ] **Step 5: Commit (deferred — bundled into Commit 1)**

---

## Task 6: Chapter 1 subagents section + harness section (lines 327, 339, 341, 345, 349, 353)

**Why:** The subagents section's "other five primitives" wording, plus the harness section's count references and the line 349 vocabulary note all need the count dropped.

**Files:**
- Modify: `source/Ship_It_With_AI.md` — lines 327, 339, 341, 345, 349, 353

- [ ] **Step 1: Locate the lines**

```bash
grep -n "other five primitives\|five primitives - it has\|organizes all six\|six primitives all live\|is the six primitives\|six primitives are capability\|^Six primitives\. Context window" source/Ship_It_With_AI.md
```

Expected: lines 327, 339, 341, 345, 349, 353.

- [ ] **Step 2: Line 327 — drop "other five"**

Find:

```
What makes subagents structurally distinct from the other five primitives is that they are recursive. A subagent is another instance of the five primitives - it has its own context window, its own tools, its own skills, plugins, MCP - bounded to a smaller task and isolated from the orchestrator's context.
```

Replace with:

```
What makes subagents structurally distinct from the other primitives is that they are recursive. A subagent is another instance of the primitives - it has its own context window, its own tools, its own skills, plugins, MCP, memory - bounded to a smaller task and isolated from the orchestrator's context.
```

- [ ] **Step 3: Line 339 — `all six` → `them all`**

Find `One more piece organizes all six.` Replace with `One more piece organizes them all.`

- [ ] **Step 4: Line 341 — `The six primitives all live` → `The primitives all live`**

Find `The six primitives all live inside the harness.` Replace with `The primitives all live inside the harness.`

- [ ] **Step 5: Line 345 — drop "six"**

Find `The middleware *is* the harness, *is* the six primitives, *is* what you are buying when you adopt an agent.` Replace with `The middleware *is* the harness, *is* the primitives, *is* what you are buying when you adopt an agent.`

- [ ] **Step 6: Line 349 — capability primitives expansion**

Find:

```
A note on vocabulary. The six primitives are capability primitives: what the agent uses to know, act, extend, integrate, and delegate. The governance mechanisms in Chapter 3 - permissions, sandboxing, hooks, telemetry - are not additional primitives. They are control layers around the primitives, especially around tools and subagents.
```

Replace with:

```
A note on vocabulary. The primitives named here are capability primitives: what the agent uses to know, act, extend, integrate, remember, and delegate. The governance mechanisms in Chapter 3 - permissions, sandboxing, hooks, telemetry - are not additional primitives. They are control layers around the primitives, especially around tools and subagents.
```

- [ ] **Step 7: Line 353 — closing list (list-led opener)**

Find:

```
Six primitives. Context window. Tools. Skills. Plugins. MCP. Subagents. Plus the harness as the runtime that organizes them.
```

Replace with:

```
Context window. Tools. Skills. Plugins. MCP. Memory. Subagents. Plus the harness as the runtime that organizes them. That is the list today. The set is open; expect it to grow. Memory was missing eighteen months ago and converged across the major agents within a six-month window. The next one will appear when the convergence appears, not before.
```

- [ ] **Step 8: Rebuild + verify all the sweeps landed**

```bash
python3 build/build_spa.py
python3 -c "
content = open('_site/chapter-1-primitives/index.html').read()
forbidden = ['other five primitives', 'five primitives - it', 'organizes all six', 'six primitives all live', 'is the six primitives', 'six primitives are capability', 'Six primitives. Context window']
hits = [p for p in forbidden if p in content]
assert not hits, f'forbidden phrasings still present: {hits}'
print('OK: chapter 1 forbidden phrasings all swept')
"
```

Expected: `OK: chapter 1 forbidden phrasings all swept`.

- [ ] **Step 9: Commit (deferred — bundled into Commit 1)**

---

## Task 7: Chapter 1 evaluation questions (lines 354, 357)

**Why:** Add the Memory question (split into two for operational clarity); keep a dated count on the closer.

**Files:**
- Modify: `source/Ship_It_With_AI.md` — lines 354, 357

- [ ] **Step 1: Locate**

```bash
grep -n "How does it expose subagents\|^Six questions\.\|How does it speak MCP" source/Ship_It_With_AI.md
```

Expected: lines 354 + 357.

- [ ] **Step 2: Line 354 — add memory questions in primitive order**

Find:

```
How big is the context window and how does the agent manage it under pressure? What tools are available and how are they constrained? How are skills implemented - always-loaded, or dispatched on detection? Is there a plugin marketplace and is it growing? Does it speak MCP, and how good is the MCP integration? How does it expose subagents - and is parallel dispatch a first-class operation or an afterthought?
```

Replace with (Memory inserted between MCP and subagents, as TWO questions):

```
How big is the context window and how does the agent manage it under pressure? What tools are available and how are they constrained? How are skills implemented - always-loaded, or dispatched on detection? Is there a plugin marketplace and is it growing? Does it speak MCP, and how good is the MCP integration? Does it read a team-shared memory file at session start? Does it maintain any agent-written learned memory across sessions? How does it expose subagents - and is parallel dispatch a first-class operation or an afterthought?
```

- [ ] **Step 3: Line 357 — keep a dated count**

Find `Six questions. They tell you almost everything you need to know to compare the new agent to the one you are using today.`

Replace with `Eight questions today; more tomorrow. They tell you almost everything you need to know to compare the new agent to the one you are using today.`

- [ ] **Step 4: Rebuild + verify**

```bash
python3 build/build_spa.py
grep -c "Eight questions today\|team-shared memory file\|agent-written learned memory" _site/chapter-1-primitives/index.html
grep -c "Six questions\." _site/chapter-1-primitives/index.html
```

Expected: first `>= 3` (all three new phrases present); second `0`.

- [ ] **Step 5: Commit (deferred — bundled into Commit 1)**

---

## Task 8: Chapter 1 figure caption (line 259)

**Files:**
- Modify: `source/Ship_It_With_AI.md` — line 259

- [ ] **Step 1: Locate + replace**

```bash
grep -n "^\*Figure: The six primitives" source/Ship_It_With_AI.md
```

Expected: line 259.

Find:

```
*Figure: The six primitives and the harness that runs them. Subagents are the recursive primitive: each subagent is itself an instance of the other five.*
```

Replace with:

```
*Figure: The primitives and the harness that runs them. Memory is the most recent primitive to converge across the major agents. Subagents sit below the line because they are the recursive primitive: each subagent is itself an instance of the others.*
```

- [ ] **Step 2: Verify**

```bash
python3 build/build_spa.py
grep -c "instance of the other five\|six primitives and the harness" _site/read/index.html
grep -c "Memory is the most recent primitive to converge" _site/read/index.html
```

Expected: first `0`; second `>= 1`.

- [ ] **Step 3: Commit (deferred — bundled into Commit 1)**

---

## Task 9: Chapter 1 diagram (`diagram_primitives()` + CSS)

**Why:** Memory takes the 6th cell of the grid; subagents lives below the grid in a full-width row with a thin divider above.

**Files:**
- Modify: `build/build_spa.py` — `diagram_primitives()` function (lines ~27-42)
- Modify: `build/spa_template.html` — add three new CSS rules in the critical CSS region

- [ ] **Step 1: Find the existing function**

```bash
grep -n "^def diagram_primitives\|primitives-grid\|primitive-recursive" build/build_spa.py
```

- [ ] **Step 2: Replace `diagram_primitives()`**

Edit `build/build_spa.py`. Replace the entire `diagram_primitives()` function with:

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

- [ ] **Step 3: Find the critical CSS region in the template**

```bash
grep -n "/* @region-end critical \*/\|\.primitives-grid\|\.primitive-recursive" build/spa_template.html
```

Locate the `.primitives-grid` rule (existing) and the critical-region end marker.

- [ ] **Step 4: Add the three new CSS rules**

In `build/spa_template.html`, immediately after the existing `.primitive-recursive` rule (or near the other `.primitive*` rules — anywhere inside the critical region works), insert:

```css
    .primitives-divider {
      height: 1px;
      background: var(--color-border);
      margin: 20px 0;
      width: 100%;
    }
    .primitives-recursive {
      display: flex;
      justify-content: center;
      margin-top: 4px;
    }
    .primitives-recursive .primitive {
      border-color: var(--color-border-strong);
      border-width: 1.5px;
      background: var(--color-surface);
      box-shadow: var(--shadow-sm);
    }
    .primitive-sublist {
      display: flex;
      flex-direction: column;
      gap: 2px;
      margin-top: 6px;
    }
    .primitive-sub {
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--color-text-muted);
      line-height: 1.2;
    }
```

(These reference CSS variables that already exist in the template's `:root` block per the feedback-pass work.)

- [ ] **Step 5: Rebuild + verify the new diagram renders**

```bash
python3 build/build_spa.py
grep -c "primitives-divider\|primitives-recursive\|primitive-sublist\|primitive-sub" _site/chapter-1-primitives/index.html
grep -c "primitive-memory" _site/chapter-1-primitives/index.html
grep -c "instance of the others" _site/chapter-1-primitives/index.html
```

Expected: first `>= 4`; second `>= 1`; third `>= 1`.

- [ ] **Step 6: Spot-check visually**

```bash
node build/tests/verify_seo_pass.js 2>&1 | tail -5
ls build/tests/screenshots/seo-pass/hero_desktop_light.png
```

The verify script regenerates hero screenshots. Open one in a browser to confirm the layout still looks right (the hero is unaffected; the diagram itself is inside Chapter 1's body which the existing screenshots don't capture — manual browser check at `/chapter-1-primitives/` recommended).

- [ ] **Step 7: Commit (deferred — bundled into Commit 1)**

---

## Task 10: JS redirect stub at old slug + `render_redirect_stub()`

**Why:** The renamed slug breaks any inbound link to `/chapter-1-six-primitives/`. Emit a small page that 0-second-redirects to the new URL with a canonical pointing forward.

**Files:**
- Modify: `build/build_spa.py` — new `render_redirect_stub()` function + call from `main()` + sitemap exclusion logic

- [ ] **Step 1: Add the renderer function**

In `build/build_spa.py`, near the other `render_*` helpers (e.g., near `render_404` or `render_sitemap`), add:

```python
def render_redirect_stub(old_slug: str, new_slug: str, new_title: str) -> str:
    """Emit a tiny redirect-stub HTML page at the old slug.

    Used when a chapter slug is renamed so inbound bookmarks don't dead-end.
    Combines meta-refresh (works without JS), location.replace (immediate
    in modern browsers), and a canonical pointing to the new URL so
    crawlers consolidate ranking.
    """
    new_url = f"/{new_slug}/"
    new_url_absolute = f"https://ship-it-with.ai{new_url}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Moved - {new_title}</title>
  <link rel="canonical" href="{new_url_absolute}">
  <meta http-equiv="refresh" content="0; url={new_url}">
  <meta name="robots" content="noindex, follow">
  <script>location.replace('{new_url}');</script>
</head>
<body>
  <p>This page has moved to <a href="{new_url}">{new_url}</a>.</p>
</body>
</html>
"""
```

- [ ] **Step 2: Call it from `main()` after per-chapter rendering**

Find the place in `main()` where the per-chapter loop ends (search for `Wrote {len(sections)} chapter pages`). Immediately after that loop, add:

```python
    # Renamed-slug redirect stubs: old slug -> new slug.
    # Memory primitive pass (2026-05-27): chapter-1-six-primitives -> chapter-1-primitives.
    redirect_stubs = [
        ("chapter-1-six-primitives", "chapter-1-primitives", "The primitives"),
    ]
    for old_slug, new_slug, new_title in redirect_stubs:
        dest = SITE_DIR / old_slug
        dest.mkdir(exist_ok=True)
        (dest / "index.html").write_text(render_redirect_stub(old_slug, new_slug, new_title))
    if redirect_stubs:
        print(f"Wrote {len(redirect_stubs)} redirect stub(s)")
```

- [ ] **Step 3: Exclude old slugs from sitemap**

Find `render_sitemap` in `build/build_spa.py`. It currently lists every section slug. Before generating, filter out the old slugs:

```python
def render_sitemap(sections: list[Section]) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Slugs renamed in earlier passes — old URLs serve as redirect stubs,
    # not as canonical URLs. Exclude from sitemap so Google doesn't index them.
    REDIRECTED_OLD_SLUGS = {"chapter-1-six-primitives"}

    urls = ["https://ship-it-with.ai/", "https://ship-it-with.ai/read/"]
    urls += [
        f"https://ship-it-with.ai/{s.slug}/"
        for s in sections
        if s.slug not in REDIRECTED_OLD_SLUGS
    ]
    body = "\n".join(
        f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>' for u in urls
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
'''
```

(The filter is defensive — since the SECTION_SLUGS rename means the parser never produces the old slug, but this guards against future renames.)

- [ ] **Step 4: Rebuild + verify the stub lands**

```bash
python3 build/build_spa.py
ls _site/chapter-1-six-primitives/index.html
cat _site/chapter-1-six-primitives/index.html | head -10
grep -c "chapter-1-six-primitives" _site/sitemap.xml
grep -c "chapter-1-primitives" _site/sitemap.xml
```

Expected: stub file exists; cat shows the meta-refresh page; sitemap count for old slug = `0`; sitemap count for new slug = `1` (just the chapter URL — no `six-primitives` substring elsewhere).

- [ ] **Step 5: Verify the redirect chain via HTTP**

```bash
python3 -m http.server -d _site 8765 > /dev/null 2>&1 &
sleep 1
curl -sI http://localhost:8765/chapter-1-six-primitives/ | head -5
curl -s http://localhost:8765/chapter-1-six-primitives/ | grep -E "meta http-equiv|canonical|location\.replace"
kill %1
```

Expected: 200 status; the body contains all three redirect mechanisms (meta-refresh, canonical link, JS location.replace).

- [ ] **Step 6: Commit (deferred — bundled into Commit 1)**

---

## Task 11: Foreword line 161 + line 287 (tech-debt pickup)

**Files:**
- Modify: `source/Ship_It_With_AI.md` — line 161 (Foreword), line 287 (Chapter 1 / existing AGENTS.md vs CLAUDE.md imprecision)

- [ ] **Step 1: Line 161 — redraft Foreword**

```bash
grep -n "If a future agent ships without something that maps" source/Ship_It_With_AI.md
```

Expected: line 161.

Find the sentence ending in `...I missed an invariant that I thought was structural.`. Replace the entire sentence (just that one sentence) with:

```
The primitives are an open set. Memory was missing from the original list eighteen months ago; the major agents converged on it within a six-month window. If a future agent ships without a mechanism that maps to one of the primitives, I missed an invariant I thought was structural. If a new primitive emerges, the list grows.
```

- [ ] **Step 2: Line 287 — fix the pre-existing Claim 5 imprecision**

```bash
grep -n "the always-loaded primitive has converged on two names" source/Ship_It_With_AI.md
```

Expected: line 287.

Find:

```
The implementation of skills varies between agents in file names and loading semantics, but the underlying primitive is now shared across the major agents. The always-loaded primitive has converged on two names: the vendor-neutral [AGENTS.md](https://agents.md/), supported by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider ecosystem; and CLAUDE.md, the Claude Code-specific variant. Both are markdown files at the project root, both load at session start, both serve the same role.
```

Replace with:

```
The implementation of skills varies between agents in file names and loading semantics, but the underlying primitive is now shared across the major agents. The always-loaded primitive has converged on two filenames: the vendor-neutral [AGENTS.md](https://agents.md/), supported by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider ecosystem; and CLAUDE.md, which Claude Code reads natively. The two are interoperable - Claude Code can import AGENTS.md into CLAUDE.md so the team's content lives in one place across vendors. Both load at session start, both serve the same role.
```

- [ ] **Step 3: Rebuild + verify both edits**

```bash
python3 build/build_spa.py
grep -c "If a future agent ships without a mechanism that maps" _site/read/index.html
grep -c "which Claude Code reads natively\|interoperable - Claude Code can import" _site/read/index.html
grep -c "If a future agent ships without something that maps\|CLAUDE.md, the Claude Code-specific variant" _site/read/index.html
```

Expected: first `>= 1`; second `>= 1`; third `0`.

- [ ] **Step 4: Commit (deferred — bundled into Commit 1)**

---

## Task 12: Chapter 2 sweep (lines 406, 411, 412, 415, 428, 446-447, 449, 480, 484)

**Why:** Chapter 2's case-note + inspection sequence + Ship-this-week all reference the six count.

**Files:**
- Modify: `source/Ship_It_With_AI.md` — lines 406, 411, 412, 415, 428, 446-447, 449, 480, 484

- [ ] **Step 1: Locate all the lines**

```bash
grep -n "two-agent demo, six primitives\|six primitives were not\|identifies the six primitives\|Same six primitives present\|six primitives plus the way\|locate the permission gate\|^Eight inspection points\|name the six primitives\|The six primitives, the diagnostic" source/Ship_It_With_AI.md
```

Expected: approximately the lines above.

- [ ] **Step 2: Line 406 — case-note title**

Find:

```
**Case note: the two-agent demo, six primitives observable in both.**
```

Replace with:

```
**Case note: the two-agent demo, the primitives observable in both.**
```

- [ ] **Step 3: Lines 411, 412, 415 — case-note table cells**

Find each occurrence in the case-note table and rewrite:

- `the six primitives were not Claude-Code-specific marketing` → `the primitives were not Claude-Code-specific marketing`
- `agent identifies the six primitives in each codebase` → `agent identifies the primitives in each codebase`
- `Same six primitives present in both codebases` → `Same primitives present in both codebases`

- [ ] **Step 4: Line 428 — harness phrasing**

Find `The harness is the six primitives plus the way they are organized` → replace `The harness is the primitives plus the way they are organized`.

- [ ] **Step 5: Lines 446-447 — inspection sequence**

Find:

```
You open its repository. You locate context assembly. You locate the tool registry. You locate skills loading. You locate plugin extension. You check for MCP support. You locate subagent dispatch. You locate the permission gate. You locate the sandbox - all wrapped by the harness's agent loop.
```

Replace with:

```
You open its repository. You locate context assembly. You locate the tool registry. You locate skills loading. You locate plugin extension. You check for MCP support. You locate the memory layer (AGENTS.md or equivalent; any auto-memory surface the vendor exposes). You locate subagent dispatch. You locate the permission gate. You locate the sandbox - all wrapped by the harness's agent loop.
```

- [ ] **Step 6: Line 449 — inspection summary (keep dated count, bumped to 9)**

Find:

```
Eight inspection points: context assembly, tool registry, skills loading, plugin extension, MCP support, subagent dispatch, permission gate, sandbox - all wrapped by the harness's agent loop.
```

Replace with:

```
Nine inspection points: context assembly, tool registry, skills loading, plugin extension, MCP support, memory layer, subagent dispatch, permission gate, sandbox - all wrapped by the harness's agent loop.
```

- [ ] **Step 7: Locate the artifact callout that also mentions the eight inspection points**

```bash
grep -n "Source-inspection checklist\|eight inspection points from this chapter" source/Ship_It_With_AI.md
```

Find the artifact-callout sentence:

```
**Artifact: Source-inspection checklist.** The eight inspection points from this chapter. Use the checklist on the next agent that lands in your team's evaluation queue.
```

Replace with:

```
**Artifact: Source-inspection checklist.** The nine inspection points from this chapter. Use the checklist on the next agent that lands in your team's evaluation queue.
```

- [ ] **Step 8: Line 480 — Ship-this-week**

Find `Walk this codebase and name the six primitives - context window, tools, skills, plugins, MCP, subagents.` Replace with `Walk this codebase and name the primitives - context window, tools, skills, plugins, MCP, memory, subagents.`

- [ ] **Step 9: Line 484 — Try-it-yourself**

Find `The six primitives, the diagnostic, and what the diagnostic tells you about governance will be.` Replace with `The primitives, the diagnostic, and what the diagnostic tells you about governance will be.`

- [ ] **Step 10: Rebuild + verify Chapter 2 sweep**

```bash
python3 build/build_spa.py
python3 -c "
content = open('_site/chapter-2-anatomy-invariant/index.html').read()
forbidden = ['two-agent demo, six primitives observable', 'six primitives were not Claude-Code', 'identifies the six primitives in each', 'Same six primitives present', 'six primitives plus the way', 'Eight inspection points:', 'eight inspection points from this chapter', 'name the six primitives - context window', 'The six primitives, the diagnostic']
hits = [p for p in forbidden if p in content]
assert not hits, f'forbidden phrasings still present: {hits}'
print('OK: chapter 2 forbidden phrasings all swept')
# positive markers
assert 'Nine inspection points:' in content, 'missing positive marker'
assert 'nine inspection points from this chapter' in content, 'missing positive marker'
assert 'name the primitives - context window' in content, 'missing positive marker'
print('OK: chapter 2 positive markers present')
"
```

Expected: both `OK` messages.

- [ ] **Step 11: Commit (deferred — bundled into Commit 1)**

---

## Task 13: Chapter 5 line 858

**Files:**
- Modify: `source/Ship_It_With_AI.md` — line 858

- [ ] **Step 1: Locate + replace**

```bash
grep -n "sixth primitive from Chapter 1" source/Ship_It_With_AI.md
```

Expected: line 858.

Find:

```
This is where the sixth primitive from Chapter 1 - subagents - earns its keep. Execute is the phase where the orchestrator dispatches multiple constrained children, each working on a bounded task in its own isolated context.
```

Replace with:

```
This is where the recursive primitive from Chapter 1 - subagents - earns its keep. Execute is the phase where the orchestrator dispatches multiple constrained children, each working on a bounded task in its own isolated context.
```

- [ ] **Step 2: Rebuild + verify**

```bash
python3 build/build_spa.py
grep -c "sixth primitive from Chapter 1" _site/read/index.html
grep -c "recursive primitive from Chapter 1 - subagents - earns" _site/read/index.html
```

Expected: first `0`; second `>= 1`.

- [ ] **Step 3: Commit (deferred — bundled into Commit 1)**

---

## Task 14: Closing line 1882

**Files:**
- Modify: `source/Ship_It_With_AI.md` — line 1882

- [ ] **Step 1: Locate + replace**

```bash
grep -n "The architecture you learned in Part I is invariant" source/Ship_It_With_AI.md
```

Expected: line 1882.

Find the paragraph containing:

```
The architecture you learned in Part I is invariant. The six primitives - context window, tools, skills, plugins, MCP, subagents - plus the harness that organizes them. Most production-grade coding agents converge on this anatomy. The coding agents that emerge in the next decade will, in most cases, take a similar shape, because the anatomy is determined by the work, not by the vendor. When you evaluate a new agent, you walk down the list, ask the six questions, and you have your answer.
```

Replace with:

```
The architecture you learned in Part I is invariant. The primitives - context window, tools, skills, plugins, MCP, memory, subagents - plus the harness that organizes them. Most production-grade coding agents converge on this anatomy. The coding agents that emerge in the next decade will, in most cases, take a similar shape, because the anatomy is determined by the work, not by the vendor. When you evaluate a new agent, you walk down the list, ask the question for each primitive, and you have your answer. The list is open; new primitives will appear as the major agents converge on new mechanisms.
```

- [ ] **Step 2: Rebuild + verify**

```bash
python3 build/build_spa.py
grep -c "six primitives - context window, tools, skills, plugins, MCP, subagents - plus the harness" _site/read/index.html
grep -c "The list is open; new primitives will appear" _site/read/index.html
```

Expected: first `0`; second `>= 1`.

- [ ] **Step 3: Commit (deferred — bundled into Commit 1)**

---

## Task 15: Appendix C cross-reference labels + line 2311

**Files:**
- Modify: `source/Ship_It_With_AI.md` — line 2311 + every `Chapter 1 (Six primitives)` cross-reference label

- [ ] **Step 1: Find all Appendix C label occurrences**

```bash
grep -n "Chapter 1 (Six primitives)\|same six primitives this manual identifies" source/Ship_It_With_AI.md
```

Note all the line numbers. Spec says ~7-8 entries (lines 2285, 2292, 2299, 2306, 2313, 2334, 2343-2344 — verify with this grep).

- [ ] **Step 2: Bulk-rewrite the labels**

Using sed or your editor, change every occurrence of:

```
Chapter 1 (Six primitives)
```

to:

```
Chapter 1 (The primitives)
```

Concrete invocation if you want to use sed:

```bash
sed -i 's/Chapter 1 (Six primitives)/Chapter 1 (The primitives)/g' source/Ship_It_With_AI.md
```

- [ ] **Step 3: Line 2311 — text body**

Find:

```
Source-organized around the same six primitives this manual identifies in Codex CLI and Claude Code.
```

Replace with:

```
Source-organized around the same primitives this manual identifies in Codex CLI and Claude Code.
```

- [ ] **Step 4: Rebuild + verify Appendix C sweep**

```bash
python3 build/build_spa.py
grep -c "Chapter 1 (Six primitives)\|same six primitives this manual identifies" _site/appendix-c-sources/index.html
grep -c "Chapter 1 (The primitives)" _site/appendix-c-sources/index.html
```

Expected: first `0`; second `>= 5` (one per old occurrence).

- [ ] **Step 5: Commit (deferred — bundled into Commit 1)**

---

## Task 16: Verify script Commit 1 assertions

**Files:**
- Modify: `build/tests/verify_seo_pass.js`

- [ ] **Step 1: Find the SLUGS list**

```bash
grep -n "chapter-1-six-primitives\|SLUGS\|const SLUGS" build/tests/verify_seo_pass.js
```

- [ ] **Step 2: Update the SLUGS list**

Find the hardcoded SLUGS array (~around line 280-300 in the existing verify script). Change `'chapter-1-six-primitives'` to `'chapter-1-primitives'`.

- [ ] **Step 3: Add Commit 1 assertions**

Locate the "Commit 3 assertions" block from the SEO pass (this becomes the natural extension point — the new assertions land alongside). Insert a new block:

```javascript
// ===== Memory primitive + open-set pass assertions =====

// 1. Slug rename: old URL serves a redirect stub, new URL serves the chapter.
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();

  const stubResp = await page.goto(`${baseUrl}/chapter-1-six-primitives/`);
  if (!stubResp || stubResp.status() !== 200) fail(`old slug status ${stubResp && stubResp.status()}`);
  const stubHtml = await page.content();
  if (!/meta http-equiv="refresh"/i.test(stubHtml)) fail('old slug missing meta refresh');
  if (!/canonical[^>]*href="https:\/\/ship-it-with\.ai\/chapter-1-primitives\/"/.test(stubHtml)) fail('old slug missing canonical to new');
  ok('old slug serves redirect stub with canonical + meta refresh');

  const newResp = await page.goto(`${baseUrl}/chapter-1-primitives/`);
  if (!newResp || newResp.status() !== 200) fail(`new slug status ${newResp && newResp.status()}`);
  const h1 = await page.locator('h1').first().textContent();
  if (h1.trim() !== 'The primitives') fail(`new slug H1: got "${h1}", expected "The primitives"`);
  else ok('new slug H1 is "The primitives"');

  await ctx.close();
}

// 2. Sitemap excludes old slug, includes new slug.
{
  const sitemap = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
  if (sitemap.includes('chapter-1-six-primitives')) fail('sitemap still lists old slug');
  else ok('sitemap excludes old slug');
  if (!sitemap.includes('chapter-1-primitives')) fail('sitemap missing new slug');
  else ok('sitemap includes new slug');
}

// 3. Hash redirect map: /#chapter-1 lands on new URL.
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/#chapter-1`);
  await page.waitForURL(/chapter-1-primitives/, { timeout: 2000 }).catch(() => {});
  const url = page.url();
  if (!url.includes('/chapter-1-primitives/')) fail(`hash-redirect: landed at ${url}`);
  else ok('hash-redirect /#chapter-1 → /chapter-1-primitives/');
  await ctx.close();
}

// 4. Global content sweep — count-anchored phrasings must be 0 in /read/.
{
  const readHtml = fs.readFileSync(path.join(repoRoot, '_site', 'read', 'index.html'), 'utf8');
  const forbidden = [
    'six primitives', 'sixth primitive', 'the other five', 'five primitives',
    'five capabilities', 'six conceptual', 'Six questions', 'Eight inspection points'
  ];
  // "six-phase loop" / "all six phases" are explicit exceptions (Chapter 5 methodology).
  for (const phrase of forbidden) {
    // Filter out the six-phase-loop matches if checking against "six".
    if (phrase === 'six primitives' || phrase === 'sixth primitive' || phrase === 'six conceptual') {
      // Strict phrase match — these never appear in six-phase loop context.
      if (readHtml.includes(phrase)) fail(`/read/ still contains "${phrase}"`);
    } else {
      if (readHtml.includes(phrase)) fail(`/read/ still contains "${phrase}"`);
    }
  }
  ok('/read/ contains zero forbidden count-anchored phrasings');
}

// 5. Positive markers in /read/.
{
  const readHtml = fs.readFileSync(path.join(repoRoot, '_site', 'read', 'index.html'), 'utf8');
  const required = [
    'Eight questions today',
    'Nine inspection points',
    'auto-memory system',
    'early-mover signal',
    'which Claude Code reads natively',
    'manually defined memory',
    'The primitives are an open set',
  ];
  for (const phrase of required) {
    if (!readHtml.includes(phrase)) fail(`/read/ missing positive marker "${phrase}"`);
  }
  ok('/read/ contains all positive markers');
}

// 6. Chapter 1 has the new diagram structure.
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/chapter-1-primitives/`);
  const dividerCount = await page.locator('.primitives-divider').count();
  const recursiveCount = await page.locator('.primitives-recursive .primitive').count();
  const sublistCount = await page.locator('.primitive-sublist').count();
  if (dividerCount < 1) fail('chapter-1 diagram missing .primitives-divider');
  if (recursiveCount < 1) fail('chapter-1 diagram missing .primitives-recursive .primitive');
  if (sublistCount < 1) fail('chapter-1 diagram missing .primitive-sublist (Memory cell)');
  if (dividerCount && recursiveCount && sublistCount) ok('chapter-1 diagram has divider + recursive row + Memory sublist');
  await ctx.close();
}

// 7. TOC entry on landing.
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/`);
  const tocText = await page.locator('a[href="/chapter-1-primitives/"]').first().textContent();
  if (!/The primitives/i.test(tocText || '')) fail(`landing TOC entry: ${tocText}`);
  else ok('landing TOC entry reads "The primitives"');
  await ctx.close();
}
```

- [ ] **Step 4: Run verify**

```bash
node build/tests/verify_seo_pass.js 2>&1 | tail -40
```

Expected: `Verification PASSED.` with all new assertions printing `OK:` lines.

- [ ] **Step 5: COMMIT COMMIT 1**

```bash
git status
git add source/Ship_It_With_AI.md build/build_spa.py build/spa_template.html build/tests/verify_seo_pass.js index.html 2>/dev/null || true
# index.html at repo root is gone post-SEO; only seo-pass branch had it. Don't worry if `git add` skips it.
git add source/Ship_It_With_AI.md build/build_spa.py build/spa_template.html build/tests/verify_seo_pass.js
git commit -m "feat: memory primitive + open-set framing — chapter 1 rewrite + book-wide sweep

Chapter 1 renamed: \"Six primitives\" → \"The primitives\". Slug renamed:
/chapter-1-six-primitives/ → /chapter-1-primitives/ with JS+meta-refresh
redirect stub at the old URL. Structural argument rewritten from
\"five local + one recursive\" to \"most local; one (subagents) recursive\".
New Memory section between MCP and Subagents with two halves: manually
defined memory (agent-agnostic) and auto-memory system (Claude-Code-led,
early-mover signal). Diagram updated: 2x3 grid keeps named primitives;
subagents sits below a thin divider in a full-width row. Cross-book
sweep of all count-anchored references (~25 lines across Foreword,
Chapter 1, Chapter 2, Chapter 5, Closing, Appendix C, TOC). Pre-existing
Claim 5 imprecision on line 287 fixed in the same sweep (Claude Code
reads CLAUDE.md; AGENTS.md interop is via @AGENTS.md import).
Operational counts kept and dated (\"Eight questions today; more
tomorrow\", \"Nine inspection points\") per reader-experience review.
Verify script extended with redirect-stub, sitemap-exclusion,
hash-redirect, content-sweep, positive-marker, and diagram-structure
assertions."
```

---

# COMMIT 2 — Chapter 6 intro + Appendix C entries

## Task 17: Chapter 6 framing intro paragraph

**Files:**
- Modify: `source/Ship_It_With_AI.md` — prepend new opening paragraph to Chapter 6 body

- [ ] **Step 1: Find Chapter 6's first body paragraph**

```bash
grep -n "^## Chapter 6\|^## AGENTS.md as team\|^I was sitting with\|^Six months in\|^A senior engineer at" source/Ship_It_With_AI.md | head -10
```

Locate the very first prose paragraph of Chapter 6's body (after the `## AGENTS.md as team infrastructure` heading).

- [ ] **Step 2: Insert the framing intro**

Insert a new paragraph as the chapter's opening (before the existing first body paragraph), separated by a blank line:

```markdown
AGENTS.md is the manually defined layer of the Memory primitive named in Chapter 1. It is the team-shareable surface - the layer the team authors, reviews, and owns in source control, as infrastructure the team owns. The auto-memory system (Auto Memory, Auto Dream) is per-developer and largely automatic; this chapter focuses on the layer the team explicitly owns, because that is where team-level discipline lives. What follows is six things that go in AGENTS.md, the 200-line budget rule, and the failure modes you see in practice.

---

```

(The trailing `---` plus blank line follows the source's existing section-separator pattern.)

- [ ] **Step 3: Rebuild + verify**

```bash
python3 build/build_spa.py
grep -c "manually defined layer of the Memory primitive named in Chapter 1" _site/chapter-6-agents-md/index.html
```

Expected: `>= 1`.

- [ ] **Step 4: Commit (deferred — bundled into Commit 2)**

---

## Task 18: Appendix C — three new entries

**Why:** The book's citation discipline requires sourcing the new Memory claims.

**Files:**
- Modify: `source/Ship_It_With_AI.md` — append three new entries to Appendix C

- [ ] **Step 1: Find the Appendix C structure**

```bash
grep -n "^## Appendix C\|^### " source/Ship_It_With_AI.md | grep -A 5 "Appendix C"
```

Locate the existing Appendix C subsections (e.g., "Vendor documentation", "Industry standards", etc.). The three new entries should go in a logical group — likely create a new "Memory primitive sources" subsection at the END of Appendix C, OR slot them into the existing "Standards and conventions" subsection.

- [ ] **Step 2: Insert the three entries**

If creating a new subsection, append at the end of Appendix C (before the next top-level heading, which is About-the-author):

```markdown
### Memory primitive sources

#### AGENTS.md as cross-vendor standard

**Claim:** AGENTS.md is read at session start by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider open-source coding-agent ecosystem (20+ vendors listed at agents.md as of 2026-05). Claude Code reads CLAUDE.md, which can import AGENTS.md to share the same content with other agents. The convergence puts AGENTS.md in the manually defined memory layer of the Memory primitive named in Chapter 1.

**Source:** [agents.md](https://agents.md/) (the open standard's site), plus vendor documentation for each agent listed.

**Where used:** Chapter 1 (The primitives, Memory section) and Chapter 6 (AGENTS.md as team infrastructure).

**Caveat:** The exact filename and load semantics vary by vendor - Claude Code reads CLAUDE.md (importable from AGENTS.md via `@AGENTS.md` or symlink); Cursor reads AGENTS.md plus `.cursorrules`. Convergence is on the structural role - user-written, always-loaded, team-shareable - not on byte-identical file format.

---

#### Claude Code Auto Memory

**Claim:** Claude Code maintains an auto-memory layer in which Claude writes notes for itself across sessions - build commands it figured out, debugging insights it confirmed, code-style preferences it inferred - distinct from the user-written CLAUDE.md. Requires Claude Code v2.1.59+; on by default; per-repo storage.

**Source:** [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).

**Where used:** Chapter 1 (The primitives, Memory section).

**Caveat:** Auto memory is Claude-Code-specific at the time of writing. Other coding agents are converging on similar mechanisms but had not shipped an equivalent at publication date.

---

#### Auto Dream (Anthropic background memory consolidation)

**Claim:** Anthropic publicly unveiled Dreaming as part of Claude Managed Agents at Code with Claude SF on 2026-05-06 - a scheduled background process that reviews recent sessions and the memory store, identifies recurring mistakes and convergent workflows, and writes consolidated notes back into long-term memory. The Claude Code surface (`Auto Dream`, accessible via `/dream`) shipped earlier as a research preview gated behind developer access and was documented in March 2026.

**Source:** Code with Claude SF announcement, 2026-05-06; [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).

**Where used:** Chapter 1 (The primitives, Memory section).

**Caveat:** Auto Dream is Claude-Code-specific at publication date. The structural role is what this manual indexes, not the vendor.

---

```

- [ ] **Step 3: Rebuild + verify the three entries**

```bash
python3 build/build_spa.py
grep -c "AGENTS.md as cross-vendor standard\|Claude Code Auto Memory\|Auto Dream (Anthropic background" _site/appendix-c-sources/index.html
grep -c "Code with Claude SF\|code\.claude\.com/docs/en/memory\|agents\.md" _site/appendix-c-sources/index.html
```

Expected: first `>= 3`; second `>= 3` (each of the three sources cited at least once).

- [ ] **Step 4: Verify each entry has the Claim/Source/Where used/Caveat structure**

```bash
python3 -c "
content = open('_site/appendix-c-sources/index.html').read()
# Each new entry should have all four labels in proximity
for heading in ['AGENTS.md as cross-vendor standard', 'Claude Code Auto Memory', 'Auto Dream (Anthropic background']:
    idx = content.find(heading)
    assert idx >= 0, f'missing entry: {heading}'
    section = content[idx:idx+2500]
    for label in ['<strong>Claim:</strong>', '<strong>Source:</strong>', '<strong>Where used:</strong>', '<strong>Caveat:</strong>']:
        assert label in section, f'entry \"{heading}\" missing label {label}'
print('OK: all 3 new Appendix C entries have full Claim/Source/Where used/Caveat structure')
"
```

Expected: `OK: all 3 new Appendix C entries have full Claim/Source/Where used/Caveat structure`.

- [ ] **Step 5: Commit (deferred — bundled into Commit 2)**

---

## Task 19: Verify script Commit 2 assertions + final commit

**Files:**
- Modify: `build/tests/verify_seo_pass.js`

- [ ] **Step 1: Add Commit 2 assertions**

Inside the verify script's main run block, add after the Commit 1 (memory pass) assertions:

```javascript
// ===== Memory primitive — Commit 2 assertions (Chapter 6 + Appendix C) =====

// 8. Chapter 6 framing intro paragraph.
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/chapter-6-agents-md/`);
  const body = await page.locator('main').textContent();
  if (!/manually defined layer of the Memory primitive named in Chapter 1/.test(body || '')) {
    fail('chapter-6 missing Memory framing intro paragraph');
  } else ok('chapter-6 framing intro present');
  await ctx.close();
}

// 9. Appendix C three new entries.
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${baseUrl}/appendix-c-sources/`);
  const body = await page.locator('main').textContent() || '';
  const required_entries = [
    'AGENTS.md as cross-vendor standard',
    'Claude Code Auto Memory',
    'Auto Dream',
  ];
  for (const heading of required_entries) {
    if (!body.includes(heading)) fail(`appendix-c missing entry "${heading}"`);
  }
  if (!body.includes('Code with Claude SF')) fail('appendix-c missing Auto Dream attribution');
  if (process.exitCode !== 1) ok('appendix-c has all 3 new entries with correct sources');
  await ctx.close();
}
```

- [ ] **Step 2: Run the full verify script**

```bash
node build/tests/verify_seo_pass.js 2>&1 | tail -40
```

Expected: `Verification PASSED.` with all new Commit 2 assertions printing `OK:` lines.

- [ ] **Step 3: COMMIT COMMIT 2**

```bash
git status
git add source/Ship_It_With_AI.md build/tests/verify_seo_pass.js
git commit -m "feat: chapter 6 framing intro + appendix C memory sources

Chapter 6 prepended with a one-paragraph intro anchoring AGENTS.md as
the manually defined layer of the Memory primitive named in Chapter 1.
Three new Appendix C entries source the load-bearing Memory claims:
AGENTS.md cross-vendor standard (agents.md), Claude Code Auto Memory
(code.claude.com/docs/en/memory), and Auto Dream (Code with Claude SF
2026-05-06 + the earlier quieter Claude Code rollout). All three use
the existing claim/source/where-used/caveat structure. Verify script
extended with chapter-6 intro and appendix-c entry assertions."
```

---

## Task 20: Final verification + screenshots + PR

- [ ] **Step 1: Clean run**

```bash
rm -rf build/tests/screenshots/seo-pass _site
node build/tests/verify_seo_pass.js 2>&1 | tail -50
```

Expected: `Verification PASSED.` with all assertions OK (existing SEO + new memory pass).

- [ ] **Step 2: Walk the site manually**

```bash
python3 -m http.server -d _site 8765 > /dev/null 2>&1 &
sleep 1
```

In a browser, open and inspect:

- `http://localhost:8765/` — landing TOC should show "Chapter 1 — The primitives" (not "Six primitives")
- `http://localhost:8765/chapter-1-primitives/` — H1 reads "The primitives"; Memory section present; diagram has 6-cell grid + thin divider + subagents below
- `http://localhost:8765/chapter-1-six-primitives/` — redirect stub serves; should immediately replace the URL with `/chapter-1-primitives/` in browser
- `http://localhost:8765/chapter-2-anatomy-invariant/` — case-note title reads "the primitives observable in both"; "Nine inspection points"
- `http://localhost:8765/chapter-6-agents-md/` — opening paragraph mentions "manually defined layer of the Memory primitive named in Chapter 1"
- `http://localhost:8765/appendix-c-sources/` — three new entries visible at the end
- `http://localhost:8765/#chapter-1` — hash-redirect lands on `/chapter-1-primitives/`

Kill server: `kill %1`.

- [ ] **Step 3: Eyeball the hero screenshots**

```bash
ls build/tests/screenshots/seo-pass/
```

The verify-script regen produces fresh hero shots. Spot-check `hero_desktop_light.png` — landing visually unchanged (the memory work is in chapter body, not hero).

- [ ] **Step 4: Push and prepare PR**

```bash
git push -u origin memory-primitive
```

Then either run `gh pr create ...` (if your gh CLI has CreatePullRequest perm) or open the PR via:

`https://github.com/ro-ai-labs/ship-it-with-ai/compare/main...memory-primitive`

PR title: `Memory primitive + open-set framing: chapter 1 rewrite + book-wide sweep`

PR body (copy-paste):

```markdown
## Summary

Retroactively adds **Memory** as a named primitive across the book, drops the closed "six" count for an open-set framing, and rewrites Chapter 1's structural argument. Driven by the parallel workshop spec promoting Memory across the workshop chain; this PR applies the same reframing to the book.

### Commit 1 — Chapter 1 + book-wide sweep
- Chapter 1 renamed: "Six primitives" → "The primitives". Slug `/chapter-1-six-primitives/` → `/chapter-1-primitives/` with JS+meta-refresh redirect stub at the old URL.
- New Memory section between MCP and Subagents (two halves: manually defined memory, agent-agnostic; auto-memory system, Claude-Code-led early-mover signal).
- Structural argument: "most local; one (subagents) recursive" replaces "five local + one recursive".
- Diagram: keep 2x3 grid for named primitives; subagents lives below a thin divider in a full-width row (synthesizes reader + argument reviewer feedback).
- Cross-book sweep: ~25 count-anchored lines across Foreword, Chapter 1, Chapter 2, Chapter 5, Closing, Appendix C, TOC.
- Operational counts kept and dated ("Eight questions today; more tomorrow", "Nine inspection points") per reader-experience review.
- Pre-existing Claim 5 imprecision on line 287 of the published manual fixed in the same sweep (Claude Code reads CLAUDE.md natively; AGENTS.md interop is via `@AGENTS.md` import).

### Commit 2 — Chapter 6 intro + Appendix C
- Chapter 6 prepended with a one-paragraph intro anchoring AGENTS.md as the manually defined layer of the Memory primitive named in Chapter 1.
- Three new Appendix C entries: AGENTS.md as cross-vendor standard (agents.md), Claude Code Auto Memory (code.claude.com/docs/en/memory), Auto Dream (Code with Claude SF 2026-05-06 + the earlier Claude Code rollout). All use the existing claim/source/where-used/caveat structure.

## Verification

`build/tests/verify_seo_pass.js` extended with: redirect-stub assertion, sitemap exclusion, hash-redirect, content sweep (no `six primitives` / `Six questions` / `Eight inspection points`), positive markers (`Eight questions today`, `Nine inspection points`, `auto-memory system`, `early-mover signal`, etc.), diagram structure (`.primitives-divider`, `.primitives-recursive`, `.primitive-sublist`), Chapter 6 intro, Appendix C entries. All passing.

## Spec & plan
- Spec: `docs/superpowers/specs/2026-05-27-memory-primitive-and-open-set-design.md`
- Plan: `docs/superpowers/plans/2026-05-27-memory-primitive-and-open-set.md`

## Test plan
- [x] `node build/tests/verify_seo_pass.js` passes
- [x] Manual walk: landing, /chapter-1-primitives/, /chapter-1-six-primitives/ (stub), /chapter-2-anatomy-invariant/, /chapter-6-agents-md/, /appendix-c-sources/, /#chapter-1 (hash-redirect)
- [ ] Reviewer eyeballs a chapter or two
- [ ] CI rebuilds and deploys on merge

## Out of scope (deliberate)
- Restructuring Chapter 6 around all four memory layers (three of four aren't team-level).
- Dedicated "Boundary primitives" section (hooks/LSPs would have contradicted line 349; the open-set framing carries it).
- "Six-phase loop" in Chapter 5 (different "six", intentionally counted).
- "Six things go in AGENTS.md" structure in Chapter 6 (orthogonal to primitive count).
```

CI rebuilds the `_site/` tree from source and deploys to ship-it-with.ai on merge.

---

## Self-review (run by the engineer before opening the PR)

**Spec coverage:**
- [x] Chapter 1 heading + slug rename → Tasks 2, 3
- [x] Chapter 1 structural argument rewrite → Task 4
- [x] Memory section (two halves, asymmetry named) → Task 5
- [x] Chapter 1 subagents + harness sweep → Task 6
- [x] Chapter 1 evaluation questions (Memory split into 2, dated count) → Task 7
- [x] Chapter 1 figure caption → Task 8
- [x] Diagram (`diagram_primitives()` + CSS) → Task 9
- [x] JS redirect stub at old slug → Task 10
- [x] Foreword 161 + line 287 tech debt → Task 11
- [x] Chapter 2 sweep (case-note, inspection sequence, artifact, Ship-this-week, Try-it-yourself) → Task 12
- [x] Chapter 5 line 858 → Task 13
- [x] Closing line 1882 → Task 14
- [x] Appendix C label sweep + line 2311 → Task 15
- [x] Verify Commit 1 assertions → Task 16
- [x] Chapter 6 intro paragraph → Task 17
- [x] Appendix C three new entries → Task 18
- [x] Verify Commit 2 assertions → Task 19
- [x] Final verification + screenshots + PR → Task 20

**Files touched (verify no orphans):**
- `source/Ship_It_With_AI.md` — Tasks 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 17, 18
- `build/build_spa.py` — Tasks 2, 9, 10
- `build/spa_template.html` — Task 9
- `build/tests/verify_seo_pass.js` — Tasks 16, 19
