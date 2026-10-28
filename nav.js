(function () {
  var btn = document.querySelector(".menu-btn"), nav = document.getElementById("site-nav");
  if (!btn || !nav) return;
  document.documentElement.classList.add("js");
  function set(open) {
    nav.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.querySelector(".lbl").textContent = open ? "Close" : "Menu";
  }
  btn.addEventListener("click", function () { set(!nav.classList.contains("open")); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { set(false); btn.focus(); } });
  document.addEventListener("click", function (e) { if (!nav.contains(e.target) && !btn.contains(e.target)) set(false); });
  nav.addEventListener("click", function (e) { if (e.target.tagName === "A") set(false); });
  window.addEventListener("resize", function () { if (window.innerWidth > 820) set(false); });
})();
