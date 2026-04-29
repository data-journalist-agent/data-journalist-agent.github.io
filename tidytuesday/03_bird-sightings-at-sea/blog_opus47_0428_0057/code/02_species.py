"""Species composition: top species, taxonomic concentration, aggregates."""
import pandas as pd
import numpy as np
import os

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/03_bird-sightings-at-sea"
birds = pd.read_csv(os.path.join(DATA, "birds.csv"))

# Filter sentinel 99999 from count for sums
birds['count_clean'] = birds['count'].replace(99999, np.nan)

# Drop NA species (no-birds censuses) for species ranking
species_obs = birds.dropna(subset=['species_common_name']).copy()

# --- ana_03: top 15 species by record count ---
print("=== ana_03 ===")
top15 = species_obs['species_common_name'].value_counts().head(15)
print(top15)
total_records = len(species_obs)
print(f"total non-empty bird obs records: {total_records}")
print(f"unique species_common_name strings: {species_obs['species_common_name'].nunique()}")

# --- ana_04: top 15 species by total bird count ---
print("=== ana_04 ===")
sums = species_obs.groupby('species_common_name')['count_clean'].sum().sort_values(ascending=False).head(15)
print(sums)
print(f"total birds counted (excluding sentinels): {species_obs['count_clean'].sum():.0f}")
print(f"records flagged 99999: {(birds['count']==99999).sum()}")

# --- ana_05: aggregates (slash entries) share ---
print("=== ana_05 ===")
agg_mask = species_obs['species_scientific_name'].str.contains('/', na=False)
agg_count = agg_mask.sum()
print(f"aggregate (slash) records: {agg_count} ({agg_count/len(species_obs)*100:.1f}%)")
single = (~agg_mask).sum()
print(f"single-species records: {single} ({single/len(species_obs)*100:.1f}%)")

# --- ana_06: no-birds census rate ---
print("=== ana_06 ===")
no_bird = birds['species_common_name'].isna().sum()
total = len(birds)
print(f"no-birds censuses: {no_bird} of {total} ({no_bird/total*100:.1f}%)")
