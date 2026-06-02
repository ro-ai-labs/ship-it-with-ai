#!/usr/bin/env python3
"""Convert build/cover.png to cover.webp at exactly 1200x630.

Dev-only one-shot. Run when build/cover.png changes:
    python3 build/cover_to_webp.py

Center-crops to 1200:630 aspect ratio first (no letterboxing), then resizes.
Output goes to ./cover.webp (repo root). Move to build/static/cover.webp in
Commit 2 of the SEO pass.
"""
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
SOURCE = HERE / "cover.png"
STATIC_DIR = HERE / "static"
TARGET_W, TARGET_H = 1200, 630
TARGET_RATIO = TARGET_W / TARGET_H


def main() -> int:
    if not SOURCE.exists():
        raise SystemExit(f"missing source: {SOURCE}")

    img = Image.open(SOURCE).convert("RGB")
    w, h = img.size
    src_ratio = w / h

    if src_ratio > TARGET_RATIO:
        new_w = int(h * TARGET_RATIO)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif src_ratio < TARGET_RATIO:
        new_h = int(w / TARGET_RATIO)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    base = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    for name, w, h in [("cover.webp", TARGET_W, TARGET_H), ("cover-720.webp", 720, 378)]:
        out = STATIC_DIR / name
        base.resize((w, h), Image.Resampling.LANCZOS).save(out, format="WEBP", quality=82, method=6)
        print(f"wrote {out.relative_to(REPO_ROOT)} ({out.stat().st_size / 1024:.1f} KB, {w}x{h})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
