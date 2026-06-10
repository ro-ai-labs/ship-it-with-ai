# Spec: the outer loop (/loop trend) enters the manual — 2026-06-10

Goal (user, via /goal): "/loop has become a new trend in Agentic AI Software engineering and I think
we need to cover it in the book - do a indepth research and write the best possible advice on it for
the book, then publish the updated book."

Research: deep-research workflow `wf_2f41c2ad-9b0` (5 angles: primary sources, lineage/discourse,
vendor convergence, failure modes/controls, economics). Findings feed the FACT SLOTS below.

## Placement decision

**Primary: Chapter 9, pattern eight — "the outer loop."** Rationale:
- Ch9's maturity-pattern set is the structural home: the pattern *depends on* pattern one
  (worktrees), pattern three (hookify), pattern four (PR review floor), Ch5 verify, Ch8 traffic
  light. Every precondition is already on the reader's table by Ch9.
- Ch9 was flagged underweight in the 2026-06-02 review; this closes that finding.
- It is NOT a Chapter 1 primitive. The book's convergence test (:389) is for primitives; the outer
  loop is a workflow pattern riding on primitives. Ch1 already names observability event-push as
  the next-primitive candidate — do not contradict.
- Form: bold-paragraph heading (`**Pattern eight: the outer loop.**`), matching patterns 1-7.
  No new `##` (SECTION_SLUGS/EXPECTED_PAGE_COUNT=19 stays). No `###` inside Ch9.

**Secondary edits:**
1. Ch5, after the half-the-loop sidebar (~:1031), before the Superpowers paragraph (:1035): a short
   vocabulary paragraph - six-phase loop = inner loop (one unit of work, gated by you); outer loop =
   re-invoking the agent with nobody between iterations; pointer to Ch9 pattern eight; the
   dependency claim (outer-loop safety is proportional to how mechanized these six functions are).
2. Ch9 count edits: :1635 "seven patterns"→"eight", "The final three ... watchlist"→"final four ...
   watchlist, and the outer loop"; :1715 "Three more patterns, briefly"→reworked signpost (three
   brief + one that needs room); :1749 "Seven patterns total"/"remaining three"→eight/four.
3. App B: new `### B.6 Outer-loop contract (one-pager)` template; intro :2125 "Five copy-paste
   templates"→"Six".
4. App C: 3-5 new sourced entries in existing categories (Tool documentation; Named incidents if
   research yields one; Studies if citable). No new category unless forced.
5. Changelog: `### 2026-06-10 — The outer loop (pattern eight)` + paragraph (match existing format,
   em-dash in heading is the apparatus convention).
6. "A note on dated claims" :153: "current as of May 2026" → "June 2026".
7. NO changes to: Contents, Cases list (single-chapter case), Scope-and-limits, Ch1, artifact box
   :1755, Ship-this-week :1759.

## Pattern eight content skeleton (~600-750 words)

1. **Name the trend.** Re-invoking the agent automatically until a condition holds - slash-command
   loops, bash while-loops around a CLI agent, scheduled/background cloud agents. The slash command
   is one vendor's spelling; the shape is general. [FACT SLOT: which vendors ship what, dates,
   convergence verdict.]
2. **Inner vs outer loop.** Ch5's six-phase loop = inner loop. Outer loop re-runs the unit with no
   human between iterations. The outer loop adds attempts, not judgment - it multiplies whatever
   the inner loop permits: gated → compounding progress; ungated → compounding slop.
3. **Lineage beat.** 2023 AutoGPT/BabyAGI looped a model on its own opinion of progress - collapsed
   (nothing external graded an iteration). [FACT SLOT: Ralph Wiggum - Huntley, dates, the actual
   technique]: fresh context per iteration, repo as the only shared state, every iteration graded
   by compile/tests/diff. Ties to Ch5 :906 (context contamination kills long sessions) - done
   right, the outer loop is a context-hygiene instrument: state lives in git, not in the window.
4. **The loop contract** (the control core; capability/workflow/adoption mapping):
   - stop condition a machine can evaluate (queue empty / suite green / budget spent) -
     "a loop without a stop condition is not autonomy; it is abandonment"
   - budget: tokens, money, iterations, or hours - whichever hits first (App A cross-ref)
   - per-iteration gate the agent cannot edit (CI/hooks own the grader; hookify deny on test
     config/CI/hook rules) - cf. Ch5 "evidence, not proof" + coverage-gaming caveat
   - durable state between iterations: queue + journal files in the repo, committed
   - isolation: worktree per loop, sandbox on, no production secrets, network constrained -
     unattended means prompt injection has no human to catch it (Ch3)
   - morning review floor: overnight PRs reviewed as PRs (pattern four floor, extra force)
5. **Eligibility (adoption).** Loop-eligible work = many similar units + machine-verifiable per
   unit + reversible per unit (migrations, lint/typing sweeps, coverage backfill, dep bumps).
   GREEN codebases only - Ch8 traffic light with extra force; YELLOW means supervised and the
   outer loop has no supervisor.
6. **Loop kill signals** (4, echo Ch8 discipline): oscillation (same diff applied and reverted);
   budget burn without queue progress; the gate got touched (auto-stop, mirrors signal-6 logic);
   same failure recurring - the task needs a human.
7. **Close.** Not for the first 90 days - it is what month 4 can look like when the first 90 days
   were honest. Unattended, the contract is the only reviewer awake: the outer loop is the first
   consumer of every control this manual installs.

## House-style constraints (hard)

- Spaced hyphen ` - ` in body prose; no em-dashes in prose (changelog heading exempt, matches file).
- NEVER write these substrings anywhere (verify_seo_pass.js /read/ blocklist, case-insensitive):
  "six primitives", "sixth primitive", "the other five", "five primitives", "five capabilities",
  "six conceptual", "six questions", "nine inspection points", "of the six",
  "are not additional primitives", "the sixth one is newer".
  ("six functions" is safe and already in print at :1029.)
- Numerals for statistics; spelled-out small counts otherwise.
- opencode lowercase, never sentence-initial. AGENTS.md bare link at most once per chapter
  (Ch9 already links it at :1655 - pattern eight must use plain "AGENTS.md" if needed).
- No fabricated forensics: trend/lineage claims come from the research record with App C sources;
  any first-person observation stays pattern-level (no invented dates/metrics/companies).

## Verification plan

1. `python3 build/build_spa.py` (or project build command), then `bash build/tests/smoke_check.sh _site`.
2. `SITE_NO_REBUILD=1 npm --prefix build run verify:site` - run bare, NEVER piped into tail in the
   same chain as a commit (pipeline exit-code trap from 2026-06-09).
3. `git checkout -- build/tests/screenshots` before committing (Playwright byte-churn).
4. Commit WITHOUT Claude attribution (user standing preference). Push, poll deploy ~120s, curl
   marker sweep on https://ship-it-with.ai/read/ for: "Pattern eight: the outer loop",
   "B.6", changelog entry date, Ch5 vocabulary paragraph marker.
