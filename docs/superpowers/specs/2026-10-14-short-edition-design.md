# Short edition - design

Date: 2026-10-14. Branch: `short-edition`.

## Why

The manual is ~58.7k words (~53k on the reading path, Foreword through Closing). Readers of the target
generation will not sit through that. A six-agent review (five per-part reviewers plus an editor-in-chief)
found that roughly two thirds of the reading path is repetition, stacked evidence, meta-commentary and
reference material that sits in the reading path. Reports: session scratchpad `review-*.md` (not committed).

Headline repetition: "tools change, the method endures" 10+ times; PocketOS told 7 times; "15 minutes vs a
senior's week" 10 times; most chapters end with three boxes (Artifact / Ship this week / Try it yourself)
doing one job; Appendix B restates Ch6, Ch8 and Ch10 near-verbatim.

## Decisions (founder, 2026-10-14)

- **Reading path target: ~15,000 words** (from ~53k), chapters of ~1,100-1,900 words.
- **Audience: unchanged** (practitioners and tech leads), written phone-first. No invented examples.
- **Archive: yes.** The September 2026 edition is frozen and served at `/full/` (and `/ro/full/`),
  `noindex, follow`, canonical to the new edition. Nothing is lost.
- Dual edition still binding: every change lands in EN and RO.

## New structure

| # | Title (working) | Words | Built from (current) |
|---|---|---|---|
| Prologue | Nine seconds | 900 | Prologue + the Foreword's thesis, tagline, 3-line author note, 3-bullet scope |
| Part I | Architecture | | |
| 1 | What an agent is | 1,700 | Ch1 (primitives as cards) + Ch2 (anatomy demo as one proof box) |
| 2 | Guardrails in five layers | 1,500 | Ch3 (one layer table, PocketOS referenced not retold) |
| Part II | Method | | |
| 3 | The bottleneck moved | 1,100 | Ch4 (three habits, when-to-use rule, unknowns table, one case) |
| 4 | The six-phase loop | 1,900 | Ch5 research/plan/execute/ship, wire-priority feature as the spine |
| 5 | Review and verify | 1,500 | Ch5 review/verify, diff read order, "evidence not proof", Ch9 P4 failure story |
| 6 | AGENTS.md and context | 1,700 | Ch6 (six-rule checklist, validation case) + Ch5 context hygiene |
| 7 | Map it first: architecture review | 1,100 | Ch7 (banking case as the chapter) |
| Part III | Reality | | |
| 8 | Should the agent touch this code? | 1,400 | Ch8 (signals table + traffic light flowchart, signal 6 weighting) |
| 9 | Rolling it out | 1,800 | Ch9 P1/P3 (worktrees, two kinds of hooks) + Ch10 grassroots path, 90-day arc, roles |
| Closing | Understand the problem | 400 | Closing L2128-L2136 + one return to PocketOS |

Out of the reading path:
- **Appendix A - For managers** (~1,800): cost economics (trimmed), the manager role, the 20-engineer case,
  portfolio framing from Ch8.
- **Appendix B - Templates** (~1,600): deduplicated against chapters; absorbs the per-chapter try-it exercises
  and the plugin-vetting checklist.
- **Appendix C - Sources**: kept whole (credibility moat), entries untouched.
- **Appendix D - Deep dives** (new, ~4-6k): every study, benchmark, vendor-dated detail and long sidebar moved
  out of the chapters, organized by new chapter number. Each chapter's "Go deeper" links here.
- Foreword, How to read, Dated claims, Scope, Cases index: removed as sections; the essentials fold into the
  Prologue; a one-line dated-claims note goes in the Prologue footer.
- About the author: ~200 words. Changelog: unchanged plus one new entry for this edition.

## Chapter format (every chapter)

1. Title + one-line promise ("By the end you can ...").
2. **TL;DR**: 3 bullets.
3. **One story**, told once (150-250 words). Later chapters refer back in one line.
4. **One visual**: the chapter's table or diagram.
5. Short sections, each opening with a **bold one-line rule**. Paragraphs of 4 sentences max.
6. **When it breaks**: 1-3 one-line failure modes (this is where the safety caveats survive).
7. **Do this Monday**: one checklist; first step under 30 minutes. Replaces Artifact / Ship this week / Try it.
8. **Go deeper**: links to the template (App. B), the deep dive (App. D) and sources (App. C).

House rules: keep a number only if it changes a decision; at most one study per claim in the body; no
chapter-tour paragraphs; the thesis is stated in the Prologue and the Closing only; ASCII hyphen ` - ` as in
the current text; no new facts.

## Hard constraints for the rewrite

- **No invented facts.** Every claim, number and example must exist in the current text. Wording may change.
- **Preserve figure blocks** verbatim (fenced block + `*Figure: ...*` caption). The build matches captions by
  substring: "primitives and the harness", "five governance layers", "six-phase loop", "kill signals and the
  traffic", "90-day adoption arc" (RO equivalents in `build_spa.py`).
- **Preserve explicit anchors** used by FAQ / SEO / inbound links, on whatever section now holds the idea:
  what-is-a-primitive, permissions-sandbox, what-is-mcp, memory, effort, what-is-the-six-phase-loop,
  reviewing-agent-diffs, trusting-agent-tests, context-hygiene, agents-md-vs-claude-md, what-is-agents-md,
  when-not-to-use-agents, are-agents-production-ready, how-to-roll-out, nine-seconds, about-the-author,
  changelog, how-much-does-it-cost, cost-levers, a-worked-example.
- Fix known consistency bugs while rewriting: nine primitives (not eight); Effort missing from the lists at
  current L535/L2086; AGENTS.md map is loaded on demand (current L1454 says at startup); Ch7 codebase age
  (table says 3 years, narrative 2018-2024); "nine person-months saved" vs 18 -> 3 months; Ch7 try-it step 3
  contradicts Ch6's no-layout rule.

## Build changes

- `SECTION_SLUGS`: new chapter titles/slugs; removed or merged sections (foreword, chapter-2, old chapter
  numbers) become redirect stubs via the existing `render_redirect_stub`; hash redirects updated.
- `/full/` and `/ro/full/`: render the frozen sources (`source/Ship_It_With_AI.full.md`,
  `source/Ship_It_With_AI.RO.full.md`) with the all-in-one `/read/` renderer, noindex, canonical to `/`.
- `EXPECTED_PAGE_COUNT`, FAQ anchors, llms.txt / sitemap regenerate; Playwright tests updated.

## Execution phases

1. **Prep**: fix the consistency bugs in the current text, freeze it as the `.full.md` archive (EN + RO).
2. **Pilot**: rewrite new Ch4 (the loop, from the 7k-word Ch5) alone; founder approves voice and format.
3. **EN fan-out**: remaining chapters + Prologue/Closing + Appendices A, B, D, one writer each
   (Sonnet xhigh); then a fidelity check per chapter (Sonnet medium: every claim traceable to the old text);
   then one integration pass (Opus xhigh: cross-references, duplication, voice, word budget).
4. **Build** changes + tests (Opus medium).
5. **RO mirror**: per chapter (Sonnet xhigh) following `source/RO_STYLE_GUIDE.md`, reusing the existing RO
   wording where the sentence survived; RO fidelity check.
6. **Verify**: build_spa.py, `npm run verify`, `npm run verify:site`, smoke check, mobile screenshots.
   Deploy and IndexNow only after the founder signs off.
