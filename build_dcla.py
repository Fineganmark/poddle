# Dublin Corporation Waterworks map sheets (Nov 2026), run by build.py after build_archive.py.
# Mark's own photographs of the Ordnance Survey sheets annotated by the Waterworks Department,
# held by Dublin City Library & Archive (DCLA) in WW/12/17, WW/12/18 and WW/12/19.
# DCLA gave permission on 9 Nov 2026 (Hannah Keelan). Every image must carry
# "[Image Ref] Courtesy of Dublin City Library & Archive". Archive maps stay in colour, north up.
# The pictures are cropped and turned north-up from the pinned photos (dcla-maps in project files).

_DCLA = "Courtesy of Dublin City Library & Archive."
_SOUTH = "WW/12/17–18"   # South Side volumes 1 and 2 (which volume each sheet is in not yet noted)
_COUNTY = "WW/12/19"     # South County Dublin

def _dcla(desc, sheet, ref):
    return f"{desc} {sheet} {ref} – {_DCLA}"

_RED = "annotated by the Dublin Corporation Waterworks Department (water mains in red)"
DCLA_IMAGES = {
 "ravensdale": [
  ("dcla-1911-kimmage-ravensdale", _dcla(
    "Kimmage, Larkfield and Ravensdale before the suburbs: the Poddle and its mill races winding through open fields.",
    f"Ordnance Survey sheet XXII.2, revised 1907, published 1911, annotated by the Dublin Corporation Waterworks Department.",
    f"{_COUNTY} Sheet XXII.2, Kimmage, Larkfield and Ravensdale Mills"))],
 "mount-jerome": [
  ("dcla-1911-harolds-cross", _dcla(
    "Mount Jerome Cemetery and Harold’s Cross, with the Poddle crossing Harold’s Cross Road.",
    f"Ordnance Survey sheet XVIII.15, revised 1907, published 1911, annotated by the Dublin Corporation Waterworks Department.",
    f"{_COUNTY} Sheet XVIII.15, Harold’s Cross, Mount Jerome and Greenmount"))],
 "meander-dolphins-barn": [
  ("dcla-1909-dolphins-barn", _dcla(
    "Dolphin’s Barn and Rialto in 1909, with the Grand Canal crossing from the left. Behind Reuben Street the water splits: the City Watercourse heads north to the Back of the Pipes and a “Poddle River” branch heads east.",
    f"Ordnance Survey city sheet XVIII.75, 1909 edition, {_RED}.",
    f"{_SOUTH} Sheet XVIII.75, Dolphin’s Barn and Reuben Street")),
  ("dcla-1890-dolphins-barn", _dcla(
    "The same ground about twenty years earlier, when a single channel ran behind Reuben Street.",
    f"Ordnance Survey city sheet XVIII.75, reprint of about 1890, {_RED}.",
    f"{_SOUTH} Sheet XVIII.75, Dolphin’s Barn and Rialto"))],
 "city-watercourse": [
  ("dcla-1909-rutland", _dcla(
    "The City Watercourse running north past Rutland, along today’s Rutland Avenue, to the Grand Canal at Dolphin’s Barn, 1909.",
    f"Ordnance Survey city sheet XVIII.85, 1909 edition, {_RED}.",
    f"{_SOUTH} Sheet XVIII.85, Rutland, Crumlin Road")),
  ("dcla-1876-rutland", _dcla(
    "The same stretch of the City Watercourse as first surveyed in 1876, past Rutland House.",
    f"Ordnance Survey city sheet XVIII.85, surveyed 1876, {_RED}.",
    f"{_SOUTH} Sheet XVIII.85, Rutland"))],
 "meander-st-jamess-gate": [
  ("dcla-1908-james-basin", _dcla(
    "The City Basin off James’s Street, where the City Watercourse ended, beside the Grand Canal harbour, 1908.",
    f"Ordnance Survey city sheet XVIII.65, 1908 edition, {_RED}.",
    f"{_SOUTH} Sheet XVIII.65, James’s Basin")),
  ("dcla-1890-james-basin", _dcla(
    "The City Basin and the canal harbour about 1890, with “Poddle River” and “Water Course” marked side by side.",
    f"Ordnance Survey city sheet, reprint of about 1890, {_RED}.",
    f"{_SOUTH} James’s Basin and canal harbour"))],
 "meander-abbey-stream": [
  ("dcla-1909-donore-avenue", _dcla(
    "Donore Avenue, Harman Street and Warrenmount, 1909, with the culverted “Poddle River” shown dashed.",
    f"Ordnance Survey city sheet XVIII.76, 1909 edition, {_RED}.",
    f"{_SOUTH} Sheet XVIII.76, Donore Avenue and Warrenmount")),
  ("dcla-1886-donore-avenue", _dcla(
    "Donore Avenue and Greenville before most of the houses were built, 1886.",
    f"Ordnance Survey city sheet XVIII.76, revised and lithographed 1886, {_RED}.",
    f"{_SOUTH} Donore Avenue"))],
 "st-patricks": [
  ("dcla-1908-patrick-street", _dcla(
    "Patrick Street, St Patrick’s Cathedral and the Coombe, 1908, over the line of the Poddle’s culvert.",
    f"Ordnance Survey city sheet XVIII.66, 1908 edition, {_RED}.",
    f"{_SOUTH} Sheet XVIII.66, Patrick Street and St Patrick’s Cathedral")),
  ("dcla-1890-patrick-street", _dcla(
    "The same streets about 1890, before the Iveagh clearances and St Patrick’s Park.",
    f"Ordnance Survey city sheet XVIII.66, reprint of about 1890, {_RED}.",
    f"{_SOUTH} Patrick Street and St Patrick’s Cathedral"))],
 "ship-street-little": [
  ("dcla-1909-ship-street", _dcla(
    "Ship Street, Bishop Street and Jacob’s biscuit factory below Dublin Castle, 1909.",
    f"Ordnance Survey city sheet XVIII.67, 1909 edition, {_RED}.",
    f"{_SOUTH} Sheet XVIII.67, Ship Street and Dublin Castle")),
  ("dcla-1890-ship-street", _dcla(
    "The same streets about 1890.",
    f"Ordnance Survey city sheet XVIII.67, reprint of about 1890, {_RED}.",
    f"{_SOUTH} Ship Street and Dublin Castle"))],
 "liffey": [
  ("dcla-1909-wellington-quay", _dcla(
    "Wellington Quay, East Essex Street and Eustace Street on a large-scale 1909 plan; the sheet marks the “Mouth of the Poddle” on the quay wall just above this extract.",
    f"Ordnance Survey large-scale city plan, 1909, {_RED}.",
    f"{_SOUTH} Wellington Quay, mouth of the Poddle")),
  ("dcla-1876-wellington-quay", _dcla(
    "The Liffey from Wellington Quay to Temple Bar in 1876, with lines drawn in by hand by the Waterworks Department.",
    f"Ordnance Survey city sheet, surveyed 1876, annotated by the Dublin Corporation Waterworks Department.",
    f"{_SOUTH} Wellington Quay and the Liffey"))],
}

_PAGES = {p["slug"]: p for p in STOPS + HISTORY + MEANDERS}
for _slug, _imgs in DCLA_IMAGES.items():
    _PAGES[_slug]["images"] = list(_PAGES[_slug]["images"]) + _imgs

# The credit must go with every DCLA picture, so they are never used where no caption shows:
# the page's share image (og:image) or the picture in a map popup.
def share_img(p):
    return next((f for f, _ in p["images"] if not f.startswith("dcla-")), None)
