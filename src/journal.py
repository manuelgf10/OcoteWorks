"""Bitácora / Journal de OcoteWorks.

Cada entrada es una lista de bloques por idioma:
  ("p", texto)            párrafo (admite <b>, <em>, <a>)
  ("h2", texto)           subtítulo
  ("ul", [items])         lista
  ("img", clave, pie)     imagen de assets/journal/<slug>/<clave>-<ancho>.webp|jpg
  ("img2", clave1, clave2, pie)  dos imágenes lado a lado con un pie común
  ("quote", texto)        frase destacada
Para agregar una entrada: copiar el bloque de la primera, exportar fotos a assets/journal/<slug>/ y regenerar.
"""

ENTRIES = [
    {
        "slug": "ow-02-silueta",
        "date": "2026-11-09",
        "category": {"es": "Taller", "en": "Build"},
        "product": "OW-02",
        "cover": "carton-34",
        # clave: (anchos disponibles, ancho, alto)
        "images": {
            "carton-34": ((700, 1200, 1800), 2576, 1680),
            "carton-lado": ((700, 1200, 1800), 2576, 1932),
            "carton-arriba": ((700, 1200, 1800), 2576, 1932),
            "boceto": ((700, 1086), 1086, 1448),
        },
        "es": {
            "title": "Que siga pareciendo dirt bike",
            "dek": "Cómo nació el OW-02: una parrilla trasera para la Ténéré 700 pensada para cargar lo justo sin cambiarle la silueta.",
            "alts": {
                "carton-34": "Prototipo de cartón de la parrilla montado en la cola de una Ténéré 700, vista de tres cuartos",
                "carton-lado": "Prototipo de cartón visto de lado, atornillado en los puntos de fábrica junto al asiento",
                "carton-arriba": "Vista superior del prototipo de cartón siguiendo la forma de la cola de la moto",
                "boceto": "Hoja de cuaderno con bocetos a lápiz de la parrilla y notas de diseño",
            },
            "body": [
                ("p", "La Ténéré 700 tiene algo que me gusta mucho: de lado todavía se lee como una dirt bike grande. Asiento largo y plano, cola alta y delgada, nada que sobre. Se ve hecha para salirse del pavimento."),
                ("p", "El problema empieza cuando quieres cargarla. Casi todas las parrillas traseras que encuentras son anchas, altas y pesadas. Le pones una, luego un top case, y poco a poco la moto deja de parecer lo que es: termina viéndose como una moto que nunca sale del pavimento."),
                ("quote", "Quería lo contrario: una parrilla que casi no se note, pero que esté ahí cuando necesitas amarrar algo."),
                ("h2", "Tres reglas"),
                ("p", "Antes de dibujar me puse tres reglas:"),
                ("ul", ["<b>Respetar la silueta.</b> La parrilla tiene que seguir la línea del asiento y de la cola, no sobresalir de ella.",
                        "<b>Cargar cerca del centro.</b> Mientras más baja y más adelante va la carga, menos se siente en la moto, sobre todo fuera del camino.",
                        "<b>Pesar poco.</b> Si la idea es mantener el carácter de dirt bike, no tiene sentido colgarle kilos de acero."]),
                ("h2", "Primero, el cuaderno"),
                ("p", "Empecé a mano. Me gusta bocetar antes de abrir el CAD porque obliga a pensar en la idea completa y no en los detalles. En esta hoja ya estaba casi todo: una sola lámina doblada, brazos laterales que se atornillan a la moto y una placa trasera con ranuras para pasar straps."),
                ("img", "boceto", "Primeros bocetos. Abajo, las preguntas que quedaban abiertas: patrón de ranuras, posición de barrenos, ángulo y altura, peso."),
                ("p", "Las preguntas al pie de la hoja eran las importantes. Y esas no se contestan en papel."),
                ("h2", "Cartón antes que aluminio"),
                ("p", "Antes de cortar metal, la corté en cartón con láser y la monté en la moto con los tornillos de fábrica. Es una prueba barata y rápida, y contesta cosas que en la pantalla engañan: cómo se ve la proporción contra el asiento, qué tanto se asoma sobre la calavera y si las ranuras quedan donde de verdad van a caer las cintas."),
                ("img", "carton-lado", "Prototipo de cartón cortado en láser, atornillado en los puntos de fábrica."),
                ("img", "carton-arriba", "Desde arriba: la placa sigue la forma de la cola."),
                ("p", "Ver la pieza puesta, aunque sea en cartón, cambia la conversación. Una cosa es un render flotando sobre un fondo gris y otra es la parrilla junto a una moto con polvo en el asiento. De tres cuartos, como en la foto de arriba, la parrilla se pierde en la línea de la moto. Eso era lo que buscaba."),
                ("h2", "Una sola pieza"),
                ("p", "La versión final es una lámina de aluminio 6061 cortada en láser y doblada. Sin soldaduras ni uniones: menos piezas, menos peso y menos lugares por donde algo se pueda aflojar. Las ranuras llevan los cantos redondeados en CNC para que no corten las cintas, y el acabado es pintura electrostática en negro o blanco mate."),
                ("render", "hero", "Render del modelo CAD, versión 1."),
                ("h2", "Lo que sigue"),
                ("p", "El siguiente paso es el prototipo en aluminio y probarlo donde importa: terracería, vibración y lluvia. Antes de fabricar el primer lote quiero saber cuánta gente lo quiere, así que abrí una lista. Si te interesa, apúntate en la <a href=\"{product_url}\">ficha del OW-02</a>: no se cobra nada y te aviso primero."),
                ("p", "Lo iré contando aquí, con los errores incluidos."),
            ],
            "facts": [("Proyecto", "OW-02 Tail Rack T7"), ("Moto", "Yamaha Ténéré 700, 2019–2023"), ("Material", "Aluminio 6061"),
                      ("Proceso", "Corte láser · doblado · cantos CNC"), ("Etapa", "Prototipo de cartón y CAD"), ("Siguiente", "Prototipo en aluminio")],
        },
        "en": {
            "title": "Keep it looking like a dirt bike",
            "dek": "How the OW-02 started: a tail rack for the Ténéré 700 designed to carry just enough without changing its silhouette.",
            "alts": {
                "carton-34": "Cardboard prototype of the rack mounted on the tail of a Ténéré 700, three-quarter view",
                "carton-lado": "Cardboard prototype seen from the side, bolted to the factory mounting points next to the seat",
                "carton-arriba": "Top view of the cardboard prototype following the shape of the bike’s tail",
                "boceto": "Notebook page with pencil sketches of the rack and design notes",
            },
            "body": [
                ("p", "There’s something I really like about the Ténéré 700: from the side it still reads as a big dirt bike. Long flat seat, tall slim tail, nothing extra. It looks made to leave the pavement."),
                ("p", "The trouble starts when you want to carry things. Almost every tail rack out there is wide, tall and heavy. Add one, then a top case, and bit by bit the bike stops looking like what it is: it ends up looking like a bike that never leaves the pavement."),
                ("quote", "I wanted the opposite: a rack you barely notice, but that’s there when you need to strap something down."),
                ("h2", "Three rules"),
                ("p", "Before drawing anything I set myself three rules:"),
                ("ul", ["<b>Respect the silhouette.</b> The rack has to follow the line of the seat and tail, not stick out of it.",
                        "<b>Carry close to the center.</b> The lower and further forward the load sits, the less you feel it, especially off-road.",
                        "<b>Keep it light.</b> If the point is to keep the dirt-bike character, it makes no sense to hang kilos of steel on it."]),
                ("h2", "Notebook first"),
                ("p", "I started by hand. I like sketching before opening CAD because it forces you to think about the whole idea, not the details. Almost everything was already on this page: a single folded sheet, side arms that bolt to the bike and a rear plate with slots for straps."),
                ("img", "boceto", "First sketches. At the bottom, the open questions: slot pattern, hole position, angle and height, weight."),
                ("p", "The questions at the bottom of the page were the important ones. And you can’t answer those on paper."),
                ("h2", "Cardboard before aluminum"),
                ("p", "Before cutting metal, I laser cut it in cardboard and bolted it to the bike with the factory screws. It’s a cheap, fast test, and it answers things a screen gets wrong: how the proportion looks against the seat, how much it shows over the taillight and whether the slots land where the straps will actually go."),
                ("img", "carton-lado", "Laser-cut cardboard prototype, bolted to the factory mounting points."),
                ("img", "carton-arriba", "From above: the plate follows the shape of the tail."),
                ("p", "Seeing the part on the bike, even in cardboard, changes the conversation. A render floating on a grey background is one thing; the rack next to a bike with dust on the seat is another. From three-quarters, like in the photo at the top, the rack disappears into the bike’s line. That’s what I was after."),
                ("h2", "One piece"),
                ("p", "The final version is a single sheet of 6061 aluminum, laser cut and folded. No welds, no joints: fewer parts, less weight and fewer places for something to work loose. The slots get CNC-rounded edges so they won’t cut webbing, and the finish is powder coat in matte black or matte white."),
                ("render", "hero", "Render of the CAD model, version 1."),
                ("h2", "What’s next"),
                ("p", "Next is the aluminum prototype and testing it where it matters: dirt roads, vibration and rain. Before making the first batch I want to know how many people want it, so I opened a list. If you’re interested, sign up on the <a href=\"{product_url}\">OW-02 page</a>: nothing is charged and you’ll hear first."),
                ("p", "I’ll keep posting here, mistakes included."),
            ],
            "facts": [("Project", "OW-02 Tail Rack T7"), ("Bike", "Yamaha Ténéré 700, 2019–2023"), ("Material", "6061 aluminum"),
                      ("Process", "Laser cut · folded · CNC edges"), ("Stage", "Cardboard prototype and CAD"), ("Next", "Aluminum prototype")],
        },
    },
]

UI = {
    "es": dict(
        idx_title="Bitácora · Notas del taller · OcoteWorks",
        idx_description="La Bitácora de OcoteWorks: proceso de diseño, prototipos, pruebas de taller y salidas en moto, contados desde Monterrey.",
        idx_eyebrow="Bitácora · Monterrey, MX",
        idx_h1="Notas <em>del taller</em>",
        idx_lead="Proceso de diseño, prototipos, pruebas y salidas. Lo que funciona y lo que no, con fotos y detalles técnicos.",
        read="min de lectura", read_more="Leer", back="← Toda la bitácora",
        facts="Ficha", cta_product="Ver el OW-02", cta_ig="Síguenos en Instagram",
        months=["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
        by="Por Manuel García",
    ),
    "en": dict(
        idx_title="Journal · Notes from the workshop · OcoteWorks",
        idx_description="The OcoteWorks Journal: design process, prototypes, workshop tests and rides, written from Monterrey, Mexico.",
        idx_eyebrow="Journal · Monterrey, MX",
        idx_h1="Notes <em>from the workshop</em>",
        idx_lead="Design process, prototypes, tests and rides. What works and what doesn’t, with photos and technical details.",
        read="min read", read_more="Read", back="← All entries",
        facts="Facts", cta_product="See the OW-02", cta_ig="Follow on Instagram",
        months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        by="By Manuel García",
    ),
}


def url(e, lang):
    return ("/es/bitacora/" if lang == "es" else "/journal/") + e["slug"] + "/"


def date_txt(e, lang):
    y, m, d = (int(x) for x in e["date"].split("-"))
    mo = UI[lang]["months"][m - 1]
    return f"{d} de {mo} de {y}" if lang == "es" else f"{mo} {d}, {y}"


def minutes(e, lang):
    import re
    words = sum(len(re.sub(r"<[^>]+>", "", b[-1] if b[0] != "ul" else " ".join(b[1])).split()) for b in e[lang]["body"])
    return max(1, round(words / 200))


def picture(e, key, lang, sizes, eager=False):
    widths, W, H = e["images"][key]
    base = f"/assets/journal/{e['slug']}/{key}"
    webp = ", ".join(f"{base}-{w}.webp {w}w" for w in widths)
    jpg = ", ".join(f"{base}-{w}.jpg {w}w" for w in widths)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source srcset="{webp}" sizes="{sizes}" type="image/webp">'
            f'<img src="{base}-{widths[0]}.jpg" srcset="{jpg}" sizes="{sizes}" alt="{e[lang]["alts"][key]}" '
            f'width="{W}" height="{H}" {load} decoding="async"></picture>')


def body(e, lang, product, product_url):
    out = []
    for b in e[lang]["body"]:
        k = b[0]
        if k == "p":
            out.append(f"<p>{b[1].format(product_url=product_url)}</p>")
        elif k == "h2":
            out.append(f"<h2>{b[1]}</h2>")
        elif k == "ul":
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in b[1]) + "</ul>")
        elif k == "quote":
            out.append(f'<blockquote class="j-quote"><p>{b[1]}</p></blockquote>')
        elif k == "img":
            tall = e["images"][b[1]][2] > e["images"][b[1]][1]
            out.append(f'<figure class="j-fig{" j-tall" if tall else ""}">{picture(e, b[1], lang, "(max-width:900px) 100vw, 860px")}'
                       f'<figcaption>{b[2]}</figcaption></figure>')
        elif k == "render":  # render del producto (reutiliza las imágenes de la tienda)
            import products as PR
            i = [n for n, _, _ in product["images"]].index(b[1])
            out.append(f'<figure class="j-fig j-render">{PR.picture(product, i, lang, "(max-width:900px) 100vw, 860px")}'
                       f'<figcaption>{b[2]}</figcaption></figure>')
    return "\n".join(out)


def facts(e, lang):
    return "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in e[lang]["facts"])


def card(e, lang):
    u = UI[lang]
    return (f'<a class="j-card" href="{url(e, lang)}"><div class="j-card-img" style="view-transition-name:j-{e["slug"]}">{picture(e, e["cover"], lang, "(max-width:900px) 100vw, 640px")}</div>'
            f'<div class="j-card-body"><p class="j-meta"><span class="j-cat">{e["category"][lang]}</span>'
            f'<time datetime="{e["date"]}">{date_txt(e, lang)}</time><span>{minutes(e, lang)} {u["read"]}</span></p>'
            f'<h2>{e[lang]["title"]}</h2><p>{e[lang]["dek"]}</p><span class="pc-go">{u["read_more"]} →</span></div></a>')
