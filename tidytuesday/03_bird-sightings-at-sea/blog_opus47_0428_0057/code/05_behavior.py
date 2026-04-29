"""Behavior columns: feeding/sitting/following ship/accompanying. Ship-follower analysis."""
import pandas as pd
import numpy as np
import os

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/03_bird-sightings-at-sea"
birds = pd.read_csv(os.path.join(DATA, "birds.csv"))

# only records that actually observed birds
b = birds.dropna(subset=['species_common_name']).copy()
b['count_clean'] = b['count'].replace(99999, np.nan)

# --- ana_13: behaviour incidence rate (TRUE share among bird obs) ---
print("=== ana_13 ===")
behaviors = ['feeding','sitting_on_water','sitting_on_ice','sitting_on_ship','in_hand',
             'flying_past','accompanying','following_ship','moulting','naturally_feeding']
rows = []
for col in behaviors:
    vals = b[col].astype(str).str.upper()
    true_n = (vals=='TRUE').sum()
    pct = true_n/len(b)*100
    rows.append((col, int(true_n), round(pct,1)))
print(pd.DataFrame(rows, columns=['behavior','records_TRUE','pct']).to_string(index=False))

# --- ana_14: Top 10 ship-following species ---
print("=== ana_14 ===")
follow = b[b['following_ship'].astype(str).str.upper()=='TRUE']
top_follow = follow['species_common_name'].value_counts().head(10)
print(top_follow.to_string())
print(f"total ship-following obs: {len(follow)}")

# --- ana_15: Top 10 accompanying species ---
print("=== ana_15 ===")
accomp = b[b['accompanying'].astype(str).str.upper()=='TRUE']
top_acc = accomp['species_common_name'].value_counts().head(10)
print(top_acc.to_string())
print(f"total accompanying obs: {len(accomp)}")

# --- ana_16: feeding behaviour breakdown by species (top 10 species in dataset) ---
print("=== ana_16 ===")
top_species = b['species_common_name'].value_counts().head(10).index
sub = b[b['species_common_name'].isin(top_species)].copy()
piv = sub.groupby('species_common_name').apply(lambda d: pd.Series({
    'n_records': len(d),
    'pct_following_ship': (d['following_ship'].astype(str).str.upper()=='TRUE').mean()*100,
    'pct_accompanying':   (d['accompanying'].astype(str).str.upper()=='TRUE').mean()*100,
    'pct_sitting_on_water':(d['sitting_on_water'].astype(str).str.upper()=='TRUE').mean()*100,
    'pct_flying_past':    (d['flying_past'].astype(str).str.upper()=='TRUE').mean()*100,
    'pct_naturally_feeding':(d['naturally_feeding'].astype(str).str.upper()=='TRUE').mean()*100,
}), include_groups=False).reindex(top_species)
print(piv.round(1).to_string())
