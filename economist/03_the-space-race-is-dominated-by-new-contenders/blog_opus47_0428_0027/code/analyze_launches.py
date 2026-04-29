"""Space launches analysis — produces all ana_xx findings.

Run:
    python3 analyze_launches.py

Prints findings tagged === ana_xx === so calculation.lines can be located by
searching for the tag in the printed output.
"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path("/Users/forrest/Desktop/data2blog/data_pkg/economist/03_the-space-race-is-dominated-by-new-contenders")
launches = pd.read_csv(DATA_DIR / "launches.csv")
agencies = pd.read_csv(DATA_DIR / "agencies.csv")

# Treat SU and RU as one continuous Russia/USSR line
launches["state_combined"] = launches["state_code"].replace({"SU": "RU/SU", "RU": "RU/SU"})


# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"Rows: {len(launches)}")
print(f"Columns: {len(launches.columns)}")
print(f"Year range: {launches['launch_year'].min()} - {launches['launch_year'].max()}")
print(f"Unique states: {launches['state_code'].nunique()}")
print(f"Unique vehicle types: {launches['type'].nunique()}")
print(f"Unique agencies: {launches['agency'].nunique()}")
print(f"Successes (O): {(launches['category']=='O').sum()}")
print(f"Failures (F): {(launches['category']=='F').sum()}")


# --- ana_02: Launches per year (all, success only) ---
print("\n=== ana_02 ===")
yearly = launches.groupby("launch_year").size().rename("total")
yearly_success = launches[launches["category"] == "O"].groupby("launch_year").size().rename("successes")
yearly_fail = launches[launches["category"] == "F"].groupby("launch_year").size().rename("failures")
yearly_df = pd.concat([yearly, yearly_success, yearly_fail], axis=1).fillna(0).astype(int)
yearly_df = yearly_df.reset_index()
print(yearly_df.head(10).to_string(index=False))
print("...")
print(yearly_df.tail(10).to_string(index=False))
peak_year = yearly_df.loc[yearly_df["total"].idxmax()]
print(f"Peak year: {int(peak_year['launch_year'])} with {int(peak_year['total'])} total launches")


# --- ana_03: Top launching states (all-time, successful only) ---
print("\n=== ana_03 ===")
state_success = launches[launches["category"] == "O"].groupby("state_combined").size().sort_values(ascending=False)
total_success = state_success.sum()
state_pct = (state_success / total_success * 100).round(1)
top_states = pd.DataFrame({"state": state_success.index, "successes": state_success.values, "pct": state_pct.values})
print(top_states.to_string(index=False))


# --- ana_04: Annual launches by major state, success only ---
print("\n=== ana_04 ===")
major_states = ["RU/SU", "US", "CN", "F", "J", "IN"]
ms = launches[(launches["category"] == "O") & (launches["state_combined"].isin(major_states))]
by_year_state = ms.groupby(["launch_year", "state_combined"]).size().unstack(fill_value=0)
# Ensure all major states have columns
for s in major_states:
    if s not in by_year_state.columns:
        by_year_state[s] = 0
by_year_state = by_year_state[major_states].reset_index()
print(by_year_state.head(5).to_string(index=False))
print("...")
print(by_year_state.tail(15).to_string(index=False))


# --- ana_05: Soviet peak vs post-1991 collapse ---
print("\n=== ana_05 ===")
ru_su_year = launches[(launches["state_combined"] == "RU/SU") & (launches["category"] == "O")] \
    .groupby("launch_year").size()
soviet_peak = ru_su_year.idxmax()
soviet_peak_count = ru_su_year.max()
post_collapse = ru_su_year.loc[1996:2000].mean()
ratio = soviet_peak_count / post_collapse if post_collapse else float("nan")
print(f"Soviet/Russian peak year: {soviet_peak} with {soviet_peak_count} launches")
print(f"Mean 1996-2000: {post_collapse:.1f}")
print(f"Drop ratio: {ratio:.1f}x")


# --- ana_06: 2018 snapshot — China leads ---
print("\n=== ana_06 ===")
y2018 = launches[(launches["launch_year"] == 2018) & (launches["category"] == "O")]
top_2018 = y2018.groupby("state_combined").size().sort_values(ascending=False)
print(top_2018.to_string())
print(f"Total 2018 successes: {len(y2018)}")


# --- ana_07: Agency-type rise — state vs private vs startup ---
print("\n=== ana_07 ===")
type_year = launches[launches["category"] == "O"].groupby(["launch_year", "agency_type"]).size().unstack(fill_value=0)
# Reorder columns
cols = [c for c in ["state", "private", "startup"] if c in type_year.columns]
type_year = type_year[cols].reset_index()
print(type_year.head(5).to_string(index=False))
print("...")
print(type_year.tail(15).to_string(index=False))


# --- ana_08: Top agencies all-time ---
print("\n=== ana_08 ===")
agency_success = launches[launches["category"] == "O"].groupby("agency").size().sort_values(ascending=False)
top10 = agency_success.head(10).reset_index()
top10.columns = ["agency", "successes"]
print(top10.to_string(index=False))


# --- ana_09: Failure rate per decade ---
print("\n=== ana_09 ===")
launches["decade"] = (launches["launch_year"] // 10) * 10
dec = launches.groupby("decade")["category"].apply(
    lambda s: pd.Series({"total": len(s), "failures": (s == "F").sum()})
).unstack()
dec["failure_pct"] = (dec["failures"] / dec["total"] * 100).round(2)
dec = dec.reset_index()
print(dec.to_string(index=False))


# --- ana_10: SpaceX rise (private operator) ---
print("\n=== ana_10 ===")
sx = launches[(launches["agency"] == "SPX") & (launches["category"] == "O")] \
    .groupby("launch_year").size()
print(sx.to_string())
print(f"SpaceX total successes through dataset: {sx.sum()}")
print(f"SpaceX 2018 successes: {sx.get(2018, 0)}")


# --- ana_11: Cumulative launches by state — racing chart ---
print("\n=== ana_11 ===")
cum_states = ["RU/SU", "US", "CN"]
cum = launches[(launches["category"] == "O") & (launches["state_combined"].isin(cum_states))] \
    .groupby(["launch_year", "state_combined"]).size().unstack(fill_value=0)
# Fill missing years
all_years = range(launches["launch_year"].min(), launches["launch_year"].max() + 1)
cum = cum.reindex(all_years, fill_value=0)
for s in cum_states:
    if s not in cum.columns:
        cum[s] = 0
cum = cum[cum_states].cumsum().reset_index().rename(columns={"index": "launch_year"})
print(cum.head(5).to_string(index=False))
print("...")
print(cum.tail(10).to_string(index=False))


# --- ana_12: Total launches per state-decade (matrix) ---
print("\n=== ana_12 ===")
mat = launches[launches["category"] == "O"].copy()
mat["decade"] = (mat["launch_year"] // 10) * 10
mat_grp = mat.groupby(["decade", "state_combined"]).size().unstack(fill_value=0)
keep = ["US", "RU/SU", "CN", "F", "J", "IN"]
keep = [c for c in keep if c in mat_grp.columns]
mat_grp = mat_grp[keep].reset_index()
print(mat_grp.to_string(index=False))


# --- ana_13: Vehicle-family longevity (top families by total flights) ---
print("\n=== ana_13 ===")
fam = launches.groupby("type").size().sort_values(ascending=False).head(10).reset_index()
fam.columns = ["family", "flights"]
print(fam.to_string(index=False))


# --- ana_14: Agency-type share over time, every 5 years ---
print("\n=== ana_14 ===")
launches["five_year"] = (launches["launch_year"] // 5) * 5
five = launches[launches["category"] == "O"].groupby(["five_year", "agency_type"]).size().unstack(fill_value=0)
cols = [c for c in ["state", "private", "startup"] if c in five.columns]
five = five[cols]
five_pct = five.div(five.sum(axis=1), axis=0) * 100
five_pct = five_pct.round(1).reset_index()
print(five_pct.to_string(index=False))
