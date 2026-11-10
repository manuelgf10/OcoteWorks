/* OcoteWorks · movimiento sutil
   1. Cabecera compacta al bajar.
   2. Las secciones aparecen al entrar en pantalla (solo lo que está debajo del primer pantallazo).
   Respeta "reducir movimiento" y no toca el cotizador. */
(function () {
  // Para los curiosos que abren la consola: el logo en texto y una nota del taller.
  /*OW_HIDDEN*/
  try {
    var es = document.documentElement.lang === "es";
    console.log("%c" + OW_ASCII, "font:12px/1.15 ui-monospace,Menlo,monospace;color:#edb544;background:#17171a;padding:14px 18px;border-radius:6px");
    console.log("%c" + (es ? OW_NOTE.es : OW_NOTE.en), "font:13px/1.6 ui-monospace,Menlo,monospace;color:#17171a;background:#f4ead7;padding:10px 14px;border-left:4px solid #edb544");
  } catch (e) {}
  // Navegación instantánea en navegadores sin Speculation Rules (Safari, Firefox):
  // al pasar el cursor ~80 ms o tocar un enlace interno, se pide la página para que quede en caché.
  var hasSpec = window.HTMLScriptElement && HTMLScriptElement.supports && HTMLScriptElement.supports("speculationrules");
  var conn = navigator.connection;
  if (!hasSpec && window.fetch && !(conn && conn.saveData)) {
    var done = {}, timer;
    var target = function (e) {
      var a = e.target.closest && e.target.closest("a[href]");
      if (!a || a.target === "_blank" || a.hasAttribute("download") || a.origin !== location.origin) return null;
      if (/\.pdf$|^\/assets\//.test(a.pathname) || (a.pathname === location.pathname && a.hash)) return null;
      return a.pathname;
    };
    var warm = function (u) { if (done[u]) return; done[u] = 1; fetch(u, { credentials: "same-origin", priority: "low" }).catch(function () {}); };
    document.addEventListener("mouseover", function (e) { var u = target(e); if (!u) return; clearTimeout(timer); timer = setTimeout(function () { warm(u); }, 80); }, { passive: true });
    document.addEventListener("mouseout", function () { clearTimeout(timer); }, { passive: true });
    document.addEventListener("touchstart", function (e) { var u = target(e); if (u) warm(u); }, { passive: true });
  }
  // Reloj de la franja del taller (hora de Monterrey)
  var clock = document.querySelector(".st-clock");
  if (clock && window.Intl) {
    var fmt = new Intl.DateTimeFormat("es-MX", { timeZone: clock.dataset.tz, hour: "2-digit", minute: "2-digit", hour12: false });
    var tick = function () { var t = fmt.format(new Date()); clock.textContent = t; clock.setAttribute("datetime", t); };
    tick(); setInterval(tick, 15000);
  }
  // Video de portada: se carga después de la página; no en "reducir movimiento" ni con ahorro de datos.
  var hv = document.querySelector(".foto-video");
  var rmq = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var save = navigator.connection && navigator.connection.saveData;
  if (hv && !rmq && !save) {
    var startHero = function () {
      hv.src = window.matchMedia("(max-width:700px)").matches ? hv.dataset.sm : hv.dataset.lg;
      hv.addEventListener("playing", function () { hv.classList.add("on"); }, { once: true });
      var pr = hv.play(); if (pr && pr.catch) pr.catch(function () {});
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (en) {
          en.forEach(function (e) { if (e.isIntersecting) { var q = hv.play(); if (q && q.catch) q.catch(function () {}); } else hv.pause(); });
        }).observe(hv);
      }
    };
    if (document.readyState === "complete") startHero(); else window.addEventListener("load", startHero, { once: true });
  }
  // Cortometraje: botón propio de reproducir.
  document.querySelectorAll(".h-film-box").forEach(function (box) {
    var v = box.querySelector("video"), b = box.querySelector(".h-film-play");
    if (!v || !b) return;
    v.removeAttribute("controls");
    b.addEventListener("click", function () { var q = v.play(); if (q && q.catch) q.catch(function () {}); });
    v.addEventListener("play", function () { box.classList.add("playing"); v.setAttribute("controls", ""); });
  });

  var top = document.querySelector(".top");
  if (top) {
    var on = false, ticking = false;
    var check = function () {
      ticking = false;
      var now = window.scrollY > 24;
      if (now !== on) { on = now; top.classList.toggle("compact", on); }
    };
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(check); } }, { passive: true });
    check();
  }

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window) || document.body.classList.contains("q-page")) return;

  // Grupos que entran en cascada (cada hijo con un pequeño retraso).
  var GROUPS = [".trio", ".pasos", ".h-paths-grid", ".a-photos", ".a-work-grid", ".a-tools-grid", ".a-timeline",
                ".a-levels", ".s-start-grid", ".a-stats", ".lg-toc ol", ".cat-grid", ".pd-hl-grid", ".pd-specs dl", ".j-grid"];
  var fold = window.innerHeight * 0.92, items = [];
  var below = function (el) { return el.offsetHeight > 4 && el.getBoundingClientRect().top > fold; };

  GROUPS.forEach(function (sel) {
    document.querySelectorAll("main " + sel).forEach(function (g) {
      Array.prototype.forEach.call(g.children, function (c, i) {
        if (!below(c)) return;
        c.classList.add("rv"); c.style.transitionDelay = Math.min(i, 5) * 70 + "ms"; items.push(c);
      });
    });
  });
  // Bloques sueltos: hijos directos de cada sección que no contienen un grupo ya marcado.
  document.querySelectorAll("main section > .wrap > *, main .lg-main > *, main .foto, main .j-body > figure").forEach(function (el) {
    if (el.classList.contains("rv") || el.querySelector(".rv") || el.closest(".rv") || !below(el)) return;
    el.classList.add("rv"); items.push(el);
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("in"); io.unobserve(e.target);
      setTimeout(function () { e.target.style.transitionDelay = ""; }, 900);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  items.forEach(function (el) { io.observe(el); });
})();
