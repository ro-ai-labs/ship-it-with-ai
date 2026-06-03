#!/usr/bin/env python3
"""Generate favicon.ico + apple-touch-icon.png from the brand mark.

Dev-only one-shot. Run when the mark changes:
    python3 build/make_favicon.py

The mark mirrors build/static/favicon.svg: an amber (#d97706) rounded square
with a white ">" chevron (ship-it / forward). Outputs into build/static/, which
the build copies verbatim into _site/.
"""
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
STATIC = HERE / "static"
AMBER = (217, 119, 6)      # #d97706
WHITE = (255, 255, 255)


def draw(size: int) -> Image.Image:
    """Render the mark at `size` px, supersampled 4x for smooth edges."""
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=AMBER)

    w = max(2, int(s * 0.107))
    x1, x2 = int(s * 0.39), int(s * 0.595)
    y1, ym, y2 = int(s * 0.30), int(s * 0.50), int(s * 0.70)
    d.line([(x1, y1), (x2, ym), (x1, y2)], fill=WHITE, width=w, joint="curve")
    r = w // 2
    for cx, cy in [(x1, y1), (x2, ym), (x1, y2)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)

    return img.resize((size, size), Image.Resampling.LANCZOS)


def main() -> int:
    draw(48).save(STATIC / "favicon.ico", format="ICO",
                  sizes=[(16, 16), (32, 32), (48, 48)])
    draw(180).save(STATIC / "apple-touch-icon.png", format="PNG")
    print(f"wrote {(STATIC / 'favicon.ico').relative_to(HERE.parent)} "
          f"and {(STATIC / 'apple-touch-icon.png').relative_to(HERE.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
