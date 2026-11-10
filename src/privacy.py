"""Aviso de privacidad integral (LFPDPPP, vigente desde el 21 de marzo de 2025) y avisos simplificados de los formularios.

El texto en español es el que rige; el inglés es una traducción de cortesía.
Si cambia algo (otro proveedor, otra finalidad), actualizar el texto y LG_UPDATED. Analítica GoatCounter agregada el 9 nov 2026.
"""

LG_UPDATED = {"es": "10 de noviembre de 2026", "en": "November 10, 2026"}

MAIL = '<a href="mailto:hola@ocoteworks.com">hola@ocoteworks.com</a>'

SECTIONS = {
    "es": [
        ("Responsable", f"""
<p><b>Manuel García Flores</b>, persona física que opera con el nombre comercial <b>OcoteWorks</b>, es el responsable del tratamiento de tus datos personales.</p>
<p>Domicilio: Monterrey, Nuevo León, México. Para cualquier asunto relacionado con tus datos, el medio de contacto es {MAIL}. Esta misma dirección atiende las solicitudes de derechos ARCO.</p>"""),
        ("Datos que recabamos", f"""
<p>Solo los que tú nos das:</p>
<ul>
<li><b>Cotizador:</b> nombre, correo electrónico, nombre del proyecto o marca, la información que escribas en las notas y la configuración del proyecto que elegiste.</li>
<li><b>Listas de espera de productos:</b> correo electrónico y, en su caso, el acabado y el número de piezas que te interesan.</li>
<li><b>¿Tu moto no está?:</b> la moto que tienes, su año y, si lo dejas, tu correo electrónico.</li>
<li><b>Correo directo:</b> la información que incluyas en tu mensaje.</li>
</ul>
<p>No recabamos datos personales sensibles. Te pedimos no incluirlos en tus mensajes.</p>"""),
        ("Para qué los usamos", f"""
<p>Finalidades necesarias para atender lo que nos pides:</p>
<ul>
<li>Responder tu solicitud, hacerte preguntas sobre el proyecto y enviarte una propuesta y cotización.</li>
<li>Dar seguimiento al proyecto si decides contratarlo.</li>
<li>Avisarte cuando un producto de la lista de espera esté disponible, o cuando haya piezas para tu moto, y conocer cuánto interés hay en los productos en preparación y en cada moto, para decidir qué fabricar.</li>
</ul>
<p>No usamos tus datos para publicidad, no los vendemos y no los compartimos con terceros para sus propios fines. Si en el futuro quisiéramos usarlos para algo distinto, te pediríamos antes tu consentimiento.</p>"""),
        ("Cómo limitar su uso", f"""
<p>Puedes pedir en cualquier momento que dejemos de contactarte, salir de la lista de espera o que borremos tu información. Basta con escribir a {MAIL} desde el correo con el que nos contactaste.</p>"""),
        ("Derechos ARCO y revocación", f"""
<p>Tienes derecho a <b>acceder</b> a tus datos, <b>rectificarlos</b>, <b>cancelarlos</b> u <b>oponerte</b> a su uso (derechos ARCO), así como a <b>revocar</b> tu consentimiento. Para ejercerlos, escribe a {MAIL} con:</p>
<ul>
<li>Tu nombre y el correo con el que nos contactaste, que sirve para identificarte.</li>
<li>El derecho que quieres ejercer y una descripción clara de los datos de que se trata.</li>
</ul>
<p>Te responderemos por el mismo medio dentro de los plazos que establece la Ley Federal de Protección de Datos Personales en Posesión de los Particulares. La revocación no tiene efectos sobre el tratamiento que ya se haya realizado.</p>
<p>Si consideras que tus derechos no fueron atendidos, puedes acudir a la autoridad competente en materia de protección de datos personales, actualmente la Secretaría Anticorrupción y Buen Gobierno.</p>"""),
        ("Proveedores que intervienen", f"""
<p>Para operar el sitio usamos servicios que tratan datos por cuenta nuestra y solo para prestarnos el servicio:</p>
<ul>
<li><b>Formspree</b> (Estados Unidos): recibe los formularios del sitio y nos los reenvía por correo.</li>
<li><b>Google / Gmail</b>: buzón donde recibimos y respondemos los mensajes.</li>
<li><b>GoatCounter</b>: estadísticas de visitas sin cookies. Registra la página visitada, de dónde llegaste, el tipo de navegador, el tamaño de pantalla y el país y la región aproximados; no guarda tu dirección IP ni te identifica.</li>
<li><b>GitHub Pages</b> (hospedaje), <b>Adobe Fonts</b> y <b>Google Fonts</b> (tipografías): al cargar las páginas pueden recibir datos técnicos de tu navegador, como la dirección IP, conforme a sus propios avisos de privacidad.</li>
</ul>
<p>No realizamos transferencias de tus datos a terceros.</p>"""),
        ("Cookies y tecnologías similares", f"""
<p>El sitio no usa cookies ni herramientas de publicidad. Para saber cuántas personas lo visitan usamos GoatCounter, que cuenta visitas y algunas acciones (por ejemplo, pulsar «Comprar» o enviar un formulario) de forma agregada y sin cookies. Además, el sitio guarda en tu navegador, durante la visita, una marca para mostrar la animación de carga una sola vez; no te identifica y se borra al cerrar la pestaña.</p>"""),
        ("Conservación", f"""
<p>Conservamos tus datos solo el tiempo necesario para atender tu solicitud y dar seguimiento al proyecto. Los correos de la lista de espera se conservan hasta que el producto esté disponible o hasta que pidas salir.</p>"""),
        ("Cambios a este aviso", f"""
<p>Cualquier cambio se publicará en esta página con su fecha de actualización.</p>"""),
    ],
    "en": [
        ("Data controller", f"""
<p><b>Manuel García Flores</b>, an individual operating under the trade name <b>OcoteWorks</b>, is responsible for the processing of your personal data.</p>
<p>Address: Monterrey, Nuevo León, Mexico. For anything related to your data, contact {MAIL}. The same address handles ARCO rights requests.</p>"""),
        ("Data we collect", f"""
<p>Only what you give us:</p>
<ul>
<li><b>Quote builder:</b> name, email, project or brand name, anything you write in the notes and the project configuration you chose.</li>
<li><b>Product waitlists:</b> email and, where applicable, the finish and number of pieces you’re interested in.</li>
<li><b>“Your bike isn’t here?”:</b> the bike you ride, its year and, if you leave it, your email.</li>
<li><b>Direct email:</b> whatever you include in your message.</li>
</ul>
<p>We do not collect sensitive personal data. Please don’t include it in your messages.</p>"""),
        ("What we use it for", f"""
<p>Purposes needed to handle what you ask for:</p>
<ul>
<li>Reply to your request, ask questions about the project and send you a proposal and quote.</li>
<li>Follow up on the project if you decide to go ahead.</li>
<li>Let you know when a waitlisted product is available, or when there are parts for your bike, and gauge interest in products in pre-production and in each bike, to decide what to make.</li>
</ul>
<p>We don’t use your data for advertising, we don’t sell it and we don’t share it with third parties for their own purposes. If we ever wanted to use it for something else, we would ask for your consent first.</p>"""),
        ("How to limit its use", f"""
<p>You can ask us at any time to stop contacting you, to remove you from the waitlist or to delete your information. Just write to {MAIL} from the email you used to contact us.</p>"""),
        ("ARCO rights and withdrawal", f"""
<p>You have the right to <b>access</b>, <b>rectify</b> and <b>cancel</b> your data or <b>object</b> to its use (ARCO rights), and to <b>withdraw</b> your consent. To exercise them, write to {MAIL} with:</p>
<ul>
<li>Your name and the email you used to contact us, which identifies you.</li>
<li>The right you want to exercise and a clear description of the data involved.</li>
</ul>
<p>We will reply through the same channel within the time limits set by Mexico’s Federal Law on the Protection of Personal Data Held by Private Parties. Withdrawal does not affect processing already carried out.</p>
<p>If you believe your rights were not respected, you may contact the competent data protection authority, currently Mexico’s Secretaría Anticorrupción y Buen Gobierno.</p>"""),
        ("Service providers", f"""
<p>To run the site we use services that process data on our behalf and only to provide their service:</p>
<ul>
<li><b>Formspree</b> (United States): receives the site’s forms and forwards them to us by email.</li>
<li><b>Google / Gmail</b>: the inbox where we receive and answer messages.</li>
<li><b>GoatCounter</b>: cookie-free visit statistics. It records the page visited, where you came from, browser type, screen size and approximate country and region; it doesn’t store your IP address or identify you.</li>
<li><b>GitHub Pages</b> (hosting), <b>Adobe Fonts</b> and <b>Google Fonts</b> (typefaces): when pages load they may receive technical data from your browser, such as your IP address, under their own privacy notices.</li>
</ul>
<p>We do not transfer your data to third parties.</p>"""),
        ("Cookies and similar technologies", f"""
<p>The site uses no cookies and no advertising tools. To know how many people visit, we use GoatCounter, which counts visits and a few actions (such as pressing “Buy” or sending a form) in aggregate and without cookies. The site also stores a flag in your browser during your visit so the loading animation plays once; it doesn’t identify you and is cleared when you close the tab.</p>"""),
        ("Retention", f"""
<p>We keep your data only as long as needed to handle your request and follow up on the project. Waitlist emails are kept until the product is available or until you ask to be removed.</p>"""),
        ("Changes to this notice", f"""
<p>Any change will be published on this page with its update date.</p>"""),
    ],
}

TEXT = {
    "es": dict(
        lg_title="Aviso de privacidad · OcoteWorks",
        lg_description="Cómo OcoteWorks trata los datos personales que recibe por su sitio web, conforme a la LFPDPPP.",
        lg_eyebrow="OW · Legal", lg_h1="Aviso de<br><em>privacidad</em>",
        lg_lead="Qué datos recibimos por este sitio, para qué los usamos y cómo puedes controlarlos. Sin letra chica.",
        lg_updated_k="Última actualización", lg_lang_note="",
        foot_privacy="Aviso de privacidad",
        q_privacy=f'Responsable: Manuel García Flores (OcoteWorks), Monterrey, N.L. Usamos tu nombre, correo y lo que nos cuentes solo para responder y cotizar tu proyecto; no lo usamos para publicidad ni lo vendemos. Puedes pedir que lo borremos en hola@ocoteworks.com. <a href="/es/privacidad/">Aviso de privacidad</a>.',
        pr_privacy='Responsable: Manuel García Flores (OcoteWorks), Monterrey, N.L. Usamos tu correo solo para avisarte de OW-01 y puedes salir de la lista cuando quieras. <a href="/es/privacidad/">Aviso de privacidad</a>.',
    ),
    "en": dict(
        lg_title="Privacy notice · OcoteWorks",
        lg_description="How OcoteWorks handles the personal data it receives through its website, under Mexico’s data protection law.",
        lg_eyebrow="OW · Legal", lg_h1="Privacy<br><em>notice</em>",
        lg_lead="What data we receive through this site, what we use it for and how you can control it. No fine print.",
        lg_updated_k="Last updated",
        lg_lang_note='This is a courtesy translation. The <a href="/es/privacidad/">Spanish version</a> is the governing text.',
        foot_privacy="Privacy notice",
        q_privacy=f'Controller: Manuel García Flores (OcoteWorks), Monterrey, Mexico. We use your name, email and what you tell us only to reply and quote your project; never for advertising, never sold. Ask us to delete it anytime at hola@ocoteworks.com. <a href="/privacy/">Privacy notice</a>.',
        pr_privacy='Controller: Manuel García Flores (OcoteWorks), Monterrey, Mexico. We only use your email to tell you about OW-01, and you can leave the list anytime. <a href="/privacy/">Privacy notice</a>.',
    ),
}


def body(lang):
    out = []
    for n, (title, html) in enumerate(SECTIONS[lang], 1):
        out.append(f'<section class="lg-sec" id="s{n}"><h2><span class="lg-n">{n:02d}</span>{title}</h2><div class="lg-txt">{html.strip()}</div></section>')
    return "\n".join(out)


def toc(lang):
    return "".join(f'<li><a href="#s{n}"><span>{n:02d}</span>{t}</a></li>' for n, (t, _) in enumerate(SECTIONS[lang], 1))
