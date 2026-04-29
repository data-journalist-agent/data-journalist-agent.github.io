"""Season-over-season error rate trend."""
import pandas as pd

df = pd.read_parquet('/tmp/l2m_clean.parquet')

# --- ana_14: error rate by season ---
print("=== ana_14 ===")
season_stats = df.groupby('season')['review_decision'].value_counts().unstack(fill_value=0)
for col in ['CC', 'CNC', 'IC', 'INC']:
    if col not in season_stats.columns:
        season_stats[col] = 0
season_stats['total'] = season_stats[['CC', 'CNC', 'IC', 'INC']].sum(axis=1)
season_stats['incorrect'] = season_stats['IC'] + season_stats['INC']
season_stats['incorrect_pct'] = season_stats['incorrect'] / season_stats['total'] * 100
season_stats['games'] = df.groupby('season')['game_id'].nunique()
season_stats['errors_per_game'] = season_stats['incorrect'] / season_stats['games']
season_stats = season_stats.sort_index()
print(f"{'season':10s} {'games':>6s} {'plays':>6s} {'CC':>5s} {'CNC':>6s} {'IC':>4s} {'INC':>5s} {'err%':>6s} {'err/g':>7s}")
for s, row in season_stats.iterrows():
    print(f"{s:10s} {int(row['games']):6d} {int(row['total']):6d} {int(row['CC']):5d} {int(row['CNC']):6d} {int(row['IC']):4d} {int(row['INC']):5d} {row['incorrect_pct']:5.2f}% {row['errors_per_game']:6.2f}")
# end ana_14
