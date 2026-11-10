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
  // ── Secretos ─────────────────────────────────────────────
  var lang = document.documentElement.lang === "es" ? "es" : "en";
  var secretEv = function (k) { try { window.goatcounter.count({ path: "secreto-" + k, title: "Secreto · " + k, event: true }); } catch (e) {} };
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  // El ocote prende: 5 clics al logo (pie en cualquier página; cabecera en la portada).
  var toast = function (html, x, y) {
    var t = document.createElement("div"); t.className = "ow-toast"; t.innerHTML = html;
    document.body.appendChild(t);
    var w = t.offsetWidth, h = t.offsetHeight;
    t.style.left = Math.max(12, Math.min(innerWidth - w - 12, x - w / 2)) + "px";
    t.style.top = Math.max(12, Math.min(innerHeight - h - 12, y)) + "px";
    setTimeout(function () { t.style.opacity = "0"; setTimeout(function () { t.remove(); }, 450); }, 3600);
  };
  var ignite = function (el) {
    var r = el.getBoundingClientRect(), cols = ["#edb544", "#e48233", "#f4ead7", "#e48233"];
    if (!still && document.body.animate) {
      for (var i = 0; i < 34; i++) {
        var e = document.createElement("i"); e.className = "ow-ember";
        var c = cols[i % cols.length], s = 3 + Math.random() * 5;
        e.style.cssText = "left:" + (r.left + Math.random() * r.width) + "px;top:" + (r.top + r.height * (.4 + Math.random() * .6)) + "px;width:" + s + "px;height:" + s + "px;background:" + c + ";box-shadow:0 0 " + (s * 2) + "px " + c;
        document.body.appendChild(e);
        var dx = (Math.random() - .5) * 120, dy = 90 + Math.random() * 180;
        var a = e.animate([{ transform: "translate(0,0) scale(1)", opacity: 1 }, { transform: "translate(" + dx + "px," + (-dy) + "px) scale(.2)", opacity: 0 }],
          { duration: 1100 + Math.random() * 1300, delay: Math.random() * 350, easing: "cubic-bezier(.2,.6,.3,1)", fill: "both" });
        a.onfinish = (function (n) { return function () { n.remove(); }; })(e);
      }
      el.animate([{ filter: "drop-shadow(0 0 0 rgba(228,130,51,0))" }, { filter: "drop-shadow(0 0 14px rgba(228,130,51,.9))" }, { filter: "drop-shadow(0 0 0 rgba(228,130,51,0))" }], { duration: 1600, easing: "ease-out" });
    }
    toast(lang === "es" ? "<b>Ocote:</b> la astilla de pino que prende el fuego." : "<b>Ocote:</b> the pine splinter that starts the fire.",
          r.left + r.width / 2, r.top < innerHeight / 2 ? r.bottom + 12 : r.top - 70);
    secretEv("ocote");
  };
  var clicks = 0, last = 0;
  var onLogo = function (el) {
    var now = Date.now(); clicks = now - last < 1200 ? clicks + 1 : 1; last = now;
    if (clicks >= 5) { clicks = 0; ignite(el); }
  };
  var fLogo = document.querySelector(".f-brand picture");
  if (fLogo) { fLogo.style.cursor = "pointer"; fLogo.addEventListener("click", function () { onLogo(fLogo); }); }
  var hLogo = document.querySelector(".top .brand");
  if (hLogo && hLogo.pathname === location.pathname) {
    hLogo.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: still ? "auto" : "smooth" }); onLogo(hLogo.querySelector("img") || hLogo); });
  }

  // Un beso: 5 toques a la foto de Manuel en "Quién lo hace": corazones y una nota de Clau, su novia. (Luego, su video guiñando.)
  var face = document.querySelector("[data-kiss]");
  if (face) {
    var kc = 0, kl = 0;
    face.addEventListener("click", function () {
      var now = Date.now(); kc = now - kl < 1200 ? kc + 1 : 1; kl = now;
      if (kc < 5) return; kc = 0;
      var vid = face.querySelector("video[data-kiss-video]");
      if (vid) {  // cuando exista el video: la foto cobra vida y vuelve a la foto
        face.classList.add("kissing"); vid.currentTime = 0;
        var pr = vid.play(); if (pr && pr.catch) pr.catch(function () {});
        vid.onended = function () { face.classList.remove("kissing"); };
      }
      var r = face.getBoundingClientRect(), cols = ["#edb544", "#e48233", "#f4ead7"];
      if (!still && document.body.animate) {
        for (var i = 0; i < 16; i++) {
          var hrt = document.createElement("i"); hrt.className = "ow-heart"; hrt.textContent = "♥";
          hrt.style.cssText = "left:" + (r.left + r.width * (.25 + Math.random() * .5)) + "px;top:" + (r.top + r.height * (.35 + Math.random() * .2)) + "px;color:" + cols[i % 3] + ";font-size:" + (14 + Math.random() * 18) + "px";
          document.body.appendChild(hrt);
          var a = hrt.animate([{ transform: "translate(0,0) scale(.6)", opacity: 0 }, { opacity: 1, offset: .15 }, { transform: "translate(" + ((Math.random() - .5) * 140) + "px," + (-(120 + Math.random() * 160)) + "px) scale(1.1) rotate(" + ((Math.random() - .5) * 40) + "deg)", opacity: 0 }],
            { duration: 1500 + Math.random() * 1000, delay: Math.random() * 400, easing: "cubic-bezier(.2,.6,.3,1)", fill: "both" });
          a.onfinish = (function (n) { return function () { n.remove(); }; })(hrt);
        }
      }
      toast("<span class=\"ow-note\">He’s taken.</span><br><b>Atte. Clau</b> ♥", r.left + r.width / 2, r.top + r.height * .55);
      secretEv("beso");
    });
  }

  // Código Konami: vuelve a encender el tubo con un programa secreto.
  var seq = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65], pos = 0;
  document.addEventListener("keydown", function (e) {
    var k = e.keyCode || 0;
    pos = (k === seq[pos]) ? pos + 1 : (k === seq[0] ? 1 : 0);
    if (pos === seq.length) {
      pos = 0; secretEv("konami");
      try { sessionStorage.setItem("ow-secret", "1"); } catch (er) {}
      setTimeout(function () { location.reload(); }, 150);
    }
  });

  // Reloj de la franja del taller (hora de Monterrey)
  var clock = document.querySelector(".st-clock");
  if (clock && window.Intl) {
    var fmt = new Intl.DateTimeFormat("es-MX", { timeZone: clock.dataset.tz, hour: "2-digit", minute: "2-digit", hour12: false });
    var tick = function () { var t = fmt.format(new Date()); clock.textContent = t === "07:00" ? "T7:00" : t; clock.setAttribute("datetime", t); };  // a las 7:00, por la Ténéré 700
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
