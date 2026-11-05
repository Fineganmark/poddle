/* History page: the Dublin maps cross-fade in order; the dated thumbnails show one.
   Picking a thumbnail stops the slideshow (the Play button restarts it). People who ask
   for reduced motion get no autoplay and no fade; the thumbnails still work. */
(function () {
  var box = document.querySelector(".map-show");
  if (!box) return;
  var slides = box.querySelectorAll(".ms-slide"), thumbs = box.querySelectorAll(".ms-thumb");
  var cap = box.querySelector(".ms-cap"), btn = box.querySelector(".ms-play");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var cur = 0, timer = null, playing = !reduce, DELAY = 5000;

  function show(i) {
    cur = (i + slides.length) % slides.length;
    for (var k = 0; k < slides.length; k++) {
      var on = k === cur;
      slides[k].classList.toggle("on", on);
      if (on) slides[k].removeAttribute("aria-hidden"); else slides[k].setAttribute("aria-hidden", "true");
      if (on) thumbs[k].setAttribute("aria-current", "true"); else thumbs[k].removeAttribute("aria-current");
    }
    cap.textContent = slides[cur].getAttribute("data-cap") || slides[cur].querySelector("img").alt.split(",")[0];
  }
  function tick() { show(cur + 1); }
  function setPlaying(p) {
    playing = p;
    clearInterval(timer); timer = null;
    if (p) timer = setInterval(tick, DELAY);
    btn.textContent = p ? "Pause" : "Play";
    btn.setAttribute("aria-pressed", p ? "false" : "true");
    btn.setAttribute("aria-label", p ? "Pause the maps" : "Play the maps in order");
  }

  for (var k = 0; k < thumbs.length; k++) {
    thumbs[k].addEventListener("click", function (e) {
      e.preventDefault();
      show(+this.getAttribute("data-i"));
      if (playing) setPlaying(false);
    });
  }
  btn.hidden = false;
  btn.addEventListener("click", function () {
    if (!playing) show(cur + 1);
    setPlaying(!playing);
  });
  document.addEventListener("visibilitychange", function () {
    if (!playing) return;
    clearInterval(timer); timer = null;
    if (!document.hidden) timer = setInterval(tick, DELAY);
  });
  // preload the other maps so the first fades are smooth
  for (var j = 1; j < slides.length; j++) slides[j].querySelector("img").loading = "eager";
  setPlaying(playing);
})();
