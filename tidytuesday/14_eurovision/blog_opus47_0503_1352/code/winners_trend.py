"""Winners by year + winners by region (East vs West) trend."""
import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/14_eurovision"
contest = pd.read_csv(f"{DATA_DIR}/eurovision.csv")
finals = contest[contest.section.isin(["final", "grand-final"])].copy()

# --- ana_17: Winners list (year + country + song + artist) ---
print("=== ana_17 ===")
winners = finals[finals.winner == True][["year", "artist_country", "artist", "song", "total_points"]].sort_values("year")
print(winners.to_string(index=False))
print(f"total winners listed: {len(winners)}")

# --- ana_18: Winners by region (Western Europe vs Eastern Europe vs Nordic) over time ---
print("=== ana_18 ===")
WESTERN = {"United Kingdom", "France", "Germany", "Spain", "Italy", "Belgium",
           "Netherlands", "The Netherlands", "Switzerland", "Austria", "Ireland",
           "Luxembourg", "Monaco", "Portugal", "Malta"}
NORDIC = {"Sweden", "Norway", "Denmark", "Finland", "Iceland"}
EASTERN = {"Russia", "Ukraine", "Belarus", "Estonia", "Latvia", "Lithuania", "Moldova",
           "Armenia", "Azerbaijan", "Georgia", "Croatia", "Slovenia", "Serbia",
           "Bosnia & Herzegovina", "Macedonia", "F.Y.R. Macedonia", "North Macedonia",
           "Albania", "Bulgaria", "Romania", "Hungary", "Poland", "Slovakia",
           "Czech Republic", "Yugoslavia", "Serbia & Montenegro", "Montenegro"}
SOUTH = {"Greece", "Cyprus", "Turkey", "Israel"}

def region(c):
    if c in WESTERN: return "Western Europe"
    if c in NORDIC: return "Nordic"
    if c in EASTERN: return "Eastern Europe"
    if c in SOUTH: return "South/Med"
    return "Other"

winners["region"] = winners.artist_country.map(region)
print(winners.region.value_counts().to_string())
print("Decade x region:")
winners["decade"] = (winners.year // 10) * 10
print(pd.crosstab(winners.decade, winners.region).to_string())

# --- ana_19: Top points received in a single final ---
print("=== ana_19 ===")
top_pts = finals[finals.total_points.notna()].sort_values("total_points", ascending=False).head(15)
print(top_pts[["year", "artist_country", "artist", "song", "total_points", "rank"]].to_string(index=False))

# --- ana_20: Years with most/fewest competitors in final ---
print("=== ana_20 ===")
participants_per_year = finals.groupby("year").size()
print("Top 10 most-attended finals:")
print(participants_per_year.sort_values(ascending=False).head(10).to_string())
print("Bottom 10 (least competitors):")
print(participants_per_year.sort_values().head(10).to_string())

# --- ana_21: Annual competitor counts (full series, for trend chart) ---
print("=== ana_21 ===")
# include all sections so we can show growth of participation through semis
all_year = contest.groupby("year").artist_country.nunique()
print(all_year.to_string())
