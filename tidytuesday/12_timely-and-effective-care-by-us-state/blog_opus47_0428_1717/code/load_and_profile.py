"""Dataset profile for TidyTuesday 12 — Timely and Effective Care by US State."""
import pandas as pd
from pathlib import Path

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/12_timely-and-effective-care-by-us-state/care_state.csv')

df = pd.read_csv(DATA)

# US states (50) + DC vs territories (PR, GU, AS, MP, VI)
TERRITORIES = {'PR', 'GU', 'AS', 'MP', 'VI'}

# --- ana_01: Dataset shape and one-row meaning ---
print("=== ana_01 ===")
print(f"rows: {len(df)}")
print(f"cols: {df.shape[1]}")
print(f"unique states/territories: {df.state.nunique()}")
print(f"unique measure_ids: {df.measure_id.nunique()}")
print(f"unique measure_names: {df.measure_name.nunique()}")
print(f"unique conditions: {df.condition.nunique()}")
print(f"date range: {df.start_date.min()} -> {df.end_date.max()}")

# --- ana_02: Missingness profile ---
print("\n=== ana_02 ===")
total = len(df)
nulls = df.score.isna().sum()
print(f"missing scores: {nulls} of {total} ({nulls/total*100:.1f}%)")
print("missing rate by measure:")
miss_by_m = (
    df.groupby('measure_id')
    .apply(lambda g: g.score.isna().mean() * 100)
    .sort_values(ascending=False)
)
for mid, rate in miss_by_m.items():
    print(f"  {mid}: {rate:.1f}%")
print("\nstates with most missing rows:")
miss_by_s = df[df.score.isna()].state.value_counts()
for s, n in miss_by_s.head(10).items():
    print(f"  {s}: {n}")

# --- ana_03: Conditions and their measure counts ---
print("\n=== ana_03 ===")
cond = df.groupby('condition').agg(
    measures=('measure_id', 'nunique'),
    rows=('state', 'count'),
).sort_values('measures', ascending=False)
print(cond)
