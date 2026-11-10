"""Ficha técnica tipo blueprint (A3 horizontal) en PDF + vista previa PNG.

Uso: python3 src/spec_sheet.py ow-02
Vistas en línea: src/sheet/<slug>/{top,side,right,iso}.png (marfil sobre transparente) + views.json
(ancho/alto en mm del modelo, con 3 mm de margen por lado). Se generan desde el GLB con detección de bordes
(ver notas en el documento del proyecto). Requiere Playwright y las fuentes @fontsource locales (FONT_DIR).
"""
import base64, json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = "/home/claude/fontprev/node_modules/@fontsource"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import products as PR

SCALE = 3          # 1:3
MARGIN_MODEL = 3   # mm de margen en las imágenes, en unidades del modelo
REV, DATE = "A", "09.11.2026"

T = {
    "es": dict(title="Ficha técnica", top="Vista superior", side="Vista lateral", right="Vista posterior", iso="Isométrico",
               part="Pieza", code="Código", mat="Material", fin="Acabado", scale="Escala", units="Unidades", proj="Proyección",
               proj_v="3er ángulo", sheet="Hoja", rev="Rev.", date="Fecha", drawn="Dibujó", specs="Especificaciones",
               notes="Notas", stamp="Preliminar · no para fabricación",
               n=["Medidas en milímetros. Cotas generales tomadas del modelo CAD.",
                  "Especificaciones preliminares; pueden cambiar en producción.",
                  "Ténéré 700 es marca registrada de Yamaha Motor Co., Ltd. OcoteWorks no está afiliado a Yamaha."],
               mat_v="Al 6061 · 4.8 mm", fin_v="Pintura en polvo, mate", web="ocoteworks.com"),
    "en": dict(title="Spec sheet", top="Top view", side="Side view", right="Rear view", iso="Isometric",
               part="Part", code="Code", mat="Material", fin="Finish", scale="Scale", units="Units", proj="Projection",
               proj_v="3rd angle", sheet="Sheet", rev="Rev.", date="Date", drawn="Drawn", specs="Specifications",
               notes="Notes", stamp="Preliminary · not for manufacturing",
               n=["Dimensions in millimeters. Overall dimensions taken from the CAD model.",
                  "Preliminary specifications; may change in production.",
                  "Ténéré 700 is a registered trademark of Yamaha Motor Co., Ltd. OcoteWorks is not affiliated with Yamaha."],
               mat_v="6061 Al · 4.8 mm", fin_v="Matte powder coat", web="ocoteworks.com"),
}


def b64(path, mime="image/png"):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def font(face, fam, w):
    return (f"@font-face{{font-family:'{fam}';font-weight:{w};src:url({b64(f'{FONT_DIR}/{face}/files/{face}-latin-{w}-normal.woff2', 'font/woff2')}) format('woff2')}}")


def dim_h(x1, x2, y, label, ext_from=None, below=True):
    """Cota horizontal entre x1 y x2 a la altura y; líneas de extensión desde ext_from."""
    s = []
    if ext_from is not None:
        for x in (x1, x2):
            s.append(f'<line x1="{x}" y1="{ext_from + (1 if below else -1)}" x2="{x}" y2="{y + (1.5 if below else -1.5)}" class="ext"/>')
    s.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="dim" marker-start="url(#a)" marker-end="url(#a)"/>')
    s.append(f'<rect x="{(x1 + x2) / 2 - 7}" y="{y - 2.2}" width="14" height="4.4" class="lblbg"/>')
    s.append(f'<text x="{(x1 + x2) / 2}" y="{y + 1.15}" class="dimt">{label}</text>')
    return "".join(s)


def dim_v(y1, y2, x, label, ext_from=None, left=True):
    s = []
    if ext_from is not None:
        for y in (y1, y2):
            s.append(f'<line x1="{ext_from + (-1 if left else 1)}" y1="{y}" x2="{x + (-1.5 if left else 1.5)}" y2="{y}" class="ext"/>')
    s.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="dim" marker-start="url(#a)" marker-end="url(#a)"/>')
    cy = (y1 + y2) / 2
    s.append(f'<rect x="{x - 2.2}" y="{cy - 7}" width="4.4" height="14" class="lblbg"/>')
    s.append(f'<text x="{x}" y="{cy}" class="dimt" transform="rotate(-90 {x} {cy})" dy="1.15">{label}</text>')
    return "".join(s)


def sheet_html(p, lang):
    t, d = T[lang], p[lang]
    slug = p["code"].lower()
    vdir = os.path.join(ROOT, "src", "sheet", slug)
    meta = json.load(open(os.path.join(vdir, "views.json")))
    sz = {k: (meta[k]["wmm"] / SCALE, meta[k]["hmm"] / SCALE) for k in ("top", "side", "right")}
    m = MARGIN_MODEL / SCALE
    L, W, H = 489, 243, 128  # cotas generales (rack, del CAD)

    # Posiciones (mm en la hoja)
    xs, yt = 34, 47
    tw, th = sz["top"]; sw, sh = sz["side"]; rw, rh = sz["right"]
    ys = yt + th + 24
    xr = xs + sw + 30
    iso_w = 158; iso_h = iso_w * meta["iso"]["hmm"] / meta["iso"]["wmm"]
    xi, yi = 236, 56

    svg = []
    # Cotas
    svg.append(dim_h(xs + m, xs + sw - m, ys + sh + 9, str(L), ext_from=ys + sh - m))
    svg.append(dim_v(ys + m, ys + sh - m, xs - 9, str(H), ext_from=xs + m))
    svg.append(dim_v(yt + m, yt + th - m, xs - 9, str(W), ext_from=xs + m))
    svg.append(dim_h(xr + m, xr + rw - m, ys + sh + 9, str(W), ext_from=ys + sh - m))
    svg.append(dim_v(ys + m, ys + sh - m, xr + rw + 9, str(H), ext_from=xr + rw - m, left=False))
    # Líneas de proyección (punteadas) entre vistas
    svg.append(f'<line x1="{xs + sw + 4}" y1="{ys + sh / 2}" x2="{xr - 4}" y2="{ys + sh / 2}" class="proj"/>')
    svg.append(f'<line x1="{xs + sw / 2}" y1="{yt + th + 4}" x2="{xs + sw / 2}" y2="{ys - 4}" class="proj"/>')

    # Marco con zonas
    zones = []
    for i in range(8):
        x = 10 + (400 / 8) * (i + .5)
        zones.append(f'<text x="{x}" y="14.2" class="zone">{i + 1}</text><text x="{x}" y="285.3" class="zone">{i + 1}</text>')
    for i, c in enumerate("ABCD"):
        y = 17 + (263 / 4) * (i + .5)
        zones.append(f'<text x="12.6" y="{y + 1}" class="zone">{c}</text><text x="407.4" y="{y + 1}" class="zone">{c}</text>')
    ticks = "".join(f'<line x1="{10 + 50 * i}" y1="10" x2="{10 + 50 * i}" y2="17" class="fr"/><line x1="{10 + 50 * i}" y1="280" x2="{10 + 50 * i}" y2="287" class="fr"/>' for i in range(1, 8))
    ticks += "".join(f'<line x1="10" y1="{17 + 65.75 * i}" x2="17" y2="{17 + 65.75 * i}" class="fr"/><line x1="403" y1="{17 + 65.75 * i}" x2="410" y2="{17 + 65.75 * i}" class="fr"/>' for i in range(1, 4))

    # Símbolo de 3er ángulo
    proj_sym = ('<g transform="translate(0,0)" class="sym"><line x1="0" y1="2.5" x2="9" y2="2.5" class="cl"/>'
                '<path d="M1 0.5 L5 1.4 L5 3.6 L1 4.5 Z"/><circle cx="12.5" cy="2.5" r="2"/><circle cx="12.5" cy="2.5" r="0.9"/></g>')

    specs = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in d["specs"])
    notes = "".join(f"<li>{n}</li>" for n in t["n"])
    logo = b64(os.path.join(ROOT, "assets", "logo-marfil.png"))
    img = {k: b64(os.path.join(vdir, f"{k}.png")) for k in ("top", "side", "right", "iso")}
    fonts = (font("barlow-condensed", "BC", 600) + font("barlow-condensed", "BC", 700) +
             font("ibm-plex-mono", "Plex", 400) + font("ibm-plex-mono", "Plex", 500) + font("barlow", "Barlow", 400))

    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{p['code']} · {t['title']}</title><style>
{fonts}
@page{{size:420mm 297mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:420mm;height:297mm}}
body{{background:#17171a;color:#f4ead7;font-family:'Plex',monospace;-webkit-print-color-adjust:exact;print-color-adjust:exact;position:relative;overflow:hidden}}
.grid{{position:absolute;left:17mm;top:17mm;width:386mm;height:263mm;background-image:
  linear-gradient(rgba(244,234,215,.085) .25mm,transparent .25mm),linear-gradient(90deg,rgba(244,234,215,.085) .25mm,transparent .25mm),
  linear-gradient(rgba(244,234,215,.035) .15mm,transparent .15mm),linear-gradient(90deg,rgba(244,234,215,.035) .15mm,transparent .15mm);
  background-size:25mm 25mm,25mm 25mm,5mm 5mm,5mm 5mm;background-position:-.1mm -.1mm}}
.v{{position:absolute}}
.lbl{{position:absolute;font:500 2.7mm/1 'Plex';letter-spacing:.14em;text-transform:uppercase;color:#f4ead7}}
.lbl b{{color:#edb544;font-weight:500}}
svg.ov{{position:absolute;inset:0;width:420mm;height:297mm}}
.dim{{stroke:#edb544;stroke-width:.22;fill:none}} .ext{{stroke:#edb544;stroke-width:.15;opacity:.8}}
.dimt{{fill:#edb544;font:500 3.1px 'Plex';text-anchor:middle}} .lblbg{{fill:#17171a}}
.proj{{stroke:rgba(244,234,215,.28);stroke-width:.15;stroke-dasharray:2 1.2}}
.fr{{stroke:#f4ead7;stroke-width:.3}} .frame{{fill:none;stroke:#f4ead7;stroke-width:.5}} .frame2{{fill:none;stroke:#f4ead7;stroke-width:.25}}
.zone{{fill:rgba(244,234,215,.6);font:400 2.4px 'Plex';text-anchor:middle}}
.sym{{fill:none;stroke:#f4ead7;stroke-width:.25}} .cl{{stroke-dasharray:1.6 .6 .3 .6}}
.head{{position:absolute;left:24mm;top:22mm;display:flex;align-items:baseline;gap:5mm}}
.head h1{{font:700 9mm/1 'BC';letter-spacing:.01em;text-transform:uppercase}}
.head span{{font:400 2.8mm/1 'Plex';letter-spacing:.16em;text-transform:uppercase;color:#edb544}}
.stamp{{position:absolute;right:24mm;top:23mm;border:.35mm solid #edb544;color:#edb544;padding:1.6mm 3mm;font:500 2.7mm/1 'Plex';letter-spacing:.14em;text-transform:uppercase;transform:rotate(-2deg)}}
.specs{{position:absolute;left:24mm;top:225mm;width:150mm}}
.specs h2,.notes h2{{font:500 2.6mm/1 'Plex';letter-spacing:.16em;text-transform:uppercase;color:#edb544;margin-bottom:2.2mm}}
table{{border-collapse:collapse;width:100%}}
th,td{{text-align:left;font:400 2.55mm/1.25 'Plex';padding:.9mm 0;border-top:.15mm solid rgba(244,234,215,.22);vertical-align:top}}
th{{width:36mm;color:rgba(244,234,215,.62);font-weight:400;text-transform:uppercase;letter-spacing:.06em;font-size:2.25mm;padding-right:3mm}}
.notes{{position:absolute;left:184mm;top:225mm;width:104mm}}
.notes ol{{padding-left:4mm}} .notes li{{font:400 2.4mm/1.4 'Plex';margin-bottom:1.2mm;color:rgba(244,234,215,.85)}}
.tb{{position:absolute;right:17mm;bottom:17mm;width:112mm;border:.5mm solid #f4ead7;display:grid;grid-template-columns:1fr 1fr 1fr}}
.tb>div{{border-right:.25mm solid #f4ead7;border-bottom:.25mm solid #f4ead7;padding:1.3mm 2mm;min-height:9mm}}
.tb>div:nth-child(3n){{border-right:0}}
.tb .k{{display:block;font:400 1.9mm/1 'Plex';letter-spacing:.12em;text-transform:uppercase;color:rgba(244,234,215,.6);margin-bottom:1.3mm}}
.tb .val{{font:500 2.8mm/1.15 'Plex'}}
.tb .logo{{grid-column:1/3;display:flex;align-items:center;gap:3mm}}
.tb .logo img{{height:9mm}} .tb .logo small{{font:400 2.1mm/1.3 'Plex';color:rgba(244,234,215,.7)}}
.tb .name{{grid-column:1/3}} .tb .name .val{{font:700 6.4mm/1 'BC';text-transform:uppercase;letter-spacing:.01em}}
.tb .last{{border-bottom:0}}
</style></head><body>
<div class="grid"></div>
<svg class="ov" viewBox="0 0 420 297" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="a" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="2.2" markerHeight="2.2" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0 0.6 L6 3 L0 5.4 Z" fill="#edb544"/></marker></defs>
<rect x="10" y="10" width="400" height="277" class="frame"/><rect x="17" y="17" width="386" height="263" class="frame2"/>
{ticks}{''.join(zones)}{''.join(svg)}
</svg>
<div class="head"><h1>{d['name']}</h1><span>{p['code']} · {t['title']}</span></div>
<div class="stamp">{t['stamp']}</div>
<img class="v" src="{img['top']}" style="left:{xs}mm;top:{yt}mm;width:{tw}mm;height:{th}mm">
<img class="v" src="{img['side']}" style="left:{xs}mm;top:{ys}mm;width:{sw}mm;height:{sh}mm">
<img class="v" src="{img['right']}" style="left:{xr}mm;top:{ys}mm;width:{rw}mm;height:{rh}mm">
<img class="v" src="{img['iso']}" style="left:{xi}mm;top:{yi}mm;width:{iso_w}mm;height:{iso_h}mm">
<div class="lbl" style="left:{xs}mm;top:{yt - 6}mm"><b>A</b> · {t['top']} · 1:{SCALE}</div>
<div class="lbl" style="left:{xs}mm;top:{ys + sh + 16}mm"><b>B</b> · {t['side']} · 1:{SCALE}</div>
<div class="lbl" style="left:{xr}mm;top:{ys + sh + 16}mm"><b>C</b> · {t['right']} · 1:{SCALE}</div>
<div class="lbl" style="left:{xi}mm;top:{yi - 6}mm"><b>D</b> · {t['iso']}</div>
<div class="specs"><h2>{t['specs']}</h2><table>{specs}</table></div>
<div class="notes"><h2>{t['notes']}</h2><ol>{notes}</ol></div>
<div class="tb">
  <div class="logo"><img src="{logo}" alt="OcoteWorks"><small>Monterrey, N.L., México<br>{t['web']}</small></div>
  <div><span class="k">{t['code']}</span><span class="val">{p['code']}</span></div>
  <div class="name"><span class="k">{t['part']}</span><span class="val">{d['name']}</span></div>
  <div><span class="k">{t['rev']}</span><span class="val">{REV}</span></div>
  <div><span class="k">{t['mat']}</span><span class="val">{t['mat_v']}</span></div>
  <div><span class="k">{t['fin']}</span><span class="val">{t['fin_v']}</span></div>
  <div><span class="k">{t['date']}</span><span class="val">{DATE}</span></div>
  <div class="last"><span class="k">{t['scale']} · {t['units']}</span><span class="val">1:{SCALE} · mm</span></div>
  <div class="last"><span class="k">{t['proj']}</span><span class="val" style="display:flex;align-items:center;gap:2mm"><svg viewBox="0 0 15 5" style="width:12mm;height:4mm">{proj_sym}</svg>{t['proj_v']}</span></div>
  <div class="last"><span class="k">{t['drawn']} · {t['sheet']}</span><span class="val">M. García · 1/1</span></div>
</div>
</body></html>"""


def main(slug):
    p = next(x for x in PR.PRODUCTS if x["code"].lower() == slug)
    out_dir = os.path.join(ROOT, "assets", "products", slug)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for lang in ("es", "en"):
            html = sheet_html(p, lang)
            open(f"/tmp/sheet-{lang}.html", "w").write(html)
            pg = b.new_page(viewport={"width": 1588, "height": 1123})
            pg.set_content(html); pg.wait_for_timeout(400)
            pdf = os.path.join(out_dir, f"{slug}-ficha-{lang}.pdf")
            pg.pdf(path=pdf, width="420mm", height="297mm", print_background=True, prefer_css_page_size=True)
            pg.screenshot(path=f"/tmp/sheet-{lang}.png", full_page=False)
            pg.close()
            # Vista previa para la ficha web (2x para pantallas densas)
            pv = b.new_page(viewport={"width": 1588, "height": 1123}, device_scale_factor=1)
            pv.set_content(html); pv.wait_for_timeout(400); pv.screenshot(path=f"/tmp/sheet-{lang}-big.png")
            pv.close()
            from PIL import Image
            im = Image.open(f"/tmp/sheet-{lang}-big.png").convert("RGB")
            for w in (700, 1200):
                r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
                r.save(os.path.join(out_dir, f"{slug}-ficha-{lang}-{w}.webp"), quality=86, method=6)
                r.save(os.path.join(out_dir, f"{slug}-ficha-{lang}-{w}.jpg"), quality=86, optimize=True, progressive=True)
            print(pdf, os.path.getsize(pdf) // 1024, "KB")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ow-02")
