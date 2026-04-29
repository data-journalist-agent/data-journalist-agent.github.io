"""Profile dataset: file sizes, row counts, column types, missing rates, time/space scope."""
import pandas as pd
import numpy as np
import os, json

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/03_bird-sightings-at-sea"

birds = pd.read_csv(os.path.join(DATA, "birds.csv"))
ships = pd.read_csv(os.path.join(DATA, "ships.csv"), parse_dates=["date"])
beaufort = pd.read_csv(os.path.join(DATA, "beaufort_scale.csv"))
sea = pd.read_csv(os.path.join(DATA, "sea_states.csv"))

# --- ana_01: dataset profile ---
print("=== ana_01 ===")
print(f"birds rows={len(birds)} cols={birds.shape[1]}")
print(f"ships rows={len(ships)} cols={ships.shape[1]}")
print(f"beaufort rows={len(beaufort)} cols={beaufort.shape[1]}")
print(f"sea_states rows={len(sea)} cols={sea.shape[1]}")
print(f"date range: {ships['date'].min().date()} to {ships['date'].max().date()}")
print(f"unique ship records (10-min censuses): {ships['record_id'].nunique()}")
print(f"unique birds.record_id: {birds['record_id'].nunique()}")
print(f"NA species_common_name (no-birds censuses): {birds['species_common_name'].isna().sum()}")
print(f"lat range: {ships['latitude'].min():.2f} to {ships['latitude'].max():.2f}")
print(f"lon range: {ships['longitude'].min():.2f} to {ships['longitude'].max():.2f}")

# --- ana_02: missing rates per ship column ---
print("=== ana_02 ===")
missing = (ships.isna().mean()*100).round(1).sort_values(ascending=False)
print(missing.to_string())
