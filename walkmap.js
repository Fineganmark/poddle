// Map for a school walk page: the river nearby (solid open, dotted underground),
// flow arrows, and the numbered stops. Data comes from WALK, written by build_walks.py.
(function () {
  if (!window.L || !window.WALK || !document.getElementById("map")) return;
  var css = getComputedStyle(document.documentElement);
  var river = css.getPropertyValue("--river").trim() || "#2c6b9a";
  var map = L.map("map", { scrollWheelZoom: false });
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors"
  }).addTo(map);

  var water = L.layerGroup().addTo(map), open = [];
  WALK.river.forEach(function (w) {
    if (/watercourse/i.test(w.n)) return;
    L.polyline(w.c, { color: river, weight: 4, opacity: 0.9, dashArray: w.t ? "2 7" : null, lineCap: "round" })
      .bindTooltip(w.n + (w.t ? " (underground)" : "")).addTo(water);
    open.push(w.c);
  });

  var pins = [];
  WALK.stops.forEach(function (s) {
    var icon = L.divIcon({ className: "pin-stop", html: "<span>" + s.n + "</span>", iconSize: [28, 28], iconAnchor: [14, 14] });
    var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[c]; }); };
    pins.push(L.marker([s.lat, s.lon], { icon: icon, title: s.name, keyboard: true })
      .bindPopup("<div class=\"pop\"><p class=\"pk\">Stop " + s.n + "</p><h3>" + esc(s.name) + "</h3><p>" + esc(s.where) +
        "</p><a href=\"#stop-" + s.n + "\">What to see →</a></div>", { maxWidth: 240 })
      .addTo(map));
  });
  var all = L.featureGroup(pins);
  function home() { map.fitBounds(all.getBounds().pad(0.15)); }
  home();
  if (window.poddleFlow) poddleFlow(map, [{ group: water, color: river, lines: open, weight: 4 }]);
  if (window.poddleMapSafe) poddleMapSafe(map, home);
})();
