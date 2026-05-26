#!/usr/bin/env python3
"""Build the single-file SPA HTML from Ship_It_With_AI.md.

Usage: python3 build_spa.py
Output: ship_it_with_ai.html (single self-contained file)
"""

import re
import sys
import json
import html as html_lib
from datetime import datetime, timezone
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
SOURCE = REPO_ROOT / "source" / "Ship_It_With_AI.md"
OUTPUT = REPO_ROOT / "index.html"


# ---------------------------------------------------------------------------
# Diagram HTML generators
# ---------------------------------------------------------------------------

def diagram_primitives() -> str:
    return """<figure class="diagram diagram-primitives">
  <div class="harness">
    <div class="harness-label">THE HARNESS</div>
    <div class="primitives-grid">
      <div class="primitive"><div class="primitive-icon">{}</div><div class="primitive-name">context window</div></div>
      <div class="primitive"><div class="primitive-icon">{}</div><div class="primitive-name">tools</div></div>
      <div class="primitive"><div class="primitive-icon">{}</div><div class="primitive-name">skills</div></div>
      <div class="primitive"><div class="primitive-icon">{}</div><div class="primitive-name">plugins</div></div>
      <div class="primitive"><div class="primitive-icon">{}</div><div class="primitive-name">MCP</div></div>
      <div class="primitive primitive-recursive"><div class="primitive-icon">{}</div><div class="primitive-name">subagents</div><div class="primitive-note">the agent, recursively</div></div>
    </div>
    <div class="harness-foot">the agent loop binds them together;<br/>subagents spawn constrained child instances of the agent itself</div>
  </div>
  <figcaption>Figure: The six primitives and the harness that runs them. Subagents are the recursive primitive: each subagent is itself an instance of the other five.</figcaption>
</figure>""".format("◉", "⚙", "✦", "▣", "↔", "⟲")


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
# figure caption like `*Figure: ...*`. Dispatch is by document order, not by
# id (web-manual style drops figure numbering).
FIGURE_BLOCK_RE = re.compile(
    r"```\n.*?\n```\s*\n+\*Figure:\s+[^*]+\*\s*\n",
    re.DOTALL,
)


# Renderers applied in declaration order (matches document order of diagrams).
FIGURE_RENDERERS_ORDERED = [
    diagram_primitives,
    diagram_layers,
    diagram_loop,
    diagram_traffic_light,
    diagram_arc,
]


def replace_diagrams(md_text: str) -> str:
    """Replace ASCII figure blocks with HTML diagram placeholders."""

    counter = {"i": 0}

    def repl(match: re.Match) -> str:
        idx = counter["i"]
        counter["i"] += 1
        if idx >= len(FIGURE_RENDERERS_ORDERED):
            return match.group(0)
        renderer = FIGURE_RENDERERS_ORDERED[idx]
        return f"\n\n<!--RAW_HTML_START-->\n{renderer()}\n<!--RAW_HTML_END-->\n\n"

    result = FIGURE_BLOCK_RE.sub(repl, md_text)
    if counter["i"] != len(FIGURE_RENDERERS_ORDERED):
        raise RuntimeError(
            f"Figure renderer/caption count mismatch: "
            f"{counter['i']} captions, {len(FIGURE_RENDERERS_ORDERED)} renderers"
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
        slug = slugify(num)
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

    def repl(match: re.Match) -> str:
        num = match.group("num")
        title = match.group("title").strip()
        slug = f"part-{num.lower()}"
        parts.append((slug, num, title))
        # H2 (not H1) so the article hero H1 is the only true H1 on the page.
        # Visual styling preserved via .article h2.part-heading CSS.
        return (
            f'<h2 id="{slug}" class="part-heading">'
            f'<span class="part-label">Part {num}</span>'
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
        # H2 (not H1) — see transform_part_headings note.
        return (
            f'<h2 id="closing" class="closing-heading">'
            f'<span class="part-label">Closing</span>'
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
            '<span class="part-label">Prologue</span>'
            '</h2>'
        )

    return PROLOGUE_RE.sub(repl, md_text)


APPENDIX_RE = re.compile(r"^## (Appendix [A-Z])\. (.+)$", re.MULTILINE)


def transform_appendices(md_text: str) -> tuple[str, list[tuple[str, str, str]]]:
    appendices: list[tuple[str, str, str]] = []

    def repl(match: re.Match) -> str:
        label = match.group(1)
        title = match.group(2).strip()
        slug = slugify(label)
        appendices.append((slug, label, title))
        return (
            f'<h2 id="{slug}" class="appendix-heading">'
            f'<span class="appendix-label">{label}</span>'
            f'<span class="appendix-title">{html_lib.escape(title)}</span>'
            f"</h2>"
        )

    return APPENDIX_RE.sub(repl, md_text), appendices


def transform_foreword(md_text: str) -> tuple[str, tuple[str, str] | None]:
    foreword: tuple[str, str] | None = None
    pattern = re.compile(r"^## Foreword\s*-\s*(?P<title>.+)$", re.MULTILINE)

    def repl(match: re.Match) -> str:
        nonlocal foreword
        title = match.group("title").strip()
        foreword = ("foreword", title)
        return (
            f'<h2 id="foreword" class="foreword-heading">'
            f'<span class="appendix-label">Foreword</span>'
            f'<span class="appendix-title">{html_lib.escape(title)}</span>'
            f"</h2>"
        )

    return pattern.sub(repl, md_text), foreword


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.strip().lower())
    return re.sub(r"[\s_-]+", "-", text)


# Appendix C - Sources and Further Reading: rewrite the four-bold-paragraph
# entries as semantic <article> cards with category accent.
SOURCE_GROUPS = {
    "Studies and research":                ("study",    "Study"),
    "Named incidents":                     ("incident", "Incident"),
    "Vulnerabilities with patch versions": ("vuln",     "Vulnerability"),
    "Tool documentation":                  ("docs",     "Tool documentation"),
    "Marketplaces and plugin ecosystems":  ("market",   "Marketplace"),
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
            '<span class="source-note-label">Source</span>'
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
            '<span class="artifact-label">Artifact</span>'
            '</div>'
            f'<h4 class="artifact-title">{title}</h4>'
            f'<p>{body}</p>'
            '</aside>'
        )
    return ARTIFACT_RE.sub(repl, html)


AGENTS_LINK_RE = re.compile(r'<a href="https://agents\.md/?"[^>]*>AGENTS\.md</a>')
CHAPTER_SPLIT_RE = re.compile(r'(<h2 id="chapter-\d+"[^>]*>)')


def delink_repeated_agents_md(html: str) -> str:
    """Keep only the first AGENTS.md link per chapter; unwrap subsequent ones."""
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
    current_cat = ("docs", "Tool documentation")
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
                f'    <dt>Claim</dt><dd class="source-claim">{claim}</dd>\n'
                f'    <dt>Source</dt><dd class="source-source">{source}</dd>\n'
                f'    <dt>Where used</dt><dd class="source-where">{where}</dd>\n'
                f'    <dt>Caveat</dt><dd class="source-caveat">{caveat}</dd>\n'
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
    r"(?m)^(?:## Chapter \d+\b|# Part [IVX]+\b|# Closing\b|## Appendix [A-Z]\.|## About the author\b)"
)


def _strip_markdown(text: str) -> str:
    text = _MD_FENCE_RE.sub(" ", text)
    text = _MD_IMAGE_RE.sub(" ", text)
    text = _MD_LINK_RE.sub(r"\1", text)
    text = _MD_INLINE_CODE_RE.sub(" ", text)
    text = _MD_HEADING_RE.sub(" ", text)
    text = _MD_HTML_TAG_RE.sub(" ", text)
    text = _MD_BLOCKQUOTE_RE.sub("", text)
    text = _MD_LISTMARK_RE.sub("", text)
    text = _MD_ATTR_RE.sub("", text)
    text = _MD_EMPH_RE.sub("", text)
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


def build_search_index(md_text, parts, chapters, appendices, foreword, closing):
    entries = []
    seen = set()

    def add(entry):
        if entry["id"] in seen:
            return
        seen.add(entry["id"])
        entries.append(entry)

    # Parts
    for slug, num, title in parts:
        m = re.search(rf"^# Part {re.escape(num)}\b", md_text, re.MULTILINE)
        pos = m.start() if m else 0
        add({"id": slug, "title": f"Part {num}: {title}", "subtitle": "Part",
             "snippet": _snippet_for(md_text, pos), "kind": "part"})

    # Foreword
    if foreword:
        m = re.search(r"^## Foreword\b", md_text, re.MULTILINE)
        if m:
            add({"id": "foreword", "title": f"Foreword: {foreword[1]}",
                 "subtitle": "Front matter",
                 "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # Other front matter H2s
    for slug, label in [
        ("how-to-read-this-book", "How to read this manual"),
        ("a-note-on-dated-claims", "A note on dated claims"),
        ("scope-and-limits", "Scope and limits"),
        ("cases-used-in-this-book", "Cases used in this manual"),
    ]:
        m = re.search(rf"^## {re.escape(label)}\b", md_text, re.MULTILINE)
        if m:
            add({"id": slug, "title": label, "subtitle": "Front matter",
                 "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # Prologue
    m = re.search(r"^## Nine seconds\b", md_text, re.MULTILINE)
    if m:
        add({"id": "nine-seconds", "title": "Nine seconds", "subtitle": "Prologue",
             "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # Chapters
    for slug, num, title in chapters:
        pair_re = re.compile(rf"^## {re.escape(num)}\n## {re.escape(title)}\s*$", re.MULTILINE)
        m = pair_re.search(md_text)
        if not m:
            continue
        end_of_heading = md_text.find("\n", m.end())
        pos = end_of_heading if end_of_heading > 0 else m.start()
        add({"id": slug, "title": f"{num}: {title}", "subtitle": "Chapter",
             "snippet": _snippet_for(md_text, pos), "kind": "chapter"})

    # Closing
    if closing:
        m = re.search(r"^# Closing\b", md_text, re.MULTILINE)
        if m:
            add({"id": "closing", "title": f"Closing: {closing[1]}",
                 "subtitle": "Closing",
                 "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # About the author (sits between Closing and Appendices)
    m = re.search(r"^## About the author\b", md_text, re.MULTILINE)
    if m:
        add({"id": "about-the-author", "title": "About the author",
             "subtitle": "Back matter",
             "snippet": _snippet_for(md_text, m.start()), "kind": "section"})

    # Appendices
    for slug, label, title in appendices:
        m = re.search(rf"^## {re.escape(label)}\. {re.escape(title)}\b", md_text, re.MULTILINE)
        if m:
            add({"id": slug, "title": f"{label}: {title}", "subtitle": "Appendix",
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
        if stripped.startswith("## Foreword"):
            parent_label = "Foreword"
            parent_title = foreword[1] if foreword else "Foreword"
            continue
        if stripped.startswith("## Chapter "):
            for cslug, cnum, ctitle in chapters:
                if stripped == f"## {cnum}":
                    parent_label = cnum
                    parent_title = ctitle
                    break
            continue
        if stripped.startswith("## Appendix "):
            apm = re.match(r"## (Appendix [A-Z])\. (.+)", stripped)
            if apm:
                parent_label = apm.group(1)
                parent_title = apm.group(2).strip()
            continue
        if stripped.startswith("# Part "):
            pm = re.match(r"# Part ([IVX]+)\s*-\s*(.+)", stripped)
            if pm:
                parent_label = f"Part {pm.group(1)}"
                parent_title = pm.group(2).strip()
            continue
        if stripped.startswith("# Closing"):
            parent_label = "Closing"
            parent_title = closing[1] if closing else "Closing"
            continue
        if stripped.startswith("# Prologue"):
            parent_label = "Prologue"
            parent_title = "Prologue"
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
            subtitle = f"{parent_label} - {parent_title}" if parent_label else ""
            add({"id": slug, "title": title, "subtitle": subtitle,
                 "snippet": _snippet_for(md_text, line_start), "kind": "subsection"})

    # Source-group anchors from Appendix C
    for group_title in SOURCE_GROUPS:
        slug = slugify(group_title)
        m = re.search(rf"^### {re.escape(group_title)}\b", md_text, re.MULTILINE)
        if not m:
            continue
        add({"id": slug, "title": group_title, "subtitle": "Appendix C - Sources",
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

def build_toc(parts, chapters, appendices, foreword, closing, reading_times=None) -> str:
    reading_times = reading_times or {}
    """Build TOC HTML structured by Part."""
    # Map each chapter slug to which Part it belongs to.
    # Chapters list is in document order. Parts list is in document order.
    # We re-derive grouping from the source markdown's chapter-to-part mapping.
    # Hard-code the mapping for this book (small, fixed structure):
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

    parts_map = {slug: (num, title) for slug, num, title in parts}

    sections = []

    # Front matter: Foreword (with its 4 H3 subsections nested) + the other
    # H2 sections that orient the reader before Part I.
    sections.append('<div class="toc-section">')
    sections.append('<div class="toc-section-title">Front Matter</div>')
    sections.append('<ul class="toc-list toc-list-flat">')
    if foreword:
        sections.append(
            f'  <li><a href="#foreword">Foreword - {html_lib.escape(foreword[1])}</a>'
        )
        sections.append('    <ul class="toc-sublist">')
        sections.append('      <li><a href="#the-shift-in-context">The shift, in context</a></li>')
        sections.append('      <li><a href="#where-i-am-coming-from">Where I am coming from</a></li>')
        sections.append('      <li><a href="#what-agentic-ai-means-in-this-book">What "agentic AI" means in this manual</a></li>')
        sections.append('      <li><a href="#the-frame-of-this-book">The frame of this manual</a></li>')
        sections.append('    </ul>')
        sections.append('  </li>')
    sections.append('  <li><a href="#how-to-read-this-book">How to read this manual</a></li>')
    sections.append('  <li><a href="#a-note-on-dated-claims">A note on dated claims</a></li>')
    sections.append('  <li><a href="#scope-and-limits">Scope and limits</a></li>')
    sections.append('  <li><a href="#cases-used-in-this-book">Cases used in this manual</a></li>')
    sections.append("</ul></div>")

    # Prologue
    sections.append('<div class="toc-section">')
    sections.append('<div class="toc-section-title">Prologue</div>')
    sections.append('<ul class="toc-list toc-list-flat">')
    sections.append('  <li><a href="#nine-seconds">Nine seconds</a></li>')
    sections.append("</ul></div>")

    # Parts + chapters
    for slug, num, title in parts:
        sections.append('<div class="toc-section">')
        sections.append(
            f'<div class="toc-section-title"><a href="#{slug}">Part {num} - {html_lib.escape(title)}</a></div>'
        )
        sections.append('<ul class="toc-list">')
        for ch_slug, ch_num, ch_title in chapters:
            if chapter_to_part.get(ch_slug) == slug:
                ch_n = ch_num.replace("Chapter ", "")
                mins = reading_times.get(ch_slug)
                time_html = f'<span class="toc-time">{mins} min</span>' if mins else ""
                sections.append(
                    f'  <li><a href="#{ch_slug}"><span class="toc-num">{ch_n}</span>'
                    f'<span class="toc-text">Chapter {ch_n} — {html_lib.escape(ch_title)}</span>{time_html}</a></li>'
                )
        sections.append("</ul></div>")

    # Closing
    if closing:
        sections.append('<div class="toc-section">')
        sections.append('<div class="toc-section-title"><a href="#closing">Closing</a></div>')
        sections.append("</div>")

    # About the author (sits between Closing and Appendices).
    sections.append('<div class="toc-section">')
    sections.append('<div class="toc-section-title"><a href="#about-the-author">About the author</a></div>')
    sections.append("</div>")

    # Appendices
    if appendices:
        sections.append('<div class="toc-section">')
        sections.append('<div class="toc-section-title">Appendices</div>')
        sections.append('<ul class="toc-list">')
        for slug, label, title in appendices:
            sections.append(
                f'  <li><a href="#{slug}"><span class="toc-num">{label.replace("Appendix ", "")}</span>{html_lib.escape(title)}</a></li>'
            )
        sections.append("</ul></div>")

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Template
# ---------------------------------------------------------------------------

TEMPLATE_PATH = HERE / "spa_template.html"

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


def render_template(title, subtitle, author, toc_html, content_html,
                    search_index="[]", total_word_count=0) -> tuple[str, str]:
    """Render the SPA HTML and return (html, deferred_css).

    Substitutes the standard placeholders plus the SEO-pass placeholders
    {{NUMBER_OF_PAGES}} and {{DATE_MODIFIED}} used by the Book JSON-LD block.
    """
    template_raw = TEMPLATE_PATH.read_text()
    template, _critical_css, deferred_css = split_template_css(template_raw)
    html = (
        template.replace("{{TITLE}}", html_lib.escape(title))
        .replace("{{SUBTITLE}}", html_lib.escape(subtitle))
        .replace("{{AUTHOR}}", html_lib.escape(author))
        .replace("{{TOC}}", toc_html)
        .replace("{{CONTENT}}", content_html)
        .replace("{{SEARCH_INDEX}}", search_index)
        .replace("{{DATE_MODIFIED}}",
                 datetime.now(timezone.utc).strftime("%Y-%m-%d"))
        .replace("{{NUMBER_OF_PAGES}}",
                 str(max(1, round(total_word_count / 250))))
    )
    return html, deferred_css


def render_404(template: str) -> str:
    """Render a 404 page using the site template chrome.

    The body is a short "Page not found" message linking back to the homepage
    and to the all-in-one /read/ mode where every section is reachable.
    """
    body = '''
<main class="article" id="top">
  <header class="article-header">
    <h1 class="article-title">Page not found</h1>
    <p class="article-subtitle">The page you were looking for doesn't exist (yet).</p>
  </header>
  <section style="text-align:center; margin-top:48px;">
    <p>
      <a href="/">← Back to the homepage</a>
      &nbsp;·&nbsp;
      <a href="/read/">Read the whole manual in one page</a>
    </p>
  </section>
</main>
'''
    return template.replace("{{CONTENT}}", body)


def render_llms_txt() -> str:
    """Render llms.txt per the emerging convention at https://llmstxt.org/.

    Lists all site sections so AI answer engines (ChatGPT, Perplexity, etc.)
    can crawl an authoritative URL index without parsing the SPA. The chapter
    URL list here is the Commit 1 stub — full per-chapter URLs land in Commit
    3 when the SPA splits.
    """
    return """# Ship It With AI - A Field Manual for Agentic Coding

> A vendor-neutral field manual for shipping software with AI coding agents.
> Covers six primitives, the six-phase loop, AGENTS.md as team infrastructure,
> governance in layers, kill signals, brownfield patterns, and 90-day adoption.

## Docs
- [Ship It With AI - the full manual](https://ship-it-with.ai/)
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    md_text = SOURCE.read_text()

    # Pull out front-matter title/subtitle/author from the top lines.
    title_match = re.search(r"^# (.+)$", md_text, re.MULTILINE)
    subtitle_match = re.search(r"^### (.+)$", md_text, re.MULTILINE)
    author_match = re.search(r"^\*\*([^*]+)\*\*\s*$", md_text, re.MULTILINE)

    title = title_match.group(1).strip() if title_match else "Ship It With AI"
    subtitle = subtitle_match.group(1).strip() if subtitle_match else ""
    author = author_match.group(1).strip() if author_match else "Mihai Cvasnievschi"

    # Strip the front-matter from the body so it's not duplicated.
    # Remove the title line and any lines up to and including the FIRST --- divider.
    # The epigraph and Contents come after that divider; we extract them separately.
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
        # Skip a trailing --- after the epigraph
        body_md = re.sub(r"^\s*---\s*\n", "", body_md, count=1)

    # Strip the Contents block (we'll render TOC ourselves)
    body_md = re.sub(
        r"^## Contents.*?(?=^##|^#\s|\Z)", "", body_md, count=1, flags=re.DOTALL | re.MULTILINE
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

    # Source notes + artifact boxes — must run before action/try wrapping so
    # the wrapped callouts are stable siblings in the chapter-end stack.
    content_html = transform_source_notes(content_html)
    content_html = transform_artifacts(content_html)

    # Wrap each "Ship this week" paragraph as a styled card, from the bold
    # marker to the next horizontal rule.
    content_html = content_html.replace(
        "<p><strong>Ship this week.</strong></p>",
        '<div class="action-marker"><p><strong>Ship this week.</strong></p>',
    )
    content_html = re.sub(
        r'<div class="action-marker"><p><strong>Ship this week\.</strong></p>(.*?)<hr ?/?>',
        r'<aside class="action-box"><div class="action-label">Ship this week</div>\1</aside>',
        content_html,
        flags=re.DOTALL,
    )

    # Same wrapping for "Try it yourself" boxes (cyan-accented variant).
    content_html = content_html.replace(
        "<p><strong>Try it yourself.</strong></p>",
        '<div class="try-marker"><p><strong>Try it yourself.</strong></p>',
    )
    content_html = re.sub(
        r'<div class="try-marker"><p><strong>Try it yourself\.</strong></p>(.*?)<hr ?/?>',
        r'<aside class="try-box"><div class="try-label">Try it yourself</div>\1</aside>',
        content_html,
        flags=re.DOTALL,
    )

    # Chapter-end stack tightening: drop any <hr> sitting between adjacent
    # callouts (artifact-box / action-box / try-box) so CSS sibling selectors
    # take effect.
    content_html = re.sub(
        r'(</aside>)\s*<hr\s*/?>\s*(?=<aside class="(?:artifact-box|action-box|try-box)")',
        r'\1',
        content_html,
    )

    # Tag case notes
    content_html = re.sub(
        r"<p><strong>Case note:([^<]+)</strong></p>",
        r'<aside class="case-note"><div class="case-note-label">Case Note</div><div class="case-note-title">\1</div>',
        content_html,
    )
    # Close case notes at next hr (best-effort)
    content_html = re.sub(
        r'(<aside class="case-note">.*?<table>.*?</table>)',
        r"\1</aside>",
        content_html,
        flags=re.DOTALL,
    )

    # Tag the "When the agent confidently lies" subsection bold paragraph
    # already body-bold, no change needed

    # Transform Appendix C source entries into card layout
    content_html = transform_source_cards(content_html)

    # AGENTS.md de-linking — keep first link per chapter, unwrap the rest.
    content_html = delink_repeated_agents_md(content_html)

    # Per-section copy-link anchors on h2/h3 headings and artifact-boxes.
    content_html = inject_anchor_links(content_html)

    # Reading times per chapter, then TOC
    reading_times = compute_chapter_reading_times(md_text, chapters)
    toc_html = build_toc(parts, chapters, appendices, foreword, closing, reading_times=reading_times)

    # Inject epigraph at the top of content
    content_html = (epigraph_html + content_html) if epigraph_html else content_html

    # Search index over headings + first-paragraph snippets
    search_json = build_search_index(md_text, parts, chapters, appendices, foreword, closing)

    # Total word count for Book.numberOfPages (~250 words/page is the
    # convention). Commit 2 will switch this to Section-based counting.
    total_word_count = len(md_text.split())

    # Render full SPA
    spa_html, deferred_css = render_template(
        title, subtitle, author, toc_html, content_html, search_json,
        total_word_count=total_word_count,
    )
    OUTPUT.write_text(spa_html)
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Wrote {OUTPUT.relative_to(HERE.parent)} ({size_kb:.1f} KB)")

    # Deferred (async-loaded) CSS for search overlay, kbd-shortcuts overlay,
    # and the anchor-link toast. Loaded via <link rel="preload" onload>.
    (REPO_ROOT / "deferred.css").write_text(deferred_css + "\n")
    print(f"Wrote deferred.css ({len(deferred_css) / 1024:.1f} KB)")

    # 404 page (uses the same chrome).
    template_raw = TEMPLATE_PATH.read_text()
    template_for_404, _, _ = split_template_css(template_raw)
    # Make the 404 self-contained re: substitutions — use the same flow as main.
    html_404 = render_404(template_for_404)
    html_404 = (
        html_404.replace("{{TITLE}}", html_lib.escape("Page not found"))
                .replace("{{SUBTITLE}}", "")
                .replace("{{AUTHOR}}", html_lib.escape(author))
                .replace("{{TOC}}", "")
                .replace("{{SEARCH_INDEX}}", "[]")
                .replace("{{DATE_MODIFIED}}",
                         datetime.now(timezone.utc).strftime("%Y-%m-%d"))
                .replace("{{NUMBER_OF_PAGES}}",
                         str(max(1, round(total_word_count / 250))))
    )
    (REPO_ROOT / "404.html").write_text(html_404)
    print(f"Wrote 404.html ({(REPO_ROOT / '404.html').stat().st_size / 1024:.1f} KB)")

    # llms.txt for AI answer-engine crawlers.
    (REPO_ROOT / "llms.txt").write_text(render_llms_txt())
    print("Wrote llms.txt")

    return 0


if __name__ == "__main__":
    sys.exit(main())
