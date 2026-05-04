"""Jury vs televote divergence and 2022 Ukraine breakdown."""
import pandas as pd
import numpy as np

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/14_eurovision"
votes = pd.read_csv(f"{DATA_DIR}/eurovision-votes.csv")

final_votes = votes[(votes.semi_final == "f") & (votes.from_country != votes.to_country)].copy()

# --- ana_13: 2022 Ukraine jury vs televote points received ---
print("=== ana_13 ===")
ua = final_votes[(final_votes.year == 2022) & (final_votes.to_country == "Ukraine")]
print(ua.groupby("jury_or_televoting").points.agg(["sum", "count", "mean"]).to_string())
print("Distribution of jury points to UA in 2022:")
print(ua[ua.jury_or_televoting == "J"].points.value_counts().sort_index().to_string())
print("Distribution of televote points to UA in 2022:")
print(ua[ua.jury_or_televoting == "T"].points.value_counts().sort_index().to_string())

# --- ana_14: 2022 final winner gap (top by jury vs by televote) ---
print("=== ana_14 ===")
year2022 = final_votes[final_votes.year == 2022]
jury_totals = year2022[year2022.jury_or_televoting == "J"].groupby("to_country").points.sum().sort_values(ascending=False)
tele_totals = year2022[year2022.jury_or_televoting == "T"].groupby("to_country").points.sum().sort_values(ascending=False)
print("Top 10 jury totals 2022:")
print(jury_totals.head(10).to_string())
print("Top 10 televote totals 2022:")
print(tele_totals.head(10).to_string())

# --- ana_15: All jury vs televote rank divergences (post-2016) ---
print("=== ana_15 ===")
# Build per-year jury rank and televote rank, find max divergence
def yearly_rank_diverge(year):
    yv = final_votes[final_votes.year == year]
    jury = yv[yv.jury_or_televoting == "J"].groupby("to_country").points.sum().rank(ascending=False, method="min")
    tele = yv[yv.jury_or_televoting == "T"].groupby("to_country").points.sum().rank(ascending=False, method="min")
    df = pd.DataFrame({"jury_rank": jury, "tele_rank": tele}).dropna()
    df["abs_diff"] = (df.jury_rank - df.tele_rank).abs()
    return df

rows = []
for y in sorted(final_votes.year.unique()):
    yv = final_votes[final_votes.year == y]
    if yv.jury_or_televoting.nunique() < 2:
        continue
    df = yearly_rank_diverge(y)
    if len(df) == 0:
        continue
    top = df.sort_values("abs_diff", ascending=False).head(1)
    rows.append((y, top.index[0], int(top.jury_rank.values[0]), int(top.tele_rank.values[0]), int(top.abs_diff.values[0])))

div_df = pd.DataFrame(rows, columns=["year", "country", "jury_rank", "tele_rank", "rank_diff"])
print(div_df.sort_values("rank_diff", ascending=False).head(15).to_string(index=False))

# --- ana_16: Ireland's 1992-1996 streak (3 in a row + 1996) details ---
print("=== ana_16 ===")
contest = pd.read_csv(f"{DATA_DIR}/eurovision.csv")
finals = contest[contest.section.isin(["final", "grand-final"])]
ire_wins = finals[(finals.artist_country == "Ireland") & (finals.winner == True)]
print(ire_wins[["year", "artist", "song", "total_points", "rank"]].sort_values("year").to_string(index=False))
