"""Referee-level error rates and Scott Foster specifically."""
import pandas as pd

df = pd.read_parquet('/tmp/l2m_clean.parquet')

# Build a long-form referee table — one row per ref-per-play
ref_long = pd.concat([
    df[['ref_1', 'review_decision', 'game_id']].rename(columns={'ref_1': 'ref'}),
    df[['ref_2', 'review_decision', 'game_id']].rename(columns={'ref_2': 'ref'}),
    df[['ref_3', 'review_decision', 'game_id']].rename(columns={'ref_3': 'ref'}),
])
ref_long = ref_long.dropna(subset=['ref'])

# --- ana_05: top refs by games worked, and their error rates ---
print("=== ana_05 ===")
# Games per ref (unique game-ref combos)
games_per_ref = ref_long.groupby('ref')['game_id'].nunique()
# Error counts per ref (decisions observed as a crew member)
ref_decisions = ref_long.groupby('ref')['review_decision'].value_counts().unstack(fill_value=0)
for col in ['CC', 'CNC', 'IC', 'INC']:
    if col not in ref_decisions.columns:
        ref_decisions[col] = 0
ref_decisions['total_plays'] = ref_decisions[['CC', 'CNC', 'IC', 'INC']].sum(axis=1)
ref_decisions['incorrect'] = ref_decisions['IC'] + ref_decisions['INC']
ref_decisions['incorrect_pct'] = ref_decisions['incorrect'] / ref_decisions['total_plays'] * 100
ref_decisions['games'] = games_per_ref

# Filter to refs who worked ≥ 40 games (meaningful sample)
eligible = ref_decisions[ref_decisions['games'] >= 40].copy()
eligible = eligible.sort_values('games', ascending=False)

print(f"Refs with ≥40 L2M games: {len(eligible)}")
print(f"\n-- Top 15 by games worked --")
print(f"{'ref':25s} {'games':>6s} {'plays':>6s} {'IC':>4s} {'INC':>4s} {'err_pct':>8s}")
for ref, row in eligible.head(15).iterrows():
    print(f"{ref:25s} {int(row['games']):6d} {int(row['total_plays']):6d} {int(row['IC']):4d} {int(row['INC']):4d} {row['incorrect_pct']:7.2f}%")
# end ana_05

# --- ana_06: refs with highest and lowest error rates (≥40 games) ---
print("\n=== ana_06 ===")
by_err = eligible.sort_values('incorrect_pct', ascending=False)
print("TOP 10 highest error rate (≥40 games):")
print(f"{'ref':25s} {'games':>6s} {'plays':>6s} {'err_pct':>8s}")
for ref, row in by_err.head(10).iterrows():
    print(f"{ref:25s} {int(row['games']):6d} {int(row['total_plays']):6d} {row['incorrect_pct']:7.2f}%")
print("\nBOTTOM 10 lowest error rate (≥40 games):")
for ref, row in by_err.tail(10).iterrows():
    print(f"{ref:25s} {int(row['games']):6d} {int(row['total_plays']):6d} {row['incorrect_pct']:7.2f}%")
# end ana_06

# --- ana_07: Scott Foster specifically ---
print("\n=== ana_07 ===")
if 'Scott Foster' in ref_decisions.index:
    sf = ref_decisions.loc['Scott Foster']
    print(f"Scott Foster: {int(sf['games'])} games worked, {int(sf['total_plays'])} plays reviewed")
    print(f"  CC: {int(sf['CC'])}  CNC: {int(sf['CNC'])}  IC: {int(sf['IC'])}  INC: {int(sf['INC'])}")
    print(f"  error_pct: {sf['incorrect_pct']:.2f}%")
    avg = eligible['incorrect_pct'].mean()
    median = eligible['incorrect_pct'].median()
    print(f"  league median error rate (≥40 games): {median:.2f}%")
    print(f"  league mean error rate (≥40 games): {avg:.2f}%")
    rank = (eligible.sort_values('incorrect_pct')['incorrect_pct'] < sf['incorrect_pct']).sum() + 1
    print(f"  Scott Foster's rank (higher rank = worse): {rank} of {len(eligible)}")
# end ana_07
