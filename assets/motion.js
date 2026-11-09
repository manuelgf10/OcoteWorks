/* OcoteWorks · movimiento sutil
   1. Cabecera compacta al bajar.
   2. Las secciones aparecen al entrar en pantalla (solo lo que está debajo del primer pantallazo).
   Respeta "reducir movimiento" y no toca el cotizador. */
(function () {
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
                ".a-levels", ".s-start-grid", ".a-stats", ".lg-toc ol"];
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
  document.querySelectorAll("main section > .wrap > *, main .lg-main > *, main .foto").forEach(function (el) {
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
