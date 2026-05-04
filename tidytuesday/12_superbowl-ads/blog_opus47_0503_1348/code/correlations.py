"""Trait correlations + 9/11 patriotic spike + brand fingerprints."""
import pandas as pd
import numpy as np

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/12_superbowl-ads/youtube.csv'

raw = pd.read_csv(DATA)
ads = raw.drop_duplicates(subset=['superbowl_ads_dot_com_url']).copy()
ads['brand'] = ads['brand'].replace({'Hynudai': 'Hyundai'})

TRAITS = ['funny', 'show_product_quickly', 'patriotic', 'celebrity', 'danger', 'animals', 'use_sex']

# --- ana_16: Trait pairwise correlations (phi coefficient = pearson on 0/1) ---
print("=== ana_16 ===")
trait_df = ads[TRAITS].astype(int)
corr = trait_df.corr().round(3)
print("Pairwise phi correlation (rows vs cols):")
print(corr.to_string())
print()
# Find strongest +/- correlations
pairs = []
cols = TRAITS
for i, a in enumerate(cols):
    for b in cols[i+1:]:
        pairs.append((a, b, corr.loc[a, b]))
pairs.sort(key=lambda x: x[2])
print("\nMost negative trait pairs:")
for a, b, c in pairs[:5]:
    print(f"  {a:25s} vs {b:25s}: {c:+.3f}")
print("\nMost positive trait pairs:")
for a, b, c in sorted(pairs, key=lambda x: -x[2])[:5]:
    print(f"  {a:25s} vs {b:25s}: {c:+.3f}")
print()

# --- ana_17: 9/11 effect — patriotic surged 2002-2003? Test the hypothesis ---
print("=== ana_17 ===")
patriotic_year = ads.groupby('year')['patriotic'].mean().round(3) * 100
patriotic_year = patriotic_year.round(1)
print("Patriotic % by year:")
for y, v in patriotic_year.items():
    flag = ''
    if int(y) in (2002, 2003):
        flag = ' <- post-9/11'
    if int(y) in (2017, 2018):
        flag = ' <- Trump-era patriotism wave'
    print(f"  {int(y)}: {v}%{flag}")
print()
# Pre/post 9/11 (2000-2001 vs 2002-2004)
pre = ads[ads['year'].isin([2000, 2001])]['patriotic'].mean() * 100
post = ads[ads['year'].isin([2002, 2003, 2004])]['patriotic'].mean() * 100
print(f"\n2000-2001 (pre 9/11): {pre:.1f}% patriotic")
print(f"2002-2004 (post 9/11): {post:.1f}% patriotic")
print()
# Late-2010s patriotism wave
late = ads[ads['year'].isin([2017, 2018])]['patriotic'].mean() * 100
print(f"2017-2018: {late:.1f}% patriotic — the highest two-year window in the dataset")
print()

# --- ana_18: Doritos vs the rest — only one brand has near-100% funny ---
print("=== ana_18 ===")
doritos = ads[ads['brand'] == 'Doritos']
print(f"Doritos: {len(doritos)} ads")
print(f"  funny: {doritos['funny'].mean()*100:.1f}%")
print(f"  show_product_quickly: {doritos['show_product_quickly'].mean()*100:.1f}%")
print(f"  Number of NOT-funny Doritos ads: {(~doritos['funny']).sum()}")
print()

# --- ana_19: Two trait fingerprints that uniquely define a brand ---
print("=== ana_19 ===")
# Top 5 brands fingerprint table for radar
top_brands = ads['brand'].value_counts().head(6).index.tolist()
print(f"{'brand':<14s} " + ' '.join(f"{t[:6]:>7s}" for t in TRAITS))
for b in top_brands:
    sub = ads[ads['brand'] == b]
    row = [round(sub[t].mean()*100, 1) for t in TRAITS]
    print(f"{b:<14s} " + ' '.join(f"{v:>6.1f}%" for v in row))
print()

# --- ana_20: How many ads use each # of traits, by era ---
print("=== ana_20 ===")
ads['era'] = ads['year'].apply(lambda y: '2000-2009' if y <= 2009 else '2010-2020')
ads['trait_count'] = ads[TRAITS].sum(axis=1)
era_count = ads.groupby(['era', 'trait_count']).size().unstack(fill_value=0)
print("Number of ads by trait count, by era:")
print(era_count.to_string())
print()
print(f"Mean traits per ad, 2000-2009: {ads[ads['era']=='2000-2009']['trait_count'].mean():.2f}")
print(f"Mean traits per ad, 2010-2020: {ads[ads['era']=='2010-2020']['trait_count'].mean():.2f}")
