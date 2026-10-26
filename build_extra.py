# Map and live-data pages. Executed at the end of build.py, sharing its namespace.
import json

COORDS = {
 "fettercairn-house": (53.29175, -6.39758), "bancroft": (53.29255, -6.35076), "tymon": (53.29092, -6.33429),
 "balrothery-weir": (53.28870, -6.33191), "m50-crossing": (53.30160, -6.34200), "dodder-overflow": (53.30719, -6.31805),
 "kimmage-manor": (53.30853, -6.30862), "ravensdale": (53.31442, -6.29962), "stone-boat": (53.32015, -6.28987),
 "mount-argus": (53.32259, -6.28407), "mount-jerome": (53.32574, -6.28430), "st-patricks": (53.33956, -6.27148),
 "ship-street-little": (53.34230, -6.26900), "dubh-linn": (53.34220, -6.26745), "palace-street": (53.34399, -6.26614),
 "liffey": (53.34573, -6.26541)}
MILLS = [
 ("Ravensdale Mills", 53.3140, -6.2990, "Corn and flour mill with pond, sluice and weir; on maps from the 1830s to 1940.", "ravensdale"),
 ("Farrington’s Mill", 53.3121, -6.2997, "Flour mill by Kimmage Cross Roads; water turbine until the 1920s. Approximate site.", "farringtons"),
 ("Larkfield Mills", 53.3175, -6.2950, "Mill and pond, now Sundrive Shopping Centre. Approximate site.", "larkfield"),
 ("Mill and windmill, St Martin’s Drive", 53.3167, -6.2956, "Mill, pond and windmill on the first Ordnance Survey map.", "st-martins-drive"),
 ("Loader’s Park Mills", 53.3207, -6.2872, "Corn mill on Kimmage Road Lower, now the Waterwheel apartments. Approximate site.", "loaders-park"),
 ("Mount Argus mills", 53.3226, -6.2841, "Paper mill, and a flour mill on Mount Argus Road that became a laundry.", "mount-argus"),
 ("Harold’s Cross Park watermill", 53.3246, -6.2789, "One of several 19th-century mills in the village.", "harolds-cross-park"),
 ("Mill pond, Our Lady’s Hospice", 53.3277, -6.2815, "Shown on the 1910 Ordnance Survey map.", "hospice-pond"),
 ("Greenmount Mills", 53.3289, -6.2785, "Corn mill, then a cotton mill by 1807; enlarged by the Pim family.", "greenmount"),
 ("Double mill, Mill Street", 53.3368, -6.2782, "Oil and flour mill linked to St Thomas’s Abbey. Approximate site.", "mill-street"),
 ("Medieval mill, Cross Poddle", 53.3386, -6.2725, "Beside St Nicholas’ Bridge, New Street.", "cross-poddle"),
]
WORKS = [
 ("Tymon Lake flood storage", 53.2962, -6.3380, "220m embankment and flow-control structure. In use since 20 February 2025."),
 ("Integrated constructed wetland", 53.3010, -6.3330, "Tymon Park, east of the M50."),
 ("Whitehall Park storage", 53.3072, -6.3180, "Channel realignment, embankments and walls beside the Lakelands Overflow."),
 ("Ravensdale Park storage", 53.3144, -6.2996, "Reshaped to store flood water, with flood walls and a new footbridge."),
 ("Poddle Park and St Martin’s Drive", 53.3165, -6.2955, "Walls, a sloped path, a pedestrian bridge and a right-bank wall."),
 ("Mount Argus Close wall", 53.3202, -6.2899, "A 25m flood wall on the right bank."),
]
GAUGES = [
 ("09010", "Waldron’s Bridge, River Dodder", 53.30582, -6.26696),
 ("09369", "Anglesea Road, River Dodder", 53.32788, -6.23091),
]

river = json.load(open(os.path.join(OUT, "data", "river.json")))
stops_js = [dict(n=i + 1, slug=st["slug"], name=st["name"], place=st["place"], teaser=st["teaser"],
                 img=(st["images"][0][0] if st["images"] else None),
                 lat=COORDS[st["slug"]][0], lon=COORDS[st["slug"]][1])
            for i, st in enumerate(STOPS)]
# Channels drawn on top of the river line. The Abbey Stream is the three OpenStreetMap ways named "Abbey Stream"
# (joined across the unmapped gap); the others are schematic routes, labelled approximate on the map.
ABBEY = [[[53.3277939, -6.2800296], [53.3278556, -6.2800591], [53.3280273, -6.280042], [53.3284619, -6.2808933], [53.3292486, -6.2799204], [53.3294889, -6.2799365], [53.3295818, -6.2799204], [53.3296107, -6.2799687], [53.3296683, -6.2799741], [53.3298798, -6.2799097], [53.3301585, -6.27984]],
         [[53.3301585, -6.27984], [53.3342733, -6.2846827]],
         [[53.3342733, -6.2846827], [53.3344196, -6.2849265], [53.3349418, -6.2855188], [53.334991, -6.2857638], [53.3350558, -6.2860863], [53.3351109, -6.287323], [53.3351348, -6.2878031], [53.3353086, -6.2883523], [53.335491, -6.288746], [53.335642, -6.2892779]]]
CHANNELS = [
 dict(k="abbey", n="The Abbey Stream", approx=False, slug="city-watercourse", c=ABBEY,
      note="The channel marked Abbey Stream on OpenStreetMap, leaving the Poddle near the Hospice and Greenmount at Harold’s Cross and heading north-west towards St Thomas’s Abbey. The straight link across the culverted middle is approximate."),
 dict(k="citywc", n="The City Watercourse", approx=True, slug="city-watercourse",
      c=[[53.32015, -6.28987], [53.3235, -6.2950], [53.3285, -6.2985], [53.3325, -6.2950], [53.3375, -6.2960], [53.3405, -6.2945], [53.3418, -6.2915], [53.3425, -6.2855], [53.3432, -6.2790]],
      note="The artificial channel that took a third of the flow from the Stone Boat towards Dolphin’s Barn, Basin Lane, James’s Street and Thomas Street. Route approximate."),
 dict(k="tenter", n="The Tenter Water", approx=True, slug="city-watercourse",
      c=[[53.3432, -6.2790], [53.3405, -6.2770], [53.3375, -6.2745]],
      note="A branch of the City Watercourse that rejoined the Poddle at Fumbally Lane. Route approximate."),
 dict(k="overflow", n="The Dodder Overflow", approx=True, slug="dodder-overflow",
      c=[[53.3072, -6.3180], [53.3071, -6.3142], [53.3068, -6.3138], [53.3069, -6.3127], [53.3065, -6.3117], [53.3055, -6.3112], [53.3056, -6.3108], [53.3060, -6.3068], [53.3047, -6.2962], [53.3065, -6.2930]],
      note="Traced from the flood scheme’s map of the Lakeland Overflow: from the sluice at Whitehall Park past Wainsfort Manor, along College Drive and across Wainsfort and Fortfield Roads to the ponds at Terenure College (the Lakelands), which drain to the Dodder at Bushy Park. Route traced by eye, so approximate."),
]
MAPDATA = json.dumps(dict(river=river, stops=stops_js, mills=MILLS, works=WORKS, gauges=GAUGES, channels=CHANNELS), ensure_ascii=False)

map_body = (
 '<div class="wrap page"><header class="page-head"><p class="kicker">Map</p><h1>The Poddle on today’s map</h1>'
 '<p class="dek">Every stop on the river walk, the City Watercourse, the Abbey Stream, the Dodder Overflow, the mill sites and the flood works, on a modern street map. '
 'Tap a marker to see the place, then follow the link to its history.</p></header>'
 '<div class="map-shell"><div id="map" role="region" aria-label="Map of the River Poddle"></div>'
 '<ul class="legend" aria-label="Map key">'
 '<li><span class="k k-open"></span>River, open channel</li><li><span class="k k-under"></span>River, underground</li>'
 '<li><span class="k k-water"></span>City Watercourse (approx.)</li><li><span class="k k-abbey"></span>Abbey Stream</li><li><span class="k k-overflow"></span>Dodder Overflow (approx.)</li><li><span class="k k-stop">1</span>River walk stop</li>'
 '<li><span class="k k-mill"></span>Mill site</li><li><span class="k k-works"></span>Flood scheme works</li>'
 '<li><span class="k k-gauge"></span>River gauge (Dodder)</li></ul></div>'
 '<p class="note">River line © OpenStreetMap contributors. The City Watercourse, Tenter Water and Dodder Overflow are drawn as approximate routes from the written histories, not surveyed lines. Some mill sites are approximate too, and say so.</p>'
 '<noscript><p>The map needs JavaScript. The river walk is also listed on the <a href="index.html#walk">home page</a>.</p></noscript></div>'
 '<link rel="stylesheet" href="vendor/leaflet.css">'
 '<script src="vendor/leaflet.js"></script>'
 '<script>const DATA = ' + MAPDATA + ';</script>'
 '<script src="map.js?v=' + ASSET_V + '"></script>')
write("map.html", shell("map", f"Map · {SITE}", "Interactive map of the River Poddle: river walk stops, mill sites and flood works.", map_body, "map.html"))

live_body = '''<div class="wrap page"><header class="page-head"><p class="kicker">Live data</p><h1>River levels, flood maps and models</h1>
<p class="dek">What the water is doing now, and where to explore the flood models behind the scheme.</p></header>
<div class="page-grid solo"><div class="text">
<section><h2>Is there a gauge on the Poddle?</h2>
<p>Not one that publishes live readings. The Office of Public Works runs Ireland’s network of river gauges, and none of its public stations is on the Poddle. The nearest are on the Dodder, the river the monks borrowed water from at Balrothery, and the one the Lakelands Overflow still sends flood water back to. When the Dodder is high after heavy rain on the Dublin Mountains, the Poddle is usually rising too.</p></section>
<section><h2>The Dodder now</h2>
<div id="gauges" class="gauges"><p class="muted">Loading the latest readings…</p></div>
<p class="note">Water level in metres above each gauge’s staff zero, over the last seven days. Provisional data from the Office of Public Works via waterlevel.ie, refreshed on this site every hour. Not for flood warning.</p></section>
<section><h2>Flood warnings</h2>
<p>For live weather and rain warnings, check <a href="https://www.met.ie/warnings" rel="noopener">Met Éireann’s warnings page</a>. South Dublin County Council and Dublin City Council post flood alerts on their own channels during events.</p></section>
<section><h2>Explore the flood models</h2>
<p>The flood scheme was designed with a computer model of the river: a hydraulic model that works out how deep and how fast the water runs in floods of different sizes. The model itself isn’t public, but its results are.</p>
<ul class="links">
<li><a href="https://www.floodinfo.ie" rel="noopener">floodinfo.ie</a>: the national flood map portal. Search for Harold’s Cross or Kimmage to see the modelled flood extents along the Poddle.</li>
<li><a href="https://data.gov.ie/dataset/cfram-river-flood-extents-current-scenario" rel="noopener">CFRAM river flood extents</a>: the same flood outlines as open data you can download and map.</li>
<li><a href="https://data.gov.ie/dataset/cfram-model-nodes-current-scenario" rel="noopener">CFRAM model nodes</a>: points along the modelled rivers with predicted levels and flows for each flood size, with future climate scenarios alongside.</li>
<li><a href="https://data.gov.ie/dataset/cfram-modelled-river-centrelines" rel="noopener">CFRAM modelled river centrelines</a>: the river lines the model uses.</li>
<li><a href="https://data.gov.ie/dataset/wfd-river-waterbody-status-2016-2021" rel="noopener">River water quality status, 2016 to 2021</a>: the EPA’s ecological status for every river, the Poddle included.</li>
<li><a href="https://waterlevel.ie/" rel="noopener">waterlevel.ie</a>: all the Office of Public Works’ live gauges, with downloads.</li>
</ul>
<p>A 1-in-100-year flood is a flood with a 1% chance of happening in any one year. It is the standard the Poddle scheme is built to.</p></section>
</div></div></div>
<script src="levels.js?v=''' + ASSET_V + '''"></script>'''
write("river-data.html", shell("river-data", f"Live data · {SITE}", "Live river levels near the Poddle, flood maps and flood model data.", live_body, "river-data.html"))


# ------------------------------------------------------------ mill sites page
WM = "https://upload.wikimedia.org/wikipedia/commons/thumb/"
CUR = {
 "poddle-park": (WM + "9/9e/River_Poddle_at_Poddle_Park.jpg/960px-River_Poddle_at_Poddle_Park.jpg", "The Poddle at Poddle Park, Kimmage, today", "O’Dea, CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:River_Poddle_at_Poddle_Park.jpg"),
 "kimmage": ("https://upload.wikimedia.org/wikipedia/commons/d/d2/The_Poddle_River%2C_Kimmage_-_geograph.org.uk_-_447191.jpg", "The Poddle in Kimmage, 2007", "JP, CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:The_Poddle_River,_Kimmage_-_geograph.org.uk_-_447191.jpg"),
 "jerome": (WM + "3/35/River_Poddle_by_Mount_Jerome_Cemetery_%28geograph_3544859%29.jpg/960px-River_Poddle_by_Mount_Jerome_Cemetery_%28geograph_3544859%29.jpg", "The Poddle by Mount Jerome Cemetery, 2013", "jwd, CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:River_Poddle_by_Mount_Jerome_Cemetery_(geograph_3544859).jpg"),
 "greenmount": (WM + "d/dd/GREENMOUNT_LANE-AVENUE-COURT_%28HOME_TO_A_NUMBER_OF_ENTERPRISING_BUSINESSES%29-200255.jpg/960px-GREENMOUNT_LANE-AVENUE-COURT_%28HOME_TO_A_NUMBER_OF_ENTERPRISING_BUSINESSES%29-200255.jpg", "Greenmount Lane today, home to small businesses", "William Murphy, CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:GREENMOUNT_LANE-AVENUE-COURT_(HOME_TO_A_NUMBER_OF_ENTERPRISING_BUSINESSES)-200255.jpg"),
}
HIST = {
 "valuation": ("img/grifiths-valution.jpg", "Griffith’s Valuation map of Dublin, mid-19th century"),
 "ronan": ("img/mount-jerome-diversion.jpg", "Rev. Myles Ronan’s 1927 map of the Poddle at Harold’s Cross, marking the Wood Mill and a mill pond"),
 "os1848": ("img/1848-os-map-small.jpg", "Ordnance Survey map, 1848"),
}
MILL_PAGES = [
 ("ravensdale", "Ravensdale Mills", "Kimmage Road Lower", "Now", "A corn and flour mill with its own pond, sluice and weir, on maps from the 1830s until 1940. Ravensdale Park, beside the site, is one of the places being reshaped to store flood water in the flood alleviation scheme.", ["valuation"], ["kimmage"]),
 ("farringtons", "Farrington’s Mill", "Kimmage Cross Roads", "Approximate site", "A flour mill beside Kimmage Cross Roads. It worked by water turbine until the 1920s.", ["valuation"], ["kimmage"]),
 ("larkfield", "Larkfield Mills", "Sundrive Shopping Centre", "Approximate site", "A mill with its pond, on ground now covered by the Sundrive Shopping Centre. The name Larkfield survives in the area.", ["valuation"], ["poddle-park"]),
 ("st-martins-drive", "Mill, pond and windmill, St Martin’s Drive", "St Martin’s Drive", "", "The first Ordnance Survey map shows a mill, a pond and a windmill together here.", ["os1848"], ["poddle-park"]),
 ("loaders-park", "Loader’s Park Mills", "Kimmage Road Lower", "Approximate site", "A corn mill on Kimmage Road Lower. The building survives as the Waterwheel apartments, and the name keeps the memory of the wheel.", ["valuation"], []),
 ("mount-argus", "Mount Argus mills", "Mount Argus Road", "", "In the 19th century there was a paper mill here, and a flour mill on Mount Argus Road that later became a laundry. The Stone Boat, where the river divides, is nearby.", ["valuation"], ["jerome"]),
 ("harolds-cross-park", "Harold’s Cross Park watermill", "Harold’s Cross Park", "", "One of several 19th-century watermills in Harold’s Cross village. Another was a flour mill by the gates of Mount Jerome.", ["valuation"], ["jerome"]),
 ("hospice-pond", "Mill pond, Our Lady’s Hospice", "Harold’s Cross", "", "A mill pond shown on the 1910 Ordnance Survey map. Rev. Myles Ronan’s 1927 map shows a mill pond and a Wood Mill on this part of the river, next to the Hospice, with the dotted line of an older water course beside them.", ["ronan"], ["jerome"]),
 ("greenmount", "Greenmount Mills", "Greenmount, Harold’s Cross", "", "A corn mill that was turned into a cotton mill by 1807 and enlarged by the Quaker Pim family for cotton and linen. Greenmount’s mill pond was among the last to disappear, covered over in the late 1960s. The lanes around it now hold small businesses.", ["ronan"], ["greenmount"]),
 ("mill-street", "Double mill, Mill Street", "Mill Street and Sweeney’s Lane", "Approximate site", "An oil and flour mill, linked to St Thomas’s Abbey, which gave Mill Street its name. Mill Street is first mentioned in 1711. By 1830 the street had several tanners and a fancy weaver, and by 1880 five tanners and a parchment maker.", ["valuation"], []),
 ("cross-poddle", "Medieval mill, Cross Poddle", "New Street, beside St Nicholas’ Bridge", "", "A medieval mill beside St Nicholas’ Bridge, outside St Nicholas’ Gate, at the junction of New Street, Patrick Street and Kevin Street. The old Cross Poddle ran beside it.", ["valuation"], []),
]
def mill_fig(kind, key):
    if kind == "h":
        src, cap = HIST[key]
        return f'<figure class="fig"><img src="{src}" alt="{esc(cap)}" loading="lazy"><figcaption>Historic: {esc(cap)}</figcaption></figure>'
    src, cap, credit, page = CUR[key]
    return (f'<figure class="fig"><img src="{src}" alt="{esc(cap)}" loading="lazy" referrerpolicy="no-referrer"><figcaption>Today: {esc(cap)}. '
            f'<a href="{page}" rel="noopener">{esc(credit)}</a></figcaption></figure>')
cards = ""
for mid, name, where, flag, text, hist, cur in MILL_PAGES:
    figs = "".join(mill_fig("h", k) for k in hist) + "".join(mill_fig("c", k) for k in cur)
    mc = next(m for m in MILLS if m[4] == mid)
    sv = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={mc[1]},{mc[2]}"
    tag = f' <span class="mill-flag">{esc(flag)}</span>' if flag and flag != "Now" else ""
    cards += (f'<article class="mill-card" id="{mid}"><div class="mill-text"><p class="kicker">{esc(where)}{tag}</p><h2>{esc(name)}</h2>'
              f'<p>{esc(text)}</p><p class="xlink"><a href="map.html?mill={mid}">Show on the map →</a> · <a href="{sv}" rel="noopener">Street View →</a></p></div>'
              f'<div class="mill-figs">{figs}</div></article>')
mills_body = (
 '<div class="wrap page"><p class="crumb"><a href="history.html">History</a> · <a href="mills.html">The mills</a></p>'
 '<header class="page-head"><p class="kicker">Mill sites</p><h1>The mills of the Poddle, one by one</h1>'
 '<p class="dek">Eleven mill sites from Kimmage to New Street, in order from source to sea. Select a mill marker on the <a href="map.html">map</a> to land on its entry here.</p></header>'
 + cards +
 '<p class="note">Almost nothing of these mills is left to see, so the “today” photographs show the river or the street at or near each site, not the mill itself. '
 'Sites marked approximate are placed from old maps and local histories. If you have a photograph or a memory of any of them, <a href="about.html">get in touch</a>.</p></div>')
write("mill-sites.html", shell("mill-sites", f"Mill sites · {SITE}", "The mills on the River Poddle, one by one, with historic maps and photographs of the sites today.", mills_body, "history.html"))
