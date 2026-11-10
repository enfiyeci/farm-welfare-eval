"""Round two, pick H: Google Maps dataset (Delmarva) -> index/delmarva-places.csv.

Usage: python3 -I r2_maps.py <pull-folder> <dataset.json>
One row per place. `kind` is a rough role from the Maps category and the name (integrator-site = a Perdue, Tyson,
Mountaire, Allen Harim or Amick site listed under a farm-like category, usually a plant or office); `other` rows
(restaurants, shops) came from the broad search terms and are kept only for completeness.
Phone numbers and street addresses stay in raw/; coordinates are rounded to 3 decimals (about 100 m).
"""
import csv, json, re, sys, collections
from pathlib import Path

root, src = Path(sys.argv[1]), Path(sys.argv[2])
INTEGRATORS = re.compile(r"perdue|tyson|mountaire|allen harim|amick|purdue", re.I)
def kind(x):
    cat, name = (x.get("categoryName") or ""), (x.get("title") or "")
    if re.search(r"hatchery", name, re.I) or cat == "Hatchery":
        return "hatchery"
    if re.search(r"processing|processor|plant", name + " " + cat, re.I) or cat in ("Meat processor", "Food processing company"):
        return "processing"
    if re.search(r"feed|grain|mill", name + " " + cat, re.I) or cat in ("Grain elevator", "Mill"):
        return "feed"
    if INTEGRATORS.search(name) and cat in ("Poultry farm", "Farm", "Food products supplier", "Food manufacturer", "Bus stop", ""):
        return "integrator-site"  # plants, offices and complexes listed under a farm-like category
    if cat in ("Poultry farm", "Farm", "Livestock producer", "Agricultural production", "Ranch", "Cattle farm"):
        return "farm"
    if cat in ("Agricultural service", "Farm equipment supplier", "Equipment supplier", "Agricultural organization",
               "Farm bureau", "Laboratory", "Corporate office"):
        return "service"
    return "other"

rows = []
for x in json.load(open(src)):
    loc = x.get("location") or {}
    rows.append({"name": x.get("title"), "kind": kind(x), "integrator_named": bool(INTEGRATORS.search(x.get("title") or "")),
                 "category": x.get("categoryName"), "city": x.get("city"), "state": x.get("state"),
                 "postal_code": x.get("postalCode"),
                 "lat": round(loc["lat"], 3) if loc.get("lat") else "", "lng": round(loc["lng"], 3) if loc.get("lng") else "",
                 "search_term": x.get("searchString"), "reviews": x.get("reviewsCount"),
                 "closed": "permanently" if x.get("permanentlyClosed") else ("temporarily" if x.get("temporarilyClosed") else ""),
                 "website": x.get("website") or "", "maps_url": x.get("url")})
rows.sort(key=lambda r: (r["kind"], r["state"] or "", r["name"] or ""))
with open(root / "index/delmarva-places.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "places;", collections.Counter(r["kind"] for r in rows), "; integrator-named:", sum(r["integrator_named"] for r in rows))
for r in rows:
    if r["kind"] in ("processing", "hatchery") or r["integrator_named"]:
        print(" ", r["kind"], "|", r["name"], "|", r["category"], "|", r["city"], r["state"])
