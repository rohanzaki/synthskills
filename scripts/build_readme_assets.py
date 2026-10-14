#!/usr/bin/env python3
"""Rebuild the README's self-contained SVG artwork (standard library only)."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace"
THEMES = {
    "light": dict(bg="#FAF9F6", ink="#182B2A", muted="#596C68", accent="#087F72",
                  wash="#E6F0EB", card="#FFFFFF", line="#D5E2DC", faint="#EDF0EA"),
    "dark": dict(bg="#101B1B", ink="#F2F5EF", muted="#A6B8B2", accent="#67D4BC",
                 wash="#1B3833", card="#172727", line="#304B45", faint="#182A27"),
}


def txt(x, y, text, size, color, weight=400, mono=False, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{escape(MONO if mono else SANS, quote=True)}" '
            f'font-size="{size}" font-weight="{weight}" {extra}>{escape(text)}</text>')


def rect(x, y, w, h, r, fill, stroke=None):
    edge = f' stroke="{stroke}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{edge}/>'


def svg(width, height, title, desc, elements):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title>\n<desc id="desc">{escape(desc)}</desc>\n'
            + "\n".join(elements) + "\n</svg>\n")


def banner(theme):
    c = THEMES[theme]
    e = [rect(0, 0, 1280, 400, 24, c["bg"]),
         f'<path d="M684 36V364" stroke="{c["line"]}"/>',
         rect(56, 39, 30, 30, 9, c["accent"]),
         '<path d="M63 60L68 48L74 60L79 48" fill="none" stroke="' + c["bg"] + '" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
         txt(100, 59, "A PUBLIC SKILL LIBRARY", 13, c["muted"], 600, extra='letter-spacing="2.5"'),
         txt(52, 151, "SynthSkills", 78, c["ink"], 650, extra='letter-spacing="-4"'),
         txt(56, 197, "Reviewed professional skills", 27, c["muted"]),
         txt(56, 233, "for AI agents", 27, c["muted"]),
         rect(56, 273, 563, 46, 23, c["wash"]),
         f'<circle cx="78" cy="296" r="4" fill="{c["accent"]}"/>',
         txt(94, 302, "https://synthskills.synthminds.pk/mcp", 19, c["accent"], 500, mono=True),
         txt(56, 365, "247 skills", 15, c["ink"], 600),
         txt(148, 365, "/", 15, c["muted"]),
         txt(168, 365, "20 areas", 15, c["muted"]),
         txt(254, 365, "/", 15, c["muted"]),
         txt(274, 365, "Public beta", 15, c["muted"])]
    # A continuous, quiet trail: the skill library is connected, not a prompt dump.
    trail = "M764 99C842 99 857 80 934 80S1136 82 1136 150S1000 224 957 206S784 191 784 259S839 341 947 322S1178 364 1178 280S1124 271 1100 262"
    e += [f'<path d="{trail}" fill="none" stroke="{c["faint"]}" stroke-width="13" stroke-linecap="round"/>',
          f'<path d="{trail}" fill="none" stroke="{c["line"]}" stroke-width="1.8" stroke-linecap="round"/>',
          f'<path d="M1136 150C1136 204 1000 224 957 206" fill="none" stroke="{c["accent"]}" stroke-width="1.8" stroke-linecap="round"/>']
    chips = [(718, 80, 116, "ffmpeg"), (917, 61, 139, "Blender"),
             (1075, 131, 110, "glTF"), (900, 187, 112, "ACES"),
             (727, 240, 118, "restic"), (875, 303, 120, "EPUB"),
             (1118, 326, 110, "GDAL"), (1030, 243, 159, "LLM evals")]
    for x, y, w, label in chips:
        e.append(rect(x-3, y-3, w+6, 44, 15, c["faint"]))
        e.append(rect(x, y, w, 38, 12, c["card"], c["line"]))
        e.append(txt(x+w/2, y+25, label, 17, c["ink"], 500, mono=True, extra='text-anchor="middle"'))
    for x, y in [(873, 85), (1136, 199), (857, 328), (1178, 308)]:
        e.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="1.5"/>')
    return svg(1280, 400, "SynthSkills — reviewed professional skills for AI agents",
               "247 public skills in 20 areas. Connect at https://synthskills.synthminds.pk/mcp. A connected trail links ffmpeg, Blender, glTF, ACES, restic, EPUB, GDAL and LLM evals.", e)


def diagram(theme):
    c = THEMES[theme]
    e = [rect(0, 0, 1280, 656, 24, c["bg"]),
         txt(52, 56, "One task. A few sections. A clear record.", 28, c["ink"], 600),
         txt(52, 83, "Connect once, then follow the numbered trail.", 17, c["muted"]),
         '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto-start-reverse">'
         f'<path d="M1 1L6 4L1 7" fill="none" stroke="{c["accent"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
         '</marker></defs>']
    cards = [(52, 115, "01", "Connect", "Streamable HTTP · no header"),
             (462, 115, "02", "join_library", "Free key · save it privately"),
             (872, 115, "03", "accept_charter", "Accept the rules · get a pass"),
             (872, 301, "04", "ask_receptionist", "Describe the task · get a plan"),
             (462, 301, "05", "read_skill", "Read only the needed sections"),
             (52, 301, "06", "log_skill_use", "Record each skill you used")]
    for x, y, n, label, caption in cards:
        e.extend([rect(x-4, y-4, 364, 132, 21, c["faint"]),
                  rect(x, y, 356, 124, 17, c["card"], c["line"]),
                  txt(x+22, y+30, n, 15, c["accent"], 600, mono=True),
                  txt(x+22, y+66, label, 25, c["ink"], 600, mono=label != "Connect"),
                  txt(x+22, y+99, caption, 18, c["muted"])])
    paths = ["M420 177H448", "M830 177H858", "M1050 253V287", "M860 363H832", "M450 363H422"]
    for p in paths:
        e.append(f'<path d="{p}" fill="none" stroke="{c["accent"]}" stroke-width="1.7" marker-end="url(#arrow)"/>')
    e += [txt(52, 468, "WHEN NOTHING FITS", 13, c["accent"], 600, extra='letter-spacing="2"'),
          f'<path d="M1050 438V485H267V514" fill="none" stroke="{c["line"]}" stroke-width="1.7" stroke-dasharray="5 5" marker-end="url(#arrow)"/>']
    branch = [(52, 530, 440, "report_feedback", 'kind="missing"'),
              (548, 530, 190, "ticket", "Keep the receipt"),
              (794, 530, 434, "my_requests", "Follow up after 48 hours · keyless")]
    for x, y, w, label, caption in branch:
        e.extend([rect(x, y, w, 90, 16, c["wash"]),
                  txt(x+22, y+34, label, 23, c["ink"], 500, mono=True),
                  txt(x+22, y+64, caption, 18, c["muted"], mono=caption.startswith("kind="))])
    for p in ["M504 575H534", "M750 575H780"]:
        e.append(f'<path d="{p}" fill="none" stroke="{c["accent"]}" stroke-width="1.7" marker-end="url(#arrow)"/>')
    return svg(1280, 656, "How SynthSkills works",
               'Connect → join_library (free reader key) → accept_charter (pass) → ask_receptionist → read_skill (sections) → log_skill_use. When nothing fits: report_feedback(kind="missing") → ticket → my_requests after 48 hours. Requests are not promised.', e)


ICONS = {
    "reviewed": ("Reviewed and scored", '<path d="M26 22H46L53 29V54H26Z"/><path d="M46 22V29H53M32 34H43M32 40H39M32 46H36"/><circle cx="49" cy="48" r="10"/><path d="M44 48L48 52L54 45"/>'),
    "sections": ("Read only what you need", '<path d="M24 24H38Q40 24 40 28V55Q40 51 36 51H24ZM56 24H42Q40 24 40 28V55Q40 51 44 51H56Z"/><path d="M29 31H34M29 37H34M46 31H51M46 43H51"/><path d="M46 37H51" stroke-width="3.5"/>'),
    "clients": ("Works with Claude Code, Codex and Cursor", '<rect x="22" y="23" width="36" height="26" rx="5"/><path d="M32 59H48M40 49V59M29 31L34 36L29 41M39 41H47"/>'),
    "free-key": ("Free key in one call", '<circle cx="32" cy="35" r="11"/><circle cx="32" cy="35" r="3"/><path d="M40 43L55 58M48 51L53 46M52 55L57 50"/>'),
    "missing": ("Ask for missing skills", '<path d="M24 23H56V48H39L29 57V48H24Z"/><path d="M32 32H48M32 39H41"/><path d="M52 52V64M46 58H58"/>'),
    "charter": ("Charter-protected", '<path d="M40 20L57 27V39C57 50 50 57 40 62C30 57 23 50 23 39V27Z"/><path d="M32 40L38 46L49 34"/>'),
}


def main():
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "features").mkdir(exist_ok=True)
    for theme in THEMES:
        (ASSETS / f"banner-{theme}.svg").write_text(banner(theme), encoding="utf-8")
        (ASSETS / f"how-it-works-{theme}.svg").write_text(diagram(theme), encoding="utf-8")
    for name, (title, paths) in ICONS.items():
        elements = [rect(0, 0, 80, 80, 20, THEMES["light"]["wash"]),
                    '<g fill="none" stroke="#087F72" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + paths + '</g>']
        (ASSETS / "features" / f"{name}.svg").write_text(svg(80, 80, title, title, elements), encoding="utf-8")
    print("Built 10 self-contained SVG assets.")


if __name__ == "__main__":
    main()
