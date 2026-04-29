"""Spatial patterns: lat/lon density grid; map-ready data."""
import pandas as pd
import numpy as np
import os

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/03_bird-sightings-at-sea"
ships = pd.read_csv(os.path.join(DATA, "ships.csv"))
birds = pd.read_csv(os.path.join(DATA, "birds.csv"))

birds['count_clean'] = birds['count'].replace(99999, np.nan)
# ship-record level totals
ship_birds = birds.groupby('record_id')['count_clean'].sum().rename('birds_total').reset_index()
ships2 = ships.merge(ship_birds, on='record_id', how='left').fillna({'birds_total':0})
ships2 = ships2.dropna(subset=['latitude','longitude'])

# --- ana_10: lat/lon coverage ---
print("=== ana_10 ===")
print(f"lat min/max: {ships2['latitude'].min():.2f} / {ships2['latitude'].max():.2f}")
print(f"lon min/max: {ships2['longitude'].min():.2f} / {ships2['longitude'].max():.2f}")

# --- ana_11: gridded density (5-deg cells), top cells by census count and by bird sum ---
print("=== ana_11 ===")
ships2['lat_bin'] = (np.floor(ships2['latitude']/5)*5).astype(int)
ships2['lon_bin'] = (np.floor(ships2['longitude']/5)*5).astype(int)
grid = ships2.groupby(['lat_bin','lon_bin']).agg(
    n_censuses=('record_id','count'),
    sum_birds=('birds_total','sum')
).reset_index().sort_values('n_censuses', ascending=False)
print(grid.head(20).to_string(index=False))
print(f"total non-empty cells: {len(grid)}")

# Save grid for designer/programmer (top 60 cells)
grid_top = grid.head(60).copy()
grid_top.to_csv("/Users/forrest/Desktop/data2blog/project/tidytuesday/03_bird-sightings-at-sea/blog_opus47_0428_0057/code/grid_top60.csv", index=False)

# --- ana_12: lat band aggregation ---
print("=== ana_12 ===")
ships2['lat_band'] = pd.cut(ships2['latitude'], bins=[-70,-60,-50,-40,-30,-20,-10,0,10,20,30],
                             labels=['-70 to -60','-60 to -50','-50 to -40','-40 to -30','-30 to -20','-20 to -10','-10 to 0','0 to 10','10 to 20','20 to 30'])
lb = ships2.groupby('lat_band', observed=True).size().rename('censuses')
print(lb.to_string())
