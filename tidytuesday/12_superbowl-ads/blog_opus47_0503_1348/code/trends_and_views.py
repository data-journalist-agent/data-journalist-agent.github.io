"""Trends across years + view-count analyses for the Super Bowl ads dataset."""
import pandas as pd
import json

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/12_superbowl-ads/youtube.csv'

raw = pd.read_csv(DATA)
ads = raw.drop_duplicates(subset=['superbowl_ads_dot_com_url']).copy()
ads['brand'] = ads['brand'].replace({'Hynudai': 'Hyundai'})
raw['brand'] = raw['brand'].replace({'Hynudai': 'Hyundai'})

TRAITS = ['funny', 'show_product_quickly', 'patriotic', 'celebrity', 'danger', 'animals', 'use_sex']

# --- ana_07: Trait prevalence by year (3-year rolling era buckets for stability) ---
print("=== ana_07 ===")
# Compute % of ads with each trait per year
yearly = ads.groupby('year')[TRAITS].mean().round(3) * 100
yearly = yearly.round(1)
print("Yearly trait %:")
print(yearly.to_string())
print()

# --- ana_08: Era comparison — 2000-2009 vs 2010-2020 ---
print("=== ana_08 ===")
ads['era'] = ads['year'].apply(lambda y: '2000-2009' if y <= 2009 else '2010-2020')
era_means = ads.groupby('era')[TRAITS].mean().round(3) * 100
era_means = era_means.round(1)
print("Trait % by era:")
print(era_means.to_string())
print()
# Compute change
change = (era_means.loc['2010-2020'] - era_means.loc['2000-2009']).round(1)
print("Change (pp, 2010-2020 minus 2000-2009):")
print(change.sort_values())
print()

# --- ana_09: Use-sex collapse — the single largest trait change ---
print("=== ana_09 ===")
sex_by_year = ads.groupby('year')['use_sex'].mean().round(3) * 100
sex_by_year = sex_by_year.round(1)
print("use_sex % by year:")
for y, v in sex_by_year.items():
    print(f"  {int(y)}: {v}%")
e1 = ads[ads['year'] <= 2004]['use_sex'].mean() * 100
e2 = ads[ads['year'] >= 2016]['use_sex'].mean() * 100
print(f"\n2000-2004: {e1:.1f}% used sex")
print(f"2016-2020: {e2:.1f}% used sex")
print(f"Drop: {e1-e2:.1f} percentage points (~{(e1-e2)/e1*100:.0f}% relative decline)")
print()

# --- ana_10: Most-viewed ad in the dataset ---
print("=== ana_10 ===")
ranked = raw.dropna(subset=['view_count', 'title']).sort_values('view_count', ascending=False)
print("Top 10 by YouTube view count:")
for i, (_, r) in enumerate(ranked.head(10).iterrows(), 1):
    traits_on = [t for t in TRAITS if r[t]]
    print(f"  {i:>2d}. {int(r['year'])} {r['brand']:<14s} {int(r['view_count']):>11,d}  {str(r['title'])[:55]}")
    print(f"      traits: {','.join(traits_on) or '(none)'}  id={r['id']}")
print()

# --- ana_11: View count gap — how dominant is the #1 ad? ---
print("=== ana_11 ===")
top_views = float(ranked.iloc[0]['view_count'])
median_views = float(ranked['view_count'].median())
total_views = float(ranked['view_count'].sum())
print(f"Top ad views (Doritos Sling Baby 2012): {top_views:,.0f}")
print(f"Median ad views: {median_views:,.0f}")
print(f"Top ad / median: {top_views/median_views:.1f}x")
print(f"Top ad share of total views: {100*top_views/total_views:.1f}%")
top10 = ranked.head(10)['view_count'].sum()
print(f"Top 10 share of total views: {100*top10/total_views:.1f}%")
print()

# --- ana_12: Trait combinations — which 3-trait recipes recur? ---
print("=== ana_12 ===")
ads['recipe'] = ads[TRAITS].apply(lambda r: ','.join([t for t in TRAITS if r[t]]) or '(none)', axis=1)
top_recipes = ads['recipe'].value_counts().head(15)
print("Top 15 trait combinations:")
for combo, n in top_recipes.items():
    print(f"  {n:>3d}  {combo}")
print()

# --- ana_13: The Bud Light formula — funny + show_product_quickly is overwhelming ---
print("=== ana_13 ===")
bl = ads[ads['brand'] == 'Bud Light']
n = len(bl)
funny_pct = bl['funny'].mean() * 100
fast_pct = bl['show_product_quickly'].mean() * 100
both_pct = ((bl['funny']) & (bl['show_product_quickly'])).mean() * 100
print(f"Bud Light: {n} ads")
print(f"  funny:           {funny_pct:.1f}%")
print(f"  show product fast: {fast_pct:.1f}%")
print(f"  BOTH funny + fast:  {both_pct:.1f}%")
neither = ((~bl['funny']) & (~bl['show_product_quickly'])).mean() * 100
print(f"  NEITHER:        {neither:.1f}%")
print()

# --- ana_14: NFL is the outlier — never funny, never sex, never danger ---
print("=== ana_14 ===")
nfl = ads[ads['brand'] == 'NFL']
print(f"NFL: {len(nfl)} ads")
for t in TRAITS:
    pct = nfl[t].mean() * 100
    print(f"  {t:25s}: {pct:.1f}%")
print()

# --- ana_15: Funny vs serious — view count comparison ---
print("=== ana_15 ===")
mview = raw.dropna(subset=['view_count'])
print("Median views:")
print(f"  Funny ads:     {mview[mview['funny']]['view_count'].median():,.0f}")
print(f"  Not funny:     {mview[~mview['funny']]['view_count'].median():,.0f}")
print(f"  Animals:       {mview[mview['animals']]['view_count'].median():,.0f}")
print(f"  No animals:    {mview[~mview['animals']]['view_count'].median():,.0f}")
print(f"  Patriotic:     {mview[mview['patriotic']]['view_count'].median():,.0f}")
print(f"  Not patriotic: {mview[~mview['patriotic']]['view_count'].median():,.0f}")
print(f"  Celebrity:     {mview[mview['celebrity']]['view_count'].median():,.0f}")
print(f"  No celeb:      {mview[~mview['celebrity']]['view_count'].median():,.0f}")
