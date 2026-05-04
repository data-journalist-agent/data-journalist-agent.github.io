"""Profile + per-column inventory for the Eurovision dataset.
Run from DATA_DIR.
"""
import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/14_eurovision"

contest = pd.read_csv(f"{DATA_DIR}/eurovision.csv")
votes = pd.read_csv(f"{DATA_DIR}/eurovision-votes.csv")

# --- ana_00: Dataset profile ---
print("=== ana_00 ===")
print(f"contest rows={len(contest)} cols={contest.shape[1]}")
print(f"votes rows={len(votes)} cols={votes.shape[1]}")
print(f"contest year range: {int(contest.year.min())} - {int(contest.year.max())}")
print(f"votes year range: {int(votes.year.min())} - {int(votes.year.max())}")
print("contest columns:", list(contest.columns))
print("votes columns:", list(votes.columns))
print("section values:", contest.section.value_counts().to_dict())
print("jury_or_televoting:", votes.jury_or_televoting.value_counts().to_dict())
print(f"unique countries (contest): {contest.artist_country.nunique()}")
print(f"unique countries (votes from): {votes.from_country.nunique()}")
print(f"unique countries (votes to): {votes.to_country.nunique()}")

# --- ana_01: missingness in contest table ---
print("=== ana_01 ===")
miss = contest.isna().sum()
print(miss[miss > 0])
