#!/usr/bin/env python3
"""Rebuild the README artwork in the SynthSkills "studio lab" brand (design B).

GitHub cannot load web fonts inside an SVG shown through <img>, so every piece of text here is
outlined to vector paths from the brand's own open-licence fonts (SIL OFL, kept in scripts/fonts/):
Bricolage Grotesque (display), Hanken Grotesk (body) and DM Mono (labels). Each SVG carries a
<title> and <desc> instead, and the README gives every image a full alt text.

Needs: pip install fonttools brotli uharfbuzz      (the output is committed; you only need
this to change the artwork)

    python3 scripts/build_readme_assets.py
"""
import io
import json
from html import escape
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"
SITE = "skills.synthlabs.pk"

# Brand colours, from the website's stylesheet.
LIME, LILAC, APRICOT, SKY = "#D7FF3A", "#D4C8F7", "#FFC9A5", "#C2E1F2"
INK = "#141413"
THEMES = {
    "light": dict(bg="#EAE7DF", frame="#DEDAD0", paper="#FBFAF6", white="#FFFFFF", ink=INK,
                  ink2="#55524A", line="#CFCBC1", stroke=None),
    "dark": dict(bg="#141413", frame="#2A2926", paper="#1D1C1A", white="#262522", ink="#F4F1E8",
                 ink2="#A9A598", line="#3A3833", stroke="#2E2D29"),
}


# ---------------------------------------------------------------- text, outlined to paths
class Type:
    """Shapes text with HarfBuzz (so kerning is right) and returns SVG path data."""

    FILES = {
        "display": "bricolage-grotesque-latin-opsz.woff2",
        "body": "hanken-grotesk-latin-wght.woff2",
        "mono400": "dm-mono-latin-400.woff2",
        "mono500": "dm-mono-latin-500.woff2",
    }

    def __init__(self):
        self.faces = {}
        for key, name in self.FILES.items():
            font = TTFont(FONTS / name)
            font.flavor = None
            buf = io.BytesIO()
            font.save(buf)
            self.faces[key] = (hb.Face(buf.getvalue()), font["head"].unitsPerEm)
        self.cache = {}

    def _font(self, kind, size, weight):
        if kind == "mono":
            key, var = ("mono500" if weight >= 500 else "mono400"), None
        elif kind == "display":
            key, var = "display", {"wght": weight, "opsz": max(12, min(96, size))}
        else:
            key, var = "body", {"wght": weight}
        ck = (key, tuple(sorted(var.items())) if var else None)
        if ck not in self.cache:
            font = hb.Font(self.faces[key][0])
            if var:
                font.set_variations(var)
            self.cache[ck] = font
        return self.cache[ck], self.faces[key][1]

    def shape(self, text, kind, size, weight, track):
        font, upm = self._font(kind, size, weight)
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, {"kern": True, "liga": kind != "mono"})
        scale = size / upm
        out, x = [], 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((info.codepoint, x + pos.x_offset * scale, pos.y_offset * scale))
            x += pos.x_advance * scale + track * size
        return font, scale, out, x - track * size

    def width(self, text, kind, size, weight=400, track=0.0):
        return self.shape(text, kind, size, weight, track)[3]

    def path(self, x, y, text, kind, size, weight=400, track=0.0, anchor="start"):
        font, scale, glyphs, width = self.shape(text, kind, size, weight, track)
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        pen = SVGPathPen(None, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
        for gid, gx, gy in glyphs:
            font.draw_glyph_with_pen(gid, TransformPen(pen, (scale, 0, 0, -scale, x + gx, y - gy)))
        return pen.getCommands()

    def wrap(self, text, kind, size, weight, max_width, track=0.0):
        lines, line = [], ""
        for word in text.split():
            trial = (line + " " + word).strip()
            if line and self.width(trial, kind, size, weight, track) > max_width:
                lines.append(line)
                line = word
            else:
                line = trial
        return lines + [line]


TYPE = Type()


def T(x, y, text, kind, size, color, weight=400, track=0.0, anchor="start", opacity=None):
    op = f' fill-opacity="{opacity}"' if opacity is not None else ""
    return f'<path d="{TYPE.path(x, y, text, kind, size, weight, track, anchor)}" fill="{color}"{op}/>'


def head(x, y, text, size, color, weight=800, anchor="start"):
    return T(x, y, text, "display", size, color, weight, -0.035, anchor)


def label(x, y, text, size, color, anchor="start", weight=500):
    return T(x, y, text, "mono", size, color, weight, 0.05, anchor)


# ---------------------------------------------------------------- shapes
def rect(x, y, w, h, r, fill, stroke=None, sw=1.5, extra=""):
    edge = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"{edge}{extra}/>'


def circle(cx, cy, r, fill, stroke=None, sw=1.5):
    edge = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{fill}"{edge}/>'


def bezel(x, y, w, h, r, fill, frame, ring=7):
    """The site's double-bezel card: a thick stone frame around a coloured face."""
    return [rect(x, y, w, h, r, frame), rect(x + ring, y + ring, w - 2 * ring, h - 2 * ring, r - ring + 1, fill)]


def arrow(x, y, direction, color, size=7, sw=2.2):
    """A small chevron arrow head with a stem is drawn by the caller; this is just the head."""
    dx, dy = {"right": (1, 0), "left": (-1, 0), "down": (0, 1)}[direction]
    px, py = -dy, dx
    p1 = (x - dx * size + px * size * .8, y - dy * size + py * size * .8)
    p2 = (x - dx * size - px * size * .8, y - dy * size - py * size * .8)
    return (f'<path d="M{p1[0]:g} {p1[1]:g}L{x:g} {y:g}L{p2[0]:g} {p2[1]:g}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


def hl(x0, x1, baseline, size):
    """A lime highlighter box behind a word, as on the website (.hl)."""
    pad = size * 0.12
    return rect(x0 - pad, baseline - size * 0.80, x1 - x0 + 2 * pad, size * 1.03, size * 0.2, LIME)


def svg(width, height, title, desc, elements):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title>\n<desc id="desc">{escape(desc)}</desc>\n'
            + "\n".join(elements) + "\n</svg>\n")


def canvas(c, w, h):
    return rect(0.5, 0.5, w - 1, h - 1, 40, c["bg"], c["stroke"], 1) if c["stroke"] else rect(0, 0, w, h, 40, c["bg"])


# ---------------------------------------------------------------- banner
def index_card(cx, cy, rot, name_lines, tab, tab_color, w=190, h=106):
    """A tilted skill card, as in the website's receptionist panel."""
    x, y = -w / 2, -h / 2
    e = [rect(x + 4, y + 8, w, h, 15, INK, extra=' fill-opacity=".10"'),
         rect(x, y, w, h, 15, "#FBFAF6", INK, 2),
         circle(x + w - 17, y + 17, 4.5, "#EAE7DF", INK, 1.2)]
    tw = TYPE.width(tab, "mono", 11.5, 500, 0.05)
    e += [rect(x + 14, y - 10, tw + 20, 24, 8, tab_color, INK, 1.4),
          label(x + 24, y + 7, tab, 11.5, INK)]
    for i, line in enumerate(name_lines):
        e.append(T(x + 14, y + 50 + i * 23, line, "mono", 15.5, INK, 500))
    for ly in (y + h - 30, y + h - 14):
        e.append(f'<path d="M{x + 14:g} {ly:g}H{x + w - 14:g}" stroke="#CFCBC1" stroke-width="1.5"/>')
    return f'<g transform="translate({cx:g} {cy:g}) rotate({rot:g})">' + "".join(e) + "</g>"


def banner(theme):
    c = THEMES[theme]
    W, H = 1280, 540
    e = [canvas(c, W, H)]
    # left: headline card
    e += bezel(24, 24, 792, 492, 38, c["paper"], c["frame"])
    e += [circle(80, 85, 5.5, c["ink"]), label(97, 90.5, "A LIVE SKILL LIBRARY FOR AI AGENTS", 15, c["ink2"])]
    size, left = 86, 62
    tr = -0.035
    sp = size * 0.27  # word gap; the tight tracking would otherwise let the highlight touch its neighbours
    base = [180, 260, 340]
    e.append(head(left, base[0], "Give your agents", size, c["ink"]))
    w_the = TYPE.width("the", "display", size, 800, tr)
    w_pb = TYPE.width("playbooks", "display", size, 800, tr)
    x_pb = left + w_the + sp
    e.append(hl(x_pb, x_pb + w_pb, base[1], size))
    e.append(head(left, base[1], "the", size, c["ink"]))
    e.append(head(x_pb, base[1], "playbooks", size, INK))
    e.append(head(x_pb + w_pb + sp, base[1], "of", size, c["ink"]))
    e.append(head(left, base[2], "a working studio.", size, c["ink"]))
    e.append(T(66, 392, "Reviewed professional skills for AI agents, over one MCP address.", "body", 20.5, c["ink2"], 450))
    e.append(T(66, 420, "Connect once. Read only the sections the task needs.", "body", 20.5, c["ink2"], 450))
    # address pill and stat chips
    addr = "https://" + SITE + "/mcp"
    aw = TYPE.width(addr, "mono", 17, 500) + 64
    py = 450
    e += [rect(64, py, aw, 46, 23, c["white"], c["line"], 1.5), circle(88, py + 23, 6.5, LIME, INK, 1.4),
          T(106, py + 29, addr, "mono", 17, c["ink"], 500)]
    x = 64 + aw + 12
    for text, fill, tc in [("286 skills", LIME, INK), ("20 areas", c["white"], c["ink"])]:
        w = TYPE.width(text, "display", 18, 700, -0.02) + 36
        e += [rect(x, py, w, 46, 23, fill, INK if fill == LIME else c["line"], 1.4 if fill == LIME else 1.5),
              head(x + w / 2, py + 29, text, 18, tc, 700, "middle")]
        x += w + 10
    # right: the receptionist panel
    e += bezel(840, 24, 416, 492, 38, LILAC, c["frame"])
    e += [label(874, 80, "THE RECEPTIONIST", 14, "#3F3A55")]
    for i, line in enumerate(["Ask in plain words.", "Get two cards, not", "the whole shelf."]):
        e.append(head(874, 128 + i * 34, line, 31, INK, 800))
    e += [index_card(958, 296, -5, ["headless-blender-", "batch-render"], "3D & BLENDER", LIME),
          index_card(1140, 344, 4.5, ["audio-mixing-", "mastering"], "AUDIO & MUSIC", APRICOT),
          index_card(990, 450, -2, ["film-dubbing-", "pipeline"], "FILM & VIDEO", SKY)]
    pw = TYPE.width("SECTIONS READ 2 OF 14", "mono", 13.5, 500, 0.05) + 36
    e += [f'<g transform="translate(1148 484) rotate(-5)">' + rect(-pw / 2, -17, pw, 34, 17, LIME, INK, 1.8)
          + label(0, 5, "SECTIONS READ 2 OF 14", 13.5, INK, "middle") + "</g>"]
    return svg(W, H, "SynthSkills: the playbooks of a working studio, for AI agents",
               "Banner in the SynthSkills studio-lab brand. Headline: Give your agents the playbooks of a working studio. "
               f"286 skills in 20 areas, one MCP address, https://{SITE}/mcp. Skill cards for headless-blender-batch-render, "
               "audio-mixing-mastering and film-dubbing-pipeline; sections read 2 of 14.", [x for x in e if x])


# ---------------------------------------------------------------- buttons
BUTTONS = [
    ("website", "Open the website", True),
    ("connect", "Connect your agent", False),
    ("library", "Browse the library", False),
]


def button(theme, text, primary):
    c = THEMES[theme]
    size = 18
    tw = TYPE.width(text, "body", size, 650)
    W, H = int(tw + 22 + 8 + 44 + 18), 52
    if primary:
        fill, tc, ring, ic, edge = (INK, "#FFFFFF", LIME, INK, None) if theme == "light" else (LIME, INK, INK, LIME, None)
    else:
        fill, tc = ("#FFFFFF", INK) if theme == "light" else (c["bg"], c["ink"])
        ring, ic = (INK, "#FFFFFF") if theme == "light" else (LIME, INK)
        edge = "#7A766B" if theme == "light" else "#5B5850"
    cx, cy = W - 26, H / 2
    e = [rect(0.75, 0.75, W - 1.5, H - 1.5, (H - 1.5) / 2, fill, edge, 1.5 if edge else 1),
         T(26, 32.5, text, "body", size, tc, 650), circle(cx, cy, 19, ring),
         f'<path d="M{cx - 6:g} {cy:g}H{cx + 6:g}" stroke="{ic}" stroke-width="2.2" stroke-linecap="round"/>',
         arrow(cx + 6, cy, "right", ic, 5.5)]
    return svg(W, H, text, text, e)


# ---------------------------------------------------------------- how it works
def diagram(theme):
    c = THEMES[theme]
    W, H = 1280, 640
    e = [canvas(c, W, H),
         circle(60, 62, 5.5, c["ink"]), label(77, 67.5, "HOW IT WORKS", 15, c["ink2"])]
    t1, t2, t3 = "One task. A", "few sections", ". A clear record."
    S, sp = 42, 42 * 0.27
    w1 = TYPE.width(t1, "display", S, 800, -0.035)
    w2 = TYPE.width(t2, "display", S, 800, -0.035)
    x2 = 54 + w1 + sp
    e.append(hl(x2, x2 + w2, 118, S))
    e.append(head(54, 118, t1, S, c["ink"]))
    e.append(head(x2, 118, t2, S, INK))
    e.append(head(x2 + w2 + sp * 0.5, 118, t3, S, c["ink"]))
    cw, ch, gap = 376, 132, 36
    xs = [40, 40 + cw + gap, 40 + 2 * (cw + gap)]
    y1, y2 = 156, 156 + ch + gap
    cards = [(xs[0], y1, "01", "Connect", "Streamable HTTP · no header", SKY, False),
             (xs[1], y1, "02", "join_library", "Free key · save it privately", LIME, True),
             (xs[2], y1, "03", "accept_charter", "Accept the rules · get a pass", LILAC, True),
             (xs[2], y2, "04", "ask_receptionist", "intake once, then ask in plain words", APRICOT, True),
             (xs[1], y2, "05", "read_skill", "Read only the needed sections", LIME, True),
             (xs[0], y2, "06", "log_skill_use", "Record each skill you used", SKY, True)]
    for x, y, n, name, cap, tint, mono in cards:
        e += bezel(x, y, cw, ch, 30, tint, c["frame"], 5)
        e += [circle(x + 44, y + 42, 16, "#FFFFFF", INK, 1.5), label(x + 44, y + 47, n, 14, INK, "middle")]
        if mono:
            e.append(T(x + 76, y + 50, name, "mono", 24, INK, 500))
        else:
            e.append(head(x + 76, y + 51, name, 28, INK, 800))
        e.append(T(x + 30, y + 100, cap, "body", 18.5, INK, 500))
    ay, ay2 = y1 + ch / 2, y2 + ch / 2
    for x in (xs[0] + cw, xs[1] + cw):  # row 1, left to right
        e += [f'<path d="M{x + 6:g} {ay:g}H{x + gap - 8:g}" stroke="{c["ink"]}" stroke-width="2.2" stroke-linecap="round"/>',
              arrow(x + gap - 5, ay, "right", c["ink"])]
    cx = xs[2] + cw / 2  # down from 03 to 04
    e += [f'<path d="M{cx:g} {y1 + ch + 6:g}V{y2 - 9:g}" stroke="{c["ink"]}" stroke-width="2.2" stroke-linecap="round"/>',
          arrow(cx, y2 - 5, "down", c["ink"])]
    for x in (xs[2], xs[1]):  # row 2, right to left
        e += [f'<path d="M{x - 6:g} {ay2:g}H{x - gap + 8:g}" stroke="{c["ink"]}" stroke-width="2.2" stroke-linecap="round"/>',
              arrow(x - gap + 5, ay2, "left", c["ink"])]
    # when nothing fits
    by = 484
    lw = TYPE.width("WHEN NOTHING FITS", "mono", 14, 500, 0.05)
    e += [circle(54, by - 5, 5.5, c["ink"]), label(70, by, "WHEN NOTHING FITS", 14, c["ink2"]),
          f'<path d="M{70 + lw + 18:g} {by - 5:g}H{W - 40:g}" stroke="{c["line"]}" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round"/>']
    bw = [444, 240, 444]
    bx = [40, 40 + bw[0] + gap, 40 + bw[0] + bw[1] + 2 * gap]
    items = [("report_feedback", 'kind="missing"', True), ("ticket", "Keep the receipt", False),
             ("my_requests", "After 48 hours · works without a key", True)]
    for x, w, (name, cap, mono) in zip(bx, bw, items):
        e += [rect(x, by + 22, w, 90, 26, c["paper"], c["line"], 1.5),
              T(x + 28, by + 62, name, "mono", 23, c["ink"], 500),
              T(x + 28, by + 94, cap, "mono" if cap.startswith("kind") else "body", 18, c["ink2"], 500 if cap.startswith("kind") else 450)]
    for x in (bx[0] + bw[0], bx[1] + bw[1]):
        e += [f'<path d="M{x + 6:g} {by + 67:g}H{x + gap - 8:g}" stroke="{c["ink"]}" stroke-width="2.2" stroke-linecap="round"/>',
              arrow(x + gap - 5, by + 67, "right", c["ink"])]
    return svg(W, H, "How SynthSkills works",
               'Connect, then join_library (free reader key), accept_charter (pass), ask_receptionist (call intake once first), '
               'read_skill (only the needed sections) and log_skill_use. When nothing fits: report_feedback(kind="missing") '
               "returns a ticket; my_requests follows it up after 48 hours. Requests are not promised.", e)


# ---------------------------------------------------------------- feature tiles
ICONS = {
    "reviewed": '<path d="M26 22H46L53 29V54H26Z"/><path d="M46 22V29H53M32 34H43M32 40H39M32 46H36"/><circle cx="49" cy="48" r="10"/><path d="M44 48L48 52L54 45"/>',
    "sections": '<path d="M24 24H38Q40 24 40 28V55Q40 51 36 51H24ZM56 24H42Q40 24 40 28V55Q40 51 44 51H56Z"/><path d="M29 31H34M29 37H34M46 31H51M46 43H51"/><path d="M46 37H51" stroke-width="3.5"/>',
    "clients": '<rect x="22" y="23" width="36" height="26" rx="5"/><path d="M32 59H48M40 49V59M29 31L34 36L29 41M39 41H47"/>',
    "free-key": '<circle cx="32" cy="35" r="11"/><circle cx="32" cy="35" r="3"/><path d="M40 43L55 58M48 51L53 46M52 55L57 50"/>',
    "missing": '<path d="M24 23H56V48H39L29 57V48H24Z"/><path d="M32 32H48M32 39H41"/><path d="M52 52V64M46 58H58"/>',
    "charter": '<path d="M40 20L57 27V39C57 50 50 57 40 62C30 57 23 50 23 39V27Z"/><path d="M32 40L38 46L49 34"/>',
}
TILES = [
    ("reviewed", "01", ["Reviewed", "& scored"], "Full-text AI reviews with public scores for quality, depth and practical use.", LIME),
    ("sections", "02", ["Read only", "what you need"], "A short reading plan, then section reads inside a published character budget.", LILAC),
    ("clients", "03", ["Works with", "your agent"], "Claude Code, Codex, Cursor or any MCP client, over Streamable HTTP.", SKY),
    ("free-key", "04", ["A free key", "in one call"], "join_library issues a free reader key. No email is needed during the public beta.", APRICOT),
    ("missing", "05", ["Ask for", "missing skills"], "File a request when nothing fits and follow its ticket. Publication is not promised.", "paper"),
    ("charter", "06", ["Charter-", "protected"], "Guidance for the task your user gave you. Reads are traceable; no copying or training.", "ink"),
]


def features(theme):
    c = THEMES[theme]
    W, tw, th, g = 1280, 416, 240, 16
    H = 2 * th + g
    e = []
    for i, (icon, num, title, desc, tint) in enumerate(TILES):
        x, y = (i % 3) * (tw + g), (i // 3) * (th + g)
        if tint == "paper":
            fill, fg, fg2, circ, ic = c["paper"], c["ink"], c["ink2"], c["white"], c["ink"]
        elif tint == "ink":  # the black tile: lime on black in light mode, paper on dark in dark mode
            fill, fg, fg2, circ, ic = ((INK, "#FFFFFF", "#C9C5B8", LIME, INK) if theme == "light"
                                       else ("#F4F1E8", INK, "#55524A", INK, "#F4F1E8"))
        else:
            fill, fg, fg2, circ, ic = tint, INK, "#2F2D28", "#FFFFFF", INK
        ring = c["frame"] if tint == "paper" else None
        e.append(rect(x, y, tw, th, 36, c["line"] if tint == "paper" else INK, extra=' fill-opacity="0.12"') if False else "")
        e.append(rect(x, y, tw, th, 36, c["frame"] if theme == "light" else c["frame"]))
        e.append(rect(x + 5, y + 5, tw - 10, th - 10, 31, fill))
        e.append(label(x + 34, y + 53, f"{num}", 14, fg2))
        e.append(circle(x + tw - 64, y + 62, 32, circ, None if tint != "paper" else c["line"], 1.5))
        e.append(f'<g transform="translate({x + tw - 64 - 32:g} {y + 62 - 32:g}) scale(.8)" fill="none" stroke="{ic}" '
                 f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>')
        for j, line in enumerate(title):
            e.append(head(x + 34, y + 112 + j * 34, line, 33, fg if tint != "ink" or theme == "dark" else LIME))
        for j, line in enumerate(TYPE.wrap(desc, "body", 17.5, 450, tw - 68)):
            e.append(T(x + 34, y + 180 + j * 24.5, line, "body", 17.5, fg2, 450))
    names = "; ".join(f"{' '.join(t[2])}: {t[3]}" for t in TILES)
    return svg(W, H, "Built for the task in front of your agent", "Six feature tiles. " + names, [x for x in e if x])


def write(path, text):
    path.write_text(text, encoding="utf-8")


def main():
    ASSETS.mkdir(exist_ok=True)
    for old in (ASSETS / "features").glob("*.svg") if (ASSETS / "features").exists() else []:
        old.unlink()
    if (ASSETS / "features").exists():
        (ASSETS / "features").rmdir()
    (ASSETS / "buttons").mkdir(exist_ok=True)
    n = 0
    for theme in THEMES:
        write(ASSETS / f"banner-{theme}.svg", banner(theme))
        write(ASSETS / f"how-it-works-{theme}.svg", diagram(theme))
        write(ASSETS / f"features-{theme}.svg", features(theme))
        for key, text, primary in BUTTONS:
            write(ASSETS / "buttons" / f"{key}-{theme}.svg", button(theme, text, primary))
        n += 3 + len(BUTTONS)
    print(f"Built {n} self-contained SVG assets (text outlined, no web fonts).")


if __name__ == "__main__":
    main()
