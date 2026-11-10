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
