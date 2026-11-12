# The Crumlin and Walkinstown History Group's Poddle research, merged into poddle.ie with the
# group's agreement (November 2026). Executed by build.py after build_enrich.py, sharing its namespace.
#  - data/places.txt: our edited texts for their 54 places, each placed on a walk stop, a meander or a history page
#  - new walk stops (Blackpitts, Cross Poddle) and "meander" pages off the main walk line
#  - people.html (new People section), media-newspapers.html (their newspaper index), and a section on sources.html
#  - redirects from the old archive*.html / place-*.html addresses
# Raw source files from their site are in data/crumlin/.
import json as _json
import urllib.parse

ARCH_DIR = os.path.join(OUT, "data", "crumlin")
CWHG = "Crumlin and Walkinstown History Group"
VOLUNTEERS = "Aidan, Bernadette, Brendan, Carol, Kevin, Margaret, Mary, Michele, Sally-Anne and Trevor"
CREDIT_NOTE = ('<p class="note credit">Parts of this page draw on research by the volunteers of the '
               f'{CWHG}, shared with poddle.ie. <a href="sources.html#poddle-research">About their research</a>.</p>')

def _arch(name):
    with open(os.path.join(ARCH_DIR, name), encoding="utf-8") as fh:
        return fh.read()

def _html(t):
    """Escape text but keep the few inline tags used in data/places.txt."""
    t = esc(t)
    t = re.sub(r'&lt;a href=&quot;(.*?)&quot; rel=&quot;noopener&quot;&gt;(.*?)&lt;/a&gt;', r'<a href="\1" rel="noopener">\2</a>', t)
    t = re.sub(r'&lt;(/?)em&gt;', r'<\1em>', t)
    return t

# ---- map positions of their places (markers.md, from their map)
MARKERS = {}
for ln in _arch("markers.md").splitlines():
    c = [x.strip() for x in ln.strip().strip("|").split("|")]
    if len(c) == 7 and c[1][:1].isdigit():
        MARKERS[c[0].replace("  ", " ")] = (float(c[1]), float(c[2]))
_titles = {}
for chunk in _arch("text-location-pages.txt").split("===== ")[1:]:
    _l = chunk.split("\n")
    _titles[_l[0].strip()] = _l[1].strip().replace("  ", " ")
PLACE_LL = {s: MARKERS[t] for s, t in _titles.items() if t in MARKERS}

# ---- our edited texts
PLACES = []
cur = None
for ln in open(os.path.join(OUT, "data", "places.txt"), encoding="utf-8"):
    ln = ln.rstrip("\n")
    if ln.startswith("#") and not ln.startswith("##"):
        continue
    if ln.startswith("@@ "):
        f = [x.strip() for x in ln[3:].split("|")]
        slug, home, title = f[:3]
        ll = tuple(float(x) for x in f[3].split(",")) if len(f) > 3 else PLACE_LL.get(slug)  # optional "| lat,lon" for our own places
        cur = dict(slug=slug, home=home, title=title, secs=[], ll=ll)
        PLACES.append(cur)
    elif ln.startswith("## "):
        cur["secs"].append((ln[3:].strip(), []))
    elif ln.strip():
        t = ln.strip()
        cur["secs"][-1][1].append(f'<p class="note">{_html(t)}</p>' if t.startswith("Source") else f"<p>{_html(t)}</p>")

def _maplink(p):
    if not p["ll"]:
        return ""
    lat, lon = p["ll"]
    return (f'<p class="xlink"><a href="map.html?at={lat:.5f},{lon:.5f}&amp;n={urllib.parse.quote(p["title"])}">'
            f'Show {esc(p["title"])} on the map →</a></p>')

def _place_secs(p):
    out = [(h, list(ps)) for h, ps in p["secs"]]
    out[-1][1].append(_maplink(p))
    return out

# ---- two new stops on the main line, between Mount Jerome and St Patrick's
_sp = next(s for s in STOPS if s["slug"] == "st-patricks")
_move = [sec for sec in _sp["sections"] if sec[0] in ("Through the Liberties", "The Blackpitts tanners", "Donore Avenue, 1901")]
_sp["sections"] = [sec for sec in _sp["sections"] if sec not in _move]
_sp["place"] = "Patrick Street"
NEW_STOPS = [
 dict(slug="blackpitts", name="Blackpitts", place="Clanbrassil Street and Warrenmount",
      teaser="Tanners’ pits, mill streams and a river that marked a boundary.",
      brief="North of the canal the river runs underground past Warrenmount to Blackpitts, a district of tanners and mills named after the pits along the stream.",
      sections=_move, images=[]),
 dict(slug="cross-poddle", name="Cross Poddle", place="New Row and Dean Street",
      teaser="Where six streets met at the old crossing of the river.",
      brief="The Poddle’s old crossing at Dean Street, once called Cross Poddle, and the covered channels known as the Poddle Hole.",
      sections=[], images=[]),
]
_i = STOPS.index(_sp)
STOPS[_i:_i] = NEW_STOPS
for _s in NEW_STOPS:
    _s["plan"] = []
STOP_BY = {s["slug"]: s for s in STOPS}

# ---- meanders: short detours off the main line, each its own page
MEANDERS = [
 dict(slug="meander-dolphins-barn", name="Dolphin’s Barn and the City Watercourse", parent="stone-boat", place="Rutland Avenue to James’s Street",
      teaser="Follow the third of the water that left at the Stone Boat, past Shaw’s mill and the Back of the Pipes to the City Basin.",
      ll=(53.33350, -6.29120)),
 dict(slug="meander-st-jamess-gate", name="Guinness and St James’s Gate", parent="st-patricks", place="Thomas Street and James’s Street",
      teaser="Where Guinness got its water: not the Liffey but the Poddle, diverted by the monks in 1245 into the City Watercourse by a stone boat. Plus how Arthur Guinness defended that water with a pickaxe in 1775.",
      ll=(53.34330, -6.28700), own=True),  # poddle.ie's own research, not the history group's
 dict(slug="meander-abbey-stream", name="Along the Abbey Stream", parent="mount-jerome", place="Harold’s Cross to Marrowbone Lane",
      teaser="The monks’ mill stream, from the Hospice under the canal to Donore Avenue, Mill Street and Marrowbone Lane.",
      ll=(53.33300, -6.28260)),
 dict(slug="meander-liberties", name="The Liberties", parent="cross-poddle", place="The Coombe, Cork Street and Meath Street",
      teaser="The old manors outside the walls, their weavers and the Poddle Guard.",
      ll=(53.33900, -6.27900)),
 dict(slug="meander-christ-church", name="Christ Church Cathedral", parent="ship-street-little", place="Christchurch Place",
      teaser="The cathedral on the ridge above the river, where St Patrick’s came when it flooded.",
      ll=(53.34340, -6.27140)),
 dict(slug="meander-st-andrews", name="St Andrew’s and Grafton Street", parent="palace-street", place="St Andrew Street",
      teaser="A church that began in the fields by the Poddle, and a street closed for a river it never touched.",
      ll=(53.34360, -6.26120)),
]
MEANDER_BY = {m["slug"]: m for m in MEANDERS}
for m in MEANDERS:
    m.update(sections=[], images=[], places=[])

# ---- put each place on its page
for p in PLACES:
    kind, _, target = p["home"].partition(":")
    if kind == "meander":
        MEANDER_BY[target]["sections"] += _place_secs(p)
        MEANDER_BY[target]["places"].append(p)
        p["url"] = f'{target}.html#{slug_id(p["secs"][0][0])}'
    else:
        STOP_BY[kind]["sections"] += _place_secs(p)
        STOP_BY[kind]["merged"] = True
        p["url"] = f'{kind}.html#{slug_id(p["secs"][0][0])}'

for s in STOPS:
    s.setdefault("after", "")
    ms = [m for m in MEANDERS if m["parent"] == s["slug"]]
    if ms:
        s["after"] += ('<section class="watch meanders"><h2>Meander off the walk</h2><p class="note">A detour from this stop, off the main line of the river.</p><ul>'
                       + "".join(f'<li><a href="{m["slug"]}.html">{esc(m["name"])}</a>: {esc(m["teaser"])}</li>' for m in ms) + '</ul></section>')
    if s.get("merged"):
        s["after"] += CREDIT_NOTE

# ---- the extra history: words and phrases on the Origins page, and links from history pages to the walk
_orig = next(h for h in HISTORY if h["slug"] == "origins")
_orig["sections"].append(("Words and phrases", [
  "The river has also been written Pottle, and even, grandly, the Tiber, and in Irish Soulagh or Salach, the dirty one. It left its mark on the language of the Liberties:",
  '<ul class="phrases">'
  '<li><strong>The Poddle Act</strong>: “An Act for preventing the Inundations of the Poddle River in Dublin, and for preserving the Cathedral Church of Saint Patrick and the Houses of the adjoining Inhabitants from the Damages arising therefrom” (1840). <a href="https://www.irishstatutebook.ie/eli/1840/act/58/enacted/en/html" rel="noopener">Read it on the Irish Statute Book</a>.</li>'
  '<li><strong>The Poddle Tax</strong>: paid by houses built over the river, to keep its walls and arches in repair; later charged too on houses that drained into it. <a href="ship-street-little.html#st-nicholas-without">The ratepayers’ meeting of 1829</a>.</li>'
  '<li><strong>The Poddle Hole</strong>: the covered channels near St Patrick’s. <a href="cross-poddle.html#the-poddle-hole">Herrings and a bull</a>.</li>'
  '<li><strong>A Poddle Hole step</strong>: a sudden plunge of the foot in the gutter, to splash whoever was nearest.</li>'
  '<li><strong>The Poddle Guard</strong>: a party of about twenty soldiers kept at a barracks near St Patrick’s from 1725. <a href="meander-liberties.html#the-poddle-guard-and-the-city-sword">The guard in action</a>.</li>'
  '<li><strong>New Row on the Poddle</strong>: the 18th-century name of New Row. <a href="cross-poddle.html#new-row-on-the-poddle">New Row</a>.</li>'
  '<li><strong>Cross Poddle</strong>: the old name of Dean Street until 1826. <a href="cross-poddle.html#cross-poddle">Cross Poddle</a>.</li>'
  '<li><strong>Poddleologist</strong>: Sister Ann Dominica Fitzgerald’s word for anyone who follows the river. <a href="people.html#sister-ann-dominica-fitzgerald">Sister Ann</a>.</li>'
  '<li><strong>At the back of the pipes</strong>: Dublin for “nobody knows where”. <a href="meander-dolphins-barn.html#the-back-of-the-pipes">The Back of the Pipes</a>.</li>'
  '</ul>']))

HIST_WALK = {
 "city-watercourse": [("balrothery-weir.html#templeogue-house", "Templeogue House and the Domvilles"), ("dodder-overflow.html#mount-down-where-the-poddle-begins", "Mount Down, where the watercourse met the Tymon River"),
                      ("meander-dolphins-barn.html", "Meander: Dolphin’s Barn and the City Watercourse"), ("meander-abbey-stream.html", "Meander: along the Abbey Stream")],
 "mills": [("ravensdale.html#ravensdale-mill", "Ravensdale Mill"), ("stone-boat.html#larkfield-mill-and-the-kimmage-garrison", "Larkfield Mill"), ("mount-argus.html#loader-s-park-mill", "Loader’s Park Mill"),
           ("meander-abbey-stream.html#greenmount", "Greenmount spinning mill"), ("meander-dolphins-barn.html#rutland-avenue-and-shaw-s-mill", "Shaw’s mill, Rutland Avenue"), ("st-patricks.html#the-1990-dig-a-medieval-mill", "The medieval mill found in 1990")],
 "floods": [("mount-argus.html#kimmage-road-lower", "Kimmage Road Lower, 1910 and 1985"), ("meander-dolphins-barn.html#dolphin-s-barn", "Rutland Cottages, 1937"), ("dodder-overflow.html#willington-and-osprey", "Osprey Drive, 1978"),
            ("ravensdale.html#poddle-park-and-st-martin-s", "Poddle Park, 2002"), ("ship-street-little.html#the-pool-at-ship-street", "Ship Street and the Castle Yard, 1784")],
 "second-diversion": [("stone-boat.html#tonguefield", "Tonguefield and the two branches"), ("meander-dolphins-barn.html#st-thomas-s-abbey", "St Thomas’s Abbey")],
 "heart-of-dublin": [("ship-street-little.html#st-michael-le-pole", "St Michael le Pole"), ("dubh-linn.html#under-the-castle-yards", "Under the Castle yards")],
 "1719-act": [("balrothery-weir.html#templeogue-house", "Templeogue House, where the city’s water crossed private land")],
}
for h in HISTORY:
    h.setdefault("after", "")
    if HIST_WALK.get(h["slug"]):
        h["after"] += ('<section class="watch walk-links"><h2>On the walk</h2><ul>'
                       + "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in HIST_WALK[h["slug"]]) + '</ul></section>')

# meander pages' own notes (set before the People boxes are added)
for m in MEANDERS:
    m["brief"] = ""
    m["after"] = ("" if m.get("own") else CREDIT_NOTE) + f'<p class="xlink"><a href="map.html?meander={m["slug"]}">See this meander on the map →</a></p>'
def _stop_n(slug):
    return [s["slug"] for s in STOPS].index(slug) + 1

# ---- People: everyone whose story touches the river, from the existing pages and the group's research
PEOPLE = [
 dict(name="Sister Ann Dominica Fitzgerald", dates="died 2006", tag="The first Poddleologist",
      paras=["A Dominican nun from Blackrock who taught at Muckross Park in Donnybrook, Sister Ann made the Poddle her cause. She traced it on foot through the Liberties, falling in twice along the way, photographed stretches that were about to vanish, and argued that its meeting with the Liffey formed the Dubh Linn that gave the city its name. She coined the word “Poddleologist” for anyone who follows the river.",
             "In the early 1970s she campaigned against the building over of the City Watercourse at Templeogue, frustrated by what she saw as apathy and poor planning, and won the support of Seán Rothery, chairman of An Taisce. She wrote the narration for John Gleeson’s 16mm film of the watercourse, led walks along the river for the 1973 Dublin Arts Festival, and wrote “Down the Old Poddle” for The Liberties of Dublin (1973). She died on 10 March 2006."],
      links=[("city-watercourse.html#the-poddleologist", "Saving the watercourse"), ("ship-street-little.html#an-underground-river", "“An underground river!”"), ("dodder-overflow.html#willington-and-osprey", "Willington and the watercourse"), ("meander-abbey-stream.html#sweeney-s-terrace-and-mill-street", "Her walk to Warrenmount")]),
 dict(name="Red Hugh O’Donnell", dates="1572–1602", tag="Escaped from Dublin Castle by the river",
      paras=["Heir to the O’Donnells of Tír Chonaill, Red Hugh was kidnapped at fifteen in 1587, lured aboard a ship at Rathmullan, and held in Dublin Castle as a hostage. A first escape in 1590 failed. At Christmas 1591 he and Henry and Art O’Neill got free of their fetters, let themselves down by a rope into the Poddle where it ran under the Castle, crossed the moat and fled into the Wicklow mountains in deep snow. Art O’Neill died of cold, and Red Hugh lost his big toes to frostbite before the O’Byrnes of Glenmalure brought them to safety. He went on to lead the Nine Years’ War with Hugh O’Neill."],
      links=[("dubh-linn.html#defence", "The moat and the escape")]),
 dict(name="The Domvilles of Templeogue", dates="1688–1768", tag="Held the city’s water to ransom",
      paras=["Sir Thomas Domville took Templeogue House after the Talbots lost it in 1688, and with it control of the City Watercourse that crossed his land. His son Sir Compton Domville made the watercourse the centrepiece of his gardens, and is remembered for using it as a weapon: when his nephew Lord Santry was condemned for killing a tavern porter in 1739, Sir Compton is said to have threatened to cut off the city’s water unless Santry was spared. Santry was pardoned. The story is famous, though how much the threat decided it is debated."],
      links=[("balrothery-weir.html#guarding-the-water", "Guarding the water"), ("balrothery-weir.html#templeogue-house", "Templeogue House")]),
 dict(name="John Le Decer", dates="mayor 1302–1324", tag="The mayor who built the city’s fountain",
      paras=["Six times mayor of Dublin (1302, 1305, 1307 to 1309 and 1324), Le Decer paid for public works himself. In 1308 he had the watercourse cleaned and faced with stone, and built a marble cistern at Cornmarket, by St Audoen’s, fed from the City Watercourse. People called it Le Decer’s fountain, or the High Pipe. Tradition says he set the “Lucky Stone”, an early grave slab, beside it, and that whoever drank there had good luck."],
      links=[("balrothery-weir.html#rebuilt-over-the-centuries", "Rebuilding the watercourse"), ("city-watercourse.html#water-for-the-city", "Water for the city")]),
 dict(name="Jonathan Swift", dates="1667–1745", tag="Dean of St Patrick’s, on the river’s island",
      paras=["Swift was Dean of St Patrick’s from 1713 until his death, in a cathedral built on an island between two streams of the Poddle, with the water a few feet beneath its floor. He opposed a plan to crown its tower with a brick spire. One account says the Poddle Guard was set up in 1725 to stop him rousing the crowds of the Liberties against the government; others say it simply policed the rough ground by the cathedral. He left most of his fortune to found St Patrick’s Hospital, which still cares for patients today."],
      links=[("st-patricks.html#a-cathedral-on-wet-ground", "A cathedral on wet ground"), ("meander-liberties.html#the-poddle-guard-and-the-city-sword", "The Poddle Guard")]),
 dict(name="Arthur Guinness", dates="1725–1803", tag="Brewed with the City Watercourse",
      paras=["On 31 December 1759 Arthur Guinness took a lease of the disused brewery at St James’s Gate from Mark Rainsford, for 9,000 years at £45 a year. The lease gave him free use of “the said Pipe water or City Water Course”, the water the City Watercourse carried down from the Dodder and the Poddle to the City Basin beside the brewery.",
             "When Dublin Corporation came with the Sheriff in May 1775 to fill in his channel, he took a pickaxe from one of the workmen and told them the water was his and he would defend it. The quarrel ended in a compromise in the mid-1780s, when he agreed to pay £10 a year for the water."],
      links=[("meander-st-jamess-gate.html#arthur-guinness-s-lease", "Arthur Guinness’s lease"), ("meander-st-jamess-gate.html#the-pickaxe-1775", "The pickaxe, 1775"), ("meander-dolphins-barn.html#the-city-basin", "The City Basin")]),
 dict(name="Sir Benjamin Lee Guinness", dates="1798–1868", tag="Restored St Patrick’s on its island",
      paras=["Arthur Guinness’s grandson ran the brewery and was Lord Mayor of Dublin in 1851. Between 1860 and 1865 he paid for the great restoration of St Patrick’s Cathedral, when it was feared the building, standing on wet ground between two streams of the Poddle, might collapse. His statue stands outside the cathedral."],
      links=[("st-patricks.html#out-of-sight", "Out of sight"), ("meander-st-jamess-gate.html#the-guinness-family-by-the-poddle", "The Guinness family by the Poddle")]),
 dict(name="Lord Iveagh (Edward Cecil Guinness)", dates="1847–1927", tag="Rebuilt the Poddle valley",
      paras=["The third son of Sir Benjamin Lee Guinness, Edward Cecil Guinness ran the brewery and was made Lord Iveagh in 1891. Around 1900 the streets between St Patrick’s and Bride Street, the “Poddle valley”, were some of the worst slums in the city, with houses sinking into the river beneath them. Lord Iveagh cleared them and laid out St Patrick’s Park, opened in 1902, and his Iveagh Trust built the Bull Alley flats (1901 to 1906), the Iveagh Hostel and the Iveagh Baths on Bride Road (1906), and the Iveagh Play Centre (1915). He also paid for the Iveagh Markets on Francis Street.",
             "The Corporation moved part of the river to give the new buildings firm ground, and in 1902 thanked him for a gift of £1,400 towards completing the new channel from the cathedral to where the two branches met. During the works of 1901 the old carved stone thought to mark St Patrick’s Well was found in the culvert beside the cathedral."],
      links=[("st-patricks.html#out-of-sight", "Out of sight"), ("st-patricks.html#the-iveagh-buildings", "The Iveagh Buildings"), ("st-patricks.html#between-two-streams", "St Patrick’s Well"), ("meander-st-jamess-gate.html#the-guinness-family-by-the-poddle", "The Guinness family by the Poddle"), ("blackpitts.html#washing-rights-in-the-poddle", "Guinness workers at Blackpitts")]),
 dict(name="George Carr Shaw", dates="1814–1885", tag="The playwright’s father, a reluctant miller",
      paras=["Born in Kilkenny, a civil servant who sold his pension for £500 and went into the flour trade, George Carr Shaw ran Rutland mill on the City Watercourse with his partner Clibborn. His son, George Bernard Shaw, described a business that “did not work the industry: it worked them”, and his father laughing helplessly in an empty corner of the warehouse after a customer’s bankruptcy all but ruined them. The mill kept him until he died in 1885."],
      links=[("meander-dolphins-barn.html#rutland-avenue-and-shaw-s-mill", "Shaw’s mill, Rutland Avenue"), ("mills.html", "The mills")]),
 dict(name="Sir Frederick Shaw", dates="1799–1876", tag="Recorder of Dublin, at Kimmage",
      paras=["Recorder of Dublin from 1830 to 1876 and MP for the city and then Dublin University, Shaw lived at Kimmage House, on the Poddle, from 1829 until he died. He remodelled it in the Tudor style, built Whitehall Road as its new approach, and married Thomasina Emily Jocelyn, a granddaughter of the Earl of Roden. His granddaughter Flora Shaw named Nigeria."],
      links=[("kimmage-manor.html#frederick-shaw", "Frederick Shaw"), ("kimmage-manor.html#from-kimmage-house-to-kimmage-manor", "From Kimmage House to Kimmage Manor")]),
 dict(name="The Plunketts", dates="1914–1916", tag="Larkfield and the Kimmage Garrison",
      paras=["Countess Plunkett held the lease of Larkfield, the old mill on the Poddle by Sundrive Road, and her sons, Joseph Mary Plunkett among them, made it a base for the Volunteers: a store for the Howth guns of 1914 and, before Easter 1916, home to the Kimmage Garrison. Joseph Mary Plunkett signed the Proclamation and was executed after the Rising."],
      links=[("stone-boat.html#larkfield-mill-and-the-kimmage-garrison", "Larkfield Mill and the Kimmage Garrison"), ("ravensdale.html#mill-country", "Mill country")]),
 dict(name="Archbishops Comyn and de Loundres", dates="1181–1228", tag="Built on the river’s island",
      paras=["John Comyn, the first Norman archbishop of Dublin, built his palace of St Sepulchre beside the Poddle and made the little church on its island collegiate in 1191. His successor, Henry de Loundres, raised it to a cathedral, and was granted the manor of Tymon by King John in 1216."],
      links=[("st-patricks.html#a-cathedral-on-wet-ground", "A cathedral on wet ground"), ("cross-poddle.html#st-sepulchre-s-palace", "St Sepulchre’s Palace"), ("tymon.html#tymon-estate", "Tymon estate")]),
 dict(name="Mary Aikenhead", dates="1787–1858", tag="Founded the Hospice on the river",
      paras=["Founder of the Religious Sisters of Charity and of St Vincent’s Hospital, she bought Greenmount at Harold’s Cross in 1845, on the banks of the Poddle, and made it the congregation’s mother house. Our Lady’s Hospice grew from it."],
      links=[("meander-abbey-stream.html#our-lady-s-hospice", "Our Lady’s Hospice"), ("mount-jerome.html#greenmount-and-the-hospice", "Greenmount and the Hospice")]),
 dict(name="The Pims", dates="19th century", tag="Quaker mill owners at Greenmount",
      paras=["The Quaker Pim family, Thomas, Jonathan and Joseph Robinson Pim of Pim Brothers, enlarged the Greenmount mill on the Poddle into the Greenmount Spinning Company, making cotton, linen and Irish poplin, and were known for their work for better conditions and charity."],
      links=[("meander-abbey-stream.html#greenmount", "Greenmount")]),
 dict(name="Saint Charles of Mount Argus", dates="1821–1893", tag="The healer by the river",
      paras=["Charles Houben, a Dutch Passionist, came to the new monastery at Mount Argus in 1857, where the Poddle ran through the grounds. Crowds came to him for healing. He was canonised in 2007."],
      links=[("mount-argus.html#saint-charles", "Saint Charles"), ("mount-argus.html#the-first-mount-argus", "The first Mount Argus")]),
 dict(name="Mary Agnes Hammond", dates="died 1956", tag="Landlady with washing rights in the Poddle",
      paras=["Daughter of the builder Arthur Hammond, she inherited 150 houses around Blackpitts in 1902, many let to Guinness workers, with the right to wash in the River Poddle written into the deeds. She is remembered as a British spy during and after the First World War."],
      links=[("blackpitts.html#washing-rights-in-the-poddle", "Washing rights in the Poddle")]),
 dict(name="Zozimus (Michael Moran)", dates="c. 1794–1846", tag="The blind rhymer of the Liberties",
      paras=["The street balladeer Michael Moran, known as Zozimus, was born in Faddle Alley off Blackpitts and died in Patrick Street, both on the river’s course. A play about him, Zoz, was staged at the Olympia, over the Poddle, in 1975."],
      links=[("blackpitts.html#through-the-liberties", "Through the Liberties")]),
 dict(name="Dan Lowrey", dates="1879", tag="Built a music hall over the river",
      paras=["Dan Lowrey opened the Star of Erin music hall on Dame Street in 1879, now the Olympia. The Poddle beneath it decided where the stage went and why the audience still comes in through a tunnel."],
      links=[("palace-street.html#the-olympia-and-the-river", "The Olympia and the river")]),
 dict(name="Spencer Harty", dates="City Surveyor, 1890s–1900s", tag="The engineer who found St Patrick’s Well",
      paras=["As Dublin’s Borough Surveyor, Harty dealt with the open river at Donore Avenue and rebuilt the culverts in the Liberties. In June 1901, opening the old arched course of the Poddle in Patrick Street, he found the stone marking St Patrick’s Well."],
      links=[("blackpitts.html#donore-avenue-1901", "Donore Avenue, 1901"), ("st-patricks.html#between-two-streams", "Between two streams")]),
 dict(name="James Joyce", dates="1882–1941", tag="Put the Poddle in Ulysses",
      paras=["Joyce gave the river a sentence in Ulysses, misplacing its mouth at Wood Quay: “Poddle river hung out in fealty a tongue of liquid sewage.”"],
      links=[("liffey.html#ulysses", "Ulysses")]),
]
for pp in PEOPLE:
    pp["id"] = slug_id(pp["name"])

# ---- Portraits (Nov 2026): openly licensed / public-domain images, black and white, credited.
# Keyed by person id; a portrait is only shown once its file exists in img/people/.
# Sources and licences are also listed in img/people/SOURCES.md.
import os as _os
PORTRAITS = {}
_pj = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data", "portraits.json")
if _os.path.exists(_pj):
    PORTRAITS = _json.load(open(_pj, encoding="utf-8"))

def _portrait(pp):
    p = PORTRAITS.get(pp["id"])
    if not p or not _os.path.exists(_os.path.join(_os.path.dirname(_pj), "..", p["src"])):
        return ""
    return (f'<figure class="portrait"><img src="{esc(p["src"])}" alt="{esc(p["alt"])}" width="{p.get("w", 240)}" height="{p.get("h", 300)}" loading="lazy" decoding="async">'
            f'<figcaption>{esc(p["caption"])}. <a href="{esc(p["source_url"])}">{esc(p["credit"])}</a>, {esc(p["licence"])}</figcaption></figure>')
PEOPLE_ON = {}
for pp in PEOPLE:
    for u, _t in pp["links"]:
        PEOPLE_ON.setdefault(u.split(".html")[0], []).append(pp)
for it in STOPS + HISTORY + MEANDERS:
    ps = []
    for pp in PEOPLE_ON.get(it["slug"], []):
        if pp not in ps:
            ps.append(pp)
    if ps:
        box = ('<section class="watch people-links"><h2>Poddle People</h2><ul>' + "".join(
               f'<li><a href="people.html#{pp["id"]}">{esc(pp["name"])}</a>: {esc(pp["tag"])}</li>' for pp in ps) + '</ul></section>')
        it["after"] = box + it.get("after", "")

people_body = ('<div class="wrap page"><header class="page-head"><p class="kicker">People</p><h1>Poddle People</h1>'
  '<p class="dek">Archbishops and rebels, millers and nuns, a dean, a spy and a playwright’s father: the people whose lives ran alongside the river. Each links to the places on the walk and in the history where their story is told.</p></header>'
  '<nav class="arch-toc" aria-label="People on this page"><ul>' + "".join(f'<li><a href="#{pp["id"]}">{esc(pp["name"])}</a></li>' for pp in PEOPLE) + '</ul></nav>'
  '<div class="page-grid solo"><div class="text">'
  + "".join(f'<section id="{pp["id"]}" class="person"><h2>{esc(pp["name"])}</h2><p class="when">{esc(pp["dates"])} <span>·</span> {esc(pp["tag"])}</p>' + _portrait(pp)
            + "".join(f"<p>{esc(x)}</p>" for x in pp["paras"])
            + '<p class="on-site">On poddle.ie: ' + " · ".join(f'<a href="{u}">{esc(t)}</a>' for u, t in pp["links"]) + '</p></section>' for pp in PEOPLE)
  + CREDIT_NOTE + '</div></div></div>')
write("people.html", shell("people", f"Poddle People · {SITE}",
      "The people whose lives ran alongside Dublin’s River Poddle: Red Hugh O’Donnell, Dean Swift, the Domvilles, Sister Ann Dominica Fitzgerald, Lord Iveagh and more.", people_body, "people.html"))

# ---- meander pages
for m in MEANDERS:
    par = STOP_BY[m["parent"]]
    nxt = STOPS[_stop_n(m["parent"])] if _stop_n(m["parent"]) < len(STOPS) else None
    kicker = f'Meander <span>·</span> off Stop {_stop_n(m["parent"])}, {esc(par["name"])}'
    body = article(m, kicker, (par["slug"], par["name"]), (nxt["slug"], nxt["name"]) if nxt else None, (f'{par["slug"]}.html', f'Back to Stop {_stop_n(m["parent"])}: {par["name"]}'))
    body = body.replace("<span>Upstream</span>", "<span>Back to the walk</span>").replace("<span>Downstream</span>", "<span>Next stop on the walk</span>")
    toc = '<nav class="arch-toc" aria-label="On this meander"><ul>' + "".join(f'<li><a href="#{slug_id(p["secs"][0][0])}">{esc(p["title"])}</a></li>' for p in m["places"]) + '</ul></nav>'
    body = body.replace('<div class="page-grid solo">', toc + '<div class="page-grid solo">', 1)
    write(f'{m["slug"]}.html', shell(m["slug"], f'{m["name"]} · Meander · {SITE}',
          f'{m["teaser"]} A meander off the River Poddle walk, at {m["place"]}, Dublin.', body, "walk.html", article=True))

# ---- the newspaper index, as a sub-page of Media (headlines, rolled up by theme)
NEWS = _json.loads(_arch("news-index.json"))
THEME_NAMES = {"flooding": "Floods", "churches": "Churches", "building-development": "Buildings and planning", "mills": "Mills and industry",
  "culverts": "Culverts", "river-works": "River works", "water-supply": "Water supply", "litter-pollution": "Litter and pollution", "bridges": "Bridges",
  "people": "People", "accidents": "Accidents", "crime": "Crime", "schools": "Schools", "arts": "Arts", "alcohol": "Alcohol", "tunnel": "Tunnels",
  "poddle-guard": "The Poddle Guard", "poddle-tax": "The Poddle Tax", "general-information": "General"}
for n in NEWS:
    n["themes"] = [t for t in n["themes"] if t in THEME_NAMES] or ["general-information"]
    n["title"] = n["title"].strip()
_count = {}
for n in NEWS:
    _count[n["themes"][0]] = _count.get(n["themes"][0], 0) + 1
_order = [t for t in THEME_NAMES if t in _count]
NEWS.sort(key=lambda n: n["title"].lower().lstrip("‘'\"“"))
news_groups = "".join(
  f'<details class="news-group" id="{t}"><summary><strong>{esc(THEME_NAMES[t])}</strong> <span>{_count[t]} article{"" if _count[t] == 1 else "s"}</span></summary><ul class="arch-news">'
  + "".join(f'<li>{esc(n["title"])}</li>' for n in NEWS if n["themes"][0] == t) + '</ul></details>' for t in _order)
news_body = ('<div class="wrap page"><p class="crumb"><a href="media.html">Media</a></p><header class="page-head"><p class="kicker">Media</p><h1>The Poddle in the newspapers</h1>'
  f'<p class="dek">{len(NEWS)} newspaper articles about the river, from the 1730s to the 2010s, found and transcribed by volunteers of the {CWHG}. Open a theme to see its headlines, or search them all.</p></header>'
  '<aside class="brief"><strong>Coming soon</strong><p>The full transcriptions and scans of these articles are being added to the site. Until then, many of their stories are told on the '
  '<a href="walk.html">river walk</a> pages, and 17 original clippings can be seen on the <a href="floods.html">floods</a> and <a href="city-watercourse.html">City Watercourse</a> pages.</p></aside>'
  '<label class="arch-search"><span>Search the headlines</span><input type="search" id="news-q" placeholder="e.g. flood, mill, Swift" autocomplete="off"></label>'
  f'<p class="note" id="news-n" aria-live="polite">{len(NEWS)} articles in {len(_order)} themes.</p>'
  f'<div class="news-groups" id="news-groups">{news_groups}</div>'
  + CREDIT_NOTE + '</div>'
  '<script>(function(){var q=document.getElementById("news-q"),n=document.getElementById("news-n"),gs=[].slice.call(document.querySelectorAll(".news-group"));'
  'q.addEventListener("input",function(){var s=q.value.trim().toLowerCase(),c=0;gs.forEach(function(g){var k=0;[].forEach.call(g.querySelectorAll("li"),function(li){'
  'var ok=!s||li.textContent.toLowerCase().indexOf(s)>-1;li.hidden=!ok;if(ok)k++;});g.hidden=!k;g.open=!!s&&k>0;c+=k;});'
  'n.textContent=s?c+" matching headlines.":"' + str(len(NEWS)) + ' articles in ' + str(len(_order)) + ' themes.";});})();</script>')
write("media-newspapers.html", shell("media-newspapers", f"The Poddle in the newspapers · {SITE}",
      f"{len(NEWS)} newspaper articles about Dublin’s River Poddle, by theme: floods, mills, culverts, the Poddle Tax and more.", news_body, "media.html"))
MEDIA_NEWS_CARD = ('<section class="media-group" id="newspapers"><h2>The Poddle in the newspapers</h2>'
  f'<p>{len(NEWS)} newspaper articles about the river, from the 1730s to the 2010s, gathered by volunteers of the {CWHG}: floods, mills, culverts, crimes, the Poddle Tax and the Poddle Guard.</p>'
  '<p class="xlink"><a href="media-newspapers.html">Browse the newspaper index →</a></p></section>')

# ---- the group's research, as a section of the Sources page
WHERE_NOW = "".join(f'<li><a href="{p["url"]}">{esc(p["title"])}</a></li>' for p in sorted(PLACES, key=lambda p: p["title"].lower().lstrip("‘’")))
SOURCES_RESEARCH = (
  '<section id="poddle-research" class="research"><h2>The Crumlin and Walkinstown Poddle research</h2>'
  f'<p>Much of the local detail on this site comes from the Poddle River History Project, a volunteer project of the {CWHG} and Crumlin Community Cleanup. '
  'Its volunteers gave more than 500 hours to finding, transcribing and sorting newspaper articles, photographs, stories and reports about the Poddle and the City Watercourse, '
  'and first published them in October 2024 at the Dublin Festival of History, in Walkinstown Library, with a talk by Cathy Scuffil. Part of the project was funded by the Local Authority Waters Programme.</p>'
  f'<p>In November 2026 the group generously agreed to bring their research together with poddle.ie, so that the river’s story can be told in one place. Their place histories are now part of the '
  '<a href="walk.html">river walk</a> and its meanders, their people are on the <a href="people.html">Poddle People</a> page, and their newspaper index is on the <a href="media-newspapers.html">Media</a> page.</p>'
  f'<p>Thank you to the volunteers: {VOLUNTEERS}, and to the writers and Poddleologists whose work they gathered, among them Finola Watchorn, author of <em>Crumlin and the Way it Was</em>, and Betty Brunkard, author of <em>Basin Street Harbour</em>.</p>'
  '<details class="where-now"><summary>Their places, and where to find them now</summary><ul class="links plain cols">' + WHERE_NOW + '</ul></details>'
  '<p class="note">Corrections and new material are very welcome, through the <a href="about.html#contact">contact form</a>.</p></section>')

# ---- old archive addresses (live briefly in November 2026) now redirect to where the content went
def _redirect(name, to):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(f'<!doctype html>\n<html lang="en-IE"><head><meta charset="utf-8"><title>Moved · {SITE}</title>'
                 f'<meta name="robots" content="noindex"><link rel="canonical" href="{BASE}{to}"><meta http-equiv="refresh" content="0; url={to}"></head>'
                 f'<body><p>This page has moved to <a href="{to}">{to}</a>.</p></body></html>\n')
for _f in os.listdir(OUT):
    if re.fullmatch(r'place-[\w-]+\.html', _f):
        os.remove(os.path.join(OUT, _f))
for p in PLACES:
    if p["slug"] in PLACE_LL or p["slug"] in _titles:  # only the history group's old addresses need redirects
        _redirect(f'place-{p["slug"]}.html', p["url"])
_redirect("archive.html", "sources.html#poddle-research")
_redirect("archive-places.html", "sources.html#poddle-research")
_redirect("archive-people.html", "people.html")
_redirect("archive-news.html", "media-newspapers.html")
_redirect("archive-overview.html", "origins.html#words-and-phrases")

# Map data (read by build_extra.py): meander pins sit in the walk stops layer; places are looked up by ?at=
MEANDERS_JS = [dict(slug=m["slug"], name=m["name"], place=m["place"], teaser=m["teaser"], parent=_stop_n(m["parent"]),
                    lat=m["ll"][0], lon=m["ll"][1],
                    pts=[[p["title"], p["ll"][0], p["ll"][1], p["url"]] for p in m["places"] if p["ll"]]) for m in MEANDERS]
