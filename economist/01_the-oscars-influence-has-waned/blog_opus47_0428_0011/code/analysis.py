"""Analysis for The Economist's Oscars influence dataset.

Run from: project/economist/01_the-oscars-influence-has-waned/blog_opus47_*/
Data:    /Users/forrest/Desktop/data2blog/data_pkg/economist/01_the-oscars-influence-has-waned/movie-counts.csv
"""
import pandas as pd
import numpy as np

CSV = "/Users/forrest/Desktop/data2blog/data_pkg/economist/01_the-oscars-influence-has-waned/movie-counts.csv"

# Load. README says encoding may be tricky.
try:
    df = pd.read_csv(CSV)
except UnicodeDecodeError:
    df = pd.read_csv(CSV, encoding="latin-1")

# Cap at 2016 as the Economist did.
df = df[df["release_year"] <= 2016].copy()

# --- ana_01: dataset profile ---
print("=== ana_01 ===")
print(f"rows: {len(df)}")
print(f"unique films: {df['movie_name'].nunique()}")
print(f"release_year range: {df['release_year'].min()} - {df['release_year'].max()}")
print(f"oscars_year range: {df['oscars_year'].min()} - {df['oscars_year'].max()}")
print(f"Best Picture winners (W): {(df['result']=='W').sum()}")
print(f"Best Picture nominees (N): {(df['result']=='N').sum()}")
print(f"Other films: {df['result'].isna().sum() + (df['result']=='').sum()}")

# Helper: year-rank table on top-100 (data already filtered to top-100 per year per README)
print("\nrows with year_rank present:", df["year_rank"].notna().sum())

# --- ana_02: top 20 most-referenced films of all time ---
print("\n=== ana_02 ===")
top20 = df.nlargest(20, "count")[["movie_name", "release_year", "result", "count", "annual_share"]]
print(top20.to_string(index=False))

# --- ana_03: Best Picture winners ranked by their year_rank ---
print("\n=== ana_03 ===")
winners = df[df["result"] == "W"].copy()
winners["year_rank"] = winners["year_rank"].astype(int)
winners["decade"] = (winners["oscars_year"] // 10) * 10
print(f"total winners in dataset: {len(winners)}")
print("year_rank distribution among winners:")
print(winners["year_rank"].describe())
print("\nyear_rank value counts:")
print(winners["year_rank"].value_counts().sort_index().head(20))

# --- ana_04: Best Picture winner average year_rank by decade ---
print("\n=== ana_04 ===")
by_dec = winners.groupby("decade").agg(
    n=("movie_name", "count"),
    mean_year_rank=("year_rank", "mean"),
    median_year_rank=("year_rank", "median"),
    pct_rank1=("year_rank", lambda s: (s == 1).mean() * 100),
    mean_share=("annual_share", "mean"),
).round(3)
print(by_dec)

# --- ana_05: Best Picture winners with year_rank > 10 ---
print("\n=== ana_05 ===")
flops = winners[winners["year_rank"] > 10].sort_values("year_rank", ascending=False)
print(f"winners ranked outside top 10 of their year: {len(flops)} of {len(winners)}")
print(flops[["movie_name", "oscars_year", "year_rank", "count", "annual_share"]].to_string(index=False))

# --- ana_06: Year-rank-1 films that were not even nominated for Best Picture ---
print("\n=== ana_06 ===")
top1 = df[df["year_rank"] == 1].copy()
top1["nominated"] = top1["result"].isin(["W", "N"])
not_nom = top1[~top1["nominated"]].sort_values("count", ascending=False)
print(f"#1 in their year but not BP-nominated: {len(not_nom)} of {len(top1)} (={len(not_nom)/len(top1)*100:.1f}%)")
print(not_nom[["movie_name", "oscars_year", "count", "annual_share"]].head(30).to_string(index=False))

# --- ana_07: Share of total annual references captured by the Best Picture winner ---
print("\n=== ana_07 ===")
print("annual_share of BP winners over time:")
share = winners[["oscars_year", "movie_name", "annual_share", "year_rank"]].sort_values("oscars_year")
print(share.to_string(index=False))

# --- ana_08: BP winners vs nominees vs unnominated, by decade — median count and median year_rank ---
print("\n=== ana_08 ===")
df["decade"] = (df["release_year"] // 10) * 10
df["bucket"] = df["result"].map({"W": "winner", "N": "nominee"}).fillna("none")
piv_count = df.groupby(["decade", "bucket"])["count"].median().unstack().round(1)
print("median count by decade × bucket:")
print(piv_count)
print("\nmedian year_rank by decade × bucket:")
piv_rank = df.groupby(["decade", "bucket"])["year_rank"].median().unstack().round(1)
print(piv_rank)

# --- ana_09: Concentration: top film's share of references in its year, by decade ---
print("\n=== ana_09 ===")
top_per_year = df[df["year_rank"] == 1][["release_year", "annual_share", "count", "movie_name"]]
top_per_year["decade"] = (top_per_year["release_year"] // 10) * 10
conc = top_per_year.groupby("decade")["annual_share"].agg(["mean", "median", "max"]).round(3)
print("share of #1 film over all references in its year, by decade:")
print(conc)

# --- ana_10: Top film by year (1928 - 2016) ---
print("\n=== ana_10 ===")
top1_by_year = df[df["year_rank"] == 1][
    ["release_year", "movie_name", "count", "annual_share", "result"]
].sort_values("release_year")
print(top1_by_year.to_string(index=False))

# --- ana_11: Best Picture winner annual_share, decade-by-decade ---
print("\n=== ana_11 ===")
winner_share_dec = winners.groupby("decade").agg(
    n=("movie_name", "count"),
    median_share=("annual_share", "median"),
    mean_share=("annual_share", "mean"),
).round(4)
print(winner_share_dec)

# --- ana_12: Years where winner ranked #1 vs not ---
print("\n=== ana_12 ===")
winners["is_top"] = winners["year_rank"] == 1
top_ratio = winners.groupby("decade")["is_top"].mean().round(3) * 100
print("Pct of winners ranked #1 in their year, by decade:")
print(top_ratio)
print(f"\noverall: {winners['is_top'].mean()*100:.1f}% of all winners were #1 in their year")

# --- ana_13: Genre-style top-15 vs Best Picture overlap ---
print("\n=== ana_13 ===")
overall_top15 = df.nlargest(15, "count")[["movie_name", "release_year", "result", "count"]]
print(overall_top15.to_string(index=False))
print(f"\nof the all-time top 15, BP winners: {(overall_top15['result']=='W').sum()}, nominees: {(overall_top15['result']=='N').sum()}, neither: {overall_top15['result'].isna().sum()}")

# --- ana_14: Winners' pct of their year's total references — averages by era ---
print("\n=== ana_14 ===")
winners_with_share = winners[["oscars_year", "movie_name", "annual_share", "year_rank", "count"]].copy()
era_bins = [1927, 1949, 1969, 1989, 2016]
era_labels = ["1928-1949 (golden age)", "1950-1969 (studio decline)", "1970-1989 (new hollywood)", "1990-2016 (modern)"]
winners_with_share["era"] = pd.cut(winners_with_share["oscars_year"], bins=era_bins, labels=era_labels)
era_table = winners_with_share.groupby("era", observed=True).agg(
    n=("movie_name", "count"),
    mean_share=("annual_share", "mean"),
    median_share=("annual_share", "median"),
    median_year_rank=("year_rank", "median"),
    pct_rank1=("year_rank", lambda s: (s == 1).mean() * 100),
).round(3)
print(era_table)

# --- ana_15: Decades where the winner had the lowest share ---
print("\n=== ana_15 ===")
worst_winners = winners.nsmallest(15, "annual_share")[["movie_name", "oscars_year", "annual_share", "year_rank", "count"]]
print(worst_winners.to_string(index=False))

# --- ana_16: Top reference film never nominated for BP — biggest snubs ---
print("\n=== ana_16 ===")
unnom = df[(df["year_rank"] == 1) & ~df["result"].isin(["W", "N"])].copy()
# attach the BP winner of that year for comparison
winner_lookup = winners.set_index("oscars_year")[["movie_name", "count", "annual_share"]].rename(
    columns={"movie_name": "winner_name", "count": "winner_count", "annual_share": "winner_share"}
)
snubs = unnom.merge(winner_lookup, left_on="oscars_year", right_index=True, how="left")
snubs["count_ratio"] = snubs["count"] / snubs["winner_count"]
snubs = snubs.dropna(subset=["winner_name"]).sort_values("count_ratio", ascending=False)
cols = ["oscars_year", "movie_name", "count", "annual_share", "winner_name", "winner_count", "count_ratio"]
print("year-#1 (not nominated) vs that year's actual BP winner — biggest gaps:")
print(snubs[cols].head(20).to_string(index=False))
