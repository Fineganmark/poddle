"""Fetch the last week of water levels for the Dodder gauges nearest the Poddle
from waterlevel.ie (Office of Public Works, provisional data) into data/levels.json."""
import csv, io, json, sys, urllib.request
from datetime import datetime, timezone

STATIONS = [("09010", "Waldron’s Bridge, River Dodder"), ("09369", "Anglesea Road, River Dodder")]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "poddle-site (github.com/Fineganmark/poddle)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")

def parse(text):
    pts = []
    for row in csv.DictReader(io.StringIO(text)):
        try:
            pts.append([row["datetime"].replace(" ", "T") + ":00", round(float(row["value"]), 3)])
        except (KeyError, ValueError):
            continue
    return pts[::4] if len(pts) > 200 else pts   # hourly is plenty for a week

def main(out):
    stations = []
    for ref, name in STATIONS:
        try:
            pts = parse(get(f"https://waterlevel.ie/data/week/{ref}_0001.csv"))
            if pts:
                stations.append(dict(ref=ref, name=name, points=pts))
        except Exception as e:  # keep the site building even if one gauge is down
            print("skip", ref, e, file=sys.stderr)
    if not stations:
        print("no gauge data; leaving levels.json absent", file=sys.stderr)
        return
    json.dump(dict(updated=datetime.now(timezone.utc).isoformat(), stations=stations),
              open(out, "w", encoding="utf-8"), ensure_ascii=False)
    print("wrote", out, [len(s["points"]) for s in stations])

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/levels.json")
