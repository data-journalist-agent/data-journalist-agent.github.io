#!/usr/bin/env python3
"""
01_profile_and_frequency.py
Dataset profile, field inventory, ingredient-frequency analysis.
Reads:  data_pkg/pudding/53_cookies/choc_chip_cookie_ingredients.csv
Prints: machine-readable tagged blocks (=== ana_XX ===) for downstream parsing.
"""
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("/Users/forrest/Desktop/data2blog/data_pkg/pudding/53_cookies")
CSV = DATA_DIR / "choc_chip_cookie_ingredients.csv"
DIR_TXT = DATA_DIR / "All_directions.txt"

df = pd.read_csv(CSV, encoding="latin-1")
# Drop the unnamed index column
if df.columns[0].startswith("Unnamed"):
    df = df.drop(columns=[df.columns[0]])

# --- ana_profile: dataset profile ---
print("=== ana_profile ===")
print("rows:", len(df))
print("cols:", list(df.columns))
print("unique_recipes:", df["Recipe_Index"].nunique())
print("unique_ingredients:", df["Ingredient"].nunique())
print("units:", sorted(df["Unit"].astype(str).unique()))
src = df["Recipe_Index"].str.split("_").str[0].value_counts()
print("rows_by_source_prefix:\n", src.to_string())
# Number of recipes per source
recipe_src = df.drop_duplicates("Recipe_Index")["Recipe_Index"].str.split("_").str[0].value_counts()
print("recipes_by_source:\n", recipe_src.to_string())
print("missing_rating_rows:", df["Rating"].isna().sum())
print("recipes_with_any_rating:", df[df["Rating"].notna()]["Recipe_Index"].nunique())
with open(DIR_TXT, "r", encoding="latin-1") as f:
    dir_lines = [l for l in f.read().splitlines() if l.strip()]
print("direction_non_empty_lines:", len(dir_lines))

# --- ana_01: ingredient frequency across 211 recipes ---
# Count in how many DISTINCT recipes each ingredient appears
print("\n=== ana_01 ===")
recipe_ing = df.drop_duplicates(["Recipe_Index", "Ingredient"])
n_recipes = df["Recipe_Index"].nunique()
freq = recipe_ing.groupby("Ingredient")["Recipe_Index"].nunique().sort_values(ascending=False)
freq_pct = (freq / n_recipes * 100).round(1)
freq_tbl = pd.DataFrame({"ingredient": freq.index, "n_recipes": freq.values,
                          "pct_of_recipes": freq_pct.values})
print(freq_tbl.to_string(index=False))

# --- ana_02: the canonical eight — ingredients in 75%+ of recipes ---
print("\n=== ana_02 ===")
canon = freq_tbl[freq_tbl["pct_of_recipes"] >= 75].copy()
print("canonical threshold = 75% of recipes")
print(canon.to_string(index=False))
print("num_canonical_ingredients:", len(canon))

# --- ana_03: the long tail — ingredients in < 5% of recipes ---
print("\n=== ana_03 ===")
tail = freq_tbl[freq_tbl["pct_of_recipes"] < 5].copy()
print("num_tail_ingredients:", len(tail))
print("tail_total_unique:", len(tail), "out of", len(freq_tbl))
print(tail.to_string(index=False))

# --- ana_04: ingredients-per-recipe distribution ---
print("\n=== ana_04 ===")
ipr = df.groupby("Recipe_Index")["Ingredient"].nunique()
print("min_ingredients:", int(ipr.min()))
print("max_ingredients:", int(ipr.max()))
print("mean_ingredients:", round(ipr.mean(), 2))
print("median_ingredients:", float(ipr.median()))
print("std_ingredients:", round(ipr.std(), 2))
# histogram: 1-5, 6, 7, 8, 9, 10, 11, 12, 13+
bins = [0, 5, 6, 7, 8, 9, 10, 11, 12, 100]
labels = ["<=5", "6", "7", "8", "9", "10", "11", "12", "13+"]
hist = pd.cut(ipr, bins=bins, labels=labels, right=True).value_counts().reindex(labels)
print("histogram (ingredients per recipe):")
print(hist.to_string())

# save ingredients-per-recipe series to a temp file for other scripts if needed
ipr.to_csv("/tmp/ipr_53cookies.csv", header=True)
freq_tbl.to_csv("/tmp/freq_53cookies.csv", index=False)
recipe_ing.to_csv("/tmp/recipe_ing_53cookies.csv", index=False)
df.to_csv("/tmp/df_53cookies.csv", index=False)
print("\nDONE")
