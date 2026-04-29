"""Annual / monthly / seasonal trends across intakes, outcomes, save rate."""
import pandas as pd
from pathlib import Path

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/09_long-beach-animal-shelter/longbeach.csv')
df = pd.read_csv(DATA, low_memory=False)
for col in ['dob', 'intake_date', 'outcome_date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

df['intake_year'] = df['intake_date'].dt.year
df['outcome_year'] = df['outcome_date'].dt.year
df['intake_month'] = df['intake_date'].dt.month

# --- ana_01: annual intake trend ---
print("=== ana_01 ===")
intake_by_year = df.groupby('intake_year').size().astype(int)
print(intake_by_year.to_string())
print()

# --- ana_02: annual adoption trend (by outcome_year, outcome_type='adoption') ---
print("=== ana_02 ===")
ad = df[df['outcome_type'] == 'adoption'].groupby('outcome_year').size().astype(int)
print(ad.to_string())
print()

# --- ana_03: annual save rate (live release, dogs+cats only) ---
# live = anything that is NOT euthanasia / died / disposal / missing
print("=== ana_03 ===")
dc = df[df['animal_type'].isin(['cat', 'dog'])].copy()
def _live(o):
    if pd.isna(o): return None
    return o not in ('euthanasia', 'died', 'disposal', 'missing')
dc['is_live'] = dc['outcome_type'].apply(_live)
dc_known = dc.dropna(subset=['is_live']).copy()
dc_known['is_live'] = dc_known['is_live'].astype(int)
agg = dc_known.groupby('outcome_year').agg(
    total=('is_live', 'count'),
    live=('is_live', 'sum')
).dropna()
agg['save_rate_pct'] = (agg['live'].astype(float) / agg['total'].astype(float) * 100).round(1)
print(agg.to_string())
print()

# --- ana_04: outcome composition by year (adoption / rescue / RTO / euthanasia / TNR / other) ---
print("=== ana_04 ===")
def bucket(ot):
    if pd.isna(ot): return 'other'
    if ot == 'adoption': return 'adoption'
    if ot == 'rescue': return 'rescue/transfer'
    if ot == 'transfer': return 'rescue/transfer'
    if ot == 'return to owner': return 'return to owner'
    if ot in ('euthanasia',): return 'euthanasia'
    if ot in ('died', 'disposal'): return 'died/disposal'
    if ot in ('shelter, neuter, return', 'community cat', 'trap, neuter, release', 'return to wild habitat'): return 'TNR / wildlife release'
    return 'other'
df['outcome_bucket'] = df['outcome_type'].apply(bucket)
ob = df.groupby(['outcome_year', 'outcome_bucket']).size().unstack(fill_value=0).astype(int)
print(ob.to_string())
print()

# --- ana_05: monthly seasonality (kitten season) ---
print("=== ana_05 ===")
month_intake = df.groupby('intake_month').size()
month_kitten = df[(df['animal_type'] == 'cat') & (df['intake_condition'] == 'under age/weight')].groupby('intake_month').size()
print('All intakes by month:')
print(month_intake.to_string())
print('Underage kittens by month:')
print(month_kitten.to_string())
