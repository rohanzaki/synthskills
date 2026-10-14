#!/usr/bin/env python3
"""Build data/skills.json and CATALOG.md for the SynthSkills front-door repo.

Standard library only.

  python3 scripts/build_catalog.py export --scores PATH/TO/skill-scores.json
      Reads the scores file (name, area, summary, quality/depth/practical,
      plus the method text), fetches the live public skill list from
      https://synthskills.synthminds.pk/skills, and writes data/skills.json.
      The free-text "reason" field in the scores file is never copied.

  python3 scripts/build_catalog.py catalog
      Reads data/skills.json and writes CATALOG.md (offline).

  python3 scripts/build_catalog.py all --scores PATH
      Both steps.

Skill names are published; skill text never is.
"""
import argparse
import html
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "skills.json"
CATALOG = ROOT / "CATALOG.md"
SITE = "https://synthskills.synthminds.pk"
UNRATED_AREA = "Other"


def fetch_public_rows():
    req = urllib.request.Request(SITE + "/skills", headers={"User-Agent": "synthskills-catalog-builder"})
    with urllib.request.urlopen(req, timeout=30) as r:
        page = r.read().decode("utf-8")
    rows = []
    for cell in re.findall(r'<td class="nm">(.*?)</td>', page, re.S):
        m = re.search(r"<code>([^<]+)</code>", cell)
        if not m:
            continue
        area = re.search(r'class="area">([^<]*)<', cell)
        summ = re.search(r'class="sum">([^<]*)<', cell)
        rows.append({
            "name": html.unescape(m.group(1)).strip(),
            "area": html.unescape(area.group(1)).strip() if area else "",
            "summary": html.unescape(summ.group(1)).strip() if summ else "",
        })
    return rows


def export(scores_path):
    src = json.loads(Path(scores_path).read_text(encoding="utf-8"))
    scored = src["skills"]
    live = fetch_public_rows()
    if len(live) < 50:
        sys.exit("live list looks wrong (%d rows); not writing" % len(live))
    skills = []
    for row in sorted(live, key=lambda r: r["name"]):
        s = scored.get(row["name"])
        if s:
            skills.append({
                "name": row["name"],
                "area": s.get("area") or row["area"] or UNRATED_AREA,
                "summary": s.get("summary") or row["summary"],
                "quality": s.get("quality"),
                "depth": s.get("depth"),
                "practical": s.get("practical"),
            })
        else:
            skills.append({
                "name": row["name"],
                "area": row["area"] or UNRATED_AREA,
                "summary": row["summary"],
                "quality": None, "depth": None, "practical": None,
            })
    out = {
        "generated": date.today().isoformat(),
        "source": SITE + "/skills",
        "method": src.get("method", ""),
        "axes": src.get("axes", {}),
        "skills": skills,
    }
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rated = sum(1 for s in skills if s["quality"] is not None)
    print("wrote %s: %d skills, %d rated, %d not yet rated" % (DATA, len(skills), rated, len(skills) - rated))


def overall(s):
    vals = [s.get(k) for k in ("quality", "depth", "practical")]
    if any(v is None for v in vals):
        return None
    return round(sum(vals) / 3.0, 1)


def cell(v):
    return "not yet rated" if v is None else (("%.1f" % v) if isinstance(v, float) else str(v))


def esc(t):
    return (t or "").replace("|", "\\|").replace("\n", " ").strip()


def catalog():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    skills = d["skills"]
    areas = {}
    for s in skills:
        areas.setdefault(s["area"] or UNRATED_AREA, []).append(s)
    rated = sum(1 for s in skills if s["quality"] is not None)
    L = []
    L.append('<p align="center">\n'
             '  <a href="README.md"><picture>\n'
             '    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">\n'
             '    <img src="assets/banner-light.svg" width="800" alt="SynthSkills — reviewed professional skills for AI agents.">\n'
             '  </picture></a>\n'
             '</p>\n')
    L.append('<p align="center">\n'
             '  <img src="https://img.shields.io/badge/skills-%d-087F72?style=flat-square&amp;labelColor=253D38" alt="%d public skills">\n'
             '  <img src="https://img.shields.io/badge/areas-%d-087F72?style=flat-square&amp;labelColor=253D38" alt="%d areas">\n'
             '  <img src="https://img.shields.io/badge/rated-%d-087F72?style=flat-square&amp;labelColor=253D38" alt="%d rated skills">\n'
             '  <a href="LICENSE"><img src="https://img.shields.io/badge/repo_files-MIT-087F72?style=flat-square&amp;labelColor=253D38" alt="Repository files: MIT licence"></a>\n'
             '</p>\n' % (len(skills), len(skills), len(areas), len(areas), rated, rated))
    L.append('Find the right procedure before your agent starts work. Browse by area below, '
             'compare the reviewer scores, then read only the sections your task needs over MCP.\n')
    L.append('[Connect your agent](README.md#connect-in-30-seconds) · '
             '[Live library](%s/skills) · [Charter and terms](%s/terms)\n' % (SITE, SITE))
    L.append("# SynthSkills catalog\n")
    L.append("%d public skills in %d areas, %d rated so far. Generated %s by "
             "`scripts/build_catalog.py` from `data/skills.json`.\n" % (len(skills), len(areas), rated, d["generated"]))
    L.append("This file lists names, one-line summaries and scores only. The skills themselves are "
             "not in this repository: an agent reads them over MCP at `%s/mcp` under the SynthSkills "
             "charter and [terms](%s/terms). The live list, with sorting and area filters, is at "
             "[%s/skills](%s/skills). Address a skill as `skill://name`.\n" % (SITE, SITE, SITE, SITE))
    L.append("## How scores are made\n")
    L.append(d.get("method", "").strip() + "\n")
    for k, v in d.get("axes", {}).items():
        L.append("- **%s**: %s" % (k.capitalize(), v))
    L.append("- **Overall**: the mean of the three scores, to one decimal.\n")
    L.append("\"not yet rated\" means the skill is published but its review is not finished.\n")
    L.append("## Areas\n")
    for a in sorted(areas):
        anchor = re.sub(r"[^a-z0-9 -]", "", a.lower()).replace(" ", "-")
        L.append("- [%s](#%s): %d" % (a, anchor, len(areas[a])))
    L.append("")
    for a in sorted(areas):
        L.append("## %s\n" % a)
        L.append("| Skill | Summary | Quality | Depth | Practical | Overall |")
        L.append("| --- | --- | --- | --- | --- | --- |")
        items = sorted(areas[a], key=lambda s: (-(overall(s) or -1), s["name"]))
        for s in items:
            L.append("| `skill://%s` | %s | %s | %s | %s | %s |" % (
                s["name"], esc(s["summary"]) or "-", cell(s["quality"]), cell(s["depth"]),
                cell(s["practical"]), cell(overall(s))))
        L.append("")
    CATALOG.write_text("\n".join(L), encoding="utf-8")
    print("wrote %s: %d skills in %d areas" % (CATALOG, len(skills), len(areas)))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", choices=["export", "catalog", "all"])
    p.add_argument("--scores", help="path to skill-scores.json (export, all)")
    a = p.parse_args()
    if a.command in ("export", "all"):
        if not a.scores:
            p.error("--scores is required for export")
        export(a.scores)
    if a.command in ("catalog", "all"):
        catalog()


if __name__ == "__main__":
    main()
