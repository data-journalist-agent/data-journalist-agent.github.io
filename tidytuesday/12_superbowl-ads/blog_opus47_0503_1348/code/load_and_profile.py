"""Profile + dataset-level analyses for the Super Bowl ads dataset."""
import pandas as pd
import json
import sys

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/12_superbowl-ads/youtube.csv'

raw = pd.read_csv(DATA)

# De-duplicate to ad-level for trait analyses (the same ad can appear with multiple uploads)
ads = raw.drop_duplicates(subset=['superbowl_ads_dot_com_url']).copy()
ads['brand'] = ads['brand'].replace({'Hynudai': 'Hyundai'})  # fix the CSV typo
raw['brand'] = raw['brand'].replace({'Hynudai': 'Hyundai'})

TRAITS = ['funny', 'show_product_quickly', 'patriotic', 'celebrity', 'danger', 'animals', 'use_sex']

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"Raw rows: {len(raw)}")
print(f"Unique ads (de-duplicated by superbowl_ads_dot_com_url): {len(ads)}")
print(f"Year range: {int(ads['year'].min())} - {int(ads['year'].max())}")
print(f"Number of brands: {ads['brand'].nunique()}")
print(f"Brands: {sorted(ads['brand'].unique().tolist())}")
print()

# --- ana_02: Trait prevalence across all ads ---
print("=== ana_02 ===")
trait_counts = {t: int(ads[t].sum()) for t in TRAITS}
trait_pct = {t: round(100 * ads[t].mean(), 1) for t in TRAITS}
for t in TRAITS:
    print(f"  {t:25s} {trait_counts[t]:>4d} / {len(ads)}  ({trait_pct[t]}%)")
print()

# --- ana_03: How many traits does the average ad have? ---
print("=== ana_03 ===")
ads['trait_count'] = ads[TRAITS].sum(axis=1)
print(f"Mean traits per ad: {ads['trait_count'].mean():.2f}")
print(f"Median: {ads['trait_count'].median()}")
print(f"Distribution of trait_count:")
dist = ads['trait_count'].value_counts().sort_index()
for n, c in dist.items():
    print(f"  {int(n)} traits: {int(c)} ads ({100*c/len(ads):.1f}%)")
zero = int((ads['trait_count'] == 0).sum())
five_plus = int((ads['trait_count'] >= 5).sum())
print(f"Ads with 0 traits: {zero}")
print(f"Ads with 5+ traits: {five_plus}")
print()

# --- ana_04: Brand volume — top 10 most-prolific (already de-duplicated by ad) ---
print("=== ana_04 ===")
brand_volume = ads['brand'].value_counts()
print("Ads per brand:")
for b, c in brand_volume.items():
    print(f"  {b:14s} {int(c):>3d}")
print()

# --- ana_05: Ads per year — total volume across all 10 brands ---
print("=== ana_05 ===")
year_volume = ads.groupby('year').size()
print("Ads per year (total across the 10 brands):")
for y, c in year_volume.items():
    print(f"  {int(y)}: {int(c)}")
print(f"Mean ads per year: {year_volume.mean():.1f}")
print(f"Min year: {year_volume.idxmin()} ({year_volume.min()}); Max year: {year_volume.idxmax()} ({year_volume.max()})")
print()

# --- ana_06: Brand x trait — fingerprint of each top brand ---
print("=== ana_06 ===")
top_brands = brand_volume.head(10).index.tolist()
print(f"{'brand':<14s} " + ' '.join(f"{t[:6]:>7s}" for t in TRAITS))
brand_trait = {}
for b in top_brands:
    sub = ads[ads['brand'] == b]
    row = []
    bdict = {}
    for t in TRAITS:
        pct = round(100 * sub[t].mean(), 1)
        row.append(pct)
        bdict[t] = pct
    brand_trait[b] = bdict
    print(f"{b:<14s} " + ' '.join(f"{v:>6.1f}%" for v in row))
print()

# Save brand-trait table for designer
with open('/tmp/brand_trait.json', 'w') as f:
    json.dump(brand_trait, f, indent=2)
