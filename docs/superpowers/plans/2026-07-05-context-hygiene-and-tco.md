# Context Hygiene + Appendix A Worked Example Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Checkbox steps.

**Goal:** Ship the two full-read improvements: the Ch5 context-hygiene section (+ B.7 one-pager + Ch1 pointer) and the Appendix A worked TCO example, both editions, with changelog entries.

**Architecture:** All generative prose from two parallel EN drafters with tight acceptance criteria; deterministic ripples (template count, changelog) inline; one editorial review over both diffs; RO localizer mirrors the final EN; final parity review; build/verify; STOP before deploy. Branch `context-hygiene-and-tco`.

## Global Constraints (verbatim from spec)

- No em/en dashes anywhere; spaced ASCII ` - ` only. No Claude co-author trailers.
- Ch5 section: hard cap 6 short paragraphs; heading `### Context hygiene {#context-hygiene}` / RO `### Igiena contextului {#context-hygiene}`. No new `##` pages. B.7 is ONE code block styled like B.3/B.6.
- Reuse existing vocabulary ("context hygiene" from pattern eight, "durable state in the repository", "fresh context per iteration"); coin nothing.
- Appendix A: ONLY published Ch10 engagement facts (20 engineers, 13 Team + 7 Pro, 41% agent-touched, 28% cycle time, defects within noise); cost side uses round numbers EXPLICITLY labeled illustrative; no invented engagement facts, no real price quotes.
- Ripples: B intro "Six copy-paste templates" -> "Seven" (EN :2175, RO :2177 "Șase" -> "Șapte"); historical 2026-06-10 changelog line untouched; dated-claims note untouched.
- Two changelog entries dated 2026-07-05 per edition (context hygiene; Appendix A worked example), matching existing format.
- RO: match RO Ch10 sidebar terminology for the same numbers (localizer reads RO Ch10 sidebar first); "igiena contextului"/"contaminarea contextului" established; keep anchor id `#context-hygiene` in both.
- No blocklist substrings. Work stays on branch; no merge/deploy until user approves.

---

### Task 1: EN draft both additions (two drafters in parallel)

**Files:** Modify `source/Ship_It_With_AI.md` at :279 (Ch1 pointer), :1044->:1047 seam (Ch5 section), :2166 region (Appendix A worked example, before "### Pricing changes"), :2175 (template count), B.6 end ~:2414 (append B.7), changelog :2095 region (two new entries above the hooks entry).

- [ ] **Step 1:** Dispatch drafter A (context hygiene): produce Ch5 section per spec skeleton (6-item content list), the B.7 code block, the one-sentence Ch1 pointer, and the context-hygiene changelog entry. Dispatch drafter B (Appendix A): produce the worked-example subsection per spec shape + its changelog entry. Both get voice guidance + Global Constraints + the exact current anchor text.
- [ ] **Step 2:** Integrate all blocks at exact anchors; apply the "Six -> Seven" ripple.
- [ ] **Step 3:** Verify: markers present (`### Context hygiene`, `B.7`, `Seven copy-paste templates`, `A worked example`, two `2026-07-05` new entries); dashes 0; blocklist 0; "acceptance criteria|definition of done" count unchanged (1).
- [ ] **Step 4:** Commit `content: context hygiene (ch5 + B.7 + ch1 pointer) and Appendix A worked example (EN)`.

### Task 2: EN editorial review (one reviewer, both additions)

- [ ] Diff file -> reviewer checks: voice; Ch5 cap (<=6 paras, lean, no re-teaching of pattern eight); B.7 style parity with B.3/B.6; the illustrative-numbers labeling is unmistakable and no invented engagement facts; template-count ripple; changelog format; dashes; blocklist. Apply fixes; re-grep; commit if changed.

### Task 3: RO mirror

- [ ] Localizer gets final EN blocks + RO style guide + RO anchors (:279, :1045-:1049 seam, RO B intro :2177, RO B.6 end, RO Appendix A pricing section, RO changelog) + instruction to read RO Ch10 sidebar for number terminology. Integrate; ripple "Șase -> Șapte"; verify greps (markers, 0 dashes, agreement spot-checks); commit.

### Task 4: Final parity review

- [ ] One reviewer: EN<->RO parity across all seven blocks (Ch5 section, B.7, Ch1 pointer, A worked example, template count, 2 changelog entries), illustrative-labeling preserved in RO, anchor id `#context-hygiene` in both, zero dashes. Fix loop if needed.

### Task 5: Build, verify, STOP

- [ ] Build; smoke; `SITE_NO_REBUILD=1 npm --prefix build run verify:site` (bare); rendered marker sweep both editions incl. heading-skip test green; screenshots reset; present diff + results; do NOT merge/deploy until approved. On approval: merge -> push -> watch deploy -> curl live -> IndexNow.

## Self-Review
Spec coverage: A1/A2/A3 (T1 drafter A), B1 (T1 drafter B), ripples + changelog (T1 step 2), reviews (T2/T4), RO (T3), verification (T5). Placeholders: none - drafter prompts carry the spec skeletons verbatim. Consistency: heading strings, anchor id, and count ripple named identically across tasks.
