# /// script
# requires-python = ">=3.11"
# dependencies = ["ansi2html==1.9.2", "playwright==1.58.0", "pillow==11.3.0"]
# ///
"""Rasterize captured CLI/TUI output and crop native error details for the deck."""
import sys
from pathlib import Path
from ansi2html import Ansi2HTMLConverter
from playwright.sync_api import sync_playwright
from PIL import Image

source, output = map(Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    for frame in sorted([*source.glob("tui-*.ansi"), *source.glob("cli-*.ansi")]):
        text = Ansi2HTMLConverter(inline=True).convert(frame.read_text(), full=False)
        page.set_content('''<style>
            * { box-sizing: border-box; }
            body { margin: 0; background: #111318; color: #eee; }
            pre { display: inline-block; margin: 0; padding: 20px;
                  font: 16px/22px "DejaVu Sans Mono", "Menlo", monospace;
                  white-space: pre; font-variant-ligatures: none; }
            </style><pre>''' + text + '</pre>')
        page.locator("pre").screenshot(path=str(output / (frame.stem + ".png")))
    browser.close()

# Fixed regions of the pinned 120 × 34 terminal and 1100 × 720 desktop captures.
# Preserve native pixels; the slide links each detail to its complete capture.
for name, expected_size, box in [
    ("tui-error-conflict", (2392, 1576), (40, 1480, 960, 1540)),
    ("gui-error-conflict", (1100, 720), (395, 275, 705, 445)),
]:
    with Image.open(output / (name + ".png")) as capture:
        assert capture.size == expected_size, (name, capture.size)
        capture.crop(box).save(output / (name + "-detail.png"))
