"""
Reproduce the central Economist chart: mobility change by regime type, mobility category, and month.
Source table is already pre-aggregated.
"""
import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_pkg/economist/07_democracies-contain-epidemics-most-effectively"
df = pd.read_csv(f"{DATA_DIR}/mobility_change_by_type_regime_and_time.v1.2.csv")

# Strip useless first column
df = df.drop(columns=[c for c in df.columns if c == "" or c.startswith("Unnamed")])

cat_short = {
    "workplaces_percent_change_from_baseline": "Workplaces",
    "retail_and_recreation_percent_change_from_baseline": "Retail & rec.",
    "grocery_and_pharmacy_percent_change_from_baseline": "Grocery & pharmacy",
    "parks_percent_change_from_baseline": "Parks",
    "transit_stations_percent_change_from_baseline": "Transit stations",
}
df["category_short"] = df["category"].map(cat_short)

# --- ana_01: April mobility gap, by category ---
print("=== ana_01 ===")
apr = df[df["month"] == "April"].copy()
piv = apr.pivot_table(index="category_short", columns="type", values="mean").round(1)
piv["gap_pp"] = (piv["Democracies"] - piv["Non-Democracies"]).round(1)
piv = piv.sort_values("gap_pp")
print(piv)

# --- ana_02: monthly trajectory, all categories pooled ---
print("=== ana_02 ===")
month_order = ["March", "April", "May"]
pooled = (
    df.groupby(["month", "type"])["mean"].mean().round(1).unstack()
    .reindex(month_order)
)
pooled["gap_pp"] = (pooled["Democracies"] - pooled["Non-Democracies"]).round(1)
print(pooled)

# --- ana_03: full per-month per-category table for chart ---
print("=== ana_03 ===")
full = df[["month", "category_short", "type", "mean", "top_90", "bot_90"]].copy()
full["mean"] = full["mean"].round(1)
full = full.sort_values(["month", "category_short", "type"])
print(full.to_string(index=False))

# --- ana_04: peak gap (April, Retail & rec.) ---
print("=== ana_04 ===")
peak = df[(df["month"] == "April") & (df["category_short"] == "Retail & rec.")]
peak_piv = peak.pivot_table(index="category_short", columns="type", values="mean")
print(peak_piv)
gap = float(peak_piv["Democracies"].iloc[0] - peak_piv["Non-Democracies"].iloc[0])
print(f"Gap (Dem - Non): {gap:.1f} pp")

# --- ana_05: convergence in May ---
print("=== ana_05 ===")
may = df[df["month"] == "May"].copy()
may_piv = may.pivot_table(index="category_short", columns="type", values="mean").round(1)
may_piv["gap_pp"] = (may_piv["Democracies"] - may_piv["Non-Democracies"]).round(1)
print(may_piv)

# --- ana_06: dispersion (top_90 - bot_90 within group) ---
print("=== ana_06 ===")
df["spread_90"] = df["top_90"] - df["bot_90"]
disp = df.groupby("type")["spread_90"].mean().round(1)
print(disp)
