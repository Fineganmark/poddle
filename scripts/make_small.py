"""Make the small copies of the site's pictures that the pages show (Nov 2026).

For every photo or map in img/ over SMALL_OVER bytes, writes
  img/sm/<same path>.webp     at most 900 px wide, for pages and map popups
  img/sm/<same path>.t.webp   a 420 px thumbnail, for the picture grids
The originals stay where they are: clicking a picture opens the full-size file.
build.py swaps in the small copy wherever one exists, so after adding new
pictures run:  python3 scripts/make_small.py   (needs Pillow) and commit img/sm/.
"""
import os, sys
from PIL import Image, ImageOps

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")
SMALL_OVER = 90_000
MID, THUMB = 900, 420

def out_path(rel, suffix):
    return os.path.join(ROOT, "sm", os.path.splitext(rel)[0] + suffix)

def save(im, path, width, q):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "WEBP", quality=q, method=6)

def _is_grey(im):
    sm = im.resize((64, 64))
    b = sm.tobytes()
    return max(max(abs(b[i] - b[i + 1]), abs(b[i + 1] - b[i + 2])) for i in range(0, len(b), 3)) < 18

def main(force=False):
    n = 0
    for d, _, files in os.walk(ROOT):
        rel_d = os.path.relpath(d, ROOT)
        if rel_d.split(os.sep)[0] in ("sm", "shop"):
            continue
        for f in files:
            if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) or "-thumb." in f:
                continue
            src = os.path.join(d, f)
            rel = os.path.normpath(os.path.join(rel_d, f))
            if os.path.getsize(src) < SMALL_OVER:
                continue
            mid, th = out_path(rel, ".webp"), out_path(rel, ".t.webp")
            if not force and os.path.exists(mid) and os.path.exists(th) and os.path.getmtime(mid) >= os.path.getmtime(src):
                continue
            im = ImageOps.exif_transpose(Image.open(src))
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and f.lower().endswith(".png") else "RGB")
            if im.mode == "RGB" and _is_grey(im):
                im = im.convert("L")   # black-and-white scans and clippings: one channel is smaller
            save(im, mid, MID, 72)
            save(im, th, THUMB, 70)
            n += 1
    print("made small copies of", n, "pictures")

if __name__ == "__main__":
    main("--force" in sys.argv)
