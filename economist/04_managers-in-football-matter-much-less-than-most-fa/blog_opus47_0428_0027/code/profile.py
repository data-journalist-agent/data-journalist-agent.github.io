"""Dataset profile + field inventory for the football managers dataset."""
import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2blog/data_pkg/economist/04_managers-in-football-matter-much-less-than-most-fa/output_files"
ENC = "latin-1"

# --- ana_profile: Dataset profile ---
print("=== ana_profile ===")
fixtures = pd.read_csv(f"{DATA}/big_five_league_expected_points_manager_tenures_df.csv", low_memory=False, encoding=ENC)
managers = pd.read_csv(f"{DATA}/manager_ratings_df.csv", encoding=ENC)
team_season = pd.read_csv(f"{DATA}/team_season_performance_df.csv", encoding=ENC)
all_tenures = pd.read_csv(f"{DATA}/manager_all_tenures_performance_df.csv", low_memory=False, encoding=ENC)
seq = pd.read_csv(f"{DATA}/manager_sequence_overperformance_df.csv", encoding=ENC)
players = pd.read_csv(f"{DATA}/player_ratings_df.csv", encoding=ENC)
mtable = pd.read_csv(f"{DATA}/manager_table_df.csv", encoding=ENC)

print(f"Fixtures: {len(fixtures):,} matches; cols={fixtures.shape[1]}")
print(f"Manager ratings: {len(managers):,} currently-employed managers")
print(f"All tenures: {len(all_tenures):,} manager-team tenure records")
print(f"Team-season performance: {len(team_season):,} rows")
print(f"Sequence (multi-tenure managers): {len(seq):,}")
print(f"Players rated: {len(players):,}")
print(f"Manager table (current): {len(mtable):,}")

print("\nFixtures date range:", fixtures['date'].min(), "to", fixtures['date'].max())
print("Leagues:", sorted(fixtures['league_country'].unique().tolist()))
print("Seasons:", sorted(fixtures['season'].unique().tolist()))
