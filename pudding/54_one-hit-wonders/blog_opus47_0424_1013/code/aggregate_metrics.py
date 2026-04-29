"""Aggregate metrics about one-hit wonders: spike ratios by league, peak distribution, timing, etc."""

import pandas as pd
import json
from collections import Counter

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/pudding/54_one-hit-wonders/data.csv"
OHW_JSON = "code/ohw_players.json"

df = pd.read_csv(DATA)
df['rank_eff'] = df['rank'].fillna(999)

with open(OHW_JSON) as f:
    ohws = json.load(f)
ohw_df = pd.DataFrame(ohws)

# --- ana_12: Peak rank distribution among OHWs ---
print("=== ana_12 ===")
bins = [0, 5, 10, 15, 20]
labels = ['1-5','6-10','11-15','16-20']
ohw_df['peak_bucket'] = pd.cut(ohw_df['peak_rank'], bins=bins, labels=labels, include_lowest=True)
peak_dist = ohw_df['peak_bucket'].value_counts().reindex(labels).fillna(0).astype(int)
print(peak_dist.to_string())
print()

# --- ana_13: How far do OHWs fall? Spike ratio stats by league ---
print("=== ana_13 ===")
ohw_df['spike_ratio'] = ohw_df['median_rank'] / ohw_df['peak_rank']
ohw_df['gap'] = ohw_df['median_rank'] - ohw_df['peak_rank']
agg = ohw_df.groupby('league').agg(
    n=('id','size'),
    median_spike=('spike_ratio','median'),
    median_gap=('gap','median'),
    worst_drop=('worst_rank','max'),
).round(1)
print(agg)
print()

# --- ana_14: Career length of OHWs vs non-OHWs ---
print("=== ana_14 ===")
seasons_per = df.groupby(['league','id']).size().reset_index(name='seasons')
ohw_ids = set(ohw_df['id'])
seasons_per['is_ohw'] = seasons_per['id'].isin(ohw_ids)
cmp = seasons_per.groupby('is_ohw')['seasons'].agg(['mean','median','count']).round(2)
print(cmp)
print()

# --- ana_15: When (what career year) did the peak happen? ---
print("=== ana_15 ===")
# Join back to main data to get year_index at peak
ohw_peak_years = []
for _, r in ohw_df.iterrows():
    sub = df[(df['league']==r['league']) & (df['id']==r['id']) & (df['year']==r['peak_year'])]
    if not sub.empty:
        ohw_peak_years.append({
            'league': r['league'], 'name': r['name'],
            'year_index': int(sub.iloc[0]['year_index']),
            'peak_year': int(r['peak_year']),
        })
pk = pd.DataFrame(ohw_peak_years)
print(pk['year_index'].describe())
print()
print("peak at year_index bucket:")
buckets = pd.cut(pk['year_index'], bins=[-1,1,3,6,10,30], labels=['year 1','2-3','4-6','7-10','11+'])
print(buckets.value_counts().sort_index())
print()

# --- ana_16: Year-over-year drop from peak to next season ---
print("=== ana_16 ===")
drops = []
for _, r in ohw_df.iterrows():
    sub = df[(df['league']==r['league']) & (df['id']==r['id'])].sort_values('year')
    peak_year = int(r['peak_year'])
    if peak_year + 1 in sub['year'].values:
        nxt = sub[sub['year']==peak_year+1].iloc[0]
        nxt_rank = 999 if pd.isna(nxt['rank']) else float(nxt['rank'])
        drops.append({
            'league': r['league'],
            'name': r['name'],
            'peak_rank': float(r['peak_rank']),
            'next_rank': nxt_rank,
            'drop': nxt_rank - float(r['peak_rank']),
        })
dr = pd.DataFrame(drops)
print(f"N with next-year data: {len(dr)}")
print(f"median drop peak→next: {dr['drop'].median():.0f} ranks")
print(f"mean drop: {dr['drop'].mean():.0f} ranks")
print()
print("by league:")
print(dr.groupby('league')['drop'].agg(['median','mean','count']).round(0))
print()

# --- ana_17: Distribution of peak year across decades ---
print("=== ana_17 ===")
pk['decade'] = (pk['peak_year'] // 10 * 10)
dec = pk.groupby('decade').size().reset_index(name='ohw_count')
print(dec.to_string(index=False))
print()

# --- ana_18: The ten most extreme OHWs (biggest gap) — names for the blog ---
print("=== ana_18 ===")
top_extreme = ohw_df.nlargest(15, 'gap')[['league','name','peak_year','peak_rank','median_rank','worst_rank','gap','spike_ratio']]
print(top_extreme.to_string(index=False))
print()

# --- ana_19: Pudding-highlighted canonical OHWs: confirm they fit the definition ---
print("=== ana_19 ===")
CANONICAL = [('nba','Dana Barros'), ('mlb','Dontrelle Willis'), ('nhl','Jiri Hudler'),
             ('pga','Rich Beem'), ('lpga','Hilary Lunke'), ('atp','Martin Verkerk'),
             ('wta','Karolina Sprem'), ('wnba','Tracy Reid')]
for league, name in CANONICAL:
    m = ohw_df[(ohw_df['league']==league) & (ohw_df['name']==name)]
    if m.empty:
        print(f"{league:5s} {name:20s}  NOT in strict OHW set")
    else:
        r = m.iloc[0]
        print(f"{league:5s} {name:20s} peak={int(r['peak_rank']):3d} median={int(r['median_rank']):4d} seasons={int(r['seasons'])}")
print()

# --- ana_20: All 78 OHWs, for a complete table/gallery ---
print("=== ana_20 ===")
out = ohw_df[['league','name','peak_year','peak_rank','median_rank','worst_rank','seasons']].copy()
out['peak_rank'] = out['peak_rank'].astype(int)
out['median_rank'] = out['median_rank'].astype(int)
out['worst_rank'] = out['worst_rank'].astype(int)
out['seasons'] = out['seasons'].astype(int)
out = out.sort_values(['league','peak_rank'])
print(out.to_string(index=False))
