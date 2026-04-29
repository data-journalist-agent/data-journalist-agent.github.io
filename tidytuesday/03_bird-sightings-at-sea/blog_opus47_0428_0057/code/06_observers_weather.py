"""Observers, ships activity, wind/Beaufort vs sea state."""
import pandas as pd
import numpy as np
import os

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/03_bird-sightings-at-sea"
ships = pd.read_csv(os.path.join(DATA, "ships.csv"))
birds = pd.read_csv(os.path.join(DATA, "birds.csv"))
beaufort = pd.read_csv(os.path.join(DATA, "beaufort_scale.csv"))

birds['count_clean'] = birds['count'].replace(99999, np.nan)
ship_birds = birds.groupby('record_id')['count_clean'].sum().rename('birds_total').reset_index()
ships2 = ships.merge(ship_birds, on='record_id', how='left').fillna({'birds_total':0})

# --- ana_17: observers concentration ---
print("=== ana_17 ===")
obs = ships2['observer'].value_counts().rename('censuses').reset_index().rename(columns={'index':'observer'})
obs.columns = ['observer','censuses']
print(f"unique observers: {len(obs)}")
print("top 10 observers:")
print(obs.head(10).to_string(index=False))
total = obs['censuses'].sum()
top1 = obs.iloc[0]['censuses']/total*100
top5 = obs.head(5)['censuses'].sum()/total*100
top10 = obs.head(10)['censuses'].sum()/total*100
print(f"top1 share: {top1:.1f}%; top5 share: {top5:.1f}%; top10 share: {top10:.1f}%")

# --- ana_18: ship activity ---
print("=== ana_18 ===")
act = ships2['activity'].value_counts(dropna=False)
print(act.to_string())

# --- ana_19: wind speed class distribution and join to beaufort labels ---
print("=== ana_19 ===")
wd = ships2['wind_speed_class'].value_counts(dropna=False).sort_index()
labels = beaufort.set_index('wind_speed_class')['wind_description'].to_dict()
mins = beaufort.set_index('wind_speed_class')['wind_speed_knots_min'].to_dict()
maxs = beaufort.set_index('wind_speed_class')['wind_speed_knots_max'].to_dict()
rows = []
for k, n in wd.items():
    if pd.isna(k):
        rows.append(('NA','—', int(n)))
    else:
        ki=int(k)
        rows.append((ki, labels.get(ki,'?'), int(n)))
print(pd.DataFrame(rows, columns=['class','label','n']).to_string(index=False))

# --- ana_20: mean birds per census by wind speed class (only records with birds_total>0) ---
print("=== ana_20 ===")
# include zero-bird ships too as 0 — but cleaner: drop NA wind
sub = ships2.dropna(subset=['wind_speed_class']).copy()
sub['wind_speed_class'] = sub['wind_speed_class'].astype(int)
agg = sub.groupby('wind_speed_class').agg(n_censuses=('record_id','count'),
                                          mean_birds=('birds_total','mean'),
                                          median_birds=('birds_total','median')).reset_index()
agg['label'] = agg['wind_speed_class'].map(labels)
print(agg.round(2).to_string(index=False))
