(function () {
  if (!window.L || typeof PLAN === "undefined" || !document.getElementById("planmap")) return;
  var css = getComputedStyle(document.documentElement);
  var river = css.getPropertyValue("--river").trim() || "#2c6b9a";
  var red = css.getPropertyValue("--antiquity").trim() || "#9b3b2a";
  var map = L.map("planmap", { scrollWheelZoom: false }).setView([53.3395, -6.283], 14);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19,
    attribution: "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors" }).addTo(map);
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[c]; }); }
  PLAN.river.forEach(function (w) {
    var wc = /watercourse/i.test(w.n);
    L.polyline(w.c, { color: wc ? red : river, weight: wc ? 3 : 4, opacity: 0.85, dashArray: wc ? "8 6" : (w.t ? "2 7" : null) }).addTo(map);
  });
  var bounds = [];
  var dirs = { "2768/09": ["bottom", [0, 10]], "4423/19": ["top", [0, -10]], "4156/06": ["bottom", [0, 10]], "4223/18": ["left", [-10, 0]] };
  PLAN.files.forEach(function (f) {
    var d = dirs[f[0]] || ["right", [10, 0]];
    var icon = L.divIcon({ className: "pin-dig", iconSize: [18, 18], iconAnchor: [9, 9] });
    L.marker([f[2], f[3]], { icon: icon, title: f[0] + " " + f[1], keyboard: true })
      .bindTooltip(f[0] + " · " + f[1], { permanent: true, direction: d[0], offset: d[1], className: "plan-tip" })
      .bindPopup("<div class=\"pop\"><p class=\"pk\">Planning ref " + esc(f[0]) + "</p><h3>" + esc(f[1]) + "</h3><p>" + esc(f[4]) +
        "</p><a href=\"#" + f[5] + "\">Read this section ↓</a></div>", { maxWidth: 260 }).addTo(map);
    bounds.push([f[2], f[3]]);
  });
  map.fitBounds(bounds, { padding: [60, 60], maxZoom: 15 });
})();
