#!/usr/bin/env python3
"""Validate README artwork, local links and catalog facts offline. Requires pandoc."""
import collections
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import subprocess
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SVG = "{http://www.w3.org/2000/svg}"


class Document(HTMLParser):
    def __init__(self, source=False):
        super().__init__()
        self.source = source
        self.references = []
        self.ids = set()
        self.tags = collections.Counter()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags[tag] += 1
        assert tag not in {"script", "style", "iframe"}, f"Unsupported README tag: {tag}"
        if self.source:
            assert "style" not in attrs, "Inline README CSS is not allowed"
        assert not any(k.startswith("on") for k in attrs), "README event handler"
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ["href", "src", "srcset"]:
            if attrs.get(key):
                self.references.append(attrs[key])
        if tag == "img":
            assert "alt" in attrs, "Image has no alt attribute"


def rendered(path):
    # Pandoc adds alignment styles to generated table cells; the source must stay CSS-free.
    Document(source=True).feed(path.read_text())
    result = subprocess.run(["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none", str(path)],
                            capture_output=True, text=True, check=True)
    document = Document()
    document.feed(result.stdout)
    return document


def main():
    assets = list((ROOT / "assets").rglob("*.svg"))
    assert len(assets) == 10, "Expected two banners, two diagrams and six icons"
    for path in assets:
        tree = ET.parse(path).getroot()
        assert tree.tag == SVG + "svg"
        assert tree.find(SVG + "title") is not None
        assert tree.find(SVG + "desc") is not None
        for element in tree.iter():
            assert element.tag not in {SVG + "script", SVG + "foreignObject", SVG + "image"}
            assert not any(k.startswith("on") for k in element.attrib)
            for key, value in element.attrib.items():
                if key.endswith("href"):
                    assert value.startswith("#"), "External SVG dependency"
        if path.name.startswith("banner-"):
            assert tree.get("viewBox") == "0 0 1280 400"
            assert tree.findall(SVG + "text"), "Keep SVG text editable"
        if path.parent.name == "features":
            assert 64 <= int(tree.get("width")) <= 96
    print("PASS: all 10 SVGs parse; self-contained artwork and editable banner text.")

    documents = {name: rendered(ROOT / name) for name in ["README.md", "CATALOG.md"]}
    references = 0
    for name, document in documents.items():
        for reference in document.references:
            link = urlsplit(reference)
            if link.scheme:
                assert link.scheme in {"https", "mailto"}, f"Unsupported link scheme: {reference}"
                continue
            target = ROOT / unquote(link.path) if link.path else ROOT / name
            assert target.resolve().is_relative_to(ROOT), f"Link leaves repo: {reference}"
            assert target.exists(), f"Missing local link: {reference}"
            if link.fragment:
                if target.name in documents:
                    other = documents[target.name]
                else:
                    assert target.suffix == ".md", f"Cannot resolve fragment: {reference}"
                    other = rendered(target)
                assert unquote(link.fragment) in other.ids, f"Missing heading: {reference}"
            references += 1
    assert documents["README.md"].tags["picture"] == 2
    assert documents["README.md"].tags["details"] == 9
    print(f"PASS: both Markdown files render as GFM; {references} local asset, file and heading links resolve.")

    data = json.loads((ROOT / "data" / "skills.json").read_text())
    skills = data["skills"]
    axes = ["quality", "depth", "practical"]
    rated = [s for s in skills if all(s[a] is not None for a in axes)]
    counts = collections.Counter(s["area"] for s in skills)
    assert (len(skills), len(counts), len(rated)) == (247, 20, 202)
    readme = (ROOT / "README.md").read_text()
    showcase = readme.split("## Top-rated skills\n", 1)[1].split("## Library at a glance", 1)[0]
    names = re.findall(r"\| `skill://([^`]+)`", showcase)
    top = sorted(rated, key=lambda s: (-sum(s[a] for a in axes), s["name"]))[:10]
    assert names == [s["name"] for s in top], "Showcase order differs from data"
    for skill, row in zip(top, re.findall(r"^\| `skill://.*", showcase, re.M)):
        columns = row.split("|")
        assert columns[2].strip() == skill["area"]
        assert [int(columns[i].strip().split()[0]) for i in [3, 4, 5]] == [skill[a] for a in axes]
        actual = float(columns[6].strip().strip("*").split()[0])
        assert actual == round(sum(skill[a] for a in axes) / 3, 1)
    glance = readme.split("## Library at a glance\n", 1)[1].split("## Screenshots", 1)[0]
    found = {area.strip(): int(number) for area, number in re.findall(r"\| ([^|]+) \| \*\*(\d+)\*\*", glance)}
    assert found == dict(counts), "Area counts differ from data"
    catalog = (ROOT / "CATALOG.md").read_text()
    assert len(re.findall(r"^\| `skill://", catalog, re.M)) == len(skills)
    print("PASS: top-ten scores, tie order, all 20 area counts and 247 catalog rows match JSON.")

    for name in ["skills", "connect", "home"]:
        path = ROOT / "assets" / "screens" / f"{name}.png"
        raw = path.read_bytes()
        assert raw[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", raw[16:24])
        assert (width, height) == (1200, 810)
        assert len(raw) < 400_000
    print("PASS: all three screenshots are 1200 × 810 PNGs below 400 KB.")
    print("Front-door validation passed.")


if __name__ == "__main__":
    main()
