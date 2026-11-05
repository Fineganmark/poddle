# School walks: short, class-sized walks on the open river, one page each.
# Executed from build.py after build_extra.py, sharing its namespace (needs `river`).
# Stop positions for Tymon come from the GPS in Mark's photos of 1 November 2026;
# the Kimmage to Harold's Cross stops are placed from the map data, so check them on the ground.

SCHOOL_WALKS = [
 dict(slug="walk-tymon", name="Tymon Park: the lake, the flood gate and the wetland",
  short="Tymon Park", area="Tymon Park, east of the M50",
  dek="A short there-and-back walk beside the Poddle in Tymon Park, east of the M50. It takes in a lake full of waterbirds, the new gate that holds back floods and a wetland that cleans the water, all on park paths and away from traffic.",
  facts=[("Length", "About 1.6 km there and back"), ("Time", "1 to 1½ hours with stops"),
         ("Start and finish", "The Limekiln Road entrance to Tymon Park, by the Lakeside Birds sign"),
         ("Ground", "Flat park paths and a boardwalk; no roads to cross. Can be muddy after rain."),
         ("Best for", "All classes, 1st to 6th")],
  brief="This is the upper Poddle, out in the open. Children can see where the river is held back in a storm, how plants clean its water, and some of the birds that live on it, then follow it to the edge of the park on its way to the city, about 10 km away.",
  safety=["The lake and river have deep, steep edges in places. Keep the class on the paths and back from the water, especially at the flow-control structure and on the boardwalk.",
          "Don’t visit just after very heavy rain: the lake is designed to rise quickly then, by up to three metres.",
          "Tymon Park is a busy public park with dogs, bikes and runners. Agree a meeting point at the start.",
          "Please don’t feed bread to the birds, and keep away from nests in spring."],
  stops=[
   dict(name="The Limekiln lake", where="At the Lakeside Birds sign, in from the Limekiln Road entrance", lat=53.30372, lon=-6.33971,
    img=("tymon-lake-path", "The path along the Limekiln lake in Tymon Park. Photo: Mark Finegan, November 2026."),
    text=["The Poddle flows through this lake. It is one of the best places in Dublin to see waterbirds: surveys for the flood scheme counted 16 to 19 kinds on the Tymon lakes, including mute swans, mallard, coots, moorhens, tufted ducks, little grebes and gulls. Swans, coots and moorhens nest in the reeds."],
    look="Swans, ducks, coots and moorhens. Herons and little egrets sometimes stand still at the edge, waiting for fish.",
    do="Use the Lakeside Birds sign to name the birds you can see. Make a tally: which bird is the most common today?",
    ask="Why might so many birds choose to live here, in the middle of a city?",
    more=("wildlife", "Wildlife of the Poddle")),
   dict(name="The flood gate", where="The flow-control structure at the east end of the lake", lat=53.30347, lon=-6.33598,
    img=("tymon-flow-control", "The flow-control structure at the eastern end of the Limekiln lake. Photo: Mark Finegan, November 2026."),
    text=["This concrete structure with railings is the first finished part of the River Poddle Flood Alleviation Scheme. It came into use on 20 February 2025. In a big storm it lets only a set amount of water through, so the lake fills up behind the raised bank and can rise by up to three metres. The water is let out slowly once the storm has passed, so the streets downstream in Kimmage and Harold’s Cross don’t flood."],
    look="The raised grassy bank (the embankment) and the opening where the water leaves the lake.",
    do="Find something about three metres tall, like a lamp post or a tree. Imagine the lake rising that high in a storm.",
    ask="Homes in Kimmage and Harold’s Cross flooded in 1987, 1993 and 2011. How does holding water back here help them?",
    more=("floods", "Floods and the flood scheme")),
   dict(name="The wetland that cleans the river", where="The integrated constructed wetland and its boardwalk", lat=53.30408, lon=-6.33039,
    img=("tymon-wetland-boardwalk", "The boardwalk through the integrated constructed wetland, Tymon Park. Photo: Mark Finegan, November 2026."),
    text=["Like most city rivers, the Poddle carries some pollution, washed off roads and roofs or leaking from drains. The city is working hard to fix that. This wetland, built as part of the flood scheme, is part of the answer. In a constructed wetland, water moves slowly through a chain of shallow ponds full of reeds, and the plants, mud and tiny living things take out much of the dirt before it reaches the river.",
          "Surveys found three-spined sticklebacks, a small fish, in the river here. The reeds shelter dragonflies, and on summer evenings bats hunt insects over the reedbeds by the lake."],
    look="Reeds and bulrushes, ponds at different levels, and the information sign at the start.",
    do="Walk the boardwalk quietly and listen. How many different sounds can you hear: birds, wind in the reeds, water, traffic?",
    ask="Why does the water need to move slowly through the wetland to get clean?",
    more=("tymon", "Tymon on the river walk")),
   dict(name="The river leaves the park", where="The small footbridge at the east end of the wetland", lat=53.30396, lon=-6.32816,
    img=("tymon-footbridge", "The footbridge over the Poddle at the east end of the wetland, Tymon Park. Photo: Mark Finegan, November 2026."),
    text=["From here the Poddle runs on in a narrow, steep-sided channel past Whitehall, towards Kimmage. Just past Kimmage Manor it begins its first long run underground, and on its way it passes under Harold’s Cross, the Grand Canal, St Patrick’s Cathedral and Dublin Castle before it reaches the Liffey at Wellington Quay."],
    look="Which way is the water flowing? Look for a grey wagtail, a small grey and yellow bird that bobs its tail by the water.",
    do="Stand on the bridge and point the way the river is going. Then turn round and point back to the lake, upstream.",
    ask="The river goes underground in the city. Why do you think people covered it over?",
    more=("walk", "Follow the river all the way to the Liffey")),
  ],
  workbook="Tymon Park River Walk",
  extra=("Want to go further?", ["Older classes can follow the river upstream on the other side of the M50, where it runs through a beech wood with small ponds and a weir, and then under the motorway through a pair of arched tunnels. The footbridge over the M50 at the south of the park links the two halves; allow at least another hour.",
          "The <a href=\"m50-crossing.html\">M50 crossing</a> and <a href=\"tymon.html\">Tymon</a> pages have photos of that stretch, and the story of Tymon Castle and the esker, a ridge left by the Ice Age."])),

 dict(slug="walk-kimmage-harolds-cross", name="Kimmage to Harold’s Cross: the mill road",
  short="Kimmage to Harold’s Cross", area="Kimmage, Mount Argus and Harold’s Cross",
  dek="A walk down Kimmage Road Lower and Harold’s Cross Road, following the Poddle through the old mill country, past the Stone Boat that split the river in 1245, to the Grand Canal, where the river dives underneath.",
  facts=[("Length", "About 3 km, one way"), ("Time", "2 to 2½ hours with stops"),
         ("Start", "Ravensdale Park, by Kimmage Cross Roads"), ("Finish", "Harold’s Cross Bridge on the Grand Canal"),
         ("Ground", "Footpaths along busy roads and short stretches through parks. Cross at pedestrian lights."),
         ("Short version", "Stops 3 to 5, from Sundrive Road to Mount Argus: under 1 km, about 45 minutes")],
  brief="This is the middle Poddle, where it is in and out of sight. For hundreds of years its water turned mill wheels along this road. Children can find the clues the mills left behind, see the river in a park, and learn how it gets past the Grand Canal.",
  safety=["Kimmage Cross Roads, Sundrive Road and Harold’s Cross Road are busy. Cross only at pedestrian lights and keep the class together on the footpath.",
          "The flood scheme is building walls and bridges in Ravensdale Park and Poddle Park until 2027. Stay outside any hoardings; some paths may be closed.",
          "The river runs between high walls and steep banks. Keep back from railings and never lean over them.",
          "Our Lady’s Hospice and Mount Jerome Cemetery are near the end of the walk. Please pass them quietly."],
  stops=[
   dict(name="Ravensdale Park", where="Off Kimmage Road Lower, just north of Kimmage Cross Roads", lat=53.31442, lon=-6.29962,
    img=None,
    text=["The Poddle comes out from under the crossroads here. On the first Ordnance Survey maps of the 1830s and 1840s this was Ravensdale Mills, a corn and flour mill with its own pond, sluice and weir, still on the map in 1940. Beside the crossroads, Farrington’s flour mill ran a water turbine into the 1920s, and Mr Farrington was said to be the first person in the area with electric light.",
          "Today the park is being reshaped so that it can fill with flood water in a storm, with new walls and a new footbridge."],
    look="The river channel, and the new flood walls being built.",
    do="Look at the land around you. Is the park lower or higher than the road? Why would that help it hold flood water?",
    ask="Why would you build a park that is meant to flood?",
    more=("ravensdale", "Ravensdale and Poddle Park")),
   dict(name="Poddle Park", where="The road named after the river, just north of Ravensdale Park", lat=53.3165, lon=-6.2955,
    img=("os-1876-larkfield", "Ordnance Survey five-foot map, 1876, showing Larkfield Mill and its ponds. From the River Poddle flood scheme environmental impact assessment report, Chapter 11."),
    text=["This road is named after the river. Nearby, Larkfield Mills and its pond stood where Sundrive Shopping Centre is now. Another mill and a windmill stood near today’s St Martin’s Drive, and the stump of a windmill survives in St Martin’s Park.",
          "Residents have photographed grey herons fishing in the river along this stretch."],
    look="The street sign. Then look for the river beside the road, and for a heron standing very still.",
    do="Compare the 1876 map with what you can see now. What has taken the place of the mill ponds?",
    ask="Why do you think the road was named after the river?",
    more=("mill-sites", "The mill sites")),
   dict(name="The Stone Boat", where="From the bridge on Sundrive Road, looking south", lat=53.32046, lon=-6.29055,
    img=("stone-boat", "The Stone Boat dividing the flow"),
    text=["Just east of Sundrive Road, a stone shaped like the bow of a boat sits in the river and splits it in two. The first one was built in 1245, when the Norman city of Dublin was short of water. Two thirds of the water stayed in the Poddle; one third went off in a man-made channel, the City Watercourse, to St Thomas’s Abbey and the city’s drinking water. The stone there now is a modern copy on the same design.",
          "You can see it from the footpath on the bridge: look over the south side, upstream, and the stone is in the river just below you."],
    look="The pointed end of the stone facing the current, and the water parting on either side of it.",
    do="Share out 12 counters, or 12 children, the way the Stone Boat shares out the water. How many go each way?",
    ask="In 1245 there were no taps. Where did people in Dublin get their water?",
    more=("stone-boat", "The Stone Boat")),
   dict(name="The Waterwheel", where="The Waterwheel apartments, Kimmage Road Lower", lat=53.3207, lon=-6.2872,
    img=("os-1843-harolds-cross", "Ordnance Survey six-inch map, 1843, from Kimmage towards Harold’s Cross. From the River Poddle flood scheme environmental impact assessment report, Chapter 11."),
    text=["These apartments stand on the site of Loader’s Park Mills, a corn mill, and their name remembers its waterwheel. Along this short stretch of the Poddle there were once mills at Ravensdale, Larkfield, Loader’s Park, Mount Argus and Harold’s Cross, grinding corn and flour and making paper and cloth."],
    look="The name on the building. On the 1843 map, look for the word “Mill”: how many can you count?",
    do="Hold one hand flat and tilt it. Pour imaginary water down it. Mills were built where the land drops, so the water falls hard on the wheel.",
    ask="Why do you think so many mills were built close together on such a small river?",
    more=("mills", "The mills")),
   dict(name="Mount Argus", where="Mount Argus Park and the church of St Paul of the Cross", lat=53.3218, lon=-6.2850,
    img=("mount-argus-waterfall", "The Poddle at Mount Argus"),
    text=["This is the best place on the walk to see the river itself, tumbling over a weir in the park. A flood pond was made here in the 1980s. In the monastery grounds the river once fed a pond and a millrace for a paper mill.",
          "The church was built in the 1870s. Saint Charles of Mount Argus, a priest known for healing, lived and died here and is buried in the church. Bats have been recorded here, and the old trees in the park may be where they roost."],
    look="The weir, and the river disappearing again at the end of the park.",
    do="Sketch the weir. Draw arrows to show which way the water goes.",
    ask="The river goes underground again just past the park. Where do you think it comes out?",
    more=("mount-argus", "Mount Argus")),
   dict(name="Harold’s Cross Park", where="The village green where Kimmage Road Lower meets Harold’s Cross Road", lat=53.3247, lon=-6.2786,
    img=None,
    text=["Harold’s Cross was once a small mill village. The river runs just west of here, out of sight behind the houses, through the grounds of Our Lady’s Hospice and along the edge of Mount Jerome Cemetery. Downstream, Greenmount Mills made cotton and linen, and its mill pond was not covered over until the late 1960s.",
          "The park makes a good place to stop for a snack before the last stretch."],
    look="The cemetery gates on Harold’s Cross Road. Mount Jerome opened in 1836, and the river runs along its eastern side.",
    do="Count the steps between here and the canal, or time the last stretch, to work out how fast the class walks.",
    ask="The river flooded Harold’s Cross in 2011. Why might a river that runs in pipes still flood?",
    more=("mount-jerome", "Mount Jerome")),
   dict(name="Under the Grand Canal", where="Harold’s Cross Bridge (Robert Emmet Bridge)", lat=53.32990, lon=-6.27711,
    img=("siphon.svg", "How the siphon works. A simplified drawing, not to scale."),
    text=["When the Grand Canal was dug in the 1790s it cut straight across the Poddle’s path. Since then the river has gone underneath it in a siphon: a pipe that dips down below the canal bed and comes up on the far side. In 2003 archaeologists found the river rushing along at least five metres below the ground beside the canal.",
          "From here the Poddle runs underground all the way through the Liberties to the Liffey."],
    look="The canal and the bridge. The river is under your feet, but you can’t see it.",
    do="Fill a bendy straw or a piece of tubing with water at school and try it: water goes down and comes up again on its own if the far end is lower.",
    ask="Why didn’t the canal builders just let the river flow into the canal?",
    more=("mount-jerome", "Under the Grand Canal")),
  ],
  workbook="The Mill Road Walk",
  extra=("Want to go further?", ["From the canal, older classes can carry on along the river’s buried route through the Liberties to St Patrick’s Cathedral, about 1.5 km more, using the <a href=\"st-patricks.html\">St Patrick’s Cathedral</a> page. The <a href=\"shop.html\">Walk the Hidden River</a> workbook covers the city end, from Blackpitts to the Liffey."])),
]

def walk_stop(i, s):
    img = ""
    if s["img"]:
        f, cap = s["img"]
        src = f"img/{f}" if "." in f else f"img/{f}.jpg"
        img = f'<figure class="fig ws-fig"><img src="{src}" alt="{esc(cap)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>'
    rows = "".join(f'<div><dt>{t}</dt><dd>{esc(s[k])}</dd></div>' for t, k in (("Look for", "look"), ("Try this", "do"), ("Talk about", "ask")))
    return (f'<li class="ws" id="stop-{i+1}"><span class="ws-n" aria-hidden="true">{i+1}</span><div class="ws-body">'
            f'<h3><span class="vh">Stop {i+1}: </span>{esc(s["name"])}</h3><p class="ws-where">{esc(s["where"])}</p>'
            + "".join(f"<p>{esc(p)}</p>" for p in s["text"]) +
            f'<dl class="ws-do">{rows}</dl>'
            f'<p class="xlink"><a href="{s["more"][0]}.html">{esc(s["more"][1])} →</a></p></div>{img}</li>')

def walk_page(w):
    bounds = [[s["lat"], s["lon"]] for s in w["stops"]]
    lo = min(b[0] for b in bounds) - 0.004; hi = max(b[0] for b in bounds) + 0.004
    wl = min(b[1] for b in bounds) - 0.006; el = max(b[1] for b in bounds) + 0.006
    near = [r for r in river if any(lo <= c[0] <= hi and wl <= c[1] <= el for c in r["c"])]
    data = json.dumps(dict(river=near, stops=[dict(n=i + 1, name=s["name"], where=s["where"], lat=s["lat"], lon=s["lon"]) for i, s in enumerate(w["stops"])]), ensure_ascii=False)
    facts = "".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in w["facts"])
    others = [o for o in SCHOOL_WALKS if o["slug"] != w["slug"]]
    return (f'<article class="wrap page school-walk"><p class="crumb"><a href="schools.html">For teachers</a> · <a href="walk.html">The river walk</a></p>'
      f'<header class="page-head"><p class="kicker">School walk <span>·</span> {esc(w["area"])}</p><h1>{esc(w["name"])}</h1><p class="dek">{esc(w["dek"])}</p></header>'
      f'<dl class="walk-facts">{facts}</dl>'
      f'<aside class="brief"><strong>In brief</strong><p>{esc(w["brief"])}</p></aside>'
      f'<p class="walk-wb">There is a printable workbook for this walk, <a href="shop.html#workbooks">{esc(w["workbook"])}</a>, at three levels from 1st to 6th class, with activities for every stop.</p>'
      f'<p class="walk-tools"><button class="btn ghost" type="button" onclick="window.print()">Print this walk</button></p>'
      f'<section class="walk-safe"><h2>Before you go</h2><ul>' + "".join(f"<li>{esc(x)}</li>" for x in w["safety"]) +
      f'</ul><p class="note">Please plan the visit under your school’s own outings policy, and walk the route yourself first: paths and works change.</p></section>'
      f'<section class="walk-map"><h2>The route</h2><div id="map" class="map-walk" role="region" aria-label="Map of the {esc(w["short"])} school walk"></div>'
      f'<p class="note">The blue line is the river: solid where it is open, dotted where it runs underground. The numbers are the stops. River line © OpenStreetMap contributors.</p>'
      f'<noscript><p>The map needs JavaScript. The stops are listed below.</p></noscript></section>'
      f'<section class="walk-stops"><h2>The stops</h2><ol class="ws-list">' + "".join(walk_stop(i, s) for i, s in enumerate(w["stops"])) + '</ol></section>'
      f'<section class="walk-more"><h2>{esc(w["extra"][0])}</h2>' + "".join(f"<p>{p}</p>" for p in w["extra"][1]) +
      f'<p>Back in class, the <a href="schools.html">For teachers</a> page has more ideas, and the <a href="shop.html">workbooks</a> include experiments on mills and floods. '
      + " ".join(f'Try the <a href="{o["slug"]}.html">{esc(o["short"])}</a> walk too.' for o in others) + '</p></section></article>'
      '<link rel="stylesheet" href="vendor/leaflet.css"><script src="vendor/leaflet.js"></script>'
      f'<script>window.WALK = {data};</script>'
      f'<script src="mapsafe.js?v={ASSET_V}"></script><script src="flow.js?v={ASSET_V}"></script><script src="walkmap.js?v={ASSET_V}"></script>')

for w in SCHOOL_WALKS:
    write(f'{w["slug"]}.html', shell(w["slug"], f'{w["name"]} · School walk · {SITE}',
          f'A short school walk on the River Poddle in {w["area"]}, Dublin: {w["facts"][0][1].lower()}, with stops, things to look for, activities and safety notes for teachers.',
          walk_page(w), "walk.html", image=next((s["img"][0] for s in w["stops"] if s["img"] and "." not in s["img"][0]), None), article=True))
