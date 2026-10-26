"""Builds the Poddle site: one HTML file per page, sharing site.css.
index.html is written without <html>/<head> wrappers (the Artifact host adds them);
every other page is a full document so it also works on plain static hosting."""
import html, os, hashlib
def _v(*names):
    h = hashlib.md5()
    for n in names:
        h.update(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), n), "rb").read())
    return h.hexdigest()[:8]
ASSET_V = _v("site.css", "map.js", "levels.js")

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "The Poddle"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Young+Serif&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=IBM+Plex+Sans+Condensed:wght@500;600&display=swap">')

# ---------------------------------------------------------------- content
# River stops, source to sea. Each: slug, name, place, teaser, sections[(heading, [paras])], images[(file, caption)], flag
STOPS = [
 dict(slug="fettercairn-house", name="Fettercairn House", place="Tallaght",
  teaser="Where the catchment begins, in the townland of Whitehall.",
  sections=[("Fettercairn House", [
    "Fettercairn House (renamed St Mark’s House in 1985) appears on the first Ordnance Survey map of Ireland, printed in 1837.",
    "The house stands in the townland of Whitehall in Tamhlacht (Tallaght). It marks the southern edge of the Poddle catchment, where the stream is known as the Tymon Stream."]),
   ("The catchment", [
    "The Greater Dublin Strategic Drainage Study (2005) mapped the Poddle catchment beginning near Fettercairn House in Tallaght and stretching north-east through the city to the Liffey."])],
  images=[("fettercarin-house", "Fettercairn House, now St Mark’s House"), ("poddle-catchment", "The Poddle catchment, Greater Dublin Strategic Drainage Study (2005)")]),
 dict(slug="bancroft", name="Bancroft", place="Tallaght",
  teaser="The first stretch of the river you can walk beside.",
  sections=[("Bancroft Castle", [
    "The name Bancroft comes from the castle that once stood at the present junction of Greenhills Road and Tallaght Village.",
    "The castle’s history is uncertain, but its lands formed part of the wider Tymon estate."]),
   ("Bancroft Park", [
    "Bancroft Park, a northern extension of Tymon Park, is the first publicly accessible section of the Poddle. Upstream of here, the channel runs through the grounds of Technological University Dublin."])],
  images=[("bancroft-s-castle", "Bancroft’s Castle (in ruins) on an early Ordnance Survey map"), ("bancroft-park-sdcc-dee-plan-2004", "Bancroft Park, South Dublin County Council plan, 2004")]),
 dict(slug="tymon", name="Tymon", place="Tymon Park",
  teaser="A ruined castle, a glacial esker and the park built around them.",
  sections=[("Tymon Castle", [
    "The castle is thought to have been built in either the 12th or the 15th century, as a defensive outpost against Irish clans raiding the Pale.",
    "By 1547 it was recorded as ruinous, and it seems to have stayed that way, uninhabited for most of its life.",
    "During the 1798 rebellion, the body of a rebel was left at the castle by his comrades after they were attacked by soldiers near Oldbawn. British soldiers then hung it from the doorway and left it there.",
    "The Poddle flowed through the marshy ground below, with the castle on the higher ground of the esker."]),
   ("Tymon estate", [
    "In 1216 King John granted the manor of Timothan to Henry de Loundres (Henry of London), Archbishop of Dublin, and his successors, said to be in recompense for his losses in fortifying Dublin Castle. Ownership later passed through many hands, including William Conolly (1662–1729), Speaker of the Irish House of Commons.",
    "The lands later had a complex mix of owners and uses, including quarrying and farming. The state acquired them in the 1970s and opened them as a public park in 1980."]),
   ("Holding back the flood", [
    "Tymon Park now does a new job for the river. Under the River Poddle Flood Alleviation Scheme, the eastern end of the lake embankment has been raised and the old weir replaced by a flow-control structure. In a big storm, the lake at Limekiln can now rise by up to three metres, holding water back until the peak has passed downstream. The impoundment came into use on 20 February 2025, the first part of the scheme to be finished."]),
   ("Tymon and Greenhills Esker", [
    "Tymon Esker, along which Tymon Lane now runs, is a rare and important feature of the park. An esker is a long ridge of sand and gravel laid down by a stream flowing under a glacier, in this case during the last Ice Age, more than 10,000 years ago.",
    "Tymon Lane, along the ridge, was an important link between Tallaght and the townlands of Dublin, and Tymon Castle was built beside it."])],
  images=[("timon-castle-1791", "Timon Castle, 1791"), ("tymon-aerial-picture", "Tymon Park from the air"), ("greenhills-esker", "The line of the Greenhills Esker")],
  links=[("Video: Tymon Park’s esker (The Echo)", "https://youtu.be/-oMSnnBhdbI"), ("Tymon Park impoundment area becomes operational (Poddle FAS)", "https://www.poddlefas.ie/news/tymon-park-impoundment-area-becomes-operational")]),
 dict(slug="balrothery-weir", name="Balrothery Weir", place="Firhouse, on the Dodder",
  teaser="Where medieval engineers turned the Dodder towards the city.",
  sections=[("The City Weir", [
    "Balrothery Weir, also called Firhouse Weir or the City Weir, sits on the Dodder in the Dodder Valley Park, just off the M50 at exit 12. For centuries it mattered to every citizen of Dublin.",
    "By the early 13th century the Poddle alone could not supply the growing city, so water was taken from the Dodder to top it up. The weir was built at Balrothery by the monks of St Thomas’s Abbey before 1244, and the citizens enlarged it in 1244 to increase the flow.",
    "From the weir, an open channel carried the water under the main Tallaght road and on past Templeogue House, where it met the stream coming down from Tallaght. From that confluence on, the river is the Poddle proper. The Dodder–Poddle system was complete by the middle of the 13th century and stayed in use for around 500 years."]),
   ("A threat to the water", [
    "How much the city depended on this water shows in a story from 1738. Sir Compton Domvile of Templeogue House is said to have saved his nephew, Lord Santry, from execution for murder by threatening to cut off the watercourse where it crossed his land. The city had no other supply, and the threat worked."]),
   ("Crossing the weir", [
    "After the Dodder was straightened and deepened in 1845, the only way across was to wade along the top of the weir. A lattice bridge followed around 1860, replaced by the present bridge, opened by South Dublin County Council in 1995. From the weir you can reach Tymon Park through the M50 underpass."])],
  images=[("diversion-map", "The route of the diversion from the Dodder to the Poddle")]),
 dict(slug="m50-crossing", name="M50 Crossing", place="Tymon Park",
  teaser="Where the motorway sent the river underground.",
  sections=[("The M50", [
    "The M50 was planned in the 1970s, and building began in the 1980s with this section, from the N7 to the N81, first built as a single-carriageway road.",
    "The state’s purchase of the Tymon estate for the park was probably either a result of the road scheme or part of the same plan. The Poddle was presumably culverted at this point to carry it under the future motorway."]),
   ("Western Parkway", [
    "In 1990 the N3 to N81 section of the M50 opened, including the West Link bridge across the Liffey Valley, and this stretch was upgraded from single carriageway to motorway."])],
  images=[("m50-crossing", "The M50 crossing the line of the Poddle"), ("m50-crossing-upgrade", "Plan of the M50 crossing upgrade")]),
 dict(slug="dodder-overflow", name="Dodder Overflow", place="Lakelands, Terenure",
  teaser="A sluice that sends flood water back to the Dodder.",
  sections=[("Diversion", [
    "Upstream of Kimmage Manor, where the Poddle begins its first long run in culverts, the river divides twice. This is the first. Unlike the second, it sends high water out of the Poddle and into the Dodder catchment, by way of storage ponds in Terenure."]),
   ("Overflow to Terenure", [
    "A sluice gate limits how much water carries on towards Kimmage and Kimmage Road Lower. The overflow runs through culverts to the ponds at Terenure College, which drain back to the Dodder at Bushy Park.",
    "You can follow the overflow on the map page, where it is drawn as a green dashed line from the sluice at Whitehall Park to Bushy Park. The line is schematic, since the culverts are underground.",
    "This is the downstream end of the flow controls and channel works in the River Poddle Flood Alleviation Scheme. The scheme followed serious floods in Harold’s Cross and Kimmage in 1987, 1990, 1993 and 2011. It was approved by An Bord Pleanála in June 2023, the Office of Public Works began building it in April 2024, and it is due to be finished in 2027."]),
   ("Refined and defined", [
    "Along this stretch, the scheme proposes to tidy and define the channel and build walls on both sides.",
    "Flows through the Poddle in earlier centuries must have been large, without the ponds at Tymon or these control structures, and with water diverted in from the Dodder at Balrothery as well."])],
  images=[("dodder-overflow", "Route of the Lakelands overflow to the Dodder"), ("dodder-overflow-image", "The overflow channel"), ("dodder-overflow-fas-scheme", "Proposed works, Poddle Flood Alleviation Scheme")],
  links=[("See the overflow route on the map", "map.html"), ("River Poddle Flood Alleviation Scheme: news and updates", "https://www.poddlefas.ie/news")]),
 dict(slug="kimmage-manor", name="Kimmage Manor", place="Kimmage",
  teaser="A Victorian MP’s house, now a mission centre, built over the stream.",
  sections=[("1600s to 1800s", [
    "In 1641 the lands of Kimmage, Terenure and Milltown all belonged to Peter Barnewall, and there was a castle in good repair at Kimmage.",
    "Owners and tenants came and went. Rocque’s map from the mid-18th century shows extensive buildings where the Manor House stands today."]),
   ("Frederick Shaw", [
    "In 1829 Frederick Shaw and his family came to live at Kimmage, in an L-shaped part of the present manor facing today’s Mission House. Sir Frederick lived there until his death in 1876.",
    "A year after moving in, Shaw was elected MP for Dublin City, in 1830, and was re-elected in 1832. He then sat for Dublin University from 1832 to 1848, and became a Privy Councillor in 1835. He was regarded as one of the finest speakers and debaters in Parliament. One of his best-known speeches, in 1834, opposed Daniel O’Connell’s motion for a select committee into Baron Smith, who had been accused of bringing politics into his charge to a grand jury."]),
   ("Bridging the Poddle", [
    "The river enters the grounds from the west and is then piped under later additions to the manor. The manor later became a house of the Holy Ghost Fathers, and then the Kimmage Mission Institute and Development Studies Centre.",
    "The upstream sluice keeps the flow here under control and limits the risk of flooding to the buildings, with most of the water sent around the north of the site."])],
  images=[("kimmage-manor-cover-image", "Kimmage Manor"), ("fredrick-shaw", "Sir Frederick Shaw"), ("kimmage-manor-3d", "Kimmage Manor and the line of the Poddle")],
  links=[("Video: drone footage of Kimmage Manor", "https://youtu.be/e3bgOMpW9Z4")]),
 dict(slug="ravensdale", name="Ravensdale and Poddle Park", place="Kimmage Cross Roads",
  teaser="A valley of mills, and the scheme’s main flood storage in the city.",
  sections=[("Mill country", [
    "Between Kimmage Cross Roads and Sundrive Road the Poddle was once lined with mills. The first Ordnance Survey maps of the 1830s and 1840s show Ravensdale Mills, a corn and flour mill with its own pond, sluice and weir on Kimmage Road Lower, where Ravensdale Park is today. It was still marked on the map in 1940.",
    "Downstream, Larkfield Mills and its pond stood where Sundrive Shopping Centre is now, and another mill and pond sat beside the river near today’s St Martin’s Drive, with a windmill nearby on the same old mill-pond ground. The stump of a windmill survives in St Martin’s Park. At Larkfield, the Plunkett family’s mill and farm later served as a store for weapons landed in the Howth gun-running of 1914.",
    "Near the crossroads, Farrington’s flour mill ran a water turbine into the 1920s; Mr Farrington is remembered as the first person in the area with electric light, until the ESB arrived and he had to stop."]),
   ("St Anne’s and Brooklawn", [
    "Past Kimmage Manor the river runs underground through St Anne’s, comes up near the crossroads, dives under the junction and emerges again in Ravensdale Park. It once flowed through the grounds of Brooklawn, a large house beside the crossroads, and through the St Anne’s estate, where its banks stood fifteen to twenty feet high.",
    "When developers proposed flats on the St Anne’s lands in the early 1970s, with the river to be culverted, the plans were opposed. Dublin Corporation and Dublin County Council refused one scheme for 108 flats on 10 January 1974, citing the river and the land’s zoning as open space."]),
   ("Flood works", [
    "This stretch is central to the River Poddle Flood Alleviation Scheme. Ravensdale Park is being reshaped to store flood water, with new flood walls and a replacement footbridge. Poddle Park gets walls, a sloped path and a new pedestrian bridge, and a flood wall is planned at the end of St Martin’s Drive. Behind Grosvenor Court the river is being realigned with embankments on both sides. Works began in Ravensdale Park in 2025."])],
  images=[],
  links=[("Commencement of works in Ravensdale Park (Poddle FAS)", "https://www.poddlefas.ie/news")]),
 dict(slug="stone-boat", name="The Stone Boat", place="Sundrive Road, Kimmage",
  teaser="The medieval stone that splits the river two to one.",
  sections=[("The Stone Boat", [
    "Just east of Sundrive Road, a stone shaped like the bow of a boat divides the river. The first was built in 1245, when the Norman city of Dublin was short of water. It was rebuilt in 1555, and the stone you see today is a modern replacement on the same design.",
    "The canons of St Thomas’s Abbey carried out extensive works to bring water to their abbey and the city. These works took water from the Dodder at Balrothery to Kimmage, where it joined the Poddle. Here the stone tongue, known locally as the Stone Boat, split the flow two to one: two thirds stayed in the Poddle, and one third went into the City Watercourse."]),
   ("St Thomas’s Abbey", [
    "The City Watercourse, an artificial channel, carried its third of the water north-west towards Dolphin’s Barn. Near today’s Basin Lane it turned east along the south side of James’s Street and through Thomas Street into the city.",
    "The Augustinian Abbey of St Thomas the Martyr lay outside the medieval walls, in the western suburbs just off modern Thomas Street. It was founded in 1177 by William FitzAldelm, custos of Ireland, on behalf of King Henry II, and followed the Victorine rule, like St Augustine’s Abbey in Bristol, so its first canons probably came from Bristol. No trace of the abbey survives."])],
  images=[("stone-boat", "The Stone Boat dividing the flow"), ("st-thomas-abbey", "St Thomas’s Abbey on an early map of Dublin")]),
 dict(slug="mount-argus", name="Mount Argus", place="Harold’s Cross",
  teaser="Flood defences in a park, beside the church of a saint.",
  sections=[("Mount Argus Park", [
    "Past the Stone Boat, most of the Poddle’s flow enters the grounds of Mount Argus. Here modern flood-control features sit in parkland, and this is the last easily reached stretch of the river before its long run underground begins."]),
   ("Mount Argus", [
    "Mount Argus, in Harold’s Cross, was the first Passionist monastery in Ireland, founded in 1856. The present church was built between 1873 and 1878 and dedicated to St Paul of the Cross in 1878."]),
   ("Mills at Mount Argus", [
    "In the monastery grounds the Poddle once fed a pond and a millrace. Harold’s Cross was then a small mill village: a paper mill worked at Mount Argus in the 19th century, and Loader’s Park Mills, a corn mill on Kimmage Road Lower, stood where the Waterwheel apartments are now. On Mount Argus Road a former flour mill later became a laundry, and is now apartments. The old Mount Argus mill, long disused, was taken over in the 20th century by the 45th Mount Argus Scout Troop as a boxing club."]),
   ("Saint Charles", [
    "Charles Houben arrived at the newly founded monastery on 9 July 1857. Known for his gift of healing, he drew as many as 300 people a day to Mount Argus to be blessed.",
    "He died there on 5 January 1893, aged 71. Hundreds of cures were credited to him in his lifetime and after. He was beatified by Pope John Paul II in 1988 and canonised by Pope Benedict XVI on 3 June 2007. In 1949 his remains were moved into the church, where they can still be visited."])],
  images=[("mount-argus-waterfall", "The Poddle at Mount Argus"), ("mount-argus-in-snow", "Mount Argus church in snow"), ("saint-charles", "Saint Charles of Mount Argus")]),
 dict(slug="mount-jerome", name="Mount Jerome", place="Harold’s Cross",
  teaser="A Victorian cemetery, and perhaps another monks’ diversion.",
  sections=[("Mount Jerome", [
    "The General Cemetery Company of Dublin was set up by Robert Shaw under an Act of Parliament in 1834. The first burial took place on 19 September 1836, and there have been about 250,000 since.",
    "As one of Dublin’s main cemeteries it holds many graves of historical interest, among them those of John Millington Synge and Jack B. Yeats."]),
   ("Another diversion?", [
    "To enter Mount Jerome, the Poddle makes an almost right-angled turn.",
    "In his 1927 paper, Rev. Myles Ronan asks whether this was another diversion of the original river, again made for St Thomas’s Abbey, this time to serve its mills. For that reason this stretch is sometimes called the Abbey Stream, though it is more often just called the Poddle, as it carries most of the river’s water. The map page shows the Abbey Stream, which leaves the Poddle just downstream of here, as an amber band."]),
   ("Greenmount and the Hospice", [
    "A flour mill once stood near the cemetery gates. Just downstream, the Poddle powered Greenmount Mills. A corn mill on the site was turned into a cotton mill by James Greenham by 1807, and in the mid-19th century the Quaker Pim family enlarged it, making cotton and linen; the Pims were also known for Irish poplin. The mill pond survived until it was covered over in the late 1960s.",
    "Our Lady’s Hospice, founded in 1845 by Mother Mary Aikenhead, stands on the river’s banks at Harold’s Cross, and the 1910 Ordnance Survey map shows another mill pond in its grounds. In the October 2011 floods, a nurse from the hospice lost her life."]),
   ("Going underground", [
    "The stream enters the cemetery behind the Russian Orthodox Church of the Holy Apostles Peter and Paul, flows under the cemetery’s entrance road and then along its eastern boundary. From here it is culverted under Greenmount, and it passes beneath the Grand Canal in a siphon."])],
  images=[("mount-jerome-image", "The Poddle at Mount Jerome"), ("mount-jerome-diversion", "The possible diversion at Mount Jerome"), ("mount-jerome-map", "Map of Mount Jerome Cemetery")]),
 dict(slug="st-patricks", name="St Patrick’s Cathedral", place="Blackpitts and the Liberties",
  teaser="Built between two streams, and flooded by them for centuries.",
  sections=[("Through the Liberties", [
    "North of the Grand Canal, the culverted river runs along Clanbrassil Street, past Donore Avenue, Warrenmount and Blackpitts. Blackpitts, a name on maps by 1728, probably comes from the pits used by tanners along the river, and Mill Street, first mentioned in 1711, recalls a double mill for oil and flour that is linked to St Thomas’s Abbey. In 1830 the street had several tanners and a fancy weaver; by 1880 it had five tanners and a parchment maker. During a great fire on 22 June 1875, burning whiskey ran into the Poddle beneath Ardee Street and set the river alight.",
    " Near New Row it picks up its ancient course again, and at the junction of New Street, Patrick Street and Kevin Street, the old Cross Poddle, a medieval mill stood on its bank beside St Nicholas’ Bridge, outside St Nicholas’ Gate. At Fumbally Lane it is joined by the Tenter Water, a branch of the City Watercourse, and at the corner of the Coombe and Patrick Street by its one real tributary, the Commons Water, which rises in Crumlin."]),
   ("Between two streams", [
    "Near Patrick Street the Poddle once ran in two channels. The first church of St Patrick was built on the island between them, and the cathedral was founded on the same spot in 1213. It was a holy site and a very wet one."]),
   ("Boats in the nave", [
    "The cathedral flooded again and again. There was an inquiry into blockages near it as early as 1437, and Parliament ordered local people to keep the drains clear in 1493 and again in 1664. In 1701 the flooding was so bad that people could row a boat past the cathedral, and in 1744 services had to move to Christ Church. Major floods followed in 1778, 1791 and 1795, and one in the early 19th century left about five feet of water inside the building."]),
   ("Out of sight", [
    "By the 1860s the river had become an open sewer, blamed for disease as well as flooding, and its lower reaches were roofed over. Under Charles II a Poddle Commission had been set up to manage it, with power to levy a Poddle tax; its powers passed to the Paving Commissioners in 1840. Patrick Street got its brick culvert in the 1920s, and today the cathedral floor sits some seven and a half feet above the water."])],
  images=[]),
 dict(slug="ship-street-little", name="Ship Street Little", place="Dublin Castle",
  teaser="A sheep market, and a ravine as deep as any dig in Dublin.",
  sections=[("Sráid na gCaorach", [
    "Ship Street Little and Ship Street Great, which run along the southern walls of Dublin Castle, are named not after ships but after the sheep market once held here. The Irish name, Sráid na gCaorach, means Street of the Sheep.",
    "The Poddle arrives from the west and flows under Ship Street Little and the Ship Street gate of Dublin Castle."]),
   ("The original channel", [
    "Archaeological excavations in 2020, on a site just south of Ship Street Little and west of Ship Street Great, found that the Poddle here once ran through a ravine that fed into the Dubh Linn.",
    "The ravine was so deep that, at the time of writing, it was the deepest archaeological excavation in the city’s history.",
    "Once the monks of St Thomas’s Abbey had diverted water away, the channel dried up, and the ravine was quarried for stone for the walls of the Norman castle."])],
  images=[("ship-street-ravine", "The ravine uncovered at Ship Street"), ("ship-street-dig", "The excavation site, 2020"), ("ship-street-forty-steps", "The Forty Steps, Ship Street")],
  links=[("RTÉ News: the Ship Street archaeological dig, June 2020", "https://www.rte.ie/news/dublin/2020/0609/1146385-archaeological-dig/")]),
 dict(slug="dubh-linn", name="Dubh Linn", place="Dublin Castle gardens",
  teaser="The black pool that gave the city its name.",
  sections=[("Origin", [
    "The Dubh Linn, the black pool, was a pool on the Poddle just before it met the Liffey.",
    "The tidal, salty Liffey was no good for drinking, so the fresh water of the Poddle was the main drinking supply for the settlement that became Dublin.",
    "The pool may have been darkened by peat carried down from the hills. The Vikings who settled beside it called their town Dyfflin, from the Irish dubh linn. The pool itself lay under what are now the coach house and gardens of Dublin Castle."]),
   ("Defence", [
    "As the city grew, the Poddle became a key defence on its southern side. The stream was channelled, and even dammed, to act as a moat. That dam is said to have given Dame Street, which now runs in front of Dublin Castle, its name."]),
   ("Dubh Linn today", [
    "Behind Dublin Castle, the site of the Dubh Linn is kept as a garden, a monument to its importance and the Poddle’s. The Dubh Linn Garden is bordered by the Chester Beatty Library, Dublin Castle and the Poddle, which now runs underground along its southern edge."])],
  images=[("modern-balc-pool", "The Dubh Linn Garden today"), ("medieval-dublin", "Medieval Dublin"), ("schematic-dublin-castle", "The River Poddle at Dublin Castle")]),
 dict(slug="palace-street", name="Palace Street", place="Dame Street",
  teaser="Under the castle gate, Dame Street and the Olympia.",
  sections=[("Bifurcation", [
    "Inside the gates of Dublin Castle the river divides again, with one channel heading north and the other west."]),
   ("Dame Street", [
    "The river continues north under the Palace Street pedestrian gate of Dublin Castle and on to Dame Street. Dame Street takes its name from the dam on the Poddle, used both for defence and to power a mill."]),
   ("The Olympia", [
    "From the castle gates the stream continues north, under Dame Street and beneath the historic Olympia Theatre."])],
  images=[("dublin-castle-gate", "The Palace Street gate of Dublin Castle"), ("under-olympia-cropped", "The Poddle beneath the Olympia Theatre"), ("podle-beneath-dame-street", "The culvert beneath Dame Street")],
  links=[("The Irish Times: Underground Dublin, a pilgrimage through an ancient tunnel network (2021)", "https://www.irishtimes.com/culture/heritage/underground-dublin-a-pilgrimage-through-an-ancient-tunnel-network-1.4662108"), ("Video: River Poddle in Dublin’s city centre, previously unseen", "https://www.youtube.com/watch?v=SLwzXheosOI")]),
 dict(slug="liffey", name="Liffey Outfall", place="Wellington Quay",
  teaser="Journey’s end, under Wellington Quay.",
  sections=[("The outfall", [
    "The Poddle’s journey ends here, flowing out under Wellington Quay into the Liffey through a grating in the quay wall. The Liffey is tidal here, so at high tide the grating disappears under the water."]),
   ("Wellington Quay", [
    "Wellington Quay was the last of the Liffey quays to be built. It is named after the Dublin-born Arthur Wellesley, 1st Duke of Wellington, after his victory over Napoleon at Waterloo."]),
   ("Ulysses", [
    "In James Joyce’s Ulysses the outfall is placed, wrongly, at Wood Quay, in words that are unflattering but memorable:",
    "<blockquote>“From its sluice in Wood quay wall under Tom Devan’s office Poddle river hung out in fealty a tongue of liquid sewage.”</blockquote>"])],
  images=[("quay-outfall", "The Poddle outfall into the Liffey"), ("wellington-quay", "Wellington Quay"), ("ulysses-cover", "Ulysses, James Joyce")]),
]

HISTORY = [
 dict(slug="heart-of-dublin", name="At the heart of Dublin", when="c. 840 onwards",
  teaser="Drinking water, defence and power for the medieval city.",
  sections=[("At the heart of Dublin", [
    "The modest Poddle is the most historic river in Dublin. The clue is in the name: Dubh Linn, the black pool, was a pool on the stream just outside where Dublin Castle now stands.",
    "It was the city’s main source of drinking water, because the Liffey is tidal and brackish. It formed part of the city’s defences: Dame Street, one of the city’s main streets, is said to be named after the dam that turned the stream into a moat. And it powered the mills of the city’s industries and religious houses."])],
  images=[("dublin-840", "Dublin c. 840"), ("dublin-1000", "Dublin c. 1000"), ("8-the-poddle-approaches-dublin-an-artist-impression-of-the-m", "The Poddle approaches Dublin: an impression of the medieval city by Iain Barber, courtesy of the artist")]),
 dict(slug="origins", name="Origins", when="Source to sea",
  teaser="Why a small stream ended up at the centre of the city.",
  sections=[("Origin story", [
    "The stream rises in the foothills of the Dublin Mountains. Its catchment is bounded by the Dodder to the south and the Camac to the north.",
    "Both of those rivers are larger than the Poddle, but the Poddle is the one that runs to the heart of the city, while its neighbours pass to the east and west of the centre.",
    "Its route is what puts the Poddle at the heart of Dublin, physically and in its history. Today almost all of its last four kilometres, under the south inner city, runs in culverts."]),
   ("Source and names", [
    "The river rises around Cookstown, north-west of Tallaght, about 92 metres above sea level, where its first stretch is known as the Tymon River. Its catchment covers about 16 square kilometres, almost all of it now built up.",
    "The name has changed over the centuries: Podell in 1493, Puddell in 1603, and Poddle from 1695. In Irish it is An Poitéal, and it was also called the Salach, the dirty river."])],
  images=[("poddle-catchment", "The Poddle catchment between the Dodder and the Camac"), ("1848-os-map-small", "Ordnance Survey map, 1848")]),
 dict(slug="first-diversion", name="The first diversion", when="Before 1244",
  teaser="Turning the Dodder into the Poddle at Balrothery.",
  sections=[("The first diversion", [
    "The first great change was the diversion of water from the Dodder into the Poddle at Balrothery Weir, by the monks of St Thomas’s Abbey, before 1244. It was a remarkable piece of engineering. Some 10km from their abbey, the monks dug a new channel that carried part of the Dodder’s flow for over 3km to join the Poddle.",
    "They did it for two reasons. More water meant more power for their mills, and it gave them a larger and steadier supply of drinking water, which they stored in a cistern on what is now Thomas Street. The citizens enlarged the works in 1244, and the system ran for around 500 years."])],
  images=[("diversion-map", "The diversion from the Dodder to the Poddle"), ("dublin-1170", "Dublin c. 1170")],
  link=("balrothery-weir", "See Balrothery Weir on the river walk")),
 dict(slug="second-diversion", name="The second diversion", when="1245",
  teaser="The Stone Boat splits the river for St Thomas’s Abbey.",
  sections=[("The second diversion", [
    "The second diversion was no less ingenious. In 1245, at what is now Harold’s Cross, the stream was split by the Tongue, a stone shaped like the bow of a boat and known locally as the Stone Boat. It sent part of the Poddle’s water west to St Thomas’s Abbey.",
    "You can still see both diversions. The first is no longer used, but its workings can be seen at Balrothery, near Tymon Park, just outside the M50. The Tongue, or Stone Boat, is still in the river near Mount Argus."])],
  images=[("stone-boat", "The Stone Boat"), ("dublin-1370", "Dublin c. 1370")],
  link=("stone-boat", "See the Stone Boat on the river walk")),
 dict(slug="city-watercourse", name="The City Watercourse and the Abbey Stream", when="1245 to 1324",
  teaser="Two channels made for the monks and the city, and how to find them on the map.",
  sections=[("The City Watercourse", [
    "The City Watercourse is an artificial channel. At the Stone Boat, in Harold’s Cross, it took one third of the river’s water: two thirds stayed in the Poddle and one third went into the watercourse, which carried it north-west towards Dolphin’s Barn. Near today’s Basin Lane it turned east along the south side of James’s Street and through Thomas Street into the city.",
    "It was the city’s main water supply for centuries, which is why the 1719 Act of Parliament was written to keep it clean and to stop mill owners starving it of water. A branch of it, the Tenter Water, rejoined the Poddle at Fumbally Lane.",
    "On the map page the City Watercourse is shown as a dashed red line. Only its start and its general direction are recorded in the histories, so the line is an approximate route, not a surveyed one."]),
   ("The Abbey Stream", [
    "The Abbey Stream is the name given on modern maps to a channel that leaves the Poddle near the Hospice and Greenmount, at Harold’s Cross, and runs north-west towards St Thomas’s Abbey. Rev. Myles Ronan’s 1927 map marks a “course of ancient water” heading the same way, across the fields east of the river. Between 1245 and 1324 the monks redirected the river’s course to serve their mills, and this is the kind of channel that diversion would have made.",
    "At Mount Jerome the Poddle itself makes an almost right-angled turn, and Ronan asked whether that too was a diversion made for the abbey. On the map page the Abbey Stream is the amber band; its middle section is under streets, so the link across it is a straight, approximate line."]),
   ("Two channels, one river", [
    "The two are easy to confuse. The City Watercourse leaves the river at the Stone Boat, upstream. The Abbey Stream leaves it further down, at Harold’s Cross, and both were made to serve the abbey and the city."])],
  images=[("stone-boat", "The Stone Boat dividing the flow"), ("st-thomas-abbey", "St Thomas’s Abbey on an early map of Dublin")],
  links=[("See the City Watercourse, Abbey Stream and Dodder Overflow on the map", "map.html")],
  link=("mount-jerome", "See the Mount Jerome turn on the river walk")),
 dict(slug="1719-act", name="The 1719 Act", when="1719",
  teaser="Parliament acts to clean up the city’s water.",
  sections=[("The 1719 Act of Parliament", [
    "An Act of Parliament of 1719 describes the watercourse as “the chief supply of water not only for the inhabitants of the said city; but also for this majesties Castle of Dublin, and without which it would suffer exceeding great prejudice.”",
    "The Act provided for cleaning and repairing the watercourse, because:",
    "<blockquote>“…tuck mills, in which urine, soap and other unwolsome materials are made use of, and diers of linnen and woolen cloath and yarn, and skinners dip, wash, scour and cleanse great quantities of died linnen and woolen cloath, yarn and skins in the said water-course, by which the water is greatly corrupted, endangering the healths of the inhabitants of the said city.”<cite>Original 1719 spelling</cite></blockquote>",
    "Mills along the watercourse were also a problem, building dams and ponds that blocked the flow of water into the city."])],
  images=[("1719-act-of-parlament", "An Act for Cleansing and Repairing the Water-Course, Dublin, 1719")]),
 dict(slug="mills", name="The mills", when="1240s to the 1960s",
  teaser="Seven centuries of water power, from abbey mills to cotton and poplin.",
  sections=[("Why the water mattered", [
    "The Poddle was bent and diverted above all to turn mill wheels. The monks of St Thomas’s Abbey brought Dodder water into it in the 1240s partly for their mills, and between 1245 and 1324 they redirected its course again to serve them. By 1719 Parliament was complaining that mills along the watercourse were building dams and ponds and starving the city of water."]),
   ("From source to sea", [
    "<ul class=\"mill-list\"><li><strong>Mount Down Mill</strong>: local histories use it to mark the end of the Tymon River section, upstream of Kimmage.</li>"
    "<li><strong>Ravensdale Mills</strong>, Kimmage Road Lower: corn and flour, with a pond, sluice and weir, on maps from the 1830s to 1940.</li>"
    "<li><strong>Farrington’s Mill</strong>, Kimmage Cross Roads: flour, with a water turbine until the 1920s.</li>"
    "<li><strong>Larkfield Mills</strong> and a second mill and pond near St Martin’s Drive, with windmills close by.</li>"
    "<li><strong>Loader’s Park Mills</strong>, Kimmage Road Lower: a corn mill, now the Waterwheel apartments.</li>"
    "<li><strong>Mount Argus</strong>: a 19th-century paper mill and a flour mill that became a laundry.</li>"
    "<li><strong>Harold’s Cross</strong>: several watermills, including one in today’s Harold’s Cross Park and a flour mill by Mount Jerome’s gates.</li>"
    "<li><strong>Greenmount Mills</strong>: a corn mill turned cotton mill by 1807, enlarged by the Quaker Pim family for cotton and linen.</li>"
    "<li><strong>Mill Street and Sweeney’s Lane</strong>: a double mill for oil and flour linked to St Thomas’s Abbey.</li>"
    "<li><strong>Cross Poddle</strong>, New Street: a medieval mill beside St Nicholas’ Bridge.</li></ul>"]),
   ("The end of water power", [
    "Steam, electricity and competition from British and foreign manufacturers closed the mills one by one in the late 19th and early 20th centuries. Their ponds were filled in and their races culverted. Greenmount’s mill pond was among the last to go, covered over in the late 1960s. Almost nothing is left to see, but the names survive: Mill Street, the Waterwheel, Larkfield."])],
  images=[("grifiths-valution", "Griffith’s Valuation map of Dublin, mid-19th century")],
  link=("mill-sites", "Each mill site, with maps and photographs")),
 dict(slug="floods", name="Floods and the flood scheme", when="1437 to 2027",
  teaser="Six centuries of flooding, and the scheme being built to stop it.",
  sections=[("A river that floods", [
    "The Poddle has always flooded. The cathedral records run from an inquiry in 1437 to boats being rowed past St Patrick’s in 1701. In the suburbs, serious floods struck Harold’s Cross and Kimmage in 1986, 1993, 2000, 2008 and 2011, and Blackpitts flooded during Hurricane Charlie in 1986."]),
   ("24 October 2011", [
    "On the evening of 24 October 2011, between 80 and 90mm of rain fell on Dublin in six hours. The Poddle burst its banks at Tallaght, Kimmage, Harold’s Cross and Mount Jerome. Across the Dublin region about 1,000 properties flooded, 318 roads were badly flooded, power was lost, and two people died. Both South Dublin County Council and Dublin City Council activated their major emergency plans, and insurance claims were estimated at €127 million."]),
   ("The River Poddle Flood Alleviation Scheme", [
    "The scheme is a joint project of South Dublin County Council, Dublin City Council and the Office of Public Works, which funds it. It is designed to protect more than 800 properties against a 1-in-100-year flood, with an allowance for climate change. The estimated cost was €7 million in 2020, revised to €10 million by 2023.",
    "Its main idea is to store water upstream rather than build high walls in the city. Tymon Lake becomes a flood reservoir behind a 220m embankment and flow-control structure, and Whitehall Park and Ravensdale Park are reshaped to hold water. Downstream, new walls go in at Whitehall Road, Fortfield Road, Poddle Park, St Martin’s Drive and a 25m wall at Mount Argus Close. An integrated constructed wetland in Tymon Park cleans the water, and floating nesting platforms on the lake are for birds."]),
   ("Timeline", [
    "<ol class=\"timeline-list\"><li><span>2011</span> October floods</li><li><span>2018</span> Consultants appointed</li><li><span>Feb 2020</span> Planning application lodged with An Bord Pleanála</li><li><span>Jun 2023</span> Approved, the first flood scheme to go through Part 10 planning</li><li><span>Apr 2024</span> Office of Public Works starts building</li><li><span>20 Feb 2025</span> Tymon Lake flood storage goes into use</li><li><span>2025</span> Works start in Wainsfort and Ravensdale Park</li><li><span>2027</span> Expected completion</li></ol>"]),
   ("Trees and wildlife", [
    "The scheme has not been uncontroversial. When it was published in 2020, local groups including Save the Poddle’s Wildlife Sanctuary objected to the number of trees to be felled and questioned the bird surveys at Tymon Lake. Some argued for moving walls back from the river to create natural floodplain, for example at St Martin’s Drive."])],
  images=[("dodder-overflow-fas-scheme", "Proposed works, Poddle Flood Alleviation Scheme"), ("m50-crossing-upgrade", "Tymon Park works plan")],
  links=[("River Poddle Flood Alleviation Scheme website", "https://www.poddlefas.ie/"), ("Dublin InQuirer: residents debate the scheme (2020)", "https://www.dublininquirer.com/residents-debate-environmental-impact-of-a-plan-to-build-flood-defences-on-the-river-poddle/"), ("Live river levels and flood maps", "river-data.html")]),
]

RESOURCES = [
 ("UCD Digital Library: historic maps of Dublin", "https://digital.ucd.ie/view/ucdlib:40377#c0055-6-6.1"),
 ("South Dublin County Council: River Poddle Flood Alleviation Scheme", "https://consult.sdublincoco.ie/en/consultation/river-poddle-flood-alleviation-scheme-part-10-planning-submission"),
 ("Dublin.ie: The Poddle and Dublin’s hidden rivers", "https://dublin.ie/live/stories/the-poddle-and-dublins-hidden-rivers/"),
 ("Arran Henderson: The best Poddle river", "https://arranqhenderson.com/2017/07/18/the-best-poddle-river/"),
 ("Eastern CFRAM study: Poddle options report", "http://eastcfram.irish-surge-forecast.ie/wp-content/uploads/2011/10/IBE0600Rp0030_Poddle-Options-Report_F02.pdf"),
 ("Ask About Ireland: Griffith’s Valuation", "http://www.askaboutireland.ie/griffith-valuation/"),
 ("Wikipedia: River Poddle", "https://en.wikipedia.org/wiki/River_Poddle"),
 ("River Poddle Flood Alleviation Scheme", "https://www.poddlefas.ie/news"),
 ("Henry de Loundres, Archbishop of Dublin (grant of Timothan, 1216)", "https://www.biblicalcyclopedia.com/L/loundres-henry-de.html"),
]

# ---------------------------------------------------------------- templates
def esc(s): return html.escape(s, quote=True)

def para(p):
    return p if p.startswith("<") else f"<p>{esc(p)}</p>"

NAV = [("index.html", "The river"), ("map.html", "Map"), ("history.html", "History"), ("river-data.html", "Live data"), ("media.html", "Media"), ("sources.html", "Sources"), ("about.html", "About")]

def shell(slug, title, desc, body, active):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    head = (f'<title>{esc(title)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{esc(desc)}">\n{FONTS}\n<link rel="stylesheet" href="site.css?v={ASSET_V}">\n')
    page = (f'<a class="skip" href="#main">Skip to content</a>\n'
            f'<header class="top"><div class="wrap top-in"><a class="brand" href="index.html">The <span>Poddle</span></a>'
            f'<nav aria-label="Main">{nav}</nav></div></header>\n'
            f'<main id="main">{body}</main>\n'
            f'<footer class="foot"><div class="wrap foot-in"><p>The Poddle: a history of Dublin’s hidden river, from Tallaght to the Liffey.</p>'
            f'<p>Photographs and maps are credited where known. Third-party images are used for local-history purposes.</p></div></footer>\n')
    if slug == "index" and not os.environ.get("STATIC"):
        return head + page
    return ('<!doctype html>\n<html lang="en-IE">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + page + '</body>\n</html>\n')

def figures(imgs, lead=False):
    out = []
    for i, (f, cap) in enumerate(imgs):
        cls = "fig lead" if (lead and i == 0) else "fig"
        out.append(f'<figure class="{cls}"><img src="img/{f}.jpg" alt="{esc(cap)}" loading="{"eager" if i == 0 else "lazy"}"><figcaption>{esc(cap)}</figcaption></figure>')
    return "\n".join(out)

def article(item, kicker, prev, nxt, back):
    secs = "\n".join(f'<section><h2>{esc(h)}</h2>{"".join(para(p) for p in ps)}</section>' for h, ps in item["sections"])
    flag = f'<aside class="flag"><strong>To check</strong> {esc(item["flag"])}</aside>' if item.get("flag") else ""
    link = f'<p class="xlink"><a href="{item["link"][0]}.html">{esc(item["link"][1])} →</a></p>' if item.get("link") else ""
    if item.get("links"):
        link += '<section class="watch"><h2>Watch and read</h2><ul>' + "".join(f'<li><a href="{u}"{"" if u.endswith(".html") else " rel=\"noopener\""}>{esc(t)}</a></li>' for t, u in item["links"]) + '</ul></section>'
    pn = '<nav class="pn" aria-label="Previous and next">'
    pn += f'<a class="prev" href="{prev[0]}.html"><span>Upstream</span>{esc(prev[1])}</a>' if prev else '<span></span>'
    pn += f'<a class="next" href="{nxt[0]}.html"><span>Downstream</span>{esc(nxt[1])}</a>' if nxt else '<span></span>'
    pn += '</nav>'
    return (f'<article class="wrap page">'
            f'<p class="crumb"><a href="{back[0]}">{esc(back[1])}</a></p>'
            f'<header class="page-head"><p class="kicker">{kicker}</p><h1>{esc(item["name"])}</h1>'
            f'<p class="dek">{esc(item["teaser"])}</p></header>' +
            (f'<div class="page-grid"><div class="text">{flag}{secs}{link}</div>'
             f'<div class="media">{figures(item["images"], lead=True)}</div></div>' if item["images"] else
             f'<div class="page-grid solo"><div class="text">{flag}{secs}{link}</div></div>') + f'{pn}</article>')

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)

# ---------------------------------------------------------------- pages
# River stops
for i, s in enumerate(STOPS):
    prev = (STOPS[i-1]["slug"], STOPS[i-1]["name"]) if i else None
    nxt = (STOPS[i+1]["slug"], STOPS[i+1]["name"]) if i + 1 < len(STOPS) else None
    kicker = f'Stop {i+1} of {len(STOPS)} <span>·</span> {esc(s["place"])}'
    body = article(s, kicker, prev, nxt, ("index.html#walk", "The river walk"))
    write(f'{s["slug"]}.html', shell(s["slug"], f'{s["name"]} · {SITE}', s["teaser"], body, "index.html"))

# History chapters (prev/next labels say Earlier/Later)
for i, h in enumerate(HISTORY):
    prev = (HISTORY[i-1]["slug"], HISTORY[i-1]["name"]) if i else None
    nxt = (HISTORY[i+1]["slug"], HISTORY[i+1]["name"]) if i + 1 < len(HISTORY) else None
    kicker = f'History <span>·</span> {esc(h["when"])}'
    body = article(h, kicker, prev, nxt, ("history.html", "History"))
    body = body.replace("<span>Upstream</span>", "<span>Earlier</span>").replace("<span>Downstream</span>", "<span>Later</span>")
    write(f'{h["slug"]}.html', shell(h["slug"], f'{h["name"]} · {SITE}', h["teaser"], body, "history.html"))

# Home: intro + the river walk as a line diagram
def stop_li(i, s):
    note = ""
    if s["slug"] == "balrothery-weir":
        note = '<span class="branch in">Dodder water joins here</span>'
    if s["slug"] == "stone-boat":
        note = '<span class="branch out">⅓ of the flow leaves for St Thomas’s Abbey</span>'
    under = ' class="under"' if s["slug"] in ("mount-jerome", "st-patricks", "ship-street-little", "dubh-linn", "palace-street") else ""
    return (f'<li{under}><a href="{s["slug"]}.html"><span class="n">{i+1:02d}</span>'
            f'<span class="t"><strong>{esc(s["name"])}</strong><em>{esc(s["place"])}</em>'
            f'<span class="d">{esc(s["teaser"])}</span>{note}</span></a></li>')

walk = "\n".join(stop_li(i, s) for i, s in enumerate(STOPS))
home = f'''
<section class="hero"><div class="wrap hero-in">
 <div class="hero-text">
  <p class="kicker">Tallaght to Wellington Quay</p>
  <h1>The river that named Dublin</h1>
  <p class="lede">The Poddle is a small stream most Dubliners walk over without knowing. It rises in Tallaght and runs, mostly underground, to the Liffey at Wellington Quay. Yet it gave the city its name. Dubh Linn, the black pool, was a pool on the Poddle beside where Dublin Castle stands. For centuries it was the city’s drinking water, its moat and the power for its mills.</p>
  <p class="lede">This site follows the river from source to sea, stop by stop, and tells the history of how monks, citizens and engineers bent it to the city’s needs.</p>
  <p class="cta"><a class="btn" href="#walk">Walk the river</a><a class="btn ghost" href="history.html">Read the history</a></p>
 </div>
 <figure class="hero-fig"><img src="img/cover-painting.jpg" alt="Painting of a heart shape in river blue" loading="eager"><figcaption>Cover painting</figcaption></figure>
</div></section>

<section id="walk" class="walk"><div class="wrap">
 <header class="sec-head"><p class="kicker">The river walk</p><h2>{ {14: "Fourteen", 15: "Fifteen", 16: "Sixteen"}.get(len(STOPS), len(STOPS)) } stops, source to sea</h2>
  <p>Solid line: open channel. Dotted line: culverted underground.</p></header>
 <div class="walk-grid"><ol class="line">{walk}</ol>
 <div class="walk-maps">{figures([("1848-os-map-small", "Ordnance Survey map of Dublin, 1848"), ("poddle-catchment", "The Poddle catchment, from Tallaght north-east to the Liffey")])}</div></div>
</div></section>

<section class="timeline"><div class="wrap">
 <header class="sec-head"><p class="kicker">History</p><h2>The river’s story in {len(HISTORY)} chapters</h2></header>
 <ol class="tl">{"".join(f'<li><a href="{h["slug"]}.html"><span class="when">{esc(h["when"])}</span><strong>{esc(h["name"])}</strong><span>{esc(h["teaser"])}</span></a></li>' for h in HISTORY)}</ol>
</div></section>
'''
write("index.html", shell("index", "The Poddle", "A history of Dublin’s hidden river, the Poddle, from its source in Tallaght to the Liffey.", home, "index.html"))

# History index
hist = f'''<div class="wrap page"><header class="page-head"><p class="kicker">History</p><h1>How the Poddle shaped Dublin</h1>
<p class="dek">From the black pool of Dubh Linn to the flood scheme being built today.</p></header>
<div class="maps">{figures([("dublin-840","Dublin c. 840"),("dublin-1000","Dublin c. 1000"),("dublin-1170","Dublin c. 1170"),("dublin-1370","Dublin c. 1370")])}</div>
<ol class="tl big">{"".join(f'<li><a href="{h["slug"]}.html"><span class="when">{esc(h["when"])}</span><strong>{esc(h["name"])}</strong><span>{esc(h["teaser"])}</span></a></li>' for h in HISTORY)}</ol></div>'''
write("history.html", shell("history", f"History · {SITE}", "How the Poddle shaped Dublin, from Dubh Linn to the 1719 Act.", hist, "history.html"))

# Sources
src = f'''<div class="wrap page narrow"><header class="page-head"><p class="kicker">Sources</p><h1>Further reading</h1>
<p class="dek">Maps, reports and articles used in putting this site together.</p></header>
<ul class="links">{"".join(f'<li><a href="{u}" rel="noopener">{esc(t)}</a></li>' for t, u in RESOURCES)}</ul>
<section><h2>Printed sources</h2><ul class="links plain">
<li>Rev. Myles V. Ronan, “The Poddle River and its Branches”, Journal of the Royal Society of Antiquaries of Ireland, 6th series, vol. 17, no. 1 (1927), pp. 39–46</li>
<li>Greater Dublin Strategic Drainage Study (2005)</li>
<li>Poddle Flood Alleviation Scheme, Environmental Impact Assessment Report, Non-Technical Summary</li>
</ul></section>
<figure class="fig"><img src="img/journal-article.jpg" alt="Cover of the Journal of the Royal Society of Antiquaries of Ireland" loading="lazy"><figcaption>Journal of the Royal Society of Antiquaries of Ireland, 1927</figcaption></figure>
</div>'''
write("sources.html", shell("sources", f"Sources · {SITE}", "Maps, reports and articles about the River Poddle.", src, "sources.html"))

# Media
MEDIA = [
 ("Video", "Dublin’s Hidden Rivers", "A short film on the Poddle and the city’s other buried rivers.", "https://www.youtube.com/watch?v=K5ygnHSLKLY"),
 ("Video", "River Poddle in Dublin’s city centre, previously unseen", "Footage from inside the culverted river in the city centre.", "https://www.youtube.com/watch?v=SLwzXheosOI"),
 ("Video", "Poddle River bursts its banks in Kimmage", "The Irish Times, on the flooding that led to the flood alleviation scheme.", "https://www.youtube.com/watch?v=Bc7xLfytphQ"),
 ("Video", "Tymon Park’s esker", "The Echo, on the glacial ridge beside Tymon Castle.", "https://youtu.be/-oMSnnBhdbI"),
 ("Video", "Kimmage Manor from the air", "Drone footage of the manor where the river is piped under the buildings.", "https://youtu.be/e3bgOMpW9Z4"),
 ("Video", "Medieval Dublin Online: Wood Quay", "How the Viking and medieval town grew beside the Poddle and the Liffey.", "https://vimeo.com/147322671"),
 ("Television", "The Liffey, episode 1: Protection and Defence (RTÉ, 2022)", "Dublin City Council’s David Green takes the cameras underground on the Poddle.", "https://presspack.rte.ie/2022/05/15/the-liffey-brand-new-series"),
 ("Article", "Underground Dublin: a pilgrimage through an ancient tunnel network", "Patrick Freyne in The Irish Times, 2021, walking the Poddle beneath the city.", "https://www.irishtimes.com/culture/heritage/underground-dublin-a-pilgrimage-through-an-ancient-tunnel-network-1.4662108"),
 ("Article", "The Ship Street archaeological dig", "RTÉ News, June 2020, on the ravine found south of Dublin Castle.", "https://www.rte.ie/news/dublin/2020/0609/1146385-archaeological-dig/"),
 ("Photographs", "Hidden Dublin: the River Poddle", "A photo series following the river, including the grating at its outfall.", "https://hidden-dublin.com/poddle/poddle_confluence_liffey.html"),
 ("Writing", "Undercurrents, by Amanda Bell", "Haiku and prose on Irish rivers, with a section on the Poddle.", "https://www.littletoller.co.uk/?p=12682"),
]
med = '<div class="wrap page"><header class="page-head"><p class="kicker">Media</p><h1>Watch, read and listen</h1><p class="dek">Films, television and writing about the Poddle. Links open on other sites.</p></header><ol class="media-list">'
med += "".join(f'<li><a href="{u}" rel="noopener"><span class="mtype">{esc(k)}</span><strong>{esc(t)}</strong><span>{esc(d)}</span></a></li>' for k, t, d, u in MEDIA)
med += '</ol></div>'
write("media.html", shell("media", f"Media · {SITE}", "Films, television and writing about the River Poddle.", med, "media.html"))

# About
about = f'''<div class="wrap page narrow"><header class="page-head"><p class="kicker">About</p><h1>About this site</h1>
<p class="dek">A personal project tracing the Poddle from Tallaght to the Liffey.</p></header>
<section><p>Ironically, the CFRAM Poddle options report of the 2000s examined an option for flood relief: “A suitable diversion route has been identified from the Poddle to the Dodder along Tymon Park running south of the M50.” Eight centuries after the monks turned the Dodder into the Poddle, the engineers proposed sending it back.</p></section>
</div>'''
write("about.html", shell("about", f"About · {SITE}", "About The Poddle site.", about, "about.html"))
exec(open(os.path.join(OUT, "build_extra.py"), encoding="utf-8").read())
print("built", len(STOPS) + len(HISTORY) + 4, "pages")
