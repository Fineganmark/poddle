/* Site search for poddle.ie: reads search-index.json (built by build.py) and searches it in the browser. */
(function () {
  var form = document.querySelector(".site-search"), input = document.getElementById("q"),
      out = document.getElementById("search-results"), status = document.getElementById("search-status");
  if (!form || !input || !out) return;
  var docs = null, loading = null;

  function fold(s) { return s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[’‘]/g, "'").toLowerCase(); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function load() {
    if (!loading) loading = fetch("search-index.json").then(function (r) { return r.json(); }).then(function (d) {
      docs = d.map(function (p) {
        return { u: p.u, t: p.t, ft: fold(p.t), s: p.s.map(function (x) { return { id: x[0], h: x[1], b: x[2], fh: fold(x[1]), fb: fold(x[2]) }; }) };
      });
    });
    return loading;
  }
  function terms(q) {
    return fold(q).replace(/[^a-z0-9' ]+/g, " ").split(/\s+/).filter(function (w) { return w.length > 1 || /\d/.test(w); });
  }
  function count(hay, re) { var m = hay.match(re); return m ? m.length : 0; }
  function snippet(text, ftext, res) {
    var at = -1;
    for (var i = 0; i < res.length && at < 0; i++) { var m = res[i].exec(ftext); res[i].lastIndex = 0; if (m) at = m.index; }
    var start = Math.max(0, at - 70), end = Math.min(text.length, start + 220);
    if (start > 0) { var sp = text.indexOf(" ", start); if (sp > -1 && sp < at) start = sp + 1; }
    var piece = text.slice(start, end), fpiece = fold(piece), html = "", last = 0, marks = [];
    res.forEach(function (re) { var m; while ((m = re.exec(fpiece))) { marks.push([m.index, m.index + m[0].length]); } re.lastIndex = 0; });
    marks.sort(function (a, b) { return a[0] - b[0]; });
    marks.forEach(function (m) { if (m[0] < last) return; html += esc(piece.slice(last, m[0])) + "<mark>" + esc(piece.slice(m[0], m[1])) + "</mark>"; last = m[1]; });
    html += esc(piece.slice(last));
    return (start > 0 ? "… " : "") + html + (end < text.length ? " …" : "");
  }
  function run(q) {
    var ts = terms(q);
    out.innerHTML = "";
    if (!ts.length) { status.textContent = ""; return; }
    var res = ts.map(function (w) { return new RegExp("\\b" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g"); });
    var hits = [];
    docs.forEach(function (p) {
      var best = null, total = 0;
      var pageAll = res.every(function (re) { var ok = re.test(p.ft) || p.s.some(function (x) { re.lastIndex = 0; return re.test(x.fh) || re.test(x.fb); }); re.lastIndex = 0; return ok; });
      if (!pageAll) return;
      p.s.forEach(function (x) {
        var sc = 0, all = true;
        res.forEach(function (re) {
          var n = count(p.ft, re) * 12 + count(x.fh, re) * 6 + Math.min(count(x.fb, re), 8);
          if (!n) all = false; sc += n;
        });
        if (all) sc *= 2;
        total += sc;
        if (sc && (!best || sc > best.sc)) best = { x: x, sc: sc };
      });
      if (!best) return;
      hits.push({ p: p, best: best, score: total + best.sc });
    });
    hits.sort(function (a, b) { return b.score - a.score; });
    status.textContent = hits.length ? (hits.length + (hits.length === 1 ? " page" : " pages") + " found for “" + q + "”") : "Nothing found for “" + q + "”. Try a shorter or different word.";
    out.innerHTML = hits.slice(0, 40).map(function (h) {
      var x = h.best.x, href = h.p.u + (x.id ? "#" + x.id : "");
      var where = x.h && x.h !== h.p.t ? '<span class="sr-sec">' + esc(x.h) + "</span>" : "";
      return '<li><a href="' + esc(href) + '"><strong>' + esc(h.p.t) + "</strong>" + where + "</a><p>" + snippet(x.b || x.h, x.fb || x.fh, res) + "</p></li>";
    }).join("");
  }
  function go(q, push) {
    status.textContent = "Searching…";
    load().then(function () { run(q); }).catch(function () { status.textContent = "Search could not load. Please try again."; });
    if (push) history.replaceState(null, "", "search.html" + (q ? "?q=" + encodeURIComponent(q) : ""));
  }
  form.addEventListener("submit", function (e) { e.preventDefault(); go(input.value.trim(), true); });
  var t;
  input.addEventListener("input", function () { clearTimeout(t); var v = input.value.trim(); t = setTimeout(function () { if (v.length > 1) go(v, true); else { out.innerHTML = ""; status.textContent = ""; } }, 250); });
  var q0 = new URLSearchParams(location.search).get("q");
  if (q0) { input.value = q0; go(q0, false); } else { input.focus(); load(); }
})();
