"""Healthcare-personnel vaccination analyses: HCP_COVID_19 vs IMM_3 (flu)."""
import pandas as pd
from pathlib import Path

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/12_timely-and-effective-care-by-us-state/care_state.csv')
df = pd.read_csv(DATA)

# --- ana_12: HCP_COVID_19 distribution ---
print("=== ana_12 ===")
covid = df[df.measure_id == 'HCP_COVID_19'].dropna(subset=['score']).copy()
print(f"reporting: {len(covid)}")
print(covid.score.describe().round(1))
print(f"how many states <= 10%: {(covid.score <= 10).sum()}")
print(f"how many states <= 5%: {(covid.score <= 5).sum()}")

# --- ana_13: HCP_COVID_19 ranking ---
print("\n=== ana_13 ===")
covid_sorted = covid.sort_values('score', ascending=False)
print('top 10 highest HCW COVID up-to-date:')
print(covid_sorted[['state','score']].head(10).to_string(index=False))
print('bottom 10:')
print(covid_sorted[['state','score']].tail(10).to_string(index=False))

# --- ana_14: HCP_COVID_19 full state list (chart data) ---
print("\n=== ana_14 ===")
covid_full = covid.sort_values('score', ascending=False).reset_index(drop=True)
print(covid_full[['state','score']].to_string(index=False))


# --- ana_15: IMM_3 flu vaccination distribution ---
print("\n=== ana_15 ===")
flu = df[df.measure_id == 'IMM_3'].dropna(subset=['score']).copy()
print(f"reporting: {len(flu)}")
print(flu.score.describe().round(1))

# --- ana_16: COVID vs flu side by side, all states ---
print("\n=== ana_16 ===")
m = covid.set_index('state')['score'].rename('covid').to_frame().join(
    flu.set_index('state')['score'].rename('flu'), how='inner')
m['gap'] = m['flu'] - m['covid']
print(f"national medians: covid {m.covid.median():.1f}%, flu {m.flu.median():.1f}%")
print(f"average gap (flu - covid): {m.gap.mean():.1f} percentage points")
print(f"smallest gap: {m.gap.idxmin()} ({m.gap.min():.1f} pp)")
print(f"largest gap: {m.gap.idxmax()} ({m.gap.max():.1f} pp)")
print('full table sorted by gap:')
print(m.sort_values('gap', ascending=False).round(1).to_string())

# --- ana_17: COVID coverage vs ED time correlation ---
print("\n=== ana_17 ===")
op18b = df[df.measure_id == 'OP_18b'].dropna(subset=['score'])
covid_ed = covid.set_index('state')['score'].rename('covid_pct').to_frame().join(
    op18b.set_index('state')['score'].rename('ed_min'), how='inner')
corr = covid_ed['covid_pct'].corr(covid_ed['ed_min'])
print(f"Pearson corr (covid up-to-date vs ED median): r = {corr:.3f} (n={len(covid_ed)})")
# Spearman for monotone
sp = covid_ed['covid_pct'].corr(covid_ed['ed_min'], method='spearman')
print(f"Spearman: rho = {sp:.3f}")
print(covid_ed.sort_values('ed_min', ascending=False).round(1).to_string())
