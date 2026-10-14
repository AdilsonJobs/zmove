// Z-Move site: theme toggle, mobile menu, "How it works" steps, route picker, brand comparison,
// demo form. Everything is readable without JavaScript; this only adds the interactions.
(function () {
  "use strict";
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  var $ = function (sel, el) { return (el || document).querySelector(sel); };
  var $$ = function (sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); };

  // Theme. The screenshots carry a dark <source> with the system media query; an explicit choice
  // overrides that query so they follow the toggle too.
  function explicitTheme() {
    var t = root.getAttribute("data-theme");
    return t === "dark" || t === "light" ? t : null;
  }
  function effectiveTheme() {
    return explicitTheme() || (media && media.matches ? "dark" : "light");
  }
  function syncTheme() {
    var t = explicitTheme();
    var m = t === "dark" ? "all" : t === "light" ? "not all" : "(prefers-color-scheme: dark)";
    $$("source[data-theme-dark]").forEach(function (s) { s.media = m; });
    var btn = $("[data-theme-toggle]");
    if (btn) {
      var label = effectiveTheme() === "dark" ? btn.getAttribute("data-to-light") : btn.getAttribute("data-to-dark");
      btn.setAttribute("aria-label", label);
      btn.setAttribute("title", label);
    }
  }
  var themeBtn = $("[data-theme-toggle]");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = effectiveTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("zm-theme", next); } catch (e) {}
      syncTheme();
    });
  }
  if (media && media.addEventListener) media.addEventListener("change", syncTheme);
  syncTheme();

  // Mobile menu
  var menuBtn = $("[data-menu-toggle]");
  var menu = $("#m-nav");
  function setMenu(open) {
    if (!menuBtn || !menu) return;
    menu.hidden = !open;
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.setAttribute("aria-label", open ? menuBtn.getAttribute("data-close") : menuBtn.getAttribute("data-open"));
  }
  if (menuBtn && menu) {
    menuBtn.addEventListener("click", function () { setMenu(menu.hidden); });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !menu.hidden) { setMenu(false); menuBtn.focus(); }
    });
  }

  // How it works: one screenshot per step
  var stepBtns = $$("[data-step]");
  var stepCap = $("#step-cap");
  stepBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var i = btn.getAttribute("data-step");
      stepBtns.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle("is-on", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      $$("[data-step-shot]").forEach(function (f) { f.classList.toggle("is-on", f.getAttribute("data-step-shot") === i); });
      if (stepCap) stepCap.textContent = btn.getAttribute("data-cap");
    });
  });

  // Route picker: the figures for every route are in the page as JSON
  var dataEl = $("#zm-routes");
  if (dataEl) {
    var R = JSON.parse(dataEl.textContent);
    var pick = { from: "azure", to: "zadara" };
    var render = function () {
      var d = R.data[pick.from + ">" + pick.to];
      $("#rp-title").textContent = R.clouds[pick.from] + " → " + R.clouds[pick.to];
      var status = $("#rp-status");
      $("#rp-ok").hidden = !d;
      $("#rp-no").hidden = !!d;
      if (d) {
        status.textContent = R.status[d.st];
        status.className = "pill " + (d.st === "prod" ? "pill-ok" : "pill-info");
        $("#rp-how").textContent = d.how;
        $("#rp-result").textContent = d.result;
        $("#rp-os").textContent = d.os;
        $("#rp-note").textContent = d.note;
        $("#rp-boot").textContent = d.boot;
        $("#rp-bootbox").className = "boot " + (d.bootOk ? "is-ok" : "is-info");
        var ro = $("#rp-readout");
        ro.textContent = "";
        d.m.forEach(function (x) {
          var row = document.createElement("div");
          row.className = "ro";
          var v = document.createElement("span");
          v.className = "ro-v";
          v.textContent = x[0];
          var k = document.createElement("span");
          k.className = "ro-k";
          k.textContent = x[1];
          row.appendChild(v);
          row.appendChild(k);
          ro.appendChild(row);
        });
      } else {
        status.textContent = R.status.no;
        status.className = "pill pill-muted";
        $("#rp-msg").textContent = pick.from === pick.to ? R.same : R.none;
      }
      $$("[data-side]").forEach(function (b) {
        var on = pick[b.getAttribute("data-side")] === b.getAttribute("data-cloud");
        b.classList.toggle("is-on", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
    };
    $$("[data-side]").forEach(function (b) {
      b.addEventListener("click", function () {
        pick[b.getAttribute("data-side")] = b.getAttribute("data-cloud");
        render();
      });
    });
  }

  // Brand comparison
  var cmp = $(".cmp");
  var range = $("#brand-split");
  if (cmp && range) {
    var setSplit = function () { cmp.style.setProperty("--split", range.value + "%"); };
    range.addEventListener("input", setSplit);
    setSplit();
  }

  // Contact address, assembled here so it is not in the HTML as plain text
  $$("[data-mail]").forEach(function (el) {
    var addr = el.getAttribute("data-u") + "@" + el.getAttribute("data-d");
    var a = document.createElement("a");
    a.href = "mailto:" + addr;
    a.className = "mail";
    a.textContent = addr;
    el.replaceWith(a);
  });

  // Demo form, sent to Formspree. Without JavaScript the form posts normally.
  var form = $("#demo-form");
  if (form) {
    var status = $("#form-status");
    var btn = $("button[type=submit]", form);
    var say = function (msg, ok) {
      status.textContent = msg;
      status.className = "form-status " + (ok ? "is-ok" : "is-err");
    };
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if ($("input[name=_gotcha]", form).value) return;
      var name = $("#f-name").value.trim();
      var email = $("#f-email").value.trim();
      if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        say(form.getAttribute("data-msg-invalid"), false);
        return;
      }
      btn.disabled = true;
      var label = btn.textContent;
      btn.textContent = form.getAttribute("data-msg-sending");
      fetch(form.action, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          name: name,
          email: email,
          company: $("#f-company").value.trim(),
          message: $("#f-msg").value.trim(),
          page_lang: root.lang
        })
      }).then(function (res) {
        if (!res.ok) throw new Error("status " + res.status);
        form.reset();
        say(form.getAttribute("data-msg-ok"), true);
        btn.hidden = true;
      }).catch(function () {
        say(form.getAttribute("data-msg-err"), false);
        btn.disabled = false;
        btn.textContent = label;
      });
    });
  }
})();
