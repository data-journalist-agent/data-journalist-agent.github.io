"""MODIS fire pixel analysis — 7-day window 2019-12-29 to 2020-01-05.

Important: a row is a 1km satellite detection, not a fire. We are characterising
the *pattern* of detections, not estimating burned area.
"""
import pandas as pd
import json

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/05_australia-fires"

f = pd.read_csv(f"{DATA}/MODIS_C6_Australia_and_New_Zealand_7d.csv")
# Restrict to mainland Australia bounding box
mask = (f["longitude"] >= 113) & (f["longitude"] <= 154) & (f["latitude"] <= -10) & (f["latitude"] >= -45)
f = f[mask].copy()

# --- ana_08: detections per day ---
print("=== ana_08 ===")
daily = f.groupby("acq_date").size().reset_index(name="detections")
daily = daily.sort_values("acq_date")
print(daily.to_string(index=False))
print(f"total detections: {len(f):,}")

# --- ana_09: high-confidence detection share ---
print("=== ana_09 ===")
buckets = pd.cut(f["confidence"], bins=[-1, 30, 80, 101], labels=["low", "nominal", "high"])
vc = buckets.value_counts().reindex(["low", "nominal", "high"]).reset_index()
vc.columns = ["confidence_class", "count"]
vc["pct"] = (vc["count"] / vc["count"].sum() * 100).round(1)
print(vc.to_string(index=False))

# --- ana_10: assign rough state/region by lat-lon box ---
print("=== ana_10 ===")
def region(row):
    lat = row["latitude"]; lon = row["longitude"]
    # Approximate Australian state boxes
    if lat > -29 and lon < 141:
        return "QLD/NT/SA inland"
    if lat > -29 and lon >= 141:
        return "QLD"
    if lat <= -29 and lat > -34 and lon >= 141:
        return "NSW"
    if lat <= -34 and lat > -39 and lon >= 140:
        return "VIC"
    if lat <= -39 and lon >= 144:
        return "TAS"
    if lat <= -29 and lon < 129:
        return "WA"
    if lat <= -29 and lon >= 129 and lon < 141:
        return "SA"
    return "Other"

f["region"] = f.apply(region, axis=1)
reg = f.groupby("region").size().reset_index(name="detections").sort_values("detections", ascending=False)
reg["pct"] = (reg["detections"] / reg["detections"].sum() * 100).round(1)
print(reg.to_string(index=False))

# --- ana_11: fire radiative power (FRP) distribution ---
print("=== ana_11 ===")
print(f"FRP MW: median={f['frp'].median():.1f}, mean={f['frp'].mean():.1f}, p90={f['frp'].quantile(0.9):.1f}, p99={f['frp'].quantile(0.99):.1f}, max={f['frp'].max():.1f}")
# count by bucket
fp = pd.cut(f["frp"], bins=[0, 25, 100, 500, 10000], labels=["<25 MW", "25-100", "100-500", "500+"])
fpv = fp.value_counts().reindex(["<25 MW", "25-100", "100-500", "500+"]).reset_index()
fpv.columns = ["frp_class", "count"]
fpv["pct"] = (fpv["count"] / fpv["count"].sum() * 100).round(1)
print(fpv.to_string(index=False))

# --- ana_12: brightness extremes — peak heat pixels ---
print("=== ana_12 ===")
top = f.nlargest(10, "brightness")[["acq_date", "acq_time", "latitude", "longitude", "brightness", "frp", "confidence", "region", "daynight"]]
print(top.to_string(index=False))

# --- ana_13: night-fire share by region (night burns are more dangerous) ---
print("=== ana_13 ===")
night = f.groupby(["region", "daynight"]).size().unstack(fill_value=0)
night["total"] = night.sum(axis=1)
night["night_pct"] = (night["N"] / night["total"] * 100).round(1)
night = night.sort_values("total", ascending=False)
print(night.to_string())

# --- ana_14: hourly pattern (UTC, but converts roughly to Australian local) ---
print("=== ana_14 ===")
f["hour_utc"] = (f["acq_time"].astype(int) // 100)
hr = f.groupby("hour_utc").size().reset_index(name="detections")
print(hr.to_string(index=False))

# Save geojson-style sample for the map (down-sampled high-confidence)
print("=== fire_sample ===")
hi = f[f["confidence"] >= 60].copy()
# Down-sample to ~2000 points for embedding in HTML (data_table)
sample = hi.sample(min(2000, len(hi)), random_state=42)[["latitude", "longitude", "brightness", "frp", "acq_date", "daynight", "region"]]
sample = sample.round({"latitude": 3, "longitude": 3, "brightness": 1, "frp": 1})
print(f"sampled {len(sample)} of {len(hi):,} high-confidence detections; full hi total = {len(hi):,}")
sample.to_csv(f"{DATA}/_fire_sample.csv", index=False)
