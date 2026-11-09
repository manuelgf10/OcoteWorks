/* OcoteWorks · Project Builder / Cotizador
 * ------------------------------------------------------------------
 * PRECIOS Y TIEMPOS: edita solo el bloque OW_QUOTE.
 *   lo / hi  → rango en MXN antes de IVA
 *   w        → [semanas mínimo, semanas máximo]
 *   scale    → true = el precio se multiplica por la complejidad del proyecto
 * Después de editar: python3 src/build.py (copia este archivo a /assets/quote.js)
 * ------------------------------------------------------------------ */
const OW_QUOTE = {
  email: "hola@ocoteworks.com",
  round: 500,

  complexity: [
    { id: "simple", mult: 1,
      en: { t: "Single part", d: "One component: a bracket, a mount, a tool, a small object." },
      es: { t: "Pieza sencilla", d: "Un solo componente: un soporte, una base, una herramienta, un objeto pequeño." } },
    { id: "assembly", mult: 1.6,
      en: { t: "Product with a few parts", d: "2 to 10 parts that fit together: an accessory with hardware, a case, a rack." },
      es: { t: "Producto de varias piezas", d: "De 2 a 10 piezas que ensamblan: un accesorio con tornillería, un estuche, un rack." } },
    { id: "complex", mult: 2.5,
      en: { t: "Complex product", d: "Mechanisms, moving parts, or housings for electronics." },
      es: { t: "Producto complejo", d: "Mecanismos, partes móviles o carcasas para electrónica." } },
  ],

  stage: [
    { id: "idea", en: "Just an idea", es: "Solo es una idea" },
    { id: "sketch", en: "Sketches or references", es: "Bocetos o referencias" },
    { id: "cad", en: "3D model ready", es: "Modelo 3D listo" },
    { id: "proto", en: "I have a prototype", es: "Ya tengo un prototipo" },
    { id: "selling", en: "Already selling it", es: "Ya lo estoy vendiendo" },
  ],

  sections: [
    { key: "design", code: "OW-DS",
      en: { h: "Design & engineering", p: "From the first sketch to files ready to manufacture." },
      es: { h: "Diseño e ingeniería", p: "Del primer boceto a archivos listos para fabricar." },
      groups: [{ id: "design", type: "radio", scale: true, serial: true, options: [
        { id: "none", lo: 0, hi: 0, w: [0, 0],
          en: { t: "Not needed", d: "I already have production-ready files." },
          es: { t: "No lo necesito", d: "Ya tengo archivos listos para producción." } },
        { id: "dfm", lo: 4000, hi: 8000, w: [1, 1],
          en: { t: "DFM review", d: "We review your design so it's cheaper and easier to make." },
          es: { t: "Revisión DFM", d: "Revisamos tu diseño para que sea más fácil y barato de fabricar." } },
        { id: "concept", lo: 12000, hi: 22000, w: [2, 3],
          en: { t: "Concept + 3D model", d: "Sketches, two directions to choose from, and a 3D model." },
          es: { t: "Concepto + modelo 3D", d: "Bocetos, dos direcciones para elegir y un modelo 3D." } },
        { id: "full", lo: 28000, hi: 50000, w: [4, 7],
          en: { t: "Full development", d: "Concept, engineering, materials, tolerances and fabrication drawings." },
          es: { t: "Desarrollo completo", d: "Concepto, ingeniería, materiales, tolerancias y planos de fabricación." } },
      ] }] },

    { key: "proto", code: "OW-PT",
      en: { h: "Prototypes", p: "A real part to hold, fit and test before committing to production." },
      es: { h: "Prototipos", p: "Una pieza real para tocar, montar y probar antes de producir." },
      groups: [{ id: "proto", type: "radio", scale: true, serial: true, rounds: true, options: [
        { id: "none", lo: 0, hi: 0, w: [0, 0],
          en: { t: "Not now", d: "Skip prototyping for now." },
          es: { t: "Por ahora no", d: "Sin prototipos por el momento." } },
        { id: "visual", lo: 2500, hi: 6000, w: [1, 1], test: [0, 0],
          en: { t: "Visual model", d: "3D printed (FDM or resin) to check size, shape and ergonomics." },
          es: { t: "Modelo visual", d: "Impreso en 3D (FDM o resina) para revisar tamaño, forma y ergonomía." } },
        { id: "functional", lo: 8000, hi: 20000, w: [2, 3], test: [1, 1],
          en: { t: "Functional prototype", d: "CNC, sheet metal or mixed processes, made to be mounted and used." },
          es: { t: "Prototipo funcional", d: "CNC, lámina o procesos mixtos, hecho para montarse y usarse." } },
        { id: "preprod", lo: 18000, hi: 35000, w: [2, 3], test: [2, 3],
          en: { t: "Pre-production + field test", d: "Final materials and finishes, tested in real use before production." },
          es: { t: "Preserie + prueba en campo", d: "Materiales y acabados finales, probado en uso real antes de producir." } },
      ] }],
      roundsOpts: [ { n: 1, f: 1, wf: 1 }, { n: 2, f: 1.8, wf: 1.7 }, { n: 3, f: 2.5, wf: 2.3 } ] },

    { key: "brand", code: "OW-BR",
      en: { h: "Brand", p: "The name on the part, the box and the post. Built to work in metal, print and screen." },
      es: { h: "Marca", p: "El nombre en la pieza, la caja y la publicación. Pensada para metal, impresión y pantalla." },
      groups: [{ id: "brand", type: "radio", options: [
        { id: "none", lo: 0, hi: 0, w: [0, 0],
          en: { t: "Not now", d: "I already have a brand, or it can wait." },
          es: { t: "Por ahora no", d: "Ya tengo marca o puede esperar." } },
        { id: "logo", lo: 8000, hi: 15000, w: [2, 3],
          en: { t: "Logo essentials", d: "Logo, colors and typefaces, delivered in vector files." },
          es: { t: "Logo esencial", d: "Logotipo, colores y tipografías, entregado en archivos vectoriales." } },
        { id: "identity", lo: 20000, hi: 35000, w: [3, 5],
          en: { t: "Identity system", d: "Logo versions, icon, badges, palette and type for products and social." },
          es: { t: "Sistema de identidad", d: "Versiones del logo, ícono, insignias, paleta y tipografía para producto y redes." } },
        { id: "guide", lo: 40000, hi: 65000, w: [5, 8],
          en: { t: "Full brand guidelines", d: "The complete system plus a usage manual and master files." },
          es: { t: "Manual de marca completo", d: "El sistema completo, más manual de uso y archivos maestros." } },
      ] }] },

    { key: "pack", code: "OW-PK",
      en: { h: "Packaging", p: "Labels, boxes and inserts, designed with production-ready dielines." },
      es: { h: "Empaque", p: "Etiquetas, cajas e insertos, con suajes listos para producción." },
      groups: [
        { id: "pack", type: "radio", options: [
          { id: "none", lo: 0, hi: 0, w: [0, 0],
            en: { t: "Not needed", d: "No packaging for now." },
            es: { t: "No lo necesito", d: "Sin empaque por ahora." } },
          { id: "labels", lo: 4000, hi: 8000, w: [1, 1],
            en: { t: "Labels & stickers", d: "Product labels, part markings and stickers." },
            es: { t: "Etiquetas y stickers", d: "Etiquetas de producto, marcaje de piezas y stickers." } },
          { id: "retail", lo: 10000, hi: 18000, w: [2, 3],
            en: { t: "Retail box", d: "Box design and dieline, with labels included." },
            es: { t: "Caja de producto", d: "Diseño de caja y suaje, con etiquetas incluidas." } },
          { id: "premium", lo: 22000, hi: 38000, w: [3, 5],
            en: { t: "Premium packaging", d: "Custom box, fitted insert and unboxing sequence." },
            es: { t: "Empaque premium", d: "Caja a la medida, inserto ajustado y secuencia de unboxing." } },
        ] },
        { id: "ship", type: "check", options: [
          { id: "ship", lo: 5000, hi: 9000, w: [1, 2],
            en: { t: "Printed shipping box", d: "Corrugated mailer with your brand, sized for shipping." },
            es: { t: "Caja de envío impresa", d: "Caja de cartón corrugado con tu marca, dimensionada para envío." } },
        ] },
      ] },

    { key: "docs", code: "OW-DC",
      en: { h: "Instructions & print", p: "Everything that explains, sells and supports the product. Choose any." },
      es: { h: "Instructivos e impresos", p: "Todo lo que explica, vende y acompaña al producto. Elige los que quieras." },
      groups: [{ id: "docs", type: "check", options: [
        { id: "manual", lo: 8000, hi: 16000, w: [2, 3], scale: true,
          en: { t: "Illustrated instructions", d: "Step-by-step assembly or installation guide with technical illustrations." },
          es: { t: "Instructivo ilustrado", d: "Guía paso a paso de armado o instalación con ilustraciones técnicas." } },
        { id: "brochure", lo: 5000, hi: 10000, w: [1, 2],
          en: { t: "Brochure or sell sheet", d: "A printed or digital piece to present the product to clients and stores." },
          es: { t: "Brochure u hoja de venta", d: "Pieza impresa o digital para presentar el producto a clientes y tiendas." } },
        { id: "spec", lo: 3500, hi: 7000, w: [1, 1],
          en: { t: "Technical data sheet", d: "Dimensions, materials, fitment and specifications on one page." },
          es: { t: "Ficha técnica", d: "Dimensiones, materiales, compatibilidad y especificaciones en una hoja." } },
        { id: "renders", lo: 6000, hi: 12000, w: [1, 2],
          en: { t: "Product renders", d: "Six photorealistic images for your store, social and catalog." },
          es: { t: "Renders de producto", d: "Seis imágenes fotorrealistas para tienda, redes y catálogo." } },
      ] }] },

    { key: "make", code: "OW-MF",
      en: { h: "Short production run", p: "Local machining and fabrication in small batches. Unit cost is confirmed after the prototype." },
      es: { h: "Producción en serie corta", p: "Maquinado y fabricación local en lotes pequeños. El costo unitario se confirma después del prototipo." },
      groups: [{ id: "make", type: "radio", scale: true, serial: true, production: true,
        setup: [5000, 15000], unit: [350, 900],
        options: [
          { id: "none", qty: 0, disc: 0, w: [0, 0], en: { t: "Not yet", d: "Decide after the prototype." }, es: { t: "Todavía no", d: "Lo decido después del prototipo." } },
          { id: "q10", qty: 10, disc: 1, w: [2, 3], en: { t: "10 units", d: "Pilot batch for first customers." }, es: { t: "10 piezas", d: "Lote piloto para los primeros clientes." } },
          { id: "q50", qty: 50, disc: .85, w: [3, 5], en: { t: "50 units", d: "First sales run." }, es: { t: "50 piezas", d: "Primer lote de venta." } },
          { id: "q100", qty: 100, disc: .75, w: [4, 6], en: { t: "100 units", d: "Steady stock." }, es: { t: "100 piezas", d: "Inventario estable." } },
          { id: "q250", qty: 250, disc: .65, w: [5, 8], en: { t: "250 units", d: "Store and distributor volume." }, es: { t: "250 piezas", d: "Volumen para tiendas y distribuidores." } },
        ] }] },
  ],

  // Semanas que el cliente tarda en aprobar el concepto (barra rayada del cronograma)
  approval: [1, 1],

  // Especialista que el cliente tendría que contratar por separado para cada servicio (tarjeta "N → 1")
  specialists: {
    design: { en: "Industrial designer", es: "Diseñador industrial" },
    proto: { en: "Prototype shop", es: "Taller de prototipos" },
    brand: { en: "Brand studio", es: "Estudio de marca" },
    pack: { en: "Packaging designer", es: "Diseñador de empaque" },
    ship: { en: "Box maker", es: "Fabricante de cajas" },
    manual: { en: "Technical illustrator", es: "Ilustrador técnico" },
    brochure: { en: "Graphic designer", es: "Diseñador gráfico" },
    spec: { en: "Technical writer", es: "Redactor técnico" },
    renders: { en: "3D render artist", es: "Artista de renders 3D" },
    make: { en: "Machine shop", es: "Taller de maquinado" },
  },

  presets: [
    { id: "sprint",
      en: { t: "Prototype sprint", d: "Concept, 3D and a working prototype." },
      es: { t: "Sprint de prototipo", d: "Concepto, 3D y un prototipo funcional." },
      set: { design: "concept", proto: "functional", rounds: 1, brand: "none", pack: "none", ship: [], docs: [], make: "none" } },
    { id: "ready",
      en: { t: "Ready to sell", d: "Product, brand, box and a first run of 50." },
      es: { t: "Listo para vender", d: "Producto, marca, caja y un primer lote de 50." },
      set: { design: "full", proto: "preprod", rounds: 2, brand: "identity", pack: "retail", ship: ["ship"], docs: ["manual", "brochure", "renders"], make: "q50" } },
    { id: "brandpack",
      en: { t: "Brand & packaging", d: "You have the product. We make it look the part." },
      es: { t: "Marca y empaque", d: "Ya tienes el producto. Lo vestimos para venderse." },
      set: { stage: "proto", design: "none", proto: "none", rounds: 1, brand: "identity", pack: "retail", ship: [], docs: ["brochure", "renders"], make: "none" } },
    { id: "blank",
      en: { t: "Start from scratch", d: "Clear everything and choose piece by piece." },
      es: { t: "Desde cero", d: "Limpia todo y elige pieza por pieza." },
      set: { design: "none", proto: "none", rounds: 1, brand: "none", pack: "none", ship: [], docs: [], make: "none" } },
  ],
};

/* ---------------- textos de la interfaz ---------------- */
const T = {
  en: {
    presets: "Start from", project: "Your project", what: "What are you making?", where: "Where is it today?",
    factor: "Price factor", addon: "Add-on",
    scaleNote: "Design, prototype, instructions and production scale with complexity.",
    rounds: "Prototype rounds", round1: "1 round", roundN: "rounds",
    none: "—", from: "from",
    sheet: "Project sheet", ref: "Ref.", empty: "Pick at least one service to see an estimate.",
    total: "Estimated investment", vat: "MXN · before VAT", time: "Estimated timeline", weeks: "weeks", week: "week",
    review: "Send this project", copy: "Copy summary", copied: "Copied",
    disclaimer: "Ballpark ranges for planning. We confirm the price with a scoped proposal after reviewing your project.",
    unitsNote: "includes setup", perRound: "per round",
    send: { h: "Send it to the workshop", p: "Your email app opens with the whole configuration filled in. We reply within two business days with questions and a proposal.",
      name: "Name", email: "Email", projectName: "Project or brand", projectPh: "Optional", notes: "Tell us about it", notesPh: "What it is, who it's for, deadlines, references…",
      submit: "Open email with my project", required: "Please fill in your name and a valid email.",
      done: "Your email app should be open with everything filled in. If it didn't open, copy the summary and send it to" },
    mail: { subject: "Project request", hello: "Hi OcoteWorks,", intro: "I configured this project on ocoteworks.com:", link: "Configuration", notes: "Notes", from: "From", complexity: "Complexity", stage: "Stage", est: "Estimate", tl: "Timeline" },
    bar: "Estimate",
    months: m => `≈ ${m} months`, wk: "weeks",
    phases: { concept: "Concept", approval: "Concept approval", brand: "Branding", proto: "Prototyping", test: "Test & validate", pack: "Packaging", docs: "Instructions & print", make: "Low-volume release" },
    waiting: "Waiting on your approval",
    one: n => `<b>${n} specialists</b> you would otherwise find, brief and coordinate. With OcoteWorks: one workshop, one point of contact.`,
  },
  es: {
    presets: "Empieza desde", project: "Tu proyecto", what: "¿Qué quieres hacer?", where: "¿En qué punto está?",
    factor: "Factor de precio", addon: "Extra",
    scaleNote: "Diseño, prototipos, instructivos y producción se ajustan a la complejidad.",
    rounds: "Rondas de prototipo", round1: "1 ronda", roundN: "rondas",
    none: "—", from: "desde",
    sheet: "Hoja de proyecto", ref: "Ref.", empty: "Elige al menos un servicio para ver una estimación.",
    total: "Inversión estimada", vat: "MXN · más IVA", time: "Tiempo estimado", weeks: "semanas", week: "semana",
    review: "Enviar este proyecto", copy: "Copiar resumen", copied: "Copiado",
    disclaimer: "Rangos de referencia para planear. Confirmamos el precio con una propuesta formal después de revisar tu proyecto.",
    unitsNote: "incluye preparación", perRound: "por ronda",
    send: { h: "Mándalo al taller", p: "Se abre tu correo con toda la configuración ya escrita. Te respondemos en dos días hábiles con preguntas y una propuesta.",
      name: "Nombre", email: "Correo", projectName: "Proyecto o marca", projectPh: "Opcional", notes: "Cuéntanos más", notesPh: "Qué es, para quién, fechas, referencias…",
      submit: "Abrir correo con mi proyecto", required: "Escribe tu nombre y un correo válido.",
      done: "Tu app de correo debería estar abierta con todo escrito. Si no se abrió, copia el resumen y envíalo a" },
    mail: { subject: "Solicitud de proyecto", hello: "Hola, OcoteWorks:", intro: "Configuré este proyecto en ocoteworks.com:", link: "Configuración", notes: "Notas", from: "De", complexity: "Complejidad", stage: "Etapa", est: "Estimación", tl: "Tiempo" },
    bar: "Estimación",
    months: m => `≈ ${m} meses`, wk: "semanas",
    phases: { concept: "Concepto", approval: "Aprobación", brand: "Marca", proto: "Prototipos", test: "Prueba y validación", pack: "Empaque", docs: "Instructivos", make: "Serie corta" },
    waiting: "Esperando tu aprobación",
    one: n => `<b>${n} especialistas</b> que tendrías que buscar, explicarles y coordinar. Con OcoteWorks: un solo taller, un solo contacto.`,
  },
};

(function () {
  const root = document.getElementById("builder");
  if (!root) return;
  const L = document.documentElement.lang === "es" ? "es" : "en";
  const t = T[L], C = OW_QUOTE;
  const fmt = new Intl.NumberFormat("es-MX", { maximumFractionDigits: 0 });
  const money = n => "$" + fmt.format(n);
  const rLo = n => Math.floor(n / C.round) * C.round;
  const rHi = n => Math.ceil(n / C.round) * C.round;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  const d = new Date();
  const ref = "OW-Q-" + String(d.getFullYear()).slice(2) + String(d.getMonth() + 1).padStart(2, "0") + String(d.getDate()).padStart(2, "0") +
    "-" + Math.random().toString(16).slice(2, 5).toUpperCase();

  // estado inicial: sprint de prototipo
  const S = { complexity: "simple", stage: "idea", rounds: 1, design: "concept", proto: "functional", brand: "none", pack: "none", ship: [], docs: [], make: "none" };
  readHash();

  const groups = {};
  C.sections.forEach(s => s.groups.forEach(g => { groups[g.id] = Object.assign({ section: s }, g); }));
  const mult = () => C.complexity.find(c => c.id === S.complexity).mult;
  const roundsOf = () => C.sections.find(s => s.key === "proto").roundsOpts.find(r => r.n === S.rounds) || { n: 1, f: 1, wf: 1 };

  function priceOf(g, o) {
    const m = (g.scale || o.scale) ? mult() : 1;
    if (g.production) {
      if (!o.qty) return [0, 0];
      return [(g.setup[0] + g.unit[0] * o.qty * o.disc) * m, (g.setup[1] + g.unit[1] * o.qty * o.disc) * m];
    }
    let lo = o.lo * m, hi = o.hi * m;
    if (g.rounds) { const r = roundsOf(); lo *= r.f; hi *= r.f; }
    return [lo, hi];
  }
  const selected = id => Array.isArray(S[id]) ? S[id] : [S[id]];
  const rangeTxt = (lo, hi) => lo === hi ? money(rLo(lo)) : money(rLo(lo)) + " – " + money(rHi(hi));

  /* ---------- render del configurador ---------- */
  function card(name, type, value, checked, title, desc, price) {
    return `<label class="q-opt"><input type="${type}" name="${name}" value="${value}"${checked ? " checked" : ""}>` +
      `<span class="q-card"><span class="q-t">${title}</span><span class="q-d">${desc}</span><span class="q-p" data-price="${name}:${value}">${price}</span></span></label>`;
  }

  function build() {
    let h = "";
    // presets
    h += `<section class="q-sec q-presets" aria-labelledby="q-h-pre"><div class="q-head"><span class="q-code">OW-00</span><h2 id="q-h-pre">${t.presets}</h2></div><div class="q-opts q-opts-4">`;
    C.presets.forEach(p => { h += `<button type="button" class="q-preset" data-preset="${p.id}"><span class="q-t">${p[L].t}</span><span class="q-d">${p[L].d}</span></button>`; });
    h += `</div></section>`;
    // proyecto
    h += `<section class="q-sec" aria-labelledby="q-h-proj"><div class="q-head"><span class="q-code">OW-01</span><h2 id="q-h-proj">${t.project}</h2></div>`;
    h += `<fieldset><legend>${t.what}</legend><div class="q-opts q-opts-3">`;
    C.complexity.forEach(c => { h += card("complexity", "radio", c.id, S.complexity === c.id, c[L].t, c[L].d, t.factor + " ×" + c.mult); });
    h += `</div><p class="q-note">${t.scaleNote}</p></fieldset>`;
    h += `<fieldset><legend>${t.where}</legend><div class="q-chips">`;
    C.stage.forEach(s => { h += `<label class="q-chip"><input type="radio" name="stage" value="${s.id}"${S.stage === s.id ? " checked" : ""}><span>${s[L]}</span></label>`; });
    h += `</div></fieldset></section>`;
    // secciones
    C.sections.forEach((s, i) => {
      h += `<section class="q-sec" aria-labelledby="q-h-${s.key}"><div class="q-head"><span class="q-code">${s.code}</span><h2 id="q-h-${s.key}">${s[L].h}</h2><p>${s[L].p}</p></div>`;
      s.groups.forEach(g => {
        const extra = g.type === "check" && g.options.length === 1;
        h += `<fieldset><legend${extra ? "" : ' class="sr"'}>${extra ? t.addon : s[L].h}</legend><div class="q-opts${extra ? " q-opts-1" : ""}">`;
        g.options.forEach(o => h += card(g.id, g.type, o.id, selected(g.id).includes(o.id), o[L].t, o[L].d, ""));
        h += `</div></fieldset>`;
        if (g.rounds) {
          h += `<fieldset class="q-rounds"><legend>${t.rounds}</legend><div class="q-seg">`;
          s.roundsOpts.forEach(r => { h += `<label><input type="radio" name="rounds" value="${r.n}"${S.rounds === r.n ? " checked" : ""}><span>${r.n === 1 ? t.round1 : r.n + " " + t.roundN}</span></label>`; });
          h += `</div></fieldset>`;
        }
      });
      h += `</section>`;
    });
    root.innerHTML = h;
  }

  /* ---------- cálculo y resumen ---------- */
  function compute() {
    const lines = []; let lo = 0, hi = 0;
    C.sections.forEach(s => s.groups.forEach(g => {
      selected(g.id).forEach(id => {
        const o = g.options.find(x => x.id === id); if (!o) return;
        const [a, b] = priceOf(g, o); if (!b) return;
        lo += a; hi += b;
        let label = o[L].t;
        if (g.rounds && S.rounds > 1) label += ` · ${S.rounds} ${t.roundN}`;
        lines.push({ code: s.code, label, lo: a, hi: b, group: g.id, opt: o.id });
      });
    }));
    const sLo = schedule(0), sHi = schedule(1);
    return { lines, lo, hi, weeks: [sLo.total, sHi.total], sLo, sHi };
  }

  /* ---------- cronograma por fases ----------
   * Concepto → aprobación (cliente) → prototipos → prueba → serie corta.
   * Marca arranca en paralelo desde el día 0; empaque espera la aprobación y la marca;
   * instructivos e impresos arrancan con el concepto aprobado. */
  function schedule(i) {
    const pick = gid => {
      const g = groups[gid], o = g.options.find(x => x.id === S[gid]);
      if (!o || !priceOf(g, o)[1]) return null;
      return { g, o };
    };
    const ph = []; const add = (k, s, d, hatch) => { if (d > 0) ph.push({ k, s, e: s + d, hatch: !!hatch }); return s + d; };
    let a = 0;
    const ds = pick("design");
    if (ds) { const end = add("concept", 0, ds.o.w[i]); a = add("approval", end, C.approval[i], true); }
    let brandEnd = 0; const br = pick("brand");
    if (br) brandEnd = add("brand", 0, br.o.w[i]);
    let pEnd = a; const pr = pick("proto");
    if (pr) {
      const r = roundsOf();
      pEnd = add("proto", a, Math.round(pr.o.w[i] * r.wf));
      pEnd = add("test", pEnd, Math.round((pr.o.test || [0, 0])[i] * r.wf));
    }
    const pk = pick("pack");
    const shipW = S.ship.length ? groups.ship.options[0].w[i] : 0;
    const packW = (pk ? pk.o.w[i] : 0) + (pk ? Math.ceil(shipW / 2) : shipW);
    if (packW) add("pack", Math.max(a, brandEnd), packW);
    const docsW = Math.max(0, ...S.docs.map(id => groups.docs.options.find(o => o.id === id).w[i]));
    if (docsW) add("docs", a, docsW);
    const mk = pick("make");
    if (mk) add("make", pEnd, mk.o.w[i]);
    const order = ["concept", "approval", "brand", "proto", "test", "pack", "docs", "make"];
    ph.sort((x, y) => order.indexOf(x.k) - order.indexOf(y.k));
    return { ph, total: ph.reduce((m, p) => Math.max(m, p.e), 0) };
  }

  function gantt(r) {
    const el = document.getElementById("q-gantt");
    if (!r.sHi.ph.length) { el.innerHTML = ""; return; }
    const total = (r.sLo.total + r.sHi.total) / 2;
    const step = [1, 2, 4, 6, 8, 12, 16].find(s => total / s <= 4) || 24;
    const span = Math.max(step, Math.ceil(total / step) * step);
    let h = `<ul class="q-g-rows">`;
    r.sHi.ph.forEach(p => {
      const q = r.sLo.ph.find(x => x.k === p.k) || p;
      const s = (q.s + p.s) / 2, e = (q.e + p.e) / 2;
      h += `<li><span>${t.phases[p.k]}</span><i><b class="${p.hatch ? "hatch" : ""}" style="left:${(s / span * 100).toFixed(2)}%;width:${Math.max(2.5, (e - s) / span * 100).toFixed(2)}%"></b></i></li>`;
    });
    h += `</ul><div class="q-g-axis"><span>${t.wk}</span><i>`;
    for (let x = 0; x <= span; x += step) h += `<em style="left:${(x / span * 100).toFixed(2)}%">${x}</em>`;
    h += `</i></div>`;
    if (r.sHi.ph.some(p => p.hatch)) h += `<p class="q-g-legend"><b class="hatch"></b>${t.waiting}</p>`;
    el.innerHTML = h;
  }

  function oneCard() {
    const el = document.getElementById("q-one"), sp = C.specialists, list = [];
    const addSp = k => { if (sp[k] && !list.includes(sp[k][L])) list.push(sp[k][L]); };
    ["design", "proto", "brand", "pack", "make"].forEach(g => { const o = groups[g].options.find(x => x.id === S[g]); if (o && priceOf(groups[g], o)[1]) addSp(g); });
    S.ship.forEach(() => addSp("ship")); S.docs.forEach(addSp);
    if (list.length < 2) { el.hidden = true; return; }
    el.hidden = false;
    el.innerHTML = `<div class="q-one-n">${list.length}<span>→</span>1</div><div><p>${t.one(list.length)}</p><small>${list.join(" · ")}</small></div>`;
  }
  const weeksTxt = w => !w[1] ? t.none : (w[0] === w[1] ? w[0] : w[0] + "–" + w[1]) + " " + (w[1] === 1 ? t.week : t.weeks);

  function update() {
    // precios en tarjetas
    root.querySelectorAll("[data-price]").forEach(el => {
      const [gid, oid] = el.dataset.price.split(":"); const g = groups[gid]; if (!g) return;
      const o = g.options.find(x => x.id === oid); const [a, b] = priceOf(g, o);
      el.textContent = b ? rangeTxt(a, b) + (g.production ? " · " + t.unitsNote : "") : t.none;
    });
    const r = compute();
    const sum = document.getElementById("q-summary");
    let h = "";
    if (!r.lines.length) h = `<p class="q-empty">${t.empty}</p>`;
    else {
      h += `<ul class="q-lines">`;
      r.lines.forEach(l => { h += `<li><span class="q-lc">${l.code}</span><span class="q-ll">${esc(l.label)}</span><span class="q-lp">${rangeTxt(l.lo, l.hi)}</span></li>`; });
      h += `</ul>`;
    }
    sum.innerHTML = h;
    const tot = r.lines.length ? rangeTxt(r.lo, r.hi) : t.none;
    document.getElementById("q-total").textContent = tot;
    document.getElementById("q-weeks").textContent = weeksTxt(r.weeks);
    const mo = r.weeks.map(w => w / 4.33);
    document.getElementById("q-months").textContent = r.weeks[1] >= 8 ? t.months(Math.round(mo[0]) === Math.round(mo[1]) ? Math.round(mo[1]) : Math.max(1, Math.round(mo[0])) + "–" + Math.round(mo[1])) : "";
    gantt(r); oneCard();
    document.getElementById("q-bar-total").textContent = tot;
    const cx = C.complexity.find(c => c.id === S.complexity), st = C.stage.find(s => s.id === S.stage);
    document.getElementById("q-meta").textContent = cx[L].t + " · " + st[L];
    writeHash();
    return r;
  }

  /* ---------- estado en la URL (para compartir y para el correo) ---------- */
  function stateParams() {
    const p = new URLSearchParams();
    ["complexity", "stage", "design", "proto", "brand", "pack", "make"].forEach(k => p.set(k, S[k]));
    p.set("rounds", S.rounds); p.set("ship", S.ship.join(",")); p.set("docs", S.docs.join(","));
    return p.toString();
  }
  // Link que reconstruye la configuración, aunque el visitante haya usado un ancla (#q-send) después.
  const configUrl = () => location.origin + location.pathname + "#" + stateParams();
  function writeHash() { history.replaceState(null, "", "#" + stateParams()); }
  function readHash() {
    if (location.hash.length < 3) return;
    const p = new URLSearchParams(location.hash.slice(1));
    const ok = (k, list) => { const v = p.get(k); if (v && list.some(x => x.id === v)) S[k] = v; };
    ok("complexity", C.complexity); ok("stage", C.stage);
    C.sections.forEach(s => s.groups.forEach(g => {
      const v = p.get(g.id); if (v === null) return;
      if (g.type === "check") S[g.id] = v.split(",").filter(x => g.options.some(o => o.id === x));
      else if (g.options.some(o => o.id === v)) S[g.id] = v;
    }));
    const rn = parseInt(p.get("rounds"), 10); if ([1, 2, 3].includes(rn)) S.rounds = rn;
  }

  /* ---------- eventos ---------- */
  root.addEventListener("change", e => {
    const el = e.target; if (!el.name) return;
    if (el.name === "rounds") S.rounds = parseInt(el.value, 10);
    else if (Array.isArray(S[el.name])) S[el.name] = [...root.querySelectorAll(`input[name="${el.name}"]:checked`)].map(i => i.value);
    else S[el.name] = el.value;
    clearPreset(); update();
  });
  root.addEventListener("click", e => {
    const b = e.target.closest("[data-preset]"); if (!b) return;
    const p = C.presets.find(x => x.id === b.dataset.preset);
    Object.assign(S, JSON.parse(JSON.stringify(p.set)));
    build(); update();
    const nb = root.querySelector(`[data-preset="${p.id}"]`); nb.setAttribute("aria-pressed", "true"); nb.focus();
  });
  function clearPreset() { root.querySelectorAll("[data-preset]").forEach(b => b.removeAttribute("aria-pressed")); }

  /* ---------- resumen en texto ---------- */
  function summaryText(form) {
    const r = compute(), m = t.mail;
    const cx = C.complexity.find(c => c.id === S.complexity), st = C.stage.find(s => s.id === S.stage);
    let s = `${t.sheet} ${ref}\n${m.complexity}: ${cx[L].t}\n${m.stage}: ${st[L]}\n\n`;
    r.lines.forEach(l => { s += `[${l.code}] ${l.label}: ${rangeTxt(l.lo, l.hi)}\n`; });
    s += `\n${m.est}: ${r.lines.length ? rangeTxt(r.lo, r.hi) + " " + t.vat : t.none}\n${m.tl}: ${weeksTxt(r.weeks)}\n`;
    s += `${m.link}: ${configUrl()}\n`;
    if (form) {
      if (form.notes) s += `\n${m.notes}:\n${form.notes}\n`;
      s += `\n${m.from}: ${form.name} <${form.email}>${form.project ? " · " + form.project : ""}\n`;
    }
    return s;
  }

  const copyBtn = document.getElementById("q-copy");
  copyBtn.addEventListener("click", async () => {
    const f = readForm();
    const txt = summaryText(f.name ? f : null);
    try { await navigator.clipboard.writeText(txt); } catch (_) {
      const ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (__) {} ta.remove();
    }
    const old = copyBtn.textContent; copyBtn.textContent = t.copied; setTimeout(() => copyBtn.textContent = old, 1800);
  });

  function readForm() {
    const fm = document.getElementById("q-form");
    return { name: fm.name.value.trim(), email: fm.email.value.trim(), project: fm.project.value.trim(), notes: fm.notes.value.trim() };
  }
  document.getElementById("q-form").addEventListener("submit", e => {
    e.preventDefault();
    const f = readForm(), msg = document.getElementById("q-msg");
    if (!f.name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email)) { msg.textContent = t.send.required; msg.className = "q-msg err"; return; }
    const subject = `${t.mail.subject} · ${f.project || f.name} · ${ref}`;
    const body = `${t.mail.hello}\n\n${t.mail.intro}\n\n` + summaryText(f);
    location.href = `mailto:${C.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    msg.innerHTML = `${t.send.done} <a href="mailto:${C.email}">${C.email}</a>.`; msg.className = "q-msg ok";
  });

  // textos estáticos del panel
  document.getElementById("q-ref").textContent = ref;
  build(); update();
  const pre = C.presets.find(p => Object.keys(p.set).every(k => JSON.stringify(p.set[k]) === JSON.stringify(S[k])));
  if (pre) root.querySelector(`[data-preset="${pre.id}"]`).setAttribute("aria-pressed", "true");
})();
