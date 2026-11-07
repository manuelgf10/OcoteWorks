#!/usr/bin/env python3
"""Genera el sitio bilingüe de OcoteWorks.

    python3 src/build.py

Lee src/page.html + src/styles.css y escribe:
  /index.html      (inglés, versión principal)
  /es/index.html   (español)
  /assets/styles.css
  /sitemap.xml
  /404.html
Para cambiar textos, edita los diccionarios EN y ES de abajo.
"""
import hashlib
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
LASTMOD = "2026-11-07"


def service(icon, code, h3, p, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return (f'<article><span class="code">{code}</span>'
            f'<svg class="ico" aria-hidden="true"><use href="#{icon}"/></svg>'
            f"<h3>{h3}</h3><p>{p}</p><ul>{lis}</ul></article>")


def step(h3, p):
    return f"<li><h3>{h3}</h3><p>{p}</p></li>"


def value(h3, p):
    return f'<li><h3 lang="en">{h3}</h3><p>{p}</p></li>'


def root(dt, dd):
    return f"<dt>{dt}</dt><dd>{dd}</dd>"


EN = dict(
    lang="en", og_locale="en_US", url="https://ocoteworks.com/", home="/",
    cur_en=' aria-current="page"', cur_es="",
    title="OcoteWorks · Design & fabrication workshop · Monterrey, Mexico",
    description="OcoteWorks is an independent design and fabrication workshop in Monterrey, Mexico. We design, engineer and build parts and objects, starting with adventure motorcycles.",
    og_alt="OcoteWorks logo and the tagline Rooted in Mexico. Made to go further.",
    home_label="OcoteWorks, home", nav_label="Main",
    nav_what="What we do", nav_process="Process", nav_workshop="Workshop",
    cta="Start a project", cta2="How we work",
    hero_eyebrow="Design &amp; fabrication · Monterrey, MX",
    hero_h1="Rooted in<br>Mexico.<br><em>Made to go<br>further.</em>",
    hero_lead="OcoteWorks is an independent design and engineering workshop in Monterrey, Mexico. We design, prototype and build parts and objects that get used, starting with adventure motorcycles.",
    cerro_label="Silhouette of Cerro de la Silla, Monterrey", west="W",
    man_eyebrow="Manifesto",
    man_quote="Good ideas should <span>leave the page.</span>",
    man_body="<p>We shape them through design, engineering, and hands-on work.</p><p>We learn by making, testing, and using what we build.</p><p>Rooted in Mexico, made to go further.</p>",
    values="".join([
        value("Design with intent", "Every geometry, material and process has a reason. Nothing is added just to look good."),
        value("Make it real", "An idea isn’t finished until it’s physical. We prototype early, and what leaves the shop is finished properly."),
        value("Prove it in use", "We use what we make before we offer it. No part leaves without time on the bike."),
        value("Go further", "We try new processes and take things where they’re used. One new technique per project."),
    ]),
    photo_alt="A rider on an adventure motorcycle crossing a desert flat at sunset",
    photo_cap="Field testing · Northern Mexico",
    what_eyebrow="Services", what_h2="What we do",
    what_p="We take an idea from sketch to finished part. Hire us for a single stage or the whole development.",
    services="".join([
        service("i-diseno", "OW-DS", "Design", "Parts, accessories and objects designed around how they’re used: form, function and fit.",
                ["Concept &amp; sketches", "3D modeling", "Fabrication drawings"]),
        service("i-ingenieria", "OW-EN", "Engineering", "Making sure the part survives real use: materials, tolerances, calculations and testing before we cut.",
                ["Material selection", "Analysis &amp; validation", "Field testing"]),
        service("i-fabricacion", "OW-FX", "Fabrication", "From prototype to short runs, with local processes and suppliers.",
                ["Functional prototypes", "Short production runs", "Finishing &amp; assembly"]),
    ]),
    proc_eyebrow="Process", proc_h2="How we work",
    proc_p="Every part goes through the same five stages. You always know where your project is and what comes next.",
    steps="".join([
        step("Requirements", "We talk through the problem, how the part is used and where it goes."),
        step("Design", "Sketches and a 3D model to review together before cutting any material."),
        step("Prototype", "A first real part to measure, fit and adjust."),
        step("Test", "We take it out on the trail. Whatever fails gets fixed here."),
        step("Production", "We build the final version, with drawings and a part number."),
    ]),
    shop_eyebrow="The workshop", shop_h2="From Ocotepec to Monterrey",
    shop_body="<p style=\"margin-top:28px\">Ocote is the resin-rich pine splinter used to start a fire in the mountains: small, resourceful and reliable when it counts. That’s where the name comes from, along with Ocotepec, the town where it all began.</p><p>OcoteWorks is run by an industrial designer with an engineer’s mind, shaped by product engineering and the craft of mosaic. We work from Monterrey, with the Cerro de la Silla on the horizon.</p>",
    roots="".join([
        root("Engineering", "Drawings, tolerances and testing. Every part has a number and a revision."),
        root("Design", "Form, color and use, worked out together."),
        root("Craft", "Mosaic taught us to build piece by piece."),
        root("Adventure", "We make what we’d take to the mountains ourselves."),
    ]),
    con_eyebrow="Contact", con_h2="Tell us about your project",
    con_p="Write to us about what you want to build or solve. We’ll reply with questions, a proposal and an estimated timeline.",
    mexico="Mexico", foot_meta="Designed in Monterrey · Made in Mexico",
)

ES = dict(
    lang="es", og_locale="es_MX", url="https://ocoteworks.com/es/", home="/es/",
    cur_en="", cur_es=' aria-current="page"',
    title="OcoteWorks · Taller de diseño y fabricación · Monterrey, México",
    description="OcoteWorks es un taller independiente de diseño y fabricación en Monterrey, México. Diseñamos, desarrollamos y fabricamos piezas y objetos, empezando por la moto de aventura.",
    og_alt="Logo de OcoteWorks y el lema Rooted in Mexico. Made to go further.",
    home_label="OcoteWorks, inicio", nav_label="Principal",
    nav_what="Qué hacemos", nav_process="Proceso", nav_workshop="El taller",
    cta="Cotizar proyecto", cta2="Ver cómo trabajamos",
    hero_eyebrow="Diseño y fabricación · Monterrey, MX",
    hero_h1="<span lang=\"en\">Rooted in<br>Mexico.<br><em>Made to go<br>further.</em></span>",
    hero_lead="OcoteWorks es un taller independiente de diseño e ingeniería en Monterrey. Diseñamos, prototipamos y fabricamos piezas y objetos que se usan de verdad, empezando por la moto de aventura.",
    cerro_label="Silueta del Cerro de la Silla, Monterrey", west="O",
    man_eyebrow="Manifiesto",
    man_quote="Las buenas ideas tienen que <span>salir del papel.</span>",
    man_body="<p>Les damos forma con diseño, ingeniería y trabajo manual.</p><p>Aprendemos haciendo, probando y usando lo que construimos.</p><p>Con raíces en México, hechas para llegar más lejos.</p>",
    values="".join([
        value("Design with intent", "Cada geometría, material y proceso tiene una razón. Nada se agrega solo por verse bien."),
        value("Make it real", "Una idea no está terminada hasta que es física. Se prototipa pronto y lo que sale se termina bien."),
        value("Prove it in use", "Lo que hacemos se usa antes de ofrecerse. Ninguna pieza sale sin rodar en la moto."),
        value("Go further", "Probar procesos nuevos y llevar las cosas a donde se usan. Una técnica nueva por proyecto."),
    ]),
    photo_alt="Motociclista en moto de aventura cruzando una planicie del desierto al atardecer",
    photo_cap="Pruebas en campo · Norte de México",
    what_eyebrow="Servicios", what_h2="Qué hacemos",
    what_p="Llevamos una idea desde el boceto hasta la pieza terminada. Puedes contratarnos para una etapa o para todo el desarrollo.",
    services="".join([
        service("i-diseno", "OW-DS", "Diseño", "Piezas, accesorios y objetos pensados para cómo se usan: forma, función y montaje.",
                ["Concepto y bocetos", "Modelado 3D", "Planos de fabricación"]),
        service("i-ingenieria", "OW-EN", "Ingeniería", "Que la pieza aguante: materiales, tolerancias, cálculo y pruebas antes de fabricar.",
                ["Selección de materiales", "Análisis y validación", "Pruebas en campo"]),
        service("i-fabricacion", "OW-FX", "Fabricación", "Del prototipo a la serie corta, con procesos y proveedores de la región.",
                ["Prototipos funcionales", "Series cortas", "Acabados y ensamble"]),
    ]),
    proc_eyebrow="Proceso", proc_h2="Cómo trabajamos",
    proc_p="Cada pieza pasa por las mismas cinco etapas. Sabes en qué punto va tu proyecto y qué sigue.",
    steps="".join([
        step("Requisitos", "Platicamos del problema, de cómo se usa la pieza y dónde va."),
        step("Diseño", "Bocetos y modelo 3D para revisar juntos antes de cortar material."),
        step("Prototipo", "Una primera pieza real para medir, montar y ajustar."),
        step("Prueba", "La llevamos a terracería. Lo que falla se corrige aquí."),
        step("Producción", "Fabricamos la versión final, con planos y número de pieza."),
    ]),
    shop_eyebrow="El taller", shop_h2="De Ocotepec a Monterrey",
    shop_body="<p style=\"margin-top:28px\">El ocote es la astilla de pino resinoso con la que se prende el fuego en el monte. Es pequeño, ingenioso y confiable cuando hace falta. De ahí viene el nombre, y de Ocotepec, el pueblo donde empezó todo.</p><p>OcoteWorks lo dirige un diseñador industrial con cabeza de ingeniero, formado entre la ingeniería de producto y el oficio del mosaico. Trabajamos desde Monterrey, con el Cerro de la Silla en el horizonte.</p>",
    roots="".join([
        root("Ingeniería", "Planos, tolerancias y pruebas. Cada pieza tiene número y revisión."),
        root("Diseño", "Forma, color y uso pensados juntos, no por separado."),
        root("Oficio", "Del mosaico aprendimos a construir pieza por pieza."),
        root("Aventura", "Hacemos lo que nosotros mismos llevaríamos a la sierra."),
    ]),
    con_eyebrow="Contacto", con_h2="Cuéntanos tu proyecto",
    con_p="Escríbenos qué quieres construir o resolver. Te respondemos con preguntas, una propuesta y un tiempo estimado.",
    mexico="México", foot_meta="Diseñado en Monterrey · Hecho en México",
)


def jsonld(lang, url, description):
    import json
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://ocoteworks.com/#org",
                "name": "OcoteWorks",
                "url": "https://ocoteworks.com/",
                "logo": "https://ocoteworks.com/assets/logo-carbon.png",
                "image": "https://ocoteworks.com/og-image.png",
                "email": "hola@ocoteworks.com",
                "slogan": "Rooted in Mexico. Made to go further.",
                "description": description,
                "address": {"@type": "PostalAddress", "addressLocality": "Monterrey",
                            "addressRegion": "Nuevo León", "addressCountry": "MX"},
                "areaServed": "MX",
                "sameAs": SAME_AS,
                "founder": {
                    "@type": "Person",
                    "name": "Manuel",
                    "jobTitle": "Industrial Designer",
                    "sameAs": FOUNDER_SAME_AS,
                },
            },
            {
                "@type": "WebSite",
                "@id": url + "#website",
                "url": url,
                "name": "OcoteWorks",
                "inLanguage": lang,
                "publisher": {"@id": "https://ocoteworks.com/#org"},
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


# Perfiles públicos de la marca (Instagram, LinkedIn, Behance...). Agregar las URL aquí.
SAME_AS = [
    "https://www.instagram.com/ocote.works/",
]

# Perfiles personales del fundador.
FOUNDER_SAME_AS = [
    "https://www.behance.net/manuelgf",
    "https://www.linkedin.com/in/manuelgarflo",
]


def render(tpl, data):
    out = tpl
    for k, v in data.items():
        out = out.replace("{{" + k + "}}", v)
    assert "{{" not in out, out[out.index("{{"):out.index("{{") + 40]
    return out


def main():
    tpl = open(os.path.join(SRC, "page.html"), encoding="utf-8").read()
    css = open(os.path.join(SRC, "styles.css"), encoding="utf-8").read()
    cerro = open(os.path.join(SRC, "cerro_path.txt"), encoding="utf-8").read().strip()
    version = hashlib.sha1(css.encode()).hexdigest()[:8]

    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "styles.css"), "w", encoding="utf-8").write(css)

    for data, path in [(EN, "index.html"), (ES, os.path.join("es", "index.html"))]:
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        page = render(tpl, dict(data, cerro_path=cerro, version=version,
                                jsonld=jsonld(data["lang"], data["url"], data["description"])))
        open(full, "w", encoding="utf-8").write(page)

    # Página 404 (bilingüe, una sola)
    p404 = open(os.path.join(SRC, "404.html"), encoding="utf-8").read().replace("{{version}}", version)
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(p404)

    alt = ('<xhtml:link rel="alternate" hreflang="en" href="https://ocoteworks.com/"/>'
           '<xhtml:link rel="alternate" hreflang="es" href="https://ocoteworks.com/es/"/>')
    urls = "".join(
        f"  <url><loc>{u}</loc><lastmod>{LASTMOD}</lastmod>{alt}</url>\n"
        for u in ["https://ocoteworks.com/", "https://ocoteworks.com/es/"])
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
    print("ok", version)


if __name__ == "__main__":
    main()
