/* Pictures open full size in a viewer over the page (Nov 2026). The page itself shows small copies;
   the full-size file only loads when someone clicks. Without JavaScript the links simply open the picture. */
(function () {
  var links = document.querySelectorAll("a.zoom, figure.fig > a[href^='img/']");
  if (!links.length) return;
  var box, img, cap, full, last;
  function build() {
    box = document.createElement("div");
    box.className = "lb";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Picture");
    box.innerHTML = '<button class="lb-x" type="button" aria-label="Close">×</button>' +
      '<figure><img alt=""><figcaption><span class="lb-cap"></span> <a class="lb-full" target="_blank" rel="noopener">Open full size</a></figcaption></figure>';
    document.body.appendChild(box);
    img = box.querySelector("img"); cap = box.querySelector(".lb-cap"); full = box.querySelector(".lb-full");
    box.addEventListener("click", function (e) { if (e.target === box || e.target.className === "lb-x") close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && box.classList.contains("on")) close(); });
  }
  function close() {
    box.classList.remove("on");
    img.removeAttribute("src");
    document.documentElement.style.overflow = "";
    if (last) last.focus();
  }
  function open(a) {
    if (!box) build();
    last = a;
    var fig = a.closest("figure"), fc = fig && fig.querySelector("figcaption"), t = "";
    if (fc) { var c = fc.cloneNode(true); var x = c.querySelectorAll("a"); for (var i = 0; i < x.length; i++) if (/open full size/i.test(x[i].textContent)) x[i].remove(); t = c.textContent.trim(); }
    var thumb = a.querySelector("img");
    if (!t && thumb) t = thumb.alt;
    if (thumb) img.src = thumb.currentSrc || thumb.src;   // show the small copy at once, then swap in the full size
    var big = new Image();
    big.onload = function () { if (box.classList.contains("on") && last === a) img.src = big.src; };
    big.src = a.getAttribute("href");
    img.alt = thumb ? thumb.alt : "";
    img.style.filter = thumb ? getComputedStyle(thumb).filter : "";
    cap.textContent = t;
    full.href = a.getAttribute("href");
    box.classList.add("on");
    document.documentElement.style.overflow = "hidden";
    box.querySelector(".lb-x").focus();
  }
  for (var i = 0; i < links.length; i++) links[i].addEventListener("click", function (e) {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault(); open(this);
  });
})();
