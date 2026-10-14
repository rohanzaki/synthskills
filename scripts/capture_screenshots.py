#!/usr/bin/env python3
"""Capture the public site in light mode with headless Chrome. Requires Pillow."""
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "screens"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="synthskills-screens-") as temp:
        for name, route in [("skills", "/skills"), ("connect", "/connect"), ("home", "/")]:
            raw = Path(temp) / f"{name}.png"
            subprocess.run([
                "/usr/bin/google-chrome", "--headless=new", "--no-sandbox",
                "--disable-dev-shm-usage", "--hide-scrollbars", "--window-size=1440,900",
                "--force-color-profile=srgb", "--blink-settings=preferredColorScheme=1",
                "--virtual-time-budget=3000", f"--user-data-dir={temp}/profile-{name}",
                f"--screenshot={raw}", f"https://synthskills.synthminds.pk{route}",
            ], capture_output=True, check=True, timeout=45)
            with Image.open(raw) as image:
                # Keep the real page intact; trim unused margins before lossless optimization.
                image = image.convert("RGB")
                assert image.size == (1440, 900), "Unexpected viewport"
                assert min(image.getpixel((10, 10))) > 220, "Expected light theme"
                image = image.crop((120, 0, 1320, 810))
                image.save(OUT / f"{name}.png", optimize=True, compress_level=9)
            size = (OUT / f"{name}.png").stat().st_size
            assert size < 400_000, "Screenshot exceeds the README size budget"
            print(f"{name}.png: light theme, captured at 1440 × 900, cropped to 1200 × 810, {size:,} bytes")


if __name__ == "__main__":
    main()
