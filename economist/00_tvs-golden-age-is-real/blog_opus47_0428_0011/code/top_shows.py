"""Top-rated seasons and shows; within-show trajectories of legendary series."""

import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/economist/00_tvs-golden-age-is-real/IMDb_Economist_tv_ratings.csv"

df = pd.read_csv(DATA)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year

# --- ana_06: Top 20 highest-rated seasons in the whole dataset ---
print("=== ana_06 ===")
top20 = df.sort_values("av_rating", ascending=False).head(20)[
    ["title", "seasonNumber", "year", "av_rating", "share", "genres"]
]
print(top20.to_string(index=False))

# --- ana_07: Top 15 shows by their highest-rated season ---
print("\n=== ana_07 ===")
peak = (
    df.sort_values("av_rating", ascending=False)
    .groupby("title", as_index=False)
    .first()
    .sort_values("av_rating", ascending=False)
    .head(15)[["title", "seasonNumber", "year", "av_rating"]]
)
print(peak.to_string(index=False))

# --- ana_08: Shows with the most seasons in this dataset ---
print("\n=== ana_08 ===")
counts = df.groupby("title").size().sort_values(ascending=False).head(15)
print(counts.to_string())

# --- ana_09: Within-show trajectories for landmark prestige series ---
print("\n=== ana_09 ===")
landmark = [
    "Breaking Bad",
    "The Sopranos",
    "The Wire",
    "Game of Thrones",
    "Mad Men",
    "Six Feet Under",
    "Better Call Saul",
    "Fargo",
    "True Detective",
]
for show in landmark:
    sub = df[df["title"] == show].sort_values("seasonNumber")
    if sub.empty:
        print(f"-- {show}: NOT IN DATASET")
        continue
    print(f"-- {show}")
    print(
        sub[["seasonNumber", "year", "av_rating", "share"]].to_string(index=False)
    )
