"""Load L2M dataset and print basic profile."""
import pandas as pd

df = pd.read_csv('data/62_last-two-minute-report/output/all_games.csv', low_memory=False)

# Filter to rows with a valid review_decision — CC/CNC/IC/INC only
VALID = {'CC', 'CNC', 'IC', 'INC'}
clean = df[df['review_decision'].isin(VALID)].copy()
dirty = df[~df['review_decision'].isin(VALID)]

# Parse date
clean['date'] = pd.to_datetime(clean['date'].astype(str), format='%Y%m%d')
clean['year'] = clean['date'].dt.year
clean['season'] = clean.apply(
    lambda r: f"{r['date'].year-1}-{str(r['date'].year)[-2:]}"
    if r['date'].month < 10
    else f"{r['date'].year}-{str(r['date'].year+1)[-2:]}",
    axis=1,
)

# --- ana_00: dataset profile ---
print("=== ana_00 ===")
print(f"total_raw_rows: {len(df)}")
print(f"clean_rows (CC/CNC/IC/INC only): {len(clean)}")
print(f"dropped_dirty_rows: {len(dirty)}")
print(f"unique_games: {clean['game_id'].nunique()}")
print(f"date_range: {clean['date'].min().date()} to {clean['date'].max().date()}")
print(f"unique_call_types: {clean['call_type'].nunique()}")
print(f"unique_referees: {pd.concat([clean['ref_1'], clean['ref_2'], clean['ref_3']]).dropna().nunique()}")
print(f"review_decision_breakdown:")
print(clean['review_decision'].value_counts())
# end

# Save cleaned data for reuse
clean.to_parquet('/tmp/l2m_clean.parquet')
print(f"\nSaved clean data: {len(clean)} rows to /tmp/l2m_clean.parquet")
