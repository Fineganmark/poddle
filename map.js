(function () {
  if (!window.L || !document.getElementById("map")) return;
  var css = getComputedStyle(document.documentElement);
  var river = css.getPropertyValue("--river").trim() || "#2c6b9a";
  var red = css.getPropertyValue("--antiquity").trim() || "#9b3b2a";

  var map = L.map("map", { scrollWheelZoom: false }).setView([53.318, -6.31], 13);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors"
  }).addTo(map);

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[c]; }); }

  // River line: solid where open, dotted where culverted; the City Watercourse dashed.
  var riverLayer = L.layerGroup();
  DATA.river.forEach(function (w) {
    var isWc = /watercourse/i.test(w.n);
    L.polyline(w.c, {
      color: isWc ? red : river, weight: isWc ? 3 : 4, opacity: 0.9,
      dashArray: isWc ? "8 6" : (w.t ? "2 7" : null), lineCap: "round"
    }).bindTooltip(w.n + (w.t ? " (underground)" : "")).addTo(riverLayer);
  });
  riverLayer.addTo(map);

  // Channels: Abbey Stream, City Watercourse, Tenter Water, Dodder Overflow
  var style = { abbey: { color: "#c98a1b", weight: 9, opacity: 0.45 },
                citywc: { color: red, weight: 3, dashArray: "8 6", opacity: 0.95 },
                tenter: { color: red, weight: 3, dashArray: "3 6", opacity: 0.95 },
                overflow: { color: "#3b8f6a", weight: 4, dashArray: "10 5", opacity: 0.95 } };
  var groups = { abbey: L.layerGroup(), watercourse: L.layerGroup(), overflow: L.layerGroup() };
  (DATA.channels || []).forEach(function (ch) {
    var g = ch.k === "abbey" ? groups.abbey : (ch.k === "overflow" ? groups.overflow : groups.watercourse);
    var lines = ch.k === "abbey" ? ch.c : [ch.c];
    lines.forEach(function (c) {
      L.polyline(c, L.extend({ lineCap: "round" }, style[ch.k])).bindPopup("<div class=\"pop\"><p class=\"pk\">" +
        (ch.approx ? "Approximate route" : "Channel") + "</p><h3>" + esc(ch.n) + "</h3><p>" + esc(ch.note) +
        "</p><a href=\"" + ch.slug + ".html\">Read the history →</a></div>", { maxWidth: 260 }).addTo(g);
    });
  });
  groups.abbey.addTo(map); groups.watercourse.addTo(map); groups.overflow.addTo(map);

  // River walk stops
  var stops = L.layerGroup();
  DATA.stops.forEach(function (s) {
    var icon = L.divIcon({ className: "pin-stop", html: "<span>" + s.n + "</span>", iconSize: [28, 28], iconAnchor: [14, 14] });
    var img = s.img ? "<img src=\"img/" + s.img + ".jpg\" alt=\"\" loading=\"lazy\">" : "";
    L.marker([s.lat, s.lon], { icon: icon, title: s.name, keyboard: true })
      .bindPopup("<div class=\"pop\">" + img + "<p class=\"pk\">Stop " + s.n + " · " + esc(s.place) + "</p><h3>" + esc(s.name) +
        "</h3><p>" + esc(s.teaser) + "</p><a href=\"" + s.slug + ".html\">Read the history →</a></div>", { maxWidth: 260 })
      .addTo(stops);
  });
  stops.addTo(map);

  function simple(list, cls, kicker) {
    var g = L.layerGroup();
    list.forEach(function (m) {
      var icon = L.divIcon({ className: cls, iconSize: [14, 14], iconAnchor: [7, 7] });
      L.marker([m[1], m[2]], { icon: icon, title: m[0] })
        .bindPopup("<div class=\"pop\"><p class=\"pk\">" + kicker + "</p><h3>" + esc(m[0]) + "</h3><p>" + esc(m[3]) + "</p></div>", { maxWidth: 240 })
        .addTo(g);
    });
    return g;
  }
  var mills = simple(DATA.mills, "pin-mill", "Mill site");
  var works = simple(DATA.works, "pin-works", "Flood scheme works");
  mills.addTo(map);

  var gauges = L.layerGroup();
  DATA.gauges.forEach(function (g) {
    var icon = L.divIcon({ className: "pin-gauge", iconSize: [16, 16], iconAnchor: [8, 8] });
    L.marker([g[2], g[3]], { icon: icon, title: g[1] })
      .bindPopup("<div class=\"pop\"><p class=\"pk\">River gauge</p><h3>" + esc(g[1]) + "</h3><p>Office of Public Works station " + g[0] +
        ". <a href=\"river-data.html\">Latest levels →</a></p></div>", { maxWidth: 240 })
      .addTo(gauges);
  });

  L.control.layers(null, {
    "The river": riverLayer, "Abbey Stream": groups.abbey, "City Watercourse and Tenter Water": groups.watercourse, "Dodder Overflow": groups.overflow, "River walk stops": stops, "Mill sites": mills,
    "Flood scheme works": works, "Dodder gauges": gauges
  }, { collapsed: false }).addTo(map);

  var all = L.featureGroup(stops.getLayers());
  map.fitBounds(all.getBounds().pad(0.08));
  map.on("focus", function () { map.scrollWheelZoom.enable(); });
  map.on("blur", function () { map.scrollWheelZoom.disable(); });
})();
