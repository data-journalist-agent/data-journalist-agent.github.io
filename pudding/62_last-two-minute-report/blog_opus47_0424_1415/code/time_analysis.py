"""Error rate as function of seconds remaining."""
import pandas as pd

df = pd.read_parquet('/tmp/l2m_clean.parquet')

# --- ana_12: error rate by seconds-left bucket ---
print("=== ana_12 ===")
# Bucket seconds_left into 10-second buckets, only within Q4/OT last 2 min (seconds_left <= 120)
q4_ot = df[df['seconds_left'] <= 120].copy()
# Bin by 10-second intervals
q4_ot['bin'] = (q4_ot['seconds_left'] // 10 * 10).astype(int)
bins = q4_ot.groupby('bin')['review_decision'].value_counts().unstack(fill_value=0)
for col in ['CC', 'CNC', 'IC', 'INC']:
    if col not in bins.columns:
        bins[col] = 0
bins['total'] = bins[['CC', 'CNC', 'IC', 'INC']].sum(axis=1)
bins['incorrect'] = bins['IC'] + bins['INC']
bins['incorrect_pct'] = bins['incorrect'] / bins['total'] * 100
bins = bins.sort_index()
print(f"{'bin (sec_left)':15s} {'total':>7s} {'CC':>6s} {'CNC':>6s} {'IC':>5s} {'INC':>5s} {'err_pct':>8s}")
for b, row in bins.iterrows():
    label = f"{int(b)}-{int(b)+9}"
    print(f"{label:15s} {int(row['total']):7d} {int(row['CC']):6d} {int(row['CNC']):6d} {int(row['IC']):5d} {int(row['INC']):5d} {row['incorrect_pct']:7.2f}%")
# end ana_12

# --- ana_13: volume by bin (more calls near the buzzer?) ---
print("\n=== ana_13 ===")
# Already have bins[total], print that cleanly
print("Volume by 10-sec bin:")
for b, row in bins.iterrows():
    print(f"  {int(b):3d}s-{int(b)+9:3d}s: {int(row['total'])} decisions")
# Sum within last 30 seconds vs 90-120
last30 = bins.loc[0:29, 'total'].sum()
early = bins.loc[90:120, 'total'].sum()
print(f"\nTotal decisions in last 30 sec: {last30}")
print(f"Total decisions in 90-120 sec window: {early}")
# end ana_13
