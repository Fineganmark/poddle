# The Crumlin and Walkinstown History Group's Poddle archive, merged into poddle.ie
# with the group's agreement (November 2026). Their text is kept as they wrote it.
# Source files are in data/crumlin/ (taken from poddle.crumlinwalkinstownhistory.ie).
import json as _json

ARCH_DIR = os.path.join(OUT, "data", "crumlin")
CWHG = "Crumlin and Walkinstown History Group"
CWHG_URL = "https://poddle.crumlinwalkinstownhistory.ie/"
CWHG_HOME = "https://www.crumlinwalkinstownhistory.ie/"
VOLUNTEERS = "Aidan, Bernadette, Brendan, Carol, Kevin, Margaret, Mary, Michele, Sally-Anne and Trevor"
CREDIT = (f'<aside class="arch-credit"><p>From the <a href="archive.html">Poddle archive</a> of the '
          f'<a href="{CWHG_HOME}" rel="noopener">{CWHG}</a> and Crumlin Community Cleanup, researched and written by their volunteers '
          f'and first published in October 2024. It appears here with their permission. '
          f'Corrections and new material are welcome at <a href="mailto:crumlinwalkinstownhistory@gmail.com">crumlinwalkinstownhistory@gmail.com</a> '
          f'or <a href="about.html#contact">through this site</a>.</p></aside>')

def _arch(name):
    with open(os.path.join(ARCH_DIR, name), encoding="utf-8") as fh:
        return fh.read()

def _is_head(line):
    t = line.strip()
    return (0 < len(t) < 70 and not t.endswith((".", ":", ",", ";", "”", "\"", "…", ")")) and not t.lower().startswith(("source", "see more", "read more", "view ")))

def _blocks(lines):
    """Turn a run of lines into (heading, [paragraphs]) sections."""
    secs, head, paras = [], None, []
    for ln in lines:
        t = ln.strip()
        if not t or t == ".":
            continue
        if _is_head(ln):
            if paras or head:
                secs.append((head, paras))
            head, paras = t, []
        else:
            paras.append(t)
    if paras or head:
        secs.append((head, paras))
    return [(h, ps) for h, ps in secs if ps or h]

def _p(t):
    t = esc(t)
    t = re.sub(r'(https?://[^\s<“”"]+?)([.,)]?)(?=\s|$)', r'<a href="\1" rel="noopener">\1</a>\2', t)
    if t.lower().startswith("source"):
        return f'<p class="src">{t}</p>'
    return f"<p>{t}</p>"

def _secs_html(secs):
    out = []
    for h, ps in secs:
        hh = (f'<h2 id="{slug_id(h)}">{esc(h)}</h2>' if ps else f'<h2 class="arch-part" id="{slug_id(h)}">{esc(h)}</h2>') if h else ""
        out.append(f'<section>{hh}{"".join(_p(p) for p in ps)}</section>')
    return "\n".join(out)

# ---- landmarks: map pins and one page each
MARKERS = {}
for ln in _arch("markers.md").splitlines():
    c = [x.strip() for x in ln.strip().strip("|").split("|")]
    if len(c) == 7 and c[1][:1].isdigit():
        MARKERS[c[0].replace("  ", " ")] = dict(lat=float(c[1]), lon=float(c[2]), parts=c[4], desc=c[6].replace("\\n", " ").strip())

PLACES = []
for chunk in _arch("text-location-pages.txt").split("===== ")[1:]:
    lines = chunk.split("\n")
    slug = lines[0].strip()
    title = lines[1].strip().replace("  ", " ")
    body = []
    for ln in lines[2:]:
        if ln.strip().startswith(("Related newspaper articles", "WordPress", "There has been a critical error", "Learn more about troubleshooting")):
            break
        body.append(ln)
    if body and body[0].strip() == title:
        body = body[1:]
    m = MARKERS.get(title, {})
    PLACES.append(dict(slug=slug, title=title, secs=_blocks(body), **m))

# Which existing poddle.ie page covers the same place
SAME = {
 "tallaght": "fettercairn-house", "firhouse-weir": "balrothery-weir", "tymon-castle": "tymon", "kimmage-manor-kimmage-house": "kimmage-manor",
 "ravensdale-park": "ravensdale", "tongue": "stone-boat", "mount-argus": "mount-argus", "mount-jerome-cemetery": "mount-jerome",
 "grand-canal": "mount-jerome", "st-patricks-cathedral": "st-patricks", "little-ship-street": "ship-street-little", "dublin-castle": "dubh-linn",
 "wellington-quay": "liffey", "olympia-theatre": "palace-street", "mount-down-house-mill": "mill-sites", "rutland-mills": "mill-sites",
 "larkfield-mills": "mill-sites", "dolphins-barn": "city-watercourse", "back-of-the-pipes": "city-watercourse", "st-james-basin": "city-watercourse",
 "st-thomas-abbey": "second-diversion", "templeogue-house": "city-watercourse", "13th-century-corn-mill": "mills", "blackpitts": "st-patricks",
 "harolds-cross-road": "mount-jerome", "new-row": "st-patricks", "bull-alley-improvement-scheme": "st-patricks", "willington-osprey-drive": "tymon",
}
PAGE_NAMES = {s["slug"]: s["name"] for s in STOPS}
PAGE_NAMES.update({h["slug"]: h["name"] for h in HISTORY})
PAGE_NAMES.update({"mill-sites": "Mill sites", "city-watercourse": "The City Watercourse"})

AREAS = [
 ("upper", "Tallaght to Kimmage", "The Tymon River and the upper Poddle, from the source near Cookstown to the Kimmage crossroads."),
 ("middle", "Kimmage to the Grand Canal", "The Tongue, Mount Argus, Harold’s Cross and the canal crossing."),
 ("watercourse", "The City Watercourse and its branches", "The man-made channel from the Dodder at Balrothery, and the Abbey Stream, Tenter Water and Commons Water."),
 ("city", "The Liberties and the city", "Blackpitts, St Patrick’s, Dublin Castle and the outfall at Wellington Quay."),
]
def _area(p):
    parts, lat = p.get("parts", ""), p.get("lat", 53.34)
    if "City Watercourse" in parts or "Dodder Branch" in parts or "Abbey" in parts or "Tenter" in parts or "Common" in parts:
        return "watercourse" if lat < 53.3405 or "Dodder" in parts else "city"
    if lat < 53.3155:
        return "upper"
    if lat < 53.3305:
        return "middle"
    return "city"
for p in PLACES:
    p["area"] = _area(p)
PLACES.sort(key=lambda p: ([a[0] for a in AREAS].index(p["area"]), p.get("lat", 99)))

def _teaser(p):
    d = p.get("desc") or (p["secs"][0][1][0] if p["secs"] else "")
    d = re.sub(r'^[A-Z’\'()&/ .]{6,}\s+(?=[A-Z][a-z])', '', d)
    d = re.split(r'(?<=[.!?])\s', d)[0]
    return d if len(d) < 220 else d[:200].rsplit(" ", 1)[0] + "…"

for i, p in enumerate(PLACES):
    prev = PLACES[i - 1] if i else None
    nxt = PLACES[i + 1] if i + 1 < len(PLACES) else None
    same = SAME.get(p["slug"])
    also = (f'<p class="xlink"><a href="{same}.html">More on poddle.ie: {esc(PAGE_NAMES.get(same, same))} →</a></p>' if same else "")
    mapl = (f'<p class="xlink"><a href="map.html?place={p["slug"]}">See it on the map →</a></p>' if p.get("lat") else "")
    pn = '<nav class="pn" aria-label="Previous and next">'
    pn += f'<a class="prev" href="place-{prev["slug"]}.html"><span>Previous place</span>{esc(prev["title"])}</a>' if prev else '<span></span>'
    pn += f'<a class="next" href="place-{nxt["slug"]}.html"><span>Next place</span>{esc(nxt["title"])}</a>' if nxt else '<span></span>'
    pn += '</nav>'
    area = dict((a[0], a[1]) for a in AREAS)[p["area"]]
    text = _secs_html(p["secs"]) if p["secs"] else f'<p>{esc(p.get("desc", ""))}</p>'
    body = (f'<article class="wrap page arch"><p class="crumb"><a href="archive-places.html">Places along the Poddle</a></p>'
            f'<header class="page-head"><p class="kicker">Poddle archive <span>·</span> {esc(area)}</p><h1>{esc(p["title"])}</h1>'
            + (f'<p class="dek">{esc(_teaser(p))}</p>' if not (p["secs"] and p["secs"][0][1] and p["secs"][0][1][0][:50] == _teaser(p)[:50]) else '') + '</header>'
            f'<div class="page-grid solo"><div class="text">{text}{also}{mapl}{CREDIT}</div></div>{pn}</article>')
    write(f'place-{p["slug"]}.html', shell(f'place-{p["slug"]}', f'{p["title"]} · Poddle archive · {SITE}',
          f'{_teaser(p)} From the {CWHG}’s Poddle archive.', body, "archive.html", article=True))

def _place_li(p):
    return f'<li><a href="place-{p["slug"]}.html"><strong>{esc(p["title"])}</strong><span>{esc(_teaser(p))}</span></a></li>'
places_body = ('<div class="wrap page arch"><p class="crumb"><a href="archive.html">Poddle archive</a></p>'
  '<header class="page-head"><p class="kicker">Poddle archive</p><h1>Places along the Poddle</h1>'
  f'<p class="dek">{len(PLACES)} landmarks from Tallaght to the Liffey, each with its story and its link to the river. '
  'They are also on the <a href="map.html?layer=places">map</a>.</p></header>'
  + "".join(f'<section class="arch-area" id="{k}"><h2>{esc(t)}</h2><p class="note">{esc(d)}</p><ul class="arch-list">'
            + "".join(_place_li(p) for p in PLACES if p["area"] == k) + '</ul></section>' for k, t, d in AREAS)
  + CREDIT + '</div>')
write("archive-places.html", shell("archive-places", f"Places along the Poddle · Poddle archive · {SITE}",
      f"{len(PLACES)} landmarks along the River Poddle, from the {CWHG}’s Poddle archive.", places_body, "archive.html"))

# ---- people
ppl = _arch("text-people.txt").split("\n")
names = []
for ln in ppl[4:]:
    t = ln.strip()
    if not t:
        continue
    if t in names:
        break
    if len(t) < 45:
        names.append(t)
start = [i for i, ln in enumerate(ppl) if ln.strip() == names[0]][1]
PEOPLE, cur = [], None
for ln in ppl[start:]:
    t = ln.strip()
    if not t or t == ".":
        continue
    if t in names or t in [n.split(" – ")[0] for n in names]:
        t = next((n for n in names if n == t or n.split(" – ")[0] == t), t)
        cur = dict(name=t, paras=[])
        PEOPLE.append(cur)
    elif cur:
        cur["paras"].append(t)
people_body = ('<div class="wrap page arch"><p class="crumb"><a href="archive.html">Poddle archive</a></p>'
  '<header class="page-head"><p class="kicker">Poddle archive</p><h1>People of the Poddle</h1>'
  '<p class="dek">From Dean Swift and Red Hugh O’Donnell to the Shaw and Plunkett families, and the nun who fell into the river twice: the people whose lives ran alongside it.</p></header>'
  '<nav class="arch-toc" aria-label="People on this page"><ul>' + "".join(f'<li><a href="#{slug_id(p["name"])}">{esc(p["name"])}</a></li>' for p in PEOPLE) + '</ul></nav>'
  '<div class="page-grid solo"><div class="text">'
  + "".join(f'<section id="{slug_id(p["name"])}"><h2>{esc(p["name"])}</h2>{"".join(_p(x) for x in p["paras"])}</section>' for p in PEOPLE)
  + CREDIT + '</div></div></div>')
write("archive-people.html", shell("archive-people", f"People of the Poddle · Poddle archive · {SITE}",
      f"The people whose lives ran alongside Dublin’s River Poddle, from the {CWHG}’s Poddle archive.", people_body, "archive.html"))

# ---- the group's overview of the river
ov = _arch("text-the-poddle.txt").split("\n")[3:]
ov_body = ('<div class="wrap page arch"><p class="crumb"><a href="archive.html">Poddle archive</a></p>'
  '<header class="page-head"><p class="kicker">Poddle archive</p><h1>The Poddle: names, course and sayings</h1>'
  '<p class="dek">The history group’s guide to the river: what it has been called, the Vikings’ harbour, where it runs, and the phrases it gave Dublin.</p></header>'
  '<div class="page-grid solo"><div class="text">' + _secs_html(_blocks(ov)) + CREDIT + '</div></div></div>')
write("archive-overview.html", shell("archive-overview", f"The Poddle: names, course and sayings · Poddle archive · {SITE}",
      f"The River Poddle’s many names, its course and the phrases it gave Dublin, from the {CWHG}’s Poddle archive.", ov_body, "archive.html"))

# ---- newspaper archive: every article, by theme, linked to the group's transcription
NEWS = _json.loads(_arch("news-index.json"))
THEME_NAMES = {"churches": "Churches", "flooding": "Flooding", "building-development": "Buildings and planning", "general-information": "General",
  "mills": "Mills and industry", "culverts": "Culverts", "river-works": "River works", "litter-pollution": "Litter and pollution", "bridges": "Bridges",
  "water-supply": "Water supply", "people": "People", "schools": "Schools", "accidents": "Accidents", "arts": "Arts", "alcohol": "Alcohol",
  "crime": "Crime", "tunnel": "Tunnel", "poddle-guard": "Poddle Guard", "poddle-themes": "Poddle themes", "poddle-tax": "Poddle Tax"}
_count = {}
for n in NEWS:
    n["themes"] = [t for t in n["themes"] if t in THEME_NAMES and t != "uncategorized"]
    for t in n["themes"]:
        _count[t] = _count.get(t, 0) + 1
themes_sorted = sorted(_count, key=lambda t: -_count[t])
NEWS.sort(key=lambda n: n["title"].lower().lstrip("‘'\"“"))
chips = ('<div class="arch-filter" role="group" aria-label="Filter by theme"><button type="button" class="chip on" data-t="">All <span>' + str(len(NEWS)) + '</span></button>'
         + "".join(f'<button type="button" class="chip" data-t="{t}">{esc(THEME_NAMES[t])} <span>{_count[t]}</span></button>' for t in themes_sorted) + '</div>')
rows = "".join(f'<li data-t="{" ".join(n["themes"])}"><a href="{esc(n["link"])}" rel="noopener">{esc(n["title"])}</a>'
               f'<span class="tags">{" · ".join(esc(THEME_NAMES[t]) for t in n["themes"])}</span></li>' for n in NEWS)
news_body = ('<div class="wrap page arch"><p class="crumb"><a href="archive.html">Poddle archive</a></p>'
  '<header class="page-head"><p class="kicker">Poddle archive</p><h1>The Poddle in the newspapers</h1>'
  f'<p class="dek">{len(NEWS)} newspaper articles about the river, from 1784 to the 2010s, found and transcribed by the history group’s volunteers. '
  'Pick a theme or search by headline. Each article opens on the group’s site, with a scan of the original page.</p></header>'
  '<label class="arch-search"><span>Search headlines</span><input type="search" id="news-q" placeholder="e.g. flood, mill, Swift" autocomplete="off"></label>'
  + chips + f'<p class="note" id="news-n" aria-live="polite">Showing all {len(NEWS)} articles.</p><ul class="arch-news" id="news-list">' + rows + '</ul>'
  + CREDIT + '</div>'
  '<script>(function(){var q=document.getElementById("news-q"),list=document.getElementById("news-list"),n=document.getElementById("news-n"),t="";'
  'var items=[].slice.call(list.children);function run(){var s=q.value.trim().toLowerCase(),c=0;items.forEach(function(li){'
  'var ok=(!t||(" "+li.dataset.t+" ").indexOf(" "+t+" ")>-1)&&(!s||li.textContent.toLowerCase().indexOf(s)>-1);li.hidden=!ok;if(ok)c++;});'
  'n.textContent="Showing "+c+" of "+items.length+" articles.";}'
  '[].forEach.call(document.querySelectorAll(".arch-filter .chip"),function(b){b.addEventListener("click",function(){'
  '[].forEach.call(document.querySelectorAll(".arch-filter .chip"),function(x){x.classList.remove("on");x.setAttribute("aria-pressed","false")});'
  'b.classList.add("on");b.setAttribute("aria-pressed","true");t=b.dataset.t;run();});});q.addEventListener("input",run);})();</script>')
write("archive-news.html", shell("archive-news", f"The Poddle in the newspapers · Poddle archive · {SITE}",
      f"{len(NEWS)} newspaper articles about the River Poddle, 1784 to the 2010s, from the {CWHG}’s Poddle archive.", news_body, "archive.html"))

# ---- the archive's front page
about_txt = [ln.strip() for ln in _arch("text-about-the-project.txt").split("\n")[2:] if ln.strip()]
arch_body = (f'<div class="wrap page arch"><header class="page-head"><p class="kicker">Poddle archive</p><h1>The Crumlin and Walkinstown Poddle archive</h1>'
  f'<p class="dek">Over 500 hours of volunteer research into the River Poddle and the City Watercourse: {len(PLACES)} places, {len(PEOPLE)} people and {len(NEWS)} newspaper articles.</p></header>'
  f'<aside class="brief"><strong>Welcome</strong><p>This archive was researched and written by volunteers of the {CWHG} and Crumlin Community Cleanup, '
  f'and first published in October 2024 at <a href="{CWHG_URL}" rel="noopener">poddle.crumlinwalkinstownhistory.ie</a>. With the group’s generous agreement, it now also lives here, '
  f'beside the rest of poddle.ie. Their text is kept as they wrote it.</p></aside>'
  '<ul class="arch-cards">'
  f'<li><a href="archive-places.html"><strong>Places along the Poddle</strong><span>{len(PLACES)} landmarks from Tallaght to Wellington Quay, from Templeogue House to the Olympia.</span></a></li>'
  f'<li><a href="archive-people.html"><strong>People of the Poddle</strong><span>Sister Ann Dominica Fitzgerald, Dean Swift, Red Hugh O’Donnell, the Shaws and more.</span></a></li>'
  f'<li><a href="archive-news.html"><strong>The Poddle in the newspapers</strong><span>{len(NEWS)} articles from 1784 to the 2010s, by theme: floods, mills, culverts, the Poddle Tax.</span></a></li>'
  '<li><a href="archive-overview.html"><strong>Names, course and sayings</strong><span>Puddle, Salach, Glascholach: the river’s names, its course and the phrases it gave Dublin.</span></a></li>'
  '<li><a href="map.html?layer=places"><strong>The landmarks on the map</strong><span>Every place in the archive, pinned on today’s streets.</span></a></li>'
  '</ul>'
  '<div class="page-grid solo"><div class="text"><section><h2>About the project</h2>' + "".join(_p(t) for t in about_txt) + '</section>'
  f'<section><h2>Thank you</h2><p>Thank you to the volunteers, {VOLUNTEERS}, and to the Local Authority Waters Programme, which funded part of the project. '
  f'Visit the <a href="{CWHG_HOME}" rel="noopener">{CWHG}</a> for their talks, events and research on the wider area.</p></section></div></div></div>')
write("archive.html", shell("archive", f"Poddle archive · {SITE}",
      f"The {CWHG}’s Poddle archive: {len(PLACES)} places, {len(PEOPLE)} people and {len(NEWS)} newspaper articles about Dublin’s hidden river.", arch_body, "archive.html"))

# Map pins for the landmarks layer (read by build_extra.py)
LANDMARKS = [[p["title"], p["lat"], p["lon"], _teaser(p), p["slug"]] for p in PLACES if p.get("lat")]
ARCH_BACKLINKS = {}
for p in PLACES:
    if SAME.get(p["slug"]):
        ARCH_BACKLINKS.setdefault(SAME[p["slug"]], []).append((f'place-{p["slug"]}.html', p["title"]))
