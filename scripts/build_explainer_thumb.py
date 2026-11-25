#!/usr/bin/env python3
"""Make assets/explainer-thumb.jpg: a frame of the explainer film with a brand play button and a duration label.

Needs ffmpeg and Pillow (pip install pillow fonttools brotli). The film itself is not in this repository;
it is on YouTube and linked from the README.

    python3 scripts/build_explainer_thumb.py --video path/to/explainer.mp4 [--at 9]
"""
import argparse
import io
import subprocess
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path(__file__).resolve().parent / "fonts"
OUT = ROOT / "assets" / "explainer-thumb.jpg"
LIME, INK = (215, 255, 58), (20, 20, 19)
W, H = 1280, 720


def static_font(woff2, size, tmp):
    font = TTFont(FONTS / woff2)
    font.flavor = None
    path = Path(tmp) / (woff2 + ".ttf")
    font.save(path)
    return ImageFont.truetype(str(path), size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--at", default="9", help="seconds into the film")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        frame = Path(tmp) / "frame.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", args.at, "-i", args.video,
                        "-frames:v", "1", str(frame)], check=True)
        base = Image.open(frame).convert("RGB").resize((W, H), Image.LANCZOS)
        base = base.convert("RGBA")  # keep the film colours untouched

        # play button: lime disc, ink ring, white halo, soft shadow
        cx, cy, r = 240, 520, 74  # the empty lower-left of this frame, so no text is covered
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).ellipse((cx - r - 6, cy - r + 10, cx + r + 6, cy + r + 22), fill=(20, 20, 19, 120))
        base = Image.alpha_composite(base, shadow.filter(ImageFilter.GaussianBlur(18)))
        d = ImageDraw.Draw(base)
        d.ellipse((cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), fill=(251, 250, 246, 235))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=LIME, outline=INK, width=5)
        d.polygon([(cx - 22, cy - 34), (cx - 22, cy + 34), (cx + 38, cy)], fill=INK)

        # duration label, bottom right: ink pill, lime mono text
        label = "82 s"
        mono = static_font("dm-mono-latin-500.woff2", 30, tmp)
        tw = d.textlength(label, font=mono)
        pw, ph = int(tw + 44), 52
        x1, y1 = W - 36, H - 56
        d.rounded_rectangle((x1 - pw, y1 - ph, x1, y1), radius=ph // 2, fill=INK)
        d.text((x1 - pw / 2, y1 - ph / 2 + 1), label, font=mono, fill=LIME, anchor="mm")

        OUT.parent.mkdir(exist_ok=True)
        base.convert("RGB").save(OUT, quality=86, optimize=True, progressive=True)
    print(f"{OUT.relative_to(ROOT)}: {OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
