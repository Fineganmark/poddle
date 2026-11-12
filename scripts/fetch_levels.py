"""Fetch the last week of water levels for the Dodder gauges nearest the Poddle
from waterlevel.ie (Office of Public Works, provisional data), and the Liffey at
Dublin Port from the Marine Institute's tide gauge (the Poddle enters the tidal
Liffey at Wellington Quay; the OPW has no live Liffey gauge in the city), into data/levels.json."""
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
    if len(pts) > 200:   # hourly is plenty for a week, but always keep the latest reading
        pts = pts[::4] + ([pts[-1]] if (len(pts) - 1) % 4 else [])
    return pts

# Marine Institute, Irish National Tide Gauge Network (ERDDAP), every 6 minutes, metres above Ordnance Datum (Malin)
TIDE = dict(ref="dublin-port", name="Dublin Port, River Liffey (tidal)",
            url="https://erddap.marine.ie/erddap/tabledap/IrishNationalTideGaugeNetwork.csv"
                "?time,Water_Level_OD_Malin&station_id=%22Dublin%20Port%22&time%3E=now-7days",
            page="https://www.marine.ie/site-area/data-services/real-time-observations/irish-national-tide-gauge-network")

def parse_erddap(text):
    rows = list(csv.reader(io.StringIO(text)))[2:]   # header row, then a units row
    pts = []
    for r in rows:
        try:
            v = float(r[1])
            if -4 < v < 5:   # the gauge sometimes logs nonsense (e.g. -32 m); Dublin tides stay within about -3 to +3 m OD
                pts.append([r[0][:19], round(v, 3)])
        except (IndexError, ValueError):
            continue
    if len(pts) > 400:   # every 6 minutes; keep about one an hour, and the latest
        pts = pts[::10] + ([pts[-1]] if (len(pts) - 1) % 10 else [])
    return pts

def main(out):
    stations = []
    for ref, name in STATIONS:
        try:
            pts = parse(get(f"https://waterlevel.ie/data/week/{ref}_0001.csv"))
            if pts:
                stations.append(dict(ref=ref, name=name, points=pts))
        except Exception as e:  # keep the site building even if one gauge is down
            print("skip", ref, e, file=sys.stderr)
    try:
        pts = parse_erddap(get(TIDE["url"]))
        if pts:
            stations.append(dict(ref=TIDE["ref"], name=TIDE["name"], points=pts, tide=True, page=TIDE["page"]))
    except Exception as e:
        print("skip tide gauge", e, file=sys.stderr)
    if not stations:
        print("no gauge data; leaving levels.json absent", file=sys.stderr)
        return
    json.dump(dict(updated=datetime.now(timezone.utc).isoformat(), stations=stations),
              open(out, "w", encoding="utf-8"), ensure_ascii=False)
    print("wrote", out, [len(s["points"]) for s in stations])

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/levels.json")
