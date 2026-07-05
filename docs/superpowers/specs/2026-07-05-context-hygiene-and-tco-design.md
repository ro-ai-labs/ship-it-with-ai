# Spec: context hygiene section (Ch5 + B.7) and Appendix A worked example — 2026-07-05

Goal (user): from the full-read review, ship the two highest-impact-per-effort improvements:
(1) the book names context-window management "one of the central engineering disciplines" (Ch1 :279)
and calls contamination "the single biggest reason long-running sessions go wrong" (Ch5) but never
teaches the craft - add the missing section; (3) Appendix A is the only part of the book with no
numbers - add a worked TCO example. (#2, "how to read an agent diff," is deferred, not dropped.)

## Improvement A: context hygiene (Ch5 subsection + B.7 template + Ch1 pointer)

**A1 - New Ch5 subsection.** Insert after the inner/outer-loop vocabulary paragraph (EN :1043-1044,
ends "...it compounds whatever discipline - or whatever absence - it wraps.") and before "The
Superpowers plugin I have referenced..." (:1047). Form: `### Context hygiene {#context-hygiene}`
(new `###` inside ch5 page - safe, precedent "### Can you trust the tests" :954; no new `##` page,
EXPECTED_PAGE_COUNT unchanged). Length: 5-6 short paragraphs, hard cap 6 (Ch5 is the densest
chapter; this must arrive lean).

Content skeleton (the craft, operationalized):
1. Name the discipline and the stakes: the window is the agent's working memory; everything loaded
   competes with reasoning. Ch1 named the bound; this is how you work inside it. Tie back: Chapter 5
   already blamed contamination for long-session failure - here is the practice that prevents it.
2. Load what the task needs; reference the rest. Pointers over payloads: the architecture doc is
   referenced from AGENTS.md, not pasted; the research note names files rather than inlining them.
   The 200-line AGENTS.md cap (Ch6) is this same discipline applied to the always-loaded layer.
3. Session boundaries are the instrument. One unit of work per session. The loop's artifacts
   (research note, plan - committed) exist precisely so the next session can start clean and read
   state from the repository instead of dragging history. Fresh context per unit is the inner-loop
   form of what pattern eight does per iteration.
4. Warning signs of contamination, concrete: the agent re-answers a question it already settled,
   cites a stale version of a file it edited an hour ago, forgets a constraint it honored earlier,
   edit quality degrades late in a long session. The fix is not to argue with the session; commit
   durable state, end it, start clean.
5. Compaction is a handoff, not a continuation: summarization drops detail, so treat a compacted
   session like handing work to a new engineer - if the state that matters is not in a file by then,
   it is gone. Subagents are the other half of the instrument (isolation per task, Ch1/execute).
6. Close with pointer: Appendix B.7 is this discipline as a one-pager. (Mirrors the B.6 pointer
   pattern at the end of the outer-loop contract paragraph.)

**A2 - New Appendix B.7 "Context hygiene one-pager"** - a code-block checklist in the exact style of
B.3/B.6: LOAD (task-relevant only; pointers over payloads; AGENTS.md under 200 lines), SESSION (one
unit of work; start clean per unit; durable state in files, committed), WATCH FOR (the four
contamination signs), WHEN CONTAMINATED (commit state, end session, start fresh - do not argue),
COMPACTION (treat as handoff; anything not in a file is gone), SUBAGENTS (isolate per task; read
handoff summaries skeptically). Ripple: B intro :2175 "Six copy-paste templates" -> "Seven copy-paste
templates". Do NOT touch the historical 2026-06-10 changelog line "the template count is now six".

**A3 - Ch1 pointer clause.** :279 ends "They raise the ceiling." Append ONE sentence pointing
forward: the craft of working inside the bound is taught in Chapter 5 (context hygiene). One
sentence, no more - Ch1 stays a taxonomy.

## Improvement B: Appendix A worked example

**B1 - New `### A worked example` subsection** inserted after "What is not in the sticker price"
(the four TCO categories) and before "### Pricing changes; the math does not" (:2167). Length: ~4-6
short paragraphs or paragraphs + one small table.

Content and the honesty constraint (binding):
- Use ONLY the operational facts already in print from the Ch10 20-engineer financial-services
  engagement: 20 engineers, Team tier for 13 / Pro seats for 7, 41% of PRs agent-touched in month
  two, cycle time on those PRs 28% lower than baseline, defect rate within noise.
- Do NOT invent new engagement facts (no "integration took N weeks at this client", no real
  price quotes). The cost side runs on EXPLICITLY ILLUSTRATIVE round numbers, labeled as such in
  the prose ("round numbers for the arithmetic, not quotes - plug in your own"), consistent with
  the appendix's own stance that specific prices go stale quarterly.
- Shape of the walk: seats (13 + 7 at illustrative round rates) -> the four TCO categories with
  magnitude language the book already uses (integration: engineer-weeks, one-time; skill-authoring:
  a few hours per engineer per month plus the champion's part-time quarter; review: concentrated on
  seniors; governance: a week to a quarter) -> the value side anchored on the published 28% cycle
  time and the bounding heuristic's hours-saved arithmetic (an engineer at an illustrative loaded
  cost covering a seat with a few saved hours) -> the honest close: the sticker is the smallest
  line; the TCO categories dominate; the operational number (28% at flat defects) is what the
  manager defends, per Chapter 10.
- Cross-reference Chapter 10's manager sidebar explicitly (the numbers come from there).

## Changelog (per the changelog-major-updates-only rule: both ARE new material -> entries)

Two dated 2026-07-05 entries in both editions (same-date multiples have precedent, 2026-05-27):
- "Context hygiene (Chapter 5 + Appendix B.7)" - names the new section, the four contamination
  signs, session-boundary discipline, the B.7 one-pager, template count now seven, Ch1 pointer.
- "Appendix A worked example" - the cost appendix gains worked arithmetic anchored to the Chapter
  10 engagement's published numbers, with illustrative rates flagged as illustrative.
Do NOT bump "A note on dated claims" (June 2026): these additions carry no new tool-dated claims -
same reasoning as the outcome-throughline spec.

## RO mirror (dual-edition rule; anchors verified)

- RO vocabulary paragraph ends at :1045 region; Superpowers paragraph at :1049. "igiena contextului"
  is ESTABLISHED RO vocabulary (:1779 "un instrument de igienă a contextului") - use it for the
  heading: `### Igiena contextului {#context-hygiene}` (keep the same anchor id for hreflang parity).
- "contaminarea contextului" established (:1779 region and Ch5 RO). "sesiune" for session;
  compaction -> "compactare"; "stare durabilă în repository" established phrasing (:1779). Pointers
  over payloads -> paraphrase, no calc.
- RO B intro :2177 "Șase template-uri de copiat și lipit" -> "Șapte template-uri...". RO B.7 mirrors
  the EN block. RO Ch1 pointer after :279 "Doar ridică plafonul."
- RO Appendix A: mirror the worked example; keep EN terms per lexicon (Team tier, Pro, PR-uri,
  cycle time or the RO phrasing already used in the Ch10 RO sidebar - MATCH the existing RO Ch10
  sidebar's terminology for the same numbers; the localizer must read RO Ch10 :~1938 region first).
- RO changelog entries mirror EN.

## House-style constraints (hard)

- Spaced hyphen ` - `; NO em/en dashes anywhere. No Claude co-author trailer on commits.
- No blocklist substrings (esp. do not write "six primitives" etc.; "Seven copy-paste templates" is
  safe). No brand names beyond those already in print. No new failure story; no invented forensics.
- New `###` sections only; no new `##`; B.7 is one code block like B.3/B.6.
- Reuse existing vocabulary: "context hygiene" (already coined by pattern eight), "durable state in
  the repository", "fresh context per iteration". Do not coin new jargon.
- The verify_seo_pass changelog check is containment-based (adding entries is safe).

## Execution: expert team (consolidated, <=4 concurrent, ~6 total)

Two EN drafters in parallel (one per improvement) -> integrate inline -> one editorial review (both
diffs) -> RO localizer -> RO review folded into final parity review if clean -> build/verify ->
STOP for user deploy approval on branch `context-hygiene-and-tco`.

## Verification plan

1. Build + smoke + `SITE_NO_REBUILD=1 npm --prefix build run verify:site` (bare).
2. Greps: EN/RO markers for the Ch5 section, B.7, "Seven copy-paste templates"/"Șapte template-uri",
   Appendix A worked example, changelog entries; zero typographic dashes; blocklist clean.
3. Rendered sweep: chapter-5 and appendix pages both editions; heading-skip test must stay green.
4. `git checkout -- build/tests/screenshots`; commit; STOP before merge/deploy; on approval:
   merge -> push -> poll deploy -> curl live markers -> IndexNow re-ping.
