# Spec: git commit/push hooks join Chapter 9 pattern three — 2026-07-05

Goal (user): "in chapter 9 we should also mention github pre-commit/pre-push hooks that should be
used alongside hooks and pr reviews. spawn a team of experts to help out adding that part, use
superpowers to spec plan and do it."

Vetting: four expert reviewers (technical/domain, authorial-voice/structure, RO localization,
adversarial skeptic) read the chapter and vetted the design. Their converged verdict and corrections
are baked into the decisions below (not left as open FACT SLOTS - the technical review is the
fact-check for a section this size).

## Placement decision

**Expand Chapter 9 pattern three from "hookify rules" into "two kinds of hooks."** Count stays EIGHT.
Rationale:
- Git commit/push hooks belong in the same "structural enforcement vs polite request" family the
  pattern already runs (AGENTS.md request -> hookify boundary). They are the third rung of that
  ladder, not a new operating pattern a team installs *for* agentic work.
- The intro (:1641 EN / :1643 RO) already names this pattern "hooks" generically ("worktrees,
  champions, hooks, and PR review"), so a "two kinds of hooks" heading aligns the section title with
  what the intro already calls it. An un-numbered bridge wedged between patterns three and four would
  break that clean first-four enumeration worse than extending pattern three does.
- The naming-collision risk (the book gave "hook" a narrow meaning - agent pre-tool-use, defined in
  Ch3 ~:665) is turned into a deliberate teaching beat by naming the collision, not papered over.
  Done as an *extended ladder*, the addition SHARPENS "hookify = agent boundary": hookify's
  agent-specificity stands out precisely because it now sits beside a sibling that binds everyone.
- Form: bold-paragraph heading (`**Pattern three: two kinds of hooks.**`), matching patterns 1-8.
  NO new `##` section, NO `###` inside Ch9. SECTION_SLUGS / EXPECTED_PAGE_COUNT unchanged. No build
  config change.

**Rejected:** ninth pattern (renumbers the whole chapter, rewrites "eight patterns" x4 + recaps +
artifact - most invasive); un-numbered bridge (skeptic's pick - breaks the first-four enumeration,
and the collision is better handled by naming it than by hiding the material elsewhere).

## The load-bearing spine (why this is not devops boilerplate)

The skeptic's decisive objection: "set up pre-commit hooks to run lint" is 2015 hygiene a senior
reader already runs with or without AI. The addition earns its place ONLY on the agentic spine, which
must be central, not decorative:

1. The agent is **just another committer**. A deterministic commit/push gate applies to it for free,
   the same as to every human author - no agent-specific wiring needed.
2. The agent's escape hatch is `--no-verify` (and it can also edit the hook config). You close the
   agent's hatch with a **hookify deny rule** - pattern three's other half. The two boundaries cover
   each other's blind spot: hookify catches the agent mid-session; the git gate + CI catch every
   author (and every path) hookify never sees.
3. Honest hierarchy (both technical + skeptic reviewers insisted): **local hooks are fast feedback,
   not enforcement.** They are bypassable and may not be installed on a given machine. **CI is the
   real gate** - and pattern eight already owns that argument, so reference it, do not rebuild it.

## New-rung content skeleton (target +2 to +3 paragraphs; hard cap +3)

Keep hookify text (:1671-1677) essentially unchanged as the first two rungs. Rework the :1675 motif
("AGENTS.md is the polite request. hookify is the firm boundary.") from the pattern's closer into the
springboard to the third rung. Then:

1. **Name the collision, introduce the second kind.** The word "hook" now points at two mechanisms:
   the agent's pre-tool-use hook (above) and git's commit/push hook. The git hook fires at
   commit/push time, runs for every author, and is a deterministic script - not LLM judgment. The
   sharpest line to keep: *deterministic checks don't drift the way probabilistic reviewers can - a
   secret scanner either finds the key or it doesn't.*
2. **What runs where + why it is lean.** pre-commit = fast/local (format, lint, typecheck,
   secret-scan); pre-push = heavier (the fast test suite, the build). Keep it seconds or people reach
   for the escape hatch. Managed from a versioned config (generic "a hook manager" - NO brand names)
   so the hook installs for everyone rather than living un-versioned in `.git/hooks`.
3. **The payoff beat (mutual protection, agentic spine).** `--no-verify` is the agent's one-line
   escape hatch, closed by a hookify deny rule. Local hooks are feedback; the same checks in CI are
   the gate the agent cannot skip from its laptop - and the hook config + CI workflow are themselves
   agent-editable files, which is exactly pattern eight's "gate the agent cannot edit." One clause
   ties the git gate to pattern eight; do not expand it (pattern eight owns the outer-loop argument).

## Vetted technical corrections (must hold)

- Say **"git hooks"**, never "GitHub hooks." pre-commit/pre-push are client-side git hooks; GitHub's
  server-side controls (Actions, branch protection, push rules) are a different mechanism.
- **Tests belong in pre-push, not pre-commit.** Tests in pre-commit are the classic reason people
  reach for `--no-verify`. pre-commit = format/lint/typecheck/secret-scan (fast); pre-push = suite +
  build.
- **CI is not "un-bypassable."** It is authoritative only when the CI workflow + branch-protection
  config sit outside the committer's write scope and admin/ruleset bypass is disabled. Frame it as
  "the check you cannot skip from your laptop" / "runs regardless of local setup," and tie the
  config-must-be-agent-uneditable point to pattern eight rather than overclaiming.
- **`--no-verify` narrows, does not seal.** Other local skips exist (`core.hooksPath`, hook-manager
  env vars, editing the config, an absent/non-executable hook). Do not imply the local gate is
  airtight; that is why CI is the enforcement layer. The deny rule is hygiene; CI is enforcement.
- Long-flag only in prose: `--no-verify`. (Note for whoever writes the deny rule: `git commit -n` ==
  `--no-verify`, but `git push -n` == `--dry-run`. Prose uses the long form for both - correct.)
- No brand-drop at mechanism level (no husky / lefthook / pre-commit-framework in prose). "A hook
  manager," generic - matches the book never brand-dropping mechanisms.

## Ripple edits (EN + RO, mirrored per the dual-edition rule)

EN (`source/Ship_It_With_AI.md`):
- :1669 heading `**Pattern three: hookify rules.**` -> `**Pattern three: two kinds of hooks.**`
- :1675 motif line -> reworked as the springboard to rung three (not the closer).
- :1701 recap `... Champions. hookify rules. PR review toolkit.` -> `... Champions. Hooks. PR review
  toolkit.`
- :1765 outer-loop line `... and hook rules sit behind a deny rule (pattern three).` -> disambiguate
  `hook rules` -> `hookify rules` (restore the agent-specific label now that the pattern holds two
  kinds; keep the `(pattern three)` ref). One-word fix; do NOT expand. NOTE the deliberate split: the
  *pattern* is now named "hooks" (recap/closing), but this specific agent-side deny mechanism stays
  "hookify" - that is coherent, not inconsistent.
- :1775 closing `... champions, hookify rules, PR review toolkit ...` -> `... champions, hooks, PR
  review toolkit ...`
- :1781 artifact box: title `Worktree + hook + review` stays; body broadened to name the commit-time
  gate alongside the pre-tool-use hook.
- :1641 intro: NO change (already "hooks", now more accurate).

RO (`source/Ship_It_With_AI.RO.md`) - mirror each, per RO_STYLE_GUIDE + established lexicon:
- :1671 heading -> `**Pattern-ul trei: două feluri de hook-uri.**`
- :1677 motif `... hookify e granița fermă.` -> springboard to rung three.
- :1703 recap `Reguli hookify.` -> `Hook-uri.`
- :1767 outer-loop `regulile de hook stau în spatele unei reguli de deny (pattern-ul trei)` ->
  `regulile hookify stau în spatele unei reguli de deny (pattern-ul trei)` (restore agent-specific
  label; keep the (pattern-ul trei) ref).
- :1777 closing `... championi, reguli hookify, PR review toolkit` -> `... championi, hook-uri, PR
  review toolkit`.
- :1783 artifact body -> add the git side, e.g. `un hook de agent (pre-tool-use) pentru acțiunile
  periculoase și hook-uri de git (pre-commit / pre-push) ca gate determinist pentru oricine face
  commit`.
- :1643 intro: NO change (already "hook-uri").

## RO terminology + agreement (from the localization review)

Stay English-articulated: hook(-uri), pre-commit, pre-push, commit, push, lint, typecheck, build, CI,
gate, hookify, `--no-verify`, deny, required status check, bypass, formatter.
Get a Romanian word: determinist, scanarea de secrete, teste unitare, formatare, verificare de
tipuri, configurație versionată, manager de hook-uri, jumătăți, oglindește.
Paraphrase (never calc): "committer" -> "oricine face commit" (NOT "committer-ul"); "mirror" ->
"CI-ul oglindește gate-ul local"; "required status check" stays English.

Gender / agreement traps (highest-frequency error = neuter-plural flip):
- `hook`, `gate` are neuter: sg masculine, **pl feminine** -> "hook-uri **versionate / rapide /
  deterministe**", "gate-uri **deterministe**" (NEVER singular-masculine endings in the plural).
- `regula` (fem) -> aplicată/deterministă; `scanarea` (fem) -> rapidă; `configurația` (fem) ->
  versionată; `suita` (fem) -> completă/verde; `managerul` (masc) -> versionat; `commit-ul` /
  `push-ul` (masc); `jumătățile` (fem) -> "cele două jumătăți se protejează reciproc".
- `gate` stays English (style guide bans "poartă"); never translate/mangle `--no-verify`.

## House-style constraints (hard)

- Spaced hyphen ` - ` in body prose. NO em/en dashes anywhere (content, commit msg, PR body) - ASCII
  hyphen only. This overrides any harness default.
- No Claude/Anthropic commit co-author trailer; no `Claude-Session` trailer. Commits look
  human-authored.
- Do NOT introduce any verify_seo_pass.js /read/ blocklist substring ("six primitives", "the other
  five", etc.). This section is about git hooks - low risk - but the drafter must not paraphrase into
  a banned string.
- opencode lowercase, never sentence-initial. AGENTS.md bare link at most once per chapter (Ch9
  already links it in pattern two / champions, ~:1661 both editions) - new prose uses plain
  "AGENTS.md", no repeat link.
- No fabricated forensics: no invented failure story (line ~:1691 reserves the named-failure device
  for pattern four; pattern three must NOT acquire one). No invented dates/metrics/companies.
- Proportion: pattern three ends at ~6-7 short paragraphs total. Do not inflate the hookify half to
  "balance" the new half - hookify stays the spine, git hooks arrive lean.

## Out of scope / deferred (conscious omissions)

- **Changelog entry.** The book self-documents content updates in its Changelog section (both
  editions). Precedent (2026-06-10 outer-loop spec) added one. This is a real edit but a scope-add
  beyond "add the git-hooks content." DEFAULT: add a short dated entry (2026-07-05) to both editions
  matching the existing format, since a reader-facing content change belongs in the changelog. Flag
  to user at plan review; drop if they prefer the content-only change.
- **"A note on dated claims" global date.** Leave as-is. This addition does not change the book's
  overall freshness window; bumping the global "current as of" date implies a full freshness pass
  this is not.
- **Pattern eight expansion.** One clause tie-in only. Pattern eight owns the outer-loop / CI-gate
  argument; do not relitigate it in pattern three.

## Execution: the expert team (post-plan)

Lean team, <=4 concurrent, ~4 total (well under limits):
1. EN drafter - writes rung-three prose in the chapter's exact voice from this skeleton.
2. Editorial reviewer - voice match, no fabrication, dash sweep, proportion, blocklist check.
3. RO localizer - mirrors into RO per the terminology + agreement plan above.
4. (Optional) RO reviewer - agreement/diacritics pass, or fold into the localizer.

## Verification plan

1. `python3 build/build_spa.py`, then `bash build/tests/smoke_check.sh _site`.
2. `SITE_NO_REBUILD=1 npm --prefix build run verify:site` - run bare; never pipe into tail in the
   same chain as a commit (pipeline exit-code trap).
3. 0-dashes sweep on both source files and rendered pages; JSON-LD parse still valid.
4. Confirm the chapter still reads "eight patterns" (intro, recap, closing) and renders in both
   editions; pattern-three page shows the new heading + rung-three markers, both langs.
5. `git checkout -- build/tests/screenshots` before committing (Playwright byte-churn).
6. Commit on branch `ch9-git-hooks` (no Claude attribution). Do NOT merge to main / deploy until the
   user approves. On approval: merge -> push -> poll deploy ~120s -> curl marker sweep on
   https://ship-it-with.ai/read/ and /ro/read/ -> re-ping IndexNow.
