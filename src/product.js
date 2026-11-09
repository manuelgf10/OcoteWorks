/* OcoteWorks · ficha de producto
   Galería, selector de acabado y botón Comprar → panel honesto de lista del primer lote (Formspree, sin cobro). */
(function () {
  // Galería: las miniaturas cambian la imagen principal.
  var gal = document.querySelector(".pd-gallery");
  if (gal) {
    var srcs = gal.dataset.srcs.split("|"), main = gal.querySelector(".pd-main"), thumbs = gal.querySelectorAll(".pd-thumb");
    thumbs.forEach(function (t) {
      t.addEventListener("click", function () {
        var i = +t.dataset.i, img = main.querySelector("img"), src = main.querySelector("source");
        var timg = t.querySelector("img");
        src.srcset = srcs[i] + ".webp"; img.removeAttribute("srcset"); src.removeAttribute("sizes");
        img.src = srcs[i] + ".jpg"; img.alt = timg.alt;
        img.width = timg.width; img.height = timg.height;
        main.classList.toggle("tall", timg.naturalHeight > timg.naturalWidth || +timg.getAttribute("height") > +timg.getAttribute("width"));
        thumbs.forEach(function (x) { x.removeAttribute("aria-current"); });
        t.setAttribute("aria-current", "true");
      });
    });
  }

  // Acabado elegido → se refleja en el panel y en el formulario.
  var dlg = document.getElementById("pd-dlg"), form = dlg && dlg.querySelector("form");
  var note = document.querySelector(".pd-var-note");
  var setVariant = function (v, i) {
    if (!form) return;
    form.variant.value = v; form._subject.value = "Interés · " + form.dataset.code + " · " + v;
    dlg.querySelector("[data-variant-out]").textContent = v;
    if (note) note.hidden = i === 0;
  };
  document.querySelectorAll('.pd-var input[name="variant"]').forEach(function (r, i) {
    r.addEventListener("change", function () { if (r.checked) setVariant(r.value, i); });
  });

  // Comprar → panel.
  var open = document.querySelector("[data-open]");
  if (open && dlg) {
    open.addEventListener("click", function () {
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
          msg.textContent = form.dataset.ok.replace("{code}", form.dataset.code).replace("{variant}", form.variant.value);
        })
        .catch(function () { btn.disabled = false; msg.textContent = form.dataset.err; msg.classList.add("err"); });
    });
  }
})();
