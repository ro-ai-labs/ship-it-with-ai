# Chapter 9 Git Commit/Push Hooks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand Chapter 9 pattern three from "hookify rules" into "two kinds of hooks" so the manual covers git pre-commit/pre-push hooks alongside agent hooks and PR review, in both the EN and RO editions.

**Architecture:** Pattern three gains a third rung on its existing enforcement ladder (AGENTS.md request -> hookify boundary -> git commit/push gate). ~3 new paragraphs of generative prose (drafted in-voice by an expert-team subagent), a handful of deterministic string edits (heading, recap, closing, artifact, pattern-eight disambiguation), a full RO mirror, and an optional changelog entry. No new `##`/`###` sections, so the build's section/page invariants are untouched.

**Tech Stack:** Python static-site generator (`build/build_spa.py`), bash smoke check, Node verify:site (Playwright), markdown sources.

## Global Constraints

Copied verbatim from the spec (`docs/superpowers/specs/2026-07-05-ch9-git-commit-push-hooks-design.md`). Every task's requirements include these:

- Count stays EIGHT patterns. Pattern three becomes "two kinds of hooks"; no ninth pattern; no renumbering.
- Agentic spine is load-bearing, not decorative: agent = just another committer; `--no-verify` is the agent's escape hatch closed by a hookify deny rule; local hooks are fast feedback, CI is the enforcement (defer the CI/gate argument to pattern eight, do not rebuild it).
- Say "git hooks", never "GitHub hooks". Tests in pre-push, not pre-commit (pre-commit = format/lint/typecheck/secret-scan). CI is "the check you cannot skip from your laptop", never "un-bypassable". `--no-verify` narrows, does not seal.
- No brand names at mechanism level (no husky/lefthook/pre-commit-framework) - "a hook manager", generic.
- No new failure story in pattern three (line ~:1691 reserves that device for pattern four).
- Proportion: pattern three ends at ~6-7 short paragraphs; hookify stays the spine, git hooks arrive lean (+2 to +3 paragraphs, hard cap +3).
- House style: spaced hyphen ` - ` in prose; NO em/en dashes anywhere (content, commit msg, PR body) - ASCII hyphen only. opencode lowercase. Plain "AGENTS.md" in new prose (no repeat bare link).
- No verify_seo_pass.js /read/ blocklist substring ("six primitives", "the other five", etc.).
- Every EN edit mirrored in RO per RO_STYLE_GUIDE + the terminology/agreement table in the spec. Neuter-plural agreement: "hook-uri versionate/rapide/deterministe" (never singular-masculine in the plural). `gate` stays English; `--no-verify` never translated.
- Commits: no Claude/Anthropic co-author trailer, no `Claude-Session` trailer. Work stays on branch `ch9-git-hooks`; do NOT merge to main / deploy until the user approves.

---

### Task 1: EN pattern three - draft and integrate the third rung

**Files:**
- Modify: `source/Ship_It_With_AI.md` (pattern three heading :1669; motif :1675; body ends :1677, before the `---` at :1679)

**Interfaces:**
- Produces: the EN rung-three prose that Task 4 (RO) mirrors and Task 3 (review) checks. Establishes the exact heading string `**Pattern three: two kinds of hooks.**` and the git-hook vocabulary (pre-commit/pre-push, hook manager, deny rule, CI mirror) that later tasks reuse.

- [ ] **Step 1: Dispatch the EN drafter subagent.** Prompt it with: the current pattern three text (:1669-1677), the "New-rung content skeleton" + "Vetted technical corrections" + "load-bearing spine" sections of the spec, and the Global Constraints above. Ask for ONLY the new prose: (a) the reworked/springboard handling so the :1675 "firm boundary" line sets up rung three rather than closing the pattern (e.g. amend to "the firm boundary on the agent"), and (b) 2-3 new paragraphs for rung three. Require: names the "hook" collision explicitly; keeps the line "deterministic checks don't drift the way probabilistic reviewers can - a secret scanner either finds the key or it doesn't" (or equivalent); pre-commit fast/local vs pre-push heavier; generic "a hook manager" + versioned-config point; `--no-verify` closed by a hookify deny rule; local-is-feedback / CI-is-enforcement with a one-clause tie to pattern eight's "gate the agent cannot edit"; NO brand names, NO failure story, NO em dashes.

- [ ] **Step 2: Integrate the heading.** Replace `**Pattern three: hookify rules.**` (:1669) with `**Pattern three: two kinds of hooks.**`.

- [ ] **Step 3: Integrate the springboard + rung-three paragraphs.** Apply the drafter's :1675 springboard tweak, then insert the new paragraphs after the current pattern-three body (after :1677 "Five to ten rules is usually enough..."), before the `---` separator that precedes pattern four. Keep blank-line paragraph separation matching the file.

- [ ] **Step 4: Verify markers present and forbidden strings absent.**

Run:
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && \
grep -n "Pattern three: two kinds of hooks" source/Ship_It_With_AI.md && \
grep -niE "pre-commit|pre-push|--no-verify|hook manager" source/Ship_It_With_AI.md | grep -c "" && \
echo "--- must be ZERO hits below ---" && \
grep -nE $'—|–' source/Ship_It_With_AI.md | wc -l && \
grep -niE "GitHub pre-commit|GitHub hook|husky|lefthook|six primitives|the other five" source/Ship_It_With_AI.md | wc -l
```
Expected: heading line found; several pre-commit/etc. hits; dash count `0`; brand/blocklist count `0`.

- [ ] **Step 5: Verify pattern three length proportion.** Eyeball the pattern-three block: heading + <=7 short paragraphs. If the hookify half was inflated to "balance", trim back - hookify stays as-was.

- [ ] **Step 6: Commit.**
```bash
git add source/Ship_It_With_AI.md
git commit -m "content(ch9): pattern three becomes two kinds of hooks - add git commit/push gate (EN)"
```

---

### Task 2: EN deterministic ripple edits

**Files:**
- Modify: `source/Ship_It_With_AI.md` recap :1701; pattern-eight contract :1765; closing :1775; artifact :1781

**Interfaces:**
- Consumes: the "two kinds of hooks" pattern name from Task 1.
- Produces: the exact ripple wording the RO edition (Task 5) mirrors.

- [ ] **Step 1: Recap (:1701).** In `Four patterns. Worktrees. Champions. hookify rules. PR review toolkit.` replace `hookify rules.` with `Hooks.` -> `Four patterns. Worktrees. Champions. Hooks. PR review toolkit.`

- [ ] **Step 2: Pattern-eight disambiguation (:1765).** In `... tests, lint configuration, CI workflow, and hook rules sit behind a deny rule (pattern three).` replace `and hook rules sit behind` with `and the hookify rules sit behind` (restore the agent-specific label; keep `(pattern three)`). Do NOT expand the sentence.

- [ ] **Step 3: Closing (:1775).** In `The first four - worktrees, champions, hookify rules, PR review toolkit - apply broadly.` replace `hookify rules` with `hooks` -> `... worktrees, champions, hooks, PR review toolkit - apply broadly.`

- [ ] **Step 4: Artifact box (:1781).** Broaden the body clause `an isolated worktree for agent work, a pre-tool-use hook for the dangerous-action categories, and a PR review checklist tuned to agent-generated diffs.` to name the commit-time gate, e.g. `... a pre-tool-use hook for the dangerous-action categories, a git commit/push gate for the mechanical ones, and a PR review checklist tuned to agent-generated diffs.` Keep the title `Worktree + hook + review pattern.` unchanged. (This makes it three named controls + the gate; keep the sentence readable, no em dash.)

- [ ] **Step 5: Verify.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && \
grep -n "Champions. Hooks. PR review toolkit" source/Ship_It_With_AI.md && \
grep -n "the hookify rules sit behind a deny rule" source/Ship_It_With_AI.md && \
grep -n "champions, hooks, PR review toolkit" source/Ship_It_With_AI.md && \
grep -niE "eight pattern" source/Ship_It_With_AI.md && \
grep -nE $'—|–' source/Ship_It_With_AI.md | wc -l
```
Expected: first three greps each match once; "eight patterns" still present (intro/closing intact); dash count `0`.

- [ ] **Step 6: Commit.**
```bash
git add source/Ship_It_With_AI.md
git commit -m "content(ch9): ripple edits for two-kinds-of-hooks (recap, closing, artifact, pattern-eight) - EN"
```

---

### Task 3: EN editorial review pass

**Files:** none modified unless the review finds fixes.

- [ ] **Step 1: Dispatch the editorial reviewer subagent.** Give it the final EN pattern three (Tasks 1-2) and the Global Constraints. Ask it to check ONLY: voice match to the surrounding chapter; agentic spine is central (not boilerplate); no fabricated forensics/failure story; proportion (<=7 paras); zero em/en dashes; no brand names; no blocklist substrings; "git hooks" not "GitHub hooks"; tests-in-pre-push; CI not called "un-bypassable"; the pattern still reads as one of eight. Return a short list of required fixes with exact line + replacement, or "clean".

- [ ] **Step 2: Apply any required fixes** to `source/Ship_It_With_AI.md` exactly as specified by the reviewer.

- [ ] **Step 3: Re-run the Task 1 Step 4 + Task 2 Step 5 grep checks** to confirm still green after fixes.

- [ ] **Step 4: Commit (only if fixes were applied).**
```bash
git add source/Ship_It_With_AI.md
git commit -m "content(ch9): editorial fixes on two-kinds-of-hooks (EN)"
```

---

### Task 4: RO pattern three - mirror the third rung

**Files:**
- Modify: `source/Ship_It_With_AI.RO.md` heading :1671; motif :1677; body ends :1679

**Interfaces:**
- Consumes: the final EN rung-three prose (Tasks 1-3).
- Produces: the RO rung-three prose that Task 6 reviews.

- [ ] **Step 1: Dispatch the RO localizer subagent.** Give it: the final EN pattern three, the RO terminology + agreement table from the spec, `source/RO_STYLE_GUIDE.md`, and the current RO pattern three (:1671-1677). Ask for ONLY the RO prose mirroring Task 1's additions: the springboard tweak on :1677 ("hookify e granița fermă" -> extend to "granița fermă pe agent" or equivalent) and the 2-3 rung-three paragraphs. Enforce: neuter-plural agreement ("hook-uri versionate/rapide/deterministe"); `gate` stays English (never "poartă"); `--no-verify` untranslated in backticks; "committer" -> "oricine face commit"; "mirror" -> "CI-ul oglindește gate-ul local"; diacritics; ASCII hyphens only; no brand names.

- [ ] **Step 2: Integrate the heading.** Replace `**Pattern-ul trei: regulile hookify.**` (:1671) with `**Pattern-ul trei: două feluri de hook-uri.**`.

- [ ] **Step 3: Integrate the springboard + rung-three paragraphs** after the current RO pattern-three body (after :1677), before the `---` separator preceding pattern four.

- [ ] **Step 4: Verify markers + agreement + dashes.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && \
grep -n "Pattern-ul trei: două feluri de hook-uri" source/Ship_It_With_AI.RO.md && \
grep -niE "pre-commit|pre-push|--no-verify|manager de hook-uri" source/Ship_It_With_AI.RO.md | grep -c "" && \
echo "--- must be ZERO below ---" && \
grep -nE $'—|–' source/Ship_It_With_AI.RO.md | wc -l && \
grep -niE "poartă determinist|husky|lefthook|hook-uri versionat |gate determinista" source/Ship_It_With_AI.RO.md | wc -l
```
Expected: heading found; several term hits; dash count `0`; agreement/brand count `0`.

- [ ] **Step 5: Commit.**
```bash
git add source/Ship_It_With_AI.RO.md
git commit -m "content(ch9): pattern-ul trei devine două feluri de hook-uri - hook-uri de git (RO)"
```

---

### Task 5: RO deterministic ripple edits

**Files:**
- Modify: `source/Ship_It_With_AI.RO.md` recap :1703; pattern-eight :1767; closing :1777; artifact :1783

- [ ] **Step 1: Recap (:1703).** In `Patru pattern-uri. Worktree-uri. Championi. Reguli hookify. PR review toolkit.` replace `Reguli hookify.` with `Hook-uri.`

- [ ] **Step 2: Pattern-eight (:1767).** In `... workflow-ul de CI și regulile de hook stau în spatele unei reguli de deny (pattern-ul trei).` replace `regulile de hook stau` with `regulile hookify stau`.

- [ ] **Step 3: Closing (:1777).** In `Primele patru - worktree-uri, championi, reguli hookify, PR review toolkit - se aplică pe scară largă.` replace `reguli hookify` with `hook-uri`.

- [ ] **Step 4: Artifact (:1783).** Broaden the body `... un hook pre-tool-use pentru categoriile de acțiuni periculoase și un checklist de review de PR ...` to add the git side, e.g. `... un hook pre-tool-use pentru acțiunile periculoase, un gate de git la commit/push pentru cele mecanice și un checklist de review de PR ...`. Keep the title `pattern-ul worktree + hook + review.` unchanged.

- [ ] **Step 5: Verify.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && \
grep -n "Championi. Hook-uri. PR review toolkit" source/Ship_It_With_AI.RO.md && \
grep -n "regulile hookify stau în spatele" source/Ship_It_With_AI.RO.md && \
grep -n "championi, hook-uri, PR review toolkit" source/Ship_It_With_AI.RO.md && \
grep -niE "opt pattern-uri" source/Ship_It_With_AI.RO.md && \
grep -nE $'—|–' source/Ship_It_With_AI.RO.md | wc -l
```
Expected: first three greps match; "opt pattern-uri" still present; dash count `0`.

- [ ] **Step 6: Commit.**
```bash
git add source/Ship_It_With_AI.RO.md
git commit -m "content(ch9): ripple edits pentru două-feluri-de-hook-uri (RO)"
```

---

### Task 6: RO review pass (agreement + diacritics)

- [ ] **Step 1: Dispatch the RO reviewer subagent** (or fold into Task 4's localizer if same session). Give it the final RO pattern three + `RO_STYLE_GUIDE.md` + the agreement table. Check ONLY: gender/number agreement (the neuter-plural flip especially), diacritics complete, romgleza register consistent with the chapter, `gate`/`--no-verify` untouched, no dashes, meaning matches the EN. Return exact fixes or "clean".

- [ ] **Step 2: Apply any fixes**, then re-run Task 4 Step 4 + Task 5 Step 5 greps.

- [ ] **Step 3: Commit (only if fixes were applied).**
```bash
git add source/Ship_It_With_AI.RO.md
git commit -m "content(ch9): RO agreement/diacritics fixes on two-kinds-of-hooks"
```

---

### Task 7: Changelog entries (both editions) - DEFAULT ON, drop if user declined

**Files:**
- Modify: `source/Ship_It_With_AI.md` Changelog section (~:2079); `source/Ship_It_With_AI.RO.md` Changelog (~:2081)

- [ ] **Step 1: Read the current changelog format** in both files (top entry) to match heading style and prose length exactly.

- [ ] **Step 2: Add a dated 2026-07-05 entry to EN** matching the format: one short paragraph noting pattern three now covers two kinds of hooks (agent hooks + git commit/push hooks), and why (the agent is just another committer; `--no-verify` closed by a deny rule). No em dashes.

- [ ] **Step 3: Add the mirrored RO entry** per style guide.

- [ ] **Step 4: Verify.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && \
grep -n "2026-07-05" source/Ship_It_With_AI.md source/Ship_It_With_AI.RO.md && \
grep -nE $'—|–' source/Ship_It_With_AI.md source/Ship_It_With_AI.RO.md | wc -l
```
Expected: 2026-07-05 present in both; dash count `0` (changelog headings in this book use ASCII per house rule).

- [ ] **Step 5: Commit.**
```bash
git add source/Ship_It_With_AI.md source/Ship_It_With_AI.RO.md
git commit -m "content: changelog entry for two-kinds-of-hooks (EN + RO)"
```

---

### Task 8: Build, verify, and marker sweep (STOP before deploy)

**Files:** none (build output only).

- [ ] **Step 1: Build the site.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && python3 build/build_spa.py
```
Expected: build succeeds, no placeholder/template errors.

- [ ] **Step 2: Smoke check.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && bash build/tests/smoke_check.sh _site
```
Expected: PASS.

- [ ] **Step 3: Full site verify (run BARE - never piped into tail in the same chain as a commit).**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && SITE_NO_REBUILD=1 npm --prefix build run verify:site
```
Expected: all assertions pass (including verify_seo_pass.js).

- [ ] **Step 4: Rendered-page marker sweep (both editions).**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && \
grep -rl "two kinds of hooks" _site/read/ && \
grep -rl "două feluri de hook-uri" _site/ro/ && \
grep -rnE $'—|–' _site/read/index.html _site/ro/read/index.html | wc -l
```
Expected: EN + RO markers found in rendered output; dash count `0`.

- [ ] **Step 5: Reset Playwright screenshot byte-churn.**
```bash
cd /home/mihai/ai-labs/ship-it-with-ai && git checkout -- build/tests/screenshots 2>/dev/null; git status --short
```
Expected: no stray screenshot diffs staged.

- [ ] **Step 6: STOP. Present the diff to the user.** Do NOT merge to main or deploy. Summarize what changed (both editions), confirm all checks green, and ask for approval to merge `ch9-git-hooks` -> main (which triggers the GitHub Pages deploy). On approval: merge, push, poll deploy ~120s, curl-marker-sweep https://ship-it-with.ai/read/ and /ro/read/, then re-ping IndexNow per the indexnow-key memory.

---

## Self-Review

**Spec coverage:** placement (Task 1 heading + rung three); load-bearing spine (Task 1 Step 1 requirements); technical corrections (Global Constraints + Task 1/3 checks); EN ripple x4 (Task 2); RO mirror (Task 4); RO ripple x4 (Task 5); RO agreement (Tasks 4/6); house style + dashes (every verify step); changelog (Task 7, flagged optional); verification plan (Task 8). All spec sections map to a task.

**Placeholder scan:** deterministic edits carry exact before/after strings; generative prose carries explicit acceptance criteria + drafting prompt (the honest form for authored content - the exact final paragraphs are produced by the drafter at execution, then gated by Task 3/6 review and the grep/build checks). No "TBD"/"handle edge cases"/"similar to Task N".

**Type consistency:** the pattern name "two kinds of hooks" / "două feluri de hook-uri", the disambiguation "hookify rules" / "regulile hookify", and the recap/closing "Hooks" / "hook-uri" / "hooks" are used identically across Tasks 1, 2, 4, 5. The `--no-verify`, "hook manager", "git commit/push gate" vocabulary is consistent EN-side; the RO renderings match the spec table.
