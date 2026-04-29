"""Core analyses for the football managers dataset.

Each finding section is delimited with `# --- ana_xx: label ---` and prints
`=== ana_xx ===` so analyst.json can cite exact line ranges and outputs.
"""
import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/economist/04_managers-in-football-matter-much-less-than-most-fa/output_files"
ENC = "latin-1"

fixtures = pd.read_csv(f"{DATA}/big_five_league_expected_points_manager_tenures_df.csv", low_memory=False, encoding=ENC)
managers = pd.read_csv(f"{DATA}/manager_ratings_df.csv", encoding=ENC)
team_season = pd.read_csv(f"{DATA}/team_season_performance_df.csv", encoding=ENC)
all_tenures = pd.read_csv(f"{DATA}/manager_all_tenures_performance_df.csv", low_memory=False, encoding=ENC)
seq = pd.read_csv(f"{DATA}/manager_sequence_overperformance_df.csv", encoding=ENC)
players = pd.read_csv(f"{DATA}/player_ratings_df.csv", encoding=ENC)


# --- ana_01: Average forecast error per team-season ---
print("=== ana_01 ===")
ts = team_season.copy()
ts["abs_err"] = (ts["total_points"] - ts["total_expected_points"]).abs()
mean_err = ts["abs_err"].mean()
median_err = ts["abs_err"].median()
print(f"Mean absolute error: {mean_err:.2f} points")
print(f"Median absolute error: {median_err:.2f} points")
print(f"Team-seasons covered: {len(ts):,}")
print(f"Within 10 pts: {(ts['abs_err'] <= 10).mean()*100:.1f}%")
print(f"Within 5 pts: {(ts['abs_err'] <= 5).mean()*100:.1f}%")
err_buckets = pd.cut(ts["abs_err"], bins=[0,5,10,15,20,30,100], include_lowest=True)
print("\nError distribution:")
print(err_buckets.value_counts().sort_index())


# --- ana_02: Manager rating distribution — points added per season ---
print("\n=== ana_02 ===")
m = managers["ProjPointsAboveAverage"]
print(f"N managers (currently employed, 596): {len(managers)}")
print(f"Mean: {m.mean():.3f}")
print(f"Median: {m.median():.3f}")
print(f"Std: {m.std():.3f}")
print(f"Min: {m.min():.3f}  Max: {m.max():.3f}")
print(f"5th pct: {m.quantile(0.05):.3f}  95th pct: {m.quantile(0.95):.3f}")
print(f"Range top - bottom: {m.max() - m.min():.2f} points/season")
# bucket distribution for chart
buckets = pd.cut(m, bins=np.arange(-5, 5.5, 0.5), include_lowest=True)
hist = buckets.value_counts().sort_index()
print("\nDistribution (0.5-pt bins):")
for b, c in hist.items():
    mid = (b.left + b.right) / 2
    print(f"  bin_mid={mid:.2f}  count={c}")


# --- ana_03: Top 10 managers by projected points-above-average ---
print("\n=== ana_03 ===")
mgr = managers.copy()
mgr["TM_manager_name"] = mgr["TM_manager_name"].fillna("Unknown")
mgr["CurrentTeam"] = mgr["CurrentTeam"].fillna("(none)")
top = mgr.sort_values("ProjPointsAboveAverage", ascending=False).head(10)
for _, r in top.iterrows():
    print(f"{str(r['TM_manager_name']):<30s} ({str(r['CurrentTeam']):<22s})  proj={r['ProjPointsAboveAverage']:+.2f}  matches={int(r['PrevCareerMatches'])}")


# --- ana_04: Bottom 10 managers by projected points-above-average ---
print("\n=== ana_04 ===")
bot = mgr.sort_values("ProjPointsAboveAverage").head(10)
for _, r in bot.iterrows():
    print(f"{str(r['TM_manager_name']):<30s} ({str(r['CurrentTeam']):<22s})  proj={r['ProjPointsAboveAverage']:+.2f}  matches={int(r['PrevCareerMatches'])}")


# --- ana_05: 51% repeat overperformance — sequence test ---
print("\n=== ana_05 ===")
# Multi-tenure: rows where tenure2_above_expectation is not null.
multi = seq.dropna(subset=["tenure1_above_expectation", "tenure2_above_expectation"]).copy()
print(f"Managers with >=2 tenures of >=15 league games: {len(multi)}")
multi["t1_over"] = multi["tenure1_above_expectation"] > 0
multi["t2_over"] = multi["tenure2_above_expectation"] > 0
overachievers = multi[multi["t1_over"]]
n_over = len(overachievers)
n_repeat = overachievers["t2_over"].sum()
print(f"Overperformed in tenure 1: {n_over}")
print(f"Of those, also overperformed in tenure 2: {n_repeat} ({n_repeat/n_over*100:.1f}%)")

underachievers = multi[~multi["t1_over"]]
n_under = len(underachievers)
n_underrepeat = (~underachievers["t2_over"]).sum()
print(f"Underperformed in tenure 1: {n_under}")
print(f"Of those, also underperformed in tenure 2: {n_underrepeat} ({n_underrepeat/n_under*100:.1f}%)")


# --- ana_06: Squad strength dwarfs manager — Messi worth 9.2 vs Favre 3.76 ---
print("\n=== ana_06 ===")
top_mgr = managers["ProjPointsAboveAverage"].max()
top_player = players["PointsAboveAverage"].max()
top_player_name = players.loc[players["PointsAboveAverage"].idxmax(), "FIFA_player_name"]
print(f"Best projected manager (per season): +{top_mgr:.2f} pts")
print(f"Best single player ({top_player_name}): +{top_player:.2f} pts/season")
print(f"Top player worth {top_player/top_mgr:.2f}x the top manager")
# Top 10 attackers and goalkeepers
att = players[players["PosGroup"] == "attack"].sort_values("PointsAboveAverage", ascending=False).head(5)
gk = players[players["PosGroup"] == "goalkeeper"].sort_values("PointsAboveAverage", ascending=False).head(5)
print("Top attackers:")
for _, r in att.iterrows():
    print(f"  {r['FIFA_player_name']:<30s} +{r['PointsAboveAverage']:.2f} pts/season")
print("Top goalkeepers:")
for _, r in gk.iterrows():
    print(f"  {r['FIFA_player_name']:<30s} +{r['PointsAboveAverage']:.2f} pts/season")


# --- ana_07: Distribution of player value by position group ---
print("\n=== ana_07 ===")
for grp in ["attack", "defence", "goalkeeper"]:
    sub = players[players["PosGroup"] == grp]["PointsAboveAverage"]
    print(f"{grp:<11s} n={len(sub):4d}  median={sub.median():+.2f}  p95={sub.quantile(0.95):+.2f}  max={sub.max():+.2f}")


# --- ana_08: Biggest team season-level surprises (top overperformers) ---
print("\n=== ana_08 ===")
ts2 = team_season.copy()
ts2["over"] = ts2["total_points"] - ts2["total_expected_points"]
top_over = ts2.sort_values("over", ascending=False).head(10)
for _, r in top_over.iterrows():
    print(f"{int(r['season'])} {r['league_country']:<8s} {r['team']:<20s}  actual={r['total_points']:.0f}  exp={r['total_expected_points']:.1f}  +{r['over']:.1f}")


# --- ana_09: Biggest team season-level disappointments ---
print("\n=== ana_09 ===")
worst = ts2.sort_values("over").head(10)
for _, r in worst.iterrows():
    print(f"{int(r['season'])} {r['league_country']:<8s} {r['team']:<20s}  actual={r['total_points']:.0f}  exp={r['total_expected_points']:.1f}  {r['over']:+.1f}")


# --- ana_10: Manager rating spans only ~7 points; squad spans 70+ ---
print("\n=== ana_10 ===")
mgr_range = managers["ProjPointsAboveAverage"].max() - managers["ProjPointsAboveAverage"].min()
sq_range = ts["total_expected_points"].max() - ts["total_expected_points"].min()
print(f"Manager rating range (best - worst, currently employed): {mgr_range:.2f} pts/season")
print(f"Team expected-points range across all team-seasons: {sq_range:.1f} pts")
print(f"Best team xPts: {ts['total_expected_points'].max():.1f}  Worst: {ts['total_expected_points'].min():.1f}")


# --- ana_11: Tenure carryover — how much past performance follows a manager ---
print("\n=== ana_11 ===")
# Per the methodology (det_05): w = games / (games + 461)
def carry(games):
    return games / (games + 461)
xs = [38, 76, 114, 190, 380, 570]
for g in xs:
    print(f"games={g:>4d}  carryover={carry(g)*100:.1f}%")


# --- ana_12: Famous-name reality check ---
print("\n=== ana_12 ===")
names = ["Pep Guardiola", "Jürgen Klopp", "Jurgen Klopp", "José Mourinho", "Jose Mourinho",
         "Sir Alex Ferguson", "Mauricio Pochettino", "Maurizio Sarri", "Antonio Conte",
         "Carlo Ancelotti", "Diego Simeone", "Massimiliano Allegri", "Lucien Favre",
         "Marcelo Bielsa", "Eddie Howe", "Sean Dyche", "Arsène Wenger", "Arsene Wenger",
         "Zinédine Zidane", "Zinedine Zidane"]
sub = mgr[mgr["TM_manager_name"].isin(names)].sort_values("ProjPointsAboveAverage", ascending=False)
for _, r in sub.iterrows():
    print(f"{str(r['TM_manager_name']):<26s} ({str(r['CurrentTeam']):<22s})  {r['ProjPointsAboveAverage']:+.2f}  matches={int(r['PrevCareerMatches'])}")


# --- ana_13: Career length distribution among rated managers ---
print("\n=== ana_13 ===")
games = managers["PrevCareerMatches"]
print(f"N managers: {len(managers)}")
print(f"Median games: {games.median():.0f}")
print(f"Mean games: {games.mean():.1f}")
print(f"Pct with <=38 games (1 season): {(games <= 38).mean()*100:.1f}%")
print(f"Pct with <=76 games (2 seasons): {(games <= 76).mean()*100:.1f}%")
print(f"Pct with >=380 games (10 seasons): {(games >= 380).mean()*100:.1f}%")


# --- ana_14: Distribution of manager nationalities ---
print("\n=== ana_14 ===")
nat = all_tenures.drop_duplicates(subset=["TM_manager_id"])["TM_manager_nationality"].value_counts().head(10)
print(nat)


# --- ana_15: How sackings shape the data — tenure lengths ---
print("\n=== ana_15 ===")
games_per_tenure = all_tenures["current_tenure_total_games"].dropna()
print(f"N tenures with >=1 game: {len(games_per_tenure)}")
print(f"Median tenure length (games): {games_per_tenure.median():.0f}")
print(f"Mean: {games_per_tenure.mean():.1f}")
print(f"<= 38 games (1 season): {(games_per_tenure <= 38).mean()*100:.1f}%")
print(f"<= 76 games (2 seasons): {(games_per_tenure <= 76).mean()*100:.1f}%")
print(f">= 190 games (5 seasons): {(games_per_tenure >= 190).mean()*100:.1f}%")
