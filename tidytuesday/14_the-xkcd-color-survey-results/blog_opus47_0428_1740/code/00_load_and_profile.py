"""Load and profile all three xkcd Color Survey CSVs.

Run from this directory; data lives at the absolute path below.
"""
import pandas as pd
import numpy as np

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/14_the-xkcd-color-survey-results'

# --- ana_01: Dataset shape ---
print("=== ana_01 ===")
color_ranks = pd.read_csv(f'{DATA_DIR}/color_ranks.csv')
users = pd.read_csv(f'{DATA_DIR}/users.csv')
# answers is large — use chunked count first
answers_n = sum(1 for _ in open(f'{DATA_DIR}/answers.csv')) - 1
print(f"color_ranks rows: {len(color_ranks)}, cols: {len(color_ranks.columns)}")
print(f"users rows: {len(users)}, cols: {len(users.columns)}")
print(f"answers rows (line count): {answers_n}")

# --- ana_02: User demographics composition ---
print("=== ana_02 ===")
print("Monitor distribution:")
print(users['monitor'].value_counts(dropna=False))
print(f"\nY-chromosome rate (1 = yes): {users['y_chromosome'].mean():.4f} (n_yes={int(users['y_chromosome'].sum())} / n={len(users)})")
print(f"Colorblind rate: {users['colorblind'].mean():.4f} (n_yes={int(users['colorblind'].sum())} / n={len(users)})")
print(f"Mean spam_prob: {users['spam_prob'].mean():.4f}, median: {users['spam_prob'].median():.4f}")
print(f"Spam_prob > 0.5: {(users['spam_prob'] > 0.5).sum()} ({(users['spam_prob'] > 0.5).mean()*100:.2f}%)")

# --- ana_03: Colorblindness by chromosome ---
print("=== ana_03 ===")
ct = pd.crosstab(users['y_chromosome'], users['colorblind'], margins=True)
print(ct)
xy = users[users['y_chromosome'] == 1]
xx = users[users['y_chromosome'] == 0]
print(f"Colorblind | XY: {xy['colorblind'].mean()*100:.3f}% (n={len(xy)})")
print(f"Colorblind | XX: {xx['colorblind'].mean()*100:.3f}% (n={len(xx)})")
ratio = xy['colorblind'].mean() / max(xx['colorblind'].mean(), 1e-9)
print(f"Ratio XY/XX: {ratio:.2f}x")

# --- ana_04: color_ranks profile ---
print("=== ana_04 ===")
print(color_ranks.head(10))
print(f"\nTotal named colors: {len(color_ranks)}")
print(f"Unique color names: {color_ranks['color'].nunique()}")
print(f"Unique hex codes: {color_ranks['hex'].nunique()}")
