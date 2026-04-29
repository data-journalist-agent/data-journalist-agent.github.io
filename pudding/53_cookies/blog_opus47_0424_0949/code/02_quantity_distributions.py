#!/usr/bin/env python3
"""
02_quantity_distributions.py
Distribution stats (mean, median, IQR, min, max, std) for core ingredients.
All quantities are per-48-cookie recipe.
"""
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("/Users/forrest/Desktop/data2blog/data_pkg/pudding/53_cookies")
df = pd.read_csv(DATA_DIR / "choc_chip_cookie_ingredients.csv", encoding="latin-1")
if df.columns[0].startswith("Unnamed"):
    df = df.drop(columns=[df.columns[0]])

# For each recipe × ingredient, sum quantities (defensive — handles duplicate rows).
agg = df.groupby(["Recipe_Index", "Ingredient", "Unit"], as_index=False)["Quantity"].sum()

CORE = ["all purpose flour", "butter", "sugar", "light brown sugar",
        "egg", "vanilla", "baking soda", "salt", "semisweet chocolate chip"]

def stats(series):
    return {
        "n": int(series.count()),
        "mean": round(float(series.mean()), 3),
        "median": round(float(series.median()), 3),
        "p25": round(float(series.quantile(0.25)), 3),
        "p75": round(float(series.quantile(0.75)), 3),
        "min": round(float(series.min()), 3),
        "max": round(float(series.max()), 3),
        "std": round(float(series.std()), 3),
    }

# --- ana_05: distribution of core ingredient quantities ---
print("=== ana_05 ===")
rows = []
for ing in CORE:
    sub = agg[agg["Ingredient"] == ing]
    if sub.empty:
        continue
    unit = sub["Unit"].mode().iat[0]
    s = stats(sub["Quantity"])
    rows.append([ing, unit, s["n"], s["mean"], s["median"], s["p25"], s["p75"], s["min"], s["max"], s["std"]])
stat_tbl = pd.DataFrame(rows, columns=["ingredient","unit","n","mean","median","p25","p75","min","max","std"])
print(stat_tbl.to_string(index=False))

# --- ana_06: the arithmetic-mean 48-cookie recipe (top canon) ---
print("\n=== ana_06 ===")
print("Average recipe (ingredients present in >=50% of recipes only):")
freq = agg.groupby("Ingredient")["Recipe_Index"].nunique()
n_recipes = df["Recipe_Index"].nunique()
common = freq[freq / n_recipes >= 0.5].index
avg_rows = []
for ing in common:
    sub = agg[agg["Ingredient"] == ing]
    unit = sub["Unit"].mode().iat[0]
    avg_rows.append([ing, unit, round(float(sub["Quantity"].mean()), 3), int(sub.shape[0])])
avg_df = pd.DataFrame(avg_rows, columns=["ingredient","unit","mean_qty","n_recipes"]).sort_values("n_recipes", ascending=False)
print(avg_df.to_string(index=False))

# --- ana_07: 48-cookie ratios vs Wakefield original (scaled from 60-cookie recipe) ---
# Wakefield original is 2-1/4 cups flour; 1 cup butter; 3/4 cup granulated; 3/4 cup brown;
# 2 eggs; 1 tsp soda; 1 tsp salt; 1 tsp vanilla; 2 cups chips — yields ~60 cookies.
# Scale to 48 cookies: factor = 48/60 = 0.8
print("\n=== ana_07 ===")
scale = 48 / 60
wake = {
    "all purpose flour": 2.25 * scale,   # cup
    "butter":             1.0  * scale,   # cup
    "sugar":              0.75 * scale,   # cup (granulated)
    "light brown sugar":  0.75 * scale,   # cup
    "egg":                2.0  * scale,   # eggs
    "baking soda":        1.0  * scale,   # teaspoon
    "salt":               1.0  * scale,   # teaspoon
    "vanilla":            1.0  * scale,   # teaspoon
    "semisweet chocolate chip": 2.0 * scale  # cup
}
print("Wakefield 1938 original (scaled to 48 cookies) vs modern mean (48 cookies):")
print("ingredient,unit,wakefield_48,modern_mean_48,modern_median_48,delta_pct_mean_vs_wake")
for ing, wake_val in wake.items():
    sub = agg[agg["Ingredient"] == ing]
    if sub.empty:
        continue
    unit = sub["Unit"].mode().iat[0]
    m_mean = float(sub["Quantity"].mean())
    m_med  = float(sub["Quantity"].median())
    delta = round((m_mean - wake_val) / wake_val * 100, 1)
    print(f"{ing},{unit},{round(wake_val,3)},{round(m_mean,3)},{round(m_med,3)},{delta}")

# --- ana_08: outlier recipes — biggest and smallest flour amounts ---
print("\n=== ana_08 ===")
flour = agg[agg["Ingredient"] == "all purpose flour"].copy().sort_values("Quantity")
print("10 smallest flour (cups):")
print(flour[["Recipe_Index","Quantity","Unit"]].head(10).to_string(index=False))
print("\n10 largest flour (cups):")
print(flour[["Recipe_Index","Quantity","Unit"]].tail(10).to_string(index=False))
print(f"\n2-SD outliers (|z|>2):")
z = (flour["Quantity"] - flour["Quantity"].mean()) / flour["Quantity"].std()
outliers = flour[z.abs() > 2]
print(outliers[["Recipe_Index","Quantity"]].to_string(index=False))

# --- ana_09: butter-to-flour ratio distribution ---
print("\n=== ana_09 ===")
butter = agg[agg["Ingredient"] == "butter"].groupby("Recipe_Index")["Quantity"].sum()
flour_q = agg[agg["Ingredient"] == "all purpose flour"].groupby("Recipe_Index")["Quantity"].sum()
ratio = (butter / flour_q).dropna()
print("butter/flour ratio (cups/cups):")
print("n:", len(ratio), "mean:", round(ratio.mean(),3),
      "median:", round(ratio.median(),3), "p25:", round(ratio.quantile(0.25),3),
      "p75:", round(ratio.quantile(0.75),3))
# histogram
bins = [0, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0, 2.0]
labels = ["0-0.25","0.25-0.4","0.4-0.5","0.5-0.6","0.6-0.75","0.75-1.0",">1.0"]
hist = pd.cut(ratio, bins=bins, labels=labels, right=True).value_counts().reindex(labels)
print("ratio histogram:")
print(hist.to_string())

agg.to_csv("/tmp/agg_53cookies.csv", index=False)
