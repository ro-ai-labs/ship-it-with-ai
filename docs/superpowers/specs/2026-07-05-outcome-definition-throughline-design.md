# Spec: the expected-outcome throughline (define it in research + plan, verify against it) — 2026-07-05

Goal (user): "improve the book to clarify that in order to have good results you need to have an
outcome well defined and that the purpose of research and plan to help properly define the expected
outcome."

Discovery: a four-lens review team (current-state cartographer, gap diagnostician, in-voice proposer,
adversarial reconciler) read Ch4/Ch5/Ch7/Ch8/Foreword. Their converged verdict drives this spec.

## The finding (why this is a small, surgical change, not a new chapter)

The thesis is ~70% ALREADY the book's central claim - "formulation discipline: vague specifications
produce guessing; sharp specifications produce predictable execution" (Ch4 :764). Restating it
wholesale is redundant AND risks a WATERFALL smell that contradicts the book's identity (research
:884 SURFACES open questions; the enum-vs-free-text decision :996 is co-discovered mid-loop; failures
route back to Plan :874).

The genuine 30% gap: the six-phase loop grades everything against "the spec" (Review :928 "does the
implementation match the spec?"; Verify :964 "the assertion has to come from the intent") but NO
phase is ever credited with PRODUCING that spec. Research reads as current-state archaeology, Plan as
task-sequencing. The connective principle - research and plan are where the expected outcome gets
defined; verify checks against it - is load-bearing everywhere and stated nowhere.

## The binding reconciliation (guardrail against waterfall - do NOT violate)

Frame as CONVERGENCE, not up-front commitment: the expected outcome is an OUTPUT of the front of the
loop, not a fixed input you must hold before you start. Research pins down what it can and surfaces
what it cannot; the human settles the open questions; the plan turns the settled outcome into
per-task checks; when a later phase fails it routes back to Plan to sharpen the outcome. For genuinely
novel work you define what you can and let research close the gap. Any sentence that reads as
"fully define the outcome before you begin" is wrong and must be reworded.

## Naming decision (binding)

Do NOT coin "acceptance criteria" or "definition of done" - they collide with the book's existing
"the spec" (= research note + approved plan) and "the intent" (:964), and echo the competing "Spec
Kit" framework the book names at :838/:1041. Reuse the book's own vocabulary: "the spec", "the
intent", and "what 'done' means" / "Done when" (already used in Appendix B.6 :2388). The move is to
say the research note + plan ARE the spec that Review/Verify grade against - convergence, not a new
term.

## The edits (all EN + RO, mirrored per the dual-edition rule)

EN = `source/Ship_It_With_AI.md`; RO twin = `source/Ship_It_With_AI.RO.md` at the parallel positions
the review confirmed exist 1:1.

**E1 - KEYSTONE (the whole win).** EN :876, after "...what the whole thing looks like when it runs
end to end on a real piece of work." and before the `---` / "Phase one: research". Add ONE short
paragraph (~4-5 sentences) that: names the principle (a good result needs a well-defined expected
outcome; the agent can build anything but cannot know which thing you meant); assigns defining it to
research + plan; states verify checks against it; carries the convergence reconciliation (output of
the front of the loop, refined on failure-routes-back-to-plan, not held complete up front); lands the
cost beat (skip it and review has no spec to compare, verify has nothing to check, "done" is whatever
the agent decided). Supplies the missing referent for "the spec" (:928) and "the intent" (:964).

**E2 - VERIFY PIN.** EN :940, reframe "Verify is about whether the change is actually correct, not
just whether the existing tests still pass." to make the target explicit: correct AGAINST THE OUTCOME
YOU DEFINED in research and plan. One added clause + at most one closer that dovetails with the
existing :956 "evidence, not proof" section (do NOT rebuild it).

**E3 - RESEARCH REFRAME.** EN :884, extend the "Open questions the agent has - places where the
codebase is ambiguous and a human needs to decide." bullet: these are not loose ends; they are the
decisions that define what "done" will look like, surfaced now so you settle them before the plan
commits. (This is the convergence mechanism in situ - it strengthens, not contradicts, "research
surfaces questions".) PLUS EN :996 worked example, after "I picked enum.": one clause naming the move
- that choice defined the target the later phases would be checked against.

**E4 - PLAN "DONE".** EN :896 (after the tests sentence), add ~2 sentences: the plan also states what
"done" means for the change as a whole - the outcome verify checks against - not just per-task
verification; a plan that names files, tasks, and tests but never says what the change must achieve
has decomposed the work without defining it. Mirror the outer-loop's existing "Done when" discipline
(B.6) into the inner loop. PLUS Appendix B.3 :2240 PLAN block, add one checklist line after "- Plan
names test changes for any code change": `- Plan states what "done" means for the whole change, not
just per task`.

**E5 - CH4 ECHO.** EN :776, after the "Three habits..." paragraph, add ~2 sentences: name what the
first two habits are FOR - domain clarity and decomposition are not ends in themselves; they are how
you arrive at a well-defined expected outcome, and the third habit (test evidence) is evidence
AGAINST that defined result. Plants the thesis at its first home so the Ch5 keystone reads as payoff.

**Optional polish (include only if core lands; flag to user, default OFF to keep scope tight):**
summary-table cells (EN ~:1016-1017 "Research -> Missing context", "Plan -> Bad decomposition" ->
"...or undefined target" / "Undefined outcome / bad decomposition"); half-the-loop sidebar (~:1029);
a one-line Ch5->B.6 cross-reference. DEFAULT: skip these; the five edits above carry the load.

## House-style constraints (hard)

- Spaced hyphen ` - ` in prose; NO em/en dashes anywhere (content, commit, PR). ASCII only.
- No Claude/Anthropic co-author trailer; no `Claude-Session` trailer.
- Reuse existing vocabulary; do NOT coin "acceptance criteria" / "definition of done".
- No new `##`/`###` section (SECTION_SLUGS / EXPECTED_PAGE_COUNT unchanged); B.3 stays one code block;
  B.6 template count unchanged (no new template).
- opencode lowercase; AGENTS.md already linked in this chapter - new prose uses plain "AGENTS.md".
- No verify_seo_pass.js /read/ blocklist substring. No fabricated forensics - the worked example's
  facts (enum, audit-log bug, dashboard question) are real and stay as-is; only add the naming clause.
- Proportion: Ch5 is the book's densest chapter. E1 is ONE paragraph; E2/E3 are reframes; E4 is ~2
  sentences. Do NOT add a throughline running through every phase, a new sidebar, or a new artifact.

## Execution: the expert team (post-plan)

Lean, <=4 concurrent, ~4-5 total: EN drafter (all E1-E5 prose in one pass) -> editorial reviewer
(voice, waterfall-check, naming-collision-check, dashes, proportion) -> RO localizer (mirror per
RO_STYLE_GUIDE + lexicon) -> RO reviewer (agreement/diacritics) -> final whole-branch parity review.

## Verification plan

1. `python3 build/build_spa.py`; `bash build/tests/smoke_check.sh _site`.
2. `SITE_NO_REBUILD=1 npm --prefix build run verify:site` (run bare).
3. 0-dashes sweep on both sources + rendered read pages; JSON-LD still valid; chapter/page counts
   unchanged (no new sections).
4. Marker sweep both editions: keystone phrase present on chapter-5 page + /read/; B.3 line present.
5. `git checkout -- build/tests/screenshots` before committing (Playwright byte-churn).
6. Commit on branch `ch5-outcome-definition` (no Claude attribution). STOP - do not merge/deploy until
   the user approves. On approval: merge -> push -> poll deploy ~120s -> curl marker sweep on
   https://ship-it-with.ai/chapter-5-.../ + /ro/... -> re-ping IndexNow.
