# /// script
# requires-python = ">=3.11"
# dependencies = ["ansi2html==1.9.2", "playwright==1.58.0"]
# ///
"""Rasterize actual Bubble Tea ANSI frames in a headless terminal-like viewport."""
import sys
from pathlib import Path
from ansi2html import Ansi2HTMLConverter
from playwright.sync_api import sync_playwright

source, output = map(Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    for frame in sorted(source.glob("tui-*.ansi")):
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
