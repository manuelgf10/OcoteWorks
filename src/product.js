/* OcoteWorks · ficha de producto
   Galería, selector de acabado y botón Comprar → panel honesto de lista del primer lote (Formspree, sin cobro). */
(function () {
  // Eventos para GoatCounter (si está bloqueado, no pasa nada).
  var ev = function (path, title) {
    try { window.goatcounter.count({ path: path, title: title || path, event: true }); } catch (e) {}
  };
  var code = (document.querySelector("#pd-dlg form") || { dataset: {} }).dataset.code || "producto";
  var slug = code.toLowerCase();
  var key = function () { var r = document.querySelector('.pd-var input[name="variant"]:checked'); return r ? r.dataset.key : "base"; };
  var seenVariant = {};

  // Galerías (una por acabado): las miniaturas cambian la imagen principal; la miniatura 3D abre el visor.
  var gals = document.querySelectorAll(".pd-gallery");
  var color = function () { var r = document.querySelector('.pd-var input[name="variant"]:checked'); return r ? r.dataset.color : null; };
  var viewer = null, libLoading = null, in3D = false;
  var loadLib = function (src) {
    if (window.customElements && customElements.get("model-viewer")) return Promise.resolve();
    if (!libLoading) libLoading = new Promise(function (ok, ko) {
      var s = document.createElement("script"); s.type = "module"; s.src = src;
      s.onerror = ko; document.head.appendChild(s);
      customElements.whenDefined("model-viewer").then(ok);
    });
    return libLoading;
  };
  var paint = function () {
    if (!viewer || !viewer.model) return;
    var c = color(); if (!c) return;
    viewer.model.materials[0].pbrMetallicRoughness.setBaseColorFactor(c);
    viewer.exposure = c.toLowerCase() === "#17171a" ? 1.1 : 0.85;  // el blanco se quema con la misma luz
  };
  var buildViewer = function (t) {
    var d = t.dataset, mv = document.createElement("model-viewer");
    var attrs = { src: d["3d"], alt: d.alt, "camera-controls": "", "touch-action": "pan-y", ar: "", "ar-modes": "webxr scene-viewer quick-look",
      "ar-scale": "fixed", "camera-orbit": "35deg 68deg 0.68m", "min-camera-orbit": "auto auto 0.35m", "max-camera-orbit": "auto auto 1.3m",
      "field-of-view": "28deg", "tone-mapping": "neutral", exposure: "1.1", "shadow-intensity": "0.9", "shadow-softness": "0.8",
      "environment-image": "neutral", "interaction-prompt": "none" };
    Object.keys(attrs).forEach(function (k) { mv.setAttribute(k, attrs[k]); });
    mv.innerHTML = '<button slot="ar-button" class="pd-ar" type="button">' + d.ar + '</button>' +
      '<div slot="progress-bar" class="pd-3d-load">' + d.load + '</div>';
    mv.addEventListener("load", function () { mv.querySelector(".pd-3d-load").hidden = true; paint(); });
    mv.addEventListener("error", function () { mv.querySelector(".pd-3d-load").textContent = d.err; });
    return mv;
  };
  var show3D = function (gal, on) {
    var stage = gal.querySelector(".pd-3d"), pic = gal.querySelector(".pd-main"), t3 = gal.querySelector("[data-3d]");
    if (!stage) return;
    if (on) {
      if (!viewer) viewer = buildViewer(t3);
      if (viewer.parentNode !== stage) {
        stage.innerHTML = ""; stage.appendChild(viewer);
        stage.insertAdjacentHTML("beforeend", '<p class="pd-3d-hint">' + t3.dataset.hint + '</p>');
      }
      loadLib(t3.dataset.lib).catch(function () { viewer.querySelector(".pd-3d-load").textContent = t3.dataset.err; });
      paint();
    }
    stage.hidden = !on; pic.hidden = on;
    gal.querySelectorAll(".pd-thumb").forEach(function (x) { x.removeAttribute("aria-current"); });
  };
  gals.forEach(function (gal) {
    var srcs = gal.dataset.srcs.split("|"), main = gal.querySelector(".pd-main"), thumbs = gal.querySelectorAll(".pd-thumb");
    thumbs.forEach(function (t) {
      t.addEventListener("click", function () {
        if (t.hasAttribute("data-3d")) {
          if (!in3D) ev("3d-" + slug, "Abre 3D · " + code);
          in3D = true; show3D(gal, true); t.setAttribute("aria-current", "true"); return;
        }
        in3D = false; show3D(gal, false);
        var i = +t.dataset.i, img = main.querySelector("img"), src = main.querySelector("source");
        var timg = t.querySelector("img");
        src.srcset = srcs[i] + ".webp"; img.removeAttribute("srcset"); src.removeAttribute("sizes");
        img.src = srcs[i] + ".jpg"; img.alt = timg.alt;
        img.width = timg.width; img.height = timg.height;
        main.classList.toggle("tall", +timg.getAttribute("height") > +timg.getAttribute("width"));
        t.setAttribute("aria-current", "true");
      });
    });
  });
  var showGallery = function (i) {
    var hit = document.querySelector('.pd-gallery[data-variant="' + i + '"]') ? String(i) : "0";
    gals.forEach(function (g) {
      g.hidden = g.dataset.variant !== hit;
      if (!g.hidden && in3D) { show3D(g, true); g.querySelector("[data-3d]").setAttribute("aria-current", "true"); }
    });
    paint();
  };

  // Acabado elegido → se refleja en el panel y en el formulario.
  var dlg = document.getElementById("pd-dlg"), form = dlg && dlg.querySelector("form");
  var setVariant = function (v, i) {
    showGallery(i);
    var k = document.querySelectorAll('.pd-var input[name="variant"]')[i].dataset.key;
    if (i && !seenVariant[k]) { seenVariant[k] = 1; ev("acabado-" + slug + "-" + k, "Ve acabado · " + code + " · " + v); }
    if (!form) return;
    form.variant.value = v; form._subject.value = "Interés · " + form.dataset.code + " · " + v;
    dlg.querySelector("[data-variant-out]").textContent = v;
  };
  document.querySelectorAll('.pd-var input[name="variant"]').forEach(function (r, i) {
    r.addEventListener("change", function () { if (r.checked) setVariant(r.value, i); });
  });

  // Comprar → panel.
  var open = document.querySelector("[data-open]");
  if (open && dlg) {
    open.addEventListener("click", function () {
      ev("comprar-" + slug + "-" + key(), "Comprar · " + code + " · " + form.variant.value);
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
      setTimeout(function () { form.email.focus(); }, 50);
    });
    dlg.querySelectorAll("[data-close]").forEach(function (b) { b.addEventListener("click", function () { dlg.close(); }); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
  }

  // Envío a Formspree (sin montos: el filtro anti-spam los retiene).
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = form.querySelector(".pd-msg"), btn = form.querySelector('button[type="submit"]');
      if (form._gotcha.value) return;
      if (!form.email.checkValidity()) { form.email.reportValidity(); return; }
      btn.disabled = true; msg.textContent = ""; msg.classList.remove("err");
      fetch(form.action, { method: "POST", headers: { Accept: "application/json" }, body: new FormData(form) })
        .then(function (r) {
          if (!r.ok) throw 0;
          form.classList.add("done");
          ev("lista-" + slug + "-" + key(), "Se anota · " + code + " · " + form.variant.value + " · " + form.quantity.value);
          msg.textContent = form.dataset.ok.replace("{code}", form.dataset.code).replace("{variant}", form.variant.value);
        })
        .catch(function () { btn.disabled = false; msg.textContent = form.dataset.err; msg.classList.add("err"); });
    });
  }
})();
