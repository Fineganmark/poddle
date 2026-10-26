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
 ("Ravensdale Mills", 53.3140, -6.2990, "Corn and flour mill with pond, sluice and weir; on maps from the 1830s to 1940."),
 ("Farrington’s Mill", 53.3121, -6.2997, "Flour mill by Kimmage Cross Roads; water turbine until the 1920s. Approximate site."),
 ("Larkfield Mills", 53.3175, -6.2950, "Mill and pond, now Sundrive Shopping Centre. Approximate site."),
 ("Mill and windmill, St Martin’s Drive", 53.3167, -6.2956, "Mill, pond and windmill on the first Ordnance Survey map."),
 ("Loader’s Park Mills", 53.3207, -6.2872, "Corn mill on Kimmage Road Lower, now the Waterwheel apartments. Approximate site."),
 ("Mount Argus mills", 53.3226, -6.2841, "Paper mill, and a flour mill on Mount Argus Road that became a laundry."),
 ("Harold’s Cross Park watermill", 53.3246, -6.2789, "One of several 19th-century mills in the village."),
 ("Mill pond, Our Lady’s Hospice", 53.3277, -6.2815, "Shown on the 1910 Ordnance Survey map."),
 ("Greenmount Mills", 53.3289, -6.2785, "Corn mill, then a cotton mill by 1807; enlarged by the Pim family."),
 ("Double mill, Mill Street", 53.3368, -6.2782, "Oil and flour mill linked to St Thomas’s Abbey. Approximate site."),
 ("Medieval mill, Cross Poddle", 53.3386, -6.2725, "Beside St Nicholas’ Bridge, New Street."),
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
