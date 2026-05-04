"""NSW Rural Fire Service major incidents — snapshot at 2020-01-06."""
import json
import re
from collections import Counter

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/05_australia-fires"

with open(f"{DATA}/majorIncidents-2020-01-06.json") as fh:
    rfs = json.load(fh)

feats = rfs["features"]
print(f"total incidents: {len(feats)}")

def parse_props(props):
    desc = props.get("description") or ""
    # description is "ALERT LEVEL: Advice <br />LOCATION: ... <br />..."
    out = {}
    for line in re.split(r"<br\s*/?>", desc):
        line = line.strip()
        m = re.match(r"^([A-Z][A-Z ]+?):\s*(.*)$", line)
        if m:
            out[m.group(1).strip()] = m.group(2).strip()
    return out

# --- ana_15: status of NSW incidents on 2020-01-06 ---
print("=== ana_15 ===")
status_counts = Counter()
alert_counts = Counter()
type_counts = Counter()
size_total_ha = 0.0
sizes = []
for f in feats:
    p = f.get("properties", {})
    parsed = parse_props(p)
    status_counts[parsed.get("STATUS", "Unknown")] += 1
    alert_counts[parsed.get("ALERT LEVEL", "Unknown")] += 1
    type_counts[parsed.get("TYPE", "Unknown")] += 1
    sz = parsed.get("SIZE", "0 ha")
    m = re.match(r"([\d,]+(?:\.\d+)?)\s*ha", sz)
    if m:
        v = float(m.group(1).replace(",", ""))
        sizes.append(v)
        size_total_ha += v

print("status:")
for k, v in status_counts.most_common():
    print(f"  {k}: {v}")
print("alert:")
for k, v in alert_counts.most_common():
    print(f"  {k}: {v}")
print("type:")
for k, v in type_counts.most_common():
    print(f"  {k}: {v}")
print(f"summed declared size: {size_total_ha:,.0f} ha across {len(sizes)} incidents")
print(f"largest incident: {max(sizes):,.0f} ha")

# --- ana_16: top-10 largest incidents and their status ---
print("=== ana_16 ===")
def first_point(geom):
    if not geom:
        return None, None
    if geom.get("type") == "Point":
        c = geom["coordinates"]
        return c[1], c[0]
    if geom.get("type") == "GeometryCollection":
        for g in geom.get("geometries", []):
            lat, lon = first_point(g)
            if lat is not None:
                return lat, lon
    if geom.get("type") in ("Polygon", "MultiPolygon"):
        if geom["type"] == "Polygon":
            ring = geom["coordinates"][0]
        else:
            ring = geom["coordinates"][0][0]
        if ring:
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]
            return sum(lats)/len(lats), sum(lons)/len(lons)
    return None, None

records = []
for f in feats:
    p = f.get("properties", {})
    parsed = parse_props(p)
    sz = parsed.get("SIZE", "0 ha")
    m = re.match(r"([\d,]+(?:\.\d+)?)\s*ha", sz)
    val = float(m.group(1).replace(",", "")) if m else 0
    lat, lon = first_point(f.get("geometry"))
    records.append({
        "title": p.get("title", ""),
        "size_ha": val,
        "status": parsed.get("STATUS", ""),
        "alert": parsed.get("ALERT LEVEL", ""),
        "loc": parsed.get("LOCATION", ""),
        "type": parsed.get("TYPE", ""),
        "lat": lat,
        "lon": lon,
    })
records.sort(key=lambda r: r["size_ha"], reverse=True)
for r in records[:15]:
    print(f"{r['size_ha']:>12,.0f} ha | {r['status']:<20} | {r['alert']:<20} | {r['title'][:60]}")

# --- ana_17: incident size distribution ---
print("=== ana_17 ===")
sizes_pos = [r["size_ha"] for r in records if r["size_ha"] > 0]
print(f"incidents with declared size > 0: {len(sizes_pos)}")
print(f"sum (declared ha): {sum(sizes_pos):,.0f} ha = {sum(sizes_pos)/1e6:.2f} million ha")
print(f"largest: {max(sizes_pos):,.0f} ha; median: {sorted(sizes_pos)[len(sizes_pos)//2]:,.0f} ha")
import json as _json
with open("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/05_australia-fires/_rfs_incidents.json", "w") as fh:
    _json.dump(records, fh)
print(f"wrote {len(records)} parsed incidents to _rfs_incidents.json")
