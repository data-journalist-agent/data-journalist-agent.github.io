"""Error rates by call type."""
import pandas as pd

df = pd.read_parquet('/tmp/l2m_clean.parquet')

# --- ana_03: error rates by call type ---
print("=== ana_03 ===")
ct = df.groupby('call_type')['review_decision'].value_counts().unstack(fill_value=0)
for col in ['CC', 'CNC', 'IC', 'INC']:
    if col not in ct.columns:
        ct[col] = 0
ct['total'] = ct[['CC', 'CNC', 'IC', 'INC']].sum(axis=1)
ct['incorrect'] = ct['IC'] + ct['INC']
ct['incorrect_pct'] = ct['incorrect'] / ct['total'] * 100
# Filter to call types with at least 100 decisions for meaningful rates
top = ct[ct['total'] >= 100].sort_values('incorrect_pct', ascending=False)
print("Call types with ≥100 plays, sorted by error %:")
for idx, row in top.iterrows():
    print(f"  {idx:40s} total={int(row['total']):5d}  IC={int(row['IC']):4d}  INC={int(row['INC']):4d}  error_pct={row['incorrect_pct']:.1f}%")
# end ana_03

# --- ana_04: volume of each call type (most common in crunch time) ---
print("\n=== ana_04 ===")
top_volume = ct.sort_values('total', ascending=False).head(10)
print("Top 10 call types by volume:")
for idx, row in top_volume.iterrows():
    print(f"  {idx:40s} total={int(row['total']):5d}")
# end ana_04
