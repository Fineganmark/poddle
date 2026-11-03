// Stops the page's maps from trapping visitors. On touch screens one finger
// scrolls the page and two fingers move or zoom the map; on desktop the mouse
// wheel scrolls the page and Ctrl (or Cmd) + wheel zooms the map. A "Whole
// map" button puts the view back to where it started.
window.poddleMapSafe = function (map, reset) {
  var box = map.getContainer();
  var touch = window.matchMedia && matchMedia("(pointer: coarse)").matches;
  var mac = /Mac|iP(hone|ad|od)/.test(navigator.platform || navigator.userAgent);
  var hint = L.DomUtil.create("div", "map-hint", box);
  hint.setAttribute("aria-hidden", "true");
  hint.textContent = touch ? "Use two fingers to move the map" : "Use " + (mac ? "⌘" : "Ctrl") + " + scroll to zoom the map";
  var timer;
  function show() {
    L.DomUtil.addClass(hint, "on");
    clearTimeout(timer);
    timer = setTimeout(function () { L.DomUtil.removeClass(hint, "on"); }, 1400);
  }

  map.scrollWheelZoom.disable();
  box.addEventListener("wheel", function (e) {
    if (e.ctrlKey || e.metaKey) { map.scrollWheelZoom.enable(); L.DomUtil.removeClass(hint, "on"); }
    else { map.scrollWheelZoom.disable(); show(); }
  }, { capture: true, passive: true });

  if (touch) {
    // With dragging off, Leaflet leaves touch-action as pan-x pan-y, so the
    // browser scrolls the page with one finger; the two-finger pinch still
    // moves and zooms the map.
    map.dragging.disable();
    if (map.tap) map.tap.disable();
    var one = false;
    box.addEventListener("touchstart", function (e) { one = e.touches.length === 1; }, { passive: true });
    box.addEventListener("touchmove", function (e) {
      if (one && e.touches.length === 1) show(); else { one = false; L.DomUtil.removeClass(hint, "on"); }
    }, { passive: true });
  }

  var Home = L.Control.extend({
    options: { position: "topleft" },
    onAdd: function () {
      var wrap = L.DomUtil.create("div", "leaflet-bar map-home");
      var a = L.DomUtil.create("a", "", wrap);
      a.href = "#"; a.setAttribute("role", "button");
      a.title = "Show the whole map"; a.setAttribute("aria-label", "Show the whole map");
      a.innerHTML = "<svg viewBox=\"0 0 20 20\" width=\"16\" height=\"16\" aria-hidden=\"true\"><path d=\"M3 8V3h5M17 8V3h-5M3 12v5h5M17 12v5h-5\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"/></svg>";
      L.DomEvent.disableClickPropagation(wrap);
      L.DomEvent.on(a, "click", function (e) { L.DomEvent.preventDefault(e); map.closePopup(); reset(); });
      return wrap;
    }
  });
  map.addControl(new Home());
};
