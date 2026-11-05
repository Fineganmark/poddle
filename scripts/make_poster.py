"""Make the A4 schools poster (poster.pdf) from poster.html with Playwright.
Run: python3 scripts/make_poster.py  (needs `pip install qrcode` and Node Playwright)."""
import base64, io, os, subprocess, qrcode, qrcode.image.svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://poddle.ie/map.html"
svg = qrcode.make(URL, image_factory=qrcode.image.svg.SvgPathImage, border=0)
buf = io.BytesIO(); svg.save(buf)
qr = "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()
photo = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(ROOT, "img/mount-argus-waterfall.jpg"), "rb").read()).decode()

html = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 210mm; height: 297mm; font-family: Georgia, "Times New Roman", serif; color: #1c2530; background: #f2f3ee; position: relative; }}
.photo {{ height: 62mm; background: url({photo}) center 60% / cover; }}
.in {{ padding: 9mm 14mm 0; }}
.kicker {{ font: bold 11pt Arial, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #9b3b2a; }}
h1 {{ font-weight: normal; font-size: 36pt; line-height: 1.02; margin-top: 2mm; }}
h1 b {{ color: #2c6b9a; font-weight: normal; }}
.lede {{ font-size: 14pt; line-height: 1.35; margin-top: 4mm; }}
.facts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-top: 6mm; }}
.fact {{ background: #fbfbf8; border: 1px solid #d5d9d3; border-top: 4px solid #2c6b9a; padding: 3.5mm 4mm; }}
.fact .big {{ font-size: 24pt; color: #2c6b9a; line-height: 1; }}
.fact p {{ font-size: 11.5pt; line-height: 1.3; margin-top: 2mm; }}
.fact.q {{ border-top-color: #9b3b2a; }}
.fact.q .big {{ color: #9b3b2a; }}
.foot {{ position: absolute; left: 14mm; right: 14mm; bottom: 11mm; display: flex; gap: 8mm; align-items: center; border-top: 2px solid #1c2530; padding-top: 6mm; }}
.foot img {{ width: 32mm; height: 32mm; }}
.foot p {{ font-size: 12pt; line-height: 1.4; }}
.foot strong {{ font-size: 22pt; color: #2c6b9a; display: block; font-weight: normal; }}
.foot small {{ display: block; font: 9pt Arial, sans-serif; color: #5b6672; margin-top: 2mm; }}
</style></head><body>
<div class="photo"></div>
<div class="in">
<p class="kicker">Dublin’s hidden river</p>
<h1>Is there a secret river <b>under your school?</b></h1>
<p class="lede">The River Poddle flows from Tallaght to the Liffey, mostly hidden under roads, parks and houses. Can you find where it runs near you?</p>
<div class="facts">
<div class="fact"><div class="big">Dubh Linn</div><p>Dublin is named after a black pool on this river. It was where Dublin Castle’s gardens are today.</p></div>
<div class="fact"><div class="big">2020</div><p>The year otters moved back to the Poddle, in Tymon Park. What other animals live there?</p></div>
<div class="fact"><div class="big">The Stone Boat</div><p>A stone hundreds of years old still splits the river in two on Sundrive Road. Why would anyone do that?</p></div>
<div class="fact"><div class="big">3 metres</div><p>How much the lake in Tymon Park can now rise in a storm, to stop houses flooding.</p></div>
<div class="fact q"><div class="big">Mills!</div><p>For hundreds of years the river turned mill wheels to grind flour. Was there one near you?</p></div>
<div class="fact q"><div class="big">Your turn</div><p>Find your school on the map, and follow the river all the way to the sea.</p></div>
</div>
</div>
<div class="foot"><img src="{qr}" alt=""><p><strong>Scan me, or go to poddle.ie</strong>Explore the map, walk the river and check live river levels.<small>Teachers: free class ideas from 1st to 6th class at poddle.ie/schools.html</small></p></div>
</body></html>"""
open(os.path.join(ROOT, "poster.html"), "w", encoding="utf-8").write(html)
subprocess.run(["node", "-e", f"""
const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{ROOT}/poster.html');await p.pdf({{path:'{ROOT}/poster.pdf',format:'A4',printBackground:true}});
await p.setViewportSize({{width:794,height:1123}});await p.screenshot({{path:'{ROOT}/img/poster-preview.png'}});await b.close();}})();"""], check=True)
os.remove(os.path.join(ROOT, "poster.html"))
