/* Pictures open full size in a viewer over the page (Nov 2026). The page itself shows small copies;
   the full-size file only loads when someone clicks. Without JavaScript the links simply open the picture. */
(function () {
  var links = document.querySelectorAll("a.zoom, figure.fig > a[href^='img/']");
  if (!links.length) return;
  var box, img, cap, full, last, pushed = false;
  function build() {
    box = document.createElement("div");
    box.className = "lb";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Picture");
    // A large, high-contrast close button kept clear of the phone's notch and status bar (see .lb-x in site.css).
    box.innerHTML = '<button class="lb-x" type="button" aria-label="Close picture" title="Close (Esc)">' +
      '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><path d="M5 5l14 14M19 5L5 19" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" fill="none"/></svg></button>' +
      '<figure><img alt=""><figcaption><span class="lb-cap"></span> <a class="lb-full">Open full size</a></figcaption></figure>';
    document.body.appendChild(box);
    img = box.querySelector("img"); cap = box.querySelector(".lb-cap"); full = box.querySelector(".lb-full");
    // Close with the X, by tapping the dark background or the picture itself, with Esc, or with the phone's Back button.
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target === img || e.target.closest(".lb-x")) close();
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && box.classList.contains("on")) close(); });
    window.addEventListener("popstate", function () { if (box.classList.contains("on")) { pushed = false; hide(); } });
  }
  function close() {
    if (pushed) { pushed = false; history.back(); }   // popstate then hides the viewer
    else hide();
  }
  function hide() {
    if (!box.classList.contains("on")) return;
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
    if (!pushed && history.pushState) { try { history.pushState({ lb: 1 }, ""); pushed = true; } catch (err) {} }
    box.querySelector(".lb-x").focus();
  }
  for (var i = 0; i < links.length; i++) links[i].addEventListener("click", function (e) {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault(); open(this);
  });
})();
