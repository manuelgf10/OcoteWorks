"""Catálogo de productos de OcoteWorks.

Prueba de demanda: los productos marcados con status "batch" muestran precio y botón Comprar, pero el botón abre un
panel honesto ("todavía no lo fabricamos") que apunta a una lista de interés en Formspree. No se cobra nada.
Para agregar un producto: copiar el bloque de OW-02, cambiar los textos e imágenes (assets/products/<slug>/) y regenerar.
"""

FORMSPREE = "https://formspree.io/f/mwllgewa"

PRODUCTS = [
    {
        "code": "OW-02",
        "slug": "ow-02-tail-rack",
        "status": "batch",
        "price_mxn": 1532,
        "img_dir": "/assets/products/ow-02",
        # Modelo 3D (GLB en metros, desde el STEP de SolidWorks; material 0 = "rack", se pinta según el acabado).
        "model": "/assets/products/ow-02/ow-02.glb",
        # Ficha técnica tipo blueprint (src/spec_sheet.py): PDF A3 + vista previa por idioma.
        "sheet": True,
        # Cotas generales del CAD (largo, ancho, alto) en mm y datos para la banda de plano animada.
        "dims": (489, 243, 128),
        "bp_stats": [("4.8", "mm"), ("0.5", "kg"), ("1", ""), ("0", "")],
        # (archivo base, anchos disponibles, ancho x alto del original)
        "images": [("hero", (600, 1000, 1600), (2576, 1449)), ("top", (600, 1000, 1600), (2576, 1449)),
                   ("front", (600, 1000, 1600), (2576, 1449)), ("detail", (500, 900), (1308, 2326))],
        "variants": [("black", "#17171a"), ("white", "#f4f2ee")],
        # Galería propia por acabado (mismo orden que "images"); el negro usa "images".
        "variant_images": {"white": [("w-hero", (600, 1000, 1400), (1536, 1024)), ("w-top", (600, 1000, 1400), (1536, 1024)),
                                     ("w-front", (600, 1000, 1400), (1448, 1086)), ("w-detail", (500, 900), (1024, 1536))]},
        "es": {
            "name": "Tail Rack T7",
            "fit": "Yamaha Ténéré 700 · 2019–2023",
            "tagline": "Una sola pieza de aluminio doblado. Discreta, respeta la silueta de la T7 y lleva lo justo: una bolsa pequeña o un par de straps.",
            "card": "Parrilla trasera de una sola pieza para la Ténéré 700.",
            "intent": "La idea: una parrilla que casi no se note en la moto, pero que esté ahí cuando necesitas amarrar algo.",
            "variants": {"black": "Negro mate", "white": "Blanco mate"},
            "alts": ["Tail rack OW-02 en negro mate, vista en tres cuartos",
                     "Tail rack OW-02 visto desde un costado, con las ranuras de amarre",
                     "Tail rack OW-02 visto de frente",
                     "Detalle de la placa superior del OW-02 con el logo grabado y las ranuras redondeadas"],
            "variant_alts": {"white": ["Tail rack OW-02 en blanco mate, vista en tres cuartos",
                                       "Tail rack OW-02 en blanco mate visto desde un costado",
                                       "Tail rack OW-02 en blanco mate visto de frente",
                                       "Detalle de la placa superior del OW-02 en blanco mate con el logo grabado"]},
            "highlights": [
                ("Una sola pieza", "Lámina de aluminio 6061 cortada en láser y doblada. Sin soldaduras ni uniones."),
                ("Perfil bajo", "Sigue la línea del asiento y de la cola. De lejos, la moto se ve como salió de fábrica."),
                ("Puntos de amarre", "Ranuras para straps y bolsas pequeñas, con los cantos redondeados en CNC para no cortar las cintas."),
            ],
            "specs": [
                ("Compatibilidad", "Yamaha Ténéré 700, 2019–2023"),
                ("Material", "Aluminio 6061, espesor aprox. 4.8 mm (3/16″)"),
                ("Proceso", "Corte láser · doblado · cantos redondeados en CNC"),
                ("Acabado", "Pintura electrostática en polvo, negro o blanco mate"),
                ("Medidas aprox.", "489 × 243 × 128 mm (largo × ancho × alto)"),
                ("Peso aprox.", "0.5 kg sin tornillería"),
                ("Incluye", "Tornillería de montaje"),
                ("Uso", "Cargas ligeras: bolsas pequeñas y straps"),
            ],
        },
        "en": {
            "name": "Tail Rack T7",
            "fit": "Yamaha Ténéré 700 · 2019–2023",
            "tagline": "One piece of folded aluminum. Low-profile, keeps the T7’s lines and carries just enough: a small bag or a couple of straps.",
            "card": "One-piece rear rack for the Ténéré 700.",
            "intent": "The idea: a rack you barely notice on the bike, but that’s there when you need to strap something down.",
            "variants": {"black": "Matte black", "white": "Matte white"},
            "alts": ["OW-02 tail rack in matte black, three-quarter view",
                     "OW-02 tail rack seen from the side, showing the strap slots",
                     "OW-02 tail rack seen from the front",
                     "Close-up of the OW-02 top plate with the engraved logo and rounded slots"],
            "variant_alts": {"white": ["OW-02 tail rack in matte white, three-quarter view",
                                       "OW-02 tail rack in matte white seen from the side",
                                       "OW-02 tail rack in matte white seen from the front",
                                       "Close-up of the matte white OW-02 top plate with the engraved logo"]},
            "highlights": [
                ("One piece", "6061 aluminum sheet, laser cut and folded. No welds, no joints."),
                ("Low profile", "Follows the line of the seat and tail. From a distance the bike looks stock."),
                ("Tie-down points", "Slots for straps and small bags, with CNC-rounded edges so they won’t cut webbing."),
            ],
            "specs": [
                ("Fitment", "Yamaha Ténéré 700, 2019–2023"),
                ("Material", "6061 aluminum, approx. 4.8 mm (3/16″) thick"),
                ("Process", "Laser cut · folded · CNC-rounded edges"),
                ("Finish", "Powder coat, matte black or matte white"),
                ("Approx. size", "489 × 243 × 128 mm (length × width × height)"),
                ("Approx. weight", "0.5 kg without hardware"),
                ("Includes", "Mounting hardware"),
                ("Use", "Light loads: small bags and straps"),
            ],
        },
    },
]

UI = {
    "es": dict(
        home_eyebrow="Tienda · Primer lote",
        home_all="Todos los productos",
        cat_title="Productos · OcoteWorks",
        cat_description="Productos propios de OcoteWorks, diseñados y probados en Monterrey: OW-02 Tail Rack para la Ténéré 700 y OW-01, equipaje rackless en desarrollo.",
        cat_eyebrow="Productos · Monterrey, MX",
        cat_h1="Diseñado <em>en el taller</em>",
        cat_lead="Piezas propias para motos de aventura. Algunas están en preparación: si te interesan, únete a la lista y ayúdanos a decidir qué fabricar primero.",
        cat_view="Ver producto",
        sheet_k="Ficha técnica", sheet_cta="Descargar PDF", sheet_meta="A3 · vistas, cotas generales y especificaciones",
        sheet_alt="Vista previa de la ficha técnica del OW-02 en estilo plano: vistas superior, lateral, posterior e isométrica con cotas",
        v3d="Ver en 3D", v3d_hint="Arrastra para girar · pellizca o usa la rueda para acercar", v3d_ar="Ver en tu espacio",
        v3d_load="Cargando modelo 3D…", v3d_err="No se pudo cargar el modelo 3D.",
        v3d_alt="Modelo 3D del tail rack OW-02",
        status_batch="Primer lote en preparación",
        status_dev="En desarrollo",
        ow01_name="Equipaje rackless",
        ow01_card="Maletas laterales de cuero con herrajes maquinados. Sin parrillas.",
        ow01_link="Avísame",
        price_note="Precio objetivo del primer lote",
        buy="Comprar",
        buy_note="Sin cobro: al pulsar, te unes a la lista del primer lote.",
        variant="Acabado",
        hl_eyebrow="01 · Diseño",
        hl_h2="Lo justo, <em>nada más</em>",
        specs_eyebrow="03 · Especificaciones",
        bp_eyebrow="02 · Medidas", bp_h2="Sacado del CAD", bp_p="Vista lateral y posterior a escala, con las cotas generales tomadas del modelo en SolidWorks.",
        bp_side="Vista lateral", bp_rear="Vista posterior", bp_stats=["Espesor", "Peso aprox.", "Pieza", "Soldaduras"],
        bp_alt_side="Vista lateral del OW-02 en línea, estilo plano", bp_alt_rear="Vista posterior del OW-02 en línea, estilo plano",
        specs_h2="Ficha técnica",
        specs_note="Especificaciones preliminares; pueden cambiar en producción.",
        fine=("Imágenes y modelo 3D: tomados del modelo CAD. Ténéré 700 es una marca registrada de Yamaha Motor Co., Ltd. "
              "OcoteWorks no está afiliado a Yamaha; el nombre se usa solo para indicar compatibilidad."),
        back="← Todos los productos",
        dlg_k="Primer lote",
        dlg_h="Todavía no lo fabricamos.",
        dlg_p=("Estamos midiendo cuánta gente lo quiere antes de producir el primer lote. Déjanos tu correo y te avisamos primero, "
               "con el precio de lanzamiento. No se cobra nada."),
        dlg_email="Tu correo", dlg_ph="tu@correo.com", dlg_qty="Piezas",
        dlg_submit="Unirme a la lista", dlg_close="Cerrar",
        dlg_ok="Listo. Estás en la lista del primer lote de {code} ({variant}). Te escribimos antes que a nadie.",
        dlg_err="Algo falló. Escríbenos a hola@ocoteworks.com.",
        dlg_privacy='Usamos tu correo solo para avisarte de este producto. <a href="/es/privacidad/">Aviso de privacidad</a>.',
    ),
    "en": dict(
        home_eyebrow="Shop · First batch",
        home_all="All products",
        cat_title="Products · OcoteWorks",
        cat_description="Original OcoteWorks products, designed and tested in Monterrey: the OW-02 Tail Rack for the Ténéré 700 and OW-01 rackless luggage in development.",
        cat_eyebrow="Products · Monterrey, MX",
        cat_h1="Designed <em>in the workshop</em>",
        cat_lead="Original parts for adventure motorcycles. Some are in pre-production: if one interests you, join the list and help us decide what to make first.",
        cat_view="View product",
        sheet_k="Spec sheet", sheet_cta="Download PDF", sheet_meta="A3 · views, overall dimensions and specifications",
        sheet_alt="Preview of the OW-02 spec sheet in blueprint style: top, side, rear and isometric views with dimensions",
        v3d="View in 3D", v3d_hint="Drag to rotate · pinch or scroll to zoom", v3d_ar="View in your space",
        v3d_load="Loading 3D model…", v3d_err="The 3D model couldn’t load.",
        v3d_alt="3D model of the OW-02 tail rack",
        status_batch="First batch in pre-production",
        status_dev="In development",
        ow01_name="Rackless luggage",
        ow01_card="Leather side bags with machined hardware. No racks.",
        ow01_link="Notify me",
        price_note="Target price for the first batch",
        buy="Buy",
        buy_note="No charge: tapping it adds you to the first-batch list.",
        variant="Finish",
        hl_eyebrow="01 · Design",
        hl_h2="Just enough, <em>nothing more</em>",
        specs_eyebrow="03 · Specifications",
        bp_eyebrow="02 · Dimensions", bp_h2="Straight from CAD", bp_p="Side and rear views to scale, with overall dimensions taken from the SolidWorks model.",
        bp_side="Side view", bp_rear="Rear view", bp_stats=["Thickness", "Approx. weight", "Piece", "Welds"],
        bp_alt_side="Line drawing of the OW-02, side view, blueprint style", bp_alt_rear="Line drawing of the OW-02, rear view, blueprint style",
        specs_h2="Spec sheet",
        specs_note="Preliminary specifications; may change in production.",
        fine=("Images and 3D model: from the CAD model. Ténéré 700 is a registered trademark of Yamaha Motor Co., Ltd. "
              "OcoteWorks is not affiliated with Yamaha; the name is used only to indicate fitment."),
        back="← All products",
        dlg_k="First batch",
        dlg_h="We haven’t made it yet.",
        dlg_p=("We’re measuring how many people want it before producing the first batch. Leave your email and you’ll hear first, "
               "with the launch price. Nothing is charged."),
        dlg_email="Your email", dlg_ph="you@email.com", dlg_qty="Pieces",
        dlg_submit="Join the list", dlg_close="Close",
        dlg_ok="Done. You’re on the first-batch list for {code} ({variant}). You’ll hear before anyone else.",
        dlg_err="Something went wrong. Please write to hola@ocoteworks.com.",
        dlg_privacy='We only use your email to tell you about this product. <a href="/privacy/">Privacy notice</a>.',
    ),
}


def url(p, lang):
    return ("/es/productos/" if lang == "es" else "/products/") + p["slug"] + "/"


def price(p):
    return f"${p['price_mxn']:,} MXN"


def image_set(p, lang, v=None):
    """Imágenes y textos alternativos de un acabado (None o el primero = las de "images")."""
    if v and v in p.get("variant_images", {}):
        return p["variant_images"][v], p[lang]["variant_alts"][v]
    return p["images"], p[lang]["alts"]


def picture(p, i, lang, sizes, cls="", eager=False, v=None):
    imgs, alts = image_set(p, lang, v)
    name, widths, (W, H) = imgs[i]
    base = p["img_dir"] + "/" + name
    webp = ", ".join(f"{base}-{w}.webp {w}w" for w in widths)
    jpg = ", ".join(f"{base}-{w}.jpg {w}w" for w in widths)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture{cls}><source srcset="{webp}" sizes="{sizes}" type="image/webp">'
            f'<img src="{base}-{widths[1] if len(widths) > 1 else widths[0]}.jpg" srcset="{jpg}" sizes="{sizes}" '
            f'alt="{alts[i]}" width="{W}" height="{H}" {load} decoding="async"></picture>')


def gallery(p, lang):
    """Una galería por acabado; solo la del acabado elegido está visible (las ocultas no descargan nada)."""
    out = []
    for vi, (v, _) in enumerate(p["variants"]):
        imgs, alts = image_set(p, lang, v)
        tall = ' class="pd-main tall"' if imgs[0][2][1] > imgs[0][2][0] else ' class="pd-main"'
        if vi == 0:
            tall += f' style="{vt(p)}"'
        main = picture(p, 0, lang, "(max-width:900px) 100vw, 640px", tall, eager=vi == 0, v=v)
        thumbs = "".join(
            f'<button type="button" class="pd-thumb" data-i="{i}" aria-label="{alts[i]}"{" aria-current=\"true\"" if i == 0 else ""}>'
            f'{picture(p, i, lang, "120px", v=v)}</button>' for i in range(len(imgs)))
        # Fuentes de cada imagen para que el JS cambie la principal sin recargar.
        data = "|".join(f'{p["img_dir"]}/{n}-{w[-1]}' for n, w, _ in imgs)
        if vi and v not in p.get("variant_images", {}):
            continue  # acabado sin fotos propias: se queda la galería principal
        if p.get("model"):
            u = UI[lang]
            thumbs += (f'<button type="button" class="pd-thumb pd-thumb-3d" data-3d="{p["model"]}" data-lib="/assets/vendor/model-viewer-4.4.0.min.js" '
                       f'data-alt="{u["v3d_alt"]}" data-hint="{u["v3d_hint"]}" data-ar="{u["v3d_ar"]}" data-load="{u["v3d_load"]}" data-err="{u["v3d_err"]}" '
                       f'aria-label="{u["v3d"]}">'
                       '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5 20.5 7v10L12 21.5 3.5 17V7z M3.5 7 12 11.5 20.5 7 M12 11.5v10"/></svg>'
                       '<span>3D</span></button>')
            main += '<div class="pd-3d" hidden></div>'
        out.append(f'<div class="pd-gallery{" has-3d" if p.get("model") else ""}" data-variant="{vi}" data-srcs="{data}"{" hidden" if vi else ""}>'
                   f'<div class="pd-stage">{main}</div><div class="pd-thumbs">{thumbs}</div></div>')
    return "".join(out)


def _bp_fig(p, lang, key, label, alt, vb_w, vb_h, img_box, dims, delay):
    """Una vista del plano: imagen en línea + cotas SVG (en mm del modelo) + etiquetas HTML posicionadas en %."""
    x0, y0, w, h = img_box
    pct = lambda x, y: f"left:{x / vb_w * 100:.3f}%;top:{y / vb_h * 100:.3f}%"
    base = f'{p["img_dir"]}/bp-{key}'
    widths = (900, 1600) if key == "side" else (500, 900)
    svg, labels = [], []
    for kind, a, b, at, value in dims:
        if kind == "h":   # cota horizontal de x=a a x=b en y=at; extensiones desde la vista
            for x in (a, b):
                svg.append(f'<path class="bp-ext" pathLength="1" d="M{x} {y0 + h - 1} V{at + 5}"/>')
            svg.append(f'<path class="bp-dim" pathLength="1" d="M{a} {at} H{b}"/>')
            svg.append(f'<path class="bp-ah" d="M{a} {at} l7 -2.6 v5.2z M{b} {at} l-7 -2.6 v5.2z"/>')
            labels.append(f'<span class="bp-n" style="{pct((a + b) / 2, at)}" data-to="{value}">{value}</span>')
        else:             # cota vertical de y=a a y=b en x=at
            for y in (a, b):
                start, end = (x0 - 2, at - 5) if at < x0 else (x0 + w + 2, at + 5)
                svg.append(f'<path class="bp-ext" pathLength="1" d="M{start} {y} H{end}"/>')
            svg.append(f'<path class="bp-dim" pathLength="1" d="M{at} {a} V{b}"/>')
            svg.append(f'<path class="bp-ah" d="M{at} {a} l-2.6 7 h5.2z M{at} {b} l-2.6 -7 h5.2z"/>')
            labels.append(f'<span class="bp-n bp-nv" style="{pct(at, (a + b) / 2)}" data-to="{value}">{value}</span>')
    return (f'<figure class="bp-fig bp-{key}" style="--vbw:{vb_w:.2f};--vbh:{vb_h:.2f};--d:{delay}s">'
            f'<div class="bp-draw" style="aspect-ratio:{vb_w:.2f}/{vb_h:.2f}">'
            f'<div class="bp-img" style="{pct(x0, y0)};width:{w / vb_w * 100:.3f}%;height:{h / vb_h * 100:.3f}%">'
            f'<picture><source srcset="{base}-{widths[0]}.webp {widths[0]}w, {base}-{widths[1]}.webp {widths[1]}w" sizes="(max-width:860px) 100vw, 760px" type="image/webp">'
            f'<img src="{base}-{widths[0]}.png" srcset="{base}-{widths[0]}.png {widths[0]}w, {base}-{widths[1]}.png {widths[1]}w" sizes="(max-width:860px) 100vw, 760px" '
            f'alt="{alt}" loading="lazy" decoding="async"></picture><i class="bp-scan" aria-hidden="true"></i></div>'
            f'<svg viewBox="0 0 {vb_w:.2f} {vb_h:.2f}" aria-hidden="true">{"".join(svg)}</svg>{"".join(labels)}</div>'
            f'<figcaption>{label} · mm</figcaption></figure>')


def blueprint(p, lang):
    """Banda tipo plano con cotas que se dibujan al hacer scroll (punto 5)."""
    if not p.get("dims"):
        return ""
    import json, os
    u, d = UI[lang], p[lang]
    meta = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet", p["code"].lower(), "views.json")))
    L, W, H = p["dims"]
    M = 3  # margen (mm) dentro de las imágenes
    sw, sh = meta["side"]["wmm"], meta["side"]["hmm"]
    rw, rh = meta["right"]["wmm"], meta["right"]["hmm"]
    vbh = sh + 42
    side = _bp_fig(p, lang, "side", u["bp_side"], u["bp_alt_side"], 28 + sw + 6, vbh, (28, 0, sw, sh),
                   [("h", 28 + M, 28 + sw - M, sh + 26, L), ("v", M, sh - M, 11, H)], 0)
    rear = _bp_fig(p, lang, "right", u["bp_rear"], u["bp_alt_rear"], rw + 34, vbh, (0, 0, rw, rh),
                   [("h", M, rw - M, rh + 26, W), ("v", M, rh - M, rw + 21, H)], .55)
    stats = "".join(f'<div><b><span class="bp-c" data-to="{v}">{v}</span>{" " + unit if unit else ""}</b><small>{lbl}</small></div>'
                    for (v, unit), lbl in zip(p["bp_stats"], u["bp_stats"]))
    return (f'<section class="pd-bp" aria-labelledby="bp-h"><div class="wrap">'
            f'<div class="sec-head"><div><p class="eyebrow">{u["bp_eyebrow"]}</p><h2 id="bp-h">{u["bp_h2"]}</h2></div><p>{u["bp_p"]}</p></div>'
            f'<div class="bp-views">{side}{rear}</div><div class="bp-stats">{stats}</div></div></section>')


def sheet_card(p, lang):
    """Tarjeta con la vista previa del plano y descarga del PDF."""
    if not p.get("sheet"):
        return ""
    u, slug = UI[lang], p["code"].lower()
    base = f'{p["img_dir"]}/{slug}-ficha-{lang}'
    return (f'<a class="pd-sheet" href="{base}.pdf" download data-goatcounter-click="ficha-{slug}-{lang}">'
            f'<picture><source srcset="{base}-700.webp 700w, {base}-1200.webp 1200w" sizes="(max-width:860px) 100vw, 440px" type="image/webp">'
            f'<img src="{base}-700.jpg" srcset="{base}-700.jpg 700w, {base}-1200.jpg 1200w" sizes="(max-width:860px) 100vw, 440px" '
            f'alt="{u["sheet_alt"]}" width="1200" height="849" loading="lazy" decoding="async"></picture>'
            f'<span class="pd-sheet-t"><b>{u["sheet_k"]}</b><small>{u["sheet_meta"]}</small><em>{u["sheet_cta"]} ↓</em></span></a>')


def variants(p, lang):
    names = p[lang]["variants"]
    return "".join(
        f'<label class="pd-sw"><input type="radio" name="variant" value="{names[k]}" data-key="{k}" data-color="{c}"{" checked" if i == 0 else ""}>'
        f'<i style="--sw:{c}"></i><span>{names[k]}</span></label>'
        for i, (k, c) in enumerate(p["variants"]))


def highlights(p, lang):
    return "".join(f'<article><span class="pd-hn">{i + 1:02d}</span><h3>{h}</h3><p>{t}</p></article>'
                   for i, (h, t) in enumerate(p[lang]["highlights"]))


def specs(p, lang):
    return "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p[lang]["specs"])


def buy_dialog(p, lang):
    u = UI[lang]
    qty = "".join(f'<option value="{q}">{q}</option>' for q in ("1", "2", "3+"))
    return (f'<dialog class="pd-dlg" id="pd-dlg" aria-labelledby="pd-dlg-h">'
            f'<form class="pd-form" action="{FORMSPREE}" method="POST" data-ok="{u["dlg_ok"]}" data-err="{u["dlg_err"]}" data-code="{p["code"]}">'
            f'<button type="button" class="pd-x" data-close aria-label="{u["dlg_close"]}">×</button>'
            f'<p class="pd-dlg-k">{p["code"]} · {u["dlg_k"]}</p><h2 id="pd-dlg-h">{u["dlg_h"]}</h2><p class="pd-dlg-p">{u["dlg_p"]}</p>'
            f'<p class="pd-dlg-v">{p[lang]["name"]} · <b data-variant-out>{p[lang]["variants"][p["variants"][0][0]]}</b></p>'
            f'<div class="pd-fields"><label><span>{u["dlg_email"]}</span><input type="email" name="email" required autocomplete="email" placeholder="{u["dlg_ph"]}"></label>'
            f'<label class="pd-q"><span>{u["dlg_qty"]}</span><select name="quantity">{qty}</select></label></div>'
            f'<input type="hidden" name="variant" value="{p[lang]["variants"][p["variants"][0][0]]}">'
            f'<input type="hidden" name="product" value="{p["code"]} {p[lang]["name"]}">'
            f'<input type="hidden" name="language" value="{lang.upper()}">'
            f'<input type="hidden" name="source" value="Product page · first-batch list">'
            f'<input type="hidden" name="_subject" value="Interés · {p["code"]} · {p[lang]["variants"][p["variants"][0][0]]}">'
            f'<input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">'
            f'<button class="btn" type="submit">{u["dlg_submit"]}</button>'
            f'<p class="pd-msg" role="status" aria-live="polite"></p>'
            f'<p class="f-privacy">{u["dlg_privacy"]}</p></form></dialog>')


def vt(p):
    """Nombre de view-transition de la imagen principal de un producto (morph entre páginas)."""
    return f'view-transition-name:{p["code"].lower()}-img'


def card(p, lang):
    u = UI[lang]
    return (f'<a class="pc" href="{url(p, lang)}"><div class="pc-img" style="{vt(p)}">{picture(p, 0, lang, "(max-width:860px) 100vw, 560px")}'
            f'<span class="pc-code">{p["code"]}</span></div><div class="pc-body">'
            f'<p class="pc-fit">{p[lang]["fit"]}</p><h2>{p[lang]["name"]}</h2><p>{p[lang]["card"]}</p>'
            f'<div class="pc-foot"><span class="pc-price">{price(p)}</span><span class="pc-st">{u["status_batch"]}</span></div>'
            f'<span class="pc-go">{u["cat_view"]} →</span></div></a>')


def card_ow01(lang, moto):
    u = UI[lang]
    return (f'<a class="pc pc-dev" href="#ow-01"><div class="pc-img pc-ill">{moto}<span class="pc-code">OW-01</span></div><div class="pc-body">'
            f'<p class="pc-fit">{"Motos de aventura" if lang == "es" else "Adventure motorcycles"}</p><h2>{u["ow01_name"]}</h2><p>{u["ow01_card"]}</p>'
            f'<div class="pc-foot"><span class="pc-st pc-st-dev">{u["status_dev"]}</span></div>'
            f'<span class="pc-go">{u["ow01_link"]} →</span></div></a>')


def home_feature(p, lang, products_url):
    """Bloque de la tienda en la página de inicio: el producto destacado del catálogo."""
    u, P = UI[lang], p[lang]
    return (f'<section class="h-shop on-dark" aria-labelledby="h-shop-h"><div class="wrap h-shop-grid">'
            f'<a class="h-shop-img" href="{url(p, lang)}" tabindex="-1" aria-hidden="true" style="{vt(p)}">{picture(p, 0, lang, "(max-width:900px) 100vw, 660px")}'
            f'<span class="pc-code">{p["code"]}</span></a>'
            f'<div class="h-shop-info"><p class="eyebrow">{u["home_eyebrow"]}</p><h2 id="h-shop-h">{P["name"]}</h2>'
            f'<p class="h-shop-fit">{P["fit"]}</p><p class="h-shop-tag">{P["tagline"]}</p>'
            f'<div class="h-shop-price"><span>{price(p)}</span><span class="pc-st">{u["status_batch"]}</span></div>'
            f'<div class="ctas"><a class="btn" href="{url(p, lang)}" data-goatcounter-click="inicio-tienda-{p["code"].lower()}">{u["cat_view"]}</a>'
            f'<a class="btn ghost" href="{products_url}">{u["home_all"]}</a></div></div></div></section>')
