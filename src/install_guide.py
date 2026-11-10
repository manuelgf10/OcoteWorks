"""Guía de instalación imprimible (A4 vertical) en PDF, ES/EN.

Uso: python3 src/install_guide.py ow-02
Usa los mismos textos y figuras que la sección '04 · Instalación' de la ficha (products.py) y
las ilustraciones de src/sheet/<slug>/guide-*.png. Requiere Playwright y FONT_DIR (fuentes @fontsource locales).
"""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import products as PR
from spec_sheet import b64, font

T = {"es": dict(title="Guía de instalación", web="ocoteworks.com · hola@ocoteworks.com"),
     "en": dict(title="Installation guide", web="ocoteworks.com · hola@ocoteworks.com")}


def guide_html(p, lang):
    u, d, gd = PR.UI[lang], p[lang], p[lang]["guide"]
    sdir = os.path.join(ROOT, "src", "sheet", p["code"].lower())
    fig1, fig2 = PR.guide_figs(p, lang, src=lambda name: b64(os.path.join(sdir, f"{name}.png")))
    fonts = (font("barlow-condensed", "BC", 700) + font("ibm-plex-mono", "Plex", 400) + font("ibm-plex-mono", "Plex", 500) +
             font("barlow", "Barlow", 400) + font("barlow", "Barlow", 500))
    logo = b64(os.path.join(ROOT, "assets", "logo-carbon.png"))
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{p['code']} · {T[lang]['title']}</title><style>
{fonts}
@page{{size:210mm 297mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:210mm;height:297mm;background:#fbf7ef;color:#17171a;font:400 3.3mm/1.45 'Barlow',sans-serif;padding:14mm 14mm 12mm;position:relative;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
header{{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:.7mm solid #17171a;padding-bottom:5mm}}
header img{{height:13mm}}
header .t{{text-align:right}}
header .k{{font:500 2.5mm/1 'Plex';letter-spacing:.14em;text-transform:uppercase;color:#5c574f}}
header h1{{font:700 11mm/.9 'BC';text-transform:uppercase;margin-top:2mm}}
header .n{{font:500 3mm/1 'Plex';letter-spacing:.08em;margin-top:2mm}}
.chips{{display:flex;gap:2.5mm;margin-top:5mm;list-style:none}}
.chips li{{border:.45mm solid #17171a;border-radius:1.2mm;padding:1.8mm 3mm;font-size:3.1mm;background:#f4ead7}}
.chips b{{font:400 2.2mm/1 'Plex';letter-spacing:.12em;text-transform:uppercase;color:#5c574f;margin-right:2mm}}
.chips .gd-pre{{border-style:dashed;background:none;font:500 2.4mm/1.3 'Plex';letter-spacing:.1em;text-transform:uppercase}}
.row{{display:grid;grid-template-columns:1.05fr .95fr;gap:7mm;align-items:center;margin-top:12mm}}
.row.b{{grid-template-columns:.85fr 1.15fr}}
.gd-fig{{margin:0}} .gd-fig img{{display:block;width:100%;height:auto}}
.gd-fig figcaption{{margin-top:2mm;font:400 2.2mm/1.3 'Plex';letter-spacing:.12em;text-transform:uppercase;color:#5c574f}}
ol{{list-style:none}}
li.s{{display:grid;grid-template-columns:10mm 1fr;gap:3mm;padding:3mm 0;border-top:.25mm solid #d8cdb8}}
li.s:first-child{{border-top:.6mm solid #17171a}}
.gd-sn{{display:grid;place-items:center;width:9mm;height:9mm;border-radius:1.2mm;background:#edb544;font:700 5mm/1 'BC'}}
li.s h3{{font:700 5.2mm/.95 'BC';text-transform:uppercase}}
li.s p{{margin-top:1mm;color:#3d3a35;font-size:3.1mm}}
.gd-top-in{{position:relative}}
.gd-top-in svg{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
.gd-top-in line{{stroke:#17171a;stroke-width:.35;stroke-dasharray:1.4 1}}
.gd-n{{position:absolute;transform:translate(-50%,-50%);display:grid;place-items:center;width:5.5mm;height:5.5mm;border-radius:50%;background:#17171a;color:#edb544;font:500 2.8mm/1 'Plex'}}
.gd-front{{position:absolute;left:0;top:50%;transform:translateY(-50%);font:400 2.2mm/1 'Plex';letter-spacing:.12em;text-transform:uppercase;color:#5c574f;background:#fbf7ef;padding:.8mm 1.2mm}}
footer{{position:absolute;left:14mm;right:14mm;bottom:12mm;display:flex;justify-content:space-between;gap:8mm;border-top:.25mm solid #d8cdb8;padding-top:3mm;font:400 2.3mm/1.45 'Plex';color:#5c574f}}
footer p{{max-width:120mm}}
</style></head><body>
<header><img src="{logo}" alt="OcoteWorks"><div class="t"><p class="k">{p['code']} · {d['fit']}</p><h1>{T[lang]['title']}</h1><p class="n">{d['name']}</p></div></header>
<ul class="chips"><li><b>{u['g_kit']}</b>{gd['kit']}</li><li><b>{u['g_tool']}</b>{gd['tool']}</li><li class="gd-pre">{u['g_pre']}</li></ul>
<div class="row">{fig1}<ol>{PR.guide_steps(p, lang, 0, 4).replace('<li>', '<li class="s">')}</ol></div>
<div class="row b"><ol>{PR.guide_steps(p, lang, 4, 6).replace('<li>', '<li class="s">')}</ol>{fig2}</div>
<footer><p>{u['g_note']} {PR.UI[lang]['fine']}</p><p style="text-align:right;white-space:nowrap">{T[lang]['web']}</p></footer>
</body></html>"""


def main(slug):
    p = next(x for x in PR.PRODUCTS if x["code"].lower() == slug)
    out_dir = os.path.join(ROOT, "assets", "products", slug)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for lang in ("es", "en"):
            pg = b.new_page(viewport={"width": 794, "height": 1123})
            pg.set_content(guide_html(p, lang)); pg.wait_for_timeout(400)
            pdf = os.path.join(out_dir, f"{slug}-guia-{lang}.pdf")
            pg.pdf(path=pdf, width="210mm", height="297mm", print_background=True, prefer_css_page_size=True)
            pg.screenshot(path=f"/tmp/guia-{lang}.png")
            pg.close()
            print(pdf, os.path.getsize(pdf) // 1024, "KB")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ow-02")
