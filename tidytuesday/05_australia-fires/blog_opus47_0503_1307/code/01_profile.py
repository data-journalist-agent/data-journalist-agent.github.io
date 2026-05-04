"""Profile the Australia Fires dataset.

Files of interest:
  - temperature.csv (long: city x date x min/max)
  - rainfall.csv (long: station x year/month/day)
  - MODIS_C6_Australia_and_New_Zealand_7d.csv (NASA hotspot pixels)
  - majorIncidents-2020-01-06.json (NSW RFS GeoJSON of active incidents)
"""
import json
import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/05_australia-fires"

# --- ana_profile: dataset profile ---
print("=== ana_profile ===")

temp = pd.read_csv(f"{DATA}/temperature.csv")
rain = pd.read_csv(f"{DATA}/rainfall.csv", dtype={"month": str, "day": str})
fires = pd.read_csv(f"{DATA}/MODIS_C6_Australia_and_New_Zealand_7d.csv")
with open(f"{DATA}/majorIncidents-2020-01-06.json") as f:
    rfs = json.load(f)

print(f"temperature.csv: rows={len(temp):,}, cols={len(temp.columns)}, span={temp['date'].min()} to {temp['date'].max()}")
print(f"  cities: {sorted(temp['city_name'].unique().tolist())}")
print(f"  temp_type: {temp['temp_type'].value_counts().to_dict()}")
print(f"rainfall.csv: rows={len(rain):,}, cols={len(rain.columns)}, span={rain['year'].min()} to {rain['year'].max()}")
print(f"  cities: {sorted(rain['city_name'].unique().tolist())}")
print(f"fires (MODIS): rows={len(fires):,}, cols={len(fires.columns)}, dates={fires['acq_date'].min()} to {fires['acq_date'].max()}")
print(f"  daynight: {fires['daynight'].value_counts().to_dict()}")
print(f"  satellite: {fires['satellite'].value_counts().to_dict()}")
print(f"  confidence min={fires['confidence'].min()}, mean={fires['confidence'].mean():.1f}, max={fires['confidence'].max()}")
print(f"  brightness mean K={fires['brightness'].mean():.1f}, max K={fires['brightness'].max():.1f}")
print(f"  frp mean MW={fires['frp'].mean():.1f}, max MW={fires['frp'].max():.1f}")
print(f"RFS major incidents: features={len(rfs.get('features', []))}")
