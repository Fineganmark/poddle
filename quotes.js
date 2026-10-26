(function () {
  var stage = document.getElementById("quotes");
  if (!stage) return;
  var items = Array.prototype.slice.call(stage.querySelectorAll(".q"));
  if (items.length < 2) return;
  var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var i = 0, timer = null, paused = false;
  stage.classList.add("js");
  // Reserve height for the tallest quote so the page doesn't jump.
  function size() {
    var h = 0;
    items.forEach(function (q) { q.style.position = "static"; q.style.visibility = "hidden"; q.style.display = "block"; h = Math.max(h, q.offsetHeight); q.style.cssText = ""; });
    stage.style.minHeight = h + "px";
  }
  size();
  window.addEventListener("resize", size);
  function show(n) {
    items[i].classList.remove("on");
    i = n;
    items[i].classList.add("on");
  }
  function next() { if (!paused) show((i + 1) % items.length); }
  function wait() { return Math.min(14000, 5200 + items[i].textContent.length * 38); }
  function loop() { timer = setTimeout(function () { next(); loop(); }, wait()); }
  stage.addEventListener("mouseenter", function () { paused = true; });
  stage.addEventListener("mouseleave", function () { paused = false; });
  stage.addEventListener("focusin", function () { paused = true; });
  stage.addEventListener("focusout", function () { paused = false; });
  document.addEventListener("visibilitychange", function () { paused = document.hidden; });
  if (calm) stage.classList.add("calm");
  loop();
})();
