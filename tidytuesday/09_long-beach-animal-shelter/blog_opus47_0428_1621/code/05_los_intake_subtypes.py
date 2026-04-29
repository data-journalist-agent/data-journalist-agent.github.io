"""Length-of-stay, intake subtype/reason analysis."""
import pandas as pd
import numpy as np
from pathlib import Path

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/09_long-beach-animal-shelter/longbeach.csv')
df = pd.read_csv(DATA, low_memory=False)
for col in ['dob', 'intake_date', 'outcome_date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

df['los_days'] = (df['outcome_date'] - df['intake_date']).dt.days

# --- ana_15: length of stay by outcome_type (cats+dogs) ---
print("=== ana_15 ===")
dc = df[df['animal_type'].isin(['cat', 'dog'])].copy()
los_o = dc.groupby('outcome_type')['los_days'].agg(['count', 'median', 'mean']).round(1)
los_o = los_o.sort_values('count', ascending=False)
print(los_o.to_string())
print()

# --- ana_16: length of stay by species ---
print("=== ana_16 ===")
los_s = df.groupby('animal_type')['los_days'].agg(['count', 'median', 'mean']).round(1)
los_s = los_s.sort_values('count', ascending=False)
print(los_s.to_string())
print()

# --- ana_17: intake_type counts ---
print("=== ana_17 ===")
it = df['intake_type'].value_counts()
print(it.to_string())
print()

# --- ana_18: reason_for_intake (owner-surrender reasons) ---
print("=== ana_18 ===")
sur = df[df['intake_type'] == 'owner surrender']
rs = sur['reason_for_intake'].value_counts(dropna=False).head(20)
print(f"Total owner-surrender rows: {len(sur)}")
print(rs.to_string())
print()

# --- ana_19: jurisdiction breakdown ---
print("=== ana_19 ===")
jr = df['jurisdiction'].value_counts().head(10)
print(jr.to_string())

# --- ana_20: intake by 90-day moving window for plot ---
print("=== ana_20 ===")
qrt = df.groupby(pd.Grouper(key='intake_date', freq='QE')).size()
qrt.index = qrt.index.to_period('Q').astype(str)
print(qrt.to_string())
