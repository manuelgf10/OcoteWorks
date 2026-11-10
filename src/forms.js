/* OcoteWorks · formularios simples (lista de espera) enviados a Formspree sin salir de la página */
document.querySelectorAll("form.w-form").forEach(function (f) {
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var msg = f.querySelector(".w-msg"), btn = f.querySelector("button");
    if (f._gotcha && f._gotcha.value) return;
    if (!f.email.checkValidity()) { f.email.reportValidity(); return; }
    btn.disabled = true;
    fetch(f.action, { method: "POST", headers: { Accept: "application/json" }, body: new FormData(f) })
      .then(function (r) {
        if (!r.ok) throw 0; f.classList.add("done");
        try { window.goatcounter.count({ path: "lista-espera-" + ((f._subject && f._subject.value.split("·").pop().trim()) || "general").toLowerCase().replace(/[^a-z0-9]+/g, "-"), title: "Lista de espera", event: true }); } catch (e) {} msg.textContent = f.dataset.ok; f.email.value = ""; })
      .catch(function () { btn.disabled = false; msg.textContent = f.dataset.err; msg.classList.add("err"); });
  });
});

/* "¿Tu moto no está?": voto por moto (y correo opcional) */
document.querySelectorAll("form.moto-form").forEach(function (f) {
  var other = f.querySelector(".mf-other"), msg = f.querySelector(".w-msg"), btn = f.querySelector("button");
  f.addEventListener("change", function (e) {
    if (e.target.name !== "moto") return;
    var isO = e.target.value === "other"; other.hidden = !isO; if (isO) f.moto_otra.focus();
    msg.textContent = ""; msg.classList.remove("err");
  });
  // la última pieza que vio en el mapa
  document.querySelectorAll(".km-pt").forEach(function (b) { b.addEventListener("click", function () { f.pieza_vista.value = b.getAttribute("aria-label") || ""; }); });
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    if (f._gotcha && f._gotcha.value) return;
    var sel = f.querySelector("input[name=moto]:checked");
    var moto = sel ? (sel.value === "other" ? f.moto_otra.value.trim() : sel.value) : "";
    if (!moto) { msg.textContent = f.dataset.pick; msg.classList.add("err"); return; }
    if (f.email.value && !f.email.checkValidity()) { f.email.reportValidity(); return; }
    f._subject.value = "Moto · " + moto;
    btn.disabled = true;
    fetch(f.action, { method: "POST", headers: { Accept: "application/json" }, body: new FormData(f) })
      .then(function (r) {
        if (!r.ok) throw 0; f.classList.add("done"); msg.classList.remove("err"); msg.textContent = f.dataset.ok;
        try { window.goatcounter.count({ path: "moto-" + moto.toLowerCase().replace(/[^a-z0-9]+/g, "-"), title: "Voto de moto", event: true }); } catch (e) {}
      })
      .catch(function () { btn.disabled = false; msg.textContent = f.dataset.err; msg.classList.add("err"); });
  });
});
