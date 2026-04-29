"""Outcome distributions by species and intake-condition."""
import pandas as pd
from pathlib import Path

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/09_long-beach-animal-shelter/longbeach.csv')
df = pd.read_csv(DATA, low_memory=False)
for col in ['dob', 'intake_date', 'outcome_date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# --- ana_06: animal_type composition ---
print("=== ana_06 ===")
ac = df['animal_type'].value_counts()
print(ac.to_string())
total = len(df)
for k, v in ac.items():
    print(f"{k}: {v} ({v/total*100:.1f}%)")
print()

# --- ana_07: outcome_type composition ---
print("=== ana_07 ===")
oc = df['outcome_type'].value_counts(dropna=False)
print(oc.to_string())
print()

# --- ana_08: outcome by species (pct within species) ---
print("=== ana_08 ===")
for sp in ['cat', 'dog', 'bird', 'wild', 'other', 'rabbit', 'reptile', 'guinea pig']:
    sub = df[df['animal_type'] == sp]
    if len(sub) == 0:
        continue
    print(f"--- {sp} (n={len(sub)}) ---")
    pct = (sub['outcome_type'].value_counts(normalize=True) * 100).round(1)
    print(pct.head(10).to_string())
    print()

# --- ana_09: live-release rate by species ---
print("=== ana_09 ===")
def is_live(o):
    if pd.isna(o): return None
    return o not in ('euthanasia', 'died', 'disposal', 'missing')
df['is_live'] = df['outcome_type'].apply(is_live)
df_known = df.dropna(subset=['is_live']).copy()
df_known['is_live'] = df_known['is_live'].astype(int)
sp_save = df_known.groupby('animal_type').agg(total=('is_live', 'count'), live=('is_live', 'sum'))
sp_save['save_pct'] = (sp_save['live'].astype(float) / sp_save['total'].astype(float) * 100).round(1)
sp_save = sp_save.sort_values('total', ascending=False)
print(sp_save.to_string())
print()

# --- ana_10: outcome by intake_condition (cats+dogs) ---
print("=== ana_10 ===")
dc = df_known[df_known['animal_type'].isin(['cat', 'dog'])].copy()
ic = dc.groupby('intake_condition').agg(total=('is_live', 'count'), live=('is_live', 'sum'))
ic['save_pct'] = (ic['live'].astype(float) / ic['total'].astype(float) * 100).round(1)
ic = ic.sort_values('total', ascending=False)
print(ic.to_string())
