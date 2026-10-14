// Applies the theme the visitor chose, before the first paint. Without a choice, the CSS follows the system.
(function () {
  try {
    var t = localStorage.getItem("zm-theme");
    if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t);
  } catch (e) {}
})();
