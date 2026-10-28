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
 ("Mount Down Mill", 53.3044, -6.3188, "Flour mill where the City Watercourse met the stream from Tallaght; shown as disused on the 1906 to 1909 Ordnance Survey map. Position after the Crumlin and Walkinstown History Group’s map, so approximate.", "mount-down"),
 ("Ravensdale Mills and Farrington’s Mill", 53.3131, -6.2994, "Corn and flour mill with pond, sluice and weir (Ravensdale, 1830s to 1940), and Farrington’s flour mill by Kimmage Cross Roads, which used a water turbine until the 1920s. Farrington’s site is approximate.", "ravensdale"),
 ("Larkfield Mills and the St Martin’s Drive mill", 53.3171, -6.2953, "Larkfield mill and pond, now Sundrive Shopping Centre, and a mill, pond and windmill on the first Ordnance Survey map near St Martin’s Drive. Approximate site.", "larkfield"),
 ("Loader’s Park Mills", 53.3207, -6.2872, "Corn mill on Kimmage Road Lower, now the Waterwheel apartments. Approximate site.", "loaders-park"),
 ("Mount Argus mills", 53.3226, -6.2841, "Paper mill, and a flour mill on Mount Argus Road that became a laundry.", "mount-argus"),
 ("Harold’s Cross Park watermill", 53.3246, -6.2789, "One of several 19th-century mills in the village.", "harolds-cross-park"),
 ("Greenmount Mills and the Hospice mill pond", 53.3283, -6.2800, "Greenmount: a corn mill, then a cotton mill by 1807, enlarged by the Pim family. Beside it, the mill pond by Our Lady’s Hospice shown on the 1910 Ordnance Survey map.", "greenmount"),
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
DIGS = [
 ("Tenters Blackpitts, Mill Street", 53.3367, -6.2756, "Digs in 2005, 2007 and 2016 found a possible river channel, a red-brick culvert, tannery remains and two de-hairing barrels. The 2009 planning drawings show the culvert about two metres below the street.", "planning-record", "Archaeological dig"),
 ("Reuben Street watercourse", 53.3344, -6.2906, "A watercourse recorded by the National Monuments Service, and the medieval City Watercourse found in two investigations nearby. Position from the record’s grid reference.", "planning-record", "Recorded watercourse"),
 ("Site of Donore Castle", 53.3372, -6.2812, "A medieval castle in a borough mentioned in 1228, shown on the 1837 map. No trace is visible; the site is now a business park. The 2006 plans for the neighbouring Donore Avenue site show the Poddle culvert running diagonally across it, with a 6 m keep-clear strip.", "planning-record", "Recorded monument"),
 ("Site of Tymon Castle", 53.2883, -6.3606, "A 15th-century tower house in Tymon Park, drawn by Beranger in 1763 and demolished in 1960.", "planning-record", "Recorded monument"),
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
# (joined across the unmapped gap); the City Watercourse follows OSM way 1495732873 to Dolphin's Barn; the rest are schematic routes, labelled approximate on the map.
ABBEY = [[[53.3277939, -6.2800296], [53.3278556, -6.2800591], [53.3280273, -6.280042], [53.3284619, -6.2808933], [53.3292486, -6.2799204], [53.3294889, -6.2799365], [53.3295818, -6.2799204], [53.3296107, -6.2799687], [53.3296683, -6.2799741], [53.3298798, -6.2799097], [53.3301585, -6.27984]],
         [[53.3301585, -6.27984], [53.3342733, -6.2846827]],
         [[53.3342733, -6.2846827], [53.3344196, -6.2849265], [53.3349418, -6.2855188], [53.334991, -6.2857638], [53.3350558, -6.2860863], [53.3351109, -6.287323], [53.3351348, -6.2878031], [53.3353086, -6.2883523], [53.335491, -6.288746], [53.335642, -6.2892779]]]
CHANNELS = [
 dict(k="abbey", n="The Abbey Stream", approx=False, slug="city-watercourse", c=ABBEY,
      note="The channel marked Abbey Stream on OpenStreetMap, leaving the Poddle near the Hospice and Greenmount at Harold’s Cross and heading north-west towards St Thomas’s Abbey. The straight link across the culverted middle is approximate."),
 dict(k="citywc", n="The City Watercourse", approx=True, slug="city-watercourse",
      c=[[53.32031, -6.29067], [53.32035, -6.29063], [53.32039, -6.29053], [53.32044, -6.29041], [53.32051, -6.29022], [53.32077, -6.29037], [53.32156, -6.29059], [53.32172, -6.29059], [53.32180, -6.29052], [53.32187, -6.29044], [53.32196, -6.29034], [53.32239, -6.29014], [53.32248, -6.28998], [53.32273, -6.28942], [53.32281, -6.28942], [53.32431, -6.28960], [53.32520, -6.28975], [53.32587, -6.28998], [53.32624, -6.29016], [53.32653, -6.29031], [53.32803, -6.29118], [53.32828, -6.29182], [53.33002, -6.29267], [53.33081, -6.29346], [53.33119, -6.29427], [53.33142, -6.29454], [53.33319, -6.29533], [53.33366, -6.29501], [53.33409, -6.29472], [53.33457, -6.29412], [53.33671, -6.29198], [53.33853, -6.28979], [53.33880, -6.28938], [53.34071, -6.28936], [53.34209, -6.28600], [53.34210, -6.28451], [53.34301, -6.28068], [53.34278, -6.27903], [53.34274, -6.27763], [53.34303, -6.27604], [53.34320, -6.27444], [53.34269, -6.27173]],
      note="The artificial channel that took a third of the flow from the Stone Boat past Eamonn Ceannt Park and along Rutland Avenue to Dolphin’s Barn, then on to Basin Lane, James’s Street and Thomas Street. From the Stone Boat to Dolphin’s Barn the line follows the OpenStreetMap route, which its mappers drew from the 1912 Ordnance Survey six-inch map, the 1870 one-inch map and Taylor’s 1816 map; north of Dolphin’s Barn, past the Back of the Pipes and the James’s Street basin and along Thomas Street and High Street to Christ Church, it follows the hand-drawn map of the Crumlin and Walkinstown History Group, which gives no source for its lines. All of it is approximate."),
 dict(k="citywc", n="The City Watercourse, from the Dodder", approx=True, slug="balrothery-weir",
      c=[[53.28877, -6.33132], [53.28873, -6.33060], [53.28884, -6.32931], [53.28896, -6.32895], [53.28929, -6.32763], [53.28951, -6.32674], [53.28993, -6.32593], [53.29066, -6.32479], [53.29124, -6.32389], [53.29202, -6.32287], [53.29287, -6.32187], [53.29343, -6.32155], [53.29411, -6.32072], [53.29423, -6.32035], [53.29428, -6.31990], [53.29418, -6.31858], [53.29437, -6.31768], [53.29520, -6.31674], [53.29570, -6.31638], [53.29602, -6.31631], [53.29731, -6.31980], [53.29751, -6.32002], [53.29838, -6.31945], [53.29864, -6.31922], [53.29911, -6.31883], [53.30125, -6.31857], [53.30233, -6.31876], [53.30308, -6.31958], [53.30348, -6.31960], [53.30433, -6.31899], [53.30461, -6.31877], [53.30479, -6.31898]],
      note="The first stretch of the City Watercourse, from the sluices at Balrothery (Firhouse) Weir past Templeogue House to the stream from Tallaght near Mount Down. Drawn after the hand-drawn map of the Crumlin and Walkinstown History Group, which joins the two at Mount Down; older accounts put the meeting a little further north, near Whitehall. Route approximate."),
 dict(k="tenter", n="The Tenter Water", approx=True, slug="city-watercourse",
      c=[[53.32671, -6.28999], [53.32681, -6.28811], [53.32821, -6.28728], [53.33119, -6.28790], [53.33496, -6.28473], [53.33658, -6.27964], [53.33714, -6.27501]],
      note="A branch of the City Watercourse that rejoined the Poddle at Fumbally Lane. The line follows the hand-drawn map of the Crumlin and Walkinstown History Group, which takes it off the City Watercourse at Rutland Avenue and across Donore to Blackpitts; it gives no source. Route approximate."),
 dict(k="commons", n="The Commons Water", approx=True, slug="st-patricks",
      c=[[53.33662, -6.29141], [53.33742, -6.28986], [53.33787, -6.28751], [53.33856, -6.28484], [53.33860, -6.28375], [53.33877, -6.28160], [53.33881, -6.28073], [53.33897, -6.27970], [53.33937, -6.27993], [53.33970, -6.27936], [53.33994, -6.27797], [53.33973, -6.27580], [53.33900, -6.27267]],
      note="The Poddle’s one real tributary, also called the Common Water. It rose in Crumlin and joined the Poddle near the corner of the Coombe and Patrick Street. Only the city stretch is drawn, from the Back of the Pipes along the Cork Street area to Cross Poddle, after the hand-drawn map of the Crumlin and Walkinstown History Group, which gives no source. Route approximate."),
 dict(k="abbey", n="The Abbey Stream, lower course", approx=True, slug="city-watercourse",
      c=[[[53.335642, -6.2892779], [53.33664, -6.29145], [53.33803, -6.28972], [53.33941, -6.28696], [53.34051, -6.28460], [53.34082, -6.28470], [53.34120, -6.28130], [53.34005, -6.28058], [53.33676, -6.27819], [53.33687, -6.27723]]],
      note="Where the Abbey Stream went after the mapped channel ends: round by Marrowbone Lane and Pimlico towards St Thomas’s Abbey, then down by Ardee Street to rejoin the Poddle near New Row. Joined up by eye from the fragments on the hand-drawn map of the Crumlin and Walkinstown History Group, which gives no source. Route approximate."),
 dict(k="overflow", n="The Dodder Overflow", approx=True, slug="dodder-overflow",
      c=[[53.3072, -6.3180], [53.3071, -6.3142], [53.3068, -6.3138], [53.3069, -6.3127], [53.3065, -6.3117], [53.3055, -6.3112], [53.3056, -6.3108], [53.3060, -6.3068], [53.3047, -6.2962], [53.3065, -6.2930]],
      note="Traced from the flood scheme’s map of the Lakeland Overflow: from the sluice at Whitehall Park past Wainsfort Manor, along College Drive and across Wainsfort and Fortfield Roads to the ponds at Terenure College (the Lakelands), which drain to the Dodder at Bushy Park. Route traced by eye, so approximate."),
]
MAPDATA = json.dumps(dict(river=river, stops=stops_js, mills=MILLS, works=WORKS, digs=DIGS, gauges=GAUGES, channels=CHANNELS), ensure_ascii=False)

map_body = (
 '<div class="wrap page"><header class="page-head"><p class="kicker">Map</p><h1>The Poddle on today’s map</h1>'
 '<p class="dek">Every stop on the river walk, the City Watercourse, the Abbey Stream, the Tenter and Commons Waters, the Dodder Overflow, the mill sites and the flood works, on a modern street map. '
 'Tap a marker to see the place, then follow the link to its history. Routes are drawn as best we can: the river has been moved, culverted and rebuilt many times, so treat every line as a friendly guide rather than a survey.</p></header>'
 '<div class="map-shell"><div id="map" role="region" aria-label="Map of the River Poddle"></div>'
 '<div id="layers" class="layers-below" aria-label="Choose what to show on the map"></div><ul class="legend" aria-label="Map key">'
 '<li><span class="k k-open"></span>River, open channel</li><li><span class="k k-under"></span>River, underground</li>'
 '<li><span class="k k-water"></span>City Watercourse (approx.)</li><li><span class="k k-abbey"></span>Abbey Stream</li><li><span class="k k-commons"></span>Commons Water (approx.)</li><li><span class="k k-overflow"></span>Dodder Overflow (approx.)</li><li><span class="k k-stop">1</span>River walk stop</li>'
 '<li><span class="k k-mill"></span>Mill site</li><li><span class="k k-works"></span>Flood scheme works</li>'
 '<li><span class="k k-dig"></span>Archaeology and monuments</li><li><span class="k k-gauge"></span>River gauge (Dodder)</li></ul></div>'
 '<p class="note">River line © OpenStreetMap contributors. The City Watercourse, Tenter Water and Dodder Overflow are approximate routes, not surveyed lines. The City Watercourse as far as Dolphin’s Barn follows the OpenStreetMap line, which was drawn from old Ordnance Survey and Taylor maps; The rest of the City Watercourse, the Tenter Water, the Commons Water and the lower Abbey Stream follow the hand-drawn map of the <a href=\"https://poddle.crumlinwalkinstownhistory.ie/\" rel=\"noopener\">Crumlin and Walkinstown History Group’s Poddle project</a>, which gives no source for its lines. Some mill sites are approximate too, and say so.</p>'
 '<noscript><p>The map needs JavaScript. The river walk is also listed on the <a href="walk.html">river walk page</a>.</p></noscript></div>'
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
<li><a href="https://www.floodinfo.ie/map/floodmaps/" rel="noopener">floodinfo.ie flood maps</a>: the national interactive flood map. Zoom to Harold’s Cross, Kimmage or Templeogue and switch on the river flood extents to see the modelled flood outlines along the Poddle.</li>
<li><a href="https://www.floodinfo.ie/map/floodplans/" rel="noopener">floodinfo.ie flood plans</a>: the flood risk management plans and the schemes proposed for each area.</li>
<li><a href="https://www.poddlefas.ie/" rel="noopener">poddlefas.ie</a>: the flood alleviation scheme’s own site, with the project background and updates.</li>
<li><a href="https://data.gov.ie/dataset/wfd-river-waterbody-status-2016-2021" rel="noopener">River water quality status, 2016 to 2021</a>: the EPA’s ecological status for every river, the Poddle included.</li>
<li><a href="https://waterlevel.ie/" rel="noopener">waterlevel.ie</a>: all the Office of Public Works’ live gauges, with downloads.</li>
</ul>
<p>A 1-in-100-year flood is a flood with a 1% chance of happening in any one year. It is the standard the Poddle scheme is built to.</p></section>
</div></div></div>
<script src="levels.js?v=''' + ASSET_V + '''"></script>'''
live_body = re.sub(r'<a href="(https?://[^"]+)"( rel="noopener")?>', r'<a href="\1" target="_blank" rel="noopener noreferrer">', live_body)
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
 "duncan": ("img/duncan-1821-poddle.jpg", "Duncan’s map of the County of Dublin, 1821, showing the Poddle flowing north-east from Tallaght. Figure 11-6. From the River Poddle flood scheme environmental impact assessment report, Chapter 11 (An Bord Pleanála case 306725)."),
 "os1843k": ("img/os-1843-kimmage.jpg", "Ordnance Survey six-inch map, 1843, showing the Poddle through Kimmage, with the Mount Down flour mill at lower left. Figure 11-7. From the River Poddle flood scheme environmental impact assessment report, Chapter 11 (An Bord Pleanála case 306725)."),
 "os1843h": ("img/os-1843-harolds-cross.jpg", "Ordnance Survey six-inch map, 1843, from Kimmage towards Harold’s Cross. Figure 11-8. From the River Poddle flood scheme environmental impact assessment report, Chapter 11 (An Bord Pleanála case 306725)."),
 "os1876t": ("img/os-1876-tinker-mill.jpg", "Ordnance Survey five-foot map, 1876, showing Tinker Mill and Brook Lawn. Figure 11-9. From the River Poddle flood scheme environmental impact assessment report, Chapter 11 (An Bord Pleanála case 306725)."),
 "os1876l": ("img/os-1876-larkfield.jpg", "Ordnance Survey five-foot map, 1876, showing Larkfield Mill and its ponds. Figure 11-10. From the River Poddle flood scheme environmental impact assessment report, Chapter 11 (An Bord Pleanála case 306725)."),
 "os1906mj": ("img/os-1906-mount-jerome.jpg", "Ordnance Survey 25-inch map, 1906 to 1909, showing Mount Jerome and Harold’s Cross. Figure 11-11. From the River Poddle flood scheme environmental impact assessment report, Chapter 11 (An Bord Pleanála case 306725)."),
 "taylor": ("img/taylor-1816-tongue.jpg", "Taylor’s map of the environs of Dublin, 1816, from Kimmage to Harold’s Cross, with the Tongue and a mill. Figure 11-5. From the River Poddle flood scheme environmental impact assessment report, Chapter 11 (An Bord Pleanála case 306725)."),
}
MILL_PAGES = [
 ("mount-down", "Mount Down Mill (Domville Mill)", "Templeogue", "Approximate site", "Duncan’s 1821 map of Dublin shows Domville Mill at Templeogue, upstream of Kimmage. Old accounts of the City Watercourse say the Poddle joined it at Mount Down Flour Mills. The 1906 to 1909 Ordnance Survey map labels it Mount Down Mill and shows it as disused. Local histories use the mill to mark the end of the Tymon River section.", ["duncan", "os1843k"], []),
 ("ravensdale", "Ravensdale Mills and Farrington’s Mill", "Kimmage Road Lower and Kimmage Cross Roads", "Farrington’s site approximate", "Two mills worked side by side on this stretch. Ravensdale Mills was a corn and flour mill with its own pond, sluice and weir, on maps from the 1830s until 1940. Farrington’s Mill, beside Kimmage Cross Roads, was a flour mill that worked by water turbine until the 1920s. The 1843 Ordnance Survey map also shows Cutlers Mill and its millrace, and a flour mill with a pond in the Kimmage demesne, and the flood scheme’s heritage report says remains of the Ravensdale mill and Cutlers millrace may survive below ground. Ravensdale Park, beside the site, is one of the places being reshaped to store flood water in the flood alleviation scheme.", ["os1843k"], ["kimmage"]),
 ("larkfield", "Larkfield Mills and the St Martin’s Drive mill", "Sundrive Shopping Centre and St Martin’s Drive", "Approximate site", "Larkfield Mills, a mill with its pond, stood where the Sundrive Shopping Centre is now, and the name Larkfield survives in the area. Close by, near St Martin’s Drive, the first Ordnance Survey map shows another mill, a pond and a windmill together. The 1876 map names Tinker Mill and Larkfield Mill in the Brook Lawn and Sundrive Road area.", ["os1876t", "os1876l"], ["poddle-park"]),
 ("loaders-park", "Loader’s Park Mills", "Kimmage Road Lower", "Approximate site", "Local histories describe a corn mill on Kimmage Road Lower, and the building survives as the Waterwheel apartments. The flood scheme’s heritage report lists Loader’s Park Mill as a paper mill on the 1906 to 1909 map, south-east of Mount Argus, so the site may have changed use over time. The report finds no significant impact on its millrace.", ["valuation"], []),
 ("mount-argus", "Mount Argus mills", "Mount Argus Road", "", "In the 19th century there was a paper mill here, and a flour mill on Mount Argus Road that later became a laundry. The Stone Boat, where the river divides, is nearby.", ["taylor"], ["jerome"]),
 ("harolds-cross-park", "Harold’s Cross Park watermill", "Harold’s Cross Park", "", "One of several 19th-century watermills in Harold’s Cross village. Another was a flour mill by the gates of Mount Jerome.", ["os1843h"], ["jerome"]),
 ("greenmount", "Greenmount Mills and the Hospice mill pond", "Greenmount and Our Lady’s Hospice, Harold’s Cross", "", "The National Monuments Service records a mill site here. Greenmount was a corn mill that became a cotton mill by 1807 and was enlarged by the Quaker Pim family for cotton and linen. Beside it, a mill pond by Our Lady’s Hospice is shown on the 1910 Ordnance Survey map, and Rev. Myles Ronan’s 1927 map shows a mill pond and a Wood Mill on this part of the river, with the dotted line of an older water course beside them. Greenmount’s mill pond was among the last to disappear, covered over in the late 1960s. The lanes around it now hold small businesses.", ["ronan", "os1906mj"], ["greenmount"]),
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
    mc = next((m for m in MILLS if m[4] == mid), None)
    links = (f' <p class="xlink"><a href="map.html?mill={mid}">Show on the map →</a> · <a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={mc[1]},{mc[2]}" rel="noopener">Street View →</a></p>') if mc else ""
    tag = f' <span class="mill-flag">{esc(flag)}</span>' if flag and flag != "Now" else ""
    cards += (f'<article class="mill-card" id="{mid}"><div class="mill-text"><p class="kicker">{esc(where)}{tag}</p><h2>{esc(name)}</h2>'
              f'<p>{esc(text)}</p>{links}</div>'
              f'<div class="mill-figs">{figs}</div></article>')
mills_body = (
 '<div class="wrap page"><p class="crumb"><a href="history.html">History</a> · <a href="mills.html">The mills</a></p>'
 '<header class="page-head"><p class="kicker">Mill sites</p><h1>The mills of the Poddle, one by one</h1>'
 '<p class="dek">Nine mill sites, some of them groups of neighbours, from Templeogue to New Street, in order from source to sea. Select a mill marker on the <a href="map.html">map</a> to land on its entry here.</p></header>'
 + cards +
 '<p class="note">Almost nothing of these mills is left to see, so the “today” photographs show the river or the street at or near each site, not the mill itself. '
 'Sites marked approximate are placed from old maps and local histories. If you have a photograph or a memory of any of them, <a href="about.html">get in touch</a>.</p></div>')
write("mill-sites.html", shell("mill-sites", f"Mill sites · {SITE}", "The mills on the River Poddle, one by one, with historic maps and photographs of the sites today.", mills_body, "history.html"))

# ---- planning-record page: clickable map of the files
PLAN = [
 ("2768/09", "Tenters, Blackpitts", 53.3367, -6.2756, "Drawings for the Tenters development, 2009: long sections through the culverts about 2 m below the street.", "blackpitts-the-culvert-on-the-drawings"),
 ("4156/06", "Donore Avenue", 53.3372, -6.2812, "2006 plans: culvert crossing the old printing works, with a 6 m keep-clear strip.", "donore-avenue-keeping-clear-of-the-culvert"),
 ("4423/19", "27–29 New Row South", 53.3371, -6.2769, "2019 plans: culvert and culverted mill race under the site; 3 m clear each side; Dutch Billy houses found below the slab.", "new-row-south-the-culvert-and-the-mill-race"),
 ("4223/18", "Ship Street Great", 53.3416, -6.2692, "2018 plans: the Poddle’s line through the city near the Castle, with a Dublin City Council drainage record map.", "ship-street-and-the-castle-the-line-through-the-city"),
]
PLANDATA = json.dumps(dict(river=river, channels=CHANNELS, works=WORKS, files=PLAN), ensure_ascii=False)
_pm = ('<div class="plan-map"><div id="planmap" role="region" aria-label="Map of the planning files"></div>'
       '<p class="note">River line © OpenStreetMap contributors. Marker positions are approximate, from the site addresses.</p></div>'
       '<link rel="stylesheet" href="vendor/leaflet.css"><script src="vendor/leaflet.js"></script>'
       '<script>const PLAN = ' + PLANDATA + ';</script><script src="planmap.js?v=' + ASSET_V + '"></script>')
_p = os.path.join(OUT, "planning-record.html")
_t = open(_p, encoding="utf-8").read()
assert "<!--PLANMAP-->" in _t
open(_p, "w", encoding="utf-8").write(_t.replace("<!--PLANMAP-->", _pm))
