(function () {
  // Mobile menu
  var menu = document.querySelector("[data-menu]");
  var mnav = document.querySelector("[data-mobile-nav]");
  if (menu && mnav) {
    menu.addEventListener("click", function () {
      var open = mnav.hidden;
      mnav.hidden = !open;
      menu.setAttribute("aria-expanded", String(open));
      menu.textContent = open ? "Close" : "Menu";
    });
    mnav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        mnav.hidden = true;
        menu.setAttribute("aria-expanded", "false");
        menu.textContent = "Menu";
      }
    });
  }

  // Contact form: organization fields appear only when relevant
  var orgFields = document.querySelector("[data-org-fields]");
  var reasonInputs = Array.prototype.slice.call(document.querySelectorAll('input[name="reason"]'));
  function syncOrgFields() {
    if (!orgFields) return;
    var picked = reasonInputs.filter(function (r) { return r.checked; })[0];
    var show = !!picked && picked.value === "organization";
    orgFields.hidden = !show;
    orgFields.querySelectorAll("[data-required-when-shown]").forEach(function (el) {
      el.required = show;
    });
  }
  reasonInputs.forEach(function (r) { r.addEventListener("change", syncOrgFields); });
  var topic = new URLSearchParams(window.location.search).get("topic");
  if (topic) {
    var match = reasonInputs.filter(function (r) { return r.value === topic; })[0];
    if (match) match.checked = true;
  }
  syncOrgFields();

  // Forms: validate in place, keep what people typed, never show a false confirmation
  var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function fieldValid(el) {
    if (!el.required && !el.value.trim()) return true;
    if (el.type === "email") return emailPattern.test(el.value.trim());
    if (el.type === "radio") {
      return Array.prototype.some.call(el.form.querySelectorAll('input[name="' + el.name + '"]'), function (r) { return r.checked; });
    }
    return el.value.trim().length > 0;
  }

  function showError(el, ok) {
    var errId = el.getAttribute("data-error");
    var err = errId && document.getElementById(errId);
    if (el.type !== "radio") el.setAttribute("aria-invalid", ok ? "false" : "true");
    if (err) err.hidden = ok;
  }

  document.querySelectorAll("form[data-site-form]").forEach(function (form) {
    var status = form.querySelector("[data-form-status]");
    var fields = Array.prototype.slice.call(form.querySelectorAll("input, select, textarea")).filter(function (el) {
      return el.hasAttribute("data-error");
    });

    fields.forEach(function (el) {
      el.addEventListener("blur", function () { if (el.value) showError(el, fieldValid(el)); });
      el.addEventListener("change", function () { showError(el, fieldValid(el)); });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      fields.forEach(function (el) {
        if (el.closest("[hidden]")) return;
        var ok = fieldValid(el);
        showError(el, ok);
        if (!ok && !firstBad) firstBad = el;
      });
      if (firstBad) { firstBad.focus(); return; }

      var endpoint = form.getAttribute("data-endpoint");
      status.hidden = false;
      if (!endpoint) {
        // No form service is connected yet. Say so plainly; keep the entries.
        status.textContent = "Preview only: this form isn't connected yet, so nothing was sent. Your entries are still here.";
        return;
      }
      status.textContent = "Sending...";
      fetch(endpoint, { method: "POST", body: new FormData(form) })
        .then(function (r) {
          if (!r.ok) throw new Error(String(r.status));
          status.textContent = form.getAttribute("data-success") || "Thanks. We received your message.";
          form.reset();
          syncOrgFields();
        })
        .catch(function () {
          status.textContent = "We couldn't send this just now. Everything you typed is still here, so please try again in a minute.";
        });
    });
  });
})();
