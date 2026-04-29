"""Worst games — most errors in a single L2M-reviewed game."""
import pandas as pd

df = pd.read_parquet('/tmp/l2m_clean.parquet')

# --- ana_15: games with most errors ---
print("=== ana_15 ===")
# Per game, count errors and context
errs = df[df['review_decision'].isin(['IC', 'INC'])].copy()
per_game = errs.groupby('game_id').size().sort_values(ascending=False)
# Get game context for top 10
top_game_ids = per_game.head(10).index.tolist()
print(f"{'game_id':25s} {'date':>10s} {'matchup':>15s} {'errors':>7s} {'refs':>0s}")
for gid in top_game_ids:
    gm = df[df['game_id'] == gid].iloc[0]
    refs = f"{gm.get('ref_1','?')}, {gm.get('ref_2','?')}, {gm.get('ref_3','?')}"
    date = str(gm['date'].date())
    matchup = f"{gm['away']} at {gm['home']}"
    n = per_game[gid]
    print(f"{gid:25s} {date:>10s} {matchup:>15s} {int(n):7d}  {refs}")
# end ana_15

# --- ana_16: ref_made_call true vs false rates ---
print("\n=== ana_16 ===")
# ref_made_call is whether the original call was blown (made) or non-call
# When it's True: IC means the call should not have been made (wrong whistle)
# When it's False: INC means the call should have been made (missed)
# This is just a sanity check
print("ref_made_call distribution:")
print(df['ref_made_call'].value_counts(dropna=False))
# end ana_16
