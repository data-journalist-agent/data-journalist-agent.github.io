"""Naming-region analysis for xkcd Color Survey.

DATA SHAPE: answers.csv = ~1M rows; each row is one user shown a unique
random hex who typed one of the top-5 ranked color names:
    rank=1 → "purple", rank=2 → "green", rank=3 → "blue",
    rank=4 → "pink",   rank=5 → "brown".
Each displayed hex is shown to at most ~5 users — so the unit of analysis is
not a single hex but a *region* of color space.  We bin the RGB cube into
12x12x12 cells (1728 cells) and analyze each cell's name distribution,
demographic effects, and the cells that sit on naming boundaries.
"""
import pandas as pd
import numpy as np
import colorsys

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/14_the-xkcd-color-survey-results'
print("Loading...")
answers = pd.read_csv(f'{DATA_DIR}/answers.csv')
users = pd.read_csv(f'{DATA_DIR}/users.csv')
color_ranks = pd.read_csv(f'{DATA_DIR}/color_ranks.csv')
print(f"answers: {len(answers):,}, users: {len(users):,}, colors: {len(color_ranks):,}")

TOP5 = {1:'purple', 2:'green', 3:'blue', 4:'pink', 5:'brown'}
answers['answer_name'] = answers['rank'].map(TOP5)
answers['hex_lower'] = answers['hex'].str.lower()

# Compute RGB and HSV
hexes = answers['hex_lower'].values
def hex_to_rgb_hsv(h):
    r,g,b = int(h[1:3],16), int(h[3:5],16), int(h[5:7],16)
    H,S,V = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return r,g,b, H*360, S, V

print("Decoding hexes...")
arr = np.empty((len(hexes), 6), dtype=np.float32)
for i,h in enumerate(hexes):
    arr[i] = hex_to_rgb_hsv(h)
answers['R']=arr[:,0]; answers['G']=arr[:,1]; answers['B']=arr[:,2]
answers['H']=arr[:,3]; answers['S']=arr[:,4]; answers['V']=arr[:,5]

# Bin into 12x12x12 RGB cube (cells are 256/12 ~= 21.3 wide)
NB = 12
answers['Rb'] = np.minimum((answers['R']/256*NB).astype(int), NB-1)
answers['Gb'] = np.minimum((answers['G']/256*NB).astype(int), NB-1)
answers['Bb'] = np.minimum((answers['B']/256*NB).astype(int), NB-1)
answers['cell'] = answers['Rb']*NB*NB + answers['Gb']*NB + answers['Bb']

df = answers.merge(users, on='user_id', how='left')
print(f"After merge: {len(df):,} rows")

# --- ana_10: Overall distribution among the top-5 names ---
print("=== ana_10 ===")
overall = df['answer_name'].value_counts(normalize=True) * 100
print("Among the ~1M top-5 answers, fraction by name:")
for n, p in overall.items():
    print(f"  {n}: {p:.2f}%")
print(f"\nTotal top-5 answers: {len(df):,}")

# --- ana_11: Hue centroid (median H,S,V) for each top-5 name ---
print("=== ana_11 ===")
centroids = df.groupby('answer_name').agg(
    n=('hex_lower','size'),
    H_med=('H','median'), S_med=('S','median'), V_med=('V','median'),
    H_mean=('H','mean'),  S_mean=('S','mean'),  V_mean=('V','mean'),
).reset_index()
print(centroids.to_string(index=False))
centroids.to_csv('/tmp/centroids.csv', index=False)

# --- ana_12: Hue histograms — fraction of each name that fell into each hue bin ---
print("=== ana_12 ===")
df['hue10'] = (df['H']//10 * 10).astype(int)  # 10° bins
hue_pivot = df.groupby(['hue10','answer_name']).size().unstack(fill_value=0)
hue_pivot_pct = hue_pivot.div(hue_pivot.sum(axis=1), axis=0)*100
print("Within each hue bin, % of answers by name (sample):")
print(hue_pivot_pct.round(1).head(20))
hue_pivot_pct.reset_index().to_csv('/tmp/hue_name_pct.csv', index=False)

# Total counts (hue × name) for stacked area
hue_pivot_long = hue_pivot.reset_index().melt(id_vars='hue10', var_name='name', value_name='n')
hue_pivot_long.to_csv('/tmp/hue_name_count.csv', index=False)

print("\n5th–95th percentile hue range per name:")
range_data = []
for name in TOP5.values():
    sub = df[df['answer_name']==name]
    h = sub['H'].values
    if len(h)==0: continue
    p5, p95 = np.percentile(h, [5,95])
    md = np.median(h)
    print(f"  {name}: hue {p5:.0f}–{p95:.0f}° (median {md:.0f}°), n={len(sub):,}")
    range_data.append({'name':name, 'p5':p5, 'p95':p95, 'median':md, 'n':len(sub)})
pd.DataFrame(range_data).to_csv('/tmp/hue_range.csv', index=False)

# --- ana_13: RGB-cube cells, name dominance ---
print("=== ana_13 ===")
cell_counts = df.groupby('cell').size()
print(f"Non-empty cells (of {NB**3} possible): {len(cell_counts)}")
print(f"Cells with n>=50: {(cell_counts>=50).sum()}")
print(f"Cells with n>=200: {(cell_counts>=200).sum()}")
print(f"Mean answers per non-empty cell: {cell_counts.mean():.1f}, median: {cell_counts.median():.0f}")

# Aggregate per cell: name distribution
cell_grp = df.groupby(['cell','answer_name']).size().unstack(fill_value=0)
cell_grp['n'] = cell_grp.sum(axis=1)
for name in TOP5.values():
    if name not in cell_grp.columns:
        cell_grp[name] = 0
cell_grp['winner'] = cell_grp[list(TOP5.values())].idxmax(axis=1)
cell_grp['winner_pct'] = cell_grp[list(TOP5.values())].max(axis=1) / cell_grp['n']
cell_grp = cell_grp.reset_index()

# Cell coordinates: average RGB of cell center
def cell_to_rgb(c):
    r=c//(NB*NB); g=(c%(NB*NB))//NB; b=c%NB
    return (r+0.5)*256/NB, (g+0.5)*256/NB, (b+0.5)*256/NB
cell_rgb = np.array([cell_to_rgb(c) for c in cell_grp['cell']])
cell_grp['cR']=cell_rgb[:,0]; cell_grp['cG']=cell_rgb[:,1]; cell_grp['cB']=cell_rgb[:,2]

# Restrict to well-sampled cells
ws = cell_grp[cell_grp['n']>=50].copy()
print(f"\nWell-sampled cells (n>=50): {len(ws)}")
print("Winner-name distribution across well-sampled cells:")
print(ws['winner'].value_counts())
print(f"\nMean winner share: {ws['winner_pct'].mean()*100:.2f}%")
print(f"Median winner share: {ws['winner_pct'].median()*100:.2f}%")
print(f"Cells with winner_pct >= 0.95: {(ws['winner_pct']>=0.95).sum()}")
print(f"Cells with winner_pct >= 0.90: {(ws['winner_pct']>=0.90).sum()}")
print(f"Cells with winner_pct < 0.50: {(ws['winner_pct']<0.50).sum()}")
print(f"Cells with winner_pct < 0.40: {(ws['winner_pct']<0.40).sum()}")

# --- ana_14: Most ambiguous cells — naming boundaries ---
print("=== ana_14 ===")
amb = ws.nsmallest(25, 'winner_pct').copy()
# convert center RGB to hex
def rgb_to_hex(r,g,b):
    return '#%02x%02x%02x' % (int(r),int(g),int(b))
amb['center_hex'] = amb.apply(lambda r: rgb_to_hex(r['cR'],r['cG'],r['cB']), axis=1)
print("Top 25 most ambiguous cells (closest to a naming boundary):")
print(amb[['center_hex','n','winner','winner_pct','purple','green','blue','pink','brown']].to_string(index=False))
amb.to_csv('/tmp/most_ambiguous_cells.csv', index=False)

# Save full well-sampled set
ws['center_hex'] = ws.apply(lambda r: rgb_to_hex(r['cR'],r['cG'],r['cB']), axis=1)
ws.to_csv('/tmp/well_sampled_cells.csv', index=False)

# --- ana_15: Within-name dominance: which cells are most "purely" green, blue, etc ---
print("=== ana_15 ===")
for name in TOP5.values():
    pure = ws[ws['winner']==name].nlargest(5, 'winner_pct')
    pure['center_hex'] = pure.apply(lambda r: rgb_to_hex(r['cR'],r['cG'],r['cB']), axis=1)
    print(f"\nMost canonically '{name}' cells (highest winner_pct):")
    print(pure[['center_hex','n','winner_pct',name]].to_string(index=False))

# --- ana_16: Boundary divergence by chromosome ---
print("=== ana_16 ===")
clean = df[df['spam_prob'] < 0.5].copy()
print(f"Clean rows (spam_prob<0.5): {len(clean):,}")

cell_xy = clean[clean['y_chromosome']==1].groupby(['cell','answer_name']).size().unstack(fill_value=0)
cell_xx = clean[clean['y_chromosome']==0].groupby(['cell','answer_name']).size().unstack(fill_value=0)
for name in TOP5.values():
    if name not in cell_xy.columns: cell_xy[name]=0
    if name not in cell_xx.columns: cell_xx[name]=0
cell_xy['n_xy']=cell_xy[list(TOP5.values())].sum(axis=1)
cell_xx['n_xx']=cell_xx[list(TOP5.values())].sum(axis=1)
xyxx = cell_xy.join(cell_xx, lsuffix='_xy', rsuffix='_xx', how='inner').reset_index()
xyxx = xyxx[(xyxx['n_xy']>=50) & (xyxx['n_xx']>=20)].copy()
print(f"Cells with XY n>=50, XX n>=20: {len(xyxx)}")

# Compute divergence (sum |p_xy - p_xx| / 2)
div = np.zeros(len(xyxx))
for name in TOP5.values():
    p_xy = xyxx[f'{name}_xy'].values / xyxx['n_xy'].values
    p_xx = xyxx[f'{name}_xx'].values / xyxx['n_xx'].values
    div += np.abs(p_xy - p_xx)
xyxx['divergence'] = div / 2
print(f"Mean cell-level XY-XX divergence: {xyxx['divergence'].mean():.4f}")
print(f"Median: {xyxx['divergence'].median():.4f}")
print(f"Max: {xyxx['divergence'].max():.4f}")

# Pick top divergent cells
top_div = xyxx.nlargest(20, 'divergence').copy()
def cell_to_rgb_hex(c):
    r=c//(NB*NB); g=(c%(NB*NB))//NB; b=c%NB
    return rgb_to_hex((r+0.5)*256/NB, (g+0.5)*256/NB, (b+0.5)*256/NB)
top_div['center_hex'] = top_div['cell'].apply(cell_to_rgb_hex)

# For each divergent cell, identify the winner names per group
def winner_pair(row):
    xy_pcts = {n: row[f'{n}_xy']/row['n_xy'] for n in TOP5.values()}
    xx_pcts = {n: row[f'{n}_xx']/row['n_xx'] for n in TOP5.values()}
    xy_w = max(xy_pcts, key=xy_pcts.get)
    xx_w = max(xx_pcts, key=xx_pcts.get)
    return xy_w, xy_pcts[xy_w], xx_w, xx_pcts[xx_w]

wp = top_div.apply(lambda r: pd.Series(winner_pair(r), index=['xy_winner','xy_winner_pct','xx_winner','xx_winner_pct']), axis=1)
top_div = pd.concat([top_div, wp], axis=1)
print("\nTop 20 cells with highest XY-vs-XX naming divergence:")
print(top_div[['center_hex','n_xy','n_xx','xy_winner','xy_winner_pct','xx_winner','xx_winner_pct','divergence']].to_string(index=False))
top_div.to_csv('/tmp/chrom_divergent_cells.csv', index=False)

# --- ana_17: Aggregate naming-rate diff by name (XY vs XX) ---
print("=== ana_17 ===")
xy_total = clean[clean['y_chromosome']==1]['answer_name'].value_counts(normalize=True)
xx_total = clean[clean['y_chromosome']==0]['answer_name'].value_counts(normalize=True)
agg_diff = pd.DataFrame({'XY':xy_total*100, 'XX':xx_total*100})
agg_diff['XX_minus_XY'] = agg_diff['XX'] - agg_diff['XY']
print("Aggregate share of each top-5 name by chromosome (%):")
print(agg_diff.round(2))
agg_diff.reset_index().to_csv('/tmp/agg_chrom_share.csv', index=False)

# --- ana_18: Spam probability distribution by chromosome ---
print("=== ana_18 ===")
print("Mean spam_prob by chromosome:")
print(users.groupby('y_chromosome')['spam_prob'].agg(['mean','median','count']))
print("\n% spam_prob > 0.5 by chromosome:")
print(users.assign(s=users['spam_prob']>0.5).groupby('y_chromosome')['s'].mean()*100)

bins = [0, 0.05, 0.1, 0.25, 0.5, 0.75, 1.01]
labels = ['<0.05','0.05-0.1','0.1-0.25','0.25-0.5','0.5-0.75','>0.75']
users['spam_bucket'] = pd.cut(users['spam_prob'], bins=bins, labels=labels, include_lowest=True)
ct_pct = pd.crosstab(users['spam_bucket'], users['y_chromosome'], normalize='index')*100
print("\nWithin each spam-prob bucket, % XY (y_chrom=1):")
print(ct_pct[1.0].round(2))

# Counts
print("\nSpam_prob bucket counts × chromosome:")
print(pd.crosstab(users['spam_bucket'], users['y_chromosome']))

# --- ana_19: Colorblindness rates by chromosome (population check) ---
print("=== ana_19 ===")
# Filter NA chromosome
xy_users = users[users['y_chromosome']==1]
xx_users = users[users['y_chromosome']==0]
print(f"XY users: {len(xy_users):,}, colorblind rate: {xy_users['colorblind'].mean()*100:.3f}%")
print(f"XX users: {len(xx_users):,}, colorblind rate: {xx_users['colorblind'].mean()*100:.3f}%")
ratio = xy_users['colorblind'].mean()/xx_users['colorblind'].mean()
print(f"XY/XX ratio: {ratio:.2f}x (population benchmark ~16x)")
print()
for thr in [0.1, 0.5, 1.01]:
    sub = users[users['spam_prob'] < thr]
    sxy = sub[sub['y_chromosome']==1]
    sxx = sub[sub['y_chromosome']==0]
    if len(sxy)==0 or len(sxx)==0: continue
    r = sxy['colorblind'].mean()/max(sxx['colorblind'].mean(),1e-9)
    print(f"  spam_prob<{thr}: XY n={len(sxy):,} cb={sxy['colorblind'].mean()*100:.3f}% | XX n={len(sxx):,} cb={sxx['colorblind'].mean()*100:.3f}% | ratio={r:.2f}x")

# --- ana_20: Colorblind cell-level divergence ---
print("=== ana_20 ===")
cell_cb = clean[clean['colorblind']==1].groupby(['cell','answer_name']).size().unstack(fill_value=0)
cell_ncb = clean[clean['colorblind']==0].groupby(['cell','answer_name']).size().unstack(fill_value=0)
for name in TOP5.values():
    if name not in cell_cb.columns: cell_cb[name]=0
    if name not in cell_ncb.columns: cell_ncb[name]=0
cell_cb['n_cb']=cell_cb[list(TOP5.values())].sum(axis=1)
cell_ncb['n_ncb']=cell_ncb[list(TOP5.values())].sum(axis=1)
cbm = cell_cb.join(cell_ncb, lsuffix='_cb', rsuffix='_ncb', how='inner').reset_index()
cbm = cbm[(cbm['n_cb']>=15) & (cbm['n_ncb']>=50)].copy()
print(f"Cells with CB n>=15, nCB n>=50: {len(cbm)}")

div = np.zeros(len(cbm))
for name in TOP5.values():
    p_cb = cbm[f'{name}_cb'].values / cbm['n_cb'].values
    p_ncb = cbm[f'{name}_ncb'].values / cbm['n_ncb'].values
    div += np.abs(p_cb - p_ncb)
cbm['divergence'] = div / 2
print(f"Mean CB-vs-nCB cell divergence: {cbm['divergence'].mean():.4f}")
print(f"Median: {cbm['divergence'].median():.4f}")

top_cb_div = cbm.nlargest(20, 'divergence').copy()
top_cb_div['center_hex'] = top_cb_div['cell'].apply(cell_to_rgb_hex)
def winner_pair2(row):
    cb_pcts = {n: row[f'{n}_cb']/row['n_cb'] for n in TOP5.values()}
    ncb_pcts = {n: row[f'{n}_ncb']/row['n_ncb'] for n in TOP5.values()}
    return max(cb_pcts, key=cb_pcts.get), cb_pcts[max(cb_pcts, key=cb_pcts.get)], max(ncb_pcts, key=ncb_pcts.get), ncb_pcts[max(ncb_pcts, key=ncb_pcts.get)]
wp = top_cb_div.apply(lambda r: pd.Series(winner_pair2(r), index=['cb_winner','cb_winner_pct','ncb_winner','ncb_winner_pct']), axis=1)
top_cb_div = pd.concat([top_cb_div, wp], axis=1)
print("\nTop 20 cells with highest CB-vs-non-CB naming divergence:")
print(top_cb_div[['center_hex','n_cb','n_ncb','cb_winner','cb_winner_pct','ncb_winner','ncb_winner_pct','divergence']].to_string(index=False))
top_cb_div.to_csv('/tmp/cb_divergent_cells.csv', index=False)

# Aggregate
print("\nAggregate share of each top-5 name by colorblindness (%):")
cb_total = clean[clean['colorblind']==1]['answer_name'].value_counts(normalize=True)*100
ncb_total = clean[clean['colorblind']==0]['answer_name'].value_counts(normalize=True)*100
print(pd.DataFrame({'CB':cb_total, 'nonCB':ncb_total, 'diff':cb_total-ncb_total}).round(2))

# --- ana_21: Monitor type effect aggregate ---
print("=== ana_21 ===")
mon_agg = clean.groupby('monitor')['answer_name'].value_counts(normalize=True).unstack(fill_value=0)*100
print("Aggregate share of each top-5 name by monitor (%):")
print(mon_agg.round(2))
mon_agg.reset_index().to_csv('/tmp/monitor_share.csv', index=False)
