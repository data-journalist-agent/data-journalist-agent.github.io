"""Identify one-hit wonders using the Pudding's definition.

Rule (per Pudding):
- Player must have played >= 5 seasons
- Exactly ONE season with rank in top-20
- ALL other seasons outside top-50 (rank > 50) — i.e. zero top-50 finishes outside the peak year
- DNP seasons (rank null) are counted as 'outside top-50' since the player didn't register.

We implement this per league.
"""

import pandas as pd
import json
from pathlib import Path

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/pudding/54_one-hit-wonders/data.csv"
OUT_JSON = "code/ohw_players.json"

df = pd.read_csv(DATA)

# Normalize rank: NaN -> large sentinel (we treat as 'outside top-50')
df['rank_eff'] = df['rank'].fillna(999)

def classify(group):
    ranks = group['rank_eff'].tolist()
    seasons = len(ranks)
    top20 = sum(1 for r in ranks if r <= 20)
    top50 = sum(1 for r in ranks if r <= 50)
    peak_idx = group['rank_eff'].idxmin()
    peak_year = int(group.loc[peak_idx, 'year'])
    peak_rank = float(group.loc[peak_idx, 'rank_eff'])
    median_rank = float(group['rank_eff'].median())
    worst = float(group['rank_eff'].max())
    # One-hit wonder:
    is_ohw = (seasons >= 5) and (top20 == 1) and (top50 == 1)
    return pd.Series({
        'seasons': seasons,
        'top20_count': top20,
        'top50_count': top50,
        'peak_year': peak_year,
        'peak_rank': peak_rank,
        'median_rank': median_rank,
        'worst_rank': worst,
        'is_ohw': is_ohw,
    })

player_summary = df.groupby(['league','id','name'], as_index=False).apply(
    classify, include_groups=False
).reset_index(drop=True)

# --- ana_05: Overall one-hit wonder counts ---
print("=== ana_05 ===")
total_eligible = (player_summary['seasons'] >= 5).sum()
ohw_total = player_summary['is_ohw'].sum()
print(f"players total: {len(player_summary)}")
print(f"players with >=5 seasons (eligible): {total_eligible}")
print(f"one-hit wonders: {ohw_total}")
print(f"ohw share of eligible: {100*ohw_total/total_eligible:.1f}%")
print()

# --- ana_06: One-hit wonders by league ---
print("=== ana_06 ===")
eligible = player_summary[player_summary['seasons'] >= 5]
by_league = eligible.groupby('league').agg(
    eligible=('id','size'),
    ohw=('is_ohw','sum'),
).reset_index()
by_league['pct'] = (100 * by_league['ohw'] / by_league['eligible']).round(1)
by_league = by_league.sort_values('pct', ascending=False)
print(by_league.to_string(index=False))
print()

# --- ana_07: The ten most extreme OHWs overall (biggest gap peak vs median) ---
print("=== ana_07 ===")
ohw = player_summary[player_summary['is_ohw']].copy()
ohw['spike_ratio'] = ohw['median_rank'] / ohw['peak_rank']
ohw['gap_peak_median'] = ohw['median_rank'] - ohw['peak_rank']
top10 = ohw.sort_values('gap_peak_median', ascending=False).head(10)
print(top10[['league','name','peak_year','peak_rank','median_rank','worst_rank','seasons','spike_ratio']].to_string(index=False))
print()

# Save list for downstream
ohw_records = ohw.to_dict(orient='records')
Path('code').mkdir(exist_ok=True)
with open(OUT_JSON, 'w') as f:
    json.dump(ohw_records, f, default=float, indent=2)
print(f"saved {len(ohw_records)} ohws to {OUT_JSON}")
