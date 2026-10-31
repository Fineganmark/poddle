"""Bake a light-blue highlight of the River Poddle onto the four history-page maps.

Shapes are traced by hand in each map's own pixel coordinates (1600px wide).
Run: python3 scripts/poddle_highlight.py  ->  img/dublin-<year>-poddle.jpg
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUE = (135, 200, 245)   # light blue; map lines darker than LREF still show through
LREF = 150
SS = 3                   # supersampling for smooth edges

def flood_mask(gray, s):
    """Pixels of the map's grey water fill connected to the seed points, inside clip."""
    import numpy as np
    from scipy import ndimage
    a = np.asarray(gray.filter(ImageFilter.MedianFilter(5)), dtype=np.int16)
    lo, hi = s.get("range", [85, 175])
    m = (a >= lo) & (a <= hi)
    clip = Image.new("L", gray.size, 0)
    ImageDraw.Draw(clip).polygon([tuple(p) for p in s["clip"]], fill=1)
    m &= np.asarray(clip, dtype=bool)
    m = ndimage.binary_opening(m, iterations=s.get("open", 3))
    lab, _ = ndimage.label(m)
    keep = {lab[y, x] for x, y in s["flood"]} - {0}
    m = np.isin(lab, list(keep))
    m = ndimage.binary_closing(m, iterations=4)
    m = ndimage.binary_fill_holes(m)
    m = ndimage.binary_dilation(m, iterations=1)
    return Image.fromarray((m * 255).astype("uint8"))

def mask_for(size, shapes, gray=None):
    w, h = size
    m = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(m)
    floods = []
    for s in shapes:
        if "flood" in s:
            floods.append(flood_mask(gray, s))
            continue
        pts = [(x * SS, y * SS) for x, y in s["pts"]]
        if s.get("fill"):
            d.polygon(pts, fill=255)
        else:
            wd = int(s["w"] * SS)
            d.line(pts, fill=255, width=wd, joint="curve")
            r = wd // 2
            for x, y in (pts[0], pts[-1]):
                d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    m = m.resize((w, h), Image.LANCZOS)
    for f in floods:
        m = ImageChops.lighter(m, f)
    return m.filter(ImageFilter.GaussianBlur(1.2))

def bake(year, shapes, out):
    src = Image.open(os.path.join(ROOT, "img", f"dublin-{year}.jpg"))
    im = src.convert("RGB")
    g = src.convert("L").point(lambda v: min(255, int(255 * v / LREF)))
    tint = ImageChops.multiply(Image.merge("RGB", (g, g, g)), Image.new("RGB", im.size, BLUE))
    m = mask_for(im.size, shapes, src.convert("L")).point(lambda v: int(v * 0.9))
    res = Image.composite(tint, im, m)
    res.save(out, quality=84, optimize=True, progressive=True)
    return res

if __name__ == "__main__":
    shapes = json.load(open(os.path.join(ROOT, "scripts", "poddle_shapes.json")))
    years = sys.argv[1:] or list(shapes)
    for y in years:
        bake(y, shapes[y], os.path.join(ROOT, "img", f"dublin-{y}-poddle.jpg"))
        print("wrote", y)
