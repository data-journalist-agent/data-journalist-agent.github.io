"""Generate chart-ready data_tables as JSON for the analyst to include."""

import pandas as pd
import json

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/pudding/54_one-hit-wonders/data.csv"
OHW_JSON = "code/ohw_players.json"

df = pd.read_csv(DATA)
df['rank_eff'] = df['rank'].fillna(999)

with open(OHW_JSON) as f:
    ohws = json.load(f)
ohw_df = pd.DataFrame(ohws)

tables = {}

# DATA TABLE A: League share
by_league = df.groupby('league').agg(players=('id','nunique'), rows=('id','size')).reset_index()
seasons_per = df.groupby(['league','id']).size().reset_index(name='seasons')
eligible = seasons_per[seasons_per['seasons']>=5].groupby('league').size().reset_index(name='eligible')
ohw_counts = ohw_df.groupby('league').size().reset_index(name='ohw')
dt = by_league.merge(eligible, on='league', how='left').merge(ohw_counts, on='league', how='left').fillna(0)
dt['ohw_pct'] = (100*dt['ohw']/dt['eligible']).round(1)
dt = dt.sort_values('ohw_pct', ascending=False)
tables['league_breakdown'] = {
    'columns': ['league','players','eligible','ohw','ohw_pct'],
    'rows': dt[['league','players','eligible','ohw','ohw_pct']].values.tolist(),
}

# DATA TABLE B: Peak-rank bucket distribution
ohw_df['peak_bucket'] = pd.cut(ohw_df['peak_rank'], bins=[0,5,10,15,20], labels=['1-5','6-10','11-15','16-20'], include_lowest=True)
pkd = ohw_df['peak_bucket'].value_counts().reindex(['1-5','6-10','11-15','16-20']).fillna(0).astype(int)
tables['peak_distribution'] = {
    'columns': ['peak_rank_bucket','count'],
    'rows': [[b, int(pkd[b])] for b in pkd.index],
}

# DATA TABLE C: Spike ratio by league
ohw_df['spike_ratio'] = ohw_df['median_rank'] / ohw_df['peak_rank']
ohw_df['gap'] = ohw_df['median_rank'] - ohw_df['peak_rank']
sp = ohw_df.groupby('league').agg(
    n=('id','size'),
    median_spike=('spike_ratio','median'),
    median_gap=('gap','median'),
).round(1).reset_index().sort_values('median_spike', ascending=False)
tables['spike_by_league'] = {
    'columns': ['league','n','median_spike','median_gap'],
    'rows': sp[['league','n','median_spike','median_gap']].values.tolist(),
}

# DATA TABLE D: OHW peak year_index (when in their career)
ohw_peak_years = []
for _, r in ohw_df.iterrows():
    sub = df[(df['league']==r['league']) & (df['id']==r['id']) & (df['year']==r['peak_year'])]
    if not sub.empty:
        ohw_peak_years.append({'year_index': int(sub.iloc[0]['year_index'])})
pk = pd.DataFrame(ohw_peak_years)
buckets = pd.cut(pk['year_index'], bins=[-1,1,3,6,10,30], labels=['year 1','year 2-3','year 4-6','year 7-10','year 11+'])
bc = buckets.value_counts().sort_index()
tables['peak_when'] = {
    'columns': ['career_year_bucket','count'],
    'rows': [[b, int(bc[b])] for b in bc.index],
}

# DATA TABLE E: Peak decade
pk_all = []
for _, r in ohw_df.iterrows():
    pk_all.append({'peak_year': int(r['peak_year'])})
pka = pd.DataFrame(pk_all)
pka['decade'] = (pka['peak_year'] // 10 * 10).astype(int)
dec = pka.groupby('decade').size().reset_index(name='count')
tables['peak_decade'] = {
    'columns': ['decade','count'],
    'rows': dec.values.tolist(),
}

# DATA TABLE F: Canonical player year-by-year trajectories
CANONICAL = [('nba','Dana Barros','VORP'),
             ('mlb','Dontrelle Willis','WAR'),
             ('nhl','Jiri Hudler','Point Shares'),
             ('pga','Rich Beem','Earnings ($)'),
             ('lpga','Hilary Lunke','Earnings ($)'),
             ('atp','Martin Verkerk','Ranking Pts'),
             ('wta','Karolina Sprem','Ranking Pts'),
             ('wnba','Tracy Reid','VORP')]
traj = {}
for league, name, stat_label in CANONICAL:
    sub = df[(df['league']==league) & (df['name']==name)].sort_values('year')
    rows = []
    for _, r in sub.iterrows():
        rank = None if pd.isna(r['rank']) else int(r['rank'])
        stat_val = None if pd.isna(r['stat_val']) else float(r['stat_val'])
        rows.append([int(r['year']), int(r['year_index']), rank, stat_val])
    traj[f"{league}:{name}"] = {
        'stat_label': stat_label,
        'columns': ['year','year_index','rank','stat_val'],
        'rows': rows,
    }
tables['canonical_trajectories'] = traj

# DATA TABLE G: Top 15 most extreme OHWs (biggest gap)
top = ohw_df.nlargest(15, 'gap')[['league','name','peak_year','peak_rank','median_rank','worst_rank','gap']]
tables['most_extreme_ohws'] = {
    'columns': ['league','name','peak_year','peak_rank','median_rank','worst_rank','gap'],
    'rows': [[r['league'], r['name'], int(r['peak_year']), int(r['peak_rank']),
              int(r['median_rank']), int(r['worst_rank']), int(r['gap'])] for _, r in top.iterrows()],
}

# DATA TABLE H: Full OHW roster (all 78)
full = ohw_df.sort_values(['league','peak_rank'])[['league','name','peak_year','peak_rank','median_rank','worst_rank','seasons']]
tables['all_ohws'] = {
    'columns': ['league','name','peak_year','peak_rank','median_rank','worst_rank','seasons'],
    'rows': [[r['league'], r['name'], int(r['peak_year']), int(r['peak_rank']),
              int(r['median_rank']), int(r['worst_rank']), int(r['seasons'])] for _, r in full.iterrows()],
}

# DATA TABLE I: Year-over-year drop distribution (peak to next season)
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
dr_by_league = dr.groupby('league')['drop'].agg(['median','count']).round(0).reset_index().sort_values('median', ascending=False)
tables['next_year_drop'] = {
    'columns': ['league','median_drop','n'],
    'rows': [[r['league'], int(r['median']), int(r['count'])] for _, r in dr_by_league.iterrows()],
}

# DATA TABLE J: Peak rank exact distribution (histogram)
peak_counts = ohw_df['peak_rank'].astype(int).value_counts().sort_index()
tables['peak_rank_exact'] = {
    'columns': ['peak_rank','count'],
    'rows': [[int(k), int(v)] for k,v in peak_counts.items()],
}

# DATA TABLE K: Players per league — eligible vs OHW vs non-OHW vs short
seasons_per['short_career'] = seasons_per['seasons'] < 5
short_by_league = seasons_per.groupby('league')['short_career'].sum().reset_index(name='short')
eligible_by_league = seasons_per[seasons_per['seasons']>=5].groupby('league').size().reset_index(name='eligible')
lg_all = short_by_league.merge(eligible_by_league, on='league', how='outer').merge(ohw_counts, on='league', how='outer').fillna(0)
lg_all['non_ohw'] = lg_all['eligible'] - lg_all['ohw']
lg_all = lg_all[['league','short','non_ohw','ohw']].fillna(0)
tables['pool_breakdown'] = {
    'columns': ['league','short_career','eligible_non_ohw','ohw'],
    'rows': [[r['league'], int(r['short']), int(r['non_ohw']), int(r['ohw'])] for _, r in lg_all.iterrows()],
}

with open('code/data_tables.json','w') as f:
    json.dump(tables, f, indent=2, default=str)
print("Saved data tables")
for k, v in tables.items():
    if 'rows' in v:
        print(f"  {k}: {len(v['rows'])} rows")
    else:
        print(f"  {k}: {len(v)} entries")
