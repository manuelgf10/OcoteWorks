#!/usr/bin/env python3
"""Genera el sitio bilingüe de OcoteWorks.

    python3 src/build.py

Plantillas: src/home.html, services.html, soon.html (Productos y Bitácora en construcción),
quote.html, about.html. Cabecera y pie comunes en header() y footer(). Estilos src/styles.css.
Escribe:
  /index.html      (inglés, versión principal)
  /es/index.html   (español)
  /quote/ y /es/cotizar/  (cotizador; precios en src/quote.js)
  /about/ y /es/sobre-mi/ (sobre mí; textos a_* aquí)
  /assets/styles.css
  /sitemap.xml
  /404.html
Para cambiar textos, edita los diccionarios EN y ES de abajo.
"""
import hashlib
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
LASTMOD = "2026-11-08"


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


def plate(rows):
    return "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)


def stats(items):
    return "".join(f"<li><b>{n}</b><span>{t}</span></li>" for n, t in items)


def tl(org, roles, now=False):
    cls = ' class="now"' if now else ""
    rs = "".join(f'<div class="a-r"><span class="a-yr">{y}</span><p class="a-role">{r}</p>' + (f"<p>{t}</p>" if t else "") + "</div>"
                 for y, r, t in roles)
    return f"<li{cls}><h3>{org}</h3><div>{rs}</div></li>"


def tools(groups):
    return "".join(f"<div><h3>{h}</h3><p>{' · '.join(items)}</p></div>" for h, items in groups)


def levels(groups):
    out = ""
    for i, (h, sub, items) in enumerate(groups):
        lis = "".join(f"<li>{x}</li>" for x in items)
        out += f'<div class="a-lv a-lv{i + 1}"><h3>{h}<span>{sub}</span></h3><ul>{lis}</ul></div>'
    return out


def equip(groups):
    return "".join(f"<div><h3>{h}</h3><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div>" for h, items in groups)


def work(items):
    return "".join(f'<article><span class="code">{c}</span><div class="a-ph" aria-hidden="true"></div><h3>{h}</h3><p>{p}</p><span class="a-st">{st}</span></article>'
                   for c, h, p, st in items)


# Fotos de "Sobre mí" en /assets/photos/about/ (cada una en -600 y -1000, .jpg y .webp).
# (nombre base, alt EN, alt ES, pie EN, pie ES). Si la lista está vacía, la tira no aparece.
ABOUT_PHOTOS = [
    ("bike-rebuild", "Manuel rebuilding a motorcycle in front of the workshop tool wall", "Manuel reconstruyendo una moto frente al muro de herramientas del taller", "Rebuild", "Reconstrucción"),
    ("engine-teardown", "A Honda engine and parts laid out on the workbench in front of the tool wall", "Un motor Honda y sus piezas sobre el banco de trabajo, frente al muro de herramientas", "Teardown", "Desarmado"),
    ("mini-restoration", "Manuel next to the open engine bay of a classic Mini", "Manuel junto al motor de un Mini clásico", "Restoration", "Restauración"),
    ("tenere-maintenance", "Manuel servicing his Yamaha Ténéré 700 with the rear wheel off", "Manuel dando servicio a su Yamaha Ténéré 700 sin la rueda trasera", "Maintenance · Ténéré 700", "Mantenimiento · Ténéré 700"),
]


def about_photos(lang):
    if not ABOUT_PHOTOS:
        return ""
    figs = ""
    for b, aen, aes, cen, ces in ABOUT_PHOTOS:
        alt, cap = (aen, cen) if lang == "en" else (aes, ces)
        figs += (f'<figure><picture><source srcset="/assets/photos/about/{b}-400.webp 400w, /assets/photos/about/{b}-600.webp 600w, /assets/photos/about/{b}-1000.webp 1000w" '
                 f'sizes="(max-width:760px) 46vw, 260px" type="image/webp">'
                 f'<img src="/assets/photos/about/{b}-600.jpg" alt="{alt}" width="600" height="600" loading="lazy" decoding="async"></picture>'
                 f'<figcaption>{cap}</figcaption></figure>')
    return f'<div class="wrap a-photos">{figs}</div>'


def about_plate(d):
    return (f'<aside class="a-plate" aria-label="{d["a_plate_label"]}"><div class="a-plate-top"><span>OW · ID-001</span><span>{d["a_plate_tag"]}</span></div>'
            '<div class="a-plate-id"><picture><source srcset="/assets/photos/about/portrait-360.webp 360w, /assets/photos/about/portrait-720.webp 720w" sizes="(max-width:900px) 40vw, 180px" type="image/webp">'
            f'<img src="/assets/photos/about/portrait-360.jpg" srcset="/assets/photos/about/portrait-360.jpg 360w, /assets/photos/about/portrait-720.jpg 720w" sizes="(max-width:900px) 40vw, 180px" alt="{d["a_portrait_alt"]}" width="360" height="480" loading="lazy" decoding="async"></picture>'
            f'<p class="a-plate-name">Manuel García<span>Flores</span></p></div><dl>{d["a_plate"]}</dl>'
            '<div class="a-plate-foot"><span>REV 2026</span><i aria-hidden="true"></i><i aria-hidden="true"></i><i aria-hidden="true"></i></div></aside>')


BACK_NOTE = {"es": ("El taller, de noche. Aquí pasan las cosas que no caben en el día.", "Monterrey, N.L. · después de las 11"),
             "en": ("The workshop, at night. Where the things that don’t fit in the day get done.", "Monterrey, Mexico · after 11 p.m.")}


NAME_BLOCK = {
    "es": dict(k="El nombre", h="¿Por qué Ocote?",
               defs=[("ocote", "o·có·te", "Del náhuatl <i>ocotl</i>. Nombre del pino mexicano resinoso y de su madera, usada tradicionalmente para encender el fuego."),
                     ("Ocotepec", "o·co·te·pec", "Del náhuatl, significa «en el cerro de los ocotes». El pueblo donde nací y crecí.")],
               body=["Crecí en Ocotepec, rodeado de bosques de pino.",
                     "De niño me encantaba andar por el bosque, descubrir caminos nuevos y preguntarme qué habría detrás del siguiente cerro. Ahí empezó mi curiosidad por la naturaleza, la exploración y la aventura.",
                     "Con los años, esa misma curiosidad se convirtió en una pasión por diseñar, construir y crear cosas.",
                     "OcoteWorks es el reflejo de esas raíces. Una conexión entre de dónde vengo, lo que me encanta hacer y las ganas de seguir llegando más lejos."],
               quote="Raíces profundas.<br><em>Fuego por dentro.</em>"),
    "en": dict(k="The name", h="Why Ocote?",
               defs=[("ocote", "o·KO·teh", "From Nahuatl <i>ocotl</i>. A name for resin-rich Mexican pine and its wood, traditionally used to start fires."),
                     ("Ocotepec", "o·ko·teh·PEK", "From Nahuatl, meaning “on the hill of the ocotes.” The town where I was born and raised.")],
               body=["I grew up in Ocotepec, surrounded by pine forests.",
                     "As a kid, I loved wandering through the woods, discovering new paths, and wondering what lay beyond the next hill. That’s where my curiosity for nature, exploration, and adventure began.",
                     "Over the years, that same curiosity grew into a passion for designing, building, and creating things.",
                     "OcoteWorks is a reflection of those roots. A connection between where I come from, what I love doing, and the desire to keep going further."],
               quote="Deep roots.<br><em>An inner fire.</em>"),
}


def about_name(d):
    n = NAME_BLOCK[d["lang"]]
    defs = "".join(f'<div class="an-def"><dt lang="es">{w}<span class="an-ph" aria-hidden="true">/{ph}/</span></dt><dd>{t}</dd></div>' for w, ph, t in n["defs"])
    body = "".join(f"<p>{t}</p>" for t in n["body"])
    return (f'<section class="a-name on-dark" id="{"el-nombre" if d["lang"] == "es" else "the-name"}"><div class="wrap a-name-grid">'
            f'<div><p class="eyebrow">02 · {n["k"]}</p><h2>{n["h"]}</h2><dl class="an-dict">{defs}</dl></div>'
            f'<div class="an-body">{body}<blockquote class="an-quote"><p>{n["quote"]}</p></blockquote>'
            f'<p class="an-sign" lang="en">Rooted in Mexico. Made to go further.</p></div></div></section>')


def about_hero(d):
    back = BACK_NOTE[d["lang"]]
    # Secreto: 5 toques → chispas del esmeril (origen en % de la foto); 5 más → la foto se voltea y trae una nota al reverso.
    return ('<figure class="a-hero-photo" data-sparks="26 55.5"><div class="ah-card"><div class="ah-in"><picture>'
            '<source srcset="/assets/photos/about/workshop-night-800.webp 800w, /assets/photos/about/workshop-night-1400.webp 1400w" sizes="(max-width:900px) 100vw, 480px" type="image/webp">'
            f'<img src="/assets/photos/about/workshop-night-800.jpg" alt="{d["a_hero_alt"]}" width="800" height="1000" fetchpriority="high" decoding="async"></picture>'
            f'<div class="ah-back" aria-hidden="true"><i class="ah-tape"></i><p class="ah-note">{back[0]}</p><p class="ah-sign">— M.</p>'
            f'<p class="ah-meta">{back[1]}</p><span class="ah-stamp">OW<br><small>FIELD LOG<br>002</small></span></div></div></div>'
            f'<figcaption><span>{d["a_hero_cap"]}</span><span>OW · Field log 002</span></figcaption></figure>')


def tags(items):
    return "".join(f"<li><b>{c}</b>{t}</li>" for c, t in items)


EN = dict(
    lang="en", og_locale="en_US", url="https://ocoteworks.com/", home="/",
    cur_en=' aria-current="page"', cur_es="",
    title="OcoteWorks · Design & fabrication workshop · Monterrey, Mexico",
    description="OcoteWorks is an independent design and fabrication workshop in Monterrey, Mexico. We design, engineer and build parts and objects, starting with adventure motorcycles.",
    og_alt="OcoteWorks logo and the tagline Rooted in Mexico. Made to go further.",
    home_label="OcoteWorks, home", nav_label="Main",
    nav_what="What we do", nav_process="Process", nav_workshop="Workshop", menu_label="Menu",
    cta="Start a project", cta2="How we work",
    hero_eyebrow="Design &amp; fabrication · Monterrey, MX",
    hero_h1="Rooted in<br>Mexico.<br><em>Made to go<br>further.</em>",
    hero_lead="OcoteWorks is an independent design and engineering workshop in Monterrey, Mexico. We design, prototype and build parts and objects that get used, starting with adventure motorcycles.",
    cerro_label="Silhouette of Cerro de la Silla, Monterrey", west="W",
    hero_photo_alt="A rider on an adventure motorcycle crossing the salt flats of Viesca, Coahuila, with mountains in the distance",
    hero_photo_cap="Salt flats · Viesca, Coahuila",
    man_eyebrow="Manifesto",
    man_quote="Good ideas should <span>leave the page.</span>",
    man_body="<p>We shape them through design, engineering, and hands-on work.</p><p>We learn by making, testing, and using what we build.</p><p>Rooted in Mexico, made to go further.</p>",
    values="".join([
        value("Design with intent", "Every geometry, material and process has a reason. Nothing is added just to look good."),
        value("Make it real", "An idea isn’t finished until it’s physical. We prototype early, and what leaves the shop is finished properly."),
        value("Prove it in use", "We use what we make before we offer it. No part leaves without time on the bike."),
        value("Go further", "We try new processes and take things where they’re used. One new technique per project."),
    ]),
    photo_alt="A rider on an adventure motorcycle crossing the desert near Mina, Nuevo León, at sunset",
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
    quote_href="/quote/", con_quote="Build your quote",
    # cotizador
    q_url="https://ocoteworks.com/quote/",
    q_title="Build your project · Quote builder · OcoteWorks",
    q_description="Configure your product project with OcoteWorks: design, prototypes, brand, packaging, instructions and short production runs. Get a ballpark estimate in MXN in two minutes.",
    q_nav_cta="Send project",
    q_eyebrow="Project builder · Ballpark estimate",
    q_h1="Build your <em>project</em>",
    q_h1_plain="Project builder",
    q_lead="From idea to a product ready to sell. Choose what your project needs and get a ballpark estimate and timeline in two minutes. Most creators come for the part and discover they also need the box, the instructions and a first batch. Plan it all here.",
    q_tags_label="What we can do for you",
    q_tags=tags([("OW-DS", "Design"), ("OW-PT", "Prototypes"), ("OW-BR", "Brand"), ("OW-PK", "Packaging"), ("OW-DC", "Instructions &amp; print"), ("OW-MF", "Short runs")]),
    q_noscript="The project builder needs JavaScript. Write to us and we’ll put together your estimate:",
    q_send_h="Send it to the workshop",
    q_send_p="We receive your full configuration. We reply within two business days with questions and a proposal.",
    q_name="Name", q_email="Email", q_projname="Project or brand", q_projph="Optional",
    q_notes="Tell us about it", q_notesph="What it is, who it’s for, deadlines, references…",
    q_submit="Send my project",
    q_sheet="Project sheet", q_ref="Ref.", q_total="Estimated investment", q_vat="MXN · before VAT",
    q_time="Time to launch", q_review="Send this project", q_copy="Copy summary",
    q_disclaimer="Ballpark ranges for planning. We confirm the price with a scoped proposal after reviewing your project.",
    q_bar="Estimate", q_bar_cta="View sheet",
    # sobre mí (textos de /about/)
    nav_about="About", about_href="/about/",
    a_url="https://ocoteworks.com/about/",
    a_title="About Manuel García Flores · Industrial designer & product development engineer · OcoteWorks",
    a_description="Manuel García Flores is an industrial designer and product development engineer in Monterrey, Mexico, and the founder of OcoteWorks. Design, engineering, prototyping, manufacturing and testing.",
    a_eyebrow="About", a_plate_label="Profile summary", a_plate_tag="Founder", a_portrait_alt="Portrait of Manuel García Flores, founder of OcoteWorks",
    a_hero_alt="The OcoteWorks workshop at night: Manuel at the workbench with sparks flying, next to a motorcycle and a classic Mini",
    a_hero_cap="The workshop after dark",
    a_off_alt="Manuel crossing a river on his Yamaha Ténéré 700, with green hills behind",
    a_off_cap="Field log · River crossing on the Ténéré 700",
    a_h1="Designer by training.<br><em>Engineer by habit.</em>",
    a_lead="<p>I’m Manuel García Flores, an industrial designer and product development engineer in Monterrey, Mexico, and the founder of OcoteWorks.</p>"
           "<p>I care about the whole life of a product: how it’s designed, fabricated, assembled, tested and, finally, used. Most of my week is spent between CAD and the machines that turn it into parts.</p>",
    a_cta="See my experience", a_cta2="Get in touch",
    a_plate=plate([("Role", "Product Development Engineer · Laboratory Manager"), ("Independent", "Founder, OcoteWorks"),
                   ("Base", "Monterrey, N.L., Mexico"), ("Origin", "Ocotepec"),
                   ("Education", "Industrial Design, Universidad Iberoamericana, 2015–2020"),
                   ("Product dev.", "Since 2020"), ("Ride", "Yamaha Ténéré 700")]),
    a_stats_label="Key facts",
    a_stats=stats([("2020", "In professional product development since"), ("ISO 13485", "Quality-governed development environment"),
                   ("2 roles", "Design engineering and lab management, in parallel"), ("CAD → CNC", "From the model to the machine")]),
    a_story_eyebrow="Professional background", a_story_h2="From design to how things are made",
    a_story="<p>I trained as an industrial designer at the Universidad Iberoamericana. Over time my work kept moving toward the same question: not only what a product should be, but how it gets made.</p>"
            "<p>My first industrial job, in 2015 at Mosaicos Venecianos, put me next to lathes, milling machines and equipment maintenance. At IKTA, from 2019 to 2020, I worked on steel structures and decorative architectural elements, moving between CAD, CAM and visualization.</p>"
            "<p>Since 2020 I’ve developed medical devices at Bioana, in an ISO 13485 environment where decisions are documented and parts have to be made reliably. Since 2022 I also manage the prototyping lab. Designing the parts and running the equipment that makes them has taught me more about manufacturability than either role would alone.</p>"
            "<p>OcoteWorks is my independent workshop, where that background meets motorcycles, mechanical systems and the outdoors. It is not an extension of Bioana, and it isn’t a medical device company.</p>",
    a_cv_eyebrow="Experience", a_cv_h2="Experience",
    a_cv_p="A compact timeline. Client work at Bioana is confidential, so it’s described by type of work, not by project.",
    a_timeline="".join([
        tl("OcoteWorks", [("Now", "Founder · Independent design &amp; fabrication",
                           "Original products, motorcycle components and custom hardware, from prototype to small batch. Product development for other creators.")], True),
        tl("Bioana", [("2020 – now", "Product Development Engineer",
                       "Medical device development: requirements turned into engineering solutions, mechanical components, assemblies, fixtures and tooling, CAD models, production drawings and BOMs, functional prototypes, DFM/DFA and support for verification testing. Also packaging, labeling and internal development processes."),
                      ("2022 – now", "Laboratory Manager",
                       "Technical operation of the prototyping lab: equipment documentation and operating instructions, preventive maintenance and calibration, installation and troubleshooting, new fabrication capabilities and hands-on support for R&amp;D.")], True),
        tl("IKTA", [("2019 – 2020", "Industrial design", "Steel structures and decorative architectural elements. CAD/CAM and visualization.")]),
        tl("Universidad Iberoamericana", [("2015 – 2020", "B.A. Industrial Design", "")]),
        tl("Mosaicos Venecianos", [("2015", "Early industrial experience", "Industrial equipment maintenance and conventional machining on lathes and mills.")]),
    ]),
    a_award_k="Recognition",
    a_award="<b>Best project in the Medical Equipment category</b> and <b>overall winner</b> across all categories at the fifth edition of Mexico’s national design award, which covers product, digital, spatial, visual communication and fashion design.",
    a_award_alt="Manuel holding the Diseña México 2020 trophy and diploma in front of the award’s exhibition wall",
    a_caps_eyebrow="What I do", a_caps_h2="Five disciplines, one process",
    a_caps_p="These usually sit in different departments. Working across all of them is what gets a design ready to be made.",
    a_caps=service("i-diseno", "01", "Design", "Industrial and mechanical design: concept, form, use and fit, resolved in 3D.",
                   ["Industrial design", "Mechanical design", "3D CAD &amp; assemblies"])
           + service("i-ingenieria", "02", "Engineering", "Requirements turned into parts that can be made, assembled and checked.",
                     ["GD&amp;T &amp; tolerancing", "DFM / DFA", "Material &amp; process selection"])
           + service("i-prototipo", "03", "Prototyping", "Physical parts early, to measure, fit and break.",
                     ["SLA &amp; FDM printing", "CNC routing &amp; milling", "Fixtures &amp; tooling"])
           + service("i-fabricacion", "04", "Manufacturing", "Designing with the process in mind, from one-offs to small batches.",
                     ["Process selection", "Drawings &amp; BOMs", "Small-batch fabrication"])
           + service("i-prueba", "05", "Testing", "Evidence before production: verification, measurement and real use.",
                     ["Verification support", "Force &amp; dimensional checks", "Field testing"]),
    a_tools_eyebrow="Tools &amp; technologies", a_tools_h2="Tools &amp; technologies",
    a_tools_p="Grouped by what they’re for. Levels separate what I do with my own hands from what I know from working alongside it.",
    a_tools=tools([("Design &amp; engineering", ["Industrial design", "Mechanical design", "3D CAD", "Assemblies &amp; drawings", "GD&amp;T", "DFM / DFA", "Material selection", "Engineering documentation"]),
                   ("CAD · CAM", ["SolidWorks", "Fusion 360", "Fusion 360 CAM"]),
                   ("Graphics &amp; documentation", ["Illustrator", "Photoshop", "InDesign"])]),
    a_methods_h="Fabrication methods",
    a_methods=levels([("Hands-on", "I run these myself", ["SLA printing", "FDM printing", "CNC routing", "CNC milling", "Laser cutting", "Silicone molding", "Prototype assembly", "Fixtures &amp; tooling"]),
                      ("Process knowledge", "Worked alongside, designed for", ["Conventional machining", "Injection molding", "Thermoforming", "Ultrasonic welding", "Laser welding", "Packaging &amp; sealing"])]),
    a_equip_h="Equipment experience",
    a_equip=equip([("CNC · Machining", ["Tormach 1100MX", "Avid CNC Benchtop Pro", "Conventional mills &amp; lathes"]),
                   ("Additive", ["Formlabs Form 3B+", "Formlabs Form 2", "Creality FDM"]),
                   ("Fabrication · Processing", ["LaserMex CO₂ laser", "Boy XS injection molder", "Sisma LMD-180 laser welder", "Ultrasonic welding", "Thermoforming &amp; packaging machinery"]),
                   ("Testing · Measurement", ["Mark-10 force systems", "Calipers &amp; micrometers", "Dimensional inspection tools"])]),
    a_equip_note="Equipment I’ve operated or worked with in professional labs. It belongs to those labs, not to OcoteWorks.",
    a_work_eyebrow="Selected work", a_work_h2="Selected work",
    a_work_p="Case studies are on their way: drawings, fabricated parts, mechanisms and prototypes, documented from sketch to finished part. Professional client work stays confidential.",
    a_work=work([("OW-01", "Rackless motorcycle luggage", "Machined hardware, leather and textile, with Mexican craftsmanship.", "In development"),
                 ("OW-02", "Workshop fixtures &amp; tooling", "Jigs and fixtures built to make the workshop work better.", "In preparation"),
                 ("OW-03", "Prototypes &amp; mechanisms", "Functional prototypes and mechanical studies.", "In preparation")]),
    a_off_eyebrow="Beyond the workshop", a_off_h2="Prove it in use",
    a_off_p="Motorcycles, travel, photography and mechanical restoration are where most of my ideas start. A few days on a Yamaha Ténéré 700 in northern Mexico show quickly what breaks, what’s missing and what’s worth making. OcoteWorks builds on that: products designed by someone who uses them.",
    a_con_h2="Let’s build something",
    a_con_p="For product development, collaborations or technical questions, write to me. For a ballpark on a project, use the quote builder.",
)

ES = dict(
    lang="es", og_locale="es_MX", url="https://ocoteworks.com/es/", home="/es/",
    cur_en="", cur_es=' aria-current="page"',
    title="OcoteWorks · Taller de diseño y fabricación · Monterrey, México",
    description="OcoteWorks es un taller independiente de diseño y fabricación en Monterrey, México. Diseñamos, desarrollamos y fabricamos piezas y objetos, empezando por la moto de aventura.",
    og_alt="Logo de OcoteWorks y el lema Rooted in Mexico. Made to go further.",
    home_label="OcoteWorks, inicio", nav_label="Principal",
    nav_what="Qué hacemos", nav_process="Proceso", nav_workshop="El taller", menu_label="Menú",
    cta="Cotizar proyecto", cta2="Ver cómo trabajamos",
    hero_eyebrow="Diseño y fabricación · Monterrey, MX",
    hero_h1="<span lang=\"en\">Rooted in<br>Mexico.<br><em>Made to go<br>further.</em></span>",
    hero_lead="OcoteWorks es un taller independiente de diseño e ingeniería en Monterrey. Diseñamos, prototipamos y fabricamos piezas y objetos que se usan de verdad, empezando por la moto de aventura.",
    cerro_label="Silueta del Cerro de la Silla, Monterrey", west="O",
    hero_photo_alt="Motociclista en moto de aventura cruzando las salinas de Viesca, Coahuila, con la sierra al fondo",
    hero_photo_cap="Salinas · Viesca, Coahuila",
    man_eyebrow="Manifiesto",
    man_quote="Las buenas ideas tienen que <span>salir del papel.</span>",
    man_body="<p>Les damos forma con diseño, ingeniería y trabajo manual.</p><p>Aprendemos haciendo, probando y usando lo que construimos.</p><p>Con raíces en México, hechas para llegar más lejos.</p>",
    values="".join([
        value("Design with intent", "Cada geometría, material y proceso tiene una razón. Nada se agrega solo por verse bien."),
        value("Make it real", "Una idea no está terminada hasta que es física. Se prototipa pronto y lo que sale se termina bien."),
        value("Prove it in use", "Lo que hacemos se usa antes de ofrecerse. Ninguna pieza sale sin rodar en la moto."),
        value("Go further", "Probar procesos nuevos y llevar las cosas a donde se usan. Una técnica nueva por proyecto."),
    ]),
    photo_alt="Motociclista en moto de aventura cruzando el desierto de Mina, Nuevo León, al atardecer",
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
    quote_href="/es/cotizar/", con_quote="Arma tu cotización",
    # cotizador
    q_url="https://ocoteworks.com/es/cotizar/",
    q_title="Arma tu proyecto · Cotizador · OcoteWorks",
    q_description="Configura tu proyecto de producto con OcoteWorks: diseño, prototipos, marca, empaque, instructivos y series cortas. Obtén una estimación en pesos en dos minutos.",
    q_nav_cta="Enviar proyecto",
    q_eyebrow="Cotizador · Estimación de referencia",
    q_h1="Arma tu <em>proyecto</em>",
    q_h1_plain="Cotizador de proyecto",
    q_lead="De la idea a un producto listo para vender. Elige lo que necesita tu proyecto y obtén una estimación de costo y tiempo en dos minutos. Casi todos llegan por la pieza y descubren que también hace falta la caja, el instructivo y un primer lote. Plánealo todo aquí.",
    q_tags_label="Lo que podemos hacer por ti",
    q_tags=tags([("OW-DS", "Diseño"), ("OW-PT", "Prototipos"), ("OW-BR", "Marca"), ("OW-PK", "Empaque"), ("OW-DC", "Instructivos e impresos"), ("OW-MF", "Series cortas")]),
    q_noscript="El cotizador necesita JavaScript. Escríbenos y armamos tu estimación:",
    q_send_h="Mándalo al taller",
    q_send_p="Recibimos tu configuración completa. Te respondemos en dos días hábiles con preguntas y una propuesta.",
    q_name="Nombre", q_email="Correo", q_projname="Proyecto o marca", q_projph="Opcional",
    q_notes="Cuéntanos más", q_notesph="Qué es, para quién, fechas, referencias…",
    q_submit="Enviar mi proyecto",
    q_sheet="Hoja de proyecto", q_ref="Ref.", q_total="Inversión estimada", q_vat="MXN · más IVA",
    q_time="Tiempo al lanzamiento", q_review="Enviar este proyecto", q_copy="Copiar resumen",
    q_disclaimer="Rangos de referencia para planear. Confirmamos el precio con una propuesta formal después de revisar tu proyecto.",
    q_bar="Estimación", q_bar_cta="Ver hoja",
    # sobre mí (textos de /es/sobre-mi/)
    nav_about="Sobre mí", about_href="/es/sobre-mi/",
    a_url="https://ocoteworks.com/es/sobre-mi/",
    a_title="Sobre Manuel García Flores · Diseñador industrial e ingeniero de producto · OcoteWorks",
    a_description="Manuel García Flores es diseñador industrial e ingeniero de desarrollo de producto en Monterrey y fundador de OcoteWorks. Diseño, ingeniería, prototipos, manufactura y pruebas.",
    a_eyebrow="Sobre mí", a_plate_label="Resumen de perfil", a_plate_tag="Fundador", a_portrait_alt="Retrato de Manuel García Flores, fundador de OcoteWorks",
    a_hero_alt="El taller de OcoteWorks de noche: Manuel en el banco de trabajo entre chispas, junto a una moto y un Mini clásico",
    a_hero_cap="El taller de noche",
    a_off_alt="Manuel cruzando un río en su Yamaha Ténéré 700, con cerros verdes al fondo",
    a_off_cap="Bitácora · Cruce de río en la Ténéré 700",
    a_h1="Diseñador de formación.<br><em>Ingeniero por convicción.</em>",
    a_lead="<p>Soy Manuel García Flores, diseñador industrial e ingeniero de desarrollo de producto en Monterrey, y fundador de OcoteWorks.</p>"
           "<p>Me importa la vida completa de un producto: cómo se diseña, se fabrica, se ensambla, se prueba y, al final, se usa. Paso casi toda la semana entre el CAD y las máquinas que lo convierten en piezas.</p>",
    a_cta="Ver experiencia", a_cta2="Contacto",
    a_plate=plate([("Rol", "Ingeniero de Desarrollo de Producto · Responsable de Laboratorio"), ("Independiente", "Fundador, OcoteWorks"),
                   ("Base", "Monterrey, N.L., México"), ("Origen", "Ocotepec"),
                   ("Estudios", "Diseño Industrial, Universidad Iberoamericana, 2015–2020"),
                   ("Desarrollo", "Desde 2020"), ("Moto", "Yamaha Ténéré 700")]),
    a_stats_label="Datos clave",
    a_stats=stats([("2020", "En desarrollo de producto profesional desde"), ("ISO 13485", "Entorno de desarrollo con sistema de calidad"),
                   ("2 roles", "Ingeniería de diseño y gestión de laboratorio, en paralelo"), ("CAD → CNC", "Del modelo a la máquina")]),
    a_story_eyebrow="Trayectoria profesional", a_story_h2="Del diseño a cómo se fabrican las cosas",
    a_story="<p>Me formé como diseñador industrial en la Universidad Iberoamericana. Con el tiempo, mi trabajo se fue moviendo hacia la misma pregunta: no solo qué debe ser un producto, sino cómo se fabrica.</p>"
            "<p>Mi primer trabajo industrial, en 2015 en Mosaicos Venecianos, me puso junto a tornos, fresadoras y mantenimiento de equipo. En IKTA, de 2019 a 2020, trabajé en estructuras de acero y elementos arquitectónicos decorativos, entre CAD, CAM y visualización.</p>"
            "<p>Desde 2020 desarrollo dispositivos médicos en Bioana, en un entorno ISO 13485 donde las decisiones se documentan y las piezas tienen que fabricarse de forma confiable. Desde 2022 además soy responsable del laboratorio de prototipos. Diseñar las piezas y operar el equipo que las fabrica me ha enseñado más sobre manufacturabilidad que cualquiera de los dos roles por separado.</p>"
            "<p>OcoteWorks es mi taller independiente, donde esa experiencia se junta con las motos, los sistemas mecánicos y el campo. No es una extensión de Bioana ni una empresa de dispositivos médicos.</p>",
    a_cv_eyebrow="Experiencia", a_cv_h2="Experiencia",
    a_cv_p="Una línea de tiempo breve. El trabajo para clientes en Bioana es confidencial, así que lo describo por tipo de trabajo, no por proyecto.",
    a_timeline="".join([
        tl("OcoteWorks", [("Hoy", "Fundador · Diseño y fabricación independiente",
                           "Productos propios, componentes para moto y herrajes a la medida, del prototipo a la serie corta. Desarrollo de producto para otros creadores.")], True),
        tl("Bioana", [("2020 – hoy", "Ingeniero de Desarrollo de Producto",
                       "Desarrollo de dispositivos médicos: requisitos convertidos en soluciones de ingeniería, componentes mecánicos, ensambles, fixtures y herramentales, modelos CAD, planos de producción y BOMs, prototipos funcionales, DFM/DFA y apoyo a pruebas de verificación. También empaque, etiquetado y procesos internos de desarrollo."),
                      ("2022 – hoy", "Responsable de Laboratorio",
                       "Operación técnica del laboratorio de prototipos: documentación e instructivos de equipo, mantenimiento preventivo y calibración, instalación y solución de fallas, nuevas capacidades de fabricación y apoyo directo a I+D.")], True),
        tl("IKTA", [("2019 – 2020", "Diseño industrial", "Estructuras de acero y elementos arquitectónicos decorativos. CAD/CAM y visualización.")]),
        tl("Universidad Iberoamericana", [("2015 – 2020", "Licenciatura en Diseño Industrial", "")]),
        tl("Mosaicos Venecianos", [("2015", "Primera experiencia industrial", "Mantenimiento de equipo industrial y maquinado convencional en torno y fresadora.")]),
    ]),
    a_award_k="Reconocimiento",
    a_award="<b>Mejor proyecto en la categoría de Equipo Médico</b> y <b>ganador absoluto</b> entre todas las categorías en la quinta edición del premio nacional de diseño, que abarca diseño de producto, digital, de espacios, comunicación visual y moda.",
    a_award_alt="Manuel con el trofeo y el diploma de Diseña México 2020 frente al muro de la exposición del premio",
    a_caps_eyebrow="Lo que hago", a_caps_h2="Cinco disciplinas, un proceso",
    a_caps_p="Normalmente viven en departamentos distintos. Trabajar en todas es lo que deja un diseño listo para fabricarse.",
    a_caps=service("i-diseno", "01", "Diseño", "Diseño industrial y mecánico: concepto, forma, uso y ajuste, resueltos en 3D.",
                   ["Diseño industrial", "Diseño mecánico", "CAD 3D y ensambles"])
           + service("i-ingenieria", "02", "Ingeniería", "Requisitos convertidos en piezas que se pueden fabricar, ensamblar y verificar.",
                     ["GD&amp;T y tolerancias", "DFM / DFA", "Selección de materiales y procesos"])
           + service("i-prototipo", "03", "Prototipos", "Piezas físicas desde temprano, para medir, montar y romper.",
                     ["Impresión SLA y FDM", "Ruteo y fresado CNC", "Fixtures y herramentales"])
           + service("i-fabricacion", "04", "Manufactura", "Diseñar pensando en el proceso, de la pieza única a la serie corta.",
                     ["Selección de procesos", "Planos y BOMs", "Fabricación en serie corta"])
           + service("i-prueba", "05", "Pruebas", "Evidencia antes de producir: verificación, medición y uso real.",
                     ["Apoyo a verificación", "Fuerza y dimensional", "Pruebas en campo"]),
    a_tools_eyebrow="Herramientas y tecnologías", a_tools_h2="Herramientas y tecnologías",
    a_tools_p="Agrupadas por para qué sirven. Los niveles separan lo que hago con mis propias manos de lo que conozco por trabajar junto a ello.",
    a_tools=tools([("Diseño e ingeniería", ["Diseño industrial", "Diseño mecánico", "CAD 3D", "Ensambles y planos", "GD&amp;T", "DFM / DFA", "Selección de materiales", "Documentación de ingeniería"]),
                   ("CAD · CAM", ["SolidWorks", "Fusion 360", "Fusion 360 CAM"]),
                   ("Gráficos y documentación", ["Illustrator", "Photoshop", "InDesign"])]),
    a_methods_h="Métodos de fabricación",
    a_methods=levels([("Práctica directa", "Los opero yo", ["Impresión SLA", "Impresión FDM", "Ruteo CNC", "Fresado CNC", "Corte láser", "Moldeo en silicón", "Ensamble de prototipos", "Fixtures y herramentales"]),
                      ("Conocimiento de proceso", "He trabajado junto a ellos y diseñado para ellos", ["Maquinado convencional", "Moldeo por inyección", "Termoformado", "Soldadura ultrasónica", "Soldadura láser", "Empaque y sellado"])]),
    a_equip_h="Experiencia con equipo",
    a_equip=equip([("CNC · Maquinado", ["Tormach 1100MX", "Avid CNC Benchtop Pro", "Fresadoras y tornos convencionales"]),
                   ("Aditiva", ["Formlabs Form 3B+", "Formlabs Form 2", "Creality FDM"]),
                   ("Fabricación · Procesos", ["Láser CO₂ LaserMex", "Inyectora Boy XS", "Soldadora láser Sisma LMD-180", "Soldadura ultrasónica", "Termoformado y maquinaria de empaque"]),
                   ("Pruebas · Medición", ["Sistemas de fuerza Mark-10", "Calibradores y micrómetros", "Inspección dimensional"])]),
    a_equip_note="Equipo que he operado o con el que he trabajado en laboratorios profesionales. Pertenece a esos laboratorios, no a OcoteWorks.",
    a_work_eyebrow="Trabajo seleccionado", a_work_h2="Trabajo seleccionado",
    a_work_p="Los casos de estudio vienen en camino: planos, piezas fabricadas, mecanismos y prototipos, documentados del boceto a la pieza terminada. El trabajo profesional para clientes se mantiene confidencial.",
    a_work=work([("OW-01", "Equipaje rackless para moto", "Herrajes maquinados, cuero y textil, con oficio mexicano.", "En desarrollo"),
                 ("OW-02", "Fixtures y herramentales de taller", "Plantillas y dispositivos hechos para que el taller trabaje mejor.", "En preparación"),
                 ("OW-03", "Prototipos y mecanismos", "Prototipos funcionales y estudios mecánicos.", "En preparación")]),
    a_off_eyebrow="Más allá del taller", a_off_h2="Prove it in use",
    a_off_p="Las motos, los viajes, la fotografía y la restauración mecánica son donde empiezan casi todas mis ideas. Unos días en una Yamaha Ténéré 700 por el norte de México enseñan rápido qué se rompe, qué falta y qué vale la pena hacer. OcoteWorks parte de ahí: productos diseñados por alguien que los usa.",
    a_con_h2="Construyamos algo",
    a_con_p="Para desarrollo de producto, colaboraciones o preguntas técnicas, escríbeme. Para una estimación de tu proyecto, usa el cotizador.",
)

EN_NEW = dict(
    nav_services="Services", nav_products="Products", nav_journal="Journal",
    u_home="/", u_services="/services/", u_products="/products/", u_journal="/journal/",
    foot_nav="Site",
    # inicio
    h_claim="Independent design, engineering and fabrication workshop in Monterrey, Mexico.",
    h_lead="We develop products for other creators and build our own, starting with gear for adventure motorcycles.",
    h_cta_services="Engineering services", h_cta_products="Our products",
    h_paths_h="Two ways to work with us", h_do_eyebrow="What we do", h_j_eyebrow="From the Journal",
    h_film_eyebrow="OW · Film 001", h_film_h2="From sketch to the road.",
    h_film_p="Twenty seconds of what we do: we draw it, we cut it, we bend it, we ride it.",
    h_film_play="Play", h_film_alt="OcoteWorks short film: desert riding, machining, welding and the logo sketched by hand",
    hero_video_alt="Adventure motorcycles crossing desert roads and dirt tracks in northern Mexico",
    h_p1_h="Design. Prototype. Fabricate.",
    h_p1_p="Product development for creators and brands: design, engineering, prototypes, packaging and short production runs.",
    h_p1_more="Explore services",
    h_p2_h="Original parts and gear.",
    h_p2_p="Products we design, build and test ourselves. The first one, a tail rack for the Ténéré 700, is getting its first batch ready.",
    h_p2_more="Visit the shop",
    h_man="We shape ideas through design, engineering and hands-on work, and we learn by making, testing and using what we build.",
    h_work_h2="Built, tested, documented.",
    h_work_p="Projects from the workshop, documented from sketch to finished part.",
    h_work_link="Read the Journal",
    h_maker_eyebrow="The maker",
    h_maker_alt="Manuel working on a motorcycle in the OcoteWorks workshop",
    h_maker_p="OcoteWorks is run by Manuel García Flores, industrial designer and product development engineer. Since 2020 he has developed medical devices and run a prototyping lab. Here he puts that discipline into his own products, and into yours.",
    h_maker_cta="About Manuel",
    h_award="<b>Overall winner</b> · Premio Nacional de Diseño: Diseña México 2020",
    h_con_h2="Have something in mind?",
    h_con_p="Tell us what you want to build. Get a ballpark with the quote builder, or just write to us.",
    # servicios
    s_url="https://ocoteworks.com/services/",
    s_title="Services · Design, engineering, prototyping & fabrication · OcoteWorks",
    s_description="Product development in Monterrey, Mexico: industrial design, engineering, prototypes, short production runs, packaging and instructions. Hire OcoteWorks for one stage or the whole project.",
    s_eyebrow="Services · Monterrey, MX",
    s_h1="Design. Prototype.<br><em>Fabricate.</em>",
    s_lead="From a sketch to a finished part. Hire us for a single stage or the whole development, from the first concept to a short production run with its box and instructions.",
    s_cta1="Build your quote", s_cta2="Write to us",
    s_what_eyebrow="What we do", s_what_h2="Four disciplines, one workshop",
    s_what_p="Each one can be hired on its own. Together they take a product from idea to a part you can sell.",
    s_cards=service("i-diseno", "OW-DS", "Design", "Parts, accessories and objects designed around how they’re used: form, function and fit.",
                    ["Concept &amp; sketches", "3D CAD &amp; assemblies", "Fabrication drawings"])
            + service("i-ingenieria", "OW-EN", "Engineering", "Making sure the part survives real use: materials, tolerances and testing before we cut.",
                      ["GD&amp;T &amp; tolerances", "DFM / DFA", "Material &amp; process selection"])
            + service("i-prototipo", "OW-PT", "Prototyping", "Real parts early, to measure, fit and adjust before committing.",
                      ["3D printing (SLA / FDM)", "Machined prototypes", "Fixtures &amp; tooling"])
            + service("i-fabricacion", "OW-FX", "Fabrication", "From prototype to short runs, with local processes and suppliers.",
                      ["Short production runs", "Finishing &amp; assembly", "Supplier management"]),
    s_launch_k="Launch", s_launch_h="Beyond the part",
    s_launch_p="Everything a product needs to reach a customer. Add it to your project in the quote builder.",
    s_launch_items="".join(f"<li>{x}</li>" for x in ["Brand", "Packaging &amp; labels", "Illustrated instructions", "Brochures &amp; data sheets", "Product renders"]),
    s_caps_eyebrow="Capabilities", s_caps_h2="How things get made",
    s_caps_p="What happens in our workshop and what we produce with regional suppliers. Professional experience with lab equipment is listed on the About page.",
    s_caps_link="See full experience",
    s_caps=levels([("In the workshop", "Hands-on", ["Design &amp; CAD", "FDM 3D printing", "Woodworking &amp; routing", "Metal cutting &amp; welding", "Mechanical assembly", "Field testing"]),
                   ("With regional suppliers", "Managed by us", ["CNC machining", "Laser cutting", "Sheet metal", "Anodizing &amp; coatings", "Injection molding", "Printing &amp; packaging"])]),
    s_start_eyebrow="Start a project", s_start_h2="Two ways to start",
    s_start_p="Use whichever fits. Both reach the same workshop, and we reply within two business days.",
    s_o1_h="Quote builder", s_o1_p="Pick the services you need and get a ballpark cost and timeline in two minutes.",
    s_o2_h="Write to us", s_o2_p="Prefer to explain it yourself? Send a description, sketches, photos or references.",
    # próximamente
    so_cap="Work in progress",
    pr_url="https://ocoteworks.com/products/",
    pr_title="Products · Building in progress · OcoteWorks",
    pr_description="Original OcoteWorks products are on the bench. The first one is a rackless luggage system for adventure motorcycles.",
    pr_eyebrow="Products",
    pr_lead="Our first product, a rackless luggage system for adventure motorcycles, is on the bench: machined hardware, leather and textile. We’d rather show it finished and tested than rush it.",
    pr_tag="OW-01 · Rackless luggage · In development",
    pr_cta1="Notify me", pr_cta2="Follow on Instagram",
    pr_form_label="Your email", pr_form_ph="you@email.com", pr_form_note="Just one email when OW-01 is ready. No spam.",
    pr_form_ok="You’re on the list. We’ll write when OW-01 is ready.", pr_form_err="Something went wrong. Please write to hola@ocoteworks.com.",
    pr_mail_subject="Products: notify me",
    jo_url="https://ocoteworks.com/journal/",
    jo_title="Journal · Building in progress · OcoteWorks",
    jo_description="The OcoteWorks Journal: field notes, prototypes, CNC tests, materials and trips. First entries coming soon.",
    jo_eyebrow="Journal",
    jo_lead="Field notes, prototypes, CNC tests, materials and trips. The first entries are being written, with photos and technical details.",
    jo_tag="Field log · First entries coming soon",
    jo_cta1="Follow on Instagram", jo_cta2="About the workshop",
)

ES_NEW = dict(
    nav_services="Servicios", nav_products="Productos", nav_journal="Bitácora",
    u_home="/es/", u_services="/es/servicios/", u_products="/es/productos/", u_journal="/es/bitacora/",
    foot_nav="Sitio",
    h_claim="Taller independiente de diseño, ingeniería y fabricación en Monterrey, México.",
    h_lead="Desarrollamos productos para otros creadores y fabricamos los nuestros, empezando por equipo para motos de aventura.",
    h_cta_services="Servicios de ingeniería", h_cta_products="Nuestros productos",
    h_paths_h="Dos formas de trabajar con nosotros", h_do_eyebrow="Qué hacemos", h_j_eyebrow="De la Bitácora",
    h_film_eyebrow="OW · Film 001", h_film_h2="Del boceto a la ruta.",
    h_film_p="Veinte segundos de lo que hacemos: lo dibujamos, lo cortamos, lo doblamos, lo rodamos.",
    h_film_play="Reproducir", h_film_alt="Cortometraje de OcoteWorks: rodadas en el desierto, maquinado, soldadura y el logo dibujado a mano",
    hero_video_alt="Motos de aventura cruzando carreteras y terracerías del desierto en el norte de México",
    h_p1_h="Diseñar. Prototipar. Fabricar.",
    h_p1_p="Desarrollo de producto para creadores y marcas: diseño, ingeniería, prototipos, empaque y series cortas.",
    h_p1_more="Ver servicios",
    h_p2_h="Piezas y equipo propios.",
    h_p2_p="Productos que diseñamos, fabricamos y probamos nosotros. El primero, una parrilla trasera para la Ténéré 700, prepara su primer lote.",
    h_p2_more="Ver la tienda",
    h_man="Les damos forma con diseño, ingeniería y trabajo manual, y aprendemos haciendo, probando y usando lo que construimos.",
    h_work_h2="Hecho, probado, documentado.",
    h_work_p="Proyectos del taller, documentados del boceto a la pieza terminada.",
    h_work_link="Leer la Bitácora",
    h_maker_eyebrow="Quién lo hace",
    h_maker_alt="Manuel trabajando en una moto en el taller de OcoteWorks",
    h_maker_p="OcoteWorks lo dirige Manuel García Flores, diseñador industrial e ingeniero de desarrollo de producto. Desde 2020 desarrolla dispositivos médicos y dirige un laboratorio de prototipos. Aquí pone esa disciplina en sus propios productos, y en los tuyos.",
    h_maker_cta="Sobre Manuel",
    h_award="<b>Ganador absoluto</b> · Premio Nacional de Diseño: Diseña México 2020",
    h_con_h2="¿Tienes algo en mente?",
    h_con_p="Cuéntanos qué quieres construir. Obtén una estimación con el cotizador o escríbenos directo.",
    s_url="https://ocoteworks.com/es/servicios/",
    s_title="Servicios · Diseño, ingeniería, prototipos y fabricación · OcoteWorks",
    s_description="Desarrollo de producto en Monterrey: diseño industrial, ingeniería, prototipos, series cortas, empaque e instructivos. Contrata a OcoteWorks para una etapa o para todo el proyecto.",
    s_eyebrow="Servicios · Monterrey, MX",
    s_h1="Diseñar. Prototipar.<br><em>Fabricar.</em>",
    s_lead="Del boceto a la pieza terminada. Contrátanos para una etapa o para todo el desarrollo, del primer concepto a una serie corta con su caja y su instructivo.",
    s_cta1="Arma tu cotización", s_cta2="Escríbenos",
    s_what_eyebrow="Qué hacemos", s_what_h2="Cuatro disciplinas, un taller",
    s_what_p="Cada una se puede contratar por separado. Juntas llevan un producto de la idea a una pieza que puedes vender.",
    s_cards=service("i-diseno", "OW-DS", "Diseño", "Piezas, accesorios y objetos pensados para cómo se usan: forma, función y montaje.",
                    ["Concepto y bocetos", "CAD 3D y ensambles", "Planos de fabricación"])
            + service("i-ingenieria", "OW-EN", "Ingeniería", "Que la pieza aguante el uso real: materiales, tolerancias y pruebas antes de fabricar.",
                      ["GD&amp;T y tolerancias", "DFM / DFA", "Selección de materiales y procesos"])
            + service("i-prototipo", "OW-PT", "Prototipos", "Piezas reales desde temprano, para medir, montar y ajustar antes de comprometerse.",
                      ["Impresión 3D (SLA / FDM)", "Prototipos maquinados", "Fixtures y herramentales"])
            + service("i-fabricacion", "OW-FX", "Fabricación", "Del prototipo a la serie corta, con procesos y proveedores de la región.",
                      ["Series cortas", "Acabados y ensamble", "Gestión de proveedores"]),
    s_launch_k="Lanzamiento", s_launch_h="Más allá de la pieza",
    s_launch_p="Todo lo que necesita un producto para llegar al cliente. Agrégalo a tu proyecto en el cotizador.",
    s_launch_items="".join(f"<li>{x}</li>" for x in ["Marca", "Empaque y etiquetas", "Instructivos ilustrados", "Brochures y fichas técnicas", "Renders de producto"]),
    s_caps_eyebrow="Capacidades", s_caps_h2="Cómo se fabrica",
    s_caps_p="Lo que se hace en nuestro taller y lo que producimos con proveedores de la región. La experiencia profesional con equipo de laboratorio está en la página Sobre mí.",
    s_caps_link="Ver experiencia completa",
    s_caps=levels([("En el taller", "Práctica directa", ["Diseño y CAD", "Impresión 3D FDM", "Carpintería y ruteo", "Corte y soldadura de metal", "Ensamble mecánico", "Pruebas en campo"]),
                   ("Con proveedores de la región", "Gestionado por nosotros", ["Maquinado CNC", "Corte láser", "Lámina", "Anodizado y recubrimientos", "Moldeo por inyección", "Impresión y empaque"])]),
    s_start_eyebrow="Empieza un proyecto", s_start_h2="Dos formas de empezar",
    s_start_p="Usa la que te acomode. Las dos llegan al mismo taller y respondemos en dos días hábiles.",
    s_o1_h="Cotizador", s_o1_p="Elige los servicios que necesitas y obtén una estimación de costo y tiempo en dos minutos.",
    s_o2_h="Escríbenos", s_o2_p="¿Prefieres explicarlo tú? Mándanos una descripción, bocetos, fotos o referencias.",
    so_cap="Trabajo en proceso",
    pr_url="https://ocoteworks.com/es/productos/",
    pr_title="Productos · En construcción · OcoteWorks",
    pr_description="Los productos propios de OcoteWorks están en el banco de trabajo. El primero es un sistema de equipaje rackless para motos de aventura.",
    pr_eyebrow="Productos",
    pr_lead="Nuestro primer producto, un sistema de equipaje rackless para motos de aventura, está en el banco de trabajo: herrajes maquinados, cuero y textil. Preferimos enseñarlo terminado y probado que apresurarlo.",
    pr_tag="OW-01 · Equipaje rackless · En desarrollo",
    pr_cta1="Avísame", pr_cta2="Síguenos en Instagram",
    pr_form_label="Tu correo", pr_form_ph="tu@correo.com", pr_form_note="Un solo correo cuando OW-01 esté listo. Sin spam.",
    pr_form_ok="Ya estás en la lista. Te escribimos cuando OW-01 esté listo.", pr_form_err="Algo falló. Escríbenos a hola@ocoteworks.com.",
    pr_mail_subject="Productos: avísame",
    jo_url="https://ocoteworks.com/es/bitacora/",
    jo_title="Bitácora · En construcción · OcoteWorks",
    jo_description="La Bitácora de OcoteWorks: notas de campo, prototipos, pruebas CNC, materiales y viajes. Primeras entradas muy pronto.",
    jo_eyebrow="Bitácora",
    jo_lead="Notas de campo, prototipos, pruebas CNC, materiales y viajes. Las primeras entradas se están escribiendo, con fotos y detalles técnicos.",
    jo_tag="Bitácora · Primeras entradas muy pronto",
    jo_cta1="Síguenos en Instagram", jo_cta2="Conoce el taller",
)

EN.update(EN_NEW)
ES.update(ES_NEW)


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


def person_jsonld(d):
    import json
    return json.dumps({
        "@context": "https://schema.org", "@type": "ProfilePage", "url": d["a_url"], "inLanguage": d["lang"],
        "mainEntity": {"@type": "Person", "name": "Manuel García Flores", "jobTitle": "Product Development Engineer",
                       "address": {"@type": "PostalAddress", "addressLocality": "Monterrey", "addressRegion": "Nuevo León", "addressCountry": "MX"},
                       "alumniOf": {"@type": "CollegeOrUniversity", "name": "Universidad Iberoamericana"},
                       "award": "Premio Nacional de Diseño: Diseña México 2020 — Best project, Medical Equipment category; overall winner",
                       "knowsAbout": ["Industrial design", "Product development", "CAD", "CNC machining", "Prototyping", "DFM/DFA"],
                       "worksFor": {"@id": "https://ocoteworks.com/#org"}, "sameAs": FOUNDER_SAME_AS},
    }, ensure_ascii=False, separators=(",", ":"))


# Perfiles públicos de la marca (Instagram, LinkedIn, Behance...). Agregar las URL aquí.
SAME_AS = [
    "https://www.instagram.com/ocote.works/",
]

# Perfiles personales del fundador.
FOUNDER_SAME_AS = [
    "https://www.behance.net/manuelgf",
    "https://www.linkedin.com/in/manuelgarflo",
]


NAV = [("services", "nav_services", "u_services"), ("products", "nav_products", "u_products"),
       ("about", "nav_about", "about_href"), ("journal", "nav_journal", "u_journal")]


# Franja superior: coordenadas del taller (izq.) y hora local de Monterrey en vivo (der.).
STATUS_UI = {"es": ("25° 41′ 03.7″ N, 100° 19′ 02.0″ O", "Monterrey, N.L.", "Hora local en Monterrey"),
             "en": ("25° 41′ 03.7″ N, 100° 19′ 02.0″ W", "Monterrey, Mexico", "Local time in Monterrey")}


def status_bar(d, active=""):
    coords, city, lbl = STATUS_UI[d["lang"]]
    clock = f'<span class="st-time" aria-label="{lbl}"><time class="st-clock" data-tz="America/Monterrey">--:--</time><span class="st-tz">&nbsp;CST</span></span>'
    left = (f'<span class="st-k"><i class="st-dot" aria-hidden="true"></i>{coords}<span class="st-sep st-city">·</span>'
            f'<span class="st-city">{city}</span>')
    if active == "quote":  # en el cotizador: la máquina arranca con tu proyecto
        return (f'<div class="status st-cnc" role="note"><div class="wrap">{left}<span class="st-sep">·</span>{clock}</span>'
                f'<span class="st-con" lang="en"><span class="st-cs">Cycle start</span><span class="st-feed"> · PRG OW-Q · Feed 100%</span>'
                f' · <span class="st-sp">Spindle on</span></span></div></div>')
    return f'<div class="status" role="note"><div class="wrap">{left}</span>{clock}</div></div>'


def header(d, active, en_url, es_url):
    """Cabecera común: logo, secciones, menú de celular, idioma y botón de cotizar."""
    cur = ' aria-current="page"'
    secs = "".join(f'<a class="sec" href="{d[u]}"{cur if k == active else ""}>{d[t]}</a>' for k, t, u in NAV)
    lis = "".join(f'<li><a href="{d[u]}">{d[t]}</a></li>' for k, t, u in NAV) + f'<li><a href="{d["quote_href"]}">{d["cta"]}</a></li>'
    menu = (f'<details class="m-menu"><summary aria-label="{d["menu_label"]}"><span></span><span></span><span></span></summary>'
            f'<ul>{lis}</ul></details>')
    en_cur, es_cur = (cur, "") if d["lang"] == "en" else ("", cur)
    lang = (f'<span class="lang"><a href="{en_url}" hreflang="en" lang="en"{en_cur}>ENG</a><span>/</span>'
            f'<a href="{es_url}" hreflang="es" lang="es"{es_cur}>ESP</a></span>')
    return (status_bar(d, active) + f'<header class="top"><div class="wrap">'
            f'<a class="brand" href="{d["u_home"]}" aria-label="{d["home_label"]}"><picture><source srcset="/assets/logo-carbon-176.webp" type="image/webp">'
            f'<img src="/assets/logo-carbon-176.png" alt="OcoteWorks" width="88" height="63"></picture></a>'
            f'<nav class="nav" aria-label="{d["nav_label"]}">{secs}{menu}{lang}<a class="btn" href="{d["quote_href"]}">{d["cta"]}</a></nav>'
            f'</div></header>')


FOOT_UI = {"es": dict(site="Sitio", product="Producto", legal="Legal", guide="Guía de instalación OW-02", sheet="Ficha técnica OW-02 (PDF)",
                      quote="Cotizar proyecto", place="Monterrey, N.L., México"),
           "en": dict(site="Site", product="Product", legal="Legal", guide="OW-02 installation guide", sheet="OW-02 spec sheet (PDF)",
                      quote="Start a project", place="Monterrey, N.L., Mexico")}


SILLA_PATH = "M275.11,236.51l-9.18-7.01c-6.61-5.05-10.44-9.27-12.04-17.82l-2.57-13.77c-0.49-2.64-0.93-5.48-2.35-7.76 c-1.7-2.74-2.8-5.32-3.04-8.6c-0.22-3.04-0.53-6.01-1.44-9.2c-3.09,4.83-5.72,9.81-7.39,15.14c-0.8,2.55-1.68,4.5-3.57,6.38 c-2.87,2.86-6.33,4.41-9.77,6.6c-16.6,10.58-32.31,22.17-47.84,34.25l-8.75,6.81l-56.16-0.01l25.98-14.42l12-6.61l13.87-17.61 l6.05-7.3l-2.21,7.49c-0.71,2.42-1.94,4.75-2.18,7.34c-0.5,5.42-0.01,10.85,0.95,16.18c0.34,1.9,0.86,3.61,2.02,5.3l8.05-4.78 c0.84-0.5,1.51-1.1,2.05-2.04c-2.53-3.53-4.18-7.45-5.41-11.65c-0.54-1.83-1.3-3.45-1.39-5.49c3.39,2.35,4.44,6.13,8.59,8.15 c0.5,0.24,1.05,0.15,1.5-0.06c0.46-0.21,0.66-0.74,0.77-1.32c0.58-3.07-0.18-5.71-0.99-8.57c-1.29-4.54-2.56-8.9-4.66-13.13 c-0.51-1.04-0.79-2.11-0.89-3.29c1.26,1.03,2.28,2.15,3.23,3.49l7.7,10.86l4.97,6.56c0.97,1.29,2.04,2.2,3.62,3.19 c2.55-2.18,5.35-4.32,7.06-7.28l6.47-11.28l2.28-3.4c0.55-0.82-0.21-1.98-1.16-2.32c-3.12-1.13-5.82-2.64-8.36-4.88 c-4.02-3.55-7.87-7.08-12.21-10.27l-3.69-2.24c-0.99-0.6-2.02-0.2-2.97,0.37l-10.32,6.28c-3.59,2.18-7.33,3.73-10.81,6.12 c-3.68,2.53-6.71,5.58-10.2,8.37l-10.95,8.74c-2.76,2.21-8.44,2.44-12.2,4.46c-5.81,3.13-10.95,7-15.87,11.39 c-3.34,2.98-6.66,5.52-10.49,7.84c-5.92,3.58-11.36,4.17-15.69,6.57l-16.66,9.23L58,241.44l18.64-11.67l71.85-44.35l31.22-18.26 c2.46-1.44,5.98-1.7,8.21-0.15l16.62,11.53l7.87,5.67c6.51,4.69,16.39-1.77,21.31-7.89l7.04-8.73c0.97-1.21,2.34-2.3,3.9-2.53 c2.63-0.39,5,1.46,5.5,3.93l1.13,5.62l1.41,7.01c0.3,1.52,1.34,2.76,3.01,2.91c1.96,0.17,3.72-1,4.58-2.79l4.46-9.33 c0.7-1.46,1.89-2.83,3.52-3.24c2.46-0.61,4.99,0.62,6.34,2.68l5.13,7.81c2.56,3.9,5.36,4.76,9.66,3.35 c2.6-0.85,5.14-1.04,7.75-0.2c6.95,2.23,15.11,7.44,20.91,12.02l7.78,7.15c3.79,3.49,7.34,6.82,11.51,9.94l38.95,29.15 c0.58,0.15,0.3,0.7-0.14,0.47l-9.84-0.03l-15.38-11.7l-17.21-13.75l-15.31-13.95c-4.31-3.93-7.79-7.65-13.64-9.19 c-3.73-0.99-6.8-2.79-10.14-5.1l4.9,14.83l2.77,7.13c0.96,2.47,2.84,4.39,4.57,6.38l2.62,3.02c0.15,0.17,0.45,0.25,0.59,0.23 c1.76-0.28-2.9-12.88-2.38-17.05c0.79,0.56,1.49,1.17,1.99,2.01c1.92,3.23,3.86,6.42,5.17,9.97c0.84,2.27,1.38,4.49,2.98,6.37 l9.94,11.73l11.05,9.05l-32.13,0.05c-2.61-2.9-4.45-5.97-6.52-9.12l-5.11-6.41c-0.4-0.5-0.84-0.94-0.86-1.62l9.45,5.4l5.2,2.7 l5.28,2.62c2.24,1.11,4.46,2.18,7.07,2.21c0.09-1.1-0.52-1.91-1.3-2.69l-20.51-20.52c-3.74-3.74-6.75-7.76-9.39-12.32 c-2.09-3.6-4.55-6.74-7.67-9.51c-1.23-1.09-2.14-2.33-3.06-3.71l-5.53-8.24l-3.77-4.8c-0.41,4.99,0,9.65,0.38,14.45 c0.24,3.02-0.18,5.69-1.2,8.53l-2.31,6.42c-1.07,2.98-0.95,6.17,0.63,9.26c3.1-4.86,6.27-9.34,9.74-13.94 c2.24,2.07,2.39,4.63,2.23,7.35l-0.75,12.81c-0.15,2.53,1.02,4.6,2.69,6.33c2.72,2.83,5.64,5.23,8.91,7.42l6.92,4.63 c1.78,1.19,3.62,1.91,5.55,2.72l-21.99,0.03L275.11,236.51z M202.25,233.6c4.65,0.09,8.7,1.42,12.79,3.15c2.52,1.06,5.69,0.39,7.82-1.14c0.84-0.61,0.4-2-0.03-2.71 l-5.99-9.76c-0.74-1.2-1.22-2.57-1.4-3.92c-0.38-2.96,3.5-1.95,4.63-4.44c1.36-3.02,2.54-6.04,4.6-8.64 c0.5-0.64,1.01-1.3,1.9-1.46l2.07,6.93c0.79,2.65,4.25,5.82,5.29,5.06c0.14-0.1,0.4-0.42,0.35-0.77l-1.93-13.69 c1.32,0.83,1.87,2.04,2.42,3.29l3.41,7.82c1,2.3,1.92,4.44,3.4,6.5c2.39,3.32,4.89,6.46,7.81,9.34l5.15,5.08l-14.15-1.08 c-1.35-0.1-2.51-0.45-3.85-0.78c1.67,3.07,3.95,5.14,6.31,7.27c0.66,0.6,1.41,1.11,1.82,1.9l-64.1-0.04l15.56-6.78 C198.1,234.05,199.97,233.47,202.25,233.6 M105.33,241.54l-24.67-0.06l9.51-2.88l10.12-2.32c4.74-1.08,8.88-3.43,12.6-6.54 c0.47-0.4,1.02-0.73,1.81-0.65C113.44,235.08,110.94,238.81,105.33,241.54 M362.09,241.45l-16.64,0.09l-0.96-1.9c-2.18-2.73-4.12-5.52-5.64-8.73c0.95-0.3,1.66,0.07,2.34,0.48 l6.51,3.9C352.2,237.99,357.04,239.46,362.09,241.45 M248.27,212.08c0.46,1.37,1.09,2.5,0.76,3.98c-3.23-3.96-5.96-8.28-6.8-13.68 C245.23,204.8,247.01,208.33,248.27,212.08"


def silla_svg():
    """Cerro de la Silla (dibujo de Manuel) sobre el borde del pie. El sol/luna se mueve con la hora de Monterrey (motion.js)."""
    return ('<svg class="f-silla" viewBox="58 132 318.62 109.59" aria-hidden="true" focusable="false">'
            '<g class="f-sky" transform="translate(222 149)"><circle class="f-sun" r="6"/>'
            '<path class="f-moon" d="M3-5.2A6 6 0 1 0 3 5.2A6 6 0 0 1 3-5.2Z"/></g>'
            f'<path d="{SILLA_PATH}"/></svg>')


def footer(d):
    """Pie en columnas: marca · sitio · producto (guía y ficha) · legal; abajo © y redes."""
    lang = d["lang"]; f = FOOT_UI[lang]; p = PR.PRODUCTS[0]; slug = p["code"].lower()
    site = "".join(f'<li><a href="{d[u]}">{d[t]}</a></li>' for k, t, u in NAV) + f'<li><a href="{d["quote_href"]}">{f["quote"]}</a></li>'
    prod = (f'<li><a href="{PR.url(p, lang)}#instalacion">{f["guide"]}</a></li>'
            f'<li><a href="{p["img_dir"]}/{slug}-ficha-{lang}.pdf" download data-goatcounter-click="ficha-{slug}-{lang}-pie">{f["sheet"]}</a></li>')
    priv = "/es/privacidad/" if lang == "es" else "/privacy/"
    return (f'<footer><div class="wrap f-silla-wrap">{silla_svg()}</div><div class="wrap f-grid">'
            f'<div class="f-brand"><picture><source srcset="/assets/logo-marfil-256.webp" type="image/webp"><img src="/assets/logo-marfil-256.png" alt="OcoteWorks" width="128" height="91" loading="lazy"></picture>'
            f'<p class="lema" lang="en">Rooted in Mexico.<br><span>Made to go further.</span></p>'
            f'<p class="f-contact">{f["place"]}<br><a href="mailto:hola@ocoteworks.com">hola@ocoteworks.com</a></p></div>'
            f'<nav class="f-col" aria-label="{f["site"]}"><h2>{f["site"]}</h2><ul>{site}</ul></nav>'
            f'<nav class="f-col" aria-label="{f["product"]}"><h2>{f["product"]}</h2><ul>{prod}</ul></nav>'
            f'<nav class="f-col" aria-label="{f["legal"]}"><h2>{f["legal"]}</h2><ul><li><a href="{priv}">{LG.TEXT[lang]["foot_privacy"]}</a></li></ul></nav>'
            f'</div><div class="wrap f-bottom"><span>© 2026 OcoteWorks · {d["foot_meta"]}</span>'
            f'<span><a href="https://www.instagram.com/ocote.works/" rel="me">Instagram</a> · <a href="https://www.behance.net/manuelgf" rel="me">Behance</a> · '
            f'<a href="https://www.linkedin.com/in/manuelgarflo" rel="me">LinkedIn</a></span></div></footer>')


def moto_svg():
    """Moto de aventura genérica en un banco de trabajo, sin rueda delantera (línea punteada) y una llave española."""
    return """<svg viewBox="0 0 520 330" role="img" aria-hidden="true" class="moto">
  <g fill="none" stroke="#17171a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M24 300H500" stroke-width="3"/>
    <circle cx="130" cy="228" r="62"/><circle cx="130" cy="228" r="47" stroke-width="3"/><circle cx="130" cy="228" r="8"/>
    <circle cx="398" cy="228" r="62" stroke-dasharray="10 12" stroke-width="3"/><circle cx="398" cy="228" r="6" stroke-width="3"/>
    <path d="M130 228L252 206"/><path d="M200 142L230 200"/>
    <rect x="240" y="168" width="72" height="52" rx="6"/><path d="M252 180h48M252 192h48M252 204h48" stroke-width="3"/>
    <path d="M252 206L246 150L332 118"/><path d="M312 168L338 122"/>
    <path d="M250 128Q292 98 336 112L330 142Q290 148 252 147Z" fill="#edb544"/>
    <path d="M150 132Q200 117 252 124"/><path d="M150 132L160 146H250"/><path d="M150 132L92 142"/>
    <path d="M338 112L398 228"/><path d="M347 108L404 220" stroke-width="3"/>
    <path d="M320 92L362 82"/><path d="M338 112L341 90"/>
    <path d="M354 104L380 97L392 128L368 135Z"/>
    <path d="M262 214Q205 232 175 180L152 162"/><rect x="132" y="146" width="30" height="16" rx="3" transform="rotate(35 147 154)"/>
    <path d="M236 300L252 252H302L318 300" stroke-width="4"/><path d="M246 252H308" stroke-width="4"/>
  </g>
  <g transform="translate(300 64) rotate(28)" stroke="#17171a" stroke-width="4" stroke-linejoin="round">
    <path d="M30 -8H150V8H30Z" fill="#edb544"/>
    <path d="M30 -8L20 -22A24 24 0 0 0 -16 -15L2 -6V6L-16 15A24 24 0 0 0 20 22L30 8Z" fill="#edb544"/>
    <circle cx="170" cy="0" r="21" fill="#edb544"/><circle cx="170" cy="0" r="9" fill="#f4ead7"/>
  </g>
  <g transform="translate(36 262)"><rect width="16" height="30" fill="#17171a" transform="skewX(-16.5)"/><rect x="24" width="16" height="30" fill="#edb544" transform="skewX(-16.5)"/><rect x="48" width="16" height="30" fill="#e48233" transform="skewX(-16.5)"/></g>
</svg>"""


LOADER = """<div id="ow-loader" aria-hidden="true"><div class="owl-glow"></div><div class="owl-in">
<img src="/assets/logo-marfil-360.webp" alt="" width="180" height="128">
<div class="owl-cnc"><span class="owl-prog">PROGRAM O1001 · OCOTEWORKS</span><span class="owl-btn">Cycle start</span><span class="owl-bar"><i></i></span></div>
</div></div>
<noscript><style>#ow-loader{{display:none}}</style></noscript>
<script>(function(){{var l=document.getElementById("ow-loader");if(!l)return;
var sec=null;try{{sec=sessionStorage.getItem("ow-secret");if(sec)sessionStorage.removeItem("ow-secret");if(sessionStorage.getItem("ow-lit")&&!sec){{l.remove();return}}sessionStorage.setItem("ow-lit","1")}}catch(e){{}}
if(sec){{var es=document.documentElement.lang==="es",p=l.querySelector(".owl-prog"),bt=l.querySelector(".owl-btn");if(p)p.textContent=es?"PRG SECRETO · ↑↑↓↓←→←→BA":"SECRET PRG · ↑↑↓↓←→←→BA";if(bt)bt.textContent="Cycle start";l.classList.add("owl-secret")}}
document.documentElement.classList.add("owl-on");
var t0=Date.now(),gone=false,min=matchMedia("(prefers-reduced-motion: reduce)").matches?0:(sec?3200:1900);
function done(){{if(gone)return;gone=true;setTimeout(function(){{l.classList.add("out");document.documentElement.classList.remove("owl-on");setTimeout(function(){{l.remove()}},600)}},Math.max(0,min-(Date.now()-t0)))}}
if(document.readyState==="complete")done();else addEventListener("load",done);setTimeout(done,4500)}})();</script>"""


def add_loader(html, lang):
    """Animación de carga: el logo enciende como tubo fluorescente con balastro y arranca un ciclo CNC (una vez por visita)."""
    return re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + LOADER.format(), html, count=1)


def render(tpl, data):
    out = tpl
    for k, v in data.items():
        out = out.replace("{{" + k + "}}", v)
    assert "{{" not in out, out[out.index("{{"):out.index("{{") + 40]
    return out


import privacy as LG

# Imágenes Open Graph por página (assets/og/<clave>-<idioma>.jpg). Se regeneran con src/og_images.py (necesita Playwright).
OG_PAGES = {
    "services": {"en": "OcoteWorks engineering services: Design. Prototype. Fabricate.", "es": "Servicios de ingeniería de OcoteWorks: Diseñar. Prototipar. Fabricar."},
    "about": {"en": "Manuel García in the OcoteWorks workshop at night.", "es": "Manuel García en el taller de OcoteWorks de noche."},
    "products": {"en": "Line drawing of an adventure motorcycle on a work stand, OW-01 in progress.", "es": "Dibujo de una moto de aventura en el banco de trabajo, OW-01 en desarrollo."},
    "journal": {"en": "Crossing a river on an adventure motorcycle, OcoteWorks journal.", "es": "Cruce de río en moto de aventura, bitácora de OcoteWorks."},
    "quote": {"en": "OcoteWorks quote builder project sheet.", "es": "Hoja de proyecto del cotizador de OcoteWorks."},
    "j-ow-02-silueta": {"en": "Cardboard prototype of the OW-02 tail rack on a Ténéré 700.", "es": "Prototipo de cartón del OW-02 en una Ténéré 700."},
    "ow02": {"en": "OW-02 Tail Rack T7 for the Yamaha Ténéré 700, render in matte black.", "es": "Tail Rack T7 OW-02 para la Yamaha Ténéré 700, render en negro mate."},
}

PAGES = {  # clave: (ruta EN, ruta ES)
    "home": ("/", "/es/"), "services": ("/services/", "/es/servicios/"), "products": ("/products/", "/es/productos/"),
    "about": ("/about/", "/es/sobre-mi/"), "journal": ("/journal/", "/es/bitacora/"), "quote": ("/quote/", "/es/cotizar/"),
    "privacy": ("/privacy/", "/es/privacidad/"),
}
import products as PR
for _p in PR.PRODUCTS:  # una página por producto, en los dos idiomas
    PAGES[_p["code"].lower().replace("-", "")] = (PR.url(_p, "en"), PR.url(_p, "es"))
NAV_ACTIVE = {pp["code"].lower().replace("-", ""): "products" for pp in PR.PRODUCTS}
import journal as JO
for _e in JO.ENTRIES:
    PAGES["j-" + _e["slug"]] = (JO.url(_e, "en"), JO.url(_e, "es"))
    NAV_ACTIVE["j-" + _e["slug"]] = "journal"


MOTION_V = ""
# Para los curiosos: logo en ASCII + mensaje escondido en la consola del navegador y en el código fuente.
ASCII_LOGO = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ascii_logo.txt"), encoding="utf-8").read().rstrip("\n")
HIDDEN = {
    "es": ("¿Revisando el código? Nosotros también revisamos cada tornillo.",
           "Diseñado y hecho a mano en Monterrey, México · 25° 41′ N, 100° 19′ O",
           "Si te gusta construir cosas, escríbenos: hola@ocoteworks.com"),
    "en": ("Reading the code? We check every bolt too.",
           "Designed and handmade in Monterrey, Mexico · 25° 41′ N, 100° 19′ W",
           "If you like building things, say hi: hola@ocoteworks.com"),
}
# Analítica sin cookies (GoatCounter). Panel: https://manuelgf10.goatcounter.com · vacío = desactivada.
GC_CODE = "manuelgf10"
FORMSPREE = "https://formspree.io/f/mwllgewa"


def waitlist_form(d):
    return (f'<form class="w-form" action="{FORMSPREE}" method="POST" data-ok="{d["pr_form_ok"]}" data-err="{d["pr_form_err"]}">'
            f'<label class="sr" for="w-email">{d["pr_form_label"]}</label>'
            f'<input id="w-email" type="email" name="email" required autocomplete="email" placeholder="{d["pr_form_ph"]}">'
            f'<input type="hidden" name="source" value="Waitlist · OW-01 · {d["lang"].upper()}">'
            f'<input type="hidden" name="_subject" value="Waitlist · OW-01">'
            f'<input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">'
            f'<button class="btn" type="submit">{d["pr_cta1"]}</button>'
            f'<p class="w-note">{d["pr_form_note"]}</p><p class="w-msg" role="status" aria-live="polite"></p>'
            f'<p class="f-privacy">{LG.TEXT[d["lang"]]["pr_privacy"]}</p></form>'
            f'<script src="/assets/forms.js" defer></script>')


# Microtipografía: espacio de no separación tras palabras cortas (evita "y", "de", "a"… sueltas al final de línea)
# y entre un número y la palabra que sigue ("6 semanas", "250 piezas"). Solo en texto visible, nunca en etiquetas ni scripts.
SHORT = {"es": "a|e|o|u|y|de|del|el|la|lo|los|las|en|un|una|al|con|por|para|sin|que|se|su|sus|mi|tu|no|ni|es|ya|le",
         "en": "a|an|the|of|to|in|on|at|by|for|and|or|is|it|we|i|my|no|as"}


def microtype(html, lang):
    short = re.compile(r"(?<![\w&;])(" + SHORT[lang] + r") (?=[^\s<])", re.I)
    num = re.compile(r"(?<=\d) (?=[A-Za-zÁÉÍÓÚáéíóúñ])")
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<textarea.*?</textarea>|<[^>]+>)", html, flags=re.S)
    head = 0  # dentro de h1–h3 no se pega nada: a tamaño display podría desbordar en celular
    for i, t in enumerate(parts):
        if i % 2:
            if re.match(r"<h[1-3][\s>]", t): head += 1
            elif re.match(r"</h[1-3]>", t): head = max(0, head - 1)
        elif t.strip() and not head:
            parts[i] = num.sub("\u00a0", short.sub(lambda m: m.group(1) + "\u00a0", t))
    return "".join(parts)


# Navegación instantánea: Chrome/Edge precargan (solo HTML, sin ejecutar) al pasar el cursor o tocar un enlace interno.
SPECULATION = ('<script type="speculationrules">{"prefetch":[{"source":"document","where":{"and":['
               '{"href_matches":"/*"},{"not":{"href_matches":"/*.pdf"}},{"not":{"href_matches":"/assets/*"}},'
               '{"not":{"selector_matches":"[download],[target=_blank],[href^=\'#\']"}}]},"eagerness":"moderate"}]}</script>')


def write(path, html):
    lang = "es" if '<html lang="es"' in html else "en"
    # Comentario escondido al inicio del código fuente (Ver código fuente).
    note = "\n".join(HIDDEN[lang])
    html = html.replace("<html", f"<!--\n{ASCII_LOGO}\n\n{note}\n-->\n<html", 1)
    html = microtype(html, lang)
    html = add_loader(html, lang)
    html = html.replace("</body>", f'<script src="/assets/motion.js?v={MOTION_V}" defer></script>\n</body>', 1)
    html = html.replace("</head>", SPECULATION + "\n</head>", 1)
    if GC_CODE:
        html = html.replace("</body>", f'<script data-goatcounter="https://{GC_CODE}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n</body>', 1)
    full = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)


def minify_css(css):
    """Minificado simple: quita comentarios y espacios sobrantes (el archivo editable sigue siendo src/styles.css)."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


def main():
    css = open(os.path.join(SRC, "styles.css"), encoding="utf-8").read()
    version = hashlib.sha1(css.encode()).hexdigest()[:8]
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "styles.css"), "w", encoding="utf-8").write(minify_css(css))
    qjs = open(os.path.join(SRC, "quote.js"), encoding="utf-8").read()
    open(os.path.join(ROOT, "assets", "quote.js"), "w", encoding="utf-8").write(qjs)
    qversion = hashlib.sha1(qjs.encode()).hexdigest()[:8]
    open(os.path.join(ROOT, "assets", "forms.js"), "w", encoding="utf-8").write(open(os.path.join(SRC, "forms.js"), encoding="utf-8").read())
    mjs = open(os.path.join(SRC, "motion.js"), encoding="utf-8").read()
    import json as _json
    mjs = mjs.replace("/*OW_HIDDEN*/", "var OW_ASCII = " + _json.dumps(ASCII_LOGO) + ", OW_NOTE = " + _json.dumps({k: "\n".join(v) for k, v in HIDDEN.items()}, ensure_ascii=False) + ";")
    open(os.path.join(ROOT, "assets", "motion.js"), "w", encoding="utf-8").write(mjs)
    global MOTION_V
    MOTION_V = hashlib.sha1(mjs.encode()).hexdigest()[:8]
    T = {n: open(os.path.join(SRC, n + ".html"), encoding="utf-8").read() for n in ["home", "services", "soon", "quote", "about", "legal", "product", "catalog", "journal_index", "journal_entry"]}
    pjs = open(os.path.join(SRC, "product.js"), encoding="utf-8").read()
    open(os.path.join(ROOT, "assets", "product.js"), "w", encoding="utf-8").write(pjs)
    pjsv = hashlib.sha1(pjs.encode()).hexdigest()[:8]

    for data in (EN, ES):
        i = 0 if data["lang"] == "en" else 1

        def ctx(key, **extra):
            en, es = PAGES[key]
            og = OG_PAGES.get(key)
            base = dict(data, version=version, header=header(data, NAV_ACTIVE.get(key, key), en, es), footer=footer(data),
                        og_image=f"https://ocoteworks.com/assets/og/{key}-{data['lang']}.jpg" if og else "https://ocoteworks.com/og-image.png",
                        og_alt=og[data["lang"]] if og else data["og_alt"],
                        p_alt_en="https://ocoteworks.com" + en, p_alt_es="https://ocoteworks.com" + es)
            base.update(extra)
            return base

        write(PAGES["home"][i], render(T["home"], ctx("home", h_product=PR.home_card(PR.PRODUCTS[0], data["lang"]), h_journal=JO.card(sorted(JO.ENTRIES, key=lambda x: x["date"], reverse=True)[0], data["lang"]), jsonld=jsonld(data["lang"], data["url"], data["description"]))))
        write(PAGES["services"][i], render(T["services"], ctx("services", p_title=data["s_title"], p_description=data["s_description"], p_url=data["s_url"])))
        write(PAGES["quote"][i], render(T["quote"], ctx("quote", qversion=qversion, q_privacy=LG.TEXT[data["lang"]]["q_privacy"])))
        lt = LG.TEXT[data["lang"]]
        write(PAGES["privacy"][i], render(T["legal"], ctx("privacy", p_title=lt["lg_title"], p_description=lt["lg_description"],
                                                         p_url="https://ocoteworks.com" + PAGES["privacy"][i],
                                                         lg_eyebrow=lt["lg_eyebrow"], lg_h1=lt["lg_h1"], lg_lead=lt["lg_lead"],
                                                         lg_updated_k=lt["lg_updated_k"], lg_updated=LG.LG_UPDATED[data["lang"]],
                                                         lg_note=f'<p class="lg-note">{lt["lg_lang_note"]}</p>' if lt["lg_lang_note"] else "",
                                                         lg_toc=LG.toc(data["lang"]), lg_sections=LG.body(data["lang"]))))
        write(PAGES["about"][i], render(T["about"], ctx("about", a_jsonld=person_jsonld(data), a_photos=about_photos(data["lang"]),
                                                          a_hero_visual=about_hero(data), a_plate_block=about_plate(data), a_name=about_name(data))))
        ig = "https://www.instagram.com/ocote.works/"
        subj = data["pr_mail_subject"].replace(" ", "%20").replace(":", "%3A")
        lang = data["lang"]
        U = PR.UI[lang]
        write(PAGES["products"][i], render(T["catalog"], ctx("products", p_title=U["cat_title"], p_description=U["cat_description"], p_url=data["pr_url"],
                                                             cat_eyebrow=U["cat_eyebrow"], cat_h1=U["cat_h1"], cat_lead=U["cat_lead"],
                                                             cat_cards="".join(PR.card(p, lang) for p in PR.PRODUCTS) + PR.card_ow01(lang, moto_svg()),
                                                             cat_status_dev=U["status_dev"], cat_ow01_name=U["ow01_name"], cat_bench=PR.bench(lang),
                                                             so_form=waitlist_form(data), moto_svg=moto_svg())))
        for p in PR.PRODUCTS:
            key = p["code"].lower().replace("-", "")
            P = p[lang]
            pd_url = "https://ocoteworks.com" + PR.url(p, lang)
            ld = {"@context": "https://schema.org", "@type": "Product", "name": f"{p['code']} {P['name']}", "sku": p["code"],
                  "brand": {"@type": "Brand", "name": "OcoteWorks"}, "description": P["tagline"], "url": pd_url,
                  "image": [f"https://ocoteworks.com{p['img_dir']}/{n}-{w[-1]}.jpg"
                            for n, w, _ in p["images"] + [x for v in p.get("variant_images", {}).values() for x in v]]}
            write(PAGES[key][i], render(T["product"], ctx(key, p_title=f"{p['code']} {P['name']} · {P['fit']} · OcoteWorks",
                                                          p_description=P["tagline"], p_url=pd_url,
                                                          pd_jsonld='<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
                                                          pd_back=U["back"], pd_gallery=PR.gallery(p, lang), pd_code=p["code"], pd_name=P["name"],
                                                          pd_fit=P["fit"], pd_tagline=P["tagline"], pd_intent=P["intent"], pd_price=PR.price(p), pd_price_note=U["price_note"],
                                                          pd_status=U["status_batch"], pd_variant_k=U["variant"], pd_variants=PR.variants(p, lang),
                                                          pd_buy=U["buy"], pd_buy_note=U["buy_note"],
                                                          pd_hl_eyebrow=U["hl_eyebrow"], pd_hl_h2=U["hl_h2"], pd_highlights=PR.highlights(p, lang),
                                                          pd_specs_eyebrow=U["specs_eyebrow"], pd_specs_h2=U["specs_h2"], pd_specs_note=U["specs_note"],
                                                          pd_specs=PR.specs(p, lang), pd_sheet=PR.sheet_card(p, lang), pd_blueprint=PR.blueprint(p, lang), pd_install=PR.install_guide(p, lang), pd_fine=U["fine"], pd_story="".join(f'<a class="pd-story" href="{JO.url(e, lang)}"><span>{JO.UI[lang]["idx_eyebrow"].split(" · ")[0]}</span>{e[lang]["title"]} →</a>' for e in JO.ENTRIES if e["product"] == p["code"]), pd_dialog=PR.buy_dialog(p, lang), pd_jsv=pjsv)))
        JU = JO.UI[lang]
        write(PAGES["journal"][i], render(T["journal_index"], ctx("journal", p_title=JU["idx_title"], p_description=JU["idx_description"], p_url=data["jo_url"],
                                                                 j_eyebrow=JU["idx_eyebrow"], j_h1=JU["idx_h1"], j_lead=JU["idx_lead"],
                                                                 j_cards="".join(JO.card(e, lang) for e in sorted(JO.ENTRIES, key=lambda x: x["date"], reverse=True)))))
        for e in JO.ENTRIES:
            key = "j-" + e["slug"]
            E = e[lang]
            prod = next(p for p in PR.PRODUCTS if p["code"] == e["product"])
            purl = PR.url(prod, lang)
            jurl = "https://ocoteworks.com" + JO.url(e, lang)
            ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": E["title"], "description": E["dek"],
                  "datePublished": e["date"], "inLanguage": lang, "url": jurl,
                  "image": f"https://ocoteworks.com/assets/journal/{e['slug']}/{e['cover']}-1200.jpg",
                  "author": {"@type": "Person", "name": "Manuel García", "url": "https://ocoteworks.com" + PAGES["about"][i]},
                  "publisher": {"@type": "Organization", "name": "OcoteWorks", "url": "https://ocoteworks.com/"}}
            write(PAGES[key][i], render(T["journal_entry"], ctx(key, p_title=f"{E['title']} · {JU['idx_eyebrow'].split(' · ')[0]} · OcoteWorks",
                                                                p_description=E["dek"], p_url=jurl,
                                                                j_jsonld='<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
                                                                j_back=JU["back"], j_cat=e["category"][lang], j_date_iso=e["date"], j_date=JO.date_txt(e, lang),
                                                                j_min=f'{JO.minutes(e, lang)} {JU["read"]}', j_title=E["title"], j_dek=E["dek"], j_by=JU["by"],
                                                                j_cover=JO.picture(e, e["cover"], lang, "(max-width:1200px) 100vw, 1140px", eager=True), j_vt=f"view-transition-name:j-{e['slug']}",
                                                                j_body=JO.body(e, lang, prod, purl), j_facts_k=JU["facts"], j_facts=JO.facts(e, lang),
                                                                j_product_url=purl, j_cta_product=JU["cta_product"], j_cta_ig=JU["cta_ig"])))

    # Página 404 (bilingüe, una sola)
    p404 = open(os.path.join(SRC, "404.html"), encoding="utf-8").read().replace("{{version}}", version).replace("{{speculation}}", SPECULATION).replace("<html", "<!--\n" + ASCII_LOGO + "\n\n" + "\n".join(HIDDEN["es"]) + "\n\n" + "\n".join(HIDDEN["en"]) + "\n-->\n<html", 1).replace("</body>", '<script src="/assets/motion.js?v=' + MOTION_V + '" defer></script>\n</body>', 1)
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(p404)

    def alt(en, es):
        return (f'<xhtml:link rel="alternate" hreflang="en" href="{en}"/>'
                f'<xhtml:link rel="alternate" hreflang="es" href="{es}"/>')
    pairs = [("https://ocoteworks.com" + en, "https://ocoteworks.com" + es) for en, es in PAGES.values()]
    urls = "".join(
        f"  <url><loc>{u}</loc><lastmod>{LASTMOD}</lastmod>{alt(en, es)}</url>\n"
        for en, es in pairs for u in (en, es))
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
    print("ok", version)


if __name__ == "__main__":
    main()
