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
        out += f'<div class="a-lv a-lv{i + 1}"><h4>{h}<span>{sub}</span></h4><ul>{lis}</ul></div>'
    return out


def equip(groups):
    return "".join(f"<div><h4>{h}</h4><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div>" for h, items in groups)


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
        figs += (f'<figure><picture><source srcset="/assets/photos/about/{b}-600.webp 600w, /assets/photos/about/{b}-1000.webp 1000w" '
                 f'sizes="(max-width:760px) 50vw, 290px" type="image/webp">'
                 f'<img src="/assets/photos/about/{b}-600.jpg" alt="{alt}" width="600" height="600" loading="lazy" decoding="async"></picture>'
                 f'<figcaption>{cap}</figcaption></figure>')
    return f'<div class="wrap a-photos">{figs}</div>'


def about_plate(d):
    return (f'<aside class="a-plate" aria-label="{d["a_plate_label"]}"><div class="a-plate-top"><span>OW · ID-001</span><span>{d["a_plate_tag"]}</span></div>'
            f'<p class="a-plate-name">Manuel García<span>Flores</span></p><dl>{d["a_plate"]}</dl>'
            '<div class="a-plate-foot"><span>REV 2026</span><i aria-hidden="true"></i><i aria-hidden="true"></i><i aria-hidden="true"></i></div></aside>')


def about_hero(d):
    return ('<figure class="a-hero-photo"><picture>'
            '<source srcset="/assets/photos/about/workshop-night-800.webp 800w, /assets/photos/about/workshop-night-1400.webp 1400w" sizes="(max-width:900px) 100vw, 480px" type="image/webp">'
            f'<img src="/assets/photos/about/workshop-night-800.jpg" alt="{d["a_hero_alt"]}" width="800" height="1000" fetchpriority="high" decoding="async"></picture>'
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
    photo_cap="Field testing · Mina, Nuevo León",
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
    q_noscript="The project builder needs JavaScript. Write to us and we'll put together your estimate:",
    q_send_h="Send it to the workshop",
    q_send_p="Your email app opens with the whole configuration filled in. We reply within two business days with questions and a proposal.",
    q_name="Name", q_email="Email", q_projname="Project or brand", q_projph="Optional",
    q_notes="Tell us about it", q_notesph="What it is, who it’s for, deadlines, references…",
    q_submit="Open email with my project",
    q_sheet="Project sheet", q_ref="Ref.", q_total="Estimated investment", q_vat="MXN · before VAT",
    q_time="Time to launch", q_review="Send this project", q_copy="Copy summary",
    q_disclaimer="Ballpark ranges for planning. We confirm the price with a scoped proposal after reviewing your project.",
    q_bar="Estimate", q_bar_cta="View sheet",
    # sobre mí (textos de /about/)
    nav_about="About", about_href="/about/",
    a_url="https://ocoteworks.com/about/",
    a_title="About Manuel García Flores · Industrial designer & product development engineer · OcoteWorks",
    a_description="Manuel García Flores is an industrial designer and product development engineer in Monterrey, Mexico, and the founder of OcoteWorks. Design, engineering, prototyping, manufacturing and testing.",
    a_eyebrow="About", a_plate_label="Profile summary", a_plate_tag="Founder",
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
            "<p>OcoteWorks is my independent workshop, where that background meets motorcycles, mechanical systems and the outdoors. It is not an extension of Bioana, and it isn’t a medical device company.</p>"
            "<p>The name comes from <i>ocote</i>, the resin-rich pine splinter used to start a fire in the mountains: small, resourceful and reliable when it counts. And from Ocotepec, the town where I’m from.</p>",
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
    photo_cap="Pruebas en campo · Mina, Nuevo León",
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
    q_send_p="Se abre tu correo con toda la configuración ya escrita. Te respondemos en dos días hábiles con preguntas y una propuesta.",
    q_name="Nombre", q_email="Correo", q_projname="Proyecto o marca", q_projph="Opcional",
    q_notes="Cuéntanos más", q_notesph="Qué es, para quién, fechas, referencias…",
    q_submit="Abrir correo con mi proyecto",
    q_sheet="Hoja de proyecto", q_ref="Ref.", q_total="Inversión estimada", q_vat="MXN · más IVA",
    q_time="Tiempo al lanzamiento", q_review="Enviar este proyecto", q_copy="Copiar resumen",
    q_disclaimer="Rangos de referencia para planear. Confirmamos el precio con una propuesta formal después de revisar tu proyecto.",
    q_bar="Estimación", q_bar_cta="Ver hoja",
    # sobre mí (textos de /es/sobre-mi/)
    nav_about="Sobre mí", about_href="/es/sobre-mi/",
    a_url="https://ocoteworks.com/es/sobre-mi/",
    a_title="Sobre Manuel García Flores · Diseñador industrial e ingeniero de producto · OcoteWorks",
    a_description="Manuel García Flores es diseñador industrial e ingeniero de desarrollo de producto en Monterrey y fundador de OcoteWorks. Diseño, ingeniería, prototipos, manufactura y pruebas.",
    a_eyebrow="Sobre mí", a_plate_label="Resumen de perfil", a_plate_tag="Fundador",
    a_hero_alt="El taller de OcoteWorks de noche: Manuel en el banco de trabajo entre chispas, junto a una moto y un Mini clásico",
    a_hero_cap="El taller de noche",
    a_off_alt="Manuel cruzando un río en su Yamaha Ténéré 700, con cerros verdes al fondo",
    a_off_cap="Bitácora · Cruce de río en la Ténéré 700",
    a_h1="Diseñador de formación.<br><em>Ingeniero por costumbre.</em>",
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
            "<p>OcoteWorks es mi taller independiente, donde esa experiencia se junta con las motos, los sistemas mecánicos y el campo. No es una extensión de Bioana ni una empresa de dispositivos médicos.</p>"
            "<p>El nombre viene del <i>ocote</i>, la astilla de pino resinoso con la que se prende el fuego en el monte: pequeña, ingeniosa y confiable cuando hace falta. Y de Ocotepec, el pueblo de donde soy.</p>",
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
    h_paths_h="Two ways to work with us",
    h_p1_h="Design. Prototype. Fabricate.",
    h_p1_p="Product development for creators and brands: design, engineering, prototypes, packaging and short production runs.",
    h_p1_more="Explore services",
    h_p2_h="Original parts and gear.",
    h_p2_p="Products we design, build and test ourselves. The first one, a rackless luggage system for adventure motorcycles, is on the bench.",
    h_p2_more="See what’s coming",
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
    h_paths_h="Dos formas de trabajar con nosotros",
    h_p1_h="Diseñar. Prototipar. Fabricar.",
    h_p1_p="Desarrollo de producto para creadores y marcas: diseño, ingeniería, prototipos, empaque y series cortas.",
    h_p1_more="Ver servicios",
    h_p2_h="Piezas y equipo propios.",
    h_p2_p="Productos que diseñamos, fabricamos y probamos nosotros. El primero, un sistema de equipaje rackless para motos de aventura, está en el banco de trabajo.",
    h_p2_more="Ver lo que viene",
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


def header(d, active, en_url, es_url):
    """Cabecera común: logo, secciones, menú de celular, idioma y botón de cotizar."""
    cur = ' aria-current="page"'
    secs = "".join(f'<a class="sec" href="{d[u]}"{cur if k == active else ""}>{d[t]}</a>' for k, t, u in NAV)
    lis = "".join(f'<li><a href="{d[u]}">{d[t]}</a></li>' for k, t, u in NAV) + f'<li><a href="{d["quote_href"]}">{d["cta"]}</a></li>'
    menu = (f'<details class="m-menu"><summary aria-label="{d["menu_label"]}"><span></span><span></span><span></span></summary>'
            f'<ul>{lis}</ul></details>')
    en_cur, es_cur = (cur, "") if d["lang"] == "en" else ("", cur)
    lang = (f'<span class="lang"><a href="{en_url}" hreflang="en" lang="en"{en_cur}>EN</a><span>/</span>'
            f'<a href="{es_url}" hreflang="es" lang="es"{es_cur}>ES</a></span>')
    return (f'<header class="top"><div class="wrap">'
            f'<a class="brand" href="{d["u_home"]}" aria-label="{d["home_label"]}"><picture><source srcset="/assets/logo-carbon-176.webp" type="image/webp">'
            f'<img src="/assets/logo-carbon-176.png" alt="OcoteWorks" width="88" height="63"></picture></a>'
            f'<nav class="nav" aria-label="{d["nav_label"]}">{secs}{menu}{lang}<a class="btn" href="{d["quote_href"]}">{d["cta"]}</a></nav>'
            f'</div></header>')


def footer(d):
    links = " · ".join(f'<a href="{d[u]}">{d[t]}</a>' for k, t, u in NAV)
    return (f'<footer><div class="wrap">'
            f'<picture><source srcset="/assets/logo-marfil-256.webp" type="image/webp"><img src="/assets/logo-marfil-256.png" alt="OcoteWorks" width="128" height="91" loading="lazy"></picture>'
            f'<p class="lema" lang="en">Rooted in Mexico.<br><span>Made to go further.</span></p>'
            f'<p class="meta">{d["foot_meta"]}<br><span class="f-nav" aria-label="{d["foot_nav"]}">{links}</span><br>'
            f'<a href="https://www.instagram.com/ocote.works/" rel="me">Instagram</a> · <a href="https://www.behance.net/manuelgf" rel="me">Behance</a> · '
            f'<a href="https://www.linkedin.com/in/manuelgarflo" rel="me">LinkedIn</a><br>© 2026 OcoteWorks</p></div></footer>')


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
<img src="/assets/logo-marfil.png" alt="" width="180" height="128">
<div class="owl-cnc"><span class="owl-prog">PROGRAM O1001 · OCOTEWORKS</span><span class="owl-btn">Cycle start</span><span class="owl-bar"><i></i></span></div>
</div></div>
<noscript><style>#ow-loader{{display:none}}</style></noscript>
<script>(function(){{var l=document.getElementById("ow-loader");if(!l)return;
try{{if(sessionStorage.getItem("ow-lit")){{l.remove();return}}sessionStorage.setItem("ow-lit","1")}}catch(e){{}}
document.documentElement.classList.add("owl-on");
var t0=Date.now(),gone=false,min=matchMedia("(prefers-reduced-motion: reduce)").matches?0:1900;
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


PAGES = {  # clave: (ruta EN, ruta ES)
    "home": ("/", "/es/"), "services": ("/services/", "/es/servicios/"), "products": ("/products/", "/es/productos/"),
    "about": ("/about/", "/es/sobre-mi/"), "journal": ("/journal/", "/es/bitacora/"), "quote": ("/quote/", "/es/cotizar/"),
}


def write(path, html):
    lang = "es" if '<html lang="es"' in html else "en"
    html = add_loader(html, lang)
    full = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)


def main():
    css = open(os.path.join(SRC, "styles.css"), encoding="utf-8").read()
    version = hashlib.sha1(css.encode()).hexdigest()[:8]
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "styles.css"), "w", encoding="utf-8").write(css)
    qjs = open(os.path.join(SRC, "quote.js"), encoding="utf-8").read()
    open(os.path.join(ROOT, "assets", "quote.js"), "w", encoding="utf-8").write(qjs)
    qversion = hashlib.sha1(qjs.encode()).hexdigest()[:8]
    T = {n: open(os.path.join(SRC, n + ".html"), encoding="utf-8").read() for n in ["home", "services", "soon", "quote", "about"]}

    for data in (EN, ES):
        i = 0 if data["lang"] == "en" else 1

        def ctx(key, **extra):
            en, es = PAGES[key]
            base = dict(data, version=version, header=header(data, key, en, es), footer=footer(data),
                        p_alt_en="https://ocoteworks.com" + en, p_alt_es="https://ocoteworks.com" + es)
            base.update(extra)
            return base

        write(PAGES["home"][i], render(T["home"], ctx("home", jsonld=jsonld(data["lang"], data["url"], data["description"]))))
        write(PAGES["services"][i], render(T["services"], ctx("services", p_title=data["s_title"], p_description=data["s_description"], p_url=data["s_url"])))
        write(PAGES["quote"][i], render(T["quote"], ctx("quote", qversion=qversion)))
        write(PAGES["about"][i], render(T["about"], ctx("about", a_jsonld=person_jsonld(data), a_photos=about_photos(data["lang"]),
                                                          a_hero_visual=about_hero(data), a_plate_block=about_plate(data))))
        ig = "https://www.instagram.com/ocote.works/"
        subj = data["pr_mail_subject"].replace(" ", "%20").replace(":", "%3A")
        write(PAGES["products"][i], render(T["soon"], ctx("products", p_title=data["pr_title"], p_description=data["pr_description"], p_url=data["pr_url"],
                                                          so_eyebrow=data["pr_eyebrow"], so_lead=data["pr_lead"], so_tag=data["pr_tag"],
                                                          so_cta1=data["pr_cta1"], so_cta1_href=f"mailto:hola@ocoteworks.com?subject={subj}",
                                                          so_cta2=data["pr_cta2"], so_cta2_href=ig, moto_svg=moto_svg())))
        write(PAGES["journal"][i], render(T["soon"], ctx("journal", p_title=data["jo_title"], p_description=data["jo_description"], p_url=data["jo_url"],
                                                         so_eyebrow=data["jo_eyebrow"], so_lead=data["jo_lead"], so_tag=data["jo_tag"],
                                                         so_cta1=data["jo_cta1"], so_cta1_href=ig,
                                                         so_cta2=data["jo_cta2"], so_cta2_href=data["about_href"], moto_svg=moto_svg())))

    # Página 404 (bilingüe, una sola)
    p404 = open(os.path.join(SRC, "404.html"), encoding="utf-8").read().replace("{{version}}", version)
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
