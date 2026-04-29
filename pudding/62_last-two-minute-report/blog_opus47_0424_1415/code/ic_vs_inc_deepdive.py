"""Deep dive on the asymmetry between wrong whistles (IC) and missed whistles (INC)."""
import pandas as pd

df = pd.read_parquet('/tmp/l2m_clean.parquet')

# --- ana_17: which call types are most often missed vs wrongly called ---
print("=== ana_17 ===")
errs = df[df['review_decision'].isin(['IC', 'INC'])].copy()
# Top INCs — call types most often missed
inc_by_type = errs[errs['review_decision'] == 'INC']['call_type'].value_counts().head(10)
print("Top 10 most-MISSED call types (INC):")
for c, n in inc_by_type.items():
    print(f"  {c:40s} {int(n):4d}")
print()
ic_by_type = errs[errs['review_decision'] == 'IC']['call_type'].value_counts().head(10)
print("Top 10 most-WRONGLY-CALLED call types (IC):")
for c, n in ic_by_type.items():
    print(f"  {c:40s} {int(n):4d}")
# end ana_17

# --- ana_18: Foul: Shooting has most IC ---
print("\n=== ana_18 ===")
# Which call types have highest IC share vs INC share
ct = df.groupby('call_type')['review_decision'].value_counts().unstack(fill_value=0)
for col in ['IC', 'INC', 'CC', 'CNC']:
    if col not in ct.columns:
        ct[col] = 0
ct['total'] = ct[['IC','INC','CC','CNC']].sum(axis=1)
ct['IC_pct'] = ct['IC'] / ct['total'] * 100
ct['INC_pct'] = ct['INC'] / ct['total'] * 100
# Among call types with volume ≥ 500 — which has highest IC pct?
high_vol = ct[ct['total'] >= 500]
print("Call types with ≥500 plays, sorted by IC rate (wrong whistle rate):")
print(high_vol.sort_values('IC_pct', ascending=False)[['total', 'IC', 'INC', 'IC_pct', 'INC_pct']].to_string())
# end ana_18
