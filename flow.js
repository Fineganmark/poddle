// Small arrowheads along the water lines, pointing downstream (the way each line is drawn).
// poddleFlow(map, [{ group, color, lines: [[latlng, ...], ...], weight }]) draws them into each
// group, so they show and hide with that layer, and redraws them at every zoom or pan.
(function () {
  function key(p) { return p[0].toFixed(5) + "," + p[1].toFixed(5); }

  // The river comes in many short pieces; join the ones that run on from each other,
  // so the arrows are spaced evenly along the whole course rather than piece by piece.
  function chain(lines) {
    var left = lines.map(function (l) { return l.slice(); }), out = [];
    while (left.length) {
      var cur = left.shift(), grew = true;
      while (grew) {
        grew = false;
        for (var i = 0; i < left.length; i++) {
          if (key(left[i][0]) === key(cur[cur.length - 1])) { cur = cur.concat(left[i].slice(1)); left.splice(i, 1); grew = true; break; }
          if (key(left[i][left[i].length - 1]) === key(cur[0])) { cur = left[i].concat(cur.slice(1)); left.splice(i, 1); grew = true; break; }
        }
      }
      out.push(cur);
    }
    return out;
  }

  window.poddleFlow = function (map, sets) {
    var gap = window.matchMedia && matchMedia("(max-width: 760px)").matches ? 85 : 110;
    sets.forEach(function (s) { s.chains = chain(s.lines); s.drawn = []; });

    function draw() {
      var view = map.getBounds().pad(0.25);
      sets.forEach(function (s) {
        s.drawn.forEach(function (l) { s.group.removeLayer(l); });
        s.drawn = [];
        var arm = (s.size || 6) + (s.weight || 3) / 2;
        s.chains.forEach(function (c) {
          var pts = c.map(function (p) { return map.latLngToLayerPoint(p); });
          var next = gap / 2; // first arrow half a gap in, then one every gap
          var run = 0;
          for (var i = 1; i < pts.length; i++) {
            var a = pts[i - 1], b = pts[i], dx = b.x - a.x, dy = b.y - a.y, len = Math.sqrt(dx * dx + dy * dy);
            if (!len) continue;
            while (run + len >= next) {
              var t = (next - run) / len, x = a.x + dx * t, y = a.y + dy * t;
              var ux = dx / len, uy = dy / len, tip = L.point(x + ux * arm * 0.45, y + uy * arm * 0.45);
              var ll = map.layerPointToLatLng(tip);
              if (view.contains(ll)) {
                // An open chevron: two short strokes swept back from the tip, about 70 degrees apart.
                var bx = -ux * arm, by = -uy * arm, c35 = 0.819, s35 = 0.574;
                var p1 = L.point(tip.x + bx * c35 - by * s35, tip.y + bx * s35 + by * c35);
                var p2 = L.point(tip.x + bx * c35 + by * s35, tip.y - bx * s35 + by * c35);
                var head = L.polyline([map.layerPointToLatLng(p1), ll, map.layerPointToLatLng(p2)], {
                  color: s.color, weight: s.stroke || 2.5, opacity: 1, lineCap: "round", lineJoin: "round",
                  interactive: false, className: "flow-arrow"
                });
                s.group.addLayer(head);
                s.drawn.push(head);
              }
              next += gap;
            }
            run += len;
          }
        });
      });
    }
    map.on("moveend", draw);
    draw();
  };
})();
