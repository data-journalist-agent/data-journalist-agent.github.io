"""Wins and grand-final ranking analysis."""
import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/14_eurovision"
contest = pd.read_csv(f"{DATA_DIR}/eurovision.csv")

# Treat 'final' (pre-2004) and 'grand-final' (2004+) as the equivalent main contest
finals = contest[contest.section.isin(["final", "grand-final"])].copy()

# --- ana_02: Wins by country (full table) ---
print("=== ana_02 ===")
winners = finals[finals.winner == True]
wins = winners.artist_country.value_counts()
print(wins.to_string())
print(f"countries with at least one win: {len(wins)}")

# --- ana_03: Top finalists by participation (count of grand-final/final appearances) ---
print("=== ana_03 ===")
appearances = finals.artist_country.value_counts()
print(appearances.head(15).to_string())
print(f"min year per country (top 15):")
top15_countries = appearances.head(15).index.tolist()
print(finals[finals.artist_country.isin(top15_countries)].groupby("artist_country").year.agg(["min", "max", "count"]).sort_values("count", ascending=False).head(15).to_string())

# --- ana_04: Average final rank by country (min 5 finals) ---
print("=== ana_04 ===")
ranked = finals.dropna(subset=["rank"]).copy()
ranked["rank"] = ranked["rank"].astype(int)
avg_rank = ranked.groupby("artist_country").agg(
    avg_rank=("rank", "mean"),
    median_rank=("rank", "median"),
    finals_n=("rank", "count"),
).query("finals_n >= 5").sort_values("avg_rank")
print(avg_rank.head(15).to_string())
print("---")
print(avg_rank.tail(15).to_string())

# --- ana_05: Last-place finishes (rank == max in each year's grand-final/final) ---
print("=== ana_05 ===")
ranked["yearly_max"] = ranked.groupby("year")["rank"].transform("max")
last_places = ranked[ranked["rank"] == ranked.yearly_max]
last_counts = last_places.artist_country.value_counts()
print(last_counts.head(15).to_string())
print(f"countries with at least one last place: {len(last_counts)}")

# --- ana_06: Nul-points finishes in finals (total_points == 0) ---
print("=== ana_06 ===")
nul = finals[(finals.total_points == 0) & finals.total_points.notna()]
print(f"total nul-points finishes in finals: {len(nul)}")
nul_country = nul.artist_country.value_counts()
print(nul_country.to_string())
print("Years/countries of nul-points:")
print(nul[["year", "artist_country", "song", "artist"]].sort_values("year").to_string(index=False))
