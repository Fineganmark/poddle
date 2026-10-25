(function () {
  var box = document.getElementById("gauges");
  if (!box) return;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[c]; }); }

  function chart(points) {
    // points: [[isoTime, value], ...]; simple SVG line with min/max labels
    var W = 600, H = 150, P = 6;
    var vals = points.map(function (p) { return p[1]; });
    var min = Math.min.apply(null, vals), max = Math.max.apply(null, vals);
    if (max - min < 0.05) { max += 0.025; min -= 0.025; }
    var x = function (i) { return P + (W - 2 * P) * i / Math.max(1, points.length - 1); };
    var y = function (v) { return H - P - (H - 2 * P) * (v - min) / (max - min); };
    var d = points.map(function (p, i) { return (i ? "L" : "M") + x(i).toFixed(1) + " " + y(p[1]).toFixed(1); }).join(" ");
    var area = d + " L" + x(points.length - 1).toFixed(1) + " " + (H - P) + " L" + x(0).toFixed(1) + " " + (H - P) + " Z";
    return "<svg viewBox=\"0 0 " + W + " " + H + "\" preserveAspectRatio=\"none\" class=\"spark\" role=\"img\" aria-label=\"Water level over the last seven days, from " +
      min.toFixed(2) + " to " + max.toFixed(2) + " metres\"><path class=\"a\" d=\"" + area + "\"/><path class=\"l\" d=\"" + d + "\"/>" +
      "<circle class=\"e\" cx=\"" + x(points.length - 1).toFixed(1) + "\" cy=\"" + y(vals[vals.length - 1]).toFixed(1) + "\" r=\"4\"/></svg>" +
      "<div class=\"range\"><span>Low " + min.toFixed(2) + " m</span><span>High " + max.toFixed(2) + " m</span></div>";
  }

  fetch("data/levels.json", { cache: "no-store" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) {
      var html = data.stations.map(function (s) {
        var last = s.points[s.points.length - 1];
        var when = new Date(last[0] + "Z").toLocaleString("en-IE", { weekday: "short", hour: "2-digit", minute: "2-digit", timeZone: "Europe/Dublin" });
        return "<article class=\"gauge\"><header><h3>" + esc(s.name) + "</h3><p class=\"now\"><strong>" + last[1].toFixed(2) +
          " m</strong> at " + esc(when) + "</p></header>" + chart(s.points) +
          "<p class=\"src\"><a href=\"https://waterlevel.ie/00000" + s.ref + "/0001/\" rel=\"noopener\">Station " + esc(s.ref) + " on waterlevel.ie →</a></p></article>";
      }).join("");
      box.innerHTML = html + "<p class=\"note\">Updated " + esc(new Date(data.updated).toLocaleString("en-IE", { dateStyle: "medium", timeStyle: "short", timeZone: "Europe/Dublin" })) + ".</p>";
    })
    .catch(function () {
      box.innerHTML = "<p class=\"muted\">Live readings aren’t available here right now. See the gauges directly on " +
        "<a href=\"https://waterlevel.ie/0000009010/0001/\" rel=\"noopener\">Waldron’s Bridge</a> and " +
        "<a href=\"https://waterlevel.ie/0000009369/0001/\" rel=\"noopener\">Anglesea Road</a>.</p>";
    });
})();
