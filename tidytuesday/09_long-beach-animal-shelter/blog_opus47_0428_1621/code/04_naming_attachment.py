"""Names: owner-given vs staff-given vs blank, top names, and outcomes by name-status."""
import pandas as pd
from pathlib import Path

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/09_long-beach-animal-shelter/longbeach.csv')
df = pd.read_csv(DATA, low_memory=False)
for col in ['dob', 'intake_date', 'outcome_date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

def name_status(n):
    if pd.isna(n): return 'blank'
    if str(n).startswith('*'): return 'staff_named'
    return 'owner_named'

df['name_status'] = df['animal_name'].apply(name_status)

# --- ana_11: name status counts ---
print("=== ana_11 ===")
ns = df['name_status'].value_counts()
print(ns.to_string())
total = len(df)
for k, v in ns.items():
    print(f"{k}: {v} ({v/total*100:.1f}%)")
print()

# --- ana_12: name status by intake_type ---
print("=== ana_12 ===")
ct = pd.crosstab(df['intake_type'], df['name_status'], normalize='index') * 100
print(ct.round(1).to_string())
print()

# --- ana_13: outcome by name status (cats+dogs) ---
print("=== ana_13 ===")
dc = df[df['animal_type'].isin(['cat', 'dog'])].copy()
def is_live(o):
    if pd.isna(o): return None
    return o not in ('euthanasia', 'died', 'disposal', 'missing')
dc['is_live'] = dc['outcome_type'].apply(is_live)

# Rate of return-to-owner by name status
dc['rto'] = (dc['outcome_type'] == 'return to owner')
dc['ado'] = (dc['outcome_type'] == 'adoption')
ag = dc.groupby('name_status').agg(
    n=('is_live', 'count'),
    rto_pct=('rto', lambda x: round(x.mean()*100, 1)),
    ado_pct=('ado', lambda x: round(x.mean()*100, 1)),
    save_pct=('is_live', lambda x: round(x.mean()*100, 1))
)
print(ag.to_string())
print()

# --- ana_14: top owner-given names ---
print("=== ana_14 ===")
owner = df[df['name_status'] == 'owner_named']['animal_name'].str.lower().str.strip()
top = owner.value_counts().head(15)
print(top.to_string())
print()

# --- ana_14b: top dog names vs top cat names ---
print("=== ana_14b ===")
print('Top owner-given DOG names:')
print(df[(df['name_status']=='owner_named') & (df['animal_type']=='dog')]['animal_name'].str.lower().str.strip().value_counts().head(10).to_string())
print('Top owner-given CAT names:')
print(df[(df['name_status']=='owner_named') & (df['animal_type']=='cat')]['animal_name'].str.lower().str.strip().value_counts().head(10).to_string())
