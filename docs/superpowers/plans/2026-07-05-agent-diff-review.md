# Agent-Diff Review Section Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Checkbox steps.

**Goal:** Teach the human review skill: a Ch5 question-form subsection on reading agent-written diffs, a B.8 read-order one-pager, a one-clause pattern-four back-pointer, and a changelog entry - both editions.

**Architecture:** One EN drafter produces all four blocks; deterministic ripples inline; editorial review; RO localizer mirrors final EN; final parity review; build/verify; STOP before deploy. Branch `agent-diff-review`.

## Global Constraints (verbatim from spec)

- No em/en dashes; no U+00D7; spaced ASCII ` - ` only. No Claude co-author trailers.
- Heading `### How do you review an agent-written diff? {#reviewing-agent-diffs}` / RO `### Cum faci review pe un diff scris de agent? {#reviewing-agent-diffs}` - anchor id identical. No new `##`.
- Section: hard cap 6 short paragraphs + one-line B.8 pointer. REFERENCE (one clause each), never re-teach: trusting-tests, Ch6 hallucination cross-check, pattern four's story, uncalibrated delegator.
- B.8 = one code block, B.3/B.6/B.7 register, sections BEFORE THE CODE / TESTS FIRST / BOUNDARIES / NEW NAMES / THEN LINE BY LINE / CALIBRATION.
- Ripples: "Seven copy-paste templates" -> "Eight" (EN :2221) / "Șapte" -> "Opt" (RO :2223); ONE clause appended to the pattern-four human-floor sentence (EN :1725, RO :1727); ONE changelog entry per edition. Historical changelog counts untouched.
- Reuse printed vocabulary; no new failure story; no blocklist substrings; RO established terms + diacritics + neuter-plural agreement.
- Deploy check via `gh run view --json conclusion`, never piped exit codes.

---

### Task 1: EN draft + integrate
- [ ] Dispatch EN drafter: four labeled blocks (CH5 SECTION, B8 TEMPLATE, PATTERN-FOUR CLAUSE, CHANGELOG ENTRY) per spec skeleton; give it the exact anchor texts (EN :940/:944 seam, :1725 sentence, B.7 tail, changelog head) and voice sources (trusting-tests subsection, pattern four, B.7).
- [ ] Integrate at anchors; apply Seven->Eight ripple.
- [ ] Greps: heading+anchor, B.8, "Eight copy-paste templates", pattern-four clause, changelog entry; 0 dashes; 0 `&gt;` beyond the 1 pre-existing; blocklist count unchanged.
- [ ] Commit `content(ch5): how to review an agent-written diff + B.8 read order (EN)`.

### Task 2: EN editorial review
- [ ] Diff file -> reviewer: voice; 6-para cap; reference-not-reteach discipline; read-order correctness and expert credibility (would a staff engineer learn something?); B.8 register; ripple + changelog format; dashes. Apply fixes; re-grep; commit if changed.

### Task 3: RO mirror
- [ ] Localizer gets final EN blocks + RO anchors (:942/:946 seam, :1727 sentence, RO B.7 tail, RO changelog head, :2223 count) + RO style guide + instruction to reuse pattern-four RO vocabulary ("corectitudinea de business", "potrivirea arhitecturală", "bifele verzi"). Integrate; ripple Șapte->Opt; greps (markers, 0 dashes); commit.

### Task 4: Final parity review
- [ ] Reviewer checks all six blocks per edition (section, B.8, pointer clause, count ripple, changelog, anchor id) for parity, RO agreement/diacritics, invariants. Fix loop if needed.

### Task 5: Build, verify, STOP
- [ ] Build; smoke; verify:site bare; rendered sweep (chapter-5, appendix-b, changelog, both editions); screenshots reset; present + STOP. On approval: merge -> push -> `gh run view --json conclusion` -> curl live -> IndexNow.

## Self-Review
Spec coverage: placement+section (T1), B.8 (T1), ripples (T1), reviews (T2/T4), RO (T3), verify+deploy lesson (T5). No placeholders: drafter prompt carries the spec skeleton and exact anchors. Consistency: heading/anchor/count strings identical across tasks.
