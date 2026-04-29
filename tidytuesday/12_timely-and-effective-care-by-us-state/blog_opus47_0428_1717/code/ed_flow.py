"""ED flow analyses (OP_18b family + OP_22 + OP_23) — the headline of the dataset."""
import pandas as pd
from pathlib import Path

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/12_timely-and-effective-care-by-us-state/care_state.csv')
df = pd.read_csv(DATA)
TERRITORIES = {'PR', 'GU', 'AS', 'MP', 'VI'}


# --- ana_04: OP_18b national distribution (median ED time) ---
print("=== ana_04 ===")
op18b = df[df.measure_id == 'OP_18b'].dropna(subset=['score']).copy()
print(f"reporting jurisdictions: {len(op18b)}")
print(op18b.score.describe().round(1))
print(f"national median across states: {op18b.score.median():.0f} min")
print(f"max-to-min ratio: {op18b.score.max()/op18b.score.min():.2f}x")

# --- ana_05: OP_18b state ranking — longest waits ---
print("\n=== ana_05 ===")
op18b_sorted = op18b.sort_values('score', ascending=False).reset_index(drop=True)
op18b_sorted['rank'] = op18b_sorted.index + 1
print(op18b_sorted[['rank', 'state', 'score']].head(10).to_string(index=False))

# --- ana_06: OP_18b state ranking — shortest waits ---
print("\n=== ana_06 ===")
op18b_sorted_asc = op18b.sort_values('score', ascending=True).reset_index(drop=True)
op18b_sorted_asc['rank'] = op18b_sorted_asc.index + 1
print(op18b_sorted_asc[['rank', 'state', 'score']].head(10).to_string(index=False))

# --- ana_07: ALL state OP_18b for the choropleth and dot strip ---
print("\n=== ana_07 ===")
op18b_full = op18b.sort_values('score', ascending=True).reset_index(drop=True)
op18b_full['hours'] = op18b_full.score / 60.0
op18b_full['is_territory'] = op18b_full.state.isin(TERRITORIES)
print(op18b_full[['state', 'score', 'hours', 'is_territory']].to_string(index=False))


# --- ana_08: Acuity gradient (low/medium/high/very_high) by state ---
print("\n=== ana_08 ===")
acu_ids = ['OP_18b_LOW_MIN', 'OP_18b_MEDIUM_MIN', 'OP_18b_HIGH_MIN', 'OP_18b_VERY_HIGH_MIN']
acu = df[df.measure_id.isin(acu_ids)].dropna(subset=['score']).copy()
acu_pivot = acu.pivot(index='state', columns='measure_id', values='score')
acu_pivot = acu_pivot[acu_ids]
acu_pivot.columns = ['Low', 'Medium', 'High', 'Very High']
acu_pivot['range'] = acu_pivot['Very High'] - acu_pivot['Low']
print("national medians by acuity:")
for col in ['Low', 'Medium', 'High', 'Very High']:
    print(f"  {col}: {acu_pivot[col].median():.0f} min")
print(f"\nstate with biggest acuity gap (Very High - Low): {acu_pivot['range'].idxmax()} ({acu_pivot['range'].max():.0f} min)")
print(f"state with smallest gap: {acu_pivot['range'].idxmin()} ({acu_pivot['range'].min():.0f} min)")
print("\nfull table (first 15 by Very High):")
print(acu_pivot.sort_values('Very High', ascending=False).head(15).round(0).to_string())

# --- ana_09: OP_22 left without being seen (LWBS) ---
print("\n=== ana_09 ===")
op22 = df[df.measure_id == 'OP_22'].dropna(subset=['score']).copy()
print(f"reporting: {len(op22)}, mean: {op22.score.mean():.2f}%, median: {op22.score.median():.2f}%, max: {op22.score.max():.1f}%")
op22_sorted = op22.sort_values('score', ascending=False)
print("top 10 highest LWBS:")
print(op22_sorted[['state','score']].head(10).to_string(index=False))
print("bottom 5 lowest LWBS:")
print(op22_sorted[['state','score']].tail(5).to_string(index=False))

# --- ana_10: OP_23 stroke imaging within 45 minutes ---
print("\n=== ana_10 ===")
op23 = df[df.measure_id == 'OP_23'].dropna(subset=['score']).copy()
print(f"reporting: {len(op23)}, mean: {op23.score.mean():.1f}%, median: {op23.score.median():.1f}%")
print(op23.sort_values('score', ascending=False)[['state','score']].head(5).to_string(index=False))
print('---bottom---')
print(op23.sort_values('score', ascending=True)[['state','score']].head(5).to_string(index=False))

# --- ana_11: OP_22 vs OP_18b correlation ---
print("\n=== ana_11 ===")
m = op18b.set_index('state')['score'].rename('op18b').to_frame().join(
    op22.set_index('state')['score'].rename('op22'), how='inner')
corr = m['op18b'].corr(m['op22'])
print(f"Pearson corr OP_18b vs OP_22 LWBS: r = {corr:.3f} (n={len(m)})")
print("top combinations (long ED + high LWBS):")
m['z18'] = (m['op18b'] - m['op18b'].mean()) / m['op18b'].std()
m['z22'] = (m['op22'] - m['op22'].mean()) / m['op22'].std()
m['combined'] = m['z18'] + m['z22']
print(m.sort_values('combined', ascending=False).head(8).round(2).to_string())
