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
        # Puntos de información del visor 3D: posición y normal en metros (coordenadas del GLB).
        "hotspots": [("piece", "0.0821 0.1027 0.15", "0.512 0.859 0"),
                     ("slots", "0.1008 0.0599 -0.072", "0.94 0.342 0"),
                     ("mount", "0.1045 0.0106 -0.234", "1 0 0"),
                     ("thick", "0 0.1273 0.2433", "-0.059 0.792 0.608"),
                     ("sign", "0 0.1229 0.185", "0 -1 0")],  # secreto: la firma debajo de la pieza
        "bp_stats": [("4.8", "mm"), ("0.5", "kg"), ("1", ""), ("0", "")],
        # Guía de instalación (preliminar): ilustraciones en src/sheet/<slug>/guide.json + assets guide-*.
        # Orden de apriete en cruz = índices de los tornillos en guide.json (frente izq., medio der., frente der., medio izq.).
        "guide_order": [0, 3, 2, 1],
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
            "variants": {"black": "Obsidiana · negro mate", "white": "Cantera · blanco mate"},
            "alts": ["Tail rack OW-02 en negro mate, vista en tres cuartos",
                     "Tail rack OW-02 visto desde un costado, con las ranuras de amarre",
                     "Tail rack OW-02 visto de frente",
                     "Detalle de la placa superior del OW-02 con el logo grabado y las ranuras redondeadas"],
            "guide": {
                "kit": "Rack OW-02 + 4 tornillos nuevos", "tool": "Llaves Allen",
                "steps": [("Prepara la moto", "Sobre una superficie plana, estable, apagada y con el motor frío."),
                          ("Quita los tornillos de fábrica", "Con una llave Allen, retira los 4 tornillos de los puntos de montaje que Yamaha dejó para un rack: dos en cada costado. Guárdalos por si un día quitas el rack."),
                          ("Presenta el rack", "Colócalo sobre la cola y alinea sus 4 barrenos con los puntos de montaje."),
                          ("Coloca los tornillos nuevos", "Pon los 4 tornillos del kit a mano, sin apretar, para que el rack se acomode solo."),
                          ("Aprieta en cruz", "Sigue el orden 1 → 4 de la figura. Aprieta firme y revisa que no quede juego."),
                          ("Revisa a los 100 km", "Vuelve a revisar el apriete después de los primeros 100 km y de vez en cuando, sobre todo después de terracería.")],
            },
            "hs": {"piece": ("Una sola pieza", "Lámina doblada: sin soldaduras ni uniones."),
                   "slots": ("Ranuras de amarre", "Para straps y bolsas pequeñas. Cantos redondeados en CNC para no cortar las cintas."),
                   "mount": ("Puntos de fábrica", "Se atornilla en los puntos de montaje originales de la T7."),
                   "thick": ("4.8 mm", "Aluminio 6061 de 3/16″. Todo el rack pesa cerca de 0.5 kg."),
                   "sign": ("Firma", "Si llegaste hasta aquí, eres de los nuestros. — M.")},
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
                ("Acabado", "Pintura electrostática en polvo: Obsidiana (negro mate) o Cantera (blanco mate)"),
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
            "variants": {"black": "Obsidian · matte black", "white": "Cantera · matte white"},
            "alts": ["OW-02 tail rack in matte black, three-quarter view",
                     "OW-02 tail rack seen from the side, showing the strap slots",
                     "OW-02 tail rack seen from the front",
                     "Close-up of the OW-02 top plate with the engraved logo and rounded slots"],
            "guide": {
                "kit": "OW-02 rack + 4 new bolts", "tool": "Allen keys",
                "steps": [("Prep the bike", "On flat, stable ground, switched off, with the engine cold."),
                          ("Remove the factory bolts", "With an Allen key, remove the 4 bolts from the mounting points Yamaha left for a rack: two on each side. Keep them in case you ever take the rack off."),
                          ("Offer up the rack", "Set it on the tail and line up its 4 holes with the mounting points."),
                          ("Fit the new bolts", "Thread the 4 kit bolts in by hand, without tightening, so the rack settles on its own."),
                          ("Tighten in a cross pattern", "Follow the 1 → 4 order in the drawing. Tighten firmly and check there’s no play."),
                          ("Check at 100 km", "Re-check the bolts after the first 100 km and every so often, especially after dirt roads.")],
            },
            "hs": {"piece": ("One piece", "Folded sheet: no welds, no joints."),
                   "slots": ("Tie-down slots", "For straps and small bags. CNC-rounded edges so they won’t cut webbing."),
                   "mount": ("Factory mounts", "Bolts to the T7’s original mounting points."),
                   "thick": ("4.8 mm", "3/16″ 6061 aluminum. The whole rack weighs about 0.5 kg."),
                   "sign": ("Signature", "If you made it down here, you’re one of us. — M.")},
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
                ("Finish", "Powder coat: Obsidian (matte black) or Cantera (matte white)"),
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
        g_eyebrow="04 · Instalación", g_h2="Cuatro tornillos", g_p="Se monta en los cuatro puntos que Yamaha dejó en la T7 para un rack. No hay que cortar ni perforar nada.",
        g_kit="Incluye", g_tool="Herramienta", g_pre="Guía preliminar", g_pdf="Descargar guía (PDF)",
        g_fig1="Despiece: 4 tornillos nuevos, 2 por costado", g_fig2="Orden de apriete · vista superior", g_front="Frente",
        g_note="Guía preliminar. El par de apriete y los detalles finales se publicarán con el primer lote.",
        g_alt1="Despiece del OW-02: el rack con sus 4 tornillos separados de los barrenos de montaje", g_alt2="Vista superior del OW-02 con los 4 puntos de montaje numerados en orden de apriete en cruz",
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
        g_eyebrow="04 · Installation", g_h2="Four bolts", g_p="It mounts on the four points Yamaha left on the T7 for a rack. No cutting, no drilling.",
        g_kit="Includes", g_tool="Tools", g_pre="Preliminary guide", g_pdf="Download guide (PDF)",
        g_fig1="Exploded view: 4 new bolts, 2 per side", g_fig2="Tightening order · top view", g_front="Front",
        g_note="Preliminary guide. Torque values and final details will be published with the first batch.",
        g_alt1="Exploded view of the OW-02: the rack with its 4 bolts pulled out of the mounting holes", g_alt2="Top view of the OW-02 with the 4 mounting points numbered in cross-pattern tightening order",
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


def hotspots_json(p, lang):
    import json, html
    hs = [{"k": k, "p": pos, "n": nrm, "t": p[lang]["hs"][k][0], "d": p[lang]["hs"][k][1]} for k, pos, nrm in p.get("hotspots", [])]
    return html.escape(json.dumps(hs, ensure_ascii=False), quote=True)


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
                       f"data-hs='{hotspots_json(p, lang)}' "
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


def _guide_meta(p):
    import json, os
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet", p["code"].lower(), "guide.json")))


def guide_figs(p, lang, src=None):
    """Las dos figuras de la guía. src(nombre) devuelve la URL de la imagen (para el PDF se pasa base64)."""
    u, g = UI[lang], _guide_meta(p)
    base = p["img_dir"]
    def pic(name, alt):
        m = g[name]
        if src:
            return f'<img src="{src(name)}" alt="{alt}" width="{m["w"]}" height="{m["h"]}">'
        return (f'<picture><source srcset="{base}/{name}-800.webp 800w, {base}/{name}-1400.webp 1400w" sizes="(max-width:900px) 100vw, 640px" type="image/webp">'
                f'<img src="{base}/{name}-800.png" srcset="{base}/{name}-800.png 800w, {base}/{name}-1400.png 1400w" sizes="(max-width:900px) 100vw, 640px" '
                f'alt="{alt}" width="{m["w"]}" height="{m["h"]}" loading="lazy" decoding="async"></picture>')
    pts = g["guide-top"]["pts"]; order = p["guide_order"]
    marks, lines = [], []
    for n, i in enumerate(order):
        pt = pts[i]; dv = 0.075 if pt["v"] > .5 else -0.075
        marks.append(f'<span class="gd-n" style="left:{pt["u"] * 100:.2f}%;top:{(pt["v"] + dv) * 100:.2f}%">{n + 1}</span>')
    for a, b in ((0, 1), (2, 3)):
        A, B = pts[order[a]], pts[order[b]]
        lines.append(f'<line x1="{A["u"] * 100:.2f}" y1="{A["v"] * 100:.2f}" x2="{B["u"] * 100:.2f}" y2="{B["v"] * 100:.2f}"/>')
    fig1 = f'<figure class="gd-fig">{pic("guide-explode", u["g_alt1"])}<figcaption>{u["g_fig1"]}</figcaption></figure>'
    fig2 = (f'<figure class="gd-fig gd-top"><div class="gd-top-in">{pic("guide-top", u["g_alt2"])}'
            f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{"".join(lines)}</svg>{"".join(marks)}'
            f'<span class="gd-front">← {u["g_front"]}</span></div><figcaption>{u["g_fig2"]}</figcaption></figure>')
    return fig1, fig2


def guide_steps(p, lang, a, b):
    return "".join(f'<li><span class="gd-sn">{i + 1:02d}</span><div><h3>{h}</h3><p>{t}</p></div></li>'
                   for i, (h, t) in enumerate(p[lang]["guide"]["steps"]) if a <= i < b)


def install_guide(p, lang):
    """Sección '04 · Instalación' de la ficha (punto 5)."""
    if not p.get("guide_order"):
        return ""
    u, gd, slug = UI[lang], p[lang]["guide"], p["code"].lower()
    fig1, fig2 = guide_figs(p, lang)
    pdf = f'{p["img_dir"]}/{slug}-guia-{lang}.pdf'
    return (f'<section class="pd-gd" id="instalacion"><div class="wrap">'
            f'<div class="sec-head"><div><p class="eyebrow">{u["g_eyebrow"]}</p><h2>{u["g_h2"]}</h2></div><p>{u["g_p"]}</p></div>'
            f'<ul class="gd-chips"><li><b>{u["g_kit"]}</b>{gd["kit"]}</li><li><b>{u["g_tool"]}</b>{gd["tool"]}</li><li class="gd-pre">{u["g_pre"]}</li></ul>'
            f'<div class="gd-row">{fig1}<ol class="gd-steps">{guide_steps(p, lang, 0, 4)}</ol></div>'
            f'<div class="gd-row gd-row-b"><ol class="gd-steps" start="5">{guide_steps(p, lang, 4, 6)}</ol>{fig2}</div>'
            f'<div class="gd-foot"><p>{u["g_note"]}</p><a class="btn ghost" href="{pdf}" download data-goatcounter-click="guia-{slug}-{lang}">{u["g_pdf"]} ↓</a></div>'
            f'</div></section>')


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


def _sw_label(name):
    """'Obsidiana · negro mate' → nombre en grande + acabado técnico en chico."""
    a, _, b = name.partition(" · ")
    return f"<b>{a}</b><small>{b}</small>" if b else name


def variants(p, lang):
    names = p[lang]["variants"]
    return "".join(
        f'<label class="pd-sw"><input type="radio" name="variant" value="{names[k]}" data-key="{k}" data-color="{c}"{" checked" if i == 0 else ""}>'
        f'<i style="--sw:{c}"></i><span>{_sw_label(names[k])}</span></label>'
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


def home_card(p, lang):
    """Tarjeta del producto destacado en '¿Qué hacemos?' de la portada (junto a Servicios)."""
    u, P = UI[lang], p[lang]
    return (f'<a class="h-path h-path-prod" href="{url(p, lang)}" data-goatcounter-click="inicio-tienda-{p["code"].lower()}">'
            f'<div class="h-path-img" style="{vt(p)}">{picture(p, 0, lang, "(max-width:1000px) 100vw, 560px")}<span class="pc-code">{p["code"]}</span></div>'
            f'<div><span class="h-code">02 · {u["cat_k"] if "cat_k" in u else ("Productos" if lang == "es" else "Products")}</span>'
            f'<h3 lang="en">Built with heart, ridden hard.</h3><p><b class="h-path-name">{P["name"]}</b> · {P["card"]}</p>'
            f'<p class="h-path-price"><b>{price(p)}</b><span class="pc-st">{u["status_batch"]}</span></p>'
            f'<span class="h-more">{u["cat_view"]} →</span></div></a>')


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


# ---------- En el banco: productos en camino ----------
# Espacios reservados en el catálogo. Cuando un producto tenga ficha, se mueve a PRODUCTS
# (o se le pone "img" a su espacio para mostrar render/boceto antes de tener página).
BENCH = [
    {"code": "OW-03", "nick": "Lucero", "slug": "inreach-holder",
     "es": {"name": "Porta inReach", "fit": "Correa de mochila", "line": "El comunicador satelital a la mano, sin quitarte la mochila."},
     "en": {"name": "inReach holder", "fit": "Backpack strap", "line": "Your satellite messenger within reach, without taking the pack off."}},
    {"code": "OW-04", "nick": "Cuate", "slug": "handlebar-clamp",
     "es": {"name": "Abrazadera de manubrio", "fit": "Manubrio · control DJI + GoPro", "line": "Una sola abrazadera para el control del dron y la cámara."},
     "en": {"name": "Handlebar clamp", "fit": "Handlebar · DJI controller + GoPro", "line": "One clamp for the drone controller and the camera."}},
    {"code": "OW-05", "nick": "Mirador", "slug": "nav-tower-mount",
     "es": {"name": "Montura para torre", "fit": "Torre de navegación · GoPro", "line": "La cámara y el GPS en la barra de navegación, donde los ves."},
     "en": {"name": "Nav tower mount", "fit": "Navigation tower · GoPro", "line": "Camera and GPS on the nav bar, right where you look."}},
    {"code": "OW-06", "nick": "Coyote", "slug": "t7-rally-tower",
     "es": {"name": "Torre rally T7", "fit": "Yamaha Ténéré 700", "line": "Sustituye la pantalla y el faro: cabina tipo rally."},
     "en": {"name": "T7 rally tower", "fit": "Yamaha Ténéré 700", "line": "Replaces the screen and headlight for a rally-style cockpit."}},
    {"code": "OW-07", "nick": "Mula", "slug": "luggage-adapter",
     "es": {"name": "Adaptador de equipaje", "fit": "Equipaje suave", "line": "La base para anclar bolsas de equipaje suave a la moto."},
     "en": {"name": "Luggage adapter", "fit": "Soft luggage", "line": "The base that anchors soft luggage to the bike."}},
    {"code": "OW-08", "nick": "Mecate", "slug": "footpeg-tie-downs",
     "es": {"name": "Amarres en estribos", "fit": "Estribos", "line": "Puntos de amarre firmes para llevar la moto en el remolque."},
     "en": {"name": "Footpeg tie-downs", "fit": "Footpegs", "line": "Solid tie-down points for hauling the bike on a trailer."}},
    {"code": "OW-09", "nick": "Brújula", "slug": "dash-mount",
     "es": {"name": "Montura de tablero", "fit": "Sobre el velocímetro · GPS o celular", "line": "El GPS o el celular sobre el tablero, sin tapar nada."},
     "en": {"name": "Dash mount", "fit": "Over the speedo · GPS or phone", "line": "GPS or phone over the dash, without covering a thing."}},
]

BENCH_UI = {
    "es": {"eyebrow": "Próximamente", "h2": "En el banco", "status": "En el banco", "fig": "Todavía en el cuaderno",
           "lead": "Piezas en las que estamos trabajando. Cada una tendrá su ficha cuando salga del papel.",
           "also": "El equipaje rackless (OW-01) también sigue en el banco.",
           "tm": "Garmin, inReach, DJI, GoPro y Yamaha son marcas de sus respectivos dueños. OcoteWorks no está afiliado a ellas."},
    "en": {"eyebrow": "Coming up", "h2": "On the bench", "status": "On the bench", "fig": "Still in the notebook",
           "lead": "Parts we're working on. Each one gets its own page once it leaves the paper.",
           "also": "The rackless luggage (OW-01) is on the bench too.",
           "tm": "Garmin, inReach, DJI, GoPro and Yamaha are trademarks of their respective owners. OcoteWorks is not affiliated with them."},
}


def bench_slot(b, lang):
    u, B = BENCH_UI[lang], b[lang]
    if b.get("img"):
        vis = f'<img src="{b["img"]}" alt="{b["nick"]} · {B["name"]}" loading="lazy" decoding="async">'
    else:
        vis = '<span class="bn-fig" aria-hidden="true"><i></i></span>'
    return (f'<article class="bn" id="{b["slug"]}"><div class="bn-img">{vis}<span class="pc-code">{b["code"]}</span>'
            f'<span class="bn-sign" lang="en">Coming soon!</span></div>'
            f'<div class="bn-body"><p class="pc-fit">{B["name"]}</p><h3>{b["nick"]}</h3><p>{B["line"]}</p></div></article>')


def bench(lang):
    u = BENCH_UI[lang]
    return (f'<section class="cat-bench" id="{"en-el-banco" if lang == "es" else "on-the-bench"}" aria-labelledby="bench-h"><div class="wrap">'
            f'<div class="sec-head"><p class="eyebrow">{u["eyebrow"]} · {len(BENCH)}</p><h2 id="bench-h">{u["h2"]}</h2>'
            f'<p class="lead">{u["lead"]} <a href="#ow-01">{u["also"]}</a></p></div>'
            f'<div class="bn-grid">{"".join(bench_slot(b, lang) for b in BENCH)}</div>'
            f'<p class="bn-tm">{u["tm"]}</p></div></section>')


# ---------- Fuera del taller: Bitácora de ruta (stickers) ----------
# Idea en exploración (10 nov 2026): lista pero oculta. Cambiar a True para mostrarla en Productos.
ROADLOG_ON = False

ROADLOG_UI = {
    "es": {"eyebrow": "Fuera del taller · OW-S01", "h2": "Bitácora de ruta",
           "lead": "Una serie de stickers de pueblos mágicos de México. Uno por cada pueblo al que llegamos en moto, dibujados con el mismo trazo y numerados como piezas del taller.",
           "use": "Para la maleta, el casco o la caja de herramientas.",
           "slot": "Pueblo", "pending": "Por rodar"},
    "en": {"eyebrow": "Off the bench · OW-S01", "h2": "Road log",
           "lead": "A sticker series of Mexico’s pueblos mágicos. One for every town we ride to, drawn with the same line and numbered like workshop parts.",
           "use": "For the panniers, the helmet or the toolbox.",
           "slot": "Town", "pending": "Not ridden yet"},
}
ROADLOG_SHAPES = ["c", "a", "c", "s", "a", "c"]


def roadlog(lang):
    if not ROADLOG_ON:
        return ""
    u = ROADLOG_UI[lang]
    st = "".join(f'<li class="rl-st rl-{sh}"><span class="rl-cut"><b>{u["slot"]}</b><i>PM·{n:02d}</i><em>{u["pending"]}</em></span></li>'
                 for n, sh in enumerate(ROADLOG_SHAPES, 1))
    return (f'<section class="cat-roadlog" id="{"bitacora-de-ruta" if lang == "es" else "road-log"}" aria-labelledby="rl-h"><div class="wrap rl-grid">'
            f'<div><p class="eyebrow">{u["eyebrow"]}</p><h2 id="rl-h">{u["h2"]}</h2><p class="lead">{u["lead"]}</p><p class="rl-use">{u["use"]}</p></div>'
            f'<div class="rl-sheet"><ul>{st}</ul><span class="bn-sign" lang="en">Coming soon!</span></div></div></section>')
