"""Temporal patterns: per-year effort, gap years, peak years, seasonality."""
import pandas as pd
import os

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/03_bird-sightings-at-sea"
ships = pd.read_csv(os.path.join(DATA, "ships.csv"), parse_dates=["date"])
ships['year'] = ships['date'].dt.year

# --- ana_07: censuses per year ---
print("=== ana_07 ===")
yr = ships.groupby('year').size().rename('censuses').reset_index()
all_years = pd.DataFrame({'year': range(int(ships['year'].min()), int(ships['year'].max())+1)})
yr_full = all_years.merge(yr, how='left').fillna({'censuses': 0})
yr_full['censuses'] = yr_full['censuses'].astype(int)
print(yr_full.to_string(index=False))
print(f"peak year: {yr_full.loc[yr_full['censuses'].idxmax()].to_dict()}")
print(f"zero-effort years: {yr_full[yr_full['censuses']==0]['year'].tolist()}")

# --- ana_08: censuses by season ---
print("=== ana_08 ===")
season_order = ['summer','autumn','winter','spring']
sc = ships['season'].value_counts().reindex(season_order)
print(sc.to_string())

# --- ana_09: census method (full vs partial) ---
print("=== ana_09 ===")
cm = ships['census_method'].value_counts(dropna=False)
print(cm.to_string())
print(f"full pct: {cm.get('full',0)/len(ships)*100:.1f}%")
print(f"partial pct: {cm.get('partial',0)/len(ships)*100:.1f}%")
