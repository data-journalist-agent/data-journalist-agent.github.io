"""Load Long Beach Animal Shelter data and profile basic shape, columns, missing rates."""
import pandas as pd
from pathlib import Path

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/09_long-beach-animal-shelter/longbeach.csv')
df = pd.read_csv(DATA, low_memory=False)

# Coerce dates
for col in ['dob', 'intake_date', 'outcome_date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# --- ana_profile: basic dataset shape ---
print("=== ana_profile ===")
print(f"rows={len(df)}  cols={df.shape[1]}")
print(f"intake_date: {df['intake_date'].min().date()} -> {df['intake_date'].max().date()}")
print(f"outcome_date: {df['outcome_date'].min().date()} -> {df['outcome_date'].max().date()}")
print(f"unique animal_id: {df['animal_id'].nunique()}")
print()

# --- ana_missing: missing rates ---
print("=== ana_missing ===")
miss = df.isna().mean().sort_values(ascending=False) * 100
print(miss.round(1).to_string())
print()

# --- ana_cardinality: categorical cardinality ---
print("=== ana_cardinality ===")
cats = ['animal_type', 'primary_color', 'secondary_color', 'sex',
        'intake_condition', 'intake_type', 'intake_subtype', 'reason_for_intake',
        'jurisdiction', 'outcome_type', 'outcome_subtype']
for c in cats:
    print(f"{c}: {df[c].nunique()} unique")
