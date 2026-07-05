# Expected-Outcome Throughline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Make explicit that a good result needs a well-defined expected outcome, and that research + plan are where that outcome gets defined and verify is where it gets checked - across both editions, framed as convergence (not waterfall), reusing the book's own vocabulary.

**Architecture:** Five small in-voice edits in Chapter 5 (+ one Ch4 echo, + one Appendix B.3 line), mirrored EN->RO. One new paragraph (keystone), the rest are sentence-level reframes/extensions. No new sections, no new named term, no new template.

**Tech Stack:** Python static-site generator; bash smoke; Node verify:site; markdown sources.

## Global Constraints (verbatim from the spec)

- Frame as CONVERGENCE, never waterfall: the expected outcome is an OUTPUT of the front of the loop, refined when failures route back to plan - not a fixed input held before you start. Novel work: define what you can, let research close the gap. Any "fully define before you begin" phrasing is wrong.
- Do NOT coin "acceptance criteria" / "definition of done". Reuse "the spec" (= research note + approved plan), "the intent", "what 'done' means" / "Done when" (from B.6).
- Spaced hyphen ` - `; NO em/en dashes anywhere (prose, commit, PR). No Claude co-author trailer.
- No new `##`/`###`; B.3 stays one code block; no new B template. opencode lowercase; plain "AGENTS.md".
- No blocklist substrings; no fabricated forensics (worked-example facts stay real).
- Ch5 is the densest chapter: E1 is ONE paragraph, E2/E3 reframes, E4 ~2 sentences. No new throughline/sidebar/artifact.
- Every EN edit mirrored in RO per RO_STYLE_GUIDE + lexicon.
- Work stays on branch `ch5-outcome-definition`; no merge/deploy until user approves.

---

### Task 1: EN prose - draft and integrate all five edits

**Files:** Modify `source/Ship_It_With_AI.md` at :776 (E5), :876 (E1), :884 + :996 (E3), :896 (E4), :940 (E2), and Appendix B.3 :2240 (E4 checklist line).

- [ ] **Step 1: Dispatch the EN drafter subagent** with the current text of each anchor (below), the spec's "edits" + "reconciliation" + "naming" sections, and the Global Constraints. Ask for ONLY the new/changed prose, one labeled block per edit:
  - E1 keystone (~4-5 sentence paragraph): names the principle; assigns defining the outcome to research+plan; verify checks against it; convergence reconciliation; cost beat ("review has no spec to compare, verify has nothing to check, done is whatever the agent decided"). Anchor: insert after ":876 ...on a real piece of work." before the `---`.
  - E2 verify pin: reworded ":940 Verify is about whether the change is actually correct, not just whether the existing tests still pass." making the target "correct against the outcome you defined in research and plan"; optional one closer dovetailing with :956 "evidence, not proof".
  - E3a research bullet: reworded ":884 Open questions the agent has - places where the codebase is ambiguous and a human needs to decide." adding that these are the decisions that define what "done" looks like, surfaced now so you settle them before the plan commits.
  - E3b worked-example clause: after ":996 I picked enum." one clause - that choice defined the target the later phases would be checked against.
  - E4a plan sentences (~2): after ":896 ...the plan is incomplete and the agent goes back..." the plan also states what "done" means for the change as a whole (the outcome verify checks against), not just per-task; a plan that names files/tasks/tests but never says what the change must achieve has decomposed the work without defining it.
  - E4b B.3 line: `- Plan states what "done" means for the whole change, not just per task` (insert after B.3 :2240 `- Plan names test changes for any code change`).
  - E5 Ch4 echo (~2 sentences): after ":776 Three habits..." name what the first two habits are for - domain clarity + decomposition are how you arrive at a well-defined expected outcome; test evidence is evidence against that defined result.

- [ ] **Step 2: Integrate** each block at its exact anchor (Edit tool, one edit per site). Preserve blank-line paragraph separation. B.3 line goes inside the code block.

- [ ] **Step 3: Verify markers + invariants + dashes.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai
grep -niE "well-defined expected outcome|what .done. means|defined (the )?target|against the outcome you defined" source/Ship_It_With_AI.md | head
grep -n 'Plan states what "done" means for the whole change' source/Ship_It_With_AI.md
echo "must be ZERO dashes:"; grep -cP '\x{2014}|\x{2013}' source/Ship_It_With_AI.md
echo "must be ZERO coined term:"; grep -ciE "acceptance criteria|definition of done" source/Ship_It_With_AI.md
```
Expected: markers present; B.3 line found; dash count 0; the coined-term count stays at its pre-existing value (1 - the injection-surface use at :655 - and NOT more; if it rose, a drafter slipped the banned term in).

- [ ] **Step 4: Commit.**
```bash
git add source/Ship_It_With_AI.md
git commit -m "content(ch5): name the expected-outcome throughline - research+plan define it, verify checks it (EN)"
```

---

### Task 2: EN editorial review

- [ ] **Step 1: Dispatch the editorial reviewer** with the EN diff (`git diff -U8 HEAD~1 HEAD` written to a file) + the spec + Global Constraints. Check ONLY: voice; the WATERFALL guardrail (nothing reads as "fully define up front"; convergence intact); the NAMING rule (no coined term; reuses "the spec"/"intent"/"done"); dashes 0; proportion (E1 one paragraph, no bloat in the dense chapter); the worked-example facts unchanged except the added clause; no blocklist substrings. Return exact fixes or "clean".
- [ ] **Step 2: Apply fixes**, re-run Task 1 Step 3 greps.
- [ ] **Step 3: Commit if fixes applied.**
```bash
git add source/Ship_It_With_AI.md && git commit -m "content(ch5): editorial fixes on outcome-definition throughline (EN)"
```

---

### Task 3: RO mirror - localize all five edits

**Files:** Modify `source/Ship_It_With_AI.RO.md` at the parallel positions (research ~:886, plan ~:898, verify ~:942, worked example ~:998, Ch4 ~:776, B.3 ~:2240 region, keystone seam ~:878).

- [ ] **Step 1: Dispatch the RO localizer** with the FINAL EN prose (Tasks 1-2), the RO_STYLE_GUIDE, the RO lexicon (keep English tech terms articulated; "framework" not "cadru"; ASCII hyphens; diacritics), and the current RO anchors. Produce the RO mirror of E1-E5. Keep "spec"/"spec-ul", "intent"/"intenție" consistent with existing RO usage (:930 "spec-ul", :966 "intenție"); render "what done means" as `ce înseamnă „gata” pentru schimbarea în ansamblu` (RO uses „..." quotes and „gata" for done per :774). No coined term.
- [ ] **Step 2: Integrate** each RO block at its anchor.
- [ ] **Step 3: Verify.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai
grep -niE "rezultat bun|ce înseamnă .gata.|outcome|țintă|intenție" source/Ship_It_With_AI.RO.md | head
echo "must be ZERO dashes:"; grep -cP '\x{2014}|\x{2013}' source/Ship_It_With_AI.RO.md
```
Expected: markers present; dash count 0.
- [ ] **Step 4: Commit.**
```bash
git add source/Ship_It_With_AI.RO.md && git commit -m "content(ch5): outcome-definition throughline mirrored (RO)"
```

---

### Task 4: RO review (agreement + diacritics + parity)

- [ ] **Step 1: Dispatch the RO reviewer** with the RO diff + RO_STYLE_GUIDE + the final EN. Check gender/number agreement, full diacritics, romgleza register, meaning parity vs EN, the convergence framing preserved (no waterfall in RO), zero dashes. Return fixes or "clean".
- [ ] **Step 2: Apply fixes**, re-run Task 3 Step 3 greps.
- [ ] **Step 3: Commit if fixes applied.**

---

### Task 5: Build, verify, marker sweep (STOP before deploy)

- [ ] **Step 1: Build.** `python3 build/build_spa.py`
- [ ] **Step 2: Smoke.** `bash build/tests/smoke_check.sh _site`
- [ ] **Step 3: Verify (bare).** `SITE_NO_REBUILD=1 npm --prefix build run verify:site`
- [ ] **Step 4: Rendered marker sweep + dashes.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai
grep -rl "expected outcome" _site/chapter-5*/ 2>/dev/null; grep -rl "gata" _site/ro/chapter-5*/ 2>/dev/null
grep -oP '\x{2014}|\x{2013}' _site/read/index.html _site/ro/read/index.html | wc -l
```
Expected: EN+RO markers found; dash count 0.
- [ ] **Step 5: Reset screenshot churn.** `git checkout -- build/tests/screenshots 2>/dev/null; git status --short`
- [ ] **Step 6: STOP.** Present diff + green results; do NOT merge/deploy until user approves. On approval: merge `ch5-outcome-definition` -> main, push, poll deploy, curl-verify both editions live, re-ping IndexNow.

---

### Task 6: Final whole-branch parity review

- [ ] Dispatch the final reviewer with the full branch content diff (`git diff main..HEAD -- source/*.md`) + the spec. Check EN<->RO parity across all five edits, the anti-waterfall framing in both, the naming rule, and that no section/count invariants moved. Return READY TO MERGE or a findings list -> one fix subagent.

## Self-Review

- Spec coverage: E1 keystone (T1), E2 verify (T1), E3 research+example (T1), E4 plan+B.3 (T1), E5 Ch4 (T1); RO mirror (T3); reviews (T2/T4/T6); build+verify (T5). All spec edits mapped.
- Placeholder scan: deterministic anchors carry exact current text; generative prose carries acceptance criteria + drafter prompt (honest form for authored content, gated by T2/T4/T6 + greps).
- Consistency: "the spec"/"the intent"/"what done means" used identically EN-side; RO renderings fixed in T3 prompt; the anti-waterfall + no-coined-term constraints repeated in every review dispatch.
