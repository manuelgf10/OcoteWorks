#!/usr/bin/env python3
"""Genera el sitio bilingüe de OcoteWorks.

    python3 src/build.py

Lee src/page.html + src/styles.css y escribe:
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


# Fotos de "Sobre mí": agrega aquí las fotos del taller cuando estén en /assets/photos/about/
# (nombre base sin extensión, texto alternativo EN, texto alternativo ES). Si la lista está vacía, la tira no aparece.
ABOUT_PHOTOS = []


def about_photos(lang):
    if not ABOUT_PHOTOS:
        return ""
    figs = "".join(f'<figure><img src="/assets/photos/about/{b}.jpg" alt="{en if lang == "en" else es}" loading="lazy" decoding="async"></figure>'
                   for b, en, es in ABOUT_PHOTOS)
    return f'<div class="wrap a-photos">{figs}</div>'


def about_hero(d):
    return (f'<aside class="a-plate" aria-label="{d["a_plate_label"]}"><div class="a-plate-top"><span>OW · ID-001</span><span>{d["a_plate_tag"]}</span></div>'
            f'<p class="a-plate-name">Manuel García<span>Flores</span></p><dl>{d["a_plate"]}</dl>'
            '<div class="a-plate-foot"><span>REV 2026</span><i aria-hidden="true"></i><i aria-hidden="true"></i><i aria-hidden="true"></i></div></aside>')


def tags(items):
    return "".join(f"<li><b>{c}</b>{t}</li>" for c, t in items)


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
    a_award="Recognized at the <b>Premio Nacional Diseña México 2020</b>, Mexico’s national design award.",
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
    nav_what="Qué hacemos", nav_process="Proceso", nav_workshop="El taller",
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
    a_award="Reconocido en el <b>Premio Nacional Diseña México 2020</b>, el premio nacional de diseño.",
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
                       "award": "Premio Nacional Diseña México 2020",
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

    # Cotizador
    qtpl = open(os.path.join(SRC, "quote.html"), encoding="utf-8").read()
    qjs = open(os.path.join(SRC, "quote.js"), encoding="utf-8").read()
    open(os.path.join(ROOT, "assets", "quote.js"), "w", encoding="utf-8").write(qjs)
    qversion = hashlib.sha1(qjs.encode()).hexdigest()[:8]
    for data, path in [(EN, os.path.join("quote", "index.html")), (ES, os.path.join("es", "cotizar", "index.html"))]:
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w", encoding="utf-8").write(render(qtpl, dict(data, version=version, qversion=qversion)))

    # Sobre mí
    atpl = open(os.path.join(SRC, "about.html"), encoding="utf-8").read()
    for data, path in [(EN, os.path.join("about", "index.html")), (ES, os.path.join("es", "sobre-mi", "index.html"))]:
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w", encoding="utf-8").write(render(atpl, dict(data, version=version, a_jsonld=person_jsonld(data),
                                                                 a_photos=about_photos(data["lang"]), a_hero_visual=about_hero(data))))

    # Página 404 (bilingüe, una sola)
    p404 = open(os.path.join(SRC, "404.html"), encoding="utf-8").read().replace("{{version}}", version)
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(p404)

    def alt(en, es):
        return (f'<xhtml:link rel="alternate" hreflang="en" href="{en}"/>'
                f'<xhtml:link rel="alternate" hreflang="es" href="{es}"/>')
    pairs = [("https://ocoteworks.com/", "https://ocoteworks.com/es/"),
             ("https://ocoteworks.com/quote/", "https://ocoteworks.com/es/cotizar/"),
             ("https://ocoteworks.com/about/", "https://ocoteworks.com/es/sobre-mi/")]
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
