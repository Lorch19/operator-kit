"""Render a report at phone and desktop widths and check for horizontal overflow.

Usage: python3 screenshot.py <report.html> <out_prefix>
Writes <out_prefix>_400.png (light) and <out_prefix>_1200.png (dark), all <details> opened.
Prints scrollWidth per width; it must equal the viewport width. Page errors print as ERR.
"""
import os, sys
from playwright.sync_api import sync_playwright

src, prefix = sys.argv[1], sys.argv[2]
page = os.path.abspath(prefix + "_page.html")
body = open(src, encoding="utf-8").read()
open(page, "w", encoding="utf-8").write(
    '<!doctype html><html><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'
    + body + "</body></html>")

with sync_playwright() as p:
    b = p.chromium.launch()
    for w, scheme in [(400, "light"), (1200, "dark")]:
        pg = b.new_page(viewport={"width": w, "height": 1000}, color_scheme=scheme)
        pg.on("pageerror", lambda e: print("ERR", e))
        pg.goto("file://" + page)
        pg.wait_for_timeout(1500)
        pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
        sw = pg.evaluate("document.documentElement.scrollWidth")
        print(w, scheme, "scrollWidth", sw, "OK" if sw == w else "OVERFLOW")
        pg.screenshot(path=f"{prefix}_{w}.png", full_page=True)
    b.close()
os.remove(page)
