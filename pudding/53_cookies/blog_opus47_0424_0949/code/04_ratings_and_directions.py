#!/usr/bin/env python3
"""
04_ratings_and_directions.py
Rating distribution, best/worst recipes, directions text corpus statistics
(oven temperature, bake time, sifting frequency, verb choice).
"""
import pandas as pd
import numpy as np
from pathlib import Path
import re
from collections import Counter

DATA_DIR = Path("/Users/forrest/Desktop/data2blog/data_pkg/pudding/53_cookies")
df = pd.read_csv(DATA_DIR / "choc_chip_cookie_ingredients.csv", encoding="latin-1")
if df.columns[0].startswith("Unnamed"):
    df = df.drop(columns=[df.columns[0]])
n_recipes = df["Recipe_Index"].nunique()

# Each recipe has one rating replicated across rows
recipe_rating = df.drop_duplicates("Recipe_Index")[["Recipe_Index", "Rating"]]
rated = recipe_rating.dropna(subset=["Rating"])

# --- ana_16: rating distribution ---
print("=== ana_16 ===")
print(f"recipes_with_rating: {len(rated)} / {n_recipes} ({round(len(rated)/n_recipes*100,1)}%)")
print(f"rating mean: {round(rated['Rating'].mean(),3)}")
print(f"rating median: {round(rated['Rating'].median(),3)}")
print(f"rating min: {round(rated['Rating'].min(),3)}")
print(f"rating max: {round(rated['Rating'].max(),3)}")
print(f"rating std: {round(rated['Rating'].std(),3)}")
# histogram (0–1 normalized)
bins = [0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.01]
labels = ["0-0.2","0.2-0.4","0.4-0.6","0.6-0.7","0.7-0.8","0.8-0.85","0.85-0.9","0.9-0.95","0.95-1.0"]
hist = pd.cut(rated["Rating"], bins=bins, labels=labels, right=True).value_counts().reindex(labels)
print("rating histogram:")
print(hist.to_string())

# Source-wise
print("\nrating by source:")
rated = rated.assign(source=rated["Recipe_Index"].str.split("_").str[0])
for src, sub in rated.groupby("source"):
    print(f"  {src}: n={len(sub)}, mean={round(sub['Rating'].mean(),3)}")

# --- ana_17: highest- and lowest-rated recipes ---
print("\n=== ana_17 ===")
sorted_r = rated.sort_values("Rating")
print("bottom 10 rated recipes:")
print(sorted_r.head(10)[["Recipe_Index","Rating"]].to_string(index=False))
print("\ntop 10 rated recipes (ties — showing rating=1.0 count):")
print(sorted_r.tail(10)[["Recipe_Index","Rating"]].to_string(index=False))
print(f"\nrecipes with perfect 1.0 rating: {(rated['Rating']==1.0).sum()}")

# Ingredients of the top-10 — what's in winning recipes?
top_ids = sorted_r.tail(10)["Recipe_Index"].tolist()
bot_ids = sorted_r.head(10)["Recipe_Index"].tolist()
top_ing = df[df["Recipe_Index"].isin(top_ids)]["Ingredient"].value_counts()
bot_ing = df[df["Recipe_Index"].isin(bot_ids)]["Ingredient"].value_counts()
print("\ningredients appearing in top-10 rated:")
print(top_ing.head(15).to_string())

# --- ana_18: rating vs ingredient count ---
print("\n=== ana_18 ===")
ipr = df.groupby("Recipe_Index")["Ingredient"].nunique().rename("n_ingredients")
joined = rated.set_index("Recipe_Index").join(ipr).dropna()
corr = joined[["Rating","n_ingredients"]].corr().iloc[0,1]
print(f"rating vs n_ingredients pearson: {round(corr,3)}")
# groups
buckets = pd.cut(joined["n_ingredients"], bins=[0,7,9,11,100], labels=["<=7","8-9","10-11","12+"])
tbl = joined.groupby(buckets, observed=True).agg(n=("Rating","count"), mean_rating=("Rating","mean"))
tbl["mean_rating"] = tbl["mean_rating"].round(3)
print("mean rating by ingredient-count bucket:")
print(tbl.to_string())

# --- ana_19: directions text — oven temperatures ---
print("\n=== ana_19 ===")
with open(DATA_DIR / "All_directions.txt", "r", encoding="latin-1") as f:
    text = f.read()
lines = [l for l in text.splitlines() if l.strip()]
# Oven temps (Fahrenheit)
temps = re.findall(r"(\d{3})\s*degrees?\s*F", text)
temp_cnt = Counter(int(t) for t in temps)
print("oven temperatures (Fahrenheit), top 10:")
for t, c in temp_cnt.most_common(10):
    print(f"  {t}F: {c}")
print("total_temp_mentions:", sum(temp_cnt.values()))

# Bake times: capture both single and range
bake_times = []
for m in re.finditer(r"(?:bake|baking|Bake)\b[^.]*?(\d{1,2})\s*(?:to|-|–)\s*(\d{1,2})\s*minutes?", text):
    bake_times.extend([int(m.group(1)), int(m.group(2))])
for m in re.finditer(r"(?:bake|baking|Bake)\b[^.]*?\bfor\s+(?:about\s+)?(\d{1,2})\s*minutes?", text):
    bake_times.append(int(m.group(1)))
if bake_times:
    arr = np.array(bake_times)
    print(f"\nbake_time mentions: n={len(arr)}, mean={round(arr.mean(),1)}, median={int(np.median(arr))}, min={int(arr.min())}, max={int(arr.max())}")
    # histogram of typical bake time span (rounded to bucket)
    bkt = Counter()
    for t in arr:
        if t < 8: bkt["<8 min"] += 1
        elif t <= 10: bkt["8-10 min"] += 1
        elif t <= 12: bkt["10-12 min"] += 1
        elif t <= 15: bkt["12-15 min"] += 1
        else: bkt[">15 min"] += 1
    print("bake time histogram:")
    for k in ["<8 min","8-10 min","10-12 min","12-15 min",">15 min"]:
        print(f"  {k}: {bkt.get(k,0)}")

# --- ana_20: verb usage in directions — what do bakers do? ---
print("\n=== ana_20 ===")
# Common cooking verbs — normalize to lower, count distinct recipes where verb appears.
verbs = ["preheat","cream","beat","stir","mix","combine","fold",
         "blend","sift","whisk","drop","roll","chill","refrigerate",
         "bake","cool","cut","scoop","grease","line"]
# Split into recipes — each recipe in All_directions may span multiple lines.
# Use paragraph boundary: each line is a recipe direction block (close enough for counts).
# Treat whole text as one corpus for frequency — that's what bakers say.
total_words = len(re.findall(r"\w+", text))
print(f"total directions tokens: {total_words}")
vcounts = []
for v in verbs:
    # count occurrences case-insensitively
    n = len(re.findall(rf"\b{v}\w*\b", text, flags=re.I))
    vcounts.append((v, n))
vcounts.sort(key=lambda x: -x[1])
print("verb frequency in directions corpus:")
for v, n in vcounts:
    print(f"  {v}: {n}")

# --- ana_21: "sift" or "chill" — dividing techniques ---
print("\n=== ana_21 ===")
# Approximate per-recipe by counting recipe-like paragraphs:
# Lines starting with "Preheat" are usually the first line of a new recipe
recipe_texts = []
cur = []
for l in lines:
    if re.match(r"^(Preheat|In a large|Heat the oven|Heat oven|Sift|Combine|Cream|Beat|Place|Line|Prepare)", l, flags=re.I) and cur:
        recipe_texts.append(" ".join(cur))
        cur = [l]
    else:
        cur.append(l)
if cur:
    recipe_texts.append(" ".join(cur))
# That's noisy; use a simpler proxy: total recipes that mention each word at least once
# We'll approximate: for each verb, count recipe-chunks that contain it.
n_chunks = len(recipe_texts)
print("n_recipe_chunks_estimate:", n_chunks)
for v in ["sift","chill","refrigerate","cream","whisk","fold","preheat","line"]:
    c = sum(1 for r in recipe_texts if re.search(rf"\b{v}\w*\b", r, flags=re.I))
    print(f"  chunks_mentioning_{v}: {c} ({round(c/n_chunks*100,1)}%)")

# --- ana_22: first-line openers (how recipes begin) ---
print("\n=== ana_22 ===")
openers = Counter()
for l in lines:
    # first word
    m = re.match(r"(\w+)", l)
    if m:
        openers[m.group(1).capitalize()] += 1
# A 'first line of a recipe' is any line whose previous line (if any) was empty — but we already filtered empties.
# Instead count line-starts directly.
print("top 20 first-word-of-line tokens in directions corpus:")
for w, c in openers.most_common(20):
    print(f"  {w}: {c}")

recipe_rating.to_csv("/tmp/rating_53cookies.csv", index=False)
