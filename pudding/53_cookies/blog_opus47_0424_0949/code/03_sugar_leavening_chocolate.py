#!/usr/bin/env python3
"""
03_sugar_leavening_chocolate.py
Brown vs white sugar politics, leavening choices, chocolate-type diversity.
"""
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("/Users/forrest/Desktop/data2blog/data_pkg/pudding/53_cookies")
df = pd.read_csv(DATA_DIR / "choc_chip_cookie_ingredients.csv", encoding="latin-1")
if df.columns[0].startswith("Unnamed"):
    df = df.drop(columns=[df.columns[0]])
agg = df.groupby(["Recipe_Index", "Ingredient", "Unit"], as_index=False)["Quantity"].sum()
n_recipes = df["Recipe_Index"].nunique()

# --- ana_10: brown vs white sugar — how recipes mix them ---
print("=== ana_10 ===")
pivot = agg.pivot_table(index="Recipe_Index", columns="Ingredient", values="Quantity", aggfunc="sum")
# combined brown = light brown + dark brown
pivot["brown"] = pivot.get("light brown sugar", 0).fillna(0) + pivot.get("dark brown sugar", 0).fillna(0)
pivot["white"] = pivot.get("sugar", 0).fillna(0)
def classify(r):
    b, w = r["brown"], r["white"]
    if b == 0 and w == 0:
        return "no_sugar_labeled"
    if b > 0 and w == 0:
        return "brown_only"
    if w > 0 and b == 0:
        return "white_only"
    return "both"
pivot["sugar_type"] = pivot.apply(classify, axis=1)
counts = pivot["sugar_type"].value_counts()
print("sugar type usage across", n_recipes, "recipes:")
for k, v in counts.items():
    print(f"  {k}: {v} ({round(v/n_recipes*100,1)}%)")

# for recipes that use both: distribution of brown share
both = pivot[pivot["sugar_type"] == "both"].copy()
both["brown_share"] = both["brown"] / (both["brown"] + both["white"])
print("brown_share distribution (recipes using BOTH):")
print("n:", len(both), "mean:", round(both["brown_share"].mean(), 3),
      "median:", round(both["brown_share"].median(), 3))
# histogram
bins = [0, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0]
labels = ["0-25%","25-40%","40-50%","50-60%","60-75%","75-100%"]
hist = pd.cut(both["brown_share"], bins=bins, labels=labels, right=True).value_counts().reindex(labels)
print(hist.to_string())

# --- ana_11: baking soda vs baking powder choices ---
print("\n=== ana_11 ===")
pivot["has_soda"]   = pivot.get("baking soda", 0).fillna(0) > 0
pivot["has_powder"] = pivot.get("baking powder", 0).fillna(0) > 0
def leav(r):
    s, p = r["has_soda"], r["has_powder"]
    if s and p:   return "both"
    if s:         return "soda_only"
    if p:         return "powder_only"
    return "neither"
pivot["leavening"] = pivot.apply(leav, axis=1)
lev = pivot["leavening"].value_counts()
print("leavening choice across", n_recipes, "recipes:")
for k, v in lev.items():
    print(f"  {k}: {v} ({round(v/n_recipes*100,1)}%)")

# --- ana_12: chocolate chip type diversity (semisweet, milk, dark, bitter, white) ---
print("\n=== ana_12 ===")
chip_cols = ["semisweet chocolate chip", "milk chocolate chip",
             "dark chocolate chip", "bittersweet chocolate chip",
             "white chocolate chip", "chocolate raisin", "peanut butter chips"]
have = {c: (pivot.get(c, pd.Series(0, index=pivot.index)).fillna(0) > 0) for c in chip_cols}
chip_df = pd.DataFrame(have, index=pivot.index)
chip_df["n_chip_types"] = chip_df.sum(axis=1)
n_chip_counts = chip_df["n_chip_types"].value_counts().sort_index()
print("number of distinct chip types per recipe:")
for k, v in n_chip_counts.items():
    print(f"  {k} type(s): {v} recipes ({round(v/n_recipes*100,1)}%)")
# How many recipes use ONLY semisweet among those using any chip type?
using_chips = chip_df[chip_df["n_chip_types"] > 0]
only_semi = chip_df[(chip_df["n_chip_types"] == 1) & (chip_df["semisweet chocolate chip"])]
print(f"\nrecipes using any chip: {len(using_chips)}")
print(f"recipes using ONLY semisweet: {len(only_semi)}"
      f" ({round(len(only_semi)/len(using_chips)*100,1)}% of chip-users)")
# Counts per type
print("\nby chip type:")
for c in chip_cols:
    n = chip_df[c].sum()
    print(f"  {c}: {n} recipes ({round(n/n_recipes*100,1)}%)")

# --- ana_13: nuts usage ---
print("\n=== ana_13 ===")
nut_cols = ["walnut", "pecan", "almonds", "macadmia", "nuts"]
nuts = pd.DataFrame({c: (pivot.get(c, pd.Series(0, index=pivot.index)).fillna(0) > 0) for c in nut_cols})
nuts["any_nut"] = nuts.any(axis=1)
print(f"recipes with ANY nuts: {nuts['any_nut'].sum()} ({round(nuts['any_nut'].mean()*100,1)}%)")
for c in nut_cols:
    n = nuts[c].sum()
    print(f"  {c}: {n} ({round(n/n_recipes*100,1)}%)")

# --- ana_14: fats beyond butter — shortening, margarine, oil ---
print("\n=== ana_14 ===")
fat_cols = ["butter", "shortening", "margarine", "vegetable oil"]
fats = pd.DataFrame({c: (pivot.get(c, pd.Series(0, index=pivot.index)).fillna(0) > 0) for c in fat_cols})
for c in fat_cols:
    n = fats[c].sum()
    print(f"  {c}: {n} ({round(n/n_recipes*100,1)}%)")
# both butter and shortening
both_fat = fats[fats["butter"] & fats["shortening"]]
print(f"butter + shortening combo: {len(both_fat)} ({round(len(both_fat)/n_recipes*100,1)}%)")
# no butter at all
no_butter = fats[~fats["butter"]]
print(f"zero butter: {len(no_butter)} ({round(len(no_butter)/n_recipes*100,1)}%)")

# --- ana_15: flour diversity — AP, bread, cake, wheat ---
print("\n=== ana_15 ===")
flour_cols = ["all purpose flour", "bread flour", "cake flour", "wheat flour", "flour", "brown rice flour"]
fls = pd.DataFrame({c: (pivot.get(c, pd.Series(0, index=pivot.index)).fillna(0) > 0) for c in flour_cols})
for c in flour_cols:
    n = fls[c].sum()
    print(f"  {c}: {n} ({round(n/n_recipes*100,1)}%)")
# blended flour (> 1 flour type)
fls["n_flour_types"] = fls.sum(axis=1)
multi = fls[fls["n_flour_types"] > 1]
print(f"blended-flour recipes (>=2 flour types): {len(multi)} ({round(len(multi)/n_recipes*100,1)}%)")

pivot.to_csv("/tmp/pivot_53cookies.csv")
