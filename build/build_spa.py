#!/usr/bin/env python3
"""Build the single-file SPA HTML from Ship_It_With_AI.md.

Usage: python3 build_spa.py
Output: ship_it_with_ai.html (single self-contained file)
"""

import os
import re
import subprocess
import sys
import json
import html as html_lib
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

try:
    import markdown
except ImportError:
    sys.exit("build_spa.py: missing dependency. Run: pip install -r build/requirements.txt")

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
SOURCE = REPO_ROOT / "source" / "Ship_It_With_AI.md"
SITE_DIR = REPO_ROOT / "_site"
STATIC_DIR = HERE / "static"
TEMPLATE_PATH = HERE / "spa_template.html"

# Canonical site origin, used to build absolute URLs. Kept as a constant so the
# per-language URL prefix (below) is the only thing that varies between builds.
BASE = "https://ship-it-with.ai"

# Per-language build context. set_language() (near the bottom of this file)
# rebinds these before each language pass. URL_PREFIX is "" for the default
# English build and "/ro" for the Romanian build; CFG carries every
# language-variant label, marker, and UI string. Functions read these globals
# at call time, so the English pass reproduces the historical output exactly.
URL_PREFIX = ""
CFG = None  # type: ignore[assignment]  # set by set_language() before any build


def _abs(path: str) -> str:
    """Absolute canonical URL for a site-internal path (path starts with '/')."""
    return f"{BASE}{URL_PREFIX}{path}"


def _rel(path: str) -> str:
    """Language-prefixed site-internal href (path starts with '/').

    Asset paths (favicon, cover, deferred.css) are deliberately NOT routed
    through this helper - they live at the site root and are shared across
    languages.
    """
    return f"{URL_PREFIX}{path}"


def _content_date() -> datetime:
    """Deterministic build timestamp for sitemap lastmod / JSON-LD dateModified.

    Resolution order: SOURCE_DATE_EPOCH env override -> the source file's last
    git commit date -> the source file's mtime. Never datetime.now(), so an
    unchanged source rebuilds byte-identically and lastmod reflects the last
    *content* edit rather than when CI happened to run.
    """
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc)
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(SOURCE)],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return datetime.fromisoformat(out).astimezone(timezone.utc)
    except Exception:
        pass
    return datetime.fromtimestamp(SOURCE.stat().st_mtime, tz=timezone.utc)


# ---------------------------------------------------------------------------
# Section model - SECTION_SLUGS + parser + anchor index
# ---------------------------------------------------------------------------

# (kind, identifying_text) → URL slug. identifying_text is the chapter title
# for chapters/about/foreword/etc., or "Appendix X" for appendices, or the
# heading-detected anchor for prologue.
SECTION_SLUGS: dict[tuple[str, str], str] = {
    ("foreword", "Foreword"):                                       "foreword",
    ("prologue", "Nine seconds"):                                   "prologue-nine-seconds",
    ("chapter", "The primitives"):                                  "chapter-1-primitives",
    ("chapter", "The anatomy invariant"):                           "chapter-2-anatomy-invariant",
    ("chapter", "Governance in layers"):                            "chapter-3-governance-in-layers",
    ("chapter", "From generating code to shipping software"):       "chapter-4-from-generating-code-to-shipping-software",
    ("chapter", "The six-phase loop"):                              "chapter-5-six-phase-loop",
    ("chapter", "AGENTS.md as team infrastructure"):                "chapter-6-agents-md",
    ("chapter", "Architecture Review: Documentation and Diagnosis"):"chapter-7-architecture-review",
    ("chapter", "Readiness: The Kill Signals and the Traffic Light"):"chapter-8-readiness-kill-signals",
    ("chapter", "Patterns for brownfield codebases"):               "chapter-9-brownfield-patterns",
    ("chapter", "Adoption: 90 days, three roles"):                  "chapter-10-adoption-90-days",
    ("closing", "Closing"):                                         "closing",
    ("acknowledgments", "Acknowledgments"):                         "acknowledgments",
    ("about", "About the author"):                                  "about-the-author",
    ("changelog", "Changelog"):                                     "changelog",
    ("appendix", "A"):                                              "appendix-a-cost-economics",
    ("appendix", "B"):                                              "appendix-b-templates",
    ("appendix", "C"):                                              "appendix-c-sources",
}

# Sanity: no slug collisions.
_seen: set[str] = set()
for _k, _v in SECTION_SLUGS.items():
    if _v in _seen:
        raise RuntimeError(f"duplicate slug in SECTION_SLUGS: {_v}")
    _seen.add(_v)

# Single source of truth for how many per-section pages the build must emit.
# Used by the build's own print + the CI smoke check.
EXPECTED_PAGE_COUNT = len(SECTION_SLUGS)  # 19 as of this pass

# Document-order slug list. Translated builds (whose headings don't match the
# English SECTION_SLUGS keys) assign slugs positionally from this list - the
# translation mirrors the English structure section-for-section, so position is
# a reliable join key and keeps URLs identical across languages.
CANONICAL_SLUG_ORDER = list(SECTION_SLUGS.values())


SectionKind = Literal["foreword", "prologue", "chapter", "closing",
                      "acknowledgments", "about", "changelog", "appendix"]


@dataclass
class Section:
    kind: SectionKind
    slug: str
    title: str            # H1 text on the chapter page
    body_md: str          # raw markdown for the body
    reading_time_min: int | None = None
    part_slug: str | None = None  # "part-i" / "part-ii" / "part-iii" - chapters only
    h2_subsections: list[tuple[str, str]] = field(default_factory=list)


_PART_RE = re.compile(r"^# Part ([IVX]+) - (.+)$")
_PROLOGUE_RE = re.compile(r"^# Prologue\s*$")
_CLOSING_RE = re.compile(r"^# Closing\b.*$")
_CHAPTER_NUM_RE = re.compile(r"^## Chapter \d+\s*$")
_CHAPTER_TITLE_RE = re.compile(r"^## (.+)$")
_FOREWORD_RE = re.compile(r"^## Foreword\b.*$")
_PROLOGUE_H2_RE = re.compile(r"^## (.+?)(?:\s*\{#([^}]+)\})?\s*$")
_ACK_RE = re.compile(r"^## Acknowledgments\b.*$")
_ABOUT_RE = re.compile(r"^## About the author\b.*$")
_CHANGELOG_RE = re.compile(r"^## Changelog\b.*$")
_APPENDIX_RE = re.compile(r"^## Appendix ([A-Z])\.\s*(.+)$")


def _part_slug(roman: str) -> str:
    return f"part-{roman.lower()}"


def parse_sections(md_text: str) -> list[Section]:
    """Walk the source markdown line-by-line, emit a Section per page-worthy
    heading. # Part X and # Prologue are containers (state) not sections.
    """
    lines = md_text.split("\n")
    sections: list[Section] = []
    current_part: str | None = None
    in_prologue_container = False
    part_ordinal = 0
    # English headings resolve their slug via the (kind, title) table; other
    # languages assign slugs positionally from the canonical document order.
    by_order = bool(CFG) and CFG.code != "en"

    cur_meta: tuple[str, str] | None = None
    cur_title: str = ""
    cur_part: str | None = None
    cur_body: list[str] = []

    def flush():
        nonlocal cur_meta, cur_title, cur_part, cur_body
        if cur_meta is None:
            cur_body = []
            return
        if by_order:
            slug = CANONICAL_SLUG_ORDER[len(sections)]
        else:
            slug = SECTION_SLUGS.get(cur_meta)
            if slug is None:
                raise RuntimeError(f"unknown section in SECTION_SLUGS: {cur_meta}")
        kind = cur_meta[0]
        body = "\n".join(cur_body).strip("\n")
        sections.append(Section(
            kind=kind, slug=slug, title=cur_title, body_md=body,
            part_slug=cur_part if kind == "chapter" else None,
        ))
        cur_meta = None
        cur_title = ""
        cur_part = None
        cur_body = []

    i = 0
    while i < len(lines):
        line = lines[i]

        m_part = _PART_RE.match(line)
        if m_part:
            # `# Part X` is a container, not a section. Flush the prior section
            # and zero out `cur_meta` so the part-intro lines (blockquote
            # epigraph + trailing `---`) that sit between `# Part X` and the
            # next `## Chapter N` don't get appended to the previous chapter's
            # body. Without this, /chapter-3-…/ would render the Part II
            # epigraph at its end, /chapter-7-…/ would render the Part III
            # epigraph, and /prologue-…/ would render the Part I epigraph.
            flush()
            # Slug by appearance order (part-i / part-ii / part-iii) so it is
            # language-independent - the roman numeral in the heading text is
            # only reliable in English.
            current_part = f"part-{['i', 'ii', 'iii'][part_ordinal]}"
            part_ordinal += 1
            i += 1
            continue

        if _PROLOGUE_RE.match(line):
            flush()
            in_prologue_container = True
            i += 1
            continue

        if _CLOSING_RE.match(line):
            flush()
            in_prologue_container = False
            cur_meta = ("closing", "Closing")
            cur_title = CFG.closing_label
            i += 1
            continue

        if _CHAPTER_NUM_RE.match(line):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines):
                m = _CHAPTER_TITLE_RE.match(lines[j])
                if m:
                    flush()
                    in_prologue_container = False
                    title = m.group(1).strip()
                    cur_meta = ("chapter", title)
                    cur_title = title
                    cur_part = current_part
                    i = j + 1
                    continue

        if _FOREWORD_RE.match(line):
            flush()
            in_prologue_container = False
            cur_meta = ("foreword", "Foreword")
            cur_title = CFG.foreword_label
            i += 1
            continue

        if _ACK_RE.match(line):
            flush()
            cur_meta = ("acknowledgments", "Acknowledgments")
            cur_title = CFG.ack_label
            i += 1
            continue

        if _ABOUT_RE.match(line):
            flush()
            cur_meta = ("about", "About the author")
            cur_title = CFG.about_label
            i += 1
            continue

        if _CHANGELOG_RE.match(line):
            flush()
            cur_meta = ("changelog", "Changelog")
            cur_title = CFG.changelog_label
            i += 1
            continue

        m_app = _APPENDIX_RE.match(line)
        if m_app:
            flush()
            letter = m_app.group(1)
            cur_meta = ("appendix", letter)
            cur_title = CFG.appendix_title_fmt.format(
                letter=letter, title=m_app.group(2).strip())
            i += 1
            continue

        if in_prologue_container:
            m = _PROLOGUE_H2_RE.match(line)
            if m and not line.startswith("### "):
                if cur_meta is None or cur_meta[0] != "prologue":
                    flush()
                    title = m.group(1).strip()
                    cur_meta = ("prologue", title)
                    cur_title = title
                i += 1
                continue

        cur_body.append(line)
        i += 1

    flush()

    if len(sections) != len(SECTION_SLUGS):
        raise RuntimeError(
            f"parse_sections produced {len(sections)} sections, "
            f"expected {len(SECTION_SLUGS)} (per SECTION_SLUGS table)"
        )

    return sections


_ANCHOR_RE = re.compile(r"\{#([a-z0-9-]+)\}")
_ATX_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")


def build_anchor_index(sections: list[Section]) -> dict[str, str]:
    """Map every anchor id in the source → the slug of the section that owns it.

    Anchors come from:
      - The section itself (the section's own slug is its primary anchor)
      - {#explicit-anchor} attributes on h2/h3 inside the section body
      - Auto-generated heading ids (markdown extension generates these from
        heading text); we mirror its slugify rule here approximately.
    """
    def _slugify(text: str) -> str:
        s = re.sub(r"[^\w\s-]", "", text.lower())
        s = re.sub(r"[\s_]+", "-", s).strip("-")
        return s

    index: dict[str, str] = {}

    for s in sections:
        index[s.slug] = s.slug
        if s.kind == "chapter":
            m = re.match(r"^chapter-(\d+)-", s.slug)
            if m:
                index[f"chapter-{m.group(1)}"] = s.slug
        if s.kind == "appendix":
            m = re.match(r"^appendix-([a-z])-", s.slug)
            if m:
                index[f"appendix-{m.group(1)}"] = s.slug
        if s.slug == "about-the-author":
            index["contact"] = s.slug
        if s.slug == "prologue-nine-seconds":
            index["nine-seconds"] = s.slug
        if s.slug == "foreword":
            index["foreword"] = s.slug

        for line in s.body_md.split("\n"):
            for m in _ANCHOR_RE.finditer(line):
                index[m.group(1)] = s.slug
            mh = _ATX_HEADING_RE.match(line)
            if mh and "{#" not in line:
                slug = _slugify(mh.group(1))
                if slug and slug not in index:
                    index[slug] = s.slug

    return index


# ---------------------------------------------------------------------------
# Site dir helpers
# ---------------------------------------------------------------------------

def reset_site_dir() -> None:
    """Empty _site/ so we don't leak deleted files between builds."""
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()


def copy_static() -> None:
    """Copy every file in build/static/ verbatim into _site/."""
    if not STATIC_DIR.exists():
        raise RuntimeError(f"missing static dir: {STATIC_DIR}")
    for p in STATIC_DIR.iterdir():
        if p.is_file():
            shutil.copy2(p, SITE_DIR / p.name)


# ---------------------------------------------------------------------------
# Diagram HTML generators
# ---------------------------------------------------------------------------

def diagram_primitives() -> str:
    return """<figure class="diagram diagram-primitives">
  <div class="harness">
    <div class="harness-label">THE HARNESS</div>
    <div class="primitives-grid">
      <div class="primitive"><div class="primitive-icon">◉</div><div class="primitive-name">context window</div></div>
      <div class="primitive"><div class="primitive-icon">⚙</div><div class="primitive-name">tools</div></div>
      <div class="primitive">
        <div class="primitive-icon">◫</div>
        <div class="primitive-name">permissions / sandbox</div>
        <div class="primitive-sublist">
          <span class="primitive-sub">decision layer</span>
          <span class="primitive-sub">OS enforcement</span>
        </div>
      </div>
      <div class="primitive"><div class="primitive-icon">✦</div><div class="primitive-name">skills</div></div>
      <div class="primitive"><div class="primitive-icon">▣</div><div class="primitive-name">plugins</div></div>
      <div class="primitive"><div class="primitive-icon">↔</div><div class="primitive-name">MCP</div></div>
      <div class="primitive">
        <div class="primitive-icon">▤</div>
        <div class="primitive-name">memory</div>
        <div class="primitive-sublist">
          <span class="primitive-sub">manually defined</span>
          <span class="primitive-sub">auto-memory system</span>
        </div>
      </div>
    </div>
    <div class="primitives-divider" aria-hidden="true"></div>
    <div class="primitives-recursive">
      <div class="primitive primitive-recursive"><div class="primitive-icon">⟲</div><div class="primitive-name">subagents</div><div class="primitive-note">the agent, recursively</div></div>
    </div>
    <div class="harness-foot">the agent loop binds them together;<br/>subagents spawn constrained child instances of the agent itself</div>
  </div>
  <figcaption>Figure: The primitives and the harness that runs them. Permissions / Sandbox sits in slot 3 as a primitive whose two halves - the agent-level decision layer and OS-level enforcement - converge on presence but diverge on posture across vendors. Memory is the other primitive whose second half is still mid-convergence. Subagents sit below the line because they are the recursive primitive: each subagent is itself an instance of the others.</figcaption>
</figure>"""


def diagram_layers() -> str:
    layers = [
        ("Layer 5", "Telemetry", "detective"),
        ("Layer 4", "Security hooks", "per-action enforcement"),
        ("Layer 3", "Secrets", "structural protection"),
        ("Layer 2", "Sandbox", "OS-level isolation"),
        ("Layer 1", "Permissions", "allow / ask / deny"),
    ]
    rows = "\n".join(
        f'    <div class="layer layer-{i+1}"><span class="layer-num">{n}</span><span class="layer-name">{name}</span><span class="layer-desc">{desc}</span></div>'
        for i, (n, name, desc) in enumerate(layers)
    )
    return f"""<figure class="diagram diagram-layers">
  <div class="layers-stack">
{rows}
  </div>
  <div class="layers-spine">Least privilege is the spine. Each layer catches what the others miss.</div>
  <figcaption>Figure: The five governance layers, layered as defense in depth.</figcaption>
</figure>"""


def diagram_loop() -> str:
    phases = ["Research", "Plan", "Execute", "Review", "Verify", "Ship"]
    nodes = "\n".join(
        f'    <div class="phase phase-{i+1}"><span class="phase-num">{i+1}</span><span class="phase-name">{name}</span></div>'
        for i, name in enumerate(phases)
    )
    return f"""<figure class="diagram diagram-loop">
  <div class="loop-flow">
{nodes}
  </div>
  <div class="loop-feedback">
    <span class="feedback-arrow">↻</span>
    <span class="feedback-text">Most failures route back to Plan, not back to Research</span>
  </div>
  <figcaption>Figure: The six-phase loop.</figcaption>
</figure>"""


def diagram_traffic_light() -> str:
    signals = [
        "No tests", "No documentation", "Tight coupling", "Scattered rules",
        "Regulatory constraints", "Team cannot evaluate output",
        "Model-context fit", "Velocity-of-change",
    ]
    signal_html = "\n".join(
        f'      <li><span class="sig-num">{i+1}</span>{name}</li>'
        for i, name in enumerate(signals)
    )
    return f"""<figure class="diagram diagram-traffic">
  <div class="traffic-light">
    <div class="light light-green"><span class="light-count">0 - 1</span><span class="light-label">GREEN</span><span class="light-mode">Agent-led, normal velocity</span></div>
    <div class="light light-yellow"><span class="light-count">2 - 3</span><span class="light-label">YELLOW</span><span class="light-mode">Human-led, agent support</span></div>
    <div class="light light-red"><span class="light-count">4 +</span><span class="light-label">RED</span><span class="light-mode">Stop. Fix codebase first.</span></div>
  </div>
  <div class="signal-list">
    <div class="signal-list-title">Signals (count each present)</div>
    <ol class="signal-grid">
{signal_html}
    </ol>
  </div>
  <figcaption>Figure: The kill signals and the traffic light decision rule. Signal 6 weighs more heavily than the others.</figcaption>
</figure>"""


def diagram_arc() -> str:
    phases = [
        ("Days 1 - 30", "Foundation", "Champion", [
            "Champion installs",
            "CLAUDE.md drafted",
            "First green-light project",
            "Architecture review workflow proven",
        ]),
        ("Days 31 - 60", "Expansion", "Lead", [
            "Lead onboards 2 - 3 more engineers",
            "CLAUDE.md hardened",
            "Hooks configured",
            "Skills written",
            "Kill signals applied to portfolio",
        ]),
        ("Days 61 - 90", "Productionization", "Manager", [
            "Manager folds metrics into normal velocity tracking",
            "Vendor governance signed",
            "Plugin marketplace policy in place",
        ]),
    ]
    cards = "\n".join(
        f"""    <div class="arc-card">
      <div class="arc-period">{period}</div>
      <div class="arc-phase">{phase}</div>
      <ul class="arc-items">
{chr(10).join(f'        <li>{item}</li>' for item in items)}
      </ul>
      <div class="arc-role">{role}</div>
    </div>"""
        for period, phase, role, items in phases
    )
    return f"""<figure class="diagram diagram-arc">
  <div class="arc-timeline">
{cards}
  </div>
  <figcaption>Figure: The 90-day adoption arc. Each phase has a primary role and a primary artifact set.</figcaption>
</figure>"""


# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------

# Match a fenced code block followed (after blank lines) by an italicized
# figure caption like `*Figure: ...*`. We capture the caption so each block
# can be routed to the right renderer by caption content (per-chapter
# rendering passes a subset of the document, not all 5 figures).
FIGURE_BLOCK_RE = re.compile(
    r"```\n.*?\n```\s*\n+\*Figur[ae]:\s+(?P<caption>[^*]+)\*\s*\n",
    re.DOTALL,
)


# Renderers keyed by a unique substring of their caption (more robust than
# document-order dispatch, which broke when per-chapter pages each contain a
# subset of the document's figures).
FIGURE_RENDERERS_BY_CAPTION_KEY: list[tuple[str, callable]] = [
    ("primitives and the harness",      diagram_primitives),
    ("five governance layers",          diagram_layers),
    ("six-phase loop",                  diagram_loop),
    ("kill signals and the traffic",    diagram_traffic_light),
    ("90-day adoption arc",             diagram_arc),
]


def replace_diagrams(md_text: str, *, strict: bool = True) -> str:
    """Replace ASCII figure blocks with HTML diagram placeholders.

    Dispatch is by caption-substring match so per-chapter rendering (where
    only some figures appear) works. `strict=True` (the default for the
    all-in-one pipeline) requires every renderer to fire exactly once;
    chapter-page rendering passes strict=False.
    """
    seen: list[str] = []

    def repl(match: re.Match) -> str:
        caption = match.group("caption").strip()
        for key, renderer in FIGURE_RENDERERS_BY_CAPTION_KEY:
            if key in caption:
                seen.append(key)
                html = renderer()
                # Translated builds replace the renderer's hardcoded English
                # figcaption with the source caption in the target language.
                # English keeps the renderer's caption verbatim (byte-stable).
                if CFG.code != "en":
                    html = re.sub(
                        r"<figcaption>.*?</figcaption>",
                        lambda _m: f"<figcaption>{CFG.figure_word}: {html_lib.escape(caption)}</figcaption>",
                        html,
                        count=1,
                        flags=re.DOTALL,
                    )
                return f"\n\n<!--RAW_HTML_START-->\n{html}\n<!--RAW_HTML_END-->\n\n"
        # Unknown caption - leave untouched.
        return match.group(0)

    result = FIGURE_BLOCK_RE.sub(repl, md_text)
    if strict and len(seen) != len(FIGURE_RENDERERS_BY_CAPTION_KEY):
        raise RuntimeError(
            f"Figure renderer/caption count mismatch: "
            f"{len(seen)} matched, {len(FIGURE_RENDERERS_BY_CAPTION_KEY)} renderers"
        )
    return result


# Chapter heading pattern: two consecutive `## ` lines. First is the number,
# second is the title.
CHAPTER_PAIR_RE = re.compile(
    r"^## (?P<num>Chapter \d+)\n## (?P<title>[^\n]+)$",
    re.MULTILINE,
)


def transform_chapter_headings(md_text: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Collapse `## Chapter N` + `## Title` pairs into one heading with an id.
    Returns (rewritten_md, [(id, num, title), ...])."""
    chapters: list[tuple[str, str, str]] = []

    def repl(match: re.Match) -> str:
        num = match.group("num")
        title = match.group("title").strip()
        # Language-independent anchor: chapter-<n> regardless of the heading
        # word ("Chapter"/"Capitolul"), so cross-refs and the part-mapping hold.
        slug = f"chapter-{re.search(r'[0-9]+', num).group(0)}"
        chapters.append((slug, num, title))
        # Use HTML directly so we have full control over markup
        return (
            f'<h2 id="{slug}" class="chapter-heading">'
            f'<span class="chapter-num">{num}</span>'
            f'<span class="chapter-title">{html_lib.escape(title)}</span>'
            f"</h2>"
        )

    return CHAPTER_PAIR_RE.sub(repl, md_text), chapters


PART_RE = re.compile(r"^# Part (?P<num>[IVX]+)\s*-\s*(?P<title>.+)$", re.MULTILINE)


def transform_part_headings(md_text: str) -> tuple[str, list[tuple[str, str, str]]]:
    parts: list[tuple[str, str, str]] = []
    ordinal = {"n": 0}

    def repl(match: re.Match) -> str:
        num = match.group("num").strip()
        title = match.group("title").strip()
        # Slug by appearance order so it is language-independent.
        slug = f"part-{['i', 'ii', 'iii'][ordinal['n']]}"
        ordinal["n"] += 1
        parts.append((slug, num, title))
        # H2 (not H1) so the article hero H1 is the only true H1 on the page.
        # Visual styling preserved via .article h2.part-heading CSS.
        return (
            f'<h2 id="{slug}" class="part-heading">'
            f'<span class="part-label">{CFG.part_word} {num}</span>'
            f'<span class="part-title">{html_lib.escape(title)}</span>'
            f"</h2>"
        )

    return PART_RE.sub(repl, md_text), parts


CLOSING_RE = re.compile(r"^# Closing\s*-\s*(?P<title>.+)$", re.MULTILINE)


def transform_closing(md_text: str) -> tuple[str, tuple[str, str] | None]:
    closing: tuple[str, str] | None = None

    def repl(match: re.Match) -> str:
        nonlocal closing
        title = match.group("title").strip()
        closing = ("closing", title)
        # H2 (not H1) - see transform_part_headings note.
        return (
            f'<h2 id="closing" class="closing-heading">'
            f'<span class="part-label">{CFG.closing_label}</span>'
            f'<span class="part-title">{html_lib.escape(title)}</span>'
            f"</h2>"
        )

    new_md = CLOSING_RE.sub(repl, md_text)
    return new_md, closing


PROLOGUE_RE = re.compile(r"^# Prologue\s*$", re.MULTILINE)


def transform_prologue(md_text: str) -> str:
    """Replace bare `# Prologue` with an <h2> so the page has one true H1.

    The actual story heading (`## Nine seconds`) provides the visible title;
    this banner just signals the section boundary, mirroring Part / Closing.
    """
    def repl(_match: re.Match) -> str:
        return (
            '<h2 id="prologue" class="prologue-heading">'
            f'<span class="part-label">{CFG.prologue_label}</span>'
            '</h2>'
        )

    return PROLOGUE_RE.sub(repl, md_text)


APPENDIX_RE = re.compile(r"^## (Appendix [A-Z])\. (.+)$", re.MULTILINE)


def transform_appendices(md_text: str) -> tuple[str, list[tuple[str, str, str]]]:
    appendices: list[tuple[str, str, str]] = []

    def repl(match: re.Match) -> str:
        label = match.group(1)
        title = match.group(2).strip()
        # Language-independent anchor: appendix-<letter> regardless of the
        # heading word ("Appendix"/"Anexa"). The letter is the trailing token
        # ("Appendix B" / "Anexa B"); a bare [A-Z] search would wrongly match
        # the capital in the heading word itself.
        slug = f"appendix-{label.split()[-1].lower()}"
        appendices.append((slug, label, title))
        return (
            f'<h2 id="{slug}" class="appendix-heading">'
            f'<span class="appendix-label">{label}</span>'
            f'<span class="appendix-title">{html_lib.escape(title)}</span>'
            f"</h2>"
        )

    return APPENDIX_RE.sub(repl, md_text), appendices


FOREWORD_TRANSFORM_RE = re.compile(r"^## Foreword\s*-\s*(?P<title>.+)$", re.MULTILINE)


def transform_foreword(md_text: str) -> tuple[str, tuple[str, str] | None]:
    foreword: tuple[str, str] | None = None

    def repl(match: re.Match) -> str:
        nonlocal foreword
        title = match.group("title").strip()
        foreword = ("foreword", title)
        return (
            f'<h2 id="foreword" class="foreword-heading">'
            f'<span class="appendix-label">{CFG.foreword_label}</span>'
            f'<span class="appendix-title">{html_lib.escape(title)}</span>'
            f"</h2>"
        )

    return FOREWORD_TRANSFORM_RE.sub(repl, md_text), foreword


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.strip().lower())
    return re.sub(r"[\s_-]+", "-", text)


# Appendix C - Sources and Further Reading: rewrite the four-bold-paragraph
# entries as semantic <article> cards with category accent.
SOURCE_GROUPS = {
    "Studies and research":                  ("study",    "Study"),
    "Named incidents":                       ("incident", "Incident"),
    "Vulnerabilities with patch versions":   ("vuln",     "Vulnerability"),
    "Tool documentation":                    ("docs",     "Tool documentation"),
    "Marketplaces and plugin ecosystems":    ("market",   "Marketplace"),
    "Memory primitive sources":              ("memory",   "Memory primitive"),
    "Permissions / Sandbox primitive sources": ("perms",  "Permissions / Sandbox primitive"),
}

SOURCE_ENTRY_RE = re.compile(
    r"<p>\s*"
    r"<strong>Claim:</strong>\s*(?P<claim>.*?)\s*"
    r"<strong>Source:</strong>\s*(?P<source>.*?)\s*"
    r"<strong>Where used:</strong>\s*(?P<where>.*?)\s*"
    r"<strong>Caveat:</strong>\s*(?P<caveat>.*?)\s*"
    r"</p>",
    re.DOTALL,
)


SOURCE_NOTE_RE = re.compile(
    r'<p><em>Source note\.\s*(?P<body>.*?)</em></p>',
    re.DOTALL,
)


def transform_source_notes(html: str) -> str:
    """Wrap inline `*Source note. ...*` italic paragraphs as styled callouts.

    Note: the regex halts at the first `</em>`, so source-note bodies must not
    contain nested italics. All current source notes are flat.
    """
    def repl(m):
        body = m.group("body").strip()
        return (
            '<aside class="source-note">'
            f'<span class="source-note-label">{CFG.source_note_label}</span>'
            f'<p>{body}</p>'
            '</aside>'
        )
    return SOURCE_NOTE_RE.sub(repl, html)


CLIPBOARD_SVG = (
    '<svg class="artifact-icon" viewBox="0 0 16 16" aria-hidden="true">'
    '<rect x="3" y="2" width="10" height="13" rx="1.5"></rect>'
    '<rect x="5.5" y="0.75" width="5" height="2.5" rx="0.5"></rect>'
    '<line x1="5" y1="6.5" x2="11" y2="6.5"></line>'
    '<line x1="5" y1="9" x2="11" y2="9"></line>'
    '<line x1="5" y1="11.5" x2="9" y2="11.5"></line>'
    '</svg>'
)

ARTIFACT_RE = re.compile(
    r'<p><strong>Artifact:\s*(?P<title>[^<]+?)\.</strong>\s*(?P<body>.*?)</p>',
    re.DOTALL,
)


def transform_artifacts(html: str) -> str:
    """Wrap **Artifact: TITLE.** body paragraphs into styled cards."""
    counter = {"n": 0}

    def repl(m):
        counter["n"] += 1
        slug = f"artifact-{counter['n']}"
        title = m.group("title").strip()
        body = m.group("body").strip()
        return (
            f'<aside class="artifact-box" id="{slug}">'
            '<div class="artifact-header">'
            f'{CLIPBOARD_SVG}'
            f'<span class="artifact-label">{CFG.artifact_label}</span>'
            '</div>'
            f'<p class="artifact-title">{title}</p>'
            f'<p>{body}</p>'
            '</aside>'
        )
    return ARTIFACT_RE.sub(repl, html)


AGENTS_LINK_RE = re.compile(r'<a href="https://agents\.md/?"[^>]*>AGENTS\.md</a>')
CHAPTER_SPLIT_RE = re.compile(r'(<h2 id="chapter-\d+"[^>]*>)')


def delink_repeated_agents_md(html: str, *, mode: str = "read") -> str:
    """Keep only the first AGENTS.md link per chapter; unwrap subsequent ones.

    Mode controls scope:
      'read': split on <h2 id="chapter-N"> so each chapter gets its own
              first-link allowance (the all-in-one /read/ page).
      anything else ('chapter', 'landing'): treat the whole html as one scope
              (per-chapter pages - there's only one chapter on the page).
    """
    if mode != "read":
        seen = {"flag": False}

        def keep_first_global(m):
            if seen["flag"]:
                return "AGENTS.md"
            seen["flag"] = True
            return m.group(0)

        return AGENTS_LINK_RE.sub(keep_first_global, html)

    parts = CHAPTER_SPLIT_RE.split(html)
    out = [parts[0]]
    i = 1
    while i < len(parts):
        h2 = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        seen = {"flag": False}

        def keep_first(m):
            if seen["flag"]:
                return "AGENTS.md"
            seen["flag"] = True
            return m.group(0)

        new_body = AGENTS_LINK_RE.sub(keep_first, body)
        out.extend([h2, new_body])
        i += 2

    return "".join(out)


HEADING_RE = re.compile(
    r'<(?P<tag>h2|h3) id="(?P<id>[^"]+)"(?P<attrs>[^>]*)>(?P<inner>.*?)</(?P=tag)>',
    re.DOTALL,
)
ARTIFACT_HEADER_RE = re.compile(
    r'(<aside class="artifact-box" id="(?P<aid>artifact-\d+)">\s*<div class="artifact-header">)',
    re.DOTALL,
)
SKIP_IDS = {'top', 'contact', 'about-the-author'}


def inject_anchor_links(html: str) -> str:
    """Add `<a class="anchor-link" href="#id">¶</a>` to h2/h3 and artifact-boxes.

    Preserves existing markdown {#anchor} ids (the markdown extension already set them).
    Skips ids in SKIP_IDS to avoid noise on the byline target and the About heading.
    """
    def head_repl(m):
        hid = m.group('id')
        if hid in SKIP_IDS:
            return m.group(0)
        tag = m.group('tag')
        attrs = m.group('attrs')
        inner = m.group('inner')
        anchor = f'<a class="anchor-link" href="#{hid}" aria-label="Copy link to section" tabindex="0">¶</a>'
        return f'<{tag} id="{hid}"{attrs}>{inner}{anchor}</{tag}>'

    html = HEADING_RE.sub(head_repl, html)

    def art_repl(m):
        aid = m.group('aid')
        anchor = f'<a class="anchor-link" href="#{aid}" aria-label="Copy link to artifact" tabindex="0">¶</a>'
        return m.group(1) + anchor

    html = ARTIFACT_HEADER_RE.sub(art_repl, html)
    return html


def transform_source_cards(html: str) -> str:
    # Annotate the known H3 group headings with .source-group + id slug.
    for group_title in SOURCE_GROUPS:
        html = re.sub(
            rf"<h3>{re.escape(group_title)}</h3>",
            lambda m, t=group_title: f'<h3 id="{slugify(t)}" class="source-group">{t}</h3>',
            html,
            count=1,
        )
    # Walk headings and entries in document order so each card picks up
    # the category from the most recent group heading.
    heading_re = re.compile(
        r'<h3 id="[^"]+" class="source-group">(?P<title>[^<]+)</h3>'
    )
    current_cat = CFG.source_default_cat
    events = []
    for m in heading_re.finditer(html):
        events.append((m.start(), "heading", m))
    for m in SOURCE_ENTRY_RE.finditer(html):
        events.append((m.start(), "entry", m))
    events.sort(key=lambda e: e[0])

    pieces: list[str] = []
    cursor = 0
    for pos, kind, m in events:
        pieces.append(html[cursor:m.start()])
        if kind == "heading":
            title = m.group("title").strip()
            current_cat = SOURCE_GROUPS.get(title, current_cat)
            pieces.append(m.group(0))
        else:
            cat_attr, cat_label = current_cat
            claim = m.group("claim").strip()
            source = m.group("source").strip()
            where = m.group("where").strip()
            caveat = m.group("caveat").strip()
            pieces.append(
                f'<article class="source-card" data-cat="{cat_attr}">\n'
                f'  <span class="source-card-cat">{cat_label}</span>\n'
                f'  <dl class="source-grid">\n'
                f'    <dt>{CFG.src_claim}</dt><dd class="source-claim">{claim}</dd>\n'
                f'    <dt>{CFG.src_source}</dt><dd class="source-source">{source}</dd>\n'
                f'    <dt>{CFG.src_where}</dt><dd class="source-where">{where}</dd>\n'
                f'    <dt>{CFG.src_caveat}</dt><dd class="source-caveat">{caveat}</dd>\n'
                f'  </dl>\n'
                f'</article>'
            )
        cursor = m.end()
    pieces.append(html[cursor:])
    html = "".join(pieces)

    # Drop the <hr> dividers between cards / before group headings.
    html = re.sub(
        r'(</article>)\s*<hr\s*/?>\s*(?=<article class="source-card")',
        r'\1',
        html,
    )
    html = re.sub(
        r'(</article>)\s*<hr\s*/?>\s*(?=<h3 id="[^"]+" class="source-group")',
        r'\1',
        html,
    )
    return html


# ---------------------------------------------------------------------------
# Reading time + search index (post-transform helpers, work on raw markdown)
# ---------------------------------------------------------------------------

_MD_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_MD_INLINE_CODE_RE = re.compile(r"`[^`]*`")
_MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_MD_HEADING_RE = re.compile(r"^#{1,6}\s+.*$", re.MULTILINE)
_MD_HTML_TAG_RE = re.compile(r"<[^>]+>")
_MD_EMPH_RE = re.compile(r"[*_]{1,3}")
_MD_BLOCKQUOTE_RE = re.compile(r"^>\s?", re.MULTILINE)
_MD_LISTMARK_RE = re.compile(r"^\s*([-*+]|\d+\.)\s+", re.MULTILINE)
_MD_WORD_RE = re.compile(r"\b[\w'-]+\b")
_MD_MULTI_WS_RE = re.compile(r"\s+")
_MD_ATTR_RE = re.compile(r"\{#[a-z0-9-]+\}")

_NEXT_BOUNDARY_RE = re.compile(
    r"(?m)^(?:## Chapter \d+\b|# Part [IVX]+\b|# Closing\b|## Appendix [A-Z]\.|## About the author\b|## Changelog\b)"
)


def _strip_markdown(text: str) -> str:
    text = _MD_FENCE_RE.sub(" ", text)
    text = _MD_IMAGE_RE.sub(" ", text)
    text = _MD_LINK_RE.sub(r"\1", text)
    text = _MD_INLINE_CODE_RE.sub(lambda m: m.group(0)[1:-1], text)
    text = _MD_HEADING_RE.sub(" ", text)
    text = _MD_HTML_TAG_RE.sub(" ", text)
    text = _MD_BLOCKQUOTE_RE.sub("", text)
    text = _MD_LISTMARK_RE.sub("", text)
    text = _MD_ATTR_RE.sub("", text)
    text = _MD_EMPH_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compute_chapter_reading_times(md_text, chapters, wpm=200):
    result = {}
    for slug, num, title in chapters:
        head_re = re.compile(rf"(?m)^## {re.escape(num)}\n## {re.escape(title)}\s*$")
        m = head_re.search(md_text)
        if not m:
            result[slug] = 1
            continue
        start = m.end()
        nxt = _NEXT_BOUNDARY_RE.search(md_text, pos=start)
        body = md_text[start:nxt.start()] if nxt else md_text[start:]
        words = len(_MD_WORD_RE.findall(_strip_markdown(body)))
        result[slug] = max(1, round(words / wpm))
    return result


def _snippet_for(md_text, start, limit=140):
    lines = md_text[start:].split("\n")
    paragraph = []
    in_fence = False
    started = False
    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            if started:
                break
            continue
        if stripped.startswith("#"):
            if started:
                break
            continue
        if stripped.startswith(("---", "===")):
            continue
        if stripped.startswith(">"):
            stripped = stripped.lstrip("> ").strip()
            if not stripped:
                continue
        paragraph.append(stripped)
        started = True
        if sum(len(p) for p in paragraph) > 400:
            break
    raw = " ".join(paragraph)
    clean = _MD_MULTI_WS_RE.sub(" ", _strip_markdown(raw)).strip()
    if len(clean) <= limit:
        return clean
    cut = clean[:limit].rsplit(" ", 1)[0]
    return cut + "..."


H3_ANCHOR_RE = re.compile(r"^###\s+(?P<title>.+?)\s*\{#(?P<slug>[a-z0-9-]+)\}\s*$", re.MULTILINE)


def build_search_index(md_text, parts, chapters, appendices, foreword, closing,
                       anchor_index: dict[str, str] | None = None):
    """Build the JSON search index.

    If `anchor_index` is provided, each entry gets a `url` field set to the
    owning section's per-chapter URL (e.g., `/chapter-3-governance-in-layers/`).
    Entries whose `id` isn't in the anchor_index (e.g., Part headings, certain
    front-matter anchors) fall back to `/read/#<id>` so the click handler can
    still resolve them via the all-in-one page.
    """
    anchor_index = anchor_index or {}
    entries = []
    seen = set()

    def add(entry):
        if entry["id"] in seen:
            return
        seen.add(entry["id"])
        if anchor_index:
            owner = anchor_index.get(entry["id"])
            entry["url"] = _rel(f"/{owner}/") if owner else _rel(f"/read/#{entry['id']}")
        entries.append(entry)

    # Parts
    for slug, num, title in parts:
        m = re.search(rf"^# {re.escape(CFG.part_word)} {re.escape(num)}\b", md_text, re.MULTILINE)
        pos = m.start() if m else 0
        add({"id": slug, "title": f"{CFG.part_word} {num}: {title}", "subtitle": CFG.search_part,
             "snippet": _snippet_for(md_text, pos), "kind": "part"})

    # Foreword
    if foreword:
        m = re.search(rf"^## {re.escape(CFG.foreword_label)}\b", md_text, re.MULTILINE)
        if m:
            add({"id": "foreword", "title": f"{CFG.foreword_label}: {foreword[1]}",
                 "subtitle": CFG.search_frontmatter,
                 "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # Other front matter H2s
    for slug, label in CFG.front_matter_items:
        m = re.search(rf"^## {re.escape(label)}\b", md_text, re.MULTILINE)
        if m:
            add({"id": slug, "title": label, "subtitle": CFG.search_frontmatter,
                 "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # Prologue
    m = re.search(rf"^## {re.escape(CFG.nine_seconds_label)}\b", md_text, re.MULTILINE)
    if m:
        add({"id": "nine-seconds", "title": CFG.nine_seconds_label, "subtitle": CFG.prologue_label,
             "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # Chapters
    for slug, num, title in chapters:
        pair_re = re.compile(rf"^## {re.escape(num)}\n## {re.escape(title)}\s*$", re.MULTILINE)
        m = pair_re.search(md_text)
        if not m:
            continue
        end_of_heading = md_text.find("\n", m.end())
        pos = end_of_heading if end_of_heading > 0 else m.start()
        add({"id": slug, "title": f"{num}: {title}", "subtitle": CFG.search_chapter,
             "snippet": _snippet_for(md_text, pos), "kind": "chapter"})

    # Closing
    if closing:
        m = re.search(rf"^# {re.escape(CFG.closing_label)}\b", md_text, re.MULTILINE)
        if m:
            add({"id": "closing", "title": f"{CFG.closing_label}: {closing[1]}",
                 "subtitle": CFG.closing_label,
                 "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # About the author (sits between Closing and Appendices)
    m = re.search(rf"^## {re.escape(CFG.about_label)}\b", md_text, re.MULTILINE)
    if m:
        add({"id": "about-the-author", "title": CFG.about_label,
             "subtitle": CFG.search_backmatter,
             "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # Appendices
    for slug, label, title in appendices:
        m = re.search(rf"^## {re.escape(label)}{CFG.appendix_search_sep}{re.escape(title)}\b", md_text, re.MULTILINE)
        if m:
            add({"id": slug, "title": f"{label}: {title}", "subtitle": CFG.search_appendix,
                 "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # H3 subsections (with explicit anchors)
    parent_label = ""
    parent_title = ""
    line_offsets = [0]
    for i, ch in enumerate(md_text):
        if ch == "\n":
            line_offsets.append(i + 1)
    for i, line in enumerate(md_text.split("\n")):
        line_start = line_offsets[i] if i < len(line_offsets) else 0
        stripped = line.strip()
        if stripped.startswith(f"## {CFG.foreword_label}"):
            parent_label = CFG.foreword_label
            parent_title = foreword[1] if foreword else CFG.foreword_label
            continue
        if stripped.startswith(f"## {CFG.chapter_word} "):
            for cslug, cnum, ctitle in chapters:
                if stripped == f"## {cnum}":
                    parent_label = cnum
                    parent_title = ctitle
                    break
            continue
        if stripped.startswith(f"## {CFG.appendix_word} "):
            apm = _APPENDIX_RE.match(stripped)
            if apm:
                parent_label = f"{CFG.appendix_word} {apm.group(1)}"
                parent_title = apm.group(2).strip()
            continue
        if stripped.startswith(f"# {CFG.part_word} "):
            pm = _PART_RE.match(stripped)
            if pm:
                parent_label = f"{CFG.part_word} {pm.group(1)}"
                parent_title = pm.group(2).strip()
            continue
        if stripped.startswith(f"# {CFG.closing_label}"):
            parent_label = CFG.closing_label
            parent_title = closing[1] if closing else CFG.closing_label
            continue
        if stripped.startswith(f"# {CFG.prologue_label}"):
            parent_label = CFG.prologue_label
            parent_title = CFG.prologue_label
            continue
        if stripped.startswith(f"## {CFG.changelog_label}"):
            parent_label = CFG.changelog_label
            parent_title = ""
            continue
        if stripped.startswith(f"## {CFG.about_label}"):
            parent_label = CFG.about_label
            parent_title = ""
            continue
        if stripped.startswith("### "):
            if i < 10:
                continue
            anchor_match = H3_ANCHOR_RE.match(line)
            if anchor_match:
                title = anchor_match.group("title").strip()
                slug = anchor_match.group("slug").strip()
            else:
                title = stripped[4:].strip()
                if title.endswith("}"):
                    title = re.sub(r"\s*\{#[a-z0-9-]+\}\s*$", "", title)
                slug = slugify(title)
            if not parent_label:
                subtitle = ""
            elif not parent_title or parent_title == parent_label:
                subtitle = parent_label
            else:
                subtitle = f"{parent_label}{CFG.title_dash}{parent_title}"
            add({"id": slug, "title": title, "subtitle": subtitle,
                 "snippet": _snippet_for(md_text, line_start), "kind": "subsection"})

    # Source-group anchors from Appendix C
    for group_title in SOURCE_GROUPS:
        slug = slugify(group_title)
        m = re.search(rf"^### {re.escape(group_title)}\b", md_text, re.MULTILINE)
        if not m:
            continue
        add({"id": slug, "title": group_title, "subtitle": CFG.search_appendix_c,
             "snippet": _snippet_for(md_text, m.start()), "kind": "subsection"})

    return json.dumps(entries, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def render_markdown(md_text: str) -> str:
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "attr_list", "md_in_html"],
        output_format="html5",
    )
    html = md.convert(md_text)
    # Strip the placeholder comments around our injected HTML
    html = html.replace("<!--RAW_HTML_START-->", "").replace("<!--RAW_HTML_END-->", "")
    # External links open in a new tab with safe rel; mailto and #anchor untouched.
    html = re.sub(
        r'<a href="(https?://[^"]+)"',
        r'<a href="\1" target="_blank" rel="noopener noreferrer"',
        html,
    )
    return html


# ---------------------------------------------------------------------------
# TOC
# ---------------------------------------------------------------------------

def build_toc(parts, chapters, appendices, foreword, closing,
              reading_times=None, *, mode: str = "in-page",
              legacy_to_full_slug: dict[str, str] | None = None,
              current_slug: str | None = None) -> str:
    """Build TOC HTML structured by Part.

    mode controls URL style on the anchor hrefs:
      'in-page':     #anchor          - used on /read/
      'transition':  /read/#anchor    - used on landing during Commit 2 transition
      'chapter-url': /<full-slug>/    - used on landing + chapter sidebars from Commit 3

    `legacy_to_full_slug` maps the TOC's anchor-style slugs ("chapter-3",
    "appendix-b", "foreword", "closing", "about-the-author", "nine-seconds",
    front-matter anchors) to the per-chapter URL slug
    ("chapter-3-governance-in-layers", "appendix-b-templates", ...). Required
    for mode="chapter-url". current_slug (also legacy-style) gets the
    .toc-current marker on its <li>.
    """
    reading_times = reading_times or {}
    legacy_to_full_slug = legacy_to_full_slug or {}
    chapter_to_part = {
        "chapter-1": "part-i",
        "chapter-2": "part-i",
        "chapter-3": "part-i",
        "chapter-4": "part-ii",
        "chapter-5": "part-ii",
        "chapter-6": "part-ii",
        "chapter-7": "part-ii",
        "chapter-8": "part-iii",
        "chapter-9": "part-iii",
        "chapter-10": "part-iii",
    }

    def _href(anchor: str) -> str:
        if mode == "transition":
            return _rel(f"/read/#{anchor}")
        if mode == "chapter-url":
            full = legacy_to_full_slug.get(anchor)
            if full:
                return _rel(f"/{full}/")
            # Front-matter anchors that don't own a section (how-to-read-this-book,
            # part-i/ii/iii, etc.) fall back to /read/#anchor so they still resolve.
            return _rel(f"/read/#{anchor}")
        return f"#{anchor}"

    def _li_cls(anchor: str) -> str:
        return ' class="toc-current"' if current_slug and current_slug == anchor else ''

    dash = CFG.title_dash
    sections = []

    # Front matter: Foreword (with its 4 H3 subsections nested) + the other
    # H2 sections that orient the reader before Part I.
    sections.append('<div class="toc-section">')
    sections.append(f'<div class="toc-section-title">{CFG.toc_front_matter}</div>')
    sections.append('<ul class="toc-list toc-list-flat">')
    if foreword:
        sections.append(
            f'  <li{_li_cls("foreword")}><a href="{_href("foreword")}">{CFG.foreword_label}{dash}{html_lib.escape(foreword[1])}</a>'
        )
        sections.append('    <ul class="toc-sublist">')
        for anchor, label in CFG.foreword_subitems:
            sections.append(f'      <li><a href="{_href(anchor)}">{label}</a></li>')
        sections.append('    </ul>')
        sections.append('  </li>')
    for anchor, label in CFG.front_matter_items:
        sections.append(f'  <li><a href="{_href(anchor)}">{label}</a></li>')
    sections.append("</ul></div>")

    # Prologue
    sections.append('<div class="toc-section">')
    sections.append(f'<div class="toc-section-title">{CFG.prologue_label}</div>')
    sections.append('<ul class="toc-list toc-list-flat">')
    sections.append(f'  <li{_li_cls("nine-seconds")}><a href="{_href("nine-seconds")}">{CFG.nine_seconds_label}</a></li>')
    sections.append("</ul></div>")

    # Parts + chapters
    for slug, num, title in parts:
        sections.append('<div class="toc-section">')
        sections.append(
            f'<div class="toc-section-title"><a href="{_href(slug)}">{CFG.part_word} {num}{dash}{html_lib.escape(title)}</a></div>'
        )
        sections.append('<ul class="toc-list">')
        for ch_slug, ch_num, ch_title in chapters:
            if chapter_to_part.get(ch_slug) == slug:
                ch_n = ch_num.replace(f"{CFG.chapter_word} ", "")
                mins = reading_times.get(ch_slug)
                time_html = f'<span class="toc-time">{mins} {CFG.min_label}</span>' if mins else ""
                sections.append(
                    f'  <li{_li_cls(ch_slug)}><a href="{_href(ch_slug)}"><span class="toc-num">{ch_n}</span>'
                    f'<span class="toc-text">{CFG.chapter_word} {ch_n} - {html_lib.escape(ch_title)}</span>{time_html}</a></li>'
                )
        sections.append("</ul></div>")

    # Closing
    if closing:
        closing_a_cls = ' class="toc-current-link"' if current_slug == "closing" else ''
        sections.append('<div class="toc-section">')
        sections.append(f'<div class="toc-section-title"><a href="{_href("closing")}"{closing_a_cls}>{CFG.closing_label}</a></div>')
        sections.append("</div>")

    # About the author (sits between Closing and Appendices).
    about_a_cls = ' class="toc-current-link"' if current_slug == "about-the-author" else ''
    sections.append('<div class="toc-section">')
    sections.append(f'<div class="toc-section-title"><a href="{_href("about-the-author")}"{about_a_cls}>{CFG.about_label}</a></div>')
    sections.append("</div>")

    # Changelog (sits between About and Appendices).
    changelog_a_cls = ' class="toc-current-link"' if current_slug == "changelog" else ''
    sections.append('<div class="toc-section">')
    sections.append(f'<div class="toc-section-title"><a href="{_href("changelog")}"{changelog_a_cls}>{CFG.changelog_label}</a></div>')
    sections.append("</div>")

    # Appendices
    if appendices:
        sections.append('<div class="toc-section">')
        sections.append(f'<div class="toc-section-title">{CFG.toc_appendices}</div>')
        sections.append('<ul class="toc-list">')
        for slug, label, title in appendices:
            sections.append(
                f'  <li{_li_cls(slug)}><a href="{_href(slug)}"><span class="toc-num">{label.replace(f"{CFG.appendix_word} ", "")}</span>{html_lib.escape(title)}</a></li>'
            )
        sections.append("</ul></div>")

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Template
# ---------------------------------------------------------------------------

CRITICAL_END = "/* @region-end critical */"
DEFERRED_END = "/* @region-end deferred */"


def split_template_css(template_html: str) -> tuple[str, str, str]:
    """Return (template_with_critical_inline, critical_css, deferred_css).

    Finds the inline <style>...</style> block, splits its contents on the
    region markers, and returns the deferred CSS as a separate string so the
    caller can write it to deferred.css. The returned template keeps the
    critical CSS inlined and replaces the deferred portion with the
    preload-link snippet.
    """
    style_open = template_html.find("<style>")
    style_close = template_html.find("</style>", style_open)
    if style_open == -1 or style_close == -1:
        raise RuntimeError("template missing <style>...</style> block")

    style_body = template_html[style_open + len("<style>"):style_close]
    if CRITICAL_END not in style_body or DEFERRED_END not in style_body:
        raise RuntimeError(
            f"template style block missing region markers "
            f"({CRITICAL_END!r} and {DEFERRED_END!r})"
        )

    critical, _, after_critical = style_body.partition(CRITICAL_END)
    deferred, _, _ = after_critical.partition(DEFERRED_END)
    critical = critical.strip()
    deferred = deferred.strip()

    preload_snippet = (
        '<link rel="preload" href="/deferred.css" as="style" '
        'onload="this.onload=null;this.rel=\'stylesheet\'">\n'
        '    <noscript><link rel="stylesheet" href="/deferred.css"></noscript>'
    )

    new_style_block = f"<style>\n{critical}\n    </style>\n    {preload_snippet}"
    new_template = (
        template_html[:style_open]
        + new_style_block
        + template_html[style_close + len("</style>"):]
    )
    return new_template, critical, deferred


# All-in-one body for /read/: hero + content + end-cover figure. The {CONTENT},
# {AUTHOR}, {SUBTITLE}, and {BYLINE_HREF} slots inside this fragment are resolved
# by the /read/ body builder (_read_article_body) via .format() before being
# substituted into the template - NOT via nesting another {{...}} placeholder
# pass. /read/'s byline points to #contact (the in-page About anchor); the
# CTAs link to /read/#chapter-7 / #appendix-b so they keep working as in-page
# jumps when viewing the all-in-one page.
READ_ARTICLE_BODY = '''<header class="article-header">
        <h1 class="article-title">
          Ship It With AI
          <span class="article-title-keyword">{TITLE_KEYWORD}</span>
        </h1>
        <p class="article-subtitle">{SUBTITLE}</p>
        <p class="article-dek">{DEK}</p>
        <div class="article-author"><a href="{BYLINE_HREF}">{AUTHOR}</a></div>
        <nav class="hero-cta" aria-label="{CTA_ARIA}">
          <a class="cta-primary" href="#chapter-7">{CTA_PRIMARY}</a>
          <a class="cta-secondary" href="#appendix-b">{CTA_TEMPLATES}</a>
          <a class="cta-secondary" href="mailto:info@ship-it-with.ai?subject=Agentic%20delivery%20assessment">{CTA_ASSESS}</a>
        </nav>
      </header>

      <aside class="read-mode-note">
        {READ_NOTE}
      </aside>

      {CONTENT}

      <figure class="article-cover article-cover-end">
        <picture>
          <source type="image/webp" srcset="/cover-720.webp 720w, /cover.webp 1200w" sizes="(max-width: 760px) 100vw, 720px" />
          <img src="/cover.jpg" alt="Ship It With AI - A Manual for Shipping Software with AI Agents, by {AUTHOR}" width="1200" height="630" loading="lazy" decoding="async" />
        </picture>
      </figure>'''


# Landing body: thin marketing landing - hero + TOC. The {SUBTITLE}, {AUTHOR},
# {BYLINE_HREF}, and {TOC_HTML} slots are resolved by the landing body builder
# (_landing_article_body) via .format(). CTAs link to /read/#chapter-7 etc.
# during Commit 2 (per-chapter URLs land in Commit 3).
LANDING_ARTICLE_BODY = '''<header class="article-header">
        <h1 class="article-title">
          Ship It With AI
          <span class="article-title-keyword">{TITLE_KEYWORD}</span>
        </h1>
        <p class="article-subtitle">{SUBTITLE}</p>
        <p class="article-dek">{DEK}</p>
        <div class="article-author"><a href="{BYLINE_HREF}">{AUTHOR}</a></div>
        <nav class="hero-cta" aria-label="{CTA_ARIA}">
          <a class="cta-primary" href="{CH7_HREF}">{CTA_PRIMARY}</a>
          <a class="cta-secondary" href="{APPB_HREF}">{CTA_TEMPLATES}</a>
          <a class="cta-secondary" href="mailto:info@ship-it-with.ai?subject=Agentic%20delivery%20assessment">{CTA_ASSESS}</a>
        </nav>
      </header>

      <section class="landing-toc">
        {TOC_HTML}
      </section>

      <figure class="article-cover article-cover-end">
        <picture>
          <source type="image/webp" srcset="/cover-720.webp 720w, /cover.webp 1200w" sizes="(max-width: 760px) 100vw, 720px" />
          <img src="/cover.jpg" alt="Ship It With AI - A Manual for Shipping Software with AI Agents, by {AUTHOR}" width="1200" height="630" loading="lazy" decoding="async" />
        </picture>
      </figure>'''


# Single source of truth for the FAQ. Each entry renders to (1) the visible
# landing <section>, (2) the landing FAQPage JSON-LD, and (3) - when home_slug
# is set - a FAQPage block on that chapter page.
FAQ_ENTRIES: list[dict] = [
    {
        "q": "What is agentic coding?",
        "home_slug": None,
        "a": "Agentic coding is the practice of using AI agents that read, write, run, and verify code largely on their own, with humans in the loop for review and governance rather than for every keystroke. Unlike autocomplete or chat assistants, an agentic system holds a multi-step plan, executes through real tools (filesystem, shell, browser, version control), and surfaces work for verification rather than producing isolated suggestions.",
    },
    {
        "q": "How does agentic coding differ from AI autocomplete and from vibe coding?",
        "home_slug": None,
        "a": "Autocomplete completes the next token under your cursor. Vibe coding accepts whatever the model generates with minimal verification. Agentic coding sits between: the agent plans, edits across files, runs tests, and reports back, but the human controls the context the agent sees, the actions it can take, the verification gates it passes through, and the adoption surface it operates on. The difference is methodological discipline, not model quality.",
    },
    {
        "q": "What is AGENTS.md and why does it matter?",
        "home_slug": "chapter-6-agents-md",
        "a": "AGENTS.md is a plain-Markdown file at the root of a repository that tells coding agents how the project actually works - forbidden patterns, conventions, build commands, where things live, and the mistakes the team has already made. It is the vendor-neutral standard read at session start by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, and Aider; Claude Code reads the equivalent CLAUDE.md and can import AGENTS.md to share the same content. It is tracked as an open standard at agents.md.",
    },
    {
        "q": "How do you safely roll out AI coding agents in an engineering team?",
        "home_slug": "chapter-10-adoption-90-days",
        "a": "A safe rollout treats agentic delivery as a control problem with five layers of governance: permissions, sandboxing, secrets, security hooks, and telemetry. Pair that with a clear methodology - a six-phase loop covering research, plan, execute, review, verify, ship - and a 90-day adoption arc with three named roles (Champion, Lead, Manager). Skip any of these and adoption produces more harm than benefit.",
    },
    {
        "q": "What is the six-phase agentic loop?",
        "home_slug": "chapter-5-six-phase-loop",
        "a": "The six-phase loop is a delivery discipline for agentic work: research (the agent maps the codebase into a durable note), plan (a reviewable file-level task list), execute (constrained subagents make the changes), review (separate spec-compliance and code-quality passes), verify (new tests run, including accessibility-tree UI tests), and ship (a normal pull request your existing process reviews). Most failures route back to plan, not back to research.",
    },
    {
        "q": "How much does agentic coding cost?",
        "home_slug": "appendix-a-cost-economics",
        "a": "Per-seat tool pricing is the small line item; the real cost is total cost of ownership - seats, token and usage spend, the human review time the loop requires, and the governance setup. The durable way to budget is to match seat tier to actual usage rather than buying uniform tooling, and to compare the loaded cost of agent-assisted delivery against the cost of the work it replaces, not against zero.",
    },
    {
        "q": "What is MCP (Model Context Protocol)?",
        "home_slug": "chapter-1-primitives",
        "a": "MCP, the Model Context Protocol, is a specification that lets a coding agent connect to external tools and data sources - issue trackers, databases, documentation, internal services - through a uniform interface. It is one of the agent primitives: where Tools are the agent's built-in actions, MCP is how the agent reaches capabilities the harness did not ship with.",
    },
    {
        "q": "Are AI coding agents production-ready?",
        "home_slug": "chapter-8-readiness-kill-signals",
        "a": "It depends on the codebase, not the company. Readiness is a per-project question answered by eight kill signals and a green/yellow/red traffic light: a well-tested, documented, decoupled module with a team that can evaluate the output is green; an undocumented, untested, tightly-coupled system whose team cannot verify the result is red. Most companies have a mix, and the mix tells you the order of operations.",
    },
]


def faq_jsonld(entries: list[dict]) -> str:
    """One <script type=ld+json> FAQPage block for the given entries."""
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": e["q"],
             "acceptedAnswer": {"@type": "Answer", "text": e["a"]}}
            for e in entries
        ],
    }
    return ('<script type="application/ld+json">'
            + json.dumps(faq, ensure_ascii=False)
            + '</script>')


def faq_visible_html(entries: list[dict]) -> str:
    """Visible, crawlable FAQ section: real <h2>/<h3> so search + answer engines
    see question->answer adjacency (not just JSON-LD)."""
    items = "\n".join(
        f'        <h3>{html_lib.escape(e["q"])}</h3>\n'
        f'        <p>{html_lib.escape(e["a"])}</p>'
        for e in entries
    )
    return (
        '\n      <section class="article-faq" id="faq" aria-labelledby="faq-heading">\n'
        f'        <h2 id="faq-heading">{CFG.faq_heading}</h2>\n'
        f'{items}\n'
        '      </section>\n'
    )


# Homepage JSON-LD (Book + Organization + FAQPage). Lives in the build script
# rather than the template so the 404 path can simply substitute an empty
# string for {{HEAD_SCHEMA}} - keeping crawlers from treating /404.html as a
# duplicate of the Book entity.
HOMEPAGE_HEAD_SCHEMA = '''<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Book",
    "@id": "{URL_BASE}/#book",
    "name": "{BOOK_NAME}",
    "headline": "Ship It With AI",
    "alternateName": "{BOOK_ALT}",
    "author": {{
      "@type": "Person",
      "name": "{AUTHOR}",
      "url": "https://www.linkedin.com/in/mihaicvasnievschi/"
    }},
    "publisher": {{ "@id": "{URL_BASE}/#org" }},
    "bookFormat": "https://schema.org/EBook",
    "inLanguage": "{LANG}",
    "numberOfPages": {NUMBER_OF_PAGES},
    "genre": "Technology / Software Engineering",
    "about": [
      "Agentic coding",
      "AI software delivery",
      "AGENTS.md",
      "AI coding agents"
    ],
    "description": "{BOOK_DESC}",
    "url": "{URL_BASE}/",
    "image": "https://ship-it-with.ai/cover.jpg",
    "dateModified": "{DATE_MODIFIED}"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "{URL_BASE}/#org",
    "name": "Ship It With AI",
    "url": "{URL_BASE}/",
    "logo": "https://ship-it-with.ai/cover.jpg"
  }}
  </script>'''


# Strict placeholder pattern: matches our {{UPPER_SNAKE}} tokens only.
# Deliberately narrow so it doesn't false-positive on CSS rules, JSON object
# braces, or other single-brace constructs in the template body.
_PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")


def render_template_with_placeholders(template: str, substitutions: dict) -> str:
    """Apply substitutions to template and raise if any {{...}} remains.

    All values must already be fully-rendered HTML strings (no nested
    placeholders) - the helper does a single substitution pass per key, then
    fails loudly if any `{{UPPER_SNAKE}}` token is left over. That's the
    safety net that catches the bug class where a new placeholder is added
    to the template but missed by one of the render call-sites.
    """
    for key, value in substitutions.items():
        template = template.replace("{{" + key + "}}", value)
    leftover = _PLACEHOLDER_RE.findall(template)
    if leftover:
        unique = sorted(set(leftover))
        raise RuntimeError(
            f"unresolved template placeholders after substitution: {unique}"
        )
    return template


def _read_article_body(content_html: str, subtitle: str, author: str,
                       byline_href: str) -> str:
    """Build /read/'s full article body (hero + content + end-cover).

    Author/subtitle/byline_href are inlined here (not left as nested {{...}}
    placeholders) so the substitution helper sees zero leftover tokens after a
    single pass.
    """
    return READ_ARTICLE_BODY.format(
        SUBTITLE=html_lib.escape(subtitle),
        CONTENT=content_html,
        AUTHOR=html_lib.escape(author),
        BYLINE_HREF=html_lib.escape(byline_href),
        TITLE_KEYWORD=CFG.title_keyword,
        DEK=CFG.hero_dek,
        CTA_ARIA=CFG.cta_aria,
        CTA_PRIMARY=CFG.cta_primary,
        CTA_TEMPLATES=CFG.cta_templates,
        CTA_ASSESS=CFG.cta_assess,
        READ_NOTE=CFG.read_note.format(ROOT=_rel("/")),
    )


def _landing_article_body(subtitle: str, author: str, byline_href: str,
                          toc_html: str) -> str:
    """Build the landing page's article body (hero + landing TOC + cover)."""
    body = LANDING_ARTICLE_BODY.format(
        SUBTITLE=html_lib.escape(subtitle),
        AUTHOR=html_lib.escape(author),
        BYLINE_HREF=html_lib.escape(byline_href),
        TOC_HTML=toc_html,
        TITLE_KEYWORD=CFG.title_keyword,
        DEK=CFG.hero_dek,
        CTA_ARIA=CFG.cta_aria,
        CTA_PRIMARY=CFG.cta_primary,
        CTA_TEMPLATES=CFG.cta_templates,
        CTA_ASSESS=CFG.cta_assess,
        CH7_HREF=_rel("/chapter-7-architecture-review/"),
        APPB_HREF=_rel("/appendix-b-templates/"),
    )
    return body + faq_visible_html(CFG.faq_entries)


def _json_escape(value: str) -> str:
    """Escape a string for inclusion inside a JSON string literal.

    `html_lib.escape` is wrong for JSON-LD bodies: JSON parsers see
    `O&#x27;Brien` as the literal 7-char string, not `O'Brien`. We need
    JSON-string escaping (backslash sequences, \\u00xx for control chars)
    instead. `json.dumps(s)` wraps the value in quotes; stripping the outer
    quotes yields the inner-string escape form we can splice into the
    template between literal `"..."` delimiters.
    """
    return json.dumps(value)[1:-1]


def _homepage_head_schema(author: str, number_of_pages: int, date_modified: str) -> str:
    """Build the JSON-LD for landing + /read/ (Book + Organization + FAQPage).

    Same schema on both pages is defensible because /read/'s canonical points
    to / - they are alternate formats of the same Book entity, not separate
    works.
    """
    return HOMEPAGE_HEAD_SCHEMA.format(
        AUTHOR=_json_escape(author),
        NUMBER_OF_PAGES=number_of_pages,
        DATE_MODIFIED=date_modified,
        URL_BASE=f"{BASE}{URL_PREFIX}",
        LANG=CFG.html_lang,
        BOOK_NAME=_json_escape(CFG.book_name),
        BOOK_ALT=_json_escape(CFG.book_alt),
        BOOK_DESC=_json_escape(CFG.book_desc),
    )


def render_hash_redirect_js(sections: list[Section]) -> str:
    """Landing-only hash-redirect shim. Migrates old /#chapter-N bookmarks
    that pointed at the SPA's in-page anchors to the new per-chapter URLs.

    Generated from SECTION_SLUGS so it always stays in sync with the slug
    table. During Commit 2 the per-chapter URLs don't exist yet - the
    redirect still rewrites to /<slug>/, which will 404 until Commit 3 ships.
    That is the desired behaviour: better a 404 (with the chrome and the
    chapter index) than a silent dead-end on the landing page.
    """
    redirects: dict[str, str] = {}
    for s in sections:
        redirects[f"#{s.slug}"] = _rel(f"/{s.slug}/")
        if s.kind == "chapter":
            m = re.match(r"^chapter-(\d+)-", s.slug)
            if m:
                redirects[f"#chapter-{m.group(1)}"] = _rel(f"/{s.slug}/")
        if s.kind == "appendix":
            m = re.match(r"^appendix-([a-z])-", s.slug)
            if m:
                redirects[f"#appendix-{m.group(1)}"] = _rel(f"/{s.slug}/")
        if s.slug == "about-the-author":
            redirects["#contact"] = _rel("/about-the-author/#contact")
        if s.slug == "prologue-nine-seconds":
            redirects["#nine-seconds"] = _rel("/prologue-nine-seconds/")
        if s.slug == "foreword":
            redirects["#foreword"] = _rel("/foreword/")

    map_json = json.dumps(redirects, indent=2)
    return (
        '<script>\n'
        '  (function() {\n'
        '    var hash = location.hash;\n'
        '    if (!hash) return;\n'
        f'    var REDIRECTS = {map_json};\n'
        '    var target = REDIRECTS[hash];\n'
        '    if (target) location.replace(target);\n'
        '  })();\n'
        '</script>'
    )


def render_sitemap(sections: list[Section]) -> str:
    """Full sitemap: landing + /read/ + every per-section URL."""
    today = _content_date().strftime("%Y-%m-%d")
    # Slugs renamed in earlier passes - old URLs serve as redirect stubs,
    # not as canonical URLs. Exclude from sitemap so Google doesn't index them.
    REDIRECTED_OLD_SLUGS = {"chapter-1-six-primitives"}

    # /read/ is noindex (duplicate of the per-section pages) - keep it out of the sitemap.
    urls = [_abs("/")]
    urls += [
        _abs(f"/{s.slug}/")
        for s in sections
        if s.slug not in REDIRECTED_OLD_SLUGS
    ]
    body = "\n".join(
        f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>' for u in urls
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
'''


def build_legacy_to_full_slug(sections: list[Section]) -> dict[str, str]:
    """Map the TOC's anchor-style slugs ('chapter-3', 'appendix-b', etc.) to
    the per-chapter URL slug ('chapter-3-governance-in-layers', etc.).

    Used by build_toc(mode='chapter-url') so the existing TOC builder can keep
    emitting legacy anchor names and have them routed to the new URLs.
    """
    out: dict[str, str] = {}
    for s in sections:
        if s.kind == "chapter":
            m = re.match(r"^chapter-(\d+)-", s.slug)
            if m:
                out[f"chapter-{m.group(1)}"] = s.slug
        elif s.kind == "appendix":
            m = re.match(r"^appendix-([a-z])-", s.slug)
            if m:
                out[f"appendix-{m.group(1)}"] = s.slug
        elif s.kind == "foreword":
            out["foreword"] = s.slug
        elif s.kind == "closing":
            out["closing"] = s.slug
        elif s.kind == "about":
            out["about-the-author"] = s.slug
        elif s.kind == "changelog":
            out["changelog"] = s.slug
        elif s.kind == "prologue":
            out["nine-seconds"] = s.slug
    return out


def legacy_slug_for_section(section: Section) -> str:
    """Return the TOC's anchor-style slug for a section (the value the TOC
    sidebar uses as `current_slug` to mark the active entry)."""
    if section.kind == "chapter":
        m = re.match(r"^chapter-(\d+)-", section.slug)
        if m:
            return f"chapter-{m.group(1)}"
    if section.kind == "appendix":
        m = re.match(r"^appendix-([a-z])-", section.slug)
        if m:
            return f"appendix-{m.group(1)}"
    if section.kind == "prologue":
        return "nine-seconds"
    if section.kind == "foreword":
        return "foreword"
    if section.kind == "closing":
        return "closing"
    if section.kind == "about":
        return "about-the-author"
    if section.kind == "changelog":
        return "changelog"
    return section.slug


# ---------------------------------------------------------------------------
# Per-section rendering pipeline (Commit 3)
# ---------------------------------------------------------------------------

_HREF_HASH_RE = re.compile(r'href="#([a-z0-9-]+)"')
# Locally-generated anchors that always exist within the current page -
# don't warn when they aren't in the cross-page anchor_index.
_LOCAL_ANCHOR_RE = re.compile(r"^(top|artifact-\d+)$")


def rewrite_cross_section_anchors(html: str, current_slug: str,
                                  anchor_index: dict[str, str]) -> str:
    """Rewrite intra-document hash links that cross section boundaries.

    For each `<a href="#X">`:
      - If X owns the CURRENT section's slug → keep as #X (in-page jump).
      - Else if X is in anchor_index → rewrite to /<owning-slug>/#X.
      - Else (unknown anchor) → leave as-is. Warn unless it's a locally-
        generated anchor (#top, #artifact-N) that always exists on the page.

    No-op on /read/ (all anchors are in-page there).
    """
    warnings: set[str] = set()

    def repl(m: re.Match) -> str:
        target = m.group(1)
        owner = anchor_index.get(target)
        if owner is None:
            if not _LOCAL_ANCHOR_RE.match(target):
                warnings.add(target)
            return m.group(0)
        if owner == current_slug:
            return m.group(0)
        return f'href="{_rel(f"/{owner}/#{target}")}"'

    out = _HREF_HASH_RE.sub(repl, html)
    if warnings:
        print(f"warn: unknown anchor targets in {current_slug or '/read/'}: "
              f"{sorted(warnings)[:8]}{'...' if len(warnings) > 8 else ''}")
    return out


def _wrap_callouts(content_html: str) -> str:
    """Apply Ship-this-week / Try-it-yourself / Case-note paragraph wrappers.

    Extracted from render_all_in_one_body so per-chapter rendering can reuse
    the exact same regexes (one source of truth)."""
    ship_m = re.escape(CFG.ship_marker)
    try_m = re.escape(CFG.try_marker)
    case_m = re.escape(CFG.case_marker)

    # "Ship this week"
    content_html = content_html.replace(
        f"<p><strong>{CFG.ship_marker}</strong></p>",
        f'<div class="action-marker"><p><strong>{CFG.ship_marker}</strong></p>',
    )
    content_html = re.sub(
        rf'<div class="action-marker"><p><strong>{ship_m}</strong></p>(.*?)<hr ?/?>',
        rf'<aside class="action-box"><div class="action-label">{CFG.ship_label}</div>\1</aside>',
        content_html,
        flags=re.DOTALL,
    )

    # "Try it yourself"
    content_html = content_html.replace(
        f"<p><strong>{CFG.try_marker}</strong></p>",
        f'<div class="try-marker"><p><strong>{CFG.try_marker}</strong></p>',
    )
    content_html = re.sub(
        rf'<div class="try-marker"><p><strong>{try_m}</strong></p>(.*?)<hr ?/?>',
        rf'<aside class="try-box"><div class="try-label">{CFG.try_label}</div>\1</aside>',
        content_html,
        flags=re.DOTALL,
    )

    # Drop <hr> between adjacent callouts
    content_html = re.sub(
        r'(</aside>)\s*<hr\s*/?>\s*(?=<aside class="(?:artifact-box|action-box|try-box)")',
        r'\1',
        content_html,
    )

    # Case notes
    content_html = re.sub(
        rf"<p><strong>{case_m}([^<]+)</strong></p>",
        rf'<aside class="case-note"><div class="case-note-label">{CFG.case_label}</div><div class="case-note-title">\1</div>',
        content_html,
    )
    content_html = re.sub(
        r'(<aside class="case-note">.*?<table>.*?</table>)',
        r"\1</aside>",
        content_html,
        flags=re.DOTALL,
    )
    return content_html


def apply_transforms(html: str, *, mode: str, anchor_index: dict[str, str],
                     current_slug: str) -> str:
    """Apply the full post-markdown HTML-transform pipeline.

    mode is one of: 'read', 'chapter', 'landing'. Mode affects:
      - delink_repeated_agents_md: 'read' splits on <h2 id="chapter-N"> to
        bound the first-link allowance per chapter; other modes treat the
        whole html as one scope.
      - rewrite_cross_section_anchors: no-op in 'read' mode (anchors are
        all in-page there); rewrites cross-section #refs in 'chapter' mode.
    """
    html = transform_source_notes(html)
    html = transform_artifacts(html)
    html = _wrap_callouts(html)
    html = transform_source_cards(html)
    html = delink_repeated_agents_md(html, mode=mode)
    html = inject_anchor_links(html)
    if mode != "read":
        html = rewrite_cross_section_anchors(html, current_slug, anchor_index)
    return html


def _strip_md_words(body_md: str) -> int:
    """Return the cleaned-text word count for a section's markdown body."""
    return len(_MD_WORD_RE.findall(_strip_markdown(body_md)))


def compute_section_reading_time(body_md: str, wpm: int = 200) -> int:
    return max(1, round(_strip_md_words(body_md) / wpm))


def render_section_body(section: Section, anchor_index: dict[str, str]) -> str:
    """Render a single section's markdown body to HTML via the per-chapter
    transforms pipeline. Returns just the body fragment (no <h1>, no nav).
    """
    body_md = replace_diagrams(section.body_md, strict=False)
    md_html = render_markdown(body_md)
    return apply_transforms(md_html, mode="chapter",
                            anchor_index=anchor_index,
                            current_slug=section.slug)


def render_chapter_schema(section: Section) -> str:
    """Per-chapter JSON-LD: TechArticle (linked to the Book by @id) +
    BreadcrumbList. The Book entity itself is only defined on landing/read,
    keeping a single source of truth."""
    today = _content_date().strftime("%Y-%m-%d")
    page_url = _abs(f"/{section.slug}/")

    tech_article = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": section.title,
        "url": page_url,
        "author": {"@type": "Person", "name": "Mihai Cvasnievschi"},
        "isPartOf": {"@id": f"{BASE}{URL_PREFIX}/#book"},
        "articleSection": section.title,
        "dateModified": today,
        "proficiencyLevel": "Expert",
        "dependencies": ["Claude Code", "AGENTS.md", "MCP"],
    }

    crumbs = [{"@type": "ListItem", "position": 1, "name": CFG.crumb_home,
               "item": _abs("/")}]
    if section.kind == "chapter" and section.part_slug:
        part_name = CFG.crumb_parts.get(section.part_slug, section.part_slug)
        crumbs.append({"@type": "ListItem", "position": 2, "name": part_name,
                       "item": _abs(f"/read/#{section.part_slug}")})
        crumbs.append({"@type": "ListItem", "position": 3,
                       "name": section.title, "item": page_url})
    elif section.kind == "appendix":
        crumbs.append({"@type": "ListItem", "position": 2, "name": CFG.toc_appendices,
                       "item": _abs("/read/#appendix-a")})
        crumbs.append({"@type": "ListItem", "position": 3,
                       "name": section.title, "item": page_url})
    else:
        crumbs.append({"@type": "ListItem", "position": 2,
                       "name": section.title, "item": page_url})

    breadcrumb_list = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": crumbs,
    }

    return (
        f'<script type="application/ld+json">{json.dumps(tech_article, ensure_ascii=False)}</script>\n  '
        f'<script type="application/ld+json">{json.dumps(breadcrumb_list, ensure_ascii=False)}</script>'
    )


_STABLE_SECTION_DESCRIPTIONS: dict[str, str] = {
    # Hard-coded for sections whose body contains dated/churning content that
    # would otherwise produce a different SERP snippet on every release.
    "changelog": (
        "Meaningful changes to Ship It With AI - the agentic coding field "
        "manual. Dated entries for content updates, structural revisions, "
        "and SEO passes."
    ),
}


def _section_description(section: Section, limit: int = 200) -> str:
    """Build a meta description from the section's first real paragraph.

    Strips markdown, blockquote markers, and rules. If the first paragraph is
    shorter than ~120 chars, concatenates the next paragraph too - meta
    descriptions in the 120-200 char range carry the most SERP weight.
    """
    if section.kind in _STABLE_SECTION_DESCRIPTIONS:
        return _STABLE_SECTION_DESCRIPTIONS[section.kind]
    paragraphs: list[str] = []
    buf: list[str] = []
    in_fence = False
    for line in section.body_md.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("#") or stripped.startswith("---"):
            if buf:
                paragraphs.append(" ".join(buf)); buf = []
            continue
        if stripped.startswith(">"):
            stripped = stripped.lstrip("> ").strip()
            if not stripped:
                continue
        if not stripped:
            if buf:
                paragraphs.append(" ".join(buf)); buf = []
            continue
        buf.append(stripped)
        if sum(len(p) for p in paragraphs) > limit + 50:
            break
    if buf:
        paragraphs.append(" ".join(buf))

    raw = " ".join(paragraphs[:2])
    clean = _MD_MULTI_WS_RE.sub(" ", _strip_markdown(raw)).strip()
    if len(clean) <= limit:
        return clean or f"{section.title} - Agentic Coding Field Manual."
    cut = clean[:limit].rsplit(" ", 1)[0]
    return cut + "..."


def _lang_switch_html(page_path: str) -> str:
    """Topbar EN/RO switcher. page_path is the path after the language prefix
    (e.g. '/', '/read/', '/chapter-1-primitives/'). Each language links to the
    same path under its own prefix; the current language is marked active."""
    opts = []
    for lang in LANGS:
        href = lang.prefix + page_path
        if href == "":
            href = "/"
        is_current = lang.code == CFG.code
        cls = "lang-opt lang-current" if is_current else "lang-opt"
        cur = ' aria-current="true"' if is_current else ''
        opts.append(
            f'<a href="{href}" class="{cls}" hreflang="{lang.html_lang}" '
            f'lang="{lang.html_lang}"{cur}>{lang.switch_label}</a>'
        )
    return (
        '<div class="lang-switch" role="group" aria-label="' + CFG.lang_switch_aria + '">'
        + "".join(opts) + '</div>'
    )


def _hreflang_alts(page_path: str) -> str:
    """rel=alternate hreflang links pointing every language at the equivalent
    page, plus x-default → English. Empty for noindex pages."""
    out = []
    for lang in LANGS:
        href = f"{BASE}{lang.prefix}{page_path}"
        out.append(f'<link rel="alternate" hreflang="{lang.html_lang}" href="{href}" />')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}{EN.prefix}{page_path}" />')
    return "\n  ".join(out)


def _lang_subs(page_path: str, *, hreflang: bool = True) -> dict:
    """The per-page language placeholders every render site must supply."""
    return {
        "HTML_LANG": CFG.html_lang,
        "OG_LOCALE": CFG.og_locale,
        "LANG_SWITCH": _lang_switch_html(page_path),
        "HREFLANG_ALTS": _hreflang_alts(page_path) if hreflang else "",
    }


def render_chapter(template: str, section: Section, *,
                   prev_: Section | None, next_: Section | None,
                   author: str, title_meta: str,
                   toc_html_sidebar: str, search_index: str,
                   anchor_index: dict[str, str],
                   date_modified_human: str) -> str:
    """Render a single per-section page (chapter / appendix / foreword / etc.)."""
    body_html = render_section_body(section, anchor_index)

    # Standalone pages put the chapter title at <h1>, so bump body headings up one
    # level (h3->h2, h4->h3, ...) to keep the outline sequential (h1 -> h2 -> h3).
    body_html = re.sub(
        r'<(/?)h([3-6])\b',
        lambda m: f'<{m.group(1)}h{int(m.group(2)) - 1}',
        body_html,
    )

    reading_time = (
        f'<p class="reading-time">{section.reading_time_min} {CFG.min_read}</p>'
        if section.reading_time_min and section.kind != "changelog" else ''
    )
    prev_html = (
        f'<a class="chapter-prev" href="{_rel(f"/{prev_.slug}/")}">← {html_lib.escape(prev_.title)}</a>'
        if prev_ else ''
    )
    next_html = (
        f'<a class="chapter-next" href="{_rel(f"/{next_.slug}/")}">{html_lib.escape(next_.title)} →</a>'
        if next_ else ''
    )
    nav = (
        f'<nav class="chapter-nav" aria-label="{CFG.chapter_nav_aria}">'
        f'{prev_html}{next_html}</nav>'
    )

    article_body = (
        f'<header class="article-header">\n'
        f'        <h1 id="{section.slug}" class="article-title">{html_lib.escape(section.title)}</h1>\n'
        f'        {reading_time}\n'
        f'      </header>\n'
        f'      {body_html}\n'
        f'      {nav}'
    )

    page_url = _abs(f"/{section.slug}/")
    page_title = f"{section.title}{CFG.title_suffix}"
    page_description = _section_description(section)

    substitutions = {
        "PAGE_TITLE": html_lib.escape(page_title),
        "PAGE_DESCRIPTION": html_lib.escape(page_description),
        "PAGE_URL": page_url,
        "OG_TYPE": "article",
        "OG_URL": page_url,
        "SITE_MODE": "chapter",
        "TITLE": html_lib.escape(title_meta),
        "AUTHOR": html_lib.escape(author),
        "BYLINE_HREF": _rel("/about-the-author/#contact"),
        "HEAD_SCHEMA": "",
        "HEAD_EXTRA": render_chapter_schema(section),
        "TOC": toc_html_sidebar,
        "ARTICLE_BODY": article_body,
        "SEARCH_INDEX": search_index,
        "DATE_MODIFIED_HUMAN": html_lib.escape(date_modified_human),
        **_lang_subs(f"/{section.slug}/"),
    }
    return render_template_with_placeholders(template, substitutions)


LANDING_DESCRIPTION = (
    "Agentic coding - letting an AI agent read, write, run, and verify your "
    "code - is a control problem, not a tooling problem. A vendor-neutral "
    "field manual: the primitives, the six-phase loop, AGENTS.md, governance, "
    "kill signals, brownfield patterns, 90-day adoption."
)

READ_DESCRIPTION = (
    "The full text of Ship It With AI: a vendor-neutral field manual for "
    "agentic coding. Architecture, method, and reality for shipping software "
    "with AI coding agents in 2026."
)


def render_landing(template: str, *, title: str, subtitle: str, author: str,
                   toc_html_sidebar: str, toc_html_landing: str,
                   search_index: str, head_schema: str,
                   hash_redirect_js: str,
                   date_modified_human: str) -> str:
    """Render the landing page (/)."""
    substitutions = {
        "PAGE_TITLE": html_lib.escape(CFG.landing_title),
        "PAGE_DESCRIPTION": html_lib.escape(CFG.landing_description),
        "PAGE_URL": _abs("/"),
        "OG_TYPE": "website",
        "OG_URL": _abs("/"),
        "SITE_MODE": "landing",
        "TITLE": html_lib.escape(title),
        "AUTHOR": html_lib.escape(author),
        "BYLINE_HREF": _rel("/about-the-author/#contact"),
        "HEAD_SCHEMA": head_schema,
        "HEAD_EXTRA": hash_redirect_js,
        "TOC": toc_html_sidebar,
        "ARTICLE_BODY": _landing_article_body(subtitle, author,
                                              _rel("/about-the-author/#contact"),
                                              toc_html_landing),
        "SEARCH_INDEX": search_index,
        "DATE_MODIFIED_HUMAN": html_lib.escape(date_modified_human),
        **_lang_subs("/"),
    }
    return render_template_with_placeholders(template, substitutions)


def render_read(template: str, *, title: str, subtitle: str, author: str,
                toc_html_sidebar: str, content_html: str,
                search_index: str, head_schema: str,
                date_modified_human: str) -> str:
    """Render the all-in-one /read/ page."""
    substitutions = {
        "PAGE_TITLE": html_lib.escape(CFG.read_title),
        "PAGE_DESCRIPTION": html_lib.escape(CFG.read_description),
        "PAGE_URL": _abs("/"),  # alternate format of /
        "OG_TYPE": "article",
        "OG_URL": _abs("/read/"),
        "SITE_MODE": "read",
        "TITLE": html_lib.escape(title),
        "AUTHOR": html_lib.escape(author),
        "BYLINE_HREF": "#contact",
        "HEAD_SCHEMA": head_schema,
        "HEAD_EXTRA": '<meta name="robots" content="noindex, follow">',
        "TOC": toc_html_sidebar,
        "ARTICLE_BODY": _read_article_body(content_html, subtitle, author, "#contact"),
        "SEARCH_INDEX": search_index,
        "DATE_MODIFIED_HUMAN": html_lib.escape(date_modified_human),
        **_lang_subs("/read/", hreflang=False),
    }
    return render_template_with_placeholders(template, substitutions)


# 404 body: one H1, dedicated subtitle, and links back into the live site.
# No homepage hero, no cover figure, no JSON-LD. Sits inside the template's
# existing <main class="article" id="top"> so the site chrome is reused.
_FOUR_OH_FOUR_ARTICLE_BODY = '''<header class="article-header">
        <h1 class="article-title">{TITLE}</h1>
        <p class="article-subtitle">{SUBTITLE}</p>
      </header>
      <section style="margin-top:32px;">
        <p>
          <a href="{HOME_HREF}">{HOME_LABEL}</a>
          &nbsp;·&nbsp;
          <a href="{READ_HREF}">{READ_LABEL}</a>
        </p>
      </section>'''


def render_redirect_stub(old_slug: str, new_slug: str, new_title: str) -> str:
    """Emit a tiny redirect-stub HTML page at the old slug.

    Used when a chapter slug is renamed so inbound bookmarks don't dead-end.
    Combines meta-refresh (works without JS), location.replace (immediate
    in modern browsers), and a canonical pointing to the new URL so
    crawlers consolidate ranking.
    """
    new_url = f"/{new_slug}/"
    new_url_absolute = f"https://ship-it-with.ai{new_url}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Moved - {new_title}</title>
  <link rel="canonical" href="{new_url_absolute}">
  <meta http-equiv="refresh" content="0; url={new_url}">
  <meta name="robots" content="noindex, follow">
  <script>location.replace('{new_url}');</script>
</head>
<body>
  <p>This page has moved to <a href="{new_url}">{new_url}</a>.</p>
</body>
</html>
"""


def render_404(template: str, *, title: str, author: str, toc_html: str,
               search_index: str = "[]",
               date_modified_human: str) -> str:
    """Render the 404 page reusing the homepage chrome (topbar / TOC / footer).

    Crucially, the 404 substitutes its own minimal {{ARTICLE_BODY}}, an empty
    {{HEAD_SCHEMA}} (no Book / FAQPage JSON-LD), and a noindex robots meta in
    {{HEAD_EXTRA}} (the only place a later meta in <head> can override the
    template's default index, follow). PAGE_URL points to the 404 path itself
    so canonical/og:url/twitter:url don't claim to be the homepage.
    """
    head_extra = '<meta name="robots" content="noindex, follow">'
    article_body = _FOUR_OH_FOUR_ARTICLE_BODY.format(
        TITLE=html_lib.escape(CFG.notfound_title),
        SUBTITLE=html_lib.escape(CFG.notfound_subtitle),
        HOME_HREF=_rel("/"),
        HOME_LABEL=html_lib.escape(CFG.notfound_home),
        READ_HREF=_rel("/read/"),
        READ_LABEL=html_lib.escape(CFG.notfound_read),
    )
    substitutions = {
        "PAGE_TITLE": html_lib.escape(CFG.notfound_page_title),
        "PAGE_DESCRIPTION": html_lib.escape(CFG.notfound_description),
        "PAGE_URL": _abs("/404.html"),
        "OG_TYPE": "website",
        "OG_URL": _abs("/404.html"),
        "SITE_MODE": "404",
        "TITLE": html_lib.escape(title),
        "AUTHOR": html_lib.escape(author),
        "BYLINE_HREF": _rel("/about-the-author/#contact"),
        "HEAD_SCHEMA": "",
        "HEAD_EXTRA": head_extra,
        "TOC": toc_html,
        "ARTICLE_BODY": article_body,
        "SEARCH_INDEX": search_index,
        "DATE_MODIFIED_HUMAN": html_lib.escape(date_modified_human),
        **_lang_subs("/404.html", hreflang=False),
    }
    return render_template_with_placeholders(template, substitutions)


_LLMS_KIND_LABELS = {
    "foreword":   "Foreword",
    "prologue":   "Prologue",
    "closing":    "Closing",
}


def _llms_label(section: Section) -> str:
    """Friendly link label for llms.txt.

    Examples:
      foreword            → "Foreword"
      prologue            → "Prologue - Nine seconds"
      chapter (slug=ch-1) → "Chapter 1 - The primitives"
      closing             → "Closing"
      appendix (letter A) → "Appendix A - Cost economics"
      about               → "About the author"
      acknowledgments     → "Acknowledgments"
    """
    k = section.kind
    if k == "foreword":
        return CFG.foreword_label
    if k == "closing":
        return CFG.closing_label
    if k == "prologue":
        return f"{CFG.prologue_label} - {section.title}"
    if k == "chapter":
        m = re.match(r"^chapter-(\d+)-", section.slug)
        num = m.group(1) if m else "?"
        return f"{CFG.chapter_word} {num} - {section.title}"
    if k == "appendix":
        # section.title is "<appendix-word> A <sep> Title"; normalize to " - ".
        m = re.match(rf"^{re.escape(CFG.appendix_word)} ([A-Z]).\s*(.+)$", section.title)
        if m:
            return f"{CFG.appendix_word} {m.group(1)} - {m.group(2)}"
        return section.title
    # about / acknowledgments fall through with their plain title.
    return section.title


def render_llms_txt(sections: list[Section]) -> str:
    """Render llms.txt per the emerging convention at https://llmstxt.org/.

    Lists every per-section URL so AI answer engines (ChatGPT, Perplexity, etc.)
    can crawl an authoritative URL index without parsing the SPA. Docs section
    holds the linear reading path (Foreword → Prologue → Chapters → Closing →
    Appendices); Optional holds the meta/back-matter URLs + the /read/ all-in-
    one view.
    """
    docs_order = ["foreword", "prologue", "chapter", "closing", "appendix"]
    optional_kinds = {"about", "acknowledgments", "changelog"}
    base = f"{BASE}{URL_PREFIX}"

    docs_lines: list[str] = []
    for kind in docs_order:
        for s in sections:
            if s.kind != kind:
                continue
            docs_lines.append(f"- [{_llms_label(s)}]({base}/{s.slug}/): {_section_description(s)}")

    optional_lines: list[str] = []
    for s in sections:
        if s.kind in optional_kinds:
            optional_lines.append(f"- [{_llms_label(s)}]({base}/{s.slug}/): {_section_description(s)}")
    optional_lines.append(f"- [{CFG.llms_read_label}]({base}/read/)")

    docs_block = "\n".join(docs_lines)
    optional_block = "\n".join(optional_lines)

    return f"""# {CFG.llms_title}

{CFG.llms_blurb}

{CFG.llms_fulltext_label}: {base}/llms-full.txt

## Docs
{docs_block}

## Optional
{optional_block}

## {CFG.llms_author_heading}
- [Mihai Cvasnievschi](https://www.linkedin.com/in/mihaicvasnievschi/): {CFG.llms_author_line}
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def render_all_in_one_body(md_text: str) -> tuple[str, dict, str, str, str, list, list, list, tuple | None, tuple | None]:
    """Run the full transforms pipeline on the whole source markdown and
    return the rendered <main>-body HTML plus the per-section metadata the
    TOC + search index need.

    Returns: (content_html, reading_times, title, subtitle, author,
              parts, chapters, appendices, foreword, closing).

    Search index is built separately in main() so the anchor_index can be
    threaded in (anchor_index is what populates each entry's `url` field).
    """
    # Pull out front-matter title/subtitle/author from the top lines.
    title_match = re.search(r"^# (.+)$", md_text, re.MULTILINE)
    subtitle_match = re.search(r"^### (.+)$", md_text, re.MULTILINE)
    author_match = re.search(r"^\*\*([^*]+)\*\*\s*$", md_text, re.MULTILINE)

    title = title_match.group(1).strip() if title_match else "Ship It With AI"
    subtitle = subtitle_match.group(1).strip() if subtitle_match else ""
    author = author_match.group(1).strip() if author_match else "Mihai Cvasnievschi"

    # Strip the front-matter from the body so it's not duplicated.
    lines = md_text.split("\n")
    out = []
    in_body = False
    for line in lines:
        if not in_body:
            if line.strip() == "---":
                in_body = True
                continue
            continue
        out.append(line)
    body_md = "\n".join(out).lstrip("\n")

    # Stash the epigraph (blockquote at top of body, if present)
    epigraph_match = re.match(r"^\s*(>.*(?:\n>.*)*)", body_md)
    epigraph_html = ""
    if epigraph_match:
        epigraph_md = epigraph_match.group(1)
        epigraph_lines = [ln[1:].strip() for ln in epigraph_md.split("\n") if ln.startswith(">")]
        epigraph_html = (
            '<div class="epigraph">'
            + "".join(f"<p>{html_lib.escape(l)}</p>" for l in epigraph_lines if l)
            + "</div>"
        )
        body_md = body_md[len(epigraph_md):]
        body_md = re.sub(r"^\s*---\s*\n", "", body_md, count=1)

    # Strip the Contents block (we'll render TOC ourselves)
    body_md = re.sub(
        rf"^## {re.escape(CFG.contents_heading)}.*?(?=^##|^#\s|\Z)", "", body_md, count=1, flags=re.DOTALL | re.MULTILINE
    )

    # Pre-processing pipeline
    body_md = replace_diagrams(body_md)
    body_md, chapters = transform_chapter_headings(body_md)
    body_md, parts = transform_part_headings(body_md)
    body_md, closing = transform_closing(body_md)
    body_md, appendices = transform_appendices(body_md)
    body_md, foreword = transform_foreword(body_md)
    body_md = transform_prologue(body_md)

    # Render markdown
    content_html = render_markdown(body_md)

    # Source notes + artifact boxes
    content_html = transform_source_notes(content_html)
    content_html = transform_artifacts(content_html)

    # Ship-this-week / Try-it-yourself / hr-drop / Case-note wrapping.
    # Shared with apply_transforms (per-chapter pages) via _wrap_callouts.
    content_html = _wrap_callouts(content_html)

    # Appendix C source entries → card layout
    content_html = transform_source_cards(content_html)

    # AGENTS.md de-linking - keep first link per chapter
    content_html = delink_repeated_agents_md(content_html)

    # Per-section copy-link anchors on h2/h3 headings and artifact-boxes.
    content_html = inject_anchor_links(content_html)

    # Reading times per chapter
    reading_times = compute_chapter_reading_times(md_text, chapters)

    # Inject epigraph at the top of content
    content_html = (epigraph_html + content_html) if epigraph_html else content_html

    return (content_html, reading_times, title, subtitle, author,
            parts, chapters, appendices, foreword, closing)


# ---------------------------------------------------------------------------
# Languages
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Lang:
    code: str
    html_lang: str
    og_locale: str
    prefix: str                 # "" for default English, "/ro" for Romanian
    source: Path
    out: Path
    switch_label: str
    lang_switch_aria: str

    # Structural labels
    part_word: str
    chapter_word: str
    appendix_word: str
    foreword_label: str
    closing_label: str
    prologue_label: str
    ack_label: str
    about_label: str
    changelog_label: str
    appendix_title_fmt: str
    title_dash: str
    figure_word: str
    contents_heading: str

    # Callout / source markers
    ship_marker: str
    ship_label: str
    try_marker: str
    try_label: str
    case_marker: str
    case_label: str
    artifact_label: str
    source_note_label: str
    src_claim: str
    src_source: str
    src_where: str
    src_caveat: str
    source_default_cat: tuple
    faq_heading: str
    faq_entries: list

    # TOC
    toc_front_matter: str
    foreword_subitems: list
    front_matter_items: list
    nine_seconds_label: str
    min_label: str
    toc_appendices: str

    # Chapter chrome
    min_read: str
    chapter_nav_aria: str
    title_suffix: str
    crumb_home: str
    crumb_parts: dict

    # Book / page meta
    book_name: str
    book_alt: str
    book_desc: str
    landing_title: str
    landing_description: str
    read_title: str
    read_description: str
    title_keyword: str
    hero_dek: str
    cta_aria: str
    cta_primary: str
    cta_templates: str
    cta_assess: str
    read_note: str

    # 404
    notfound_title: str
    notfound_subtitle: str
    notfound_home: str
    notfound_read: str
    notfound_page_title: str
    notfound_description: str

    # Search subtitles
    search_part: str
    search_frontmatter: str
    search_chapter: str
    search_backmatter: str
    search_appendix: str
    search_appendix_c: str
    appendix_search_sep: str    # regex fragment between appendix label and title

    # llms.txt
    llms_read_label: str
    llms_title: str
    llms_blurb: str
    llms_fulltext_label: str
    llms_author_heading: str
    llms_author_line: str


EN = Lang(
    code="en", html_lang="en", og_locale="en_US", prefix="",
    source=SOURCE, out=SITE_DIR,
    switch_label="EN", lang_switch_aria="Language",
    part_word="Part", chapter_word="Chapter", appendix_word="Appendix",
    foreword_label="Foreword", closing_label="Closing", prologue_label="Prologue",
    ack_label="Acknowledgments", about_label="About the author", changelog_label="Changelog",
    appendix_title_fmt="Appendix {letter}. {title}", title_dash=" - ",
    figure_word="Figure", contents_heading="Contents",
    ship_marker="Ship this week.", ship_label="Ship this week",
    try_marker="Try it yourself.", try_label="Try it yourself",
    case_marker="Case note:", case_label="Case Note",
    artifact_label="Artifact", source_note_label="Source",
    src_claim="Claim", src_source="Source", src_where="Where used", src_caveat="Caveat",
    source_default_cat=("docs", "Tool documentation"),
    faq_heading="Frequently asked questions", faq_entries=FAQ_ENTRIES,
    toc_front_matter="Front Matter",
    foreword_subitems=[
        ("the-shift-in-context", "The shift, in context"),
        ("where-i-am-coming-from", "Where I am coming from"),
        ("what-agentic-ai-means-in-this-book", 'What "agentic AI" means in this manual'),
        ("the-frame-of-this-book", "The frame of this manual"),
    ],
    front_matter_items=[
        ("how-to-read-this-book", "How to read this manual"),
        ("a-note-on-dated-claims", "A note on dated claims"),
        ("scope-and-limits", "Scope and limits"),
        ("cases-used-in-this-book", "Cases used in this manual"),
    ],
    nine_seconds_label="Nine seconds", min_label="min", toc_appendices="Appendices",
    min_read="min read", chapter_nav_aria="Chapter navigation",
    title_suffix=" - Agentic Coding Field Manual", crumb_home="Home",
    crumb_parts={
        "part-i": "Part I - Architecture",
        "part-ii": "Part II - Method",
        "part-iii": "Part III - Reality",
    },
    book_name="Ship It With AI: A Field Manual for Agentic Coding",
    book_alt="Agentic Coding Field Manual",
    book_desc=("A vendor-neutral field manual for shipping software with AI coding "
               "agents. Covers the primitives, the six-phase loop, AGENTS.md, "
               "governance in layers, kill signals, brownfield patterns, and "
               "90-day adoption."),
    landing_title="Agentic Coding: A Field Manual for Shipping Software With AI Agents",
    landing_description=LANDING_DESCRIPTION,
    read_title="Ship It With AI: A Field Manual for Agentic Coding (full text)",
    read_description=READ_DESCRIPTION,
    title_keyword="Agentic Coding Field Manual",
    hero_dek=("Agentic coding - letting an AI agent read, write, run, and verify "
              "your code - is now a control problem, not a tooling problem. Control "
              "the context, the actions, the verification, and the adoption surface. "
              "This field manual is the methodology."),
    cta_aria="Quick start",
    cta_primary="Start with the architecture review",
    cta_templates="Download the templates",
    cta_assess="Book an assessment",
    read_note=("You're reading in single-page mode. The landing page at "
               '<a href="{ROOT}">ship-it-with.ai</a> indexes every chapter.'),
    notfound_title="Page not found",
    notfound_subtitle="The page you were looking for doesn't exist (yet).",
    notfound_home="← Back to the homepage",
    notfound_read="Read the whole manual in one page",
    notfound_page_title="Page not found - Ship It With AI",
    notfound_description=("The page you were looking for doesn't exist. Browse the "
                          "chapter index at ship-it-with.ai or read the whole manual "
                          "in one page."),
    search_part="Part", search_frontmatter="Front matter", search_chapter="Chapter",
    search_backmatter="Back matter", search_appendix="Appendix",
    search_appendix_c="Appendix C - Sources", appendix_search_sep=r"\. ",
    llms_read_label="Read as one page",
    llms_title="Ship It With AI - A Field Manual for Agentic Coding",
    llms_blurb=("> A vendor-neutral field manual for shipping software with AI coding agents.\n"
                "> Covers the primitives, the six-phase loop, AGENTS.md as team infrastructure,\n"
                "> governance in layers, kill signals, brownfield patterns, and 90-day adoption."),
    llms_fulltext_label="Full text in a single markdown file",
    llms_author_heading="Author",
    llms_author_line="author; 25+ years shipping software, now focused on agentic delivery.",
)


# Romanian FAQ - same questions/home_slugs as English, answers in natural
# corporate-Romanian (English technical terms kept in English).
RO_FAQ_ENTRIES = [
    {
        "q": "Ce este programarea cu agenți (agentic coding)?",
        "home_slug": None,
        "a": "Programarea cu agenți e practica de a folosi agenți AI care citesc, scriu, rulează și verifică cod în mare parte singuri, cu oameni în buclă pentru review și guvernanță, nu pentru fiecare apăsare de tastă. Spre deosebire de autocomplete sau de asistenții de chat, un sistem agentic ține un plan în mai mulți pași, execută prin tool-uri reale (filesystem, shell, browser, version control) și scoate munca la verificare, în loc să producă sugestii izolate.",
    },
    {
        "q": "Cu ce diferă programarea cu agenți de AI autocomplete și de vibe coding?",
        "home_slug": None,
        "a": "Autocomplete completează următorul token de sub cursor. Vibe coding acceptă orice generează modelul, cu verificare minimă. Programarea cu agenți stă la mijloc: agentul planifică, editează în mai multe fișiere, rulează teste și raportează, dar omul controlează contextul pe care îl vede agentul, acțiunile pe care le poate face, gate-urile de verificare prin care trece și suprafața de adopție pe care operează. Diferența e disciplina de metodă, nu calitatea modelului.",
    },
    {
        "q": "Ce este AGENTS.md și de ce contează?",
        "home_slug": "chapter-6-agents-md",
        "a": "AGENTS.md e un fișier markdown din rădăcina repository-ului care spune coding agents cum funcționează de fapt proiectul - pattern-uri interzise, convenții, comenzi de build, unde stau lucrurile și greșelile pe care echipa le-a făcut deja. E standardul neutru față de vendor, citit la începutul sesiunii de Codex CLI, Cursor, GitHub Copilot, Gemini CLI și Aider; Claude Code citește echivalentul CLAUDE.md și poate importa AGENTS.md ca să partajeze același conținut. E urmărit ca standard deschis la agents.md.",
    },
    {
        "q": "Cum faci un rollout sigur de coding agents într-o echipă de engineering?",
        "home_slug": "chapter-10-adoption-90-days",
        "a": "Un rollout sigur tratează livrarea cu agenți ca pe o problemă de control, cu cinci straturi de guvernanță: permisiuni, sandbox, secrete, hook-uri de securitate și telemetrie. Pune asta lângă o metodă clară - o buclă în șase faze: research, plan, execute, review, verify, ship - și un arc de adopție de 90 de zile cu trei roluri numite (Champion, Lead, Manager). Sari peste oricare dintre ele și adopția produce mai mult rău decât bine.",
    },
    {
        "q": "Ce este bucla agentică în șase faze?",
        "home_slug": "chapter-5-six-phase-loop",
        "a": "Bucla în șase faze e o disciplină de livrare pentru lucrul cu agenți: Research (agentul mapează codebase-ul într-o notă durabilă), Plan (o listă de task-uri la nivel de fișier, care poate fi revizuită), Execute (subagenți constrânși fac modificările), Review (treceri separate de conformitate cu spec-ul și de calitate a codului), Verify (rulează teste noi, inclusiv teste de UI pe accessibility tree) și Ship (un pull request normal, pe care procesul tău existent îl revizuiește). Cele mai multe eșecuri se întorc la Plan, nu la Research.",
    },
    {
        "q": "Cât costă programarea cu agenți?",
        "home_slug": "appendix-a-cost-economics",
        "a": "Prețul per-seat al tool-ului e linia mică; costul real e total cost of ownership - seat-uri, cheltuiala pe tokeni și utilizare, timpul de review uman pe care îl cere bucla și setup-ul de guvernanță. Felul durabil de a face bugetul e să potrivești tier-ul de seat cu utilizarea reală, nu să cumperi tooling uniform, și să compari costul complet al livrării cu agenți cu costul muncii pe care o înlocuiește, nu cu zero.",
    },
    {
        "q": "Ce este MCP (Model Context Protocol)?",
        "home_slug": "chapter-1-primitives",
        "a": "MCP, Model Context Protocol, e o specificație care lasă un coding agent să se conecteze la tool-uri și surse de date externe - issue trackere, baze de date, documentație, servicii interne - printr-o interfață uniformă. E unul dintre primitivele agentului: unde Tools sunt acțiunile built-in ale agentului, MCP e felul în care agentul ajunge la capabilități cu care nu a venit harness-ul.",
    },
    {
        "q": "Sunt coding agents gata de producție?",
        "home_slug": "chapter-8-readiness-kill-signals",
        "a": "Depinde de codebase, nu de companie. Pregătirea e o întrebare per-proiect, la care răspund cele opt kill signals și un semafor verde/galben/roșu: un modul bine testat, documentat, decuplat, cu o echipă care poate evalua output-ul e verde; un sistem nedocumentat, netestat, strâns cuplat, a cărui echipă nu poate verifica rezultatul e roșu. Cele mai multe companii au un mix, iar mixul îți spune ordinea operațiilor.",
    },
]


RO = Lang(
    code="ro", html_lang="ro", og_locale="ro_RO", prefix="/ro",
    source=REPO_ROOT / "source" / "Ship_It_With_AI.RO.md", out=SITE_DIR / "ro",
    switch_label="RO", lang_switch_aria="Limbă",
    part_word="Partea", chapter_word="Capitolul", appendix_word="Anexa",
    foreword_label="Cuvânt înainte", closing_label="Încheiere", prologue_label="Prolog",
    ack_label="Mulțumiri", about_label="Despre autor", changelog_label="Changelog",
    appendix_title_fmt="Anexa {letter} - {title}", title_dash=" - ",
    figure_word="Figura", contents_heading="Cuprins",
    ship_marker="De pus în practică săptămâna asta.", ship_label="De pus în practică săptămâna asta",
    try_marker="Încearcă și tu.", try_label="Încearcă și tu",
    case_marker="Fișă de caz:", case_label="Fișă de caz",
    artifact_label="Artefact", source_note_label="Sursă",
    src_claim="Afirmația", src_source="Sursa", src_where="Unde e folosită", src_caveat="Atenție",
    source_default_cat=("docs", "Documentație"),
    faq_heading="Întrebări frecvente", faq_entries=RO_FAQ_ENTRIES,
    toc_front_matter="Materie introductivă",
    foreword_subitems=[
        ("the-shift-in-context", "Schimbarea, pusă în context"),
        ("where-i-am-coming-from", "De unde vorbesc"),
        ("what-agentic-ai-means-in-this-book", "Ce înseamnă „AI agentic” în acest manual"),
        ("the-frame-of-this-book", "Structura manualului"),
    ],
    front_matter_items=[
        ("how-to-read-this-book", "Cum se citește manualul"),
        ("a-note-on-dated-claims", "O notă despre afirmațiile datate"),
        ("scope-and-limits", "Aria de acoperire și limitele"),
        ("cases-used-in-this-book", "Cazurile folosite în manual"),
    ],
    nine_seconds_label="Nouă secunde", min_label="min", toc_appendices="Anexe",
    min_read="min de citit", chapter_nav_aria="Navigare între capitole",
    title_suffix=" - Manual de programare cu agenți", crumb_home="Acasă",
    crumb_parts={
        "part-i": "Partea I - Arhitectura",
        "part-ii": "Partea a II-a - Metoda",
        "part-iii": "Partea a III-a - Realitatea",
    },
    book_name="Ship It With AI: Manual de programare cu agenți",
    book_alt="Manual de programare cu agenți",
    book_desc=("Un manual practic, neutru față de vendor, pentru livrarea de software "
               "cu coding agents. Acoperă primitivele, bucla în șase faze, AGENTS.md, "
               "guvernanța în straturi, kill signals, pattern-uri pentru brownfield și "
               "adopția în 90 de zile."),
    landing_title="Programarea cu agenți: un manual practic pentru livrarea de software cu agenți AI",
    landing_description=("Programarea cu agenți - să lași un agent AI să citească, să scrie, "
                         "să ruleze și să verifice codul - e o problemă de control, nu de "
                         "tooling. Un manual practic, neutru față de vendor: primitivele, "
                         "bucla în șase faze, AGENTS.md, guvernanța, kill signals, pattern-uri "
                         "pentru brownfield, adopția în 90 de zile."),
    read_title="Ship It With AI: manual de programare cu agenți (text integral)",
    read_description=("Textul integral din Ship It With AI: un manual practic, neutru față "
                      "de vendor, pentru programarea cu agenți. Arhitectură, metodă și "
                      "realitate pentru livrarea de software cu coding agents în 2026."),
    title_keyword="Manual de programare cu agenți",
    hero_dek=("Programarea cu agenți - să lași un agent AI să citească, să scrie, să ruleze "
              "și să verifice codul - e acum o problemă de control, nu de tooling. Controlezi "
              "contextul, acțiunile, verificarea și suprafața de adopție. Manualul ăsta e metoda."),
    cta_aria="Start rapid",
    cta_primary="Începe cu review-ul de arhitectură",
    cta_templates="Descarcă template-urile",
    cta_assess="Programează o evaluare",
    read_note=("Citești în mod pagină unică. Pagina principală de la "
               '<a href="{ROOT}">ship-it-with.ai</a> indexează fiecare capitol.'),
    notfound_title="Pagina nu a fost găsită",
    notfound_subtitle="Pagina pe care o căutai nu există (încă).",
    notfound_home="← Înapoi la pagina principală",
    notfound_read="Citește tot manualul pe o singură pagină",
    notfound_page_title="Pagina nu a fost găsită - Ship It With AI",
    notfound_description=("Pagina pe care o căutai nu există. Răsfoiește indexul de capitole "
                          "de la ship-it-with.ai sau citește tot manualul pe o singură pagină."),
    search_part="Partea", search_frontmatter="Materie introductivă", search_chapter="Capitol",
    search_backmatter="Materie finală", search_appendix="Anexă",
    search_appendix_c="Anexa C - Surse", appendix_search_sep=r" - ",
    llms_read_label="Citește pe o singură pagină",
    llms_title="Ship It With AI - Manual de programare cu agenți",
    llms_blurb=("> Un manual practic, neutru față de vendor, pentru livrarea de software cu coding agents.\n"
                "> Acoperă primitivele, bucla în șase faze, AGENTS.md ca infrastructură de echipă,\n"
                "> guvernanța în straturi, kill signals, pattern-uri pentru brownfield și adopția în 90 de zile."),
    llms_fulltext_label="Text integral într-un singur fișier markdown",
    llms_author_heading="Autor",
    llms_author_line="autor; 25+ ani de livrat software, acum concentrat pe delivery cu agenți.",
)

LANGS = [EN, RO]


def set_language(lang: Lang) -> None:
    """Rebind the per-language build context: CFG, URL_PREFIX, and every
    heading/marker regex the pipeline matches against. English reproduces the
    historical patterns exactly so the default build is byte-stable."""
    global CFG, URL_PREFIX
    global _PART_RE, _PROLOGUE_RE, _CLOSING_RE, _CHAPTER_NUM_RE, _FOREWORD_RE
    global _ACK_RE, _ABOUT_RE, _CHANGELOG_RE, _APPENDIX_RE
    global PART_RE, CHAPTER_PAIR_RE, CLOSING_RE, PROLOGUE_RE, APPENDIX_RE
    global FOREWORD_TRANSFORM_RE, _NEXT_BOUNDARY_RE, FIGURE_RENDERERS_BY_CAPTION_KEY
    global SOURCE_GROUPS, SOURCE_ENTRY_RE, SOURCE_NOTE_RE, ARTIFACT_RE

    CFG = lang
    URL_PREFIX = lang.prefix

    if lang.code == "en":
        _PART_RE = re.compile(r"^# Part ([IVX]+) - (.+)$")
        _PROLOGUE_RE = re.compile(r"^# Prologue\s*$")
        _CLOSING_RE = re.compile(r"^# Closing\b.*$")
        _CHAPTER_NUM_RE = re.compile(r"^## Chapter \d+\s*$")
        _FOREWORD_RE = re.compile(r"^## Foreword\b.*$")
        _ACK_RE = re.compile(r"^## Acknowledgments\b.*$")
        _ABOUT_RE = re.compile(r"^## About the author\b.*$")
        _CHANGELOG_RE = re.compile(r"^## Changelog\b.*$")
        _APPENDIX_RE = re.compile(r"^## Appendix ([A-Z])\.\s*(.+)$")
        PART_RE = re.compile(r"^# Part (?P<num>[IVX]+)\s*-\s*(?P<title>.+)$", re.MULTILINE)
        CHAPTER_PAIR_RE = re.compile(r"^## (?P<num>Chapter \d+)\n## (?P<title>[^\n]+)$", re.MULTILINE)
        CLOSING_RE = re.compile(r"^# Closing\s*-\s*(?P<title>.+)$", re.MULTILINE)
        PROLOGUE_RE = re.compile(r"^# Prologue\s*$", re.MULTILINE)
        APPENDIX_RE = re.compile(r"^## (Appendix [A-Z])\. (.+)$", re.MULTILINE)
        FOREWORD_TRANSFORM_RE = re.compile(r"^## Foreword\s*-\s*(?P<title>.+)$", re.MULTILINE)
        _NEXT_BOUNDARY_RE = re.compile(
            r"(?m)^(?:## Chapter \d+\b|# Part [IVX]+\b|# Closing\b|"
            r"## Appendix [A-Z]\.|## About the author\b|## Changelog\b)"
        )
        FIGURE_RENDERERS_BY_CAPTION_KEY = [
            ("primitives and the harness", diagram_primitives),
            ("five governance layers", diagram_layers),
            ("six-phase loop", diagram_loop),
            ("kill signals and the traffic", diagram_traffic_light),
            ("90-day adoption arc", diagram_arc),
        ]
        SOURCE_GROUPS = {
            "Studies and research":                    ("study",    "Study"),
            "Named incidents":                         ("incident", "Incident"),
            "Vulnerabilities with patch versions":     ("vuln",     "Vulnerability"),
            "Tool documentation":                      ("docs",     "Tool documentation"),
            "Marketplaces and plugin ecosystems":      ("market",   "Marketplace"),
            "Memory primitive sources":                ("memory",   "Memory primitive"),
            "Permissions / Sandbox primitive sources": ("perms",    "Permissions / Sandbox primitive"),
        }
        SOURCE_ENTRY_RE = re.compile(
            r"<p>\s*<strong>Claim:</strong>\s*(?P<claim>.*?)\s*"
            r"<strong>Source:</strong>\s*(?P<source>.*?)\s*"
            r"<strong>Where used:</strong>\s*(?P<where>.*?)\s*"
            r"<strong>Caveat:</strong>\s*(?P<caveat>.*?)\s*</p>",
            re.DOTALL,
        )
        SOURCE_NOTE_RE = re.compile(r'<p><em>Source note\.\s*(?P<body>.*?)</em></p>', re.DOTALL)
        ARTIFACT_RE = re.compile(
            r'<p><strong>Artifact:\s*(?P<title>[^<]+?)\.</strong>\s*(?P<body>.*?)</p>', re.DOTALL)
    else:  # Romanian
        _PART_RE = re.compile(r"^# Partea (.+?) - (.+)$")
        _PROLOGUE_RE = re.compile(r"^# Prolog\s*$")
        _CLOSING_RE = re.compile(r"^# Încheiere\b.*$")
        _CHAPTER_NUM_RE = re.compile(r"^## Capitolul \d+\s*$")
        _FOREWORD_RE = re.compile(r"^## Cuvânt înainte\b.*$")
        _ACK_RE = re.compile(r"^## Mulțumiri\b.*$")
        _ABOUT_RE = re.compile(r"^## Despre autor\b.*$")
        _CHANGELOG_RE = re.compile(r"^## Changelog\b.*$")
        _APPENDIX_RE = re.compile(r"^## Anexa ([A-Z]) - (.+)$")
        PART_RE = re.compile(r"^# Partea (?P<num>.+?) - (?P<title>.+)$", re.MULTILINE)
        CHAPTER_PAIR_RE = re.compile(r"^## (?P<num>Capitolul \d+)\n## (?P<title>[^\n]+)$", re.MULTILINE)
        CLOSING_RE = re.compile(r"^# Încheiere\s*-\s*(?P<title>.+)$", re.MULTILINE)
        PROLOGUE_RE = re.compile(r"^# Prolog\s*$", re.MULTILINE)
        APPENDIX_RE = re.compile(r"^## (Anexa [A-Z]) - (.+)$", re.MULTILINE)
        FOREWORD_TRANSFORM_RE = re.compile(r"^## Cuvânt înainte\s*-\s*(?P<title>.+)$", re.MULTILINE)
        _NEXT_BOUNDARY_RE = re.compile(
            r"(?m)^(?:## Capitolul \d+\b|# Partea |# Încheiere\b|"
            r"## Anexa [A-Z] |## Despre autor\b|## Changelog\b)"
        )
        FIGURE_RENDERERS_BY_CAPTION_KEY = [
            ("Componentele principale și harness-ul", diagram_primitives),
            ("cinci straturi de guvernanță", diagram_layers),
            ("Bucla în șase faze", diagram_loop),
            ("Kill signals și regula de decizie", diagram_traffic_light),
            ("arcul de adopție de 90 de zile", diagram_arc),
        ]
        SOURCE_GROUPS = {
            "Studii și cercetare":                          ("study",    "Studiu"),
            "Incidente cunoscute":                          ("incident", "Incident"),
            "Vulnerabilități cu versiuni de patch":         ("vuln",     "Vulnerabilitate"),
            "Documentația tool-urilor":                     ("docs",     "Documentație"),
            "Marketplace-uri și ecosisteme de plugin-uri":  ("market",   "Marketplace"),
            "Surse pentru primitivul Memory":               ("memory",   "Primitivul Memory"),
            "Surse pentru primitivul Permisiuni / Sandbox": ("perms",    "Primitivul Permisiuni / Sandbox"),
        }
        SOURCE_ENTRY_RE = re.compile(
            r"<p>\s*<strong>Afirmația:</strong>\s*(?P<claim>.*?)\s*"
            r"<strong>Sursa:</strong>\s*(?P<source>.*?)\s*"
            r"<strong>Unde e folosită:</strong>\s*(?P<where>.*?)\s*"
            r"<strong>Atenție:</strong>\s*(?P<caveat>.*?)\s*</p>",
            re.DOTALL,
        )
        SOURCE_NOTE_RE = re.compile(r'<p><em>Notă despre surse\.\s*(?P<body>.*?)</em></p>', re.DOTALL)
        ARTIFACT_RE = re.compile(
            r'<p><strong>Artefact:\s*(?P<title>[^<]+?)\.</strong>\s*(?P<body>.*?)</p>', re.DOTALL)


# Static template-chrome strings to localize for non-English builds. Each tuple
# is (english_substring, translation). Applied to the fully-rendered page; the
# English substrings only ever appear in the template chrome (the article body
# is already in the target language), so the replacements are unambiguous.
_CHROME_RO = [
    # topbar
    ('aria-label="Toggle navigation"', 'aria-label="Comută navigarea"'),
    ('title="Search (Ctrl K)"', 'title="Căutare (Ctrl K)"'),
    ('aria-label="Open search"', 'aria-label="Deschide căutarea"'),
    ('<span class="search-trigger-label">Search</span>', '<span class="search-trigger-label">Caută</span>'),
    ('Press <kbd>?</kbd> for shortcuts', 'Apasă <kbd>?</kbd> pentru scurtături'),
    ('aria-label="Reading width: medium"', 'aria-label="Lățime de citire: medie"'),
    ('title="Reading width"', 'title="Lățime de citire"'),
    ('aria-label="Decrease font size"', 'aria-label="Micșorează fontul"'),
    ('aria-label="Increase font size"', 'aria-label="Mărește fontul"'),
    ('aria-label="Toggle theme"', 'aria-label="Comută tema"'),
    # sidebar
    ('<span>Contents</span>', '<span>Cuprins</span>'),
    ('aria-label="Hide contents"', 'aria-label="Ascunde cuprinsul"'),
    ('title="Hide contents"', 'title="Ascunde cuprinsul"'),
    ('aria-label="Show contents"', 'aria-label="Arată cuprinsul"'),
    ('<span class="toc-rail-label">Contents</span>', '<span class="toc-rail-label">Cuprins</span>'),
    # search overlay
    ('>Search the manual</label>', '>Caută în manual</label>'),
    ('placeholder="Search chapters, sections, ideas..."', 'placeholder="Caută capitole, secțiuni, idei..."'),
    ('aria-label="Close search"', 'aria-label="Închide căutarea"'),
    ('aria-label="Search results"', 'aria-label="Rezultatele căutării"'),
    ('>No results. Try a different phrase.</p>', '>Niciun rezultat. Încearcă altă formulare.</p>'),
    ('>Search across parts, chapters, sections, and appendices.</p>',
     '>Caută în părți, capitole, secțiuni și anexe.</p>'),
    ('</kbd> navigate', '</kbd> navighează'),
    ('</kbd> open', '</kbd> deschide'),
    ('</kbd> close', '</kbd> închide'),
    # keyboard help modal
    ('>Keyboard shortcuts</p>', '>Scurtături de tastatură</p>'),
    ('aria-label="Close shortcuts"', 'aria-label="Închide scurtăturile"'),
    ('<th scope="col">Key</th>', '<th scope="col">Tastă</th>'),
    ('<th scope="col">Action</th>', '<th scope="col">Acțiune</th>'),
    ('<td>Show this help</td>', '<td>Arată acest ajutor</td>'),
    ('<td>Close overlays and menus</td>', '<td>Închide overlay-urile și meniurile</td>'),
    ('<span class="kbd-or">or</span>', '<span class="kbd-or">sau</span>'),
    ('<td>Open search</td>', '<td>Deschide căutarea</td>'),
    ('<td>Open search (secondary)</td>', '<td>Deschide căutarea (secundar)</td>'),
    ('<td>Previous / next chapter</td>', '<td>Capitolul anterior / următor</td>'),
    ('<td>Jump to top</td>', '<td>Sari la început</td>'),
    ('<td>Jump to bottom</td>', '<td>Sari la final</td>'),
    ('<td>Toggle theme</td>', '<td>Comută tema</td>'),
    ('<td>Decrease / increase font size</td>', '<td>Micșorează / mărește fontul</td>'),
    ('>Shortcuts are disabled while typing in a field.</p>',
     '>Scurtăturile sunt dezactivate cât scrii într-un câmp.</p>'),
    # footer
    ('Last updated', 'Ultima actualizare'),
    ('· Bucharest · All rights reserved', '· București · Toate drepturile rezervate'),
    ('href="/changelog/"', 'href="/ro/changelog/"'),
    # head: per-language markdown mirrors + search index
    ('href="https://ship-it-with.ai/llms-full.txt"', 'href="https://ship-it-with.ai/ro/llms-full.txt"'),
    ('href="https://ship-it-with.ai/llms.txt"', 'href="https://ship-it-with.ai/ro/llms.txt"'),
    ("fetch('/search-index.json')", "fetch('/ro/search-index.json')"),
    # JS-generated visible strings
    ("toast.textContent = 'Link copied';", "toast.textContent = 'Link copiat';"),
    ("label.textContent = 'Copy';", "label.textContent = 'Copiază';"),
    ("label.textContent = 'Copied';", "label.textContent = 'Copiat';"),
    ("label.textContent = 'Press Ctrl+C';", "label.textContent = 'Apasă Ctrl+C';"),
    ("aria-label', 'Copy to clipboard'", "aria-label', 'Copiază în clipboard'"),
    ("aria-label', 'Copied to clipboard'", "aria-label', 'Copiat în clipboard'"),
    ("'Reading width: '", "'Lățime de citire: '"),
    ("collapsed ? 'Show contents' : 'Hide contents'", "collapsed ? 'Arată cuprinsul' : 'Ascunde cuprinsul'"),
    ("status.textContent = '0 results';", "status.textContent = '0 rezultate';"),
    ("announce.textContent = 'No results for ' + trimmed;",
     "announce.textContent = 'Niciun rezultat pentru ' + trimmed;"),
    ("n + ' result' + (n === 1 ? '' : 's')", "n + (n === 1 ? ' rezultat' : ' rezultate')"),
]


def localize_chrome(html: str, lang: Lang) -> str:
    """Translate static template chrome for a non-default language build."""
    if lang.code == "en":
        return html
    for en, tr in _CHROME_RO:
        html = html.replace(en, tr)
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_one(lang: Lang, template: str, deferred_css: str, *, is_default: bool) -> list:
    """Build one language into lang.out. Returns the parsed sections (used by
    the caller to emit a combined sitemap)."""
    set_language(lang)
    md_text = lang.source.read_text()

    sections = parse_sections(md_text)
    anchor_index = build_anchor_index(sections)
    legacy_to_full = build_legacy_to_full_slug(sections)
    for s in sections:
        s.reading_time_min = compute_section_reading_time(s.body_md)

    out = lang.out
    out.mkdir(parents=True, exist_ok=True)

    (content_html, reading_times, title, subtitle, author,
     parts, chapters, appendices, foreword, closing) = render_all_in_one_body(md_text)

    search_json = build_search_index(md_text, parts, chapters, appendices,
                                     foreword, closing, anchor_index=anchor_index)
    (out / "search-index.json").write_text(search_json)
    inline_index = "[]"

    toc_sidebar_read = build_toc(parts, chapters, appendices, foreword, closing,
                                 reading_times=reading_times, mode="in-page")
    toc_chapter_url = build_toc(parts, chapters, appendices, foreword, closing,
                                reading_times=reading_times, mode="chapter-url",
                                legacy_to_full_slug=legacy_to_full)

    number_of_pages = max(1, round(len(md_text.split()) / 250))
    _now_utc = _content_date()
    date_modified = _now_utc.strftime("%Y-%m-%d")
    date_modified_human = lang_date_human(_now_utc, lang)
    book_org_schema = _homepage_head_schema(author, number_of_pages, date_modified)
    head_schema_landing = book_org_schema + "\n  " + faq_jsonld(CFG.faq_entries)
    head_schema_read = book_org_schema

    hash_redirect_js = render_hash_redirect_js(sections)

    def emit(path: Path, html: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(localize_chrome(html, lang))

    emit(out / "index.html", render_landing(
        template, title=title, subtitle=subtitle, author=author,
        toc_html_sidebar=toc_chapter_url, toc_html_landing=toc_chapter_url,
        search_index=inline_index, head_schema=head_schema_landing,
        hash_redirect_js=hash_redirect_js, date_modified_human=date_modified_human))

    emit(out / "read" / "index.html", render_read(
        template, title=title, subtitle=subtitle, author=author,
        toc_html_sidebar=toc_sidebar_read, content_html=content_html,
        search_index=inline_index, head_schema=head_schema_read,
        date_modified_human=date_modified_human))

    assert len(sections) == EXPECTED_PAGE_COUNT, (
        f"[{lang.code}] emitted {len(sections)} sections, expected {EXPECTED_PAGE_COUNT}")
    for i, section in enumerate(sections):
        prev_ = sections[i - 1] if i > 0 else None
        next_ = sections[i + 1] if i + 1 < len(sections) else None
        toc_sidebar_chapter = build_toc(
            parts, chapters, appendices, foreword, closing,
            reading_times=reading_times, mode="chapter-url",
            legacy_to_full_slug=legacy_to_full,
            current_slug=legacy_slug_for_section(section))
        emit(out / section.slug / "index.html", render_chapter(
            template, section, prev_=prev_, next_=next_,
            author=author, title_meta=title,
            toc_html_sidebar=toc_sidebar_chapter, search_index=inline_index,
            anchor_index=anchor_index, date_modified_human=date_modified_human))

    # Renamed-slug redirect stubs (English history only).
    if is_default:
        for old_slug, new_slug, new_title in [
            ("chapter-1-six-primitives", "chapter-1-primitives", "The primitives"),
        ]:
            (out / old_slug).mkdir(exist_ok=True)
            (out / old_slug / "index.html").write_text(
                render_redirect_stub(old_slug, new_slug, new_title))

    emit(out / "404.html", render_404(
        template, title=title, author=author, toc_html=toc_chapter_url,
        search_index=inline_index, date_modified_human=date_modified_human))

    (out / "llms.txt").write_text(render_llms_txt(sections))
    (out / "llms-full.txt").write_text(md_text)
    (out / "sitemap.xml").write_text(render_sitemap(sections))

    print(f"[{lang.code}] wrote {len(sections)} section pages + landing/read/404 to "
          f"{out.relative_to(REPO_ROOT)}/")
    return sections


_RO_MONTHS = ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie",
              "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"]


def lang_date_human(dt: datetime, lang: Lang) -> str:
    if lang.code == "ro":
        return f"{dt.day} {_RO_MONTHS[dt.month - 1]} {dt.year}"
    return dt.strftime("%B %d, %Y")


def main() -> int:
    template_raw = TEMPLATE_PATH.read_text()
    template, _critical_css, deferred_css = split_template_css(template_raw)

    # Reset once, up front, so the Romanian pass (into _site/ro/) does not wipe
    # the English pass.
    reset_site_dir()

    per_lang_sections: list[tuple[Lang, list]] = []
    for lang in LANGS:
        sections = build_one(lang, template, deferred_css, is_default=(lang is EN))
        per_lang_sections.append((lang, sections))

    # Shared root assets (referenced as /<asset> by every page in every
    # language) + the deferred stylesheet, written once.
    (SITE_DIR / "deferred.css").write_text(deferred_css + "\n")
    print(f"Wrote _site/deferred.css ({len(deferred_css) / 1024:.1f} KB)")
    copy_static()
    print(f"Copied static files from {STATIC_DIR.relative_to(REPO_ROOT)}/")

    # Combined sitemap at the root listing every language's URLs.
    REDIRECTED_OLD_SLUGS = {"chapter-1-six-primitives"}
    today = _content_date().strftime("%Y-%m-%d")
    urls: list[str] = []
    for lang, sections in per_lang_sections:
        urls.append(f"{BASE}{lang.prefix}/")
        urls += [f"{BASE}{lang.prefix}/{s.slug}/" for s in sections
                 if s.slug not in REDIRECTED_OLD_SLUGS]
    body = "\n".join(
        f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>' for u in urls)
    (SITE_DIR / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{body}\n</urlset>\n')
    print(f"Wrote _site/sitemap.xml (combined, {len(urls)} URLs)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
