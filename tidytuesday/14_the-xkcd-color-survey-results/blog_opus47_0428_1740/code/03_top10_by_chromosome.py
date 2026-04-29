"""For each of the top-10 most popular colors, compute rank-1 agreement
by chromosome.  Also: for each color, what fraction of *answers* came
from XY vs XX users (a popularity-of-naming measure).
"""
import pandas as pd
import numpy as np

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/14_the-xkcd-color-survey-results'
answers = pd.read_csv(f'{DATA_DIR}/answers.csv')
users = pd.read_csv(f'{DATA_DIR}/users.csv')
color_ranks = pd.read_csv(f'{DATA_DIR}/color_ranks.csv')

df = answers.merge(users, on='user_id', how='left')
df = df[df['spam_prob'] < 0.5].copy()

# --- ana_17: Top 30 colors agreement breakdown by chromosome (full table for chart) ---
print("=== ana_17 ===")
top30 = color_ranks.head(30)
rows = []
for _, c in top30.iterrows():
    sub = df[df['hex'] == c['hex']]
    if len(sub) < 50:
        continue
    xy = sub[sub['y_chromosome']==1]
    xx = sub[sub['y_chromosome']==0]
    if len(xy)<30 or len(xx)<30:
        continue
    rows.append({
        'color': c['color'],
        'rank': int(c['rank']),
        'hex': c['hex'],
        'r1_xy': (xy['rank']==1).mean(),
        'r1_xx': (xx['rank']==1).mean(),
        'n_xy': len(xy),
        'n_xx': len(xx),
        'n_total': len(sub),
    })
top30df = pd.DataFrame(rows)
top30df['delta_xx_xy'] = top30df['r1_xx'] - top30df['r1_xy']
print(top30df.to_string(index=False))
top30df.to_csv('/tmp/top30_chrom.csv', index=False)

# --- ana_18: Spam_prob × monitor breakdown ---
print("=== ana_18 ===")
spam_by_mon = users.groupby('monitor')['spam_prob'].agg(['mean','median','count'])
print(spam_by_mon)
spam_by_mon_thr = users.assign(s=users['spam_prob']>0.5).groupby('monitor')['s'].agg(['mean','count'])
spam_by_mon_thr.columns = ['pct_spam_gt_0.5','n']
print(spam_by_mon_thr)

# --- ana_19: Spam-prob × y_chromosome breakdown ---
print("=== ana_19 ===")
print(users.groupby(['y_chromosome'])['spam_prob'].agg(['mean','median','count']))
ct = pd.crosstab(users['y_chromosome'], users['colorblind'], values=users['spam_prob'], aggfunc='mean')
print("\nMean spam_prob by chrom × colorblind:")
print(ct)

# --- ana_20: How does popular-color naming differ XY vs XX (which colors do XY users *answer* more often) ---
print("=== ana_20 ===")
# This counts the number of times each hex got an answer in each group, normalised
xy = df[df['y_chromosome']==1]
xx = df[df['y_chromosome']==0]
# For a fair comparison: rate = answers per user in that group
n_xy_users = users[users['y_chromosome']==1]['user_id'].nunique()
n_xx_users = users[users['y_chromosome']==0]['user_id'].nunique()
xy_per_color = xy.groupby('hex').size() / n_xy_users
xx_per_color = xx.groupby('hex').size() / n_xx_users
pop = pd.DataFrame({'xy_per_user': xy_per_color, 'xx_per_user': xx_per_color}).fillna(0).reset_index()
pop = pop.merge(color_ranks, on='hex').dropna(subset=['color'])
pop['ratio_xx_xy'] = (pop['xx_per_user'] + 1e-6) / (pop['xy_per_user'] + 1e-6)
# limit to top-100 popular ranks
pop_top = pop[pop['rank']<=100].copy()
print("Top 10 colors most XX-skewed (XX users answer more often per capita):")
print(pop_top.nlargest(10,'ratio_xx_xy')[['color','rank','hex','xy_per_user','xx_per_user','ratio_xx_xy']].to_string(index=False))
print("\nTop 10 colors most XY-skewed:")
print(pop_top.nsmallest(10,'ratio_xx_xy')[['color','rank','hex','xy_per_user','xx_per_user','ratio_xx_xy']].to_string(index=False))

# --- ana_21: Hex agreement vs Hue (does agreement depend on hue?) ---
print("=== ana_21 ===")
import colorsys
def hex_to_hsv(h):
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    H, S, V = colorsys.rgb_to_hsv(r, g, b)
    return H * 360, S, V

agree_by_hex = df.groupby('hex').agg(n=('rank','size'), rank1_frac=('rank', lambda r:(r==1).mean()))
agree_by_hex = agree_by_hex.merge(color_ranks, on='hex').dropna(subset=['color'])
agree_by_hex[['H','S','V']] = agree_by_hex['hex'].apply(lambda h: pd.Series(hex_to_hsv(h)))

# Hue bin of 30 deg
agree_by_hex['hue_bin'] = (agree_by_hex['H']//30 * 30).astype(int)
hue_agree = agree_by_hex[agree_by_hex['S']>=0.1].groupby('hue_bin')['rank1_frac'].agg(['mean','count','std'])
print("Mean rank-1 agreement by hue bin (only saturated S>=0.1):")
print(hue_agree)
hue_agree.to_csv('/tmp/hue_agree.csv')

# --- ana_22: Most-answered hexes (the "go-to" exemplars) ---
print("=== ana_22 ===")
n_answers_per_hex = df.groupby('hex').size().reset_index(name='n_answers')
n_answers_per_hex = n_answers_per_hex.merge(color_ranks, on='hex').dropna(subset=['color']).sort_values('n_answers', ascending=False)
print("Top 20 most-answered hexes:")
print(n_answers_per_hex.head(20).to_string(index=False))

# --- ana_23: Answer count distribution ---
print("=== ana_23 ===")
print(f"Median answers per color: {n_answers_per_hex['n_answers'].median():.0f}")
print(f"Mean answers per color: {n_answers_per_hex['n_answers'].mean():.0f}")
print(f"Min: {n_answers_per_hex['n_answers'].min()}, Max: {n_answers_per_hex['n_answers'].max()}")

n_answers_per_hex.to_csv('/tmp/n_answers_per_hex.csv', index=False)

# --- ana_24: Per-rank breakdown for the top 12 most-popular colors (alluvial-style) ---
print("=== ana_24 ===")
top12 = color_ranks.head(12)
rows24 = []
for _, c in top12.iterrows():
    sub = df[df['hex'] == c['hex']]
    if len(sub) < 50:
        continue
    rank_pcts = sub['rank'].value_counts(normalize=True).sort_index()
    for r, p in rank_pcts.items():
        rows24.append({'color': c['color'], 'rank_canonical': int(c['rank']), 'hex': c['hex'], 'answer_rank': int(r), 'pct': float(p)})
df24 = pd.DataFrame(rows24)
print(df24.to_string(index=False))
df24.to_csv('/tmp/top12_rank_breakdown.csv', index=False)
