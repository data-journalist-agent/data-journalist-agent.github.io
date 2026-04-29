"""Overall call distribution and error rates."""
import pandas as pd

df = pd.read_parquet('/tmp/l2m_clean.parquet')

# --- ana_01: overall correctness distribution ---
print("=== ana_01 ===")
vc = df['review_decision'].value_counts()
total = vc.sum()
for k in ['CC', 'CNC', 'IC', 'INC']:
    print(f"{k}: {vc[k]} ({vc[k]/total*100:.2f}%)")
correct = vc['CC'] + vc['CNC']
incorrect = vc['IC'] + vc['INC']
print(f"\nTOTAL correct (CC+CNC): {correct} ({correct/total*100:.2f}%)")
print(f"TOTAL incorrect (IC+INC): {incorrect} ({incorrect/total*100:.2f}%)")
print(f"\n-- breakdown of incorrect --")
print(f"IC (wrong whistles): {vc['IC']} ({vc['IC']/incorrect*100:.1f}% of all errors)")
print(f"INC (missed whistles): {vc['INC']} ({vc['INC']/incorrect*100:.1f}% of all errors)")
print(f"\nINC/IC ratio: {vc['INC']/vc['IC']:.2f} (missed calls are {vc['INC']/vc['IC']:.1f}x more common than wrong whistles)")
# end ana_01

# --- ana_02: errors per game ---
print("\n=== ana_02 ===")
per_game = df.groupby('game_id')['review_decision'].apply(
    lambda s: ((s == 'IC') | (s == 'INC')).sum()
)
print(f"games: {len(per_game)}")
print(f"mean_errors_per_game: {per_game.mean():.2f}")
print(f"median_errors_per_game: {per_game.median():.2f}")
print(f"max_errors_in_a_game: {per_game.max()}")
print(f"min_errors_in_a_game: {per_game.min()}")
print(f"games_with_zero_errors: {(per_game == 0).sum()} ({(per_game==0).sum()/len(per_game)*100:.1f}%)")
print(f"games_with_5plus_errors: {(per_game >= 5).sum()} ({(per_game>=5).sum()/len(per_game)*100:.1f}%)")

# Distribution histogram
print("\nErrors per game distribution:")
dist = per_game.value_counts().sort_index()
for k, v in dist.items():
    print(f"{k} errors: {v} games")
# end ana_02
