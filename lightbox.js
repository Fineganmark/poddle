/* Pictures open full size in a viewer over the page (Nov 2026). The page itself shows small copies;
   the full-size file only loads when someone clicks. Without JavaScript the links simply open the picture.
   Leaving the viewer must always work on a phone (16 Nov 2026): the X stays in the corner of the screen even
   after a pinch-zoom, a tap anywhere except the "Open full size" link closes it, there is a second Close
   button under the caption, Esc and the phone's Back button close it, and if Back does not answer the viewer
   closes anyway. */
(function () {
  // Every link to a picture file opens in the viewer, including the "Open full size" links under captions.
  // A home-screen icon on an iPhone opens the site with no Back button, so a link that leaves the page for a
  // bare picture file is a dead end there (Mark, 16 Nov 2026). The gallery and map-slideshow thumbnails have
  // their own scripts and are left alone.
  var links = document.querySelectorAll("a.zoom, a[href^='img/']:not(.gal-thumb):not(.ms-thumb)");
  if (!links.length) return;
  var standalone = window.navigator.standalone === true ||
    (window.matchMedia && window.matchMedia("(display-mode: standalone), (display-mode: fullscreen)").matches);
  var box, img, cap, full, xbtn, last, pushed = false, backTimer = null, vv = window.visualViewport;
  function isOn() { return !!box && box.classList.contains("on"); }
  function build() {
    box = document.createElement("div");
    box.className = "lb";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Picture");
    box.innerHTML = '<button class="lb-x" type="button" aria-label="Close picture" title="Close (Esc)">' +
      '<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" focusable="false"><path d="M5 5l14 14M19 5L5 19" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" fill="none"/></svg></button>' +
      '<figure><img alt=""><figcaption><span class="lb-cap"></span> <a class="lb-full">Open full size</a></figcaption>' +
      '<button class="lb-close" type="button">Close picture</button>' +
      '<p class="lb-hint">Tap anywhere to close</p></figure>';
    document.body.appendChild(box);
    img = box.querySelector("img"); cap = box.querySelector(".lb-cap"); full = box.querySelector(".lb-full"); xbtn = box.querySelector(".lb-x");
    // Any tap closes, except on the "Open full size" link.
    box.addEventListener("click", function (e) {
      if (e.target.closest && e.target.closest(".lb-full")) return;
      e.preventDefault();
      close();
    });
    document.addEventListener("keydown", function (e) { if ((e.key === "Escape" || e.key === "Esc") && isOn()) close(); });
    window.addEventListener("popstate", function () { if (isOn()) { pushed = false; hide(); } });
    // Coming back to the page from the full-size picture: never land on a stuck viewer.
    window.addEventListener("pageshow", function (e) { if (e.persisted && isOn()) { pushed = false; hide(); } });
    if (vv) { vv.addEventListener("resize", placeX); vv.addEventListener("scroll", placeX); }
  }
  // After a pinch-zoom a "fixed" button is pinned to the unzoomed page, so it can end up off screen.
  // Keep the X in the top-right corner of what is actually visible, at its normal size.
  function placeX() {
    if (!isOn() || !vv) return;
    var s = vv.scale || 1;
    if (s <= 1.01) { xbtn.style.left = xbtn.style.top = xbtn.style.right = xbtn.style.transform = xbtn.style.transformOrigin = ""; return; }
    xbtn.style.right = "auto";
    xbtn.style.transformOrigin = "0 0";
    xbtn.style.transform = "scale(" + (1 / s) + ")";
    xbtn.style.left = (vv.offsetLeft + vv.width - 64 / s) + "px";
    xbtn.style.top = (vv.offsetTop + 12 / s) + "px";
  }
  function close() {
    if (pushed && history.length > 1) {
      pushed = false;
      history.back();   // popstate then hides the viewer...
      clearTimeout(backTimer);
      backTimer = setTimeout(hide, 350);   // ...and if the browser ignores Back, hide it anyway
    } else { pushed = false; hide(); }
  }
  function hide() {
    clearTimeout(backTimer);
    if (!isOn()) return;
    box.classList.remove("on");
    img.removeAttribute("src");
    document.documentElement.style.overflow = "";
    document.body.style.overflow = "";
    if (last) { try { last.focus({ preventScroll: true }); } catch (err) { last.focus(); } }
  }
  function open(a) {
    if (!box) build();
    // A caption's "Open full size" link opens the same view as tapping its picture.
    if (!a.querySelector("img")) { var f0 = a.closest("figure"), z = f0 && f0.querySelector("a.zoom, a[href^='img/'] > img"); if (z) a = z.tagName === "IMG" ? z.parentNode : z; }
    last = a;
    var fig = a.closest("figure"), fc = fig && fig.querySelector("figcaption"), t = "";
    if (fc) { var c = fc.cloneNode(true); var x = c.querySelectorAll("a"); for (var i = 0; i < x.length; i++) if (/open full size/i.test(x[i].textContent)) x[i].parentNode.removeChild(x[i]); t = c.textContent.trim(); }
    var thumb = a.querySelector("img");
    if (!t && thumb) t = thumb.alt;
    if (thumb) img.src = thumb.currentSrc || thumb.src;   // show the small copy at once, then swap in the full size
    var big = new Image();
    big.onload = function () { if (isOn() && last === a) img.src = big.src; };
    big.src = a.getAttribute("href");
    img.alt = thumb ? thumb.alt : "";
    img.style.filter = thumb ? getComputedStyle(thumb).filter : "";
    cap.textContent = t;
    full.href = a.getAttribute("href");
    full.style.display = standalone ? "none" : "";   // no Back button to return from the bare file
    box.scrollTop = 0;
    box.classList.add("on");
    placeX();
    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
    if (!pushed && history.pushState) { try { history.pushState({ lb: 1 }, ""); pushed = true; } catch (err) {} }
    try { xbtn.focus({ preventScroll: true }); } catch (err) { xbtn.focus(); }
  }
  for (var i = 0; i < links.length; i++) links[i].addEventListener("click", function (e) {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault(); open(this);
  });
})();
