#!/usr/bin/env python3
"""Validate the front door offline: artwork, links, catalog facts, screenshots and a private-data scan.

Needs pandoc (renders README.md and CATALOG.md as GFM) and git (the scan reads tracked files only).
"""
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
PUBLIC_HOST = "skills.synthlabs.pk"
VIDEO = "https://youtu.be/2MHmv9d-2YU"


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


def check_artwork():
    assets = sorted((ROOT / "assets").rglob("*.svg"))
    assert len(assets) == 14, "Expected banners, diagrams, feature tiles and area chips (light and dark) plus six buttons"
    for path in assets:
        tree = ET.parse(path).getroot()
        assert tree.tag == SVG + "svg"
        assert tree.find(SVG + "title") is not None and tree.find(SVG + "desc") is not None
        assert not tree.findall(".//" + SVG + "text"), f"{path.name}: text must be outlined (GitHub has no web fonts)"
        for element in tree.iter():
            assert element.tag not in {SVG + "script", SVG + "foreignObject", SVG + "image", SVG + "style"}
            assert "font-family" not in element.attrib, "SVG depends on a font"
            assert not any(k.startswith("on") for k in element.attrib)
            for key, value in element.attrib.items():
                if key.endswith("href"):
                    assert value.startswith("#"), "External SVG dependency"
        if path.name.startswith("banner-"):
            assert tree.get("viewBox") == "0 0 1280 540"
        assert path.stat().st_size < 400_000, f"{path.name} is heavy"
    print("PASS: all 14 SVGs parse; self-contained, text outlined, no fonts or external references.")

    thumb = ROOT / "assets" / "explainer-thumb.jpg"
    raw = thumb.read_bytes()
    assert raw[:2] == b"\xff\xd8"
    index = 2
    while index < len(raw):  # find the SOF marker for the size
        marker, length = raw[index + 1], struct.unpack(">H", raw[index + 2:index + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", raw[index + 5:index + 9])
            break
        index += 2 + length
    assert (width, height) == (1280, 720) and len(raw) < 250_000
    print("PASS: explainer-thumb.jpg is a 1280 x 720 JPEG under 250 KB.")


def check_markdown():
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
                other = documents[target.name] if target.name in documents else rendered(target)
                assert unquote(link.fragment) in other.ids, f"Missing heading: {reference}"
            references += 1
    readme = documents["README.md"]
    assert readme.tags["picture"] == 7, "Expected banner, three buttons, area chips, feature tiles and diagram"
    assert readme.tags["details"] == 6, "Expected five client tabs and the prompts list"
    source = (ROOT / "README.md").read_text()
    assert VIDEO in source and "AI voice (OmniVoice)" in source, "Explainer link and AI-voice label must stay"
    assert "https://" + PUBLIC_HOST + "/mcp" in source
    print(f"PASS: both Markdown files render as GFM; {references} local asset, file and heading links resolve.")
    return source


def check_catalog(readme):
    data = json.loads((ROOT / "data" / "skills.json").read_text())
    skills = data["skills"]
    axes = ["quality", "depth", "practical"]
    rated = [s for s in skills if all(s[a] is not None for a in axes)]
    counts = collections.Counter(s["area"] for s in skills)
    n, areas, r = len(skills), len(counts), len(rated)
    for phrase in [f"{n} skills in {areas} areas", f"**{n} public skills · {areas} areas · {r} rated · {n - r} not yet rated**",
                   f"skills-{n}-D7FF3A", f"**{n - r} newly added skills are not yet rated.**"]:
        assert phrase in readme, f"README does not say: {phrase}"
    showcase = readme.split("## Top-rated skills\n", 1)[1].split("## Library at a glance", 1)[0]
    names = re.findall(r"\| `skill://([^`]+)`", showcase)
    top = sorted(rated, key=lambda s: (-sum(s[a] for a in axes), s["name"]))[:10]
    assert names == [s["name"] for s in top], "Showcase order differs from data"
    for skill, row in zip(top, re.findall(r"^\| `skill://.*", showcase, re.M)):
        columns = row.split("|")
        assert columns[2].strip() == skill["area"]
        assert [int(columns[i].strip().split()[0]) for i in [3, 4, 5]] == [skill[a] for a in axes]
        assert float(columns[6].strip().strip("*").split()[0]) == round(sum(skill[a] for a in axes) / 3, 1)
    glance = readme.split("## Library at a glance\n", 1)[1].split("[Full catalog", 1)[0]
    found = {area.strip(): int(number) for area, number in re.findall(r"\| ([^|]+) \| \*\*(\d+)\*\*", glance)}
    assert found == dict(counts), "Area counts differ from data"
    catalog = (ROOT / "CATALOG.md").read_text()
    assert len(re.findall(r"^\| `skill://", catalog, re.M)) == n
    print(f"PASS: top-ten scores, tie order, all {areas} area counts and {n} catalog rows match the JSON.")


def check_screens():
    for name in ["home", "work", "skills", "connect"]:
        raw = (ROOT / "assets" / "screens" / f"{name}.png").read_bytes()
        assert raw[:8] == b"\x89PNG\r\n\x1a\n"
        assert struct.unpack(">II", raw[16:24]) == (1440, 900)
        assert len(raw) < 400_000
    print("PASS: all four screenshots are 1440 x 900 PNGs below 400 KB.")


# --- private-data scan over tracked text files ------------------------------------------------
# Patterns are assembled from pieces so this file does not trip its own scan.
HOSTS = ["synth" + "dev", "cp" + "u2", "demp" + "-radio", ".ts" + ".net", "synthskills" + ".synthminds", "local" + "host",
         "127.0." + "0.1"]
SECRETS = [r"\bss[kp]_[A-Za-z0-9]{8,}", r"\bsk-[A-Za-z0-9_-]{16,}", r"\bghp_[A-Za-z0-9]{20,}", r"\bpdl_[A-Za-z0-9]{10,}",
           r"\bre_[A-Za-z0-9]{16,}", r"-----BEGIN [A-Z ]*PRIVATE KEY", r"\bAKIA[0-9A-Z]{16}", r"\bxox[abp]-"]
ALLOWED_EMAIL = "contact@rohanzakie.com"


def tracked_text():
    names = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    for name in filter(None, names):
        path = ROOT / name
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".woff2", ".gif", ".ico"} or not path.is_file():
            continue
        yield name, path.read_text(encoding="utf-8", errors="replace")


def check_private_data():
    findings, files = [], 0
    for name, text in tracked_text():
        files += 1
        for lineno, line in enumerate(text.splitlines(), 1):
            where = f"{name}:{lineno}"
            for host in HOSTS:
                if host in line:
                    findings.append(f"{where}: internal host {host!r}")
            if re.search(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])", line) and not re.search(r"\d+\.\d+\.\d+\.\d+\.\d", line):
                findings.append(f"{where}: IP address")
            if re.search(r"(?<![\w.:/-])/(?:home|media|Users|root)/", line):
                findings.append(f"{where}: local path")
            for pattern in SECRETS:
                if re.search(pattern, line):
                    findings.append(f"{where}: key shape {pattern}")
            for email in re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", line):
                if email != ALLOWED_EMAIL and not email.endswith(("@2x.png", "@3x.png")):
                    findings.append(f"{where}: email {email}")
        if name.endswith(".py") and re.search(r"^\s*(?:from|import)\s+(?:server|flask|fastapi|uvicorn)\b", text, re.M):
            findings.append(f"{name}: looks like server code")
    assert not findings, "Private-data scan failed:\n  " + "\n  ".join(findings)
    print(f"PASS: private-data scan of {files} tracked text files: no internal hosts, IPs, local paths, keys or stray emails.")


def main():
    check_artwork()
    readme = check_markdown()
    check_catalog(readme)
    check_screens()
    check_private_data()
    print("Front-door validation passed.")


if __name__ == "__main__":
    main()
