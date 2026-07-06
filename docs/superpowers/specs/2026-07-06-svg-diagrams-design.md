# Spec+plan: SVG diagrams (loop, layers, arc) + localized diagram bodies — 2026-07-06

Goal (user): "Make svg diagrams!" - full-read review item #5. Scope decided with user:
**3 SVG + 2 kept**: the six-phase loop (Ch5), governance layers (Ch3), and 90-day arc (Ch10) become
inline theme-aware SVG; the primitives harness (Ch1) and traffic light (Ch8) stay HTML cards (they
already reflow well). In ALL five: RO pages get localized bodies (today the renderers hardcode
English and only swap the figcaption), and the arc's "CLAUDE.md drafted/hardened" drift is fixed to
AGENTS.md (both source editions say AGENTS.md).

## Discovery that reframed the work

The site never showed ASCII: `build_spa.py` (:405-:609) replaces each fenced figure + `*Figure:*`
caption with HTML via `FIGURE_RENDERERS_BY_CAPTION_KEY`, rebound per language in `set_language()`
(:3182 EN, :3228 RO). Bugs found: RO bodies are English; arc says CLAUDE.md. The markdown ASCII
stays the canonical source (llms-full.txt keeps it); this change is presentation-layer only.

## Design (per dataviz skill: tokens for both themes, ink for text, one accent)

- Inline SVG inside the existing `<figure class="diagram diagram-*">` wrappers; all styling via
  classes defined in `spa_template.html` CSS using existing tokens (`--color-surface`, `--color-text`,
  `--color-text-soft/muted`, `--color-border-strong`, `--color-accent`, `--color-accent-soft`) so
  light/dark both deliberate. `role="img"` + localized `<title>`; figcaption stays the visible caption.
- Portrait-leaning viewBoxes with max-width caps so text stays legible at 360px:
  - **loop**: vertical chain of 6 numbered nodes, real arrows down, two dashed accent feedback
    curves on the right: Execute -> Plan ("failed plan? replan" / "plan eșuat? replanifici"),
    Verify -> Plan ("failed verify? back to plan" / "verify picat? înapoi la plan"). max-width ~460px.
  - **layers**: the five-bar defense wall (Layer 5 top -> Layer 1 bottom), num/name/desc per bar;
    the existing `.layers-spine` HTML line stays below the SVG (reflows). max-width ~560px.
  - **arc**: vertical timeline, left rail with day ranges + progression arrows, three panels
    (period small-caps accent, phase bold, items 14px pre-wrapped, role chip). max-width ~520px.
- Labels from a new module-global `DIAGRAM_LABELS` dict rebound in `set_language()` (same pattern as
  the caption keys). RO strings VERBATIM from the RO ASCII bodies (harvested): loop feedback labels;
  layers "Stratul N / Telemetrie (detectiv) / Hook-uri de securitate (per acțiune) / Secrete
  (protecție structurală) / Sandbox (izolare la nivel de OS) / Permisiuni (allow / ask / deny)";
  arc "Zilele 1-30 Fundația / 31-60 Extinderea / 61-90 Operaționalizarea" + RO items + roles stay
  Champion/Lead/Manager; traffic "VERDE/GALBEN/ROȘU", modes "Condus de agent, viteză normală" /
  "Condus de om, sprijin de agent" / "Stop. Repară întâi codebase-ul.", title "Semnale (numără
  fiecare semnal prezent)", the 8 RO signal names; primitives: only the harness foot is RO ("bucla
  agentului le leagă pe toate; subagenții pornesc instanțe-copil constrânse ale agentului însuși") -
  the RO source deliberately keeps primitive names + "the agent, recursively" in English.
- Figcaption unification: renderers emit a `__FIGCAPTION__` placeholder; `replace_diagrams`
  substitutes the SOURCE caption for every language (drops the EN special-case; EN loop caption
  regains its second sentence).
- Prune the now-dead CSS for old `.diagram-loop .phase*`, `.diagram-layers .layer*` (keep
  `.layers-spine`), `.diagram-arc .arc-*` blocks; add the new `.dsvg-*` rules.

## Tasks

1. `build_spa.py`: DIAGRAM_LABELS (EN + RO rebind); rewrite loop/layers/arc renderers as SVG;
   parameterize primitives foot + traffic labels; AGENTS.md fix; figcaption placeholder mechanism.
2. `spa_template.html`: new `.dsvg-*` CSS (both themes come free via tokens); prune dead blocks.
3. Build; screenshot all 5 figures x EN/RO x light/dark; I review the images (dataviz step 7).
4. Tests: confirm nothing asserts old loop/layers/arc classes or the short EN captions
   (chapter-1 primitives assertions untouched by design); run smoke + verify:site.
5. Changelog entry (site-level precedent, e.g. the SEO-pass entry): one dated entry per edition.
6. Review-gate: one code-reviewer subagent on the full diff; fix loop; STOP for deploy approval.
7. Deploy: merge -> push -> `gh run view --json conclusion` -> curl live markers -> IndexNow.

## Constraints

No em/en dashes in any new text; ASCII sources in markdown untouched (presentation only, except
nothing in source changes at all this round); RO strings verbatim from RO ASCII; no new npm deps;
`EXPECTED_PAGE_COUNT` / section slugs unchanged; no Claude commit trailers; branch `svg-diagrams`.
