"""Compute year-by-year trajectories for canonical one-hit wonders named in the article."""

import pandas as pd
import json

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/pudding/54_one-hit-wonders/data.csv"

df = pd.read_csv(DATA)
df['rank_eff'] = df['rank'].fillna(999)

CANONICAL = [
    ('nba',  'Dana Barros'),
    ('mlb',  'Dontrelle Willis'),
    ('nhl',  'Jiri Hudler'),
    ('pga',  'Rich Beem'),
    ('lpga', 'Hilary Lunke'),
    ('atp',  'Martin Verkerk'),
    ('wta',  'Karolina Sprem'),
    ('wnba', 'Tracy Reid'),
]

# --- ana_08: Career trajectories for canonical OHWs ---
print("=== ana_08 ===")
all_traj = {}
for league, name in CANONICAL:
    sub = df[(df['league']==league) & (df['name']==name)].sort_values('year')
    if sub.empty:
        # Try partial match
        candidates = df[(df['league']==league) & df['name'].str.contains(name.split()[-1], na=False)]['name'].unique()
        print(f"!! no match for {name} ({league}); candidates: {list(candidates)[:5]}")
        continue
    rows = []
    for _, r in sub.iterrows():
        rows.append({
            'year': int(r['year']),
            'year_index': int(r['year_index']),
            'rank': None if pd.isna(r['rank']) else int(r['rank']),
            'total_players': int(r['total_players']) if not pd.isna(r['total_players']) else None,
            'stat_val': None if pd.isna(r['stat_val']) else float(r['stat_val']),
            'stat_prop': r['stat_prop'] if pd.notna(r['stat_prop']) else None,
            'played_val': None if pd.isna(r['played_val']) else float(r['played_val']),
            'team': r['team'] if pd.notna(r['team']) else None,
            'dnp': bool(r['dnp']) if pd.notna(r['dnp']) else False,
        })
    all_traj[f"{league}:{name}"] = rows
    peak = sub.loc[sub['rank_eff'].idxmin()]
    print(f"{name} ({league}): {len(rows)} seasons, peak={int(peak['rank_eff'])} in {int(peak['year'])}")

with open('code/canonical_trajectories.json','w') as f:
    json.dump(all_traj, f, indent=2)

# --- ana_09: Detailed Dana Barros career ---
print("=== ana_09 ===")
sub = df[(df['league']=='nba') & (df['name']=='Dana Barros')].sort_values('year')
print(sub[['year','rank','stat_val','played_val','team']].to_string(index=False))

# --- ana_10: Detailed Dontrelle Willis career ---
print("=== ana_10 ===")
sub = df[(df['league']=='mlb') & (df['name']=='Dontrelle Willis')].sort_values('year')
print(sub[['year','rank','stat_val','played_val','team']].to_string(index=False))

# --- ana_11: Detailed Rich Beem career ---
print("=== ana_11 ===")
sub = df[(df['league']=='pga') & (df['name']=='Rich Beem')].sort_values('year')
print(sub[['year','rank','stat_val','played_val','team']].to_string(index=False))
