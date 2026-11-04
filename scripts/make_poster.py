"""Make the A4 schools poster (poster.pdf) from poster.html with Playwright.
Run: python3 scripts/make_poster.py  (needs `pip install qrcode` and Node Playwright)."""
import base64, io, os, subprocess, qrcode, qrcode.image.svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://poddle.ie/schools.html"
svg = qrcode.make(URL, image_factory=qrcode.image.svg.SvgPathImage, border=0)
buf = io.BytesIO(); svg.save(buf)
qr = "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()
photo = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(ROOT, "img/mount-argus-waterfall.jpg"), "rb").read()).decode()

html = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 210mm; height: 297mm; font-family: Georgia, "Times New Roman", serif; color: #1c2530; background: #f2f3ee; }}
.photo {{ height: 120mm; background: url({photo}) center / cover; position: relative; }}
.photo span {{ position: absolute; right: 8mm; bottom: 4mm; font: 9pt Arial, sans-serif; color: #fff; text-shadow: 0 0 3px #000; }}
.in {{ padding: 12mm 16mm 0; }}
.kicker {{ font: bold 11pt Arial, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #9b3b2a; }}
h1 {{ font-weight: normal; font-size: 44pt; line-height: 1.02; margin-top: 4mm; }}
h1 b {{ color: #2c6b9a; font-weight: normal; }}
.lede {{ font-size: 15pt; line-height: 1.4; margin-top: 6mm; }}
ul {{ margin-top: 6mm; padding-left: 6mm; font-size: 13pt; line-height: 1.5; }}
.foot {{ position: absolute; left: 16mm; right: 16mm; bottom: 14mm; display: flex; gap: 10mm; align-items: center; border-top: 2px solid #1c2530; padding-top: 7mm; }}
.foot img {{ width: 34mm; height: 34mm; }}
.foot p {{ font-size: 13pt; line-height: 1.45; }}
.foot strong {{ font-size: 24pt; color: #2c6b9a; display: block; font-weight: normal; }}
</style></head><body>
<div class="photo"><span>The Poddle at Mount Argus</span></div>
<div class="in">
<p class="kicker">Dublin’s hidden river</p>
<h1>There’s a river <b>under your feet</b></h1>
<p class="lede">The River Poddle flows from Tallaght to the Liffey, past Tymon Park, Kimmage, Harold’s Cross and the Liberties. It gave Dublin its name.</p>
<ul>
<li>An interactive map and a sixteen-stop river walk</li>
<li>Mills, floods and a thousand years of history</li>
<li>Otters, herons and the river’s wildlife</li>
<li>Live river levels, updated every hour</li>
</ul>
</div>
<div class="foot"><img src="{qr}" alt=""><p><strong>poddle.ie</strong>Free, with no sign-up. Teachers: class ideas from 1st to 6th class at poddle.ie/schools.html</p></div>
</body></html>"""
open(os.path.join(ROOT, "poster.html"), "w", encoding="utf-8").write(html)
subprocess.run(["node", "-e", f"""
const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{ROOT}/poster.html');await p.pdf({{path:'{ROOT}/poster.pdf',format:'A4',printBackground:true}});
await p.setViewportSize({{width:794,height:1123}});await p.screenshot({{path:'{ROOT}/img/poster-preview.png'}});await b.close();}})();"""], check=True)
os.remove(os.path.join(ROOT, "poster.html"))
