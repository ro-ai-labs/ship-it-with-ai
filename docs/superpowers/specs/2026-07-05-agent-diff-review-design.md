# Spec: how to read an agent diff (Ch5 subsection + B.8) — 2026-07-05

Goal (user, via the full-read review roadmap): the human review skill is load-bearing everywhere
(pattern four's human floor, the outer loop's morning review, Ch10's uncalibrated delegator, signal
2's drowning seniors) and taught nowhere. Teach it: how a human reads an agent-written diff, and why
agent bugs have a different signature than human bugs.

## Placement decision

**Chapter 5, new question-form `###` subsection immediately after the review phase** - after "The
output of review is structured... surfaces the suggestions for the human reviewer to decide."
(EN :940, RO :942) and before "**Phase five: verify.**" (EN :944, RO :946). Rationale:
- The review phase teaches the two AGENT reviewers; the human's craft is the missing half of the
  same phase. Placing it here completes the phase instead of adding a topic.
- Structural rhyme: verify already gets its craft-subsection ("### Can you trust the tests the
  agent writes?"); review gets the parallel one. Question-form H3 is a house pattern (and matches
  the FAQ/SEO convention).
- It becomes the referent for every later "business correctness and architectural fit" invocation,
  the same move the outcome-definition keystone made for "the spec."

Heading: `### How do you review an agent-written diff? {#reviewing-agent-diffs}`
RO: `### Cum faci review pe un diff scris de agent? {#reviewing-agent-diffs}` (anchor id identical).

Rejected: Ch9 pattern four (a patterns catalogue, and pattern four is already the longest pattern -
it gets a one-clause back-pointer instead); a template-only treatment (the skill needs prose).

## The load-bearing idea (what makes this expert content, not blog filler)

Agent bugs and human bugs differ IN KIND, so the read order inverts. Human diffs fail at errors of
execution - typos, off-by-one, the forgotten edge case - and the reviewer hunts mistakes in the
code. Agent diffs compile, pass lint, and read idiomatic; they fail at errors of intent and context:
- plausible-but-wrong (the discount-tier shape: right code, wrong business rule),
- wrong layer (the validation-in-the-controller shape, Ch6's opening story),
- invented API (the hallucination shape, Ch6),
- stale idiom (the React 18/19 shape, signal eight),
- over-scoped diff (files touched that the plan never named),
- tests that assert the implementation rather than the intent (Ch5's own trusting-tests section).
The signature sentence (aphorism-shaped, drafter should land something close): an agent bug looks
like the code a good engineer would write for a slightly different task. Fluency is not correctness.

The read order (the first ten minutes, before line-by-line):
1. Diff-stat against the plan, before any code: does the SHAPE match the ask? Unplanned files are
   the first flag.
2. Tests first - read what they assert, not whether they pass (reference the trusting-tests section
   and "the assertion has to come from the intent"; do NOT re-teach it).
3. The boundaries the team has rules about: AGENTS.md forbidden patterns and layer conventions -
   the agent violates conventions confidently and in fluent style, so style-reading will not catch
   a boundary violation.
4. Grep the new names: any API, function, or config key the diff introduces that you do not
   recognize (reference Ch6's cross-check tactic in one clause).
5. Only then line-by-line - the mechanical layer the two reviewers above have already swept; your
   minutes go where the agents cannot: business correctness and architectural fit.
Close the loop on time-shape: this is why the pattern works - the human read gets SHORTER and
SHARPER, not skipped; reference the fifteen-minutes-to-five dynamic already printed in pattern four
without re-telling the failure story.

Length: 5-6 short paragraphs, hard cap 6, plus the one-line B.8 pointer ("Appendix B.8 is this read
order as a one-pager.") mirroring the B.6/B.7 pointer pattern.

## B.8 template + ripples

**B.8** `### B.8 Agent-diff read order (one-pager)` - one code block in B.3/B.6/B.7 style. Sections:
BEFORE THE CODE (diff-stat vs plan; unplanned files = first flag), TESTS FIRST (read assertions,
not pass/fail; assertion comes from the intent), BOUNDARIES (forbidden patterns, layer rules -
fluent style hides violations), NEW NAMES (grep every API/function/config the diff introduces),
THEN LINE BY LINE (mechanical layer is pre-swept; spend minutes on business correctness +
architectural fit), CALIBRATION (fluency is not correctness; an agent bug looks like good code for
a slightly different task).

Ripples:
- B intro: "Seven copy-paste templates" -> "Eight copy-paste templates" (EN :2221); RO "Șapte" ->
  "Opt" (:2223). Historical changelog lines (six, seven) untouched.
- Ch9 pattern four, the human-floor fix sentence (EN :1725, RO :1727): append ONE clause pointing
  back - e.g. "; Chapter 5's read order for agent diffs is that floor made concrete" (RO mirror).
  One clause, no expansion. No other Ch9/Ch10/B.6 edits.
- Changelog: ONE entry per edition, `### 2026-07-05 - How to review an agent diff (Chapter 5 +
  Appendix B.8)`, existing format. (New material -> entry, per the changelog rule.)

## House-style constraints (hard)

- Spaced hyphen ` - `; NO em/en dashes; no multiplication glyph; ASCII only in new text.
- No new `##` (only `###` + anchor in both editions, id `{#reviewing-agent-diffs}` identical).
- REFERENCE, do not re-teach: trusting-tests (:964 region), Ch6 hallucination tactics, pattern
  four's failure story, the uncalibrated delegator. Each earns at most a clause.
- No new failure story, no invented forensics, no named tools beyond those in print.
- Reuse printed vocabulary: "business correctness and architectural fit", "the assertion has to
  come from the intent", "green checkmarks"/"bifele verzi", "spec compliance"/"code quality".
- RO: established terms - review, diff, PR (EN, articulated); "corectitudinea de business",
  "potrivirea arhitecturală", "pattern-urile interzise", „gata" quotes style; full diacritics;
  neuter-plural agreement.
- No blocklist substrings ("Eight copy-paste templates" is safe; never "nine inspection points").
- No Claude co-author trailer. Work on branch `agent-diff-review`; no merge/deploy until approved.

## Execution: expert team (~4 agents)

EN drafter (section + B.8 + pattern-four clause + changelog entry) -> editorial review -> RO
localizer (all blocks) -> final parity review. Deterministic ripples inline. Build/verify inline.

## Verification plan

1. Build; smoke; `SITE_NO_REBUILD=1 npm --prefix build run verify:site` run bare.
2. Greps: heading + anchor both editions; B.8; Eight/Opt template count; pattern-four clause both;
   changelog entries; zero U+2014/U+2013/U+00D7; blocklist unchanged.
3. Rendered sweep: chapter-5 + appendix-b + changelog pages, both editions; heading-skip test green.
4. Deploy gate: STOP for user approval. On approval: merge -> push -> **verify the run via
   `gh run view --json conclusion` (never a piped exit code - lesson from the B.7 deploy)** ->
   curl live markers both editions -> IndexNow re-ping.
