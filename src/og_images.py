import base64, sys, re
sys.path.insert(0, "/home/claude/ocoteworks/src")
from playwright.sync_api import sync_playwright
R = "/home/claude/ocoteworks"
FS = "file:///home/claude/fontprev/node_modules/@fontsource"
def b64(p):
    ext = p.rsplit(".",1)[1]; mime = "image/jpeg" if ext=="jpg" else "image/"+ext
    return f"data:{mime};base64," + base64.b64encode(open(p,"rb").read()).decode()
build = open(R+"/src/build.py").read()
moto = re.search(r'def moto_svg\(\):.*?return """(.*?)"""', build, re.S).group(1)
logo = b64(R+"/assets/logo-sticker.png")
CSS = f"""
@font-face{{font-family:BC;font-weight:700;src:url({FS}/barlow-condensed/files/barlow-condensed-latin-700-normal.woff2)}}
@font-face{{font-family:B;font-weight:400;src:url({FS}/barlow/files/barlow-latin-400-normal.woff2)}}
@font-face{{font-family:M;font-weight:400;src:url({FS}/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2)}}
html,body{{margin:0}}
.c{{width:1200px;height:630px;position:relative;overflow:hidden;background-color:#f4ead7;
background-image:linear-gradient(#d8cdb8 1px,transparent 1px),linear-gradient(90deg,#d8cdb8 1px,transparent 1px),linear-gradient(rgba(216,205,184,.45) 1px,transparent 1px),linear-gradient(90deg,rgba(216,205,184,.45) 1px,transparent 1px);
background-size:120px 120px,120px 120px,24px 24px,24px 24px;background-position:-1px -1px}}
.vis{{position:absolute;left:0;top:0;width:540px;height:556px;border-right:6px solid #17171a;overflow:hidden;background:#17171a}}
.vis img{{width:100%;height:100%;object-fit:cover}}
.vis.paper{{background:#fbf7ef;display:flex;align-items:center;justify-content:center}}
.vis.paper svg{{width:470px}}
.code{{position:absolute;left:28px;top:28px;background:#17171a;color:#f4ead7;font:400 18px/1 M;letter-spacing:.12em;padding:9px 12px;border-radius:3px}}
.vis.paper .code{{}}
.txt{{position:absolute;left:600px;top:56px;width:550px}}
.logo{{width:140px;margin-bottom:30px;filter:drop-shadow(3px 5px 10px rgba(23,23,26,.2))}}
.eb{{display:flex;align-items:center;gap:14px;font:400 19px/1 M;letter-spacing:.14em;color:#5c574f;text-transform:uppercase;margin-bottom:20px}}
.eb:before{{content:"";width:44px;height:8px;background:#edb544;flex:none}}
h1{{margin:0;font:700 86px/.9 BC;text-transform:uppercase;color:#17171a}}
h1 span{{background:linear-gradient(transparent 58%,#edb544 58%,#edb544 90%,transparent 90%);-webkit-box-decoration-break:clone;box-decoration-break:clone}}
p{{margin:22px 0 0;font:400 24px/1.35 B;color:#3a393d;max-width:500px}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:74px;background:#17171a;display:flex;align-items:center;justify-content:space-between;padding:0 64px 0 40px;font:400 22px/1 M;letter-spacing:.1em;color:#f4ead7;text-transform:uppercase}}
.fr{{display:flex;gap:8px}}.fr i{{width:16px;height:40px;transform:skewX(-16.5deg);background:#f4ead7}}.fr i:nth-child(2){{background:#edb544}}.fr i:nth-child(3){{background:#e48233}}
.sheet{{width:420px;background:#fbf7ef;border:4px solid #17171a;border-radius:8px;padding:26px 28px;box-shadow:10px 10px 0 #edb544;font:400 18px/1 M;color:#17171a}}
.sheet .r{{display:flex;justify-content:space-between;padding:12px 0;border-bottom:2px solid #d8cdb8}}
.sheet .h{{font:700 40px/1 BC;text-transform:uppercase;margin-bottom:10px}}
.sheet .tot{{border:0;padding-top:18px;font:700 36px/1 BC}}
.gantt{{margin-top:16px;display:grid;gap:7px}}.gantt i{{display:block;height:12px;background:#17171a;border-radius:2px}}
"""
def photo(src, code): return f'<div class="vis"><img src="{b64(R+"/assets/photos/"+src)}"><span class="code">{code}</span></div>'
def paper(inner, code): return f'<div class="vis paper">{inner}<span class="code">{code}</span></div>'
SHEET = {
 "en": ("Project sheet", [("OW-DS Design","✓"),("OW-PT Prototype","✓"),("OW-PK Packaging","✓")], "Estimate"),
 "es": ("Hoja de proyecto", [("OW-DS Diseño","✓"),("OW-PT Prototipo","✓"),("OW-PK Empaque","✓")], "Estimación"),
}
def sheet(lang):
    h, rows, est = SHEET[lang]
    r = "".join(f'<div class="r"><span>{a}</span><span>{b}</span></div>' for a,b in rows)
    g = '<div class="gantt"><i style="width:30%"></i><i style="width:22%;margin-left:30%"></i><i style="width:34%;margin-left:52%;background:#e48233"></i><i style="width:14%;margin-left:86%;background:#edb544"></i></div>'
    return f'<div class="sheet"><div class="h">{h}</div>{r}{g}</div>'
PAGES = {
 "services": {"vis": lambda l: photo("about/engine-teardown-1000.jpg","OW · 01"),
   "en": ("Engineering services","Design. Prototype. <span>Fabricate.</span>","From the idea to a part you can hold, test and sell."),
   "es": ("Servicios de ingeniería","Diseñar. Prototipar. <span>Fabricar.</span>","De la idea a una pieza que puedes tocar, probar y vender.")},
 "about": {"vis": lambda l: photo("about/workshop-night-1400.jpg","OW · ID-001"), "size": 64,
   "en": ("About · Manuel García","Designer by training. <span>Engineer by habit.</span>","Industrial designer and product development engineer in Monterrey."),
   "es": ("Sobre mí · Manuel García","Diseñador de formación. <span>Ingeniero por costumbre.</span>","Diseñador industrial e ingeniero de producto en Monterrey.")},
 "products": {"vis": lambda l: paper(moto, "OW-01 · REV 0"),
   "en": ("Products · OW-01","Building <span>in progress</span>","Rackless luggage for adventure motorcycles: machined hardware, leather and textile."),
   "es": ("Productos · OW-01","Building <span>in progress</span>","Equipaje rackless para motos de aventura: herrajes maquinados, cuero y textil.")},
 "journal": {"vis": lambda l: photo("about/river-crossing-1600.jpg","OW · LOG"),
   "en": ("Journal","Field notes &amp; <span>build logs</span>","Prototypes, CNC tests, materials and trips."),
   "es": ("Bitácora","Notas de campo <span>y de taller</span>","Prototipos, pruebas CNC, materiales y viajes.")},
 "quote": {"vis": lambda l: paper(sheet(l), "OW-Q"),
   "en": ("Quote builder","Build your <span>project</span>","Pick what you need and get a cost range and a timeline in minutes."),
   "es": ("Cotizador","Arma tu <span>proyecto</span>","Elige lo que necesitas y obtén un rango de costo y un cronograma en minutos.")},
}
PAGES["ow02"] = {"vis": lambda l: f'<div class="vis"><img src="{b64(R+"/assets/products/ow-02/hero-1600.jpg")}" style="object-fit:contain;background:linear-gradient(#d3d3d3,#c9c9c9);transform:scale(1.18)"><span class="code">OW-02</span></div>', "size": 92,
   "en": ("Ténéré 700 · 2019–2023", "Tail Rack <span>T7</span>", "One piece of folded aluminum. First batch in pre-production: join the list."),
   "es": ("Ténéré 700 · 2019–2023", "Tail Rack <span>T7</span>", "Una sola pieza de aluminio doblado. Primer lote en preparación: únete a la lista.")}
PAGES["j-ow-02-silueta"] = {"vis": lambda l: f'<div class="vis"><img src="{b64(R+"/assets/journal/ow-02-silueta/carton-lado-1200.jpg")}" style="object-position:62% 50%"><span class="code">{"BITÁCORA" if l=="es" else "JOURNAL"}</span></div>', "size": 74,
   "en": ("Journal · Build", "Keep it looking like a <span>dirt bike</span>", "How the OW-02 started: from notebook sketch to cardboard prototype."),
   "es": ("Bitácora · Taller", "Que siga pareciendo <span>dirt bike</span>", "Cómo nació el OW-02: del boceto en el cuaderno al prototipo de cartón.")}
ONLY = sys.argv[1:]  # p. ej. python3 src/og_images.py ow02
URL = {"j-ow-02-silueta":("/journal/ow-02-silueta","/es/bitacora/ow-02-silueta"),"ow02":("/products/ow-02-tail-rack","/es/productos/ow-02-tail-rack"),"services":("/services","/es/servicios"),"about":("/about","/es/sobre-mi"),"products":("/products","/es/productos"),
       "journal":("/journal","/es/bitacora"),"quote":("/quote","/es/cotizar")}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1200,"height":630})
    for key, d in PAGES.items():
        if ONLY and key not in ONLY: continue
        for i, lang in enumerate(("en","es")):
            eb, h1, lead = d[lang]
            html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="c">{d["vis"](lang)}<div class="txt"><img class="logo" src="{logo}"><div class="eb">{eb}</div><h1 style="font-size:{d.get('size',86)}px">{h1}</h1><p>{lead}</p></div><div class="foot"><span>ocoteworks.com{URL[key][i]}</span><span class="fr"><i></i><i></i><i></i></span></div></div></body></html>'
            open("/home/claude/ogwork/t.html","w").write(html)
            pg.goto("file:///home/claude/ogwork/t.html"); pg.wait_for_timeout(300)
            pg.screenshot(path=f"{R}/assets/og/{key}-{lang}.jpg", type="jpeg", quality=86)
    b.close()
print("done")
