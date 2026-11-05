"""Builds the Poddle site: one HTML file per page, sharing site.css.
index.html is written without <html>/<head> wrappers (the Artifact host adds them);
every other page is a full document so it also works on plain static hosting."""
import re, html, os, hashlib, json
def _v(*names):
    h = hashlib.md5()
    for n in names:
        h.update(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), n), "rb").read())
    return h.hexdigest()[:8]
ASSET_V = _v("site.css", "map.js", "levels.js", "quotes.js", "planmap.js", "nav.js", "maps.js", "gallery.js", "mapsafe.js", "flow.js", "walkmap.js")

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "The River Poddle, Dublin"   # title suffix
BASE = "https://poddle.ie/"
OG_DEFAULT = "img/og-poddle.jpg"   # 1200x630 social preview card
# Search engine verification codes: paste the content="..." value Mark gets from
# Google Search Console / Bing Webmaster Tools; empty adds no tag.
GOOGLE_VERIFY = ""
GOATCOUNTER = "poddle"  # cookieless visitor counter: https://poddle.goatcounter.com
BING_VERIFY = ""
SOCIAL = [("Facebook", "https://www.facebook.com/thepoddle"), ("Instagram", "https://www.instagram.com/poddle.ie/")]
SITEMAP = []   # slugs that go into sitemap.xml, filled by shell()
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
    "Bancroft Park, a northern extension of Tymon Park, is the first publicly accessible section of the Poddle. Upstream of here, the channel runs through the grounds of Technological University Dublin."]),
   ("Nearby: Talbot’s Leap", [
    "A short walk away, just off Tallaght’s main street by the old walls of St Mary’s Dominican Priory, a plaque put up by Tallaght Community Council in 2022 marks a spot called Talbot’s Leap. It is a reminder that water shaped Tallaght village too.",
    "In the 1600s, the plaque says, a drawbridge stood here over a stream that carried water to the Archbishop of Dublin’s bathhouse. The archbishops had a castle and later a palace at Tallaght; the priory now stands on its site and keeps its old tower. The stream now runs through Sean Walsh Park, but its old stone channel can still be seen running under the priory wall, and the site of the bathhouse is to the front left of the Dominican church.",
    "The story goes back to the Cromwellian wars. The Talbots of Belgard Castle, a branch of the great Norman family that also held Malahide, were Catholic royalists who fought against Cromwell; Belgard was ruined in the war and John Talbot followed Charles II into exile. Around 1651, the plaque says, Cromwell’s soldiers raided and plundered Belgard. Talbot gathered his best men, chased them and caught up with them at Tallaght, but the Ironsides were too strong. Retreating, he found the drawbridge raised, and he and his men jumped their horses across the watercourse to escape. William Handcock, writing in the 1870s, tells the same tradition and places the leap “where the little stream now crosses the road, as you go up to the church”.",
    "This is local tradition, not recorded history. Cromwell himself is not known to have come to Tallaght, though his soldiers certainly did: in 1651 a Captain Alland was quartered there, stripped the roof, timber and pews from St Maelruain’s church for his own buildings, and, so the story goes, fed his horses from the church’s stone font. The parish was paid £100 in compensation in 1662.",
    "The Talbots survived the Commonwealth. After the Restoration John Talbot recovered at least part of the Belgard estate and rebuilt the castle. He fought for James II at the Boyne, Aughrim and Limerick, was covered by the Articles of Limerick, and retired to Belgard. He had no son, and through his daughter Catherine’s marriage the house passed to the Dillons. Colonel John Talbot of Belgard is buried in St Maelruain’s churchyard; accounts differ on whether he was a captain or a colonel, and on the year he died."])],
  images=[("bancroft-s-castle", "Bancroft’s Castle (in ruins) on an early Ordnance Survey map"), ("bancroft-park-sdcc-dee-plan-2004", "Bancroft Park, South Dublin County Council plan, 2004"), ("talbots-leap-plaque", "The Talbot’s Leap plaque, Tallaght Community Council, 2022. Photo shared on Reddit (r/Dublin)."), ("talbots-leap-wall", "The plaque on the old priory wall, Tallaght. Photo shared on Reddit (r/Dublin)."), ("talbots-leap-watercourse", "The old stone watercourse running under the priory wall. Photo shared on Reddit (r/Dublin).")],
  links=[("William Handcock, The History and Antiquities of Tallaght: the church of Tallaght and Talbot’s Leap", "https://www.chaptersofdublin.ie/Handcock/tallaght3.htm"), ("South Dublin County Council: history of Tallaght (Captain Alland, 1651)", "https://sdcc.ie/en/services/planning-building-control/local-area-plans/tallaght-current/development-background/history-of-tallaght.pdf"), ("Library Ireland: the Talbots of Belgard", "https://libraryireland.com/Pedigrees2/talbot.php")]),
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
  gallery=[("tymon-flow-control", "The new flow-control structure at the eastern end of the Limekiln lake, part of the River Poddle Flood Alleviation Scheme."), ("tymon-beech-wood", "The Poddle running through the beech wood in Tymon Park."), ("tymon-weir", "A small weir on the Poddle in Tymon Park."), ("tymon-twin-culverts", "A twin-arched culvert on the Poddle in Tymon Park, just west of the M50."), ("tymon-wetland-boardwalk", "The integrated constructed wetland in Tymon Park, which helps clean the water, with its boardwalk.")],
  gallery_credit="Photos: poddle.ie, November 2026.",
  links=[("Wildlife of the Poddle: otters, bats and the birds of the Tymon lakes", "wildlife.html"), ("Video: Tymon Park’s esker (The Echo)", "https://youtu.be/-oMSnnBhdbI"), ("Tymon Park impoundment area becomes operational (Poddle FAS)", "https://www.poddlefas.ie/news/tymon-park-impoundment-area-becomes-operational")]),
 dict(slug="balrothery-weir", name="Balrothery Weir", place="Firhouse, on the Dodder",
  teaser="Where medieval engineers turned the Dodder towards the city.",
  sections=[("The City Weir", [
    "Balrothery Weir, also called Firhouse Weir, the City Weir or the Great Weir, sits on the Dodder in the Dodder Valley Park, close to where the M50 crosses the river. For more than 500 years it mattered to every citizen of Dublin, because most of the water they drank came over it.",
    "Here the Dodder was turned out of its own bed and sent north-east in a man-made channel, the first stretch of the City Watercourse. About three kilometres on, that channel met the stream coming down from Tallaght, and from that meeting the river is the Poddle proper. Everything downstream, the Tongue, the mills of Kimmage and Harold’s Cross, the cisterns at James’s Street and the moat of Dublin Castle, depended on this weir.",
    "The names are argued over. Firhouse is the village on the south bank and Balrothery the townland on the north bank, where the watercourse began. Older writers also spell it Balruddery. In 2021 a South Dublin County Council motion to rename it officially as Firhouse Weir was voted down, and the Record of Protected Structures lists it as “City Watercourse, Firhouse”."]),
   ("Why the Dodder?", [
    "The Poddle is a small river with a small catchment, and in a dry summer it carried very little. By the early 13th century it had to supply St Thomas’s Abbey, the tenants of the cathedrals and a fast-growing Norman city, and it could not.",
    "The Dodder was the obvious answer. It rises on Kippure, in the Wicklow Mountains, and runs about 29 kilometres to Ringsend, fast and well fed by mountain rain. At Firhouse it passes within three kilometres of the Poddle, and on higher ground, so water taken off here could run downhill all the way to the city."]),
   ("Who built it, and when", [
    "The usual story is that the canons of St Thomas’s Abbey built the weir before 1244, to feed their mills and their own water supply, and that the citizens enlarged it in 1244. The sources do not agree on the dates, and we give them here side by side.",
    "The firmest date is a writ of 29 April 1244. The justiciar, Maurice Fitzgerald, ordered the sheriff of Dublin to hold an inquiry “by twelve free and lawful men” into “whence water can be best and most conveniently taken from its course and conducted to the King’s city of Dublin”, at the citizens’ cost, and to report any damage it might do. The Dodder weir was chosen, and enlarged and repaired. In 1245 the King told John FitzGeffrey to finish his hall in Dublin Castle and to have water piped to it by the summer of 1246, which suggests the works were done by then.",
    "Other writers give other dates. H. F. Berry (1891) puts the watercourse in the middle of the 13th century and wrote about an inquisition of 1258, which recent reports date to 1259, recording an agreement between the monks and the citizens. Rev. Myles Ronan (1927) says the watercourse was formed between 1245 and 1254. B. Mac Giolla Phádraig (1954) dates the weir to 1254. Simpson (1997), as summarised in the flood scheme’s heritage report, reads the evidence the other way: the monks had already diverted the Dodder at Firhouse, the 1244 works were the second branch at Harold’s Cross, and the weir could date from as early as the late 12th century."]),
   ("How it works", [
    "A weir is a low wall across a river that raises the water behind it. At Firhouse the wall runs diagonally across the Dodder, which makes it longer and lets it hold up a wide, calm pool. On the north bank, at the head of that pool, a set of sluice gates opened into the City Watercourse. Raise the gates and water ran off into the channel; close them and the river carried on over the weir.",
    "In normal weather nearly the whole river was turned into the watercourse. Writing in the 1870s, William Handcock said that except in floods “the whole river” went that way, and only the flood water went on down the old bed. Ronan reckoned that the city took an average of about 613,200 gallons a day, roughly 2.8 million litres, and that the Abbey mills took twice that.",
    "From the sluices the channel ran across the fields, under the Tallaght road, past the old churchyard at Templeogue and through the grounds of Templeogue House, joining the Tallaght stream about a quarter of a mile north of Mount Down, near Whitehall. Mills crowded along it. In 1844 Robert Mallet counted 24 mills at work on the Dodder, 12 of them on the City Watercourse."]),
   ("Guarding the water", [
    "A supply this long, running through private land, was easy to tamper with. The city appointed keepers for the stretch from the Dodder to the Tongue, usually a yeoman living near Tallaght or Templeogue: John Pylle of Templeogue in 1456 and a Walsh in 1491. Millers and landowners still cut holes in the banks to take more than their share.",
    "Sometimes the water was cut off on purpose. Rebels following Silken Thomas broke the supply in 1534. The Talbots of Templeogue, through whose land it ran, blocked it in a quarrel with the mill owners; Weston St John Joyce dates this to 1573 and again 1689, other accounts to 1597. In the wars of the 1640s royalist forces are said to have cut it to leave the Cromwellian garrison in Dublin short of water and milling.",
    "The most famous threat is a story about the Hellfire Club. In August 1738 Henry Barry, Lord Santry, ran a tavern porter, Laughlin Murphy, through with his sword in Palmerstown. He was tried by his fellow peers in 1739 and sentenced to death. His uncle, Sir Compton Domvile of Templeogue House, is said to have let it be known that he would turn off the city’s water where it crossed his land. Santry was reprieved and given a full pardon in 1740, and died in England in 1751. The threat is told by many writers but is best treated as legend; Joyce even says the authorities helped Santry escape, which does not match the record of the pardon.",
    "<p>By 1718 the water arriving in the city was badly fouled, and an inquiry traced the pollution to a paper mill and a tuck mill. The result was the <a href=\"1719-act.html\">1719 Act</a> “for cleansing and repairing the watercourse from the River Dodder to the City of Dublin”, which gave the Corporation much stronger powers over the whole channel.</p>"]),
   ("Rebuilt over the centuries", [
    "What you see today is not medieval. In 1308 the mayor, John Le Decer, had the watercourse cleaned and its banks faced with stone, though it is not recorded whether he worked on the weir itself. The National Inventory of Architectural Heritage dates the present weir to about 1775, and says it is about 80 metres long and drops in three main stages from the weir pool to the river, with a group of sluice gates at the weir and nearby. Later accounts describe a final modernisation of the weir and sluices in the early 19th century, and an archaeologist in 2001 judged it largely remodelled in Victorian times.",
    "That 2001 work, monitoring the removal of gravel above the weir for flood relief and the linear park, found masonry walls along the south bank and eight hollowed-out tree trunks in the riverbed. They were probably water pipes, like the 18th-century wooden pipes found under Dublin’s streets. Nothing older was found, and the report notes that the weir was quarried for river gravel until the 19th century."]),
   ("Crossing the weir", [
    "Before the river was straightened and deepened in the 1840s you could drive across just below the weir. Afterwards the banks stood about 20 feet high, and the only way over in a flood was to wade along the top of the weir, which Handcock called dangerous. A wooden footbridge paid for by local subscription was swept away in a flood, and its planks were said to have floated down to Ringsend.",
    "An iron lattice bridge followed around 1860, 20 feet above the riverbed. The present bridge was opened by South Dublin County Council in 1995."]),
   ("The end of the watercourse", [
    "The weir’s job faded slowly. The Grand Canal began to supply the city basin in the 18th century; the flood scheme’s heritage report gives 1755, and Berry, quoted by Handcock, says the city relied on the Dodder until 1775. In the 19th century the Vartry and Bohernabreena reservoirs took over the drinking supply, and the watercourse was kept for mills and industry. Even in 1939 J. Hegarty could describe “the weir, the watercourse, the Tongue” as still in place and still doing some of their old work.",
    "In the middle of the 20th century parts of the channel were piped. In the 1970s new housing at Templeogue and Firhouse cut through its line, and newspaper letters at the time warned that bad planning would bury it. The link from the Dodder to the Poddle was then allowed to dry out. Today only a short stub of channel leaves the weir and ends within about 100 metres."]),
   ("Visiting today", [
    "The weir is in the Dodder Valley Park, between Firhouse and Balrothery, beside the M50 bridge over the Dodder. You can walk to it along the riverside path from Old Bawn or from Firhouse, both of which have parking. Stand on the 1995 footbridge for the best view of the falls, then look to the north bank for the old sluices and the start of the dry channel.",
    "It is a protected structure, and the National Inventory rates it of regional importance for its archaeological, architectural and technical interest. From the weir, a path under the M50 takes you into Tymon Park and on to the Poddle itself.",
    "The Dodder rises fast after heavy rain. Keep to the paths and the bridge, and do not try to cross on the weir."])],
  images=[("firhouse-weir-2021", "Firhouse Weir stepping down across the Dodder, January 2021. Photo: Tdr112, Wikimedia Commons, CC BY-SA 4.0."), ("firhouse-footbridge", "The footbridge over the Dodder at Firhouse, near the M50, 2012. Photo: Deitel55, Wikimedia Commons, CC BY-SA 3.0."), ("duncan-1821-city-weir", "“City Wear” on the Dodder, south of Templeogue, on Duncan’s map of the County of Dublin, 1821. Figure 11-6, EIAR Chapter 11, River Poddle Flood Alleviation Scheme (An Bord Pleanála case 306725)."), ("ronan-1927-map-ii", "The Dodder, the Poddle and the City Water, with the weir marked “Head” (B) and the Tongue (E). Map II from Rev. Myles V. Ronan, “The Poddle River and its Branches”, Journal of the Royal Society of Antiquaries of Ireland, 1927."), ("roque-1760-tymon", "The City Watercourse leaving the Dodder at Templeogue, on Rocque’s map of County Dublin, 1760. Figure 11-3, EIAR Chapter 11, River Poddle Flood Alleviation Scheme."), ("diversion-map", "The route of the diversion from the Dodder to the Poddle")],
  links=[("National Inventory of Architectural Heritage: Firhouse Weir (reg. no. 11215019)", "https://www.buildingsofireland.ie/buildings-search/building/11215019/firhouse-weir-south-dublin-county"), ("Excavations.ie: The Weir, Firhouse, 2001", "https://excavations.ie/report/2001/Dublin/0006358/"), ("Weston St John Joyce, The Neighbourhood of Dublin: the old city water supply", "https://www.chaptersofdublin.ie/Neighbourhood/chapter43.html"), ("William Handcock, The History and Antiquities of Tallaght: the River Dodder", "https://www.chaptersofdublin.ie/Handcock/tallaght17.htm"), ("Crumlin Walkinstown History: Balrothery (Firhouse) Weir, with newspaper articles", "https://poddle.crumlinwalkinstownhistory.ie/location/firhouse-weir/"), ("Our Irish Heritage: Balrothery Weir, with photographs by Tallaght Community Council", "https://www.ouririshheritage.org/content/archive/place/miscellaneous-place/balrothery-weir-on-the-dodder-part-of-tallaght-waterways-history"), ("South Dublin County Council: Firhouse Weir", "https://www.sdcc.ie/en/services/tourism/activities/sightseeing/firhouse-weir/")]),
 dict(slug="m50-crossing", name="M50 Crossing", place="Tymon Park",
  teaser="Where the motorway sent the river underground.",
  sections=[("The M50", [
    "The M50 was planned in the 1970s, and building began in the 1980s with this section, from the N7 to the N81, first built as a single-carriageway road.",
    "The state’s purchase of the Tymon estate for the park was probably either a result of the road scheme or part of the same plan. The Poddle was presumably culverted at this point to carry it under the future motorway."]),
   ("Western Parkway", [
    "In 1990 the N3 to N81 section of the M50 opened, including the West Link bridge across the Liffey Valley, and this stretch was upgraded from single carriageway to motorway."])],
  images=[("m50-crossing", "The M50 crossing the line of the Poddle"), ("m50-crossing-upgrade", "Plan of the M50 crossing upgrade"), ("m50-from-footbridge", "The M50 from the footbridge in Tymon Park. Photo: poddle.ie, November 2026."), ("m50-culvert", "The culvert that carries the Poddle under the M50, Tymon Park. Photo: poddle.ie, November 2026.")]),
 dict(slug="dodder-overflow", name="Dodder Overflow", place="Lakelands, Terenure",
  teaser="A sluice that sends flood water back to the Dodder.",
  sections=[("Diversion", [
    "Upstream of Kimmage Manor, where the Poddle begins its first long run in culverts, the river divides twice. This is the first. Unlike the second, it sends high water out of the Poddle and into the Dodder catchment, by way of storage ponds in Terenure."]),
   ("Overflow to Terenure", [
    "A sluice gate limits how much water carries on towards Kimmage and Kimmage Road Lower. The overflow runs through culverts to the ponds at Terenure College, which drain back to the Dodder at Bushy Park.",
    "An old record of the City Watercourse says a stream taken off it in Terenure fed three fishponds, so the idea of ponds there is an old one. You can follow the overflow on the map page, where it is drawn as a green dashed line from the sluice at Whitehall Park to Bushy Park. The line is schematic, since the culverts are underground.",
    "This is the downstream end of the flow controls and channel works in the River Poddle Flood Alleviation Scheme. The scheme followed serious floods in Harold’s Cross and Kimmage in 1987, 1990, 1993 and 2011. It was approved by An Bord Pleanála in June 2023, the Office of Public Works began building it in April 2024, and it is due to be finished in 2027."]),
   ("Refined and defined", [
    "Along this stretch, the scheme proposes to tidy and define the channel and build walls on both sides.",
    "Flows through the Poddle in earlier centuries must have been large, without the ponds at Tymon or these control structures, and with water diverted in from the Dodder at Balrothery as well."])],
  images=[("dodder-overflow", "Route of the Lakelands overflow to the Dodder"), ("dodder-overflow-image", "The overflow channel"), ("dodder-overflow-fas-scheme", "Proposed works, Poddle Flood Alleviation Scheme"), ("whitehall-channel", "The Poddle in its open channel near Whitehall. Photo: poddle.ie, November 2026.")],
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
    "Past the Stone Boat, most of the Poddle’s flow enters the grounds of Mount Argus. Here modern flood-control features sit in parkland, and this is the last easily reached stretch of the river before its long run underground begins. Dublin Corporation’s minutes for 1979 record the river at Mount Argus being included in an amenity improvement scheme."]),
   ("Mount Argus", [
    "Mount Argus, in Harold’s Cross, was the first Passionist monastery in Ireland, founded in 1856. The present church was built between 1873 and 1878 and dedicated to St Paul of the Cross in 1878."]),
   ("Mills at Mount Argus", [
    "In the monastery grounds the Poddle once fed a pond and a millrace. Harold’s Cross was then a small mill village: a paper mill worked at Mount Argus in the 19th century, and Loader’s Park Mills, a corn mill on Kimmage Road Lower, stood where the Waterwheel apartments are now. On Mount Argus Road a former flour mill later became a laundry, and is now apartments. The old Mount Argus mill, long disused, was taken over in the 20th century by the 45th Mount Argus Scout Troop as a boxing club."]),
   ("Saint Charles", [
    "Charles Houben arrived at the newly founded monastery on 9 July 1857. Known for his gift of healing, he drew as many as 300 people a day to Mount Argus to be blessed.",
    "He died there on 5 January 1893, aged 71. Hundreds of cures were credited to him in his lifetime and after. He was beatified by Pope John Paul II in 1988 and canonised by Pope Benedict XVI on 3 June 2007. In 1949 his remains were moved into the church, where they can still be visited."])],
  images=[("mount-argus-waterfall", "The Poddle at Mount Argus"), ("mount-argus-in-snow", "Mount Argus church in snow"), ("saint-charles", "Saint Charles of Mount Argus")]),
 dict(slug="mount-jerome", name="Mount Jerome", place="Harold’s Cross",
  teaser="A Victorian cemetery, perhaps another monks’ diversion, and a siphon under the canal.",
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
    "The stream enters the cemetery behind the Russian Orthodox Church of the Holy Apostles Peter and Paul, flows under the cemetery’s entrance road and then along its eastern boundary. From here it is culverted under Greenmount, and it passes beneath the Grand Canal in a siphon. Dublin Corporation’s minutes for 1972 record a £35,000 loan for culverting the river between Greenmount Lane and the Grand Canal."]),
   ("Under the Grand Canal", [
    "Just past Greenmount the river meets the Grand Canal, close to Robert Emmet Bridge, which most people call Harold’s Cross Bridge. The canal was dug straight across the Poddle’s path in the 1790s, and ever since then the river has had to find a way underneath it. Weston St John Joyce, writing in 1912, describes it going “under the canal at Goodbody’s factory”.",
    "It does it with a siphon: a pipe that dips down below the canal bed and comes up again on the far side. In 2003 archaeologists watching groundworks at 25 Parnell Road, beside the canal, looked down a manhole and found a fast-flowing watercourse at least five metres below the surface. They took it to be the culverted Poddle, running deep enough to pass beneath the canal.",
    '<figure class="fig diagram"><img src="img/siphon.svg" alt="Cross-section of the siphon. The river arrives in its culvert, drops below the canal bed, runs along a pipe that stays full of water, and rises on the city side a little lower than it came in. In floods, extra water spills into the drainage tunnel." width="720" height="380" loading="lazy"><figcaption>How the siphon works. A simplified drawing, not to scale.</figcaption></figure>']),
   ("How a siphon works", [
    "Water always tries to find its own level. If a pipe dips down and comes back up again, and its far end is a little lower than its near end, the pipe fills right up and stays full. Every bit of water that flows in at the top pushes the same amount out at the other end, so the river keeps moving without any pump at all.",
    "Engineers call this an inverted siphon, because it dips down under an obstacle instead of going up and over it, like the tube used to empty a fish tank. It has two drawbacks. Silt and rubbish settle at the lowest point and have to be cleared, and fish can’t easily get through. The flood scheme’s ecologists name the siphon as one of the barriers that keep trout and eels out of the Poddle."]),
   ("The siphon today", [
    "The structure there now is described as late 20th century. Around the time of the 1972 culverting, Dublin Corporation was also digging the Grand Canal Tunnel, a sewer 4.8 km long and 3.6 metres across that runs beside the canal towards Ringsend. One of its jobs, according to Dublin City Council, is to take storm water from the Poddle and the Swan River and so cut the risk of flooding. At the canal the Poddle has an overflow into this drainage pipe, so in a flood some of its water can escape there instead of backing up into Harold’s Cross. RTÉ reported in July 1975 that the tunnel had taken two and a half years to build and cost £4 million.",
    "The City Watercourse had a crossing of its own, just east of Dolphin’s Barn Bridge. A newspaper report of a flood in March 1937 says that the stream then ran underground for 400 yards from above Rutland Cottages and emptied into the canal near the bridge. Today the Grand Canal Tunnel intercepts it there.",
    "<p>We still don’t know how the Grand Canal Company carried the river across when the canal was first dug in the 1790s, or who did the work. If you know of a drawing, a record or a memory of it, please <a href=\"about.html#contact\">get in touch</a>.</p>"])],
  links=[("Excavations.ie: 25 Parnell Road, Harold’s Cross (2003)", "https://excavations.ie/report/2003/Dublin/0033528/"), ("Dublin City Council: Grand Canal storm water outfall, EIA screening report (2020)", "https://www.dublincity.ie/sites/default/files/2022-06/appendix-1a_eia-screening-report.pdf"), ("RTÉ Archives: Dublin drainage tunnel (1975)", "https://www.rte.ie/archives/2020/0619/1148461-dublin-drainage-tunnel"), ("Karl Whitney, The Irish Times: Down Dublin’s drains (2014)", "https://www.irishtimes.com/life-and-style/down-dublin-s-drains-1.1918103"), ("Weston St John Joyce, The Neighbourhood of Dublin: the old city water supply", "https://www.chaptersofdublin.ie/Neighbourhood/chapter43.html")],
  images=[("mount-jerome-image", "The Poddle at Mount Jerome"), ("mount-jerome-diversion", "The possible diversion at Mount Jerome"), ("mount-jerome-map", "Map of Mount Jerome Cemetery")]),
 dict(slug="st-patricks", name="St Patrick’s Cathedral", place="Blackpitts and the Liberties",
  teaser="Built between two streams, and flooded by them for centuries.",
  sections=[("Through the Liberties", [
    "North of the Grand Canal, the culverted river runs along Clanbrassil Street, past Donore Avenue, Warrenmount and Blackpitts. Blackpitts, a name on maps by 1728, probably comes from the pits used by tanners along the river, and Mill Street, first mentioned in 1711, recalls a double mill for oil and flour that is linked to St Thomas’s Abbey. In 1830 the street had several tanners and a fancy weaver; by 1880 it had five tanners and a parchment maker. During a great fire on 22 June 1875, burning whiskey ran into the Poddle beneath Ardee Street and set the river alight. One account of the area, on the Hidden Dublin website, describes a man-made side channel at Blackpitts that came from the direction of Ardee Street, turned east along Sweeney’s Lane and then north to join the main river; it was photographed in 2007, on a site then about to be built over. Faddle Alley, a lane off Blackpitts, is where the blind street rhymer Michael Moran, known as Zozimus, was born in about 1794. He died in lodgings on Patrick Street, also on the river’s course, in 1846.",
    " Near New Row it picks up its ancient course again, and at the junction of New Street, Patrick Street and Kevin Street, the old Cross Poddle (renamed Dean Street by the Wide Streets Commissioners in 1826), a medieval mill stood on its bank beside St Nicholas’ Bridge, outside St Nicholas’ Gate. At Fumbally Lane it is joined by the Tenter Water, a branch of the City Watercourse, and at the corner of the Coombe and Patrick Street by its one real tributary, the Commons Water, which rises in Crumlin."]),
   ("The Blackpitts tanners", [
    "Cross Poddle was much older than its mill. In the Middle Ages it was the lowest point at which the Poddle could be forded, so several important roads met there, with a gate outside the city walls and a market. The area may already have been settled before the Normans came, with several early churches and possibly an Irish suburb of the Norse town.",
    "Just upstream, the river gave Blackpitts its trade. In 2004 archaeologists excavating at 48 New Street South found more than a hundred tanning pits, dating from the late 13th century to the 17th. The archaeologist Antoine Giacometti argues that this was not one big tannery but a quarter of small household tanyards, worked behind the houses on New Street. Tanners needed a steady supply of water to soak and rinse hides, and late medieval records show ditches being dug off the Poddle to serve the tanneries. From the 15th century, laws often ordered those ditches filled in, because the Poddle kept flooding and the tanners were fouling the water.",
    "The site ran along the top of a steep slope down into the Poddle valley. A ditch dug along it in the 13th or 14th century ran into or out of the river near a medieval millpond, which was excavated just north-west of the site. The millpond was dug in the 13th or 14th century and filled in during the 14th or 15th, the same dates as the ditch, which may have been its tail race or overflow. Giacometti suggests both were part of the great programme of works in the mid-13th century, when the river was diverted round the Liberties and mills and water channels were set along its old and new courses, marking the edges of the church lands. Disputes over those mills and watercourses fill the medieval records.",
    '<div class="fig-grid"><figure class="fig"><a href="img/blackpitts-tanning-pits.jpg"><img src="img/blackpitts-tanning-pits.jpg" alt="Rows of tanning pits uncovered during an archaeological excavation at Blackpitts. Photo courtesy of Reddit user Few_shine2208." loading="lazy"></a><figcaption>Rows of tanning pits uncovered during an archaeological excavation at Blackpitts. Photo courtesy of Reddit user Few_shine2208. <a href="img/blackpitts-tanning-pits.jpg">Open full size</a></figcaption></figure></div>']),
   ("Donore Avenue, 1901", [
    "Donore Avenue was once Love Lane, and the Poddle ran open beside it. Dublin Corporation’s printed reports for 1901 (Report No. 129 of the Paving Committee, pages 301 to 316) tell the story of how it came to be covered.",
    "In 1894 an architect, Robert Stirling, laid out new roads on the Huband estate off the South Circular Road, reached through Love Lane. The Borough Surveyor, Spencer Harty, agreed to narrower roads on condition that a stretch of the Poddle he marked “A” was covered over: “this will be a great improvement.” The Corporation approved this in 1896, but the new road was never built, so the river was never covered.",
    "By 1900 the residents had had enough. A petition forwarded by the Rev. Fergus Greer, rector of St Catherine’s, and signed by the Greenmount Spinning Company and “a great many others” pointed out “the great danger and nuisance the Poddle River is to the public, when it is exposed to the open, adjoining the street, now known as Donore Avenue, formerly Love Lane.” The lane was “only 10 feet wide alongside the river”, wide enough for one vehicle at a time, and there was “the added danger to children from the narrow thoroughfare and the open river, especially now when it is contemplated building a parish school alongside the river.”",
    "Harty reported that covering about 320 feet of the river would give a road 25 feet wide with two 6-foot footpaths, for about £1,850. The Huband estate’s new agent refused to pay for its share, and the Law Agent advised that if the river was to be covered, the Corporation was the proper authority to do it. On 31 July 1901 the Paving Committee agreed the work “would be an improvement”, but “considering the pressing demand on the funds of the Corporation at this present time”, it would not recommend spending £1,850. The Corporation’s index shows a loan of £1,850 for covering the Poddle at Donore Avenue the following year, so the work went ahead in 1902.",
    "Today, according to " + "McEntee and Corcoran" + ", the old course is blocked off outside Donore Avenue church and a newer culvert carries the flow along Donore Avenue, rejoining the old route between Ebenezer Terrace and Harman Street before it reaches the old mill pond at Warrenmount."]),
   ("Between two streams", [
    "Near Patrick Street the Poddle once ran in two channels, one on each side of the street, joining again near Bride’s Alley before turning east towards the Castle. The first church of St Patrick stood on the island of dry ground between them, which is why the Normans called it St Patrick’s “in insula”, on the island. It was a holy site and a very wet one.",
    "Tradition says that St Patrick baptised converts at a well here in the fifth century. The first record of a church on the site is from 890. The cathedral’s own account says that in 1901, during building works beside it, six carved grave slabs were found, and one of them was lying over what looked like an old well; other accounts date the find to the middle of the 19th century. The carving is dated to around the tenth century. The cathedral describes this as possibly, not certainly, the well of the story. The stone is now kept inside the cathedral, and a plaque in the park marks the reputed site of the well.",
    "The architect Sir Thomas Drew left a more exact note, quoted by Ronan in 1927. On 16 June 1901, he wrote, the site of the well was found “in course of opening up the old arched course of the Poddle on the east side of Patrick Street by Spencer Harty, City Surveyor, to build a new tunnel (with concrete)”. It was marked by “an ancient granite stone marked with two crosses in high, clear relief”, built into the side of the old culvert, and the stone was taken into the cathedral on 19 June 1901. Drew and Harty thought the well itself had been lost when the river was diverted, probably under Charles II, into a great stone culvert along the cathedral’s west front to drive a corn mill there, the mill that gave Cross Poddle its name."]),
   ("A cathedral on wet ground", [
    "John Comyn, the first Norman archbishop of Dublin, made the little church collegiate in 1191, with a body of clergy for worship and learning, and dedicated it on 17 March that year. His successor, Henry de Loundres, raised it to a cathedral; most accounts date this to about 1212 or 1213, and in 1220 he created the office of dean. The great stone church we see was built in the following decades, between about 1220 and 1270 by most counts, with the Lady Chapel added around 1270.",
    "Building on an island in a river had a lasting cost. In the 20th century the water table was found to be within about 2.3 metres (seven and a half feet) of the floor, which is why the cathedral has never had a crypt, unlike Christ Church a few hundred metres away on its ridge above the Liffey."]),
   ("Boats in the nave", [
    "The cathedral flooded again and again. There was an inquiry into blockages near it as early as 1437, and Parliament ordered local people to keep the drains clear in 1493 and again in 1664. In 1701 the flooding was so bad that people could row a boat past the cathedral, and in 1744 services had to move to Christ Church. Major floods followed in 1778, 1791 and 1795, and one in the early 19th century left about five feet of water inside the building. Weston St John Joyce noted that the city streams often spilled over the low ground of the Liberties and into the cathedral precincts, doing considerable damage.",
    "Ronan, writing in 1927, says that “on several occasions the water rose in the Cathedral as high as five feet and boats plied in Patrick Street”, and lists Acts of Parliament against the nuisance in 1437, 1493, 1664, 1687, 1701, 1762, 1778, 1796 and 1840. In November 1787 a Dublin newspaper reported that “the inhabitants from the end of New Street to Bride’s Alley were necessitated to keep to the upper apartments.”"]),
   ("Ditches, pipes and culverts", [
    "A Dublin Corporation map reproduced by Rev. Myles Ronan in 1927 shows how the water around the cathedral was gradually tamed. The two arms of the Poddle run along Patrick Street, with St Patrick’s Well marked beside the cathedral. Between the cathedral and Bride Street, the old open ditches between Bull Alley, Bride’s Alley and Ross Lane are marked “ditch piped” and “brick built”, with a brick culvert running across to the river. The canons’ houses and gardens, the Chantor’s Manse, the Treasurer’s House and the Chantor’s Orchard, sat in the middle of this network of drains."]),
   ("Out of sight", [
    "By the 1860s the river had become an open sewer, blamed for disease as well as flooding, and its lower reaches were roofed over. Dublin Corporation’s minutes show the work going on in the Liberties at the start of the 20th century: the Donore Avenue covering above, then loans in 1902 and 1903 for covering, repairing and underpinning it. Under Charles II a Poddle Commission had been set up to manage it, with power to levy a Poddle tax; its powers passed in 1840 to the Paving Commissioners by one account, and to Dublin Corporation by Ronan’s. Ronan lists the brick culverts that followed: Bride’s Alley in 1868, Bull Alley in 1870, the Close in 1872 and St Patrick’s Place in 1880 to 1882.",
    "Accounts differ on Patrick Street itself. One source says the street got its brick culvert in the 1920s, but Sir Thomas Drew’s note shows the City Surveyor building “a new tunnel (with concrete)” on the east side of the street in June 1901. McEntee and Corcoran add that Patrick Street had a culvert on each side until about 1904, and that the abandoned western one was uncovered and photographed when the road was widened in the 1990s.",
    "The Guinness family changed the area twice. Benjamin Lee Guinness paid for the great restoration of the cathedral in 1860 to 1865, when it was feared the building might collapse. In 1901 his grandson Edward Guinness, Lord Iveagh, cleared the crowded houses to the north and laid out St Patrick’s Park, and it was during that work that the old slab and well were found. Newspapers of 1900 report that the Poddle’s own course was moved to make way for the new Bull Alley and Bride’s Alley buildings. In 1902 the Corporation passed a vote of thanks to Lord Iveagh for a gift of £1,400 towards the work of completing the river opposite St Patrick’s.",
    "The river shaped local life in smaller ways too. The rough ground by the cathedral was policed by the “Poddle Guard”, a party of about twenty soldiers stationed nearby from 1725, and an 18th-century insult for an unruly Liberties crowd was a splash in the Poddle Hole. These details, with the newspaper sources, are gathered by the Crumlin and Walkinstown History Group’s Poddle project."]),
   ("What to see", [
    "Stand in St Patrick’s Park and you are standing roughly on the island between the two old streams. The Poddle still runs beneath Patrick Street, along the west side of the park, in its culvert on the way to the Castle. Inside the cathedral, look for the old well slab, and notice that there are no steps down: the floor is as low as the water will allow."])],
  images=[("st-patricks-from-park", "St Patrick’s Cathedral from St Patrick’s Park, the old island between the two streams, 2015. Photo: Clara.munecas, Wikimedia Commons, CC BY-SA 4.0."), ("st-patricks-1814", "The cathedral in 1814, before the Guinness restoration. Engraving credited to James Whitelaw, public domain, via Wikimedia Commons."), ("st-patricks-lawrence", "St Patrick’s Cathedral after the restoration. Photo: William Lawrence, Lawrence Collection, public domain, via Wikimedia Commons."), ("st-patricks-west-front", "The west front and Minot’s Tower from Patrick Street, under which the Poddle runs, 2012. Photo: Andreas F. Borchert, Wikimedia Commons, CC BY-SA 4.0."), ("st-patricks-nave", "The nave, looking east. There is no crypt below it. Photo: Diliff, Wikimedia Commons, CC BY-SA 3.0."), ("st-patricks-well-stone", "The carved stone found over the old well, now in the cathedral. Photo: Wknight94, Wikimedia Commons, CC BY-SA 3.0."), ("st-patricks-well-plaque", "The plaque in St Patrick’s Park marking the reputed site of the well. Photo: Archaeomoonwalker, Wikimedia Commons, CC0."), ("ronan-1927-map-vi", "The Poddle and its ditch branches around St Patrick’s Cathedral, with St Patrick’s Well beside the cathedral, from a Dublin Corporation map. Map VI from Rev. Myles V. Ronan, “The Poddle River and its Branches”, Journal of the Royal Society of Antiquaries of Ireland, 1927.")],
  links=[("Antoine Giacometti, Blackpitts: Dublin’s medieval tanning quarter (PDF)", "https://static1.squarespace.com/static/61b0b814414fb8020e89e9d1/t/61d6c7289232d563f5e95aab/1641465663128/07+Giacometti.pdf"), ("St Patrick’s Cathedral: Saint Patrick and the cathedral", "https://www.stpatrickscathedral.ie/saint-patrick-and-the-cathedral/"), ("Weston St John Joyce, The Neighbourhood of Dublin: the old city water supply", "https://www.chaptersofdublin.ie/Neighbourhood/chapter43.html"), ("Wikipedia: Zozimus (Michael Moran), citing P. J. McCall, Dublin Historical Record, 1945", "https://en.wikipedia.org/wiki/Zozimus"), ("Arran Henderson: The best Poddle river", "https://arranqhenderson.com/2017/07/18/the-best-poddle-river/"), ("Arran Henderson: the chapel on the island", "https://arranqhenderson.com/2014/01/12/origins-of-saint-patricks-cathedral-part-one-the-chapel-on-the-island-early-celtic-church/"), ("Wikipedia: St Patrick’s Cathedral, Dublin", "https://en.wikipedia.org/wiki/St_Patrick%27s_Cathedral,_Dublin")]),
 dict(slug="ship-street-little", name="Ship Street Little", place="Dublin Castle",
  teaser="A sheep market, and a ravine as deep as any dig in Dublin.",
  sections=[("Sráid na gCaorach", [
    "Ship Street Little and Ship Street Great, which run along the southern walls of Dublin Castle, are named not after ships but after the sheep market once held here. The Irish name, Sráid na gCaorach, means Street of the Sheep.",
    "The Poddle arrives from the west and flows under Ship Street Little and the Ship Street gate of Dublin Castle."]),
   ("Round the hill, not over it", [
    "Walk from St Patrick’s Cathedral to Dublin Castle and the ground rises steeply under your feet, up Patrick Street and Nicholas Street towards Christ Church. So how does a river make the same journey? The answer is that it doesn’t climb at all. It goes round.",
    "The old walled city stands on a ridge of glacial clay and gravel between the Liffey and the Poddle. Boreholes on a site between Ship Street Great and Chancery Lane found glacial till down to about 9 metres, with limestone bedrock beneath. St Patrick’s Cathedral was built below the ridge, on low, wet ground between branches of the river, which is why it has flooded so often. Christ Church was built on top of it.",
    "From the cathedral the Poddle ran north, parallel with Patrick Street, in two or more courses down the west and east sides of the street, as far as Ross Road and the line of the southern city wall. There, at the foot of the ridge, it turned east and ran along the walls and the castle ramparts, past Ship Street, around the Royal Chapel, and out at the Lower Castle Gate at Palace Street and Dame Street on its way to the Liffey. That is the route given in Clair Sweeney’s book The Rivers of Dublin, quoted in the 2018 engineering report for the Ship Street site. Water always takes the lowest line, and the lowest line from the Liberties to the Liffey runs round the eastern tip of the ridge, not over the top.",
    "It is better to think of it the other way round. The Poddle’s valley is what makes the southern and eastern edge of the ridge, and the 2020 dig below shows how deep that valley once was. The Normans built Dublin Castle on the end of the ridge, where the river and the Dubh Linn gave them a ready-made moat. You can still feel the valley today: Ship Street Little sits well below Werburgh Street and Castle Street, and the Forty Steps climb from Ship Street up to the level of the old city.",
    '<figure class="fig diagram"><img src="img/round-the-ridge.svg" alt="Simplified plan, north at the top. The old city stands on a ridge with Christ Church on top and Dublin Castle at its eastern tip. The Poddle comes north from St Patrick’s Cathedral in the low ground, turns east along the foot of the ridge by the old city wall, passes under Ship Street and round the Castle, where it fed the Dubh Linn, and runs north under Palace Street to the Liffey. Walking north up Patrick Street climbs the ridge; the river never does." width="720" height="470" loading="lazy"><figcaption>How the Poddle goes round the ridge. A simplified drawing, not to scale; the river is culverted all the way today.</figcaption></figure>']),
   ("The original channel", [
    "Archaeological excavations in 2020, on a site just south of Ship Street Little and west of Ship Street Great, found that the Poddle here once ran through a ravine that fed into the Dubh Linn.",
    "The ravine was so deep that, at the time of writing, it was the deepest archaeological excavation in the city’s history.",
    "Once the monks of St Thomas’s Abbey had diverted water away, the channel dried up, and the ravine was quarried for stone for the walls of the Norman castle."]),
   ("“An underground river!”", [
    "Sister Ann Dominica Fitzgerald opened her 1973 essay “Down the Old Poddle” with a story from Ship Street. Condemned houses were being knocked down when the bulldozer “suddenly plunged through the surface into a void”, and the men peered down: “Be the hokey! An underground river!” The Corporation engineer who came down the steps at the back of Hoey’s Court had no doubt: “What you have there boys, is the Poddle. What else could it be in Ship Street?” The machine had broken through the arch of the Poddle, buried in the 1800s.",
    "Robert Mallet, the engineer who surveyed the river in 1844, described this last stretch the same way: from Warrenmount the water ran “in covered channels, known in the district by the name of the ‘Poddle Hole’ and passing near St. Patrick’s Cathedral, through Little Ship-street, the Castle-yard, and across Dame-street”, to the Liffey under Wellington Quay."])],
  images=[("ship-street-ravine", "The ravine uncovered at Ship Street"), ("ship-street-dig", "The excavation site, 2020"), ("ship-street-forty-steps", "The Forty Steps, Ship Street")],
  links=[("RTÉ News: the Ship Street archaeological dig, June 2020", "https://www.rte.ie/news/dublin/2020/0609/1146385-archaeological-dig/")]),
 dict(slug="dubh-linn", name="Dubh Linn", place="Dublin Castle gardens",
  teaser="The black pool that gave the city its name.",
  sections=[("Origin", [
    "The Dubh Linn, the black pool, was a pool on the Poddle just before it met the Liffey.",
    "The tidal, salty Liffey was no good for drinking, so the fresh water of the Poddle was the main drinking supply for the settlement that became Dublin.",
    "The pool may have been darkened by peat carried down from the hills. The Vikings who settled beside it called their town Dyfflin, from the Irish dubh linn. The pool itself lay under what are now the coach house and gardens of Dublin Castle."]),
   ("Defence", [
    "As the city grew, the Poddle became a key defence on its southern side. The stream was channelled, and even dammed, to act as a moat. That dam is said to have given Dame Street, which now runs in front of Dublin Castle, its name.",
    "The moat had its weak points. Red Hugh O’Donnell’s escape from the Castle in the winter of 1591 to 1592 is traditionally said to have gone by way of the moat. He did not go alone: two fellow prisoners, Henry and Art O’Neill, sons of Shane O’Neill, got out with him, and the three headed south into the Wicklow mountains in deep snow. Art died of exposure there, and Red Hugh lost both his big toes to frostbite. In 1881 the Freeman’s Journal reported the authorities blocking the Poddle outfall, described as the only underground way into the Castle. In 1961 a tunnel about seven feet high was found under the Upper Yard."]),
   ("Dubh Linn today", [
    "Behind Dublin Castle, the site of the Dubh Linn is kept as a garden, a monument to its importance and the Poddle’s. The Dubh Linn Garden is bordered by the Chester Beatty Library, Dublin Castle and the Poddle, which now runs underground along its southern edge."])],
  images=[("modern-balc-pool", "The Dubh Linn Garden today"), ("medieval-dublin", "Medieval Dublin"), ("schematic-dublin-castle", "The River Poddle at Dublin Castle")]),
 dict(slug="palace-street", name="Palace Street", place="Dame Street",
  teaser="Under the castle gate, Dame Street and the Olympia.",
  sections=[("Bifurcation", [
    "Inside the gates of Dublin Castle the river divides again. McEntee and Corcoran describe it: “Turning northwards opposite the Chapel Royal, the Poddle bifurcates inside the Palace Street Gate, the more westerly branch flowing under the open space beside City Hall before going under Dame Street. The eastern branch flows under Palace Street, beside a bank, which a gang of would-be robbers tried to access from the culvert in the 1980s.” The film Dublin’s Hidden Rivers shows that wall, from about 4:06 in (linked below), and the Media page has more on the 1985 raid.",
    "Rev. Myles Ronan, writing in 1927, gives an older version of the same split: past the Lower Castle Yard the Poddle “anciently divided again into two branches, one going by Exchange Court, Crane Lane, south side of Essex Street, to the bottom of Sycamore Street, where it met the other branch”. Sister Ann Dominica Fitzgerald’s 1973 plan of the river from Warrenmount to the Liffey shows the two channels crossing Dame Street and joining again by Essex Street East."]),
   ("Dame Street", [
    "The river continues north under the Palace Street pedestrian gate of Dublin Castle and on to Dame Street. Dame Street takes its name from the dam on the Poddle, used both for defence and to power a mill."]),
   ("The Olympia", [
    "From the castle gates the stream continues north, under Dame Street and beneath the historic Olympia Theatre. “Flowing under Dame Street and the Olympia Theatre,” McEntee and Corcoran write, “the main Poddle culvert is rejoined in Essex Street by its western or City Hall branch.”"]),
   ("Inside the culvert", [
    "People who have been down in the culverts here describe them differently, and none of this has been checked. One account, from an anonymous visitor shared on the Hidden Dublin website, says a side branch under the Olympia rejoins the main stream after about 100 metres, and that near the Record Tower a separate sewer runs alongside the river, taking its overflow when the water is high. The same account describes a stretch with a cobbled floor, thought to be among the oldest parts of the culvert, and says no sewage goes into the Poddle here and the water runs clear. Treat it as one person’s description, not a survey."]),
   ("Floods at the Castle", [
    "The Castle Yard flooded too. In November 1787 a Dublin newspaper reported that the people of Crampton Court and Palace Street “were put to distressing circumstances by the Poddle stream which breaking through its bounds in Lower Castle Yard inundated the houses of both places”.",
    "In 1814, McEntee and Corcoran record, the river was in spate when a boy working on an arch being built in the Castle Yard fell in. He was carried under Dame Street and Wellington Quay into the Liffey, and survived because the tide was out."]),
   ("Into the Castle by the river", [
    "The culvert has always worried the Castle’s guardians. On 8 March 1921, during the War of Independence, Crown forces took George Harty, Dublin Corporation’s engineer in charge of sewers, to his office in an armoured car, made him hand over the drawings of the Poddle and the sewers near the Castle, and had him lead a British officer through a length of the culvert. Manholes along the route are still checked, and welded shut, before high-profile visits to the Castle."])],
  images=[("dublin-castle-gate", "The Palace Street gate of Dublin Castle"), ("under-olympia-cropped", "The Poddle beneath the Olympia Theatre"), ("podle-beneath-dame-street", "The culvert beneath Dame Street")],
  links=[("The Irish Times: Underground Dublin, a pilgrimage through an ancient tunnel network (2021)", "https://www.irishtimes.com/culture/heritage/underground-dublin-a-pilgrimage-through-an-ancient-tunnel-network-1.4662108"), ("Video: River Poddle in Dublin’s city centre, previously unseen", "https://www.youtube.com/watch?v=SLwzXheosOI"), ("Video: Dublin’s Hidden Rivers, the wall the 1985 bank robbers tried to use (from 4:06)", "https://www.youtube.com/watch?v=K5ygnHSLKLY&t=246s")]),
 dict(slug="liffey", name="Liffey Outfall", place="Wellington Quay",
  teaser="Journey’s end, under Wellington Quay.",
  sections=[("The outfall", [
    "The Poddle’s journey ends here, flowing out under Wellington Quay into the Liffey through a grating in the quay wall, “an iron grid or portcullis”, as McEntee and Corcoran put it, “outside the Clarence Hotel”. The Liffey is tidal here, so at high tide the grating disappears under the water.",
    "Interestingly the Geological Survey Ireland, in its report on the Poddle as a County Geological Site, describes the grating as worn and dirty and suggests replacing it with stainless steel, spelling out “Poddle” in steel letters on the quay wall, and putting an information board on the far bank so people can see where Dublin’s first river meets the Liffey. Maybe that’s something worth considering for the future!"]),
   ("Wellington Quay", [
    "Wellington Quay was the last of the Liffey quays to be built. Until the early 1800s the houses along this stretch backed straight onto the river, and Faden’s map of 1797 still shows the riverside closed off by buildings.",
    "The Wide Streets Commissioners changed that. Between 1812 and 1815 they built a granite quay wall from Essex Bridge, now Grattan Bridge, to where the Ha’penny Bridge stands, to give the city a continuous quayside. Sources differ a little on the dates: one says the quay was built around 1812, another that it was laid out about 1815.",
    "The western end was already called Custom House Quay, after Thomas Burgh’s Custom House of 1704 to 1707. Gandon’s new Custom House took over its work in 1791, the old building was used partly as a barracks from 1798, and it was pulled down as the new quay went in. The Clarence Hotel now stands on much of its site.",
    "The quay is named after the Dublin-born Arthur Wellesley, 1st Duke of Wellington, after his victory over Napoleon at Waterloo in 1815, and it had its new name by 1817.",
    "The National Inventory of Architectural Heritage describes the Poddle’s outfall as an elliptical-headed culvert in the face of the wall. The arch probably dates from the building of the wall, when the river had to be carried out to the new quay line, but we haven’t found a source that says so."]),
   ("The Merchants’ Arch", [
    "On the new quay the Commissioners offered the Merchants’ Guild a site for a hall, on condition that a public right of way ran through it from Temple Bar to the Ha’penny Bridge. Frederick Darley designed the Merchants’ Hall, built in 1821 and 1822, and that passage is the Merchants’ Arch. It is one of only three guild halls left in the city."]),
   ("The Ha’penny Bridge", [
    "At the east end of the quay is the Ha’penny Bridge. Before it was built, William Walsh ran seven ferries across the Liffey here. They were in such poor repair that he was told to fix them or build a bridge, and he chose the bridge.",
    "It opened in May 1816 as the Wellington Bridge, cast in 18 sections at Coalbrookdale in Shropshire. In return Walsh could charge a halfpenny toll for 100 years, collected at turnstiles at each end. The toll was dropped in 1919, and the bridge’s official name has been the Liffey Bridge since 1922."]),
   ("Standfast Dick", [
    "Under the water off the quay lies Standfast Dick, sometimes called Steadfast Dick, a reef of rock in the bed of the Liffey that ran roughly from below Dublin Castle to Capel Street. Smaller ships coming up to the old Custom House kept getting stuck on it.",
    "In 1776 London ordered the channel deepened, and the Ballast Office set labourers “to quarry the bed of stones called Standfast near the Custom House”. They didn’t get all of it. In 1971 a newspaper reported that from the Wellington Quay wall at low tide you could still see the rock “extending far out into the bed of Anna Liffey”.",
    "James Joyce knew it too. In a 1927 draft of the Anna Livia Plurabelle chapter of Finnegans Wake he wrote of “a rise every morning for Standfast Dick and a drop every minute for Stumblestone Davy”."]),
   ("Ulysses", [
    "In James Joyce’s Ulysses the outfall is placed, wrongly, at Wood Quay, in words that are unflattering but memorable:",
    "<blockquote>“From its sluice in Wood quay wall under Tom Devan’s office Poddle river hung out in fealty a tongue of liquid sewage.”</blockquote>"])],
  images=[("quay-outfall", "The Poddle outfall into the Liffey"), ("wellington-quay", "Wellington Quay"), ("ulysses-cover", "Ulysses, James Joyce")],
  links=[("National Inventory of Architectural Heritage: Wellington Quay", "https://www.buildingsofireland.ie/buildings-search/building/50020254/wellington-quay-dublin-2-dublin"), ("National Inventory of Architectural Heritage: The Merchants’ Arch", "https://www.buildingsofireland.ie/buildings-search/building/50020156/the-merchants-arch-48-49-wellington-quay-wellington-quay-dublin-2-dublin-city"), ("Archiseek: Wellington Quay", "https://www.archiseek.com/tag/wellington-quay-dublin/"), ("Crumlin and Walkinstown History Group: Wellington Quay", "https://poddle.crumlinwalkinstownhistory.ie/location/wellington-quay/"), ("Wikipedia: The Old Custom House, Dublin", "https://en.wikipedia.org/wiki/The_Old_Custom_House,_Dublin"), ("Wikipedia: Ha’penny Bridge", "https://en.wikipedia.org/wiki/Ha%27penny_Bridge")]),
]

def gal(*items):
    return '<div class="fig-grid">' + "".join(
        f'<figure class="fig"><a href="img/{f}.jpg"><img src="img/{f}.jpg" alt="{html.escape(c, quote=True)}" loading="lazy"></a><figcaption>{html.escape(c)} <a href="img/{f}.jpg">Open full size</a></figcaption></figure>' for f, c in items) + '</div>'

EIAR_CR = "From the environmental impact assessment report for the River Poddle Flood Alleviation Scheme (An Bord Pleanála case 306725). "
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
    "Its route is what puts the Poddle at the heart of Dublin, physically and in its history. Today almost all of its last four kilometres, under the south inner city, runs in culverts.",
    "Geologically it is a young river. Geological Survey Ireland lists the Poddle as a County Geological Site for Dublin City, noting that it formed after the last Ice Age, within roughly the last 11,000 years, on low-permeability glacial till. The survey picks it out because so much of its course runs in man-made channels and tunnels underground, which is unusual in Ireland."]),
   ("Source and names", [
    "The river rises around Cookstown, north-west of Tallaght, about 92 metres above sea level, where its first stretch is known as the Tymon River. Its catchment covers about 16 square kilometres, almost all of it now built up.",
    "The name has changed over the centuries: Podell in 1493, Puddell in 1603, and Poddle from 1695. In Irish it is An Poitéal, and it was also called the Salach, the dirty river. Other names turn up in local histories, among them Glascholach and Cam Uisce, the crooked stream, which has been suggested, without certainty, as the origin of the name Kimmage."])],
  images=[("poddle-catchment", "The Poddle catchment between the Dodder and the Camac"), ("1848-os-map-small", "Ordnance Survey map, 1848")]),
 dict(slug="first-diversion", name="The first diversion", when="Before 1244",
  teaser="Turning the Dodder into the Poddle at Balrothery.",
  sections=[("The first diversion", [
    "The first great change was the diversion of water from the Dodder into the Poddle at Balrothery Weir, near Firhouse. It was a remarkable piece of engineering. Some 10km from St Thomas’s Abbey, a weir was built across the Dodder and a new channel dug that carried most of the river’s ordinary flow for about 3km to join the Poddle near Mount Down, in Kimmage.",
    "It was done for two reasons. More water meant more power for the Abbey’s mills, and it gave the Abbey and the city a larger and steadier supply of drinking water, which was stored in a cistern outside James’s Gate, on what is now Thomas Street. The system ran for around 500 years."]),
   ("The writ of 1244", [
    "The first firm date is 29 April 1244, when the justiciar, Maurice Fitzgerald, ordered the sheriff of Dublin to find out, “by twelve free and lawful men”, where water could best be taken “and conducted to the King’s city of Dublin, for the benefit of the city and at the cost of the citizens”. Anyone who got in the way could be arrested. The Dodder weir was chosen, enlarged and repaired, and in 1245 the King ordered water piped to his new hall in Dublin Castle by the following summer.",
    "Who built the weir in the first place is less certain. Most accounts say the monks of St Thomas’s had it before 1244 and the citizens enlarged it. Others date the watercourse to between 1245 and 1254, or the weir itself to 1254, and one reading of the evidence puts the weir as early as the late 12th century. The Balrothery Weir page sets these out side by side."]),
   ("A shared river", [
    "The city and the Abbey had to share. Under their agreement the city paid for works on the monks’ weir on the Dodder, and the Abbey was paid a mark and a yearly rent of five marks, though the payments were sometimes late or missed. A public cistern outside James’s Gate is recorded supplying citizens in 1254, and a second conduit was built at the Cornmarket by the mayor John Le Decer in 1308.",
    "<p>Further down, at Harold’s Cross, the combined stream was split again by the Tongue, so that one third went to the city and two thirds to the Abbey mills. That is <a href=\"second-diversion.html\">the second diversion</a>.</p>"]),
   ("Sending it back", [
    "Ironically, the CFRAM Poddle options report of the 2000s examined an option for flood relief: “A suitable diversion route has been identified from the Poddle to the Dodder along Tymon Park running south of the M50.” Eight centuries after the monks turned the Dodder into the Poddle, the engineers proposed sending it back."])],
  images=[("ronan-1927-map-ii", "The Dodder, the Poddle and the City Water, with the weir (B, “Head”) and the Tongue (E). Map II from Rev. Myles V. Ronan, “The Poddle River and its Branches”, Journal of the Royal Society of Antiquaries of Ireland, 1927."), ("diversion-map", "The diversion from the Dodder to the Poddle"), ("dublin-1170", "Dublin c. 1170")],
  link=("balrothery-weir", "Read the full story of Balrothery Weir on the river walk")),
 dict(slug="second-diversion", name="The second diversion", when="1245",
  teaser="The Stone Boat splits the river for St Thomas’s Abbey.",
  sections=[("The second diversion", [
    "The second diversion was no less ingenious. In 1245, at what is now Harold’s Cross, the stream was split by the Tongue, a stone shaped like the bow of a boat and known locally as the Stone Boat. It sent part of the Poddle’s water west to St Thomas’s Abbey.",
    "You can still see both diversions. The first is no longer used, but its workings can be seen at Balrothery, near Tymon Park, just outside the M50. The Tongue, or Stone Boat, is still in the river near Mount Argus."])],
  images=[("stone-boat", "The Stone Boat"), ("dublin-1370", "Dublin c. 1300")],
  link=("stone-boat", "See the Stone Boat on the river walk")),
 dict(slug="city-watercourse", name="The City Watercourse and the Abbey Stream", when="1245 to 1324",
  teaser="Two channels made for the monks and the city, and how to find them on the map.",
  sections=[("The City Watercourse", [
    "The City Watercourse is an artificial channel. At the Stone Boat, in Harold’s Cross, it took one third of the river’s water: two thirds stayed in the Poddle and one third went into the watercourse, which carried it north-west towards Dolphin’s Barn. Near today’s Basin Lane it turned east along the south side of James’s Street and through Thomas Street into the city.",
    "It was the city’s main water supply for centuries, which is why the 1719 Act of Parliament was written to keep it clean and to stop mill owners starving it of water. A branch of it, the Tenter Water, rejoined the Poddle at Fumbally Lane. The Poddle’s one real tributary, the Commons Water, came in from Crumlin along the Cork Street area and joined it near the Coombe; both are drawn, approximately, on the map.",
    "On the map page the City Watercourse is shown as a dashed red line, from Balrothery Weir to the Stone Boat and on to Christ Church. As far as Dolphin’s Barn it follows a line drawn from old Ordnance Survey maps; the stretches above Mount Down and beyond Dolphin’s Barn are drawn from a local hand-drawn map with no stated source. Treat all of it as approximate."]),
   ("Water for the city", [
    "The scheme began with an inquiry. In April 1244 the justiciar, Maurice FitzGerald, ordered a search for a new water supply for Dublin, and the city came to an arrangement with St Thomas’s Abbey to take water from the Dodder at Balrothery. The work went on, by most accounts, from 1245 to 1324.",
    "From the basin near James’s Street the water ran along Thomas Street and High Street to a conduit at Christ Church and the Tholsel. Householders could tap it, but private lead pipes were supposed to be no thicker than a goose quill. In 1308 the mayor, John le Decer, paid for a marble cistern at Cornmarket, and iron mains began to replace the old pipes from 1802. In November 1970 the Evening Herald reported timber water pipes, perhaps 250 years old, dug up at Weaver’s Square."]),
   ("The Poddleologist", [
    "In the early 1970s the City Watercourse between Firhouse and Kimmage was threatened by new building. A Dominican nun, Sister Ann Dominica Fitzgerald, walked its length, fell into the Poddle twice while tracing it, and called herself a “Poddleologist”. She wrote to the papers in 1972 and 1973 to save the 700-year-old channel, and in 1976 led a Poddle tour for the Dublin Arts Festival, from Mount Argus to Warrenmount.",
    "Born in Blackrock, she taught at the Dominican convent at Muckross Park in Donnybrook and took her classes out on the river whenever she could. She photographed stretches of the watercourse before they disappeared, wrote the narration for a 16mm film of it made by John Gleeson of Inchicore, who also wrote to the papers to defend it, and contributed “Down the Old Poddle” to The Liberties of Dublin, edited by Elgy Gillespie (E. and T. O’Brien, 1973). Her interest began while she was writing a schools book on the Liffey and found there were no books on the subject. In a letter to the Irish Press on 1 May 1972 she wrote that she had gone back to re-photograph Mount Down Mill and found it razed. She died on 10 March 2006."]),
   ("The Abbey Stream", [
    "The Abbey Stream is the name given on modern maps to a channel that leaves the Poddle near the Hospice and Greenmount, at Harold’s Cross, and runs north-west towards St Thomas’s Abbey. Rev. Myles Ronan’s 1927 map marks a “course of ancient water” heading the same way, across the fields east of the river. Between 1245 and 1324 the monks redirected the river’s course to serve their mills, and this is the kind of channel that diversion would have made.",
    "At Mount Jerome the Poddle itself makes an almost right-angled turn, and Ronan asked whether that too was a diversion made for the abbey. On the map page the Abbey Stream is the amber band; its middle section is under streets, so the link across it is a straight, approximate line."]),
   ("What the old records say", [
    "Older writers describe the two branches at the Tongue in detail. The branch that became the Poddle’s city course ran by Greenmount, under the canal, then by Blackpitts, New Row and Patrick Street to the castle and the Liffey. The City Watercourse proper ran to Dolphin’s Barn and along an embankment called the Pipes to the city basin near James’s Street. A cistern was built near the old reservoir around 1670. The planning file page has the full record."]),
   ("Two channels, one river", [
    "The two are easy to confuse. The City Watercourse leaves the river at the Stone Boat, upstream. The Abbey Stream leaves it further down, at Harold’s Cross, and both were made to serve the abbey and the city."]),
   ("The Earl of Meath’s Watercourse", [
    "When Henry VIII closed St Thomas’s Abbey in 1538 its lands, with “a malt mill, a wood mill and two double mills”, went to Sir William Brabazon, ancestor of the Earls of Meath. From then on the abbey’s channel through the Liberties was called the Earl of Meath’s Watercourse, and the Earls controlled water supply and charges in their Liberty for more than three centuries.",
    "Dublin Corporation eventually bought those rights, though even one book gives two versions: McEntee and Corcoran say in one chapter that it was in 1864 for £6,400, and in another that it was in 1861 for £6,000. The Earl kept the land, the river bed and banks, and the right to use the water for mills. A reservoir built for him around 1820, the Liberty Basin at Pim Street, was built over in Victorian times and uncovered again in 2006."])],
  images=[("stone-boat", "The Stone Boat dividing the flow"), ("st-thomas-abbey", "St Thomas’s Abbey on an early map of Dublin"), ("news/clip-1923-08-12-a-quaint-system", "“A Quaint System”, by Rev. M. V. Ronan, on the watercourse and the city’s conduits. Sunday Independent, 12 August 1923, p. 9. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1929-06-30-commentary-on-crumlin-cross", "“Commentary on Crumlin Cross”, by Tomás S. Cuffe, with Ronan’s figure of 613,200 gallons a day. Sunday Independent, 30 June 1929, p. 6. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1968-03-22-the-liberty-watercourse", "“Know Your Dublin: The Liberty Watercourse”. Sketch by Liam C. Martin, text by J. B. Malone. Evening Herald, 22 March 1968, p. 14. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1970-11-09-old-water-pipes-found", "“Old water pipes found” at Weaver’s Square. Evening Herald, 9 November 1970, p. 3. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1972-07-25-bad-planning-ancient-water-course", "“Bad planning may bury city’s ancient water course”, by P. J. Donaghy. Evening Herald, 25 July 1972, p. 6. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1973-01-05-city-watercourse-letter", "“City watercourse”, a letter from John Gleeson of Inchicore. Irish Press, 5 January 1973, p. 8. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1973-06-16-a-nun-who-dipped-into-history", "“A nun who dipped into history – and got wet”: Sister Ann Dominica Fitzgerald. Words by Colm Boland, pictures by Donal Doherty. Evening Herald, 16 June 1973, p. 9. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1976-03-07-follow-me-says-sister-ann", "“Follow me, says Sister Ann”: her Arts Festival walk along the Poddle. Sunday Independent, 7 March 1976, p. 9. Clipping courtesy of the Crumlin and Walkinstown History Group.")],
  links=[("See the City Watercourse, Abbey Stream and Dodder Overflow on the map", "map.html"), ("What the planning file says", "planning-record.html")],
  link=("mount-jerome", "See the Mount Jerome turn on the river walk")),
 dict(slug="1719-act", name="The 1719 Act", when="1719",
  teaser="Parliament acts to clean up the city’s water.",
  sections=[("The 1719 Act of Parliament", [
    "An Act of Parliament of 1719 describes the watercourse as “the chief supply of water not only for the inhabitants of the said city; but also for this majesties Castle of Dublin, and without which it would suffer exceeding great prejudice.”",
    "The Act provided for cleaning and repairing the watercourse, because:",
    "<blockquote>“…tuck mills, in which urine, soap and other unwolsome materials are made use of, and diers of linnen and woolen cloath and yarn, and skinners dip, wash, scour and cleanse great quantities of died linnen and woolen cloath, yarn and skins in the said water-course, by which the water is greatly corrupted, endangering the healths of the inhabitants of the said city.”<cite>Original 1719 spelling</cite></blockquote>",
    "Mills along the watercourse were also a problem, building dams and ponds that blocked the flow of water into the city."]),
   ("Why Parliament stepped in", [
    "McEntee and Corcoran explain the background. In 1718 there were complaints about effluent from a tuck mill and a paper mill on the watercourse, and the mill owners argued that the Corporation had no power to stop them. The Act, “for cleaning and repairing the watercourse from the River Dodder to the City of Dublin, and to prevent the diverting and corrupting the Water therein”, gave the Corporation full control.",
    "It also outlawed tuck mills and woollen mills on the Poddle and the City Watercourse. Mount Down Mill, near Kimmage, was one that had to change: it had been a woollen mill, and after the Act it was turned over to grinding flour.",
    "The rules were not new. A Corporation order of 1538 had already said that “no manner person may wash foul clothes … and no man cast no corrupt thing in the same water, as blood of swyne or kyne … nor wash tripes or puddings there”, on pain of a fine of twelve pence."]),
   ("After the Act", [
    "The Poddle and the City Watercourse remained the city’s only public water supply until 1745, when a pump on the Liffey at Islandbridge began to serve the north side. Water from the Grand Canal began to replace the Poddle at the City Basin in 1775 by most accounts (Fitzgerald says 1776). By then, William Handcock wrote, the citizens were lucky not to depend on it, “for it is so polluted by paper-making that it has become poisonous, and cattle and horses have died from drinking it.”"])],
  images=[("1719-act-of-parlament", "An Act for Cleansing and Repairing the Water-Course, Dublin, 1719")]),
 dict(slug="mills", name="The mills", when="1240s to the 1960s",
  teaser="Seven centuries of water power, from abbey mills to cotton and poplin.",
  sections=[("Why the water mattered", [
    "The Poddle was bent and diverted above all to turn mill wheels. The monks of St Thomas’s Abbey brought Dodder water into it in the 1240s partly for their mills, and between 1245 and 1324 they redirected its course again to serve them. Archaeology backs this up: a millpond excavated on the Poddle’s bank off New Street was dug in the 13th or 14th century and filled in during the 14th or 15th (Antoine Giacometti, “Blackpitts: Dublin’s medieval tanning quarter”). By 1719 Parliament was complaining that mills along the watercourse were building dams and ponds and starving the city of water."]),
   ("From source to sea", [
    "<ul class=\"mill-list\"><li><strong>Mount Down Mill</strong>: where the City Watercourse met the Tymon River, upstream of Kimmage. In 1952 its owner, Peter Cullen, sued Dublin Corporation for £20,000 over the mill’s ancient water right, after the Corporation lowered the crest of the city weir. Sources differ on the details: McEntee and Corcoran say he was awarded £20,000 in the High Court in 1952, while Sister Ann Dominica Fitzgerald says the weir was lowered in 1943 and the £20,000 awarded by the Supreme Court in 1960.</li>"
    "<li><strong>Ravensdale Mills</strong>, Kimmage Road Lower: corn and flour, with a pond, sluice and weir, on maps from the 1830s to 1940.</li>"
    "<li><strong>Farrington’s Mill</strong>, Kimmage Cross Roads: flour, with a water turbine until the 1920s.</li>"
    "<li><strong>Larkfield Mills</strong> and a second mill and pond near St Martin’s Drive, with windmills close by.</li>"
    "<li><strong>Loader’s Park Mills</strong>, Kimmage Road Lower: a corn mill, now the Waterwheel apartments.</li>"
    "<li><strong>Mount Argus</strong>: a 19th-century paper mill and a flour mill that became a laundry.</li>"
    "<li><strong>Harold’s Cross</strong>: several watermills, including one in today’s Harold’s Cross Park and a flour mill by Mount Jerome’s gates.</li>"
    "<li><strong>Greenmount Mills</strong>: a corn mill turned cotton mill by 1807, enlarged by the Quaker Pim family for cotton and linen.</li>"
    "<li><strong>Rutland Mill</strong>, Rutland Avenue, Dolphin’s Barn: a flour mill on the City Watercourse, run by Clibborn and Shaw. George Carr Shaw, father of George Bernard Shaw, was a partner.</li>"
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
   ("Floods in the newspapers", [
    "Old newspapers fill in the gaps between the big floods. In March 1787 Faulkner’s Dublin Journal reported that “the river Soulagh (or Poddle, as commonly called) has overflowed the end of New Street, near Kevin Street, to such a degree to make it impassable, so that the folks who pass that way are carried over the stream in Noddies”, the little one-horse cabs of the day. That November the floods came again: Patrick Street “presented a melancholy spectacle”, people from New Street to Bride’s Alley had to live in their upstairs rooms, and the river broke out in the Lower Castle Yard and flooded Crampton Court and Palace Street. In January 1784 melting snow and heavy rain flooded the Liffey, the Dodder and the Poddle together. On 21 February 1910 the Irish Independent reported the Poddle overflowing at Harold’s Cross. On 13 March 1937 the Irish Press described cottages on Rutland Avenue flooded about three feet deep when the culvert at Dolphin’s Barn choked. In December 1954 families behind Fortfield Road in Terenure were forced out of their homes, and on St Swithin’s Day, 15 July 1973, the river flooded two houses at Loder Park beside Mount Argus. In the storms at the end of December 1978 it burst its banks at Templeogue. Dublin Corporation’s minutes also record flooding of the Dodder, the Camac and the Poddle in 1959.",
    "Lower Kimmage Road had a particular problem. In November 1985 the Irish Press and the Evening Press reported back gardens collapsing into the river, more were lost in 1987, and the Corporation went to tender in 1986 for about 250 metres of precast culvert to enclose that stretch. The Corporation’s minutes for 1985 to 1987 follow the story, from a report on the river at Kimmage Road Lower and the collapse of the garden of No. 9 into it, to the culverting between Kimmage Road Lower, Harold’s Cross Bridge and Parnell Road, and a report on the 1986 flooding. The newspaper reports are collected by the Crumlin and Walkinstown History Group’s Poddle project.",
    "McEntee and Corcoran give the engineers’ side. Jack Keyes’s report of December 1986 called the Hurricane Charlie flood of that August “among the worst on this river since records began”, with 80 homes and 5 businesses flooded, worst at Kimmage Cross Roads, Ravensdale, Mount Argus and Harold’s Cross. At Lower Kimmage Road the river ran in a culvert under the front gardens of more than twenty houses; a long section collapsed in 1985, and Keyes found that only 15 per cent of the river’s course could carry a flood. The front-garden culvert was rebuilt in 1988 and 1989."]),
   ("24 October 2011", [
    "On the evening of 24 October 2011, between 80 and 90mm of rain fell on Dublin in six hours. The Poddle burst its banks at Tallaght, Kimmage, Harold’s Cross and Mount Jerome. Across the Dublin region about 1,000 properties flooded, 318 roads were badly flooded, power was lost, and two people died. Both South Dublin County Council and Dublin City Council activated their major emergency plans, and insurance claims were estimated at €127 million.",
    "On the Poddle itself, McEntee and Corcoran record, debris blocked the river screens at the Lakelands overflow and the river burst its banks and ran overland; then the screen at Gandon Hall, near Harold’s Cross, blocked too, causing widespread flooding downstream. Eleven places and 113 premises were affected, many cars were written off, and one person died."]),
   ("The River Poddle Flood Alleviation Scheme", [
    "The scheme is a joint project of South Dublin County Council, Dublin City Council and the Office of Public Works, which funds it. It is designed to protect more than 800 properties against a 1-in-100-year flood, with an allowance for climate change. The estimated cost was €7 million in 2020, revised to €10 million by 2023.",
    "Its main idea is to store water upstream rather than build high walls in the city. Tymon Lake becomes a flood reservoir behind a 220m embankment and flow-control structure, and Whitehall Park and Ravensdale Park are reshaped to hold water. Downstream, new walls go in at Whitehall Road, Fortfield Road, Poddle Park, St Martin’s Drive and a 25m wall at Mount Argus Close. An integrated constructed wetland in Tymon Park cleans the water, and floating nesting platforms on the lake are for birds."]),
   ("Timeline", [
    "<ol class=\"timeline-list\"><li><span>2011</span> October floods</li><li><span>2018</span> Consultants appointed</li><li><span>Feb 2020</span> Planning application lodged with An Bord Pleanála</li><li><span>Jun 2023</span> Approved, the first flood scheme to go through Part 10 planning</li><li><span>Apr 2024</span> Office of Public Works starts building</li><li><span>20 Feb 2025</span> Tymon Lake flood storage goes into use</li><li><span>2025</span> Works start in Wainsfort and Ravensdale Park</li><li><span>2027</span> Expected completion</li></ol>"]),
   ("Trees and wildlife", [
    "The scheme has not been uncontroversial. When it was published in 2020, local groups including Save the Poddle’s Wildlife Sanctuary objected to the number of trees to be felled and questioned the bird surveys at Tymon Lake. Some argued for moving walls back from the river to create natural floodplain, for example at St Martin’s Drive."])],
  images=[("dodder-overflow-fas-scheme", "Proposed works, Poddle Flood Alleviation Scheme"), ("m50-crossing-upgrade", "Tymon Park works plan"), ("news/clip-1934-01-06-floods-in-dublin-1784", "“Floods in Dublin”: the January 1784 flood, when the Poddle spilled over Patrick’s Street and the Close. Reprinted in the Belfast News-Letter, 6 January 1934, p. 12. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1910-02-21-remarkable-city-scenes", "“Remarkable City Scenes”: the Poddle over its banks at Harold’s Cross and Mount Argus. Irish Independent, 21 February 1910, p. 5. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1954-12-13-poddle-forced-families-out", "“Poddle Forced Families Out”: Terenure, behind Fortfield Road. Irish Independent, 13 December 1954, p. 9. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1973-07-16-river-burst", "“River Burst”: Loder Park, Mount Argus. Irish Independent, 16 July 1973, p. 1. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1978-12-30-storms-trail-of-havoc", "“Storms’ trail of havoc grows longer”: the Poddle over its banks at Templeogue. Irish Press, 30 December 1978, p. 3. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1985-11-30-poddle-surfaces-in-garden", "“Poddle surfaces in garden”: a culvert collapse on Kimmage Road Lower. Irish Press, 30 November 1985, p. 5. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1985-11-30-gardens-fall-into-river", "“Gardens fall into river”: two more Kimmage Road Lower gardens. Evening Press, 30 November 1985. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1986-05-23-culverting-kimmage-road-lower", "Dublin Corporation’s tender notice for culverting the Poddle at Kimmage Road Lower. Irish Press, 23 May 1986, p. 19. Clipping courtesy of the Crumlin and Walkinstown History Group."), ("news/clip-1987-10-22-that-sinking-feeling", "“That Sinking Feeling”: collapsed front gardens on Lower Kimmage Road. Picture by Tony Reddy. Irish Independent, 22 October 1987, p. 5. Clipping courtesy of the Crumlin and Walkinstown History Group.")],
  links=[("River Poddle Flood Alleviation Scheme website", "https://www.poddlefas.ie/"), ("Crumlin and Walkinstown History Group: newspaper reports on flooding", "https://poddle.crumlinwalkinstownhistory.ie/location/kimmage-road-lower/"), ("Dublin InQuirer: residents debate the scheme (2020)", "https://www.dublininquirer.com/residents-debate-environmental-impact-of-a-plan-to-build-flood-defences-on-the-river-poddle/"), ("Facts and figures from the planning file", "planning-record.html"), ("Live river levels and flood maps", "river-data.html")]),
 dict(slug="planning-record", name="What the planning file says", when="2019 to 2023",
  teaser="Facts and figures from the flood scheme’s planning application and environmental impact report.",
  sections=[("Where the files are", [
    "Each planning file below is placed on the map by the site it covers. Select a marker to read what that file says about the river. Positions are approximate, taken from the site addresses, and the blue line is today’s mapped course of the Poddle.",
    "<!--PLANMAP-->"]),
   ("Where this comes from", [
    "The Poddle flood scheme was a joint application by South Dublin County Council and Dublin City Council, with the Office of Public Works, to An Bord Pleanála (case 306725). The application includes a planning report, an environmental impact assessment report (EIAR) and a heritage chapter that rewrites the river’s history from the maps and excavations. This page gathers the details that are not on the other pages, from the full documents, which are linked below. It also draws on three Dublin City Council planning applications: the Tenters Blackpitts drawings (2768/09), a mixed-use scheme on Donore Avenue (4156/06) and the Ship Street office and convention centre scheme (4223/18)."]),
   ("The river in numbers", [
    "The EIAR gives the river’s length as about 11.6 km, and its catchment as about 16.4 km² (16,400 hectares). Its non-technical summary rounds the length to about 10 km. The river rises at Cookstown, north of Tallaght, and flows through Tymon Park, under the M50, past Templeogue, Kimmage, Mount Jerome and Harold’s Cross, and crosses under the Grand Canal before running under the city to the Liffey at Wellington Quay. The lower and middle reaches are heavily urbanised, culverted and partly channelled.",
    "Dublin City Council’s presentation on the scheme says the river once powered 52 mills and commercial enterprises along its course, and that it has 15 associated watercourses.",
    gal(("eiar-catchment", "The Poddle catchment, with the culverted stretches in red. Figure 1-1, EIAR Volume 2 main report, Nicholas O’Dwyer Ltd, 2019. " + EIAR_CR))]),
   ("Flood history in the report", [
    "The planning report lists the significant floods as August 1986, June 1993, November 2000, September 2008 and October 2011.",
    "On 25 August 1986, Hurricane Charlie seriously affected 80 households and 5 commercial properties from Kimmage Cross Roads to the Grand Canal. In November 2000, 103 mm of rain fell in 48 hours and the banks broke at Kimmage. In June 1993 the river overtopped after rainfall estimated at between a 1-in-100 and 1-in-250-year event, but the flooding was relatively minor. In September 2008, 58 mm fell over 11 hours in Kimmage.",
    "The October 2011 flood is the one that led to the scheme. Up to 90 mm fell in six hours, more than the 1-in-100-year level at the gauges. It flooded Our Lady’s Hospice, Greenmount Avenue, Boyne Court and Gandon Close in Harold’s Cross, and the river burst its banks at Ravensdale Park. Over 50 properties flooded.",
    gal(("eiar-flood-2011-a", "Flooding at Harold’s Cross, October 2011. Figure 4-1, EIAR Volume 2 main report. " + EIAR_CR), ("eiar-flood-2011-b", "Flooding, October 2011. Figure 4-1, EIAR Volume 2 main report. " + EIAR_CR))]),
   ("The scheme, place by place", [
    "The scheme protects against a flood with a 1% chance of happening in any year, and assumes that 60% of the 12 major culverts, and 40% of the others, are blocked. It adds a freeboard of 500 mm to embankments and 300 mm to walls. The report says 921 properties are protected, out of 1,377 at risk, and that more than 200 properties at Whitehall, Mount Argus Road and the Coombe remain at risk of surface-water flooding, which the scheme does not cover.",
    "At Tymon Park a flood storage embankment and flow control structure hold back 66,000 cubic metres and limit the flow passed downstream to 748 litres a second, the 2-year flow. An integrated constructed wetland improves water quality, and floating nesting platforms go onto Tymon Lake. At Whitehall Park the channel is realigned and walls are built around the Lakelands overflow. At Ravensdale Park flood walls 1.1 to 1.35 m high create about 800 cubic metres of extra storage. St Martin’s Drive gets a 1.1 m wall, and there are further walls at the back of Fortfield Road and at Mount Argus Close.",
    "Flap valves are fitted to every culvert that drains to the river. Manholes are sealed at Poddle Park, Ravensdale Park, St Teresa’s Gardens, Donore Avenue and the National Stadium. More than 50 culverts, weirs and bridges were surveyed from Greenhills Road to Gandon Close, and level alarms and cameras monitor the Lakelands overflow weir, the Wainsfort Manor culvert and Gandon Close.",
    "At the planning stage the report listed the lengths of wall as 453 m from Limekiln Road to Wellington Lane, 367 m from Wellington Park to Wainsfort Manor, 245 m from Glendale Park to Kimmage Manor, 255 m at Ravensdale Park, 223 m at Poddle Park and 291 m from Bangor Road to Mount Argus, plus 127 m, 284 m and 135 m of earth embankment at Tymon Castle, Tymon Lake and Whitehall Park. The designs changed before building, so treat these as the application’s figures.",
    gal(("eiar-tymon-embankment", "The proposed Tymon flood storage embankment (Option 2). Figure 4-2, EIAR Volume 2 main report. " + EIAR_CR), ("eiar-whitehall-terraces", "Whitehall Park with terracing (Option 2). Figure 4-3, EIAR Volume 2 main report. " + EIAR_CR))]),
   ("Culverts, and where the river comes up", [
    "The EIAR’s map study finds that a row of houses on the northern end of Kimmage Road Lower led to the river being culverted there by 1906 to 1909. It comes up again north of Mount Jerome Road, west of Mount Jerome Church, which matches the open stretch on the map. The scheme’s fish survey notes that the culverts have made the lower river impassable to migratory fish, and that the river has limited fisheries value."]),
   ("The river’s history, from the heritage chapter", [
    "The EIAR dates the channel from Balrothery, near Firhouse, to about 1244, with the Firhouse weir possibly as early as the late 12th century. A 1244 inquisition ordered by the justiciar Maurice Fitzgerald looked at how to bring more water to Dublin, and the Dodder weir was enlarged. In 1245 the King directed John FitzGeffrey to finish his hall in the castle and to bring water to it by the summer of 1246. A 1259 inquisition records an agreement between the monks of St Thomas’s and the citizens to make the new watercourse.",
    "The report describes the Tongue, today’s Stone Boat, as a wedge-shaped stone pier at the junction of the Poddle and the City Watercourse, which split the flow to regulate the water reaching the city. The City Watercourse was relied on until 1755, when the Grand Canal supplemented the supply, and it was replaced in the 19th century by the Bohernabreena and Vartry reservoirs. It fed cisterns near James’s Street and later the Grand Canal Basin. The name is recorded as “le Poddell” in 1506.",
    "Tymon Castle, a 15th-century tower house in Tymon Park, was demolished in 1960, and the site is a recorded monument. The report notes that the Wainsfort Manor Crescent mill, weir and millrace listed in the protected structures record could not be found on historic maps or on the ground.",
    gal(("roque-1760-watercourse", "Extract from Rocque’s map of County Dublin, 1760, marking the City Watercourse. Figure 11-4, EIAR Chapter 11. " + EIAR_CR), ("taylor-1816-tongue", "Extract from Taylor’s map of the environs of Dublin, 1816, from Kimmage to Harold’s Cross, with the Tongue. Figure 11-5, EIAR Chapter 11. " + EIAR_CR), ("roque-1760-tymon", "Extract from Rocque’s map of County Dublin, 1760, showing Tymon Castle and the City Watercourse. Figure 11-3, EIAR Chapter 11. " + EIAR_CR))]),
   ("What the digs found", [
    "Of 40 archaeological investigations within 250 m of the scheme, several found the medieval watercourses. Test pits at St Teresa’s Gardens found thick, water-laid silts from a medieval watercourse, and two investigations at Ruben Street found the medieval City Watercourse. At Cork Street the south side of the diverted Poddle was exposed. At the Mercy Convent on Cork Street, the remains of tanning boxes were found where the 1866 map shows a tan yard.",
    "Closer to the city, archaeologists working at Tenters Blackpitts, off Mill Street, in 2005, 2007 and 2016 found a possible river channel with a medieval organic layer in it, a red-brick culvert that cuts through older cobbling about half a metre below the ground, and the tanneries shown on Roque’s map of 1756, including two de-hairing barrels. The 2007 report says that the middle of the site was heavily disturbed by building the Poddle culvert and its overflow.",
    gal(("eiar-heritage-map-sw", "Heritage assets at the south-western end of the scheme. Figure 11-1, EIAR Chapter 11, Irish Archaeological Consultancy. " + EIAR_CR), ("eiar-heritage-map-ne", "Heritage assets at the north-eastern end of the scheme. Figure 11-2, EIAR Chapter 11, Irish Archaeological Consultancy. " + EIAR_CR))]),
   ("The official record of the watercourses", [
    "The heritage chapter’s appendix reproduces the National Monuments Service record for the City Watercourse. It describes the Tongue, the “wedge-shaped stone” that divided the watercourse of the Poddle and the Dodder, in the words of Weston St John Joyce in 1912. Two thirds of the flow went to the city by way of Greenmount, under the canal at Goodbody’s factory, then to Blackpitts, New Row and Patrick Street, past St Patrick’s Cathedral, and east through Castle Street and Palace Street to Wellington Quay, where it entered the Liffey. The other branch went north at the Tongue to Dolphin’s Barn, and then along an elevated rampart known as the Back of the Pipes, or the Pipes, to the old City Basin near James’s Street.",
    "The same record, drawing on H. F. Berry in 1891, says the watercourse was built in the middle of the 13th century, with its head at Balrothery, in Tallaght. It flowed north-east, skirting the churchyard wall at Templeogue, and was joined by the Poddle at Mount Down Flour Mills. From there the two ran as one stream to the Tongue at Kimmage. A large cistern was built around 1670 on or near the ancient reservoir, which is thought to have been west of St Thomas’s Abbey. Berry also wrote about an inquisition of 1258, which the EIAR dates to 1259.",
    "Later writers add numbers for the mills. J. Hegarty records that in 1844 Robert Mallet listed 24 mills at work on the Dodder, 12 on the main stream and the rest on the City Watercourse. B. Mac Giolla Phádraig dates the weir at Firhouse to 1254, and says there were 32 mills in 1879, as well as factories, breweries and distilleries on its banks. He also records that a stream taken off the watercourse in Terenure supplied three fishponds.",
    "The National Monuments Service gives map references for some of these places. Its Tongue record sits where the Stone Boat is on the map, and a recorded mill site at Harold’s Cross sits beside Greenmount. A watercourse was recorded at Reuben Street, and Donore Castle, a medieval castle mentioned in 1228, is recorded at White Swan Business Park, off Donore Avenue, with no visible trace."]),
   ("Blackpitts: the culvert on the drawings", [
    "The planning drawings for the Tenters development at Blackpitts, lodged with Dublin City Council in April 2009 for BAM Property and drawn by the engineers WYG, include a rare engineering view of the culverts. One sheet is a long section through two existing culverts. In the first, the culvert bed is at about 9.7 metres above Malin Head, its roof at about 11.1 to 11.7, and the ground above at about 11.7 to 12.1, so the culvert lies about two metres down with its roof close to the surface. In the second, the silt was too deep for the survey to find the bed. The proposal reroutes the culvert in a precast concrete box, 1.8 metres wide, with its bed at about 9.65 metres, and the drawings mention underpinning installed under an earlier planning permission (4685/05) to keep an old archway.",
    "These show the river as a working piece of drainage under a modern site, about two metres below the street, and match what the archaeologists found a few years later: a brick culvert cutting through older cobbling, and river channel deposits beneath.",
    gal(("tenters-culvert-sections", "Longitudinal sections through the existing culverts, Tenters Development, Blackpitts. Drawing C-12, WYG for BAM Property Ltd, Dublin City Council planning ref 2768/09, received 9 April 2009."), ("tenters-rerouted-culvert", "Proposed rerouted culvert, sections and details, sheet 1 of 2. Drawing C-05, WYG for BAM Property Ltd, Dublin City Council planning ref 2768/09, received 9 April 2009."))]),
   ("Donore Avenue: keeping clear of the culvert", [
    "The 2006 application for a mixed-use development on Donore Avenue, by the engineers Lohan and Donnelly and Collins Maher Martin Architects, shows the culverted Poddle running diagonally across the site, which was then a printing works beside the White Swan Business Park. The drainage drawing marks a strip along the river line “Poddle keep 6 m distance”, and the building is set back from it. The drawing also shows a 300 mm local authority sewer under Donore Avenue, and the surface-water design attenuates a 1-in-30-year storm in 23.26 cubic metres of storage so that the site does not add to the load on the old drains.",
    gal(("donore-drainage", "Drainage layout, mixed-use development at Donore Avenue, with the note “Poddle keep 6 m distance”. Drawing C01, Lohan & Donnelly, Dublin City Council planning ref 4156/06, received 21 July 2006."), ("donore-existing-site", "Existing building plan and elevations, Donore Avenue. Drawing P003/A, Collins Maher Martin Architects, 17 July 2006, Dublin City Council planning ref 4156/06."))]),
   ("New Row South: the culvert and the mill race", [
    "The 2019 application for 27 to 29 New Row South, at the junction of Blackpitts and Fumbally Lane (Dublin City Council planning ref 4423/19, for TC Fumbally Properties Ltd), is a hotel and shared-living scheme of 4 to 8 storeys round a protected former laundry building. The Poddle runs under it. The engineers’ report from J.J. Campbell & Associates says the river is enclosed in a culvert along the eastern boundary of the site, with no manholes or access points inside the site. The nearest manhole, on Fumbally Lane, has a cover level of 11.074 m, and the new ground floor is more than a metre higher.",
    "The flood risk assessment by JBA Consulting (5 November 2019) says the Poddle is a culverted watercourse along the south-eastern boundary and that the culvert system then runs north-north-east to the Liffey, 50 m west of the Ha’penny Bridge. It uses the Eastern CFRAM model: the site is in Flood Zone C, with a small strip along the southern boundary in Zone B. At the 1% flood the modelled depth is 0.25 m, and 0.5 m at the 0.1% flood, only at the corner of Blackpitts and Fumbally Lane. The modelled 1% flow in the culvert at the node 155 m downstream is 2.26 cubic metres a second. The report says the flooding would come from water surcharging out of the system upstream, where the culvert on Donore Avenue is too small, and running overland to the site from the west. It found no recorded flooding on the site, and notes that the October 2011 flood did not reach it.",
    "The engineers agreed the design with Dublin City Council’s drainage department on 12 July 2019 and discussed the culvert with its Flood Projects and Water Framework Directive Division. Their proposal keeps a clear 3 m on each side of the culvert, with a 4 m high corridor above it for an excavator. Three columns on drilled steel-lined piles are proposed where a protected wall bridges over the culvert, and the foundations are designed so that no building load reaches it. Their correspondence says the same approach was used on the neighbouring site, where about 3.7 m of headroom was provided. A local objector argued that 3 m might not be enough given the piling needed, and the planner’s report recorded that concern.",
    "The archaeology report from the city archaeologist records that the site lies in the zone of constraint for a Recorded Monument and the zone of archaeological interest. The archaeological impact assessment by Franc Myles (4 November 2019) found the ground floors of three late 17th-century Dutch Billy houses below the present slab, and identified the Poddle culvert and a culverted mill race within the site. The Newmarket and Blackpitts area was developed in the 17th century as a commercial and industrial district, and the report calls the site one of significant industrial heritage. Work down to formation level is to be monitored by an archaeologist, and any deposits above formation level excavated. The planner’s report of 30 March 2020, after further information received on 4 March 2020, recommends a grant of permission with conditions, including drainage conditions."]),
   ("Ship Street and the Castle: the line through the city", [
    "The engineering report for the Ship Street office and convention centre, lodged in 2018 for a site between Ship Street Great and Chancery Lane, has a page on the Poddle. It cites Clair Sweeney’s Rivers of Dublin, which says the river is culverted or piped for about 4 km through the city, and that its exact historic line is not known, although the section through Dublin Castle is well documented. The river ran parallel with Patrick Street, divided into two or more courses down the west and east sides of the street as far as Ross Road and the site of the southern city wall. It then ran along the walls and the castle ramparts, around the Royal Chapel, and out at the Lower Castle Gate at Palace Street and Dame Street. The report also reproduces a map from D. McEntee and M. Corcoran’s study The Rivers Dodder and Poddle: Mills, Storms, Droughts and the Public Water Supply.",
    "Boreholes sunk on the site in 2005 found made ground to between 3 and 5 metres below the surface, glacial till down to about 9 metres, and limestone bedrock between 7 and 9 metres down. The application includes a Dublin City Council drainage record map at 1:1000, dated 16 March 2016, showing the sewers around Ship Street, Chancery Lane and Golden Lane. That shows the kind of record the council will supply for a site: the sheet carries a warning that it is supplied from the corporation’s record sheets without prejudice, and that its accuracy must be checked on site.",
    gal(("shipstreet-drainage-record", "Dublin City Council drainage record sheet, scale 1:1000, 16 March 2016, around Ship Street, Chancery Lane and Golden Lane. From the Ship Street application, Dublin City Council planning ref 4223/18, received 22 October 2018. Dublin City Council Drainage Design Division, supplied without prejudice; accuracy to be verified on site."))]),
   ("Floods back to 1905", [
    "A floodinfo.ie report attached to the Ship Street application, produced on 25 May 2016, lists the floods recorded for the area. For the Poddle and its tributary it shows Limekiln Lane on 24 August 1905, St Claire’s Avenue and Limekiln Lane on 3 September 1931, a tributary at Marrowbone Lane on 21 January 1941, Clanbrassil Street and Mount Jerome at Harold’s Cross in the storm of 11 June 1963 that also flooded Grafton Street and Rathmines, the Poddle in August 1986, and Mount Argus Road and Kimmage Road Lower on 24 October 2011."]),
   ("Options and the edge of the scheme", [
    "The report compares two designs. Option 1 raised walls along the whole river, some of them 2 m or higher: 44 separate defences over 3.8 km, with pumping stations to pass surface-water runoff over the lines. The chosen Option 2 stores water upstream instead, and needs only 27 defences over 1.5 km. The application describes the works as running from Tymon North, Tallaght, to Marrowbone Lane in the city. An Bord Pleanála asked for further information on 17 July 2020, and the applicants answered on 19 October 2020, with new material on natural flood management, Whitehall Park and St Martin’s Drive."]),
   ("The mills in the report", [
    "The heritage chapter lists the mills it found on historic maps. They are described on the mill sites page, which now includes Cutlers Mill and its millrace, a flour mill in the Kimmage demesne, Tinker Mill, and the Domville or Mount Down Mill at Templeogue, where the old records say the Poddle met the City Watercourse."])],
  images=[],
  links=[("EIAR Volume 2, main report (An Bord Pleanála case 306725)", "https://www.pleanala.ie/publicaccess/EIAR-NIS/306725/River%20Poddle%20FAS/Part%203%20EIAR/Volume%202%20EIAR/Part%20I/Volume%202%20Part%201%20-%20Main%20Report.pdf"),
         ("EIAR Chapter 11: archaeology, architecture and cultural heritage", "https://www.pleanala.ie/publicaccess/EIAR-NIS/306725/River%20Poddle%20FAS/Part%203%20EIAR/Volume%202%20EIAR/Part%20II/11.%20Archaeological%20Architectural%20Cultural%20Heritage.pdf"),
         ("EIAR Volume 1: non-technical summary", "https://www.pleanala.ie/publicaccess/EIAR-NIS/306725/River%20Poddle%20FAS/Part%203%20EIAR/Volume%201%20Non-Technical%20Summary/Volume%201.%20Non-Technical%20Summary.pdf"),
         ("Planning report, February 2020", "https://www.pleanala.ie/publicaccess/EIAR-NIS/306725/River%20Poddle%20FAS/Part%201%20-%20Planning%20Application%20Documents/Section%207%20-%20Planning%20Report/Poddle%20Flood%20Alleviation%20Scheme%20Planning%20Report%2019022020.pdf"),
         ("Dublin City Council presentation on the scheme", "https://councilmeetings.dublincity.ie/documents/s20999/Presentation%20on%20River%20Poddle%20Flood%20Alleviation%20Scheme1.pdf"),
         ("Excavations.ie: Tenters Blackpitts, 2007 testing", "https://excavations.ie/?p=52698"),
         ("Excavations.ie: Tenters Blackpitts, 2016 monitoring", "https://excavations.ie/?p=52703")]),
]

RESOURCES = [
 ("Dublin City Council planning application 4423/19, 27–29 New Row South: flood risk assessment (JBA Consulting), engineering report (J.J. Campbell & Associates), city archaeologist and planner’s reports", "https://planning.agileapplications.ie/dublincity/"),
 ("An Bord Pleanála case 306725: River Poddle Flood Alleviation Scheme, EIAR and planning documents", "https://www.pleanala.ie/publicaccess/EIAR-NIS/306725/River%20Poddle%20FAS/Part%203%20EIAR/Volume%202%20EIAR/Part%20I/Volume%202%20Part%201%20-%20Main%20Report.pdf"),
 ("EIAR Chapter 11: archaeology, architecture and cultural heritage (306725)", "https://www.pleanala.ie/publicaccess/EIAR-NIS/306725/River%20Poddle%20FAS/Part%203%20EIAR/Volume%202%20EIAR/Part%20II/11.%20Archaeological%20Architectural%20Cultural%20Heritage.pdf"),
 ("Dublin City Council: presentation on the River Poddle Flood Alleviation Scheme", "https://councilmeetings.dublincity.ie/documents/s20999/Presentation%20on%20River%20Poddle%20Flood%20Alleviation%20Scheme1.pdf"),
 ("Excavations.ie: Tenters Blackpitts, Dublin 8 (2007 and 2016)", "https://excavations.ie/?p=52698"),
 ("UCD Digital Library: historic maps of Dublin", "https://digital.ucd.ie/view/ucdlib:40377#c0055-6-6.1"),
 ("South Dublin County Council: River Poddle Flood Alleviation Scheme", "https://consult.sdublincoco.ie/en/consultation/river-poddle-flood-alleviation-scheme-part-10-planning-submission"),
 ("Dublin.ie: The Poddle and Dublin’s hidden rivers", "https://dublin.ie/live/stories/the-poddle-and-dublins-hidden-rivers/"),
 ("Arran Henderson: The best Poddle river", "https://arranqhenderson.com/2017/07/18/the-best-poddle-river/"),
 ("Eastern CFRAM study: Poddle options report", "http://eastcfram.irish-surge-forecast.ie/wp-content/uploads/2011/10/IBE0600Rp0030_Poddle-Options-Report_F02.pdf"),
 ("Ask About Ireland: Griffith’s Valuation", "http://www.askaboutireland.ie/griffith-valuation/"),
 ("Geological Survey Ireland: River Poddle, County Geological Site report (Dublin City)", "https://gsi.geodata.gov.ie/downloads/Geoheritage/Reports/DC011_River_Poddle.pdf"),
 ("Wikipedia: River Poddle", "https://en.wikipedia.org/wiki/River_Poddle"),
 ("River Poddle Flood Alleviation Scheme", "https://www.poddlefas.ie/news"),
 ("Henry de Loundres, Archbishop of Dublin (grant of Timothan, 1216)", "https://www.biblicalcyclopedia.com/L/loundres-henry-de.html"),
 ("National Inventory of Architectural Heritage: Firhouse Weir, reg. no. 11215019", "https://www.buildingsofireland.ie/buildings-search/building/11215019/firhouse-weir-south-dublin-county"),
 ("Excavations.ie: The Weir, Firhouse, 2001 (Shane Delaney, IAC, licence 01E0858)", "https://excavations.ie/report/2001/Dublin/0006358/"),
 ("Weston St John Joyce, The Neighbourhood of Dublin (1912): the old city water supply", "https://www.chaptersofdublin.ie/Neighbourhood/chapter43.html"),
 ("William Handcock, The History and Antiquities of Tallaght: the River Dodder and the city weir", "https://www.chaptersofdublin.ie/Handcock/tallaght17.htm"),
 ("Crumlin and Walkinstown History Group: the Poddle River project and map", "https://poddle.crumlinwalkinstownhistory.ie/"),
 ("Crumlin Walkinstown History: Balrothery (Firhouse) Weir", "https://poddle.crumlinwalkinstownhistory.ie/location/firhouse-weir/"),
 ("Our Irish Heritage: Balrothery Weir, part of Tallaght’s waterways history", "https://www.ouririshheritage.org/content/archive/place/miscellaneous-place/balrothery-weir-on-the-dodder-part-of-tallaght-waterways-history"),
 ("South Dublin County Council: Firhouse Weir", "https://www.sdcc.ie/en/services/tourism/activities/sightseeing/firhouse-weir/"),
 ("William Handcock, The History and Antiquities of Tallaght: the church and Talbot’s Leap", "https://www.chaptersofdublin.ie/Handcock/tallaght3.htm"),
 ("South Dublin County Council: history of Tallaght", "https://sdcc.ie/en/services/planning-building-control/local-area-plans/tallaght-current/development-background/history-of-tallaght.pdf"),
 ("Library Ireland: Talbot family genealogy (Belgard)", "https://libraryireland.com/Pedigrees2/talbot.php"),
 ("Wikipedia: Henry Barry, 4th Baron Barry of Santry", "https://en.wikipedia.org/wiki/Henry_Barry,_4th_Baron_Barry_of_Santry"),
 ("St Patrick’s Cathedral: Saint Patrick and the cathedral", "https://www.stpatrickscathedral.ie/saint-patrick-and-the-cathedral/"),
 ("Wikipedia: St Patrick’s Cathedral, Dublin", "https://en.wikipedia.org/wiki/St_Patrick%27s_Cathedral,_Dublin"),
 ("Arran Henderson: origins of Saint Patrick’s Cathedral, the chapel on the island", "https://arranqhenderson.com/2014/01/12/origins-of-saint-patricks-cathedral-part-one-the-chapel-on-the-island-early-celtic-church/"),
]

# ---------------------------------------------------------------- templates
def esc(s): return html.escape(s, quote=True)

def para(p):
    return p if p.startswith("<") else f"<p>{esc(p)}</p>"

NAV = [("walk.html", "River walk"), ("map.html", "Map"), ("history.html", "History"), ("wildlife.html", "Wildlife"), ("river-data.html", "Live data"), ("media.html", "Media"), ("sources.html", "Sources"), ("shop.html", "Shop"), ("about.html", "About")]

def shell(slug, title, desc, body, active, image=None, article=False, noindex=False):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    url = BASE if slug == "index" else f"{BASE}{slug}.html"
    img = BASE + (f"img/{image}.jpg" if image else OG_DEFAULT)
    if not noindex:
        SITEMAP.append(slug)
    site = {"@type": "WebSite", "@id": BASE + "#site", "name": "The Poddle", "url": BASE, "inLanguage": "en-IE"}
    if article:
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": title.split(" · ")[0], "description": desc,
              "image": img, "url": url, "inLanguage": "en-IE", "isPartOf": site,
              "about": {"@type": "RiverBodyOfWater", "name": "River Poddle", "sameAs": "https://en.wikipedia.org/wiki/River_Poddle"}}
    elif slug == "index":
        ld = dict(site, **{"@context": "https://schema.org", "description": desc, "sameAs": [u for _, u in SOCIAL],
              "about": {"@type": "RiverBodyOfWater", "name": "River Poddle", "sameAs": "https://en.wikipedia.org/wiki/River_Poddle"}})
    else:
        ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": url, "inLanguage": "en-IE", "isPartOf": site}
    meta = (f'<link rel="canonical" href="{url}">\n'
            + ('<meta name="robots" content="noindex">\n' if noindex else '')
            + (f'<meta name="google-site-verification" content="{GOOGLE_VERIFY}">\n' if GOOGLE_VERIFY and slug == "index" else '')
            + (f'<meta name="msvalidate.01" content="{BING_VERIFY}">\n' if BING_VERIFY and slug == "index" else '')
            + f'<meta property="og:site_name" content="The Poddle">\n<meta property="og:locale" content="en_IE">\n'
            f'<meta property="og:type" content="{"article" if article else "website"}">\n'
            f'<meta property="og:title" content="{esc(title)}">\n<meta property="og:description" content="{esc(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{img}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    head = (f'<title>{esc(title)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{esc(desc)}">\n{meta}{FONTS}\n<link rel="stylesheet" href="site.css?v={ASSET_V}">\n'
            f'<link rel="icon" href="favicon.ico" sizes="32x32">\n<link rel="icon" href="favicon.svg" type="image/svg+xml">\n'
            f'<link rel="apple-touch-icon" href="apple-touch-icon.png">\n')
    page = (f'<a class="skip" href="#main">Skip to content</a>\n'
            f'<header class="top"><div class="wrap top-in"><a class="brand" href="index.html">The <span>Poddle</span></a>'
            f'<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav"><span class="bars" aria-hidden="true"></span><span class="lbl">Menu</span></button><nav id="site-nav" aria-label="Main">{nav}</nav></div></header>\n'
            f'<main id="main">{body}</main>\n'
            f'<footer class="foot"><div class="wrap foot-in"><p>The Poddle: a history of Dublin’s hidden river, from Tallaght to the Liffey.</p>'
            f'<p>Photographs and maps are credited where known. Third-party images are used for local-history purposes.</p>'
            f'<p class="social">Follow the river on ' + " and ".join(f'<a href="{u}" rel="noopener me">{n}</a>' for n, u in SOCIAL) + '.</p>'
            f'<p><a href="schools.html">For teachers</a> · <a href="privacy.html">Privacy</a></p></div></footer>\n'
            f'<script src="nav.js?v={ASSET_V}" defer></script>\n'
            + (f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n' if GOATCOUNTER else ''))
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

# Photo gallery for a stop page: one large photo with square thumbnails to pick from
# (gallery.js). Without JavaScript each thumbnail links to its full-size photo.
def gallery(photos, credit):
    first, cap0 = photos[0]
    thumbs = "".join(
        f'<li><a class="gal-thumb" href="img/{f}.jpg" data-cap="{esc(cap)}"{" aria-current=\"true\"" if i == 0 else ""}>'
        f'<img src="img/{f}-thumb.jpg" alt="{esc(cap)}" width="240" height="240" loading="lazy"></a></li>'
        for i, (f, cap) in enumerate(photos))
    return (f'<section class="gallery" aria-label="Photographs">'
            f'<figure class="gal-stage"><img src="img/{first}.jpg" alt="{esc(cap0)}" loading="lazy">'
            f'<figcaption><span class="gal-cap" aria-live="polite">{esc(cap0)}</span> {esc(credit)}</figcaption></figure>'
            f'<ul class="gal-thumbs">{thumbs}</ul></section>'
            f'<script src="gallery.js?v={ASSET_V}" defer></script>')

def slug_id(h):
    return re.sub(r'[^a-z0-9]+','-',h.lower()).strip('-')

def article(item, kicker, prev, nxt, back, top_nav=False):
    secs = "\n".join(f'<section id="{slug_id(h)}"><h2>{esc(h)}</h2>{"".join(para(p) for p in ps)}</section>' for h, ps in item["sections"])
    flag = f'<aside class="flag"><strong>To check</strong> {esc(item["flag"])}</aside>' if item.get("flag") else ""
    link = f'<p class="xlink"><a href="{item["link"][0]}.html">{esc(item["link"][1])} →</a></p>' if item.get("link") else ""
    if item.get("links"):
        link += '<section class="watch"><h2>Watch and read</h2><ul>' + "".join(f'<li><a href="{u}"{"" if u.endswith(".html") else " rel=\"noopener\""}>{esc(t)}</a></li>' for t, u in item["links"]) + '</ul></section>'
    if item.get("plan"):
        link += '<section class="watch plan"><h2>From the planning file</h2><p class="note">Facts from the flood scheme’s planning application and four local planning files.</p><ul>' + "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in item["plan"]) + '</ul></section>'
    brief = f'<aside class="brief"><strong>In brief</strong><p>{esc(item["brief"])}</p></aside>' if item.get("brief") else ""
    pn = '<nav class="pn" aria-label="Previous and next">'
    pn += f'<a class="prev" href="{prev[0]}.html"><span>Upstream</span>{esc(prev[1])}</a>' if prev else '<span></span>'
    pn += f'<a class="next" href="{nxt[0]}.html"><span>Downstream</span>{esc(nxt[1])}</a>' if nxt else '<span></span>'
    pn += '</nav>'
    top = pn.replace('class="pn"', 'class="pn pn-top"').replace('aria-label="Previous and next"', 'aria-label="Upstream and downstream"') if top_nav else ""
    return (f'<article class="wrap page">'
            f'<p class="crumb"><a href="{back[0]}">{esc(back[1])}</a></p>{top}'
            f'<header class="page-head"><p class="kicker">{kicker}</p><h1>{esc(item["name"])}</h1>'
            f'<p class="dek">{esc(item["teaser"])}</p></header>{brief}' +
            (f'<div class="page-grid"><div class="text">{flag}{secs}{link}</div>'
             f'<div class="media">{figures(item["images"], lead=True)}{gallery(item["gallery"], item["gallery_credit"]) if item.get("gallery") else ""}</div></div>' if item["images"] else
             f'<div class="page-grid solo"><div class="text">{flag}{secs}{link}</div></div>') + f'{pn}</article>')

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)

exec(open(os.path.join(OUT, "build_enrich.py"), encoding="utf-8").read())
# ---------------------------------------------------------------- pages
# River stops
for i, s in enumerate(STOPS):
    prev = (STOPS[i-1]["slug"], STOPS[i-1]["name"]) if i else None
    nxt = (STOPS[i+1]["slug"], STOPS[i+1]["name"]) if i + 1 < len(STOPS) else None
    kicker = f'Stop {i+1} of {len(STOPS)} <span>·</span> {esc(s["place"])}'
    body = article(s, kicker, prev, nxt, ("walk.html", "The river walk"), top_nav=True)
    write(f'{s["slug"]}.html', shell(s["slug"], f'{s["name"]} · {SITE}',
          f'{s["teaser"]} Stop {i+1} of {len(STOPS)} on the River Poddle walk, at {s["place"]}, Dublin.', body, "walk.html",
          image=s["images"][0][0] if s["images"] else None, article=True))

# History chapters (prev/next labels say Earlier/Later)
for i, h in enumerate(HISTORY):
    prev = (HISTORY[i-1]["slug"], HISTORY[i-1]["name"]) if i else None
    nxt = (HISTORY[i+1]["slug"], HISTORY[i+1]["name"]) if i + 1 < len(HISTORY) else None
    kicker = f'History <span>·</span> {esc(h["when"])}'
    body = article(h, kicker, prev, nxt, ("history.html", "History"))
    body = body.replace("<span>Upstream</span>", "<span>Earlier</span>").replace("<span>Downstream</span>", "<span>Later</span>")
    write(f'{h["slug"]}.html', shell(h["slug"], f'{h["name"]} · {SITE}',
          f'{h["teaser"]} {h["name"]}: a chapter in the history of the River Poddle, Dublin’s hidden river.', body, "history.html",
          image=h["images"][0][0] if h["images"] else None, article=True))

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


# Short school walks (pages written by build_walks.py); cards shown on the walk and teachers' pages.
SCHOOL_WALK_CARDS = [
 ("walk-tymon", "Tymon Park", "About 1.6 km · 1 to 1½ hours", "The lake, the flood gate and the wetland, on park paths away from traffic."),
 ("walk-kimmage-harolds-cross", "Kimmage to Harold’s Cross", "About 3 km · 2 to 2½ hours", "The old mill road, the Stone Boat and Mount Argus, to where the river dives under the Grand Canal."),
]
def walk_cards():
    return '<div class="walk-cards">' + "".join(
        f'<a class="walk-card" href="{h}.html"><em>School walk</em><strong>{esc(t)}</strong><span>{esc(m)}</span><span>{esc(d)}</span></a>'
        for h, t, m, d in SCHOOL_WALK_CARDS) + '</div>'
walk = "\n".join(stop_li(i, s) for i, s in enumerate(STOPS))
QUOTES = [
 ("From its sluice in Wood quay wall under Tom Devan’s office Poddle river hung out in fealty a tongue of liquid sewage.", "James Joyce, Ulysses"),
 ("…the chief supply of water not only for the inhabitants of the said city; but also for this majesties Castle of Dublin, and without which it would suffer exceeding great prejudice.", "An Act of Parliament, 1719, on the watercourse"),
 ("…tuck mills, in which urine, soap and other unwolsome materials are made use of, and diers of linnen and woolen cloath and yarn, and skinners dip, wash, scour and cleanse great quantities of died linnen and woolen cloath, yarn and skins in the said water-course", "An Act of Parliament, 1719"),
 ("…formed an immense sewer … putrefying the streets under which it passes…", "Warburton, Whitelaw and Walsh, History of the City of Dublin (1818), quoted by McEntee and Corcoran"),
 ("…so polluted by paper-making that it has become poisonous, and cattle and horses have died from drinking it.", "William Handcock, The History and Antiquities of Tallaght, on the Dodder"),
 ("It occasionally, however, bursts from its caverns and inundates the vicinity.", "Warburton, Whitelaw and Walsh, History of the City of Dublin (1818), quoted by McEntee and Corcoran"),
]
QUOTES_HTML = "\n".join(f'<figure class="q{" on" if i == 0 else ""}"><blockquote>“{esc(t)}”</blockquote><figcaption>{esc(a)}</figcaption></figure>' for i, (t, a) in enumerate(QUOTES))
HERO = os.environ.get("HERO", "water")
WAVES = ('<svg class="waves" aria-hidden="true" focusable="false" preserveAspectRatio="xMidYMax slice" viewBox="0 0 1440 320">'
 '<defs><pattern id="wv1" width="240" height="22" patternUnits="userSpaceOnUse"><path d="M0 11 C40 4 80 4 120 11 S200 18 240 11" fill="none" stroke="currentColor" stroke-width="2.2"/></pattern>'
 '<pattern id="wv2" width="320" height="34" patternUnits="userSpaceOnUse"><path d="M0 17 C55 8 105 8 160 17 S265 26 320 17" fill="none" stroke="currentColor" stroke-width="1.6"/></pattern>'
 '<linearGradient id="wvf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".55" stop-color="#fff" stop-opacity=".7"/><stop offset="1" stop-color="#fff"/></linearGradient>'
 '<mask id="wvm"><rect width="1440" height="320" fill="url(#wvf)"/></mask></defs>'
 '<g mask="url(#wvm)"><rect class="w1" width="1920" height="320" fill="url(#wv1)"/><rect class="w2" y="9" width="1920" height="320" fill="url(#wv2)"/></g></svg>')
PHOTO_BAND = ('<section class="hero-photo"><img src="img/hero-mount-argus.webp" alt="" width="880" height="500" fetchpriority="high">'
 '<div class="wrap hp-in"><p class="kicker">Tallaght to Wellington Quay</p><h1>The river that named Dublin</h1></div>'
 '<p class="hp-cap">The Poddle at Mount Argus</p></section>')
home = f'''{PHOTO_BAND if HERO == "photo" else ""}
<section class="hero{" water" if HERO == "water" else ""}{" after-photo" if HERO == "photo" else ""}">{WAVES if HERO == "water" else ""}<div class="wrap hero-in">
 <div class="hero-text">
{"" if HERO == "photo" else '''  <p class="kicker">Tallaght to Wellington Quay</p>
  <h1>The river that named Dublin</h1>'''}
  <p class="lede">The Poddle is the most important watercourse in Dublin city, it provided its water, its defensive moat and powered its mills. It gave the city its name.</p>
  <p class="lede">Poddle.ie traces the course of its history from source to sea, as it defined the Dublin we know today.</p>
  <p class="cta home-cta"><a class="btn" href="walk.html">Walk the river</a><a class="btn" href="history.html">Read the history</a><a class="btn" href="map.html">Open the map</a><a class="btn" href="shop.html">Resources</a></p>
 </div>
 <figure class="hero-fig"><img src="img/cover-painting.jpg" alt="Painting of a heart shape in river blue" loading="eager"></figure>
</div></section>
<section class="quotes" aria-label="Quotations about the Poddle"><div class="wrap"><div class="q-stage" id="quotes">
{QUOTES_HTML}
</div></div></section>
<script src="quotes.js?v={ASSET_V}"></script>
'''

walk_page = f'''<div class="wrap page"><header class="page-head"><p class="kicker">The river walk</p><h1>Source to sea, stop by stop</h1>
<p class="dek">The Poddle’s course has been created and recreated by nature and by people over the centuries. Here we plot it as a single line, above and below ground, as best we can. The <a href="map.html">map</a> shows the same stops on today’s streets, and <a href="planning-record.html">what the planning files say</a> adds some of the most interesting facts.</p></header>
<div class="walk-grid"><ol class="line">{walk}</ol>
<div class="walk-maps">{figures([("1848-os-map-small", "Ordnance Survey map of Dublin, 1848"), ("poddle-catchment", "The Poddle catchment, from Tallaght north-east to the Liffey")])}</div></div>
<section class="school-walks" id="school-walks"><h2>Shorter walks for schools</h2>
<p>Two class-sized walks on stretches where the river is out in the open, each with things to look for, activities and safety notes for teachers.</p>{walk_cards()}</section></div>'''
write("walk.html", shell("walk", f"The river walk · {SITE}", "Walk the River Poddle in sixteen stops, from its source in Tallaght through Kimmage, Harold’s Cross and the Liberties to the Liffey at Wellington Quay.", walk_page, "walk.html"))
write("index.html", shell("index", "The River Poddle: Dublin’s hidden river, from Tallaght to the Liffey", "The River Poddle gave Dublin its name. Follow Dublin’s hidden river from Tallaght to the Liffey: its history, mills, floods, a sixteen-stop river walk and an interactive map.", home, "index.html"))

# History index: one large map that cross-fades through the four periods (maps.js),
# with dated thumbnails to pick one. The Poddle is baked in light blue by scripts/poddle_highlight.py.
def map_show(maps):
    # maps: (image base name, thumbnail label, caption, highlighted?)
    def alt(cap, hl): return f"{cap}, with the River Poddle highlighted in light blue" if hl else cap
    slides = "".join(
        f'<figure class="ms-slide{" on" if i == 0 else ""}" id="ms-{i}" data-cap="{esc(cap)}"{"" if i == 0 else " aria-hidden=\"true\""}>'
        f'<img src="img/{f}.jpg" alt="{esc(alt(cap, hl))}" width="1600" height="1145" loading="{"eager" if i == 0 else "lazy"}"></figure>'
        for i, (f, lab, cap, hl) in enumerate(maps))
    thumbs = "".join(
        f'<li><a class="ms-thumb" href="img/{f}.jpg" data-i="{i}"{" aria-current=\"true\"" if i == 0 else ""}>'
        f'<img src="img/{f}-thumb.jpg" alt="" width="320" height="229" loading="lazy"><span>{esc(lab)}</span></a></li>'
        for i, (f, lab, cap, hl) in enumerate(maps))
    return (f'<section class="map-show" aria-label="Maps of Dublin from c. 840 to 1904">'
            f'<div class="ms-stage">{slides}</div>'
            f'<div class="ms-bar"><p class="ms-cap" aria-live="polite">{esc(maps[0][2])}</p>'
            f'<button class="ms-play" type="button" hidden aria-pressed="false">Pause</button></div>'
            f'<ol class="ms-thumbs">{thumbs}</ol>'
            f'<p class="ms-note">On the four atlas maps the River Poddle is picked out in light blue (Irish Historic Towns Atlas, 2002). '
            f'John Speed’s “Dubline”, surveyed 1610, shown from a 19th-century reprint (British Library, via Wikimedia Commons, public domain): the Poddle comes in at the bottom, by St Patrick’s (63), and runs north to the Castle (23). '
            f'Leonard R. Strangways, “The Walls of Dublin”, 1904 (via Wikimedia Commons, public domain): south is at the top, and the River Poddle is marked near Pole Gate, south of the Castle.</p></section>'
            f'<script src="maps.js?v={ASSET_V}" defer></script>')

hist = f'''<div class="wrap page"><header class="page-head"><p class="kicker">History</p><h1>How the Poddle shaped Dublin</h1>
<p class="dek">From the black pool of Dubh Linn to the flood scheme being built today. This is a friendly telling, drawn from many sources that sometimes disagree; where the record is thin we say so, and corrections are always welcome. Some of the most interesting facts come from <a href="planning-record.html">the planning files</a>, linked from the chapters below.</p></header>
{map_show([("dublin-840-poddle","c. 840","Dublin c. 840",True),("dublin-1000-poddle","c. 1000","Dublin c. 1000",True),("dublin-1170-poddle","c. 1170","Dublin c. 1170",True),("dublin-1370-poddle","c. 1300","Dublin c. 1300",True),("dublin-1610-speed","1610","Dublin in 1610, by John Speed",False),("dublin-1904-strangways","1904","The walls of medieval Dublin, by Leonard Strangways, 1904",False)])}
<ol class="tl big">{"".join(f'<li><a href="{h["slug"]}.html"><span class="when">{esc(h["when"])}</span><strong>{esc(h["name"])}</strong><span>{esc(h["teaser"])}</span></a></li>' for h in HISTORY)}</ol></div>'''
write("history.html", shell("history", f"History · {SITE}", "How the River Poddle shaped Dublin, from the black pool of Dubh Linn to medieval diversions, mills, the 1719 Act and today’s flood scheme.", hist, "history.html"))

# Wildlife page photos: Wikimedia Commons, converted to black and white (img/wild-*.jpg).
WILD_PHOTOS = {
 "tymon-2": ("The Poddle at Poddle Park, Kimmage", "O’Dea", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:River_Poddle_at_Poddle_Park.jpg", "https://creativecommons.org/licenses/by-sa/4.0"),
 "tymon-1": ("The waterfall crossing between the lakes in Tymon Park", "Alan James", "CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:The_waterfall_crossing_-_geograph.org.uk_-_1821668.jpg", "https://creativecommons.org/licenses/by-sa/2.0"),
 "stickleback": ("A male three-spined stickleback", "Gilles San Martin", "CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:Gasterosteus_aculeatus_-_Epinoche_-_Three-spined_stickleback.jpg", "https://creativecommons.org/licenses/by-sa/2.0"),
 "otter": ("An otter (photographed in Ukraine)", "Byrdyak", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:%D0%92%D0%B8%D0%B4%D1%80%D0%B0.jpg", "https://creativecommons.org/licenses/by-sa/4.0"),
 "pipistrelle": ("A common pipistrelle (photographed in Belgium)", "Gilles San Martin", "CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:Pipistrellus_pipistrellus_(5933130195).jpg", "https://creativecommons.org/licenses/by-sa/2.0"),
 "swan": ("Mute swans and cygnets (photographed in Oxford)", "Charles J. Sharp", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Mute_swans_(Cygnus_olor)_and_cygnets.jpg", "https://creativecommons.org/licenses/by-sa/4.0"),
 "heron": ("A grey heron (photographed in Co. Cork)", "Ken Billington", "CC BY-SA 3.0", "https://commons.wikimedia.org/wiki/File:Grey_Heron_(Ardea_cinerea)_(3).jpg", "https://creativecommons.org/licenses/by-sa/3.0"),
 "egret": ("A little egret (photographed in Co. Cork)", "Ken Billington", "CC BY-SA 3.0", "https://commons.wikimedia.org/wiki/File:Little_Egret_(Egretta_garzetta)_(4).jpg", "https://creativecommons.org/licenses/by-sa/3.0"),
 "grey-wagtail": ("A grey wagtail", "Charles J. Sharp", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Grey_wagtail_(Motacilla_cinerea_cinerea).jpg", "https://creativecommons.org/licenses/by-sa/4.0"),
 "flowering-rush": ("Flowering rush", "Michel Langeveld", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Butomus_umbellatus_140872752.jpg", "https://creativecommons.org/licenses/by-sa/4.0"),
 "helleborine": ("Broad-leaved helleborine", "Gllawm", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Epipactis_helleborine_(Paizay-le-Chapt)_14072016_01.jpg", "https://creativecommons.org/licenses/by-sa/4.0"),
}
def wfig(*keys):
    figs = "".join(f'<figure class="fig"><img src="img/wild-{k}.jpg" alt="{esc(WILD_PHOTOS[k][0])}" loading="lazy">'
                   f'<figcaption>{esc(WILD_PHOTOS[k][0])}. Photo: <a href="{WILD_PHOTOS[k][3]}" rel="noopener">{esc(WILD_PHOTOS[k][1])}</a>, '
                   f'<a href="{WILD_PHOTOS[k][4]}" rel="noopener">{WILD_PHOTOS[k][2]}</a></figcaption></figure>' for k in keys)
    return f'<div class="fig-grid">{figs}</div>' if len(keys) > 1 else figs

# Sources
src = f'''<div class="wrap page narrow"><header class="page-head"><p class="kicker">Sources</p><h1>Further reading</h1>
<p class="dek">Maps, reports and articles used in putting this site together.</p></header>
<ul class="links">{"".join(f'<li><a href="{u}" rel="noopener">{esc(t)}</a></li>' for t, u in RESOURCES)}</ul>
<section><h2>Photo credits</h2><p>Photographs from Wikimedia Commons, shown in black and white. Licences as stated; adapted (converted to black and white and resized).</p><ul class="links plain">
<li><a href="https://commons.wikimedia.org/wiki/File:County_Dublin_-_Firhouse_Weir_-_20210110130610.jpg" rel="noopener">Firhouse Weir, 2021</a>: Tdr112, CC BY-SA 4.0 (<a href="https://creativecommons.org/licenses/by-sa/4.0" rel="noopener">licence</a>)</li>
<li><a href="https://commons.wikimedia.org/wiki/File:FootbridgeAtFirhouse.JPG" rel="noopener">Footbridge at Firhouse</a>: Deitel55, CC BY-SA 3.0 (<a href="https://creativecommons.org/licenses/by-sa/3.0" rel="noopener">licence</a>)</li>
<li><a href="https://commons.wikimedia.org/wiki/File:La_cath%C3%A9drale_Saint-Patrick_(vue_depuis_le_St_Patrick%27s_Park).jpg" rel="noopener">St Patrick’s Cathedral from the park</a>: Clara.munecas, CC BY-SA 4.0 (<a href="https://creativecommons.org/licenses/by-sa/4.0" rel="noopener">licence</a>)</li>
<li><a href="https://commons.wikimedia.org/wiki/File:Dublin_St._Patrick%27s_Cathedral_West_Fa%C3%A7ade_at_Patrick_Street_2012_09_26.jpg" rel="noopener">West front and Minot’s Tower</a>: Andreas F. Borchert, CC BY-SA 4.0 (<a href="https://creativecommons.org/licenses/by-sa/4.0" rel="noopener">licence</a>)</li>
<li><a href="https://commons.wikimedia.org/wiki/File:St_Patrick%27s_Cathedral_Nave_2,_Dublin,_Ireland_-_Diliff.jpg" rel="noopener">The nave</a>: Diliff, CC BY-SA 3.0 (<a href="https://creativecommons.org/licenses/by-sa/3.0" rel="noopener">licence</a>)</li>
<li><a href="https://commons.wikimedia.org/wiki/File:St._Patrick%27s_Cathedral_Celtic_cross.jpg" rel="noopener">The well stone</a>: Wknight94, CC BY-SA 3.0 (<a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="noopener">licence</a>)</li>
<li><a href="https://commons.wikimedia.org/wiki/File:Location_of_the_Well_of_Saint_Patrick.JPG" rel="noopener">The well plaque</a>: Archaeomoonwalker, CC0 (<a href="https://creativecommons.org/publicdomain/zero/1.0/deed.en" rel="noopener">licence</a>)</li>
<li><a href="https://commons.wikimedia.org/wiki/File:Saint_Patricks_Cathedral_%E2%80%93_Pre_Guinness_Restoration.jpg" rel="noopener">The cathedral in 1814</a>: James Whitelaw, Public domain</li>
<li><a href="https://commons.wikimedia.org/wiki/File:St_Patrick%27s_Cathedral,_Dublin_-_WL.jpg" rel="noopener">Lawrence Collection photograph</a>: William Lawrence (Lawrence Collection), Public domain</li>
{"".join(f'<li><a href="{v[3]}" rel="noopener">{esc(v[0])}</a>: {esc(v[1])}, {v[2]} (<a href="{v[4]}" rel="noopener">licence</a>)</li>' for v in WILD_PHOTOS.values())}</ul></section>
<section><h2>Printed sources</h2><ul class="links plain">
<li>Rev. Myles V. Ronan, “The Poddle River and its Branches”, Journal of the Royal Society of Antiquaries of Ireland, 6th series, vol. 17, no. 1 (1927), pp. 39–46</li>
<li>D. McEntee and M. Corcoran, The Rivers Dodder and Poddle: Mills, Storms, Droughts and the Public Water Supply (Dublin City Council), chapters 5, 11 and 19</li>
<li>Sister Ann Dominica Fitzgerald O.P., “Down the Old Poddle”, in Elgy Gillespie (ed.), The Liberties of Dublin (E. and T. O’Brien, 1973), pp. 24–32</li>
<li>Dublin Corporation, Reports and Printed Documents, 1901, Report No. 129, “Report of the Paving Committee re Covering of the Poddle River at Donore Avenue”, pp. 301–316 (Dublin City Library and Archive)</li>
<li>J. Warburton, J. Whitelaw and R. Walsh, History of the City of Dublin (1818), as quoted by McEntee and Corcoran</li>
<li>Robert Mallet, Report on the proposed formation of reservoirs on the River Dodder (1844), as quoted by McEntee and Corcoran</li>
<li>Dublin Corporation Waterworks Department, Ordnance Survey sheets with water mains (South Side and South County Dublin, WW/12/17–19), Dublin City Library and Archive</li>
<li>Dublin Corporation (Dublin City Council) minutes, 1901–1987, from the index entries for the Poddle supplied by Dublin City Library and Archive, 2026</li>
<li>Greater Dublin Strategic Drainage Study (2005)</li>
<li>H. F. Berry, “The water supply of ancient Dublin”, Journal of the Royal Society of Antiquaries of Ireland 21 (1891), pp. 557–73</li>
<li>H. F. Berry, “Notes on an unpublished MS inquisition (AD 1258) relating to the Dublin city watercourse”, Proceedings of the Royal Irish Academy 24 (1902–4), pp. 39–46</li>
<li>Weston St John Joyce, The Neighbourhood of Dublin (1912; 1988 edition), pp. 452–3</li>
<li>William Domville Handcock, The History and Antiquities of Tallaght (1877; 2nd edition 1899)</li>
<li>J. Hegarty, “The Dodder Valley”, Dublin Historical Record 2, no. 2 (1939), p. 62</li>
<li>B. Mac Giolla Phádraig, History of Terenure (1954)</li>
<li>Simpson (1997), as cited in the flood scheme’s EIAR Chapter 11, pp. 22–5</li>
<li>Joseph W. Doyle, Ten Dozen Waters: The Rivers and Streams of County Dublin (2013; 2018 edition), as summarised in Wikipedia’s River Poddle article</li>
<li>Poddle Flood Alleviation Scheme, Environmental Impact Assessment Report, Non-Technical Summary</li>
</ul></section>
<figure class="fig"><img src="img/journal-article.jpg" alt="Cover of the Journal of the Royal Society of Antiquaries of Ireland" loading="lazy"><figcaption>Journal of the Royal Society of Antiquaries of Ireland, 1927</figcaption></figure>
</div>'''
write("sources.html", shell("sources", f"Sources · {SITE}", "Maps, reports and articles about the River Poddle.", src, "sources.html"))

# Wildlife: from the flood scheme's ecology surveys (2018-2022). Badger sett locations are
# withheld in the reports on purpose, so never add them here.
WILDLIFE = [
 ("Where the wildlife is", [
   wfig("tymon-2", "tymon-1"),
   "Almost everything that has been recorded lives on the open stretch of the river, through Tymon North, Tymon Park, Whitehall Park and Ravensdale Park. From Kimmage down, the Poddle runs mostly in walls and culverts, and very little has been found there.",
   "Most of what we know comes from the ecologists who surveyed the river for the River Poddle Flood Alleviation Scheme between 2018 and 2022. Their reports are in the scheme’s planning file, and they are listed at the bottom of this page."]),
 ("The water", [
   "Like most urban watercourses, the Poddle suffers from pollution. When the Environmental Protection Agency sampled it at Priory Road, Kimmage, in 2007, it scored Q3 on the EPA’s scale, which means moderately polluted, and samples taken at four sites in 2020 gave the same score. The small creatures living in the riverbed were the hardier kinds, such as leeches, midge larvae, water hoglice and small snails, rather than the mayflies and stoneflies of the cleanest mountain streams.",
   "The city and county councils are working hard to address that. As part of the flood scheme, an integrated constructed wetland is being created in Tymon Park: a series of planted ponds that cleans the water naturally as it passes through, with the aim of bringing it up to a “good” standard.",
   "Pollution is an old problem for the Poddle. In the 18th century the mills along its banks had already turned it into what Whitelaw and Walsh called “an immense sewer”, and there are accounts of cattle and horses dying after drinking from it."]),
 ("Fish", [
   wfig("stickleback"),
   "The only fish caught when the river was electrofished in August and September 2020 was the three-spined stickleback. There were hundreds at Whitehall Park, but only five to ten at each of the other sites. Inland Fisheries Ireland says minnows live in the river too.",
   "There are no trout, salmon or eels. Inland Fisheries Ireland told the engineers that the Poddle is “not a salmonid river”. The 2020 survey found that the gravel beds should suit young brown trout and eels, and said their absence “suggests that there are barriers to fish movement”: the culverts, and the syphon that carries the river under the Grand Canal."]),
 ("Otters", [
   wfig("otter"),
   "The otter is the river’s good-news story. In the surveys of 2018 and 2019, the ecologists found “no otter holts, nor any other evidence of otter”. Then in September 2020 a holt was found in Tymon North.",
   "A survey in February 2021 recorded 11 signs of otters, including droppings (called spraints) and two holts, one in use. Fish scales from roach were found near Kimmage Cross Roads, possibly left by an otter, but no other signs were found below Tymon North. The ecologists described it as “a natural colonisation of the river by otters”.",
   "The Poddle is still a minor otter river. A study of Dublin’s rivers for Dublin City Council found many more signs on the Dodder and the Tolka, and said the Poddle and the Camac “appeared to support far fewer otters”."]),
 ("Bats, badgers and other mammals", [
   wfig("pipistrelle"),
   "Bats feed along the river and over the Tymon lakes. Surveys in 2018 and 2019 recorded the common pipistrelle, which was active all night, the soprano pipistrelle, including at Mount Argus, and Leisler’s bat, Ireland’s largest. A bat that was probably a Daubenton’s, which hunts insects just above the water, was also picked up over Tymon. Most activity was over the reedbeds at the edge of Tymon Lake. Old trees in Mount Argus Park and the grounds of Kimmage Manor could make good roosts.",
   "Badgers have setts in Tymon North. Their exact location is kept out of the reports to protect them.",
   "Hedgehogs, pygmy shrews and stoats have been recorded in the surrounding area and may use the river banks, though none were seen in the surveys."]),
 ("Birds", [
   wfig("swan"),
   "The Tymon lakes are the best place for birds on the river. Ecologists counted 19 kinds of waterbird there in early 2018, and 2,616 birds over eight visits in the winter of 2021–22. The commonest are black-headed gulls, common gulls, herring gulls, mallard, moorhens, coots, mute swans, tufted ducks, little grebes and teal. Wigeon, shoveler and snipe have also been seen.",
   "Mute swans, mallard, coots and moorhens nest around the ponds. In April 2022 a swan was sitting on a nest in the reedbed at the south-east corner of Tymon Lake. The flood scheme’s plans include floating nesting platforms for the lake.",
   "Grey herons and little egrets fish in the river and the ponds, and grey wagtails feed along the stream. A water rail was reported in the Tymon reedbeds in the winter of 2021–22, a new record that the ecologists rated of county importance. No kingfishers or dippers were seen, though both live on the Dodder nearby.",
   wfig("heron", "egret", "grey-wagtail"),
   '<figure class="fig"><img src="img/wild-tymon-heron.jpg" alt="A grey heron standing at the edge of the lake in Tymon Park, west of the M50, among autumn reflections" loading="lazy"><figcaption>A grey heron (right, at the water’s edge) on the lake in Tymon Park, west of the M50, November 2026. Photo: poddle.ie.</figcaption></figure>',
   "Tymon Park used to be an important feeding ground for Brent geese, which fly in from Arctic Canada for the winter: about 1,200 were reported in 2008 and 700 in 2009. Disturbance by dogs has largely stopped this, and only a few have been seen since. An Taisce argued that the flood scheme’s report played them down."]),
 ("Frogs, newts and insects", [
   "Common frogs and smooth newts probably breed in the ponds at Tymon Park and Mount Argus, although the surveys did not find any. Dragonflies, including the brown rod dragonfly, hunt over the Tymon lakes, and the meadows and reedbeds hold a wide variety of insects."]),
 ("Plants", [
   wfig("flowering-rush", "helleborine"),
   "In the river itself grow watercress, spiked water-milfoil, pink water-speedwell, pondweed and green algae. Around Tymon Lake there are reedbeds of common reed and bulrush, with yellow iris, great willowherb, meadowsweet and purple-loosestrife. The meadow north and east of the lake is rich in wildflowers, including yellow-rattle, selfheal and what is probably a common spotted-orchid.",
   "Three rare plants have been found. Flowering rush, which is rare in Dublin, grows in the river below Tymon Lake, and the council has planted more at the Limekiln lakes. Galingale, a tall sedge, grows around Tymon Lake, in what may be its only wild site in Ireland, though it was probably brought in. And four stems of broad-leaved helleborine, a wild orchid, were found on bare ground near Fortfield Road.",
   "The woods of Tymon Park are mostly beech, poplar, ash, horse chestnut, willow, maple, sycamore and birch, with wet willow and alder woodland around some of the ponds.",
   "Three invasive plants have been recorded: giant rhubarb at Tymon Lake, which has since been removed, a small patch of Japanese knotweed in the north-west of Tymon Park, and Nuttall’s waterweed in the river channel."])]
WILDLIFE_SRC = [
 ("Flood scheme EIAR, Chapter 7: Biodiversity (NM Ecology, February 2020)", "https://www.pleanala.ie/publicaccess/EIAR-NIS/306725/River%20Poddle%20FAS/Part%203%20EIAR/Volume%202%20EIAR/Part%20II/7.%20Biodiversity.pdf"),
 ("Electrofishing survey and Q-value analysis (AQUAFACT, 2020)", "https://www.poddlefas.ie/_fileupload/Appendix%206%20Electrofishing%20Survey%20&%20Q%20Value%20Analysis/Appendix%206_%20River%20Poddle%20Electrofishing%20Report%20&%20Q%20Value%20Analysis.pdf"),
 ("Winter bird and mammal surveys, including the 2021 otter survey (NM Ecology, April 2022)", "https://www.poddlefas.ie/_fileupload/RFI%20Attachment%20no_%202%20Wintering%20Birds%20&%20Mammals%20Report.pdf"),
 ("The Echo: study of Dublin’s waterways finds 200 signs of otters", "https://www.echo.ie/?p=119981"),
 ("Ask About Ireland: wildlife of the lakes in South Dublin’s parks", "https://askaboutireland.ie/reading-room/environment-geography/flora-fauna/wildlife-of-the-parks-of-/lakes-and-lakesides"),
 ("Dublin Inquirer: residents debate the environmental impact of the flood scheme (March 2020)", "https://www.dublininquirer.com/residents-debate-environmental-impact-of-a-plan-to-build-flood-defences-on-the-river-poddle/"),
]
wild = (f'<article class="wrap page">'
  f'<header class="page-head"><p class="kicker">Nature</p><h1>Wildlife of the Poddle</h1>'
  f'<p class="dek">Otters, bats, herons and a rare orchid: what lives along Dublin’s hidden river.</p></header>'
  f'<aside class="brief"><strong>In brief</strong><p>Like most urban watercourses, the Poddle has suffered from pollution, and the councils are working hard to improve it. Sticklebacks and minnows live in the river, otters have moved into its upper reaches since 2020, bats hunt along it, and the lakes at Tymon Park hold swans, herons, egrets and rare plants.</p></aside>'
  f'<div class="page-grid solo"><div class="text">'
  + "\n".join(f'<section id="{slug_id(h)}"><h2>{esc(h)}</h2>{"".join(para(p) for p in ps)}</section>' for h, ps in WILDLIFE)
  + '<section class="watch"><h2>Sources</h2><p class="note">These surveys were done for the River Poddle Flood Alleviation Scheme, except where noted. Records are of what the surveyors saw on the days they visited, so other animals and plants may well be there.</p><ul>'
  + "".join(f'<li><a href="{u}" rel="noopener">{esc(t)}</a></li>' for t, u in WILDLIFE_SRC)
  + '</ul></section>'
  f'<p class="xlink"><a href="tymon.html">Walk the river: Tymon Park →</a></p></div></div></article>')
write("wildlife.html", shell("wildlife", f"Wildlife of the Poddle · {SITE}",
      "Otters, bats, herons, sticklebacks and rare plants: what lives along the River Poddle in Dublin, from the flood scheme’s ecology surveys.",
      wild, "wildlife.html", article=True))

# Media
MEDIA = [
 ("Video", "Dublin’s Hidden Rivers", "A short film on the Poddle and the city’s other buried rivers.", "https://www.youtube.com/watch?v=K5ygnHSLKLY"),
 ("Video", "River Poddle in Dublin’s city centre, previously unseen", "Footage from inside the culverted river in the city centre.", "https://www.youtube.com/watch?v=SLwzXheosOI"),
 ("Video", "The Poddle, by Gerard O’Kelly (1975)", "A 1975 film following the river from Fettercairn to Wellington Quay, with the Dubh Linn, the 1244 diversion and Red Hugh O’Donnell’s escape. Shared by the Harold’s Cross Festival.", "https://www.youtube.com/watch?v=42T1AVpYQTM"),
 ("Video", "Poddle River, Dublin: part 1, by Noel Heenan", "The first of two short films on the river posted by Noel Heenan.", "https://www.youtube.com/watch?v=xHRS5iWKziw"),
 ("Video", "Poddle River, Dublin: part 2, by Noel Heenan", "The second part of Noel Heenan’s films on the river.", "https://www.youtube.com/watch?v=-8o9vQx_90E"),
 ("Video", "Tymon Park’s esker", "The Echo, on the glacial ridge beside Tymon Castle.", "https://youtu.be/-oMSnnBhdbI"),
 ("Video", "Kimmage Manor from the air", "Drone footage of the manor where the river is piped under the buildings.", "https://youtu.be/e3bgOMpW9Z4"),
 ("Video", "Medieval Dublin Online: Wood Quay", "How the Viking and medieval town grew beside the Poddle and the Liffey.", "https://vimeo.com/147322671"),
 ("Television", "Go Outside and Play: Dublin’s Secret River (RTÉ, 2023)", "Carl Mullan follows his local river, the Poddle, from source to mouth.", "https://www.youtube.com/watch?v=yrl9EXPO2ko"),
 ("Television", "Cities of the Underworld: Viking Underground (History Channel, 2008)", "Don Wildman goes beneath the Viking towns of Europe, including Dublin.", "https://www.youtube.com/watch?v=ue_KBxfdI8Q"),
 ("Television", "The Liffey, episode 1: Protection and Defence (RTÉ, 2022)", "Dublin City Council’s David Green takes the cameras underground on the Poddle.", "https://presspack.rte.ie/2022/05/15/the-liffey-brand-new-series"),
 ("Article", "Underground Dublin: a pilgrimage through an ancient tunnel network", "Patrick Freyne in The Irish Times, 2021, walking the Poddle beneath the city.", "https://www.irishtimes.com/culture/heritage/underground-dublin-a-pilgrimage-through-an-ancient-tunnel-network-1.4662108"),
 ("Article", "The Ship Street archaeological dig", "RTÉ News, June 2020, on the ravine found south of Dublin Castle.", "https://www.rte.ie/news/dublin/2020/0609/1146385-archaeological-dig/"),
 ("Photographs", "Hidden Dublin: the River Poddle", "Photographs of the river, from the culverts under Dublin Castle and Temple Bar to Blackpitts, Donore Avenue and the grating at its outfall.", "https://www.hidden-dublin.com/poddle/river_poddle.html"),
 ("Writing", "Undercurrents, by Amanda Bell", "Haiku and prose on Irish rivers, with a section on the Poddle.", "https://www.littletoller.co.uk/?p=12682"),
]
med = '<div class="wrap page"><header class="page-head"><p class="kicker">Media</p><h1>Watch, read and listen</h1><p class="dek">Films, television and writing about the Poddle. Links open on other sites.</p></header><ol class="media-list">'
med += "".join(f'<li><a href="{u}" target="_blank" rel="noopener noreferrer"><span class="mtype">{esc(k)}</span><strong>{esc(t)}</strong><span>{esc(d)}</span></a></li>' for k, t, d, u in MEDIA)
med += '</ol>'
# Clips grouped under their own heading (Mark, 5 Nov 2026)
BANK_TUNNEL = [
 ("Television", "AIB bank robbery foiled (RTÉ News, 1985)", "Gardaí examine the tunnel dug towards the AIB on Dame Street, where the alarm foiled the raid.", "https://www.rte.ie/archives/collections/news/21193044-aib-bank-robbery-foiled/"),
 ("Article", "Bungling bank robbers tunnel into ladies’ room (UPI, 10 April 1985)", "The gang dug 25 yards from beside the Castle wall, crawled through sewers and cut into a basement washroom.", "https://www.upi.com/Archives/1985/04/10/Bungling-bank-robbers-tunnel-into-ladies-room/6614481957200/"),
 ("Video", "Dublin’s Hidden Rivers: the wall the robbers broke through", "The film goes into the culvert and shows the wall the gang tried to get through, from about 4:06.", "https://www.youtube.com/watch?v=K5ygnHSLKLY&t=246s"),
 ("Podcast", "Did you know about Dublin’s bank robbery? (98FM)", "A short episode on the Easter 1985 attempt to reach the bank through the city’s tunnels and sewers.", "https://www.98fm.com/podcasts/98fms-did-you-know/did-you-know-about-dublins-bank-robbery"),
]
med += ('<section class="media-group"><h2>The Dame Street bank tunnel, 1985</h2>'
        '<p>Over the Easter weekend of 1985 a gang tunnelled from waste ground beside the Dublin Castle wall, crawled through the sewers under Dame Street and cut through a basement wall of the AIB branch. It was the ladies’ toilet. The alarm went off and they fled empty-handed. The news reports of the time don’t name the Poddle, but the river runs under this corner of Dame Street, and the film Dublin’s Hidden Rivers shows the wall in the culvert that the gang tried to use.</p>'
        '<ol class="media-list">')
med += "".join(f'<li><a href="{u}" target="_blank" rel="noopener noreferrer"><span class="mtype">{esc(k)}</span><strong>{esc(t)}</strong><span>{esc(d)}</span></a></li>' for k, t, d, u in BANK_TUNNEL)
med += '</ol></section></div>'
write("media.html", shell("media", f"Media · {SITE}", "Films, television and writing about the River Poddle.", med, "media.html"))

# About
about = f'''<div class="wrap page narrow"><header class="page-head"><p class="kicker">About</p><h1>About this site</h1>
<p class="dek">A personal project tracing the Poddle from Tallaght to the Liffey.</p></header>
<section><p>As an engineer with an interest in both history and how things work, the Poddle has long been a fascination of mine. I hope you have enjoyed these pages, and if you get a chance to <a href="shop.html">support the page</a> to keep it alive and free, that would be amazing.</p></section>
<section id="contact"><h2>Get in touch</h2>
<ul>
<li>We would love to hear more interesting facts and stories about the Poddle, so please share them.</li>
<li>We are available to give talks and share what we know, so please reach out if you would like to organise one. Teachers, there are free class ideas on the <a href="schools.html">teachers’ page</a>.</li>
<li>There is a great deal of information about the Poddle, and much of it conflicts. If you spot something wrong, please let us know.</li>
</ul>
<form class="contact" action="https://formsubmit.co/hello@poddle.ie" method="POST">
<input type="hidden" name="_subject" value="Message from the Poddle website">
<input type="hidden" name="_next" value="https://poddle.ie/thanks.html">
<input type="hidden" name="_template" value="table">
<input type="text" name="_honey" tabindex="-1" autocomplete="off" style="display:none">
<p><label for="c-name">Your name</label><input id="c-name" name="name" type="text" required autocomplete="name"></p>
<p><label for="c-email">Your email</label><input id="c-email" name="email" type="email" required autocomplete="email"></p>
<p><label for="c-msg">Your message</label><textarea id="c-msg" name="message" rows="6" required></textarea></p>
<p><button type="submit">Send message</button></p>
</form></section>
</div>'''
write("about.html", shell("about", f"About · {SITE}", "About poddle.ie, a free local-history site about the River Poddle, Dublin’s hidden river. Send corrections, memories and photographs.", about, "about.html"))
write("thanks.html", shell("thanks", f"Thank you · {SITE}", "Message sent.", '<div class="wrap page narrow"><header class="page-head"><h1>Thank you</h1><p class="dek">Your message has been sent. We will be in touch if a reply is needed.</p></header><p><a href="index.html">Back to the home page</a></p></div>', "about.html", noindex=True))

# ---------------------------------------------------------------- teachers and privacy
# For teachers: free classroom use of the site, pages suggested by class level.
# Linked from the footer, the shop and the schools email (poddle.ie/schools).
SCHOOL_LEVELS = [
 ("1st and 2nd class", "Where is the river?", [
   ("map.html", "The map", "find the school, then follow the blue line to the Liffey"),
   ("wildlife.html", "Wildlife", "otters, swans, herons and sticklebacks"),
   ("tymon.html", "Tymon Park", "the river out in the open, with lakes and ducks")]),
 ("3rd and 4th class", "How did the river shape our area?", [
   ("walk.html", "The river walk", "sixteen stops from Tallaght to the Liffey, with photos"),
   ("dubh-linn.html", "Dubh Linn", "the black pool that gave Dublin its name"),
   ("mills.html", "The mills", "how the river powered the city for seven centuries")]),
 ("5th and 6th class", "Why does it matter now?", [
   ("history.html", "The history", "from Dubh Linn to medieval diversions and the 1719 Act"),
   ("floods.html", "Floods and the flood scheme", "six centuries of flooding and the works to stop it"),
   ("river-data.html", "Live data", "today’s river levels and the flood maps")]),
]
SCHOOL_IDEAS = [
 "Find your school on the <a href=\"map.html\">map</a> and trace the river from there to the sea. Is it above ground or below it near you?",
 "Compare the 1848 Ordnance Survey map on the <a href=\"walk.html\">river walk</a> with today’s streets on the <a href=\"map.html\">map</a>. What has changed, and what is still there?",
 "Check the <a href=\"river-data.html\">live river levels</a> after a wet weekend, and talk about why the river rises so fast in a city of roofs and roads.",
 "Pick a <a href=\"mill-sites.html\">mill site</a> near the school and find out what was made there and what stands there now.",
 "Make a wildlife list for the river from the <a href=\"wildlife.html\">wildlife page</a>, then look for the same birds in a local park.",
]
schools = f'''<div class="wrap page narrow"><header class="page-head"><p class="kicker">For teachers</p><h1>Teaching the Poddle</h1>
<p class="dek">Dublin’s hidden river runs from Tallaght to the Liffey, past or under many of south Dublin’s schools. Everything on this site is free to use in class, with no sign-up.</p></header>
<aside class="brief"><strong>In brief</strong><p>The Poddle makes a ready-made local study for SESE history and geography: local history, rivers and water, change over time and caring for the environment. It also suits the Green-Schools Water theme.</p></aside>
<section id="by-class"><h2>Pages for each class</h2>
<div class="levels-grid">''' + "".join(
  f'<div class="level"><h3>{esc(cl)}</h3><p class="note">{esc(q)}</p><ul>'
  + "".join(f'<li><a href="{h}">{esc(t)}</a>: {esc(d)}</li>' for h, t, d in pages) + '</ul></div>'
  for cl, q, pages in SCHOOL_LEVELS) + '''</div></section>
<section id="ideas"><h2>Ideas for the classroom</h2><ul>''' + "".join(f'<li>{i}</li>' for i in SCHOOL_IDEAS) + f'''</ul></section>
<section id="curriculum"><h2>Where it fits</h2><ul>
<li><strong>History:</strong> local studies, and working with evidence such as old maps, photographs and written accounts.</li>
<li><strong>Geography:</strong> rivers and the natural environment, and how a city was built over a river.</li>
<li><strong>Environmental awareness and care:</strong> pollution, wildlife and keeping homes safe from flooding.</li>
<li><strong>Green-Schools:</strong> a local river study for the Water theme.</li>
</ul></section>
<section id="walks"><h2>Visiting the river</h2>
<p>The river is open to the air through Tymon Park, Whitehall Park and Ravensdale Park, and these are the best places to see it with a class. From Kimmage down it runs mostly in walls and culverts, though you can still follow its route through the streets.</p>
<p>Two ready-made school walks give a route, stops, things to look for and activities:</p>''' + walk_cards() + '''
<p class="note">Please plan any visit under your school’s own outings policy. Keep children back from the water’s edge, and never go near culvert openings or grilles.</p></section>
<section id="workbooks"><h2>Workbooks, talks and walks</h2>
<p>There are five <a href="shop.html">activity workbooks</a> about the river, each at three levels: 1st and 2nd class, 3rd and 4th class, and 5th and 6th class. Sales help keep this site free.</p>
<p>There is also an <a href="poster.pdf">A4 poster</a> (PDF) for a classroom or staffroom wall.</p>
<p>The project also offers talks and guided walks for schools and groups. Please <a href="about.html#contact">get in touch</a> to arrange one, or to ask about anything on the site.</p></section>
</div>'''
write("schools.html", shell("schools", f"For teachers · {SITE}",
      "Free classroom resources on the River Poddle, Dublin’s hidden river: pages for 1st to 6th class, classroom ideas and curriculum links for SESE history and geography.",
      schools, ""))

privacy = f'''<div class="wrap page narrow"><header class="page-head"><p class="kicker">Privacy</p><h1>Privacy notice</h1>
<p class="dek">This site collects as little as it can. Here is what is kept, why, and how to ask for it to be removed.</p></header>
<section><h2>Who runs this site</h2><p>poddle.ie is a personal, non-commercial local-history project based in Dublin. You can contact the project through the <a href="about.html#contact">form on the About page</a>.</p></section>
<section><h2>Visitor counts</h2><p>The site counts visits with <a href="https://www.goatcounter.com" rel="noopener">GoatCounter</a>. It uses no cookies and does not track you across sites. It records which page was viewed, the site you came from, your browser and screen size and your country. Your IP address is not stored. There is no advertising on this site.</p></section>
<section><h2>Messages you send</h2><p>If you use the contact form, your name, email address and message are passed through <a href="https://formsubmit.co" rel="noopener">FormSubmit</a> and delivered to the project by email. They are used only to reply to you, and deleted when no longer needed, usually within a year.</p></section>
<section><h2>Buying a workbook</h2><p>Workbooks are sold through <a href="https://payhip.com" rel="noopener">Payhip</a>, which handles payment and delivery under its own privacy policy. Payhip shares your name, email address and what you bought with the project, so it can help with any problem with your order. The project never sees your card details.</p></section>
<section><h2>Schools</h2><p>The project may email a school’s published office address to tell it about this free resource. It keeps the school’s name, its published email address and the principal’s name, because telling local schools about a free local-history resource is a legitimate interest, and the impact on them is small. Each email says how to opt out, and if a school asks not to be contacted again, the project keeps a note of that so it never is. The other details are deleted after a year if there is no reply.</p></section>
<section><h2>Other sites</h2><p>The maps load street tiles from OpenStreetMap and the text uses Google Fonts, so your browser connects to those services to fetch them. Links to Facebook, Instagram, YouTube and other sites take you to services with their own privacy policies.</p></section>
<section><h2>Your rights</h2><p>You can ask to see, correct or delete anything the project holds about you, or object to its use, through the <a href="about.html#contact">contact form</a>. If you are unhappy with how your data has been handled, you can complain to the <a href="https://www.dataprotection.ie" rel="noopener">Data Protection Commission</a>.</p>
<p class="note">Last updated November 2026.</p></section>
</div>'''
write("privacy.html", shell("privacy", f"Privacy · {SITE}", "How poddle.ie handles visitor counts, contact messages, workbook orders and emails to schools.", privacy, ""))
# ---------------------------------------------------------------- shop / support
# Hosted checkout links. The site is static, so everything is sold off-site:
# workbooks through a digital-download shop, t-shirts through print on demand.
# Empty string = not signed up yet; the page then shows "Coming soon".
SHOP = dict(
  downloads="https://payhip.com/ThePoddle",
  tees="",                 # e.g. https://thepoddle.teemill.com
  price_single="€4",
  price_pack="€9",
  price_all="€25",
)
LEVELS = [("J", "1st and 2nd class", "ages 6 to 8"), ("M", "3rd and 4th class", "ages 8 to 10"), ("U", "5th and 6th class", "ages 10 to 12")]
WORKBOOKS = [
 ("The Secret River", "the-secret-river", "A first look at Dublin’s hidden river: where it rises, where it runs and why the city grew beside it. Fact pages, a historical source, a flood-in-a-tray experiment and a quiz."),
 ("Hunt for the Hidden River", "treasure-hunt", "A treasure hunt through the city centre. Solve a clue at each of six stops, collect the letters, and spell the secret word."),
 ("Walk the Hidden River", "walking-tour", "A self-guided walk along the Poddle’s buried course, from Blackpitts to the Liffey: seven stops, about 2.5 km, with something to look for at each."),
 ("Mill Detectives", "mill-detectives", "Water power and the mills that lined the Poddle, with a waterwheel to build from card and a paper plate, and test with a jug of water."),
 ("Flood Defenders", "flood-defenders", "Why the Poddle floods and how Dublin is keeping homes dry, with hands-on experiments and a flood defence to design."), ("Tymon Park River Walk", "tymon-walk", "A walk beside the open river in Tymon Park: the lake and its birds, the flood gate and the wetland that cleans the water, with a bird tally to fill in."),
 ("The Mill Road Walk", "mill-road-walk", "A walk from Kimmage to Harold’s Cross through the old mill country, past the Stone Boat and Mount Argus to the siphon under the Grand Canal."),
]

def shop_btn(url, label, ghost=False):
    if url:
        return f'<a class="btn{" ghost" if ghost else ""}" href="{url}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'
    return '<span class="btn soon" aria-disabled="true">Coming soon</span>'

wb_cards = "".join(
  f'<li><a href="{SHOP["downloads"] or "#workbooks"}"{" target=\"_blank\" rel=\"noopener noreferrer\"" if SHOP["downloads"] else ""}>'
  f'<span class="cover"><img src="img/shop/{img}.jpg" alt="Cover of {esc(n)}" loading="lazy" width="520" height="736"></span>'
  f'<span class="wb-t"><strong>{esc(n)}</strong><span class="wb-d">{esc(d)}</span>'
  f'<span class="lv">{"".join(f"<span>{esc(cl)}</span>" for _, cl, _ in LEVELS)}</span>'
  f'<span class="price">{SHOP["price_single"]} each · {SHOP["price_pack"]} for all three</span></span></a></li>'
  for n, img, d in WORKBOOKS)

shop_page = f'''<section class="shop-hero"><div class="wrap shop-hero-in">
 <div class="shop-hero-text">
  <p class="kicker">Support this site</p>
  <h1>Workbooks for curious kids</h1>
  <p class="lede">Everything on this site is free, and it will stay that way, with no paywall and no adverts. If you would like to help with the hosting and the hours spent in the archives, buy a workbook. It is the whole business model.</p>
  <ul class="facts"><li><strong>21</strong><span>workbooks, 1st to 6th class</span></li><li><strong>A4</strong><span>PDFs to print at home or school</span></li><li><strong>{SHOP["price_single"]}</strong><span>each, with packs and a full set</span></li></ul>
  <p class="cta">{shop_btn(SHOP["downloads"], "Browse the workbooks")}<a class="btn ghost" href="#workbooks">See what’s inside</a></p>
 </div>
 <figure class="shop-hero-fig"><img src="img/shop/complete-set.webp" alt="The five Poddle workbook covers fanned out" width="1200" height="600"></figure>
</div></section>
<div class="wrap page">
<section class="shop-sec" id="workbooks"><div class="sec-head"><p class="kicker">The workbooks</p><h2>Seven stories of the river, three levels each</h2>
<p class="dek">Original writing and artwork about Dublin’s hidden river. Each comes in versions for 1st and 2nd class, 3rd and 4th class, and 5th and 6th class, with notes for the adult, curriculum links and an answer key. One copy covers your own family or one classroom.</p></div>
<ul class="wb">{wb_cards}</ul></section>
<section class="set-panel"><figure><img src="img/shop/complete-set.webp" alt="The complete set of Poddle workbooks" loading="lazy" width="1200" height="600"></figure>
<div><p class="kicker">Best value</p><h2>The complete set</h2><p>All twenty-one workbooks for {SHOP["price_all"]}. It’s a ready-made local-history programme for a whole school, a teacher with several classes, or a family who wants the lot.</p>
<p class="cta">{shop_btn(SHOP["downloads"], "Get the complete set")}</p><p class="small">Paid securely by card or PayPal through Payhip. Your download arrives straight away.</p></div></section>
<section class="shop-sec tee"><div class="sec-head"><p class="kicker">Coming soon</p><h2>Poddle t-shirts</h2>
<p class="dek">Shirts and totes printed with the river: the 1848 line of the Poddle, the culvert arch, and the dubh linn that gave Dublin its name. They will be printed to order, so nothing is wasted.</p></div>
<p class="cta">{shop_btn(SHOP["tees"], "See the t-shirts")}</p></section>
<section class="shop-sec"><div class="sec-head"><h2>Other ways to help</h2></div>
<ul class="help">
<li><strong>Tell us what we have wrong.</strong> Corrections and local memories are worth more to this site than money. <a href="about.html#contact">Get in touch</a>.</li>
<li><strong>Share the site</strong> with a school, a history group or anyone who walks over the river without knowing it.</li>
<li><strong>Book a talk or a walk</strong> for your group.</li>
</ul></section>
</div>'''
write("shop.html", shell("shop", f"Workbooks and t-shirts · {SITE}", "Workbooks about Dublin’s hidden river for 1st to 6th class. Every sale helps keep this local-history site free.", shop_page, "shop.html"))

exec(open(os.path.join(OUT, "build_extra.py"), encoding="utf-8").read())
exec(open(os.path.join(OUT, "build_walks.py"), encoding="utf-8").read())

# 404 page, sitemap and robots.txt (after build_extra so its pages are listed)
write("404.html", shell("404", f"Page not found · {SITE}", "This page could not be found.",
      '<div class="wrap page narrow"><header class="page-head"><h1>Page not found</h1><p class="dek">This page has gone underground, like the river.</p></header>'
      '<p><a href="/">Back to the home page</a> or <a href="/walk.html">walk the river</a>.</p></div>', "", noindex=True)
      .replace('href="', 'href="/').replace('href="/http', 'href="http').replace('href="//', 'href="/').replace('href="/#', 'href="#')
      .replace('src="', 'src="/').replace('src="/http', 'src="http'))
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f'<url><loc>{BASE if s == "index" else BASE + s + ".html"}</loc></url>\n' for s in SITEMAP) + '</urlset>\n')
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
print("built", len(STOPS) + len(HISTORY) + 4, "pages")
