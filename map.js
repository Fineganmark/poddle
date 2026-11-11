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
  var riverLayer = L.layerGroup(), riverLines = [], riverWc = [];
  DATA.river.forEach(function (w) {
    var isWc = /watercourse/i.test(w.n);
    (isWc ? riverWc : riverLines).push(w.c);
    L.polyline(w.c, {
      color: isWc ? red : river, weight: isWc ? 3 : 4, opacity: 0.9,
      dashArray: isWc ? "8 6" : (w.t ? "2 7" : null), lineCap: "round"
    }).bindTooltip(w.n + (w.t ? " (underground)" : "")).addTo(riverLayer);
  });
  riverLayer.addTo(map);

  // Channels: Abbey Stream, City Watercourse, Tenter Water, Commons Water, Dodder Overflow
  var style = { abbey: { color: "#c98a1b", weight: 9, opacity: 0.45 },
                citywc: { color: red, weight: 3, dashArray: "8 6", opacity: 0.95 },
                tenter: { color: red, weight: 3, dashArray: "3 6", opacity: 0.95 },
                commons: { color: "#2a7f9e", weight: 3, dashArray: "6 5", opacity: 0.95 },
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

  // Arrowheads along every water line, pointing downstream.
  if (window.poddleFlow) {
    var flow = [{ group: riverLayer, color: river, weight: 4, lines: riverLines },
                { group: riverLayer, color: red, weight: 3, lines: riverWc }];
    var tint = { abbey: "#9a6512", citywc: red, tenter: red, commons: "#2a7f9e", overflow: "#3b8f6a" };
    (DATA.channels || []).forEach(function (ch) {
      flow.push({ group: ch.k === "abbey" ? groups.abbey : (ch.k === "overflow" ? groups.overflow : groups.watercourse),
                  color: tint[ch.k], weight: style[ch.k].weight, lines: ch.k === "abbey" ? ch.c : [ch.c] });
    });
    poddleFlow(map, flow);
  }

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

  var byId = {};
  function simple(list, cls, kicker) {
    var g = L.layerGroup();
    list.forEach(function (m) {
      var icon = L.divIcon({ className: cls, iconSize: [14, 14], iconAnchor: [7, 7] });
      L.marker([m[1], m[2]], { icon: icon, title: m[0] })
        .bindPopup("<div class=\"pop\"><p class=\"pk\">" + kicker + "</p><h3>" + esc(m[0]) + "</h3><p>" + esc(m[3]) + "</p>" + (m[4] && kicker === "Mill site" ? "<a href=\"mill-sites.html#" + m[4] + "\">Read about this mill →</a> · <a href=\"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=" + m[1] + "," + m[2] + "\" rel=\"noopener\">Street View →</a>" : "") + "</div>", { maxWidth: 240 })
        .addTo(g);
      byId[m[4] || m[0]] = g.getLayers()[g.getLayers().length - 1];
    });
    return g;
  }
  var mills = simple(DATA.mills, "pin-mill", "Mill site");
  var works = simple(DATA.works, "pin-works", "Flood scheme works");
  var digs = simple(DATA.digs || [], "pin-dig", "Archaeological dig");
  (DATA.digs || []).forEach(function (d, i) { digs.getLayers()[i].bindPopup("<div class=\"pop\"><p class=\"pk\">" + esc(d[5] || "Archaeological site") + "</p><h3>" + esc(d[0]) + "</h3><p>" + esc(d[3]) + "</p><a href=\"" + d[4] + ".html\">What the planning file says →</a></div>", { maxWidth: 240 }); });
  mills.addTo(map);

  // Where the river and the City Watercourse pass the Grand Canal
  var crossings = L.layerGroup();
  (DATA.crossings || []).forEach(function (c) {
    var icon = L.divIcon({ className: "pin-cross", iconSize: [16, 16], iconAnchor: [8, 8] });
    var img = c[5] ? "<img src=\"img/" + c[5] + "\" alt=\"Diagram of the siphon\" loading=\"lazy\">" : "";
    L.marker([c[1], c[2]], { icon: icon, title: c[0] })
      .bindPopup("<div class=\"pop\">" + img + "<p class=\"pk\">Canal crossing</p><h3>" + esc(c[0]) + "</h3><p>" + esc(c[3]) +
        "</p><a href=\"" + c[4] + "\">How it works →</a></div>", { maxWidth: 280 })
      .addTo(crossings);
  });
  crossings.addTo(map);

  var gauges = L.layerGroup();
  DATA.gauges.forEach(function (g) {
    var icon = L.divIcon({ className: "pin-gauge", iconSize: [16, 16], iconAnchor: [8, 8] });
    L.marker([g[2], g[3]], { icon: icon, title: g[1] })
      .bindPopup("<div class=\"pop\"><p class=\"pk\">River gauge</p><h3>" + esc(g[1]) + "</h3><p>Office of Public Works station " + g[0] +
        ". <a href=\"river-data.html\">Latest levels →</a></p></div>", { maxWidth: 240 })
      .addTo(gauges);
  });

  // Landmarks from the Crumlin and Walkinstown History Group's Poddle archive
  var places = L.layerGroup(), placeById = {};
  (DATA.landmarks || []).forEach(function (p) {
    var icon = L.divIcon({ className: "pin-place", iconSize: [12, 12], iconAnchor: [6, 6] });
    var mk = L.marker([p[1], p[2]], { icon: icon, title: p[0] })
      .bindPopup("<div class=\"pop\"><p class=\"pk\">Poddle archive</p><h3>" + esc(p[0]) + "</h3><p>" + esc(p[3]) + "</p><a href=\"place-" + p[4] + ".html\">Read more →</a></div>", { maxWidth: 240 })
      .addTo(places);
    placeById[p[4]] = mk;
  });

  var layerCtl = L.control.layers(null, {
    "The river": riverLayer, "Abbey Stream": groups.abbey, "City Watercourse, Tenter and Commons Waters": groups.watercourse, "Dodder Overflow": groups.overflow, "River walk stops": stops, "Mill sites": mills, "Canal crossings": crossings,
    "Flood scheme works": works, "Archaeology and monuments": digs, "Poddle archive places": places, "Dodder gauges": gauges
  }, { collapsed: false }).addTo(map);
  // The tick boxes sit in the box below the map, so they never cover it.
  var below = document.getElementById("layers");
  if (below) below.appendChild(layerCtl.getContainer());

  var all = L.featureGroup(stops.getLayers());
  function home() { map.fitBounds(all.getBounds().pad(0.08)); }
  home();
  if (window.poddleMapSafe) poddleMapSafe(map, home);
  var q = /[?&]mill=([\w-]+)/.exec(location.search);
  if (q && byId[q[1]]) { var mk = byId[q[1]]; map.setView(mk.getLatLng(), 17); mk.openPopup(); }
  if (/[?&]layer=places/.test(location.search)) { places.addTo(map); map.fitBounds(L.featureGroup(places.getLayers()).getBounds().pad(0.05)); }
  var pq = /[?&]place=([\w-]+)/.exec(location.search);
  if (pq && placeById[pq[1]]) { places.addTo(map); map.setView(placeById[pq[1]].getLatLng(), 16); placeById[pq[1]].openPopup(); }
})();
