"""Category, country, brand, year-of-production, repairability analyses."""
import pandas as pd
import numpy as np

repairs = pd.read_pickle("/tmp/repairs_clean.pkl")
total = len(repairs)

# --- ana_04: Category distribution and fix rate per category ---
print("=== ana_04 ===")
cat_grp = repairs.groupby("category")["_outcome"].value_counts().unstack(fill_value=0)
cat_grp["total"] = cat_grp.sum(axis=1)
cat_grp["fix_rate"] = 100 * cat_grp.get("fixed", 0) / cat_grp["total"]
cat_grp = cat_grp.sort_values("total", ascending=False)
print(cat_grp[["total", "fixed", "not_fixed", "partial_or_eol", "fix_rate"]].round(2))

# --- ana_05: Top kinds of products and their fix rate ---
print("=== ana_05 ===")
prod_grp = repairs.groupby("kind_of_product")["_outcome"].value_counts().unstack(fill_value=0)
prod_grp["total"] = prod_grp.sum(axis=1)
prod_grp["fix_rate"] = 100 * prod_grp.get("fixed", 0) / prod_grp["total"]
prod_grp = prod_grp[prod_grp["total"] >= 200].sort_values("total", ascending=False)
print(f"Products with >=200 visits: {len(prod_grp)}")
print(prod_grp.head(25)[["total", "fix_rate"]].round(2))

# --- ana_06: Easiest and hardest products to fix (with sample-size filter) ---
print("=== ana_06 ===")
big = prod_grp[prod_grp["total"] >= 500].copy()
print(f"Products with >=500 visits: {len(big)}")
top_easy = big.sort_values("fix_rate", ascending=False).head(10)[["total", "fix_rate"]]
top_hard = big.sort_values("fix_rate", ascending=True).head(10)[["total", "fix_rate"]]
print("Easiest (highest fix_rate):")
print(top_easy.round(2))
print("Hardest (lowest fix_rate):")
print(top_hard.round(2))

# --- ana_07: Country distribution and fix rate ---
print("=== ana_07 ===")
ctry_grp = repairs.groupby("country")["_outcome"].value_counts().unstack(fill_value=0)
ctry_grp["total"] = ctry_grp.sum(axis=1)
ctry_grp["fix_rate"] = 100 * ctry_grp.get("fixed", 0) / ctry_grp["total"]
ctry_grp = ctry_grp.sort_values("total", ascending=False)
print(ctry_grp[["total", "fix_rate"]].round(2))
print(f"Top country share of all repairs: {100*ctry_grp.iloc[0]['total']/total:.2f}%")
print(f"Top 3 country share: {100*ctry_grp.head(3)['total'].sum()/total:.2f}%")

# --- ana_08: Year-over-year repair counts (growth) ---
print("=== ana_08 ===")
repairs["year"] = repairs["repair_date"].dt.year
yr = repairs.groupby("year").size()
print(yr)
# also fix rate by year
yr_fr = repairs.groupby("year")["_outcome"].apply(lambda s: 100 * (s == "fixed").sum() / len(s))
print("Fix rate by year:")
print(yr_fr.round(2))

# --- ana_09: Country growth — leading country branches active per year ---
print("=== ana_09 ===")
# Branches active by country/year (unique repair_cafe_number)
ca_yr = repairs.groupby(["country", "year"])["repair_cafe_number"].nunique().unstack(fill_value=0)
ca_yr["change_2018_to_2024"] = ca_yr.get(2024, 0) - ca_yr.get(2018, 0)
ca_yr_sorted = ca_yr.sort_values("change_2018_to_2024", ascending=False)
print("Top countries by 2018->2024 branch growth:")
cols = [c for c in ca_yr.columns if isinstance(c, (int, np.integer))]
print(ca_yr_sorted[cols + ["change_2018_to_2024"]].head(8))

# --- ana_10: Estimated year of production distribution ---
print("=== ana_10 ===")
yp = pd.to_numeric(repairs["estimated_year_of_production"], errors="coerce")
yp = yp[(yp >= 1900) & (yp <= 2026)]
print(f"Non-missing year_of_production: {yp.notna().sum():,} ({100*yp.notna().sum()/total:.2f}%)")
print(f"Median yr of production: {int(yp.median())}")
print(f"Mean: {yp.mean():.1f}")
# Distribution by decade
decade = (yp // 10 * 10).astype(int)
dec = decade.value_counts().sort_index()
print("By decade:")
print(dec)
# Age at repair
repairs["_year_of_prod"] = yp
repairs["_age_at_repair"] = repairs["year"] - repairs["_year_of_prod"]
ages = repairs["_age_at_repair"].dropna()
ages = ages[(ages >= 0) & (ages <= 100)]
print(f"Median age at repair: {int(ages.median())} years")
print(f"Mean age: {ages.mean():.1f} years")
# Bucketed
bins = [0, 5, 10, 15, 20, 25, 30, 50, 100]
labels = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-49", "50+"]
ages_b = pd.cut(ages, bins=bins, labels=labels, right=False, include_lowest=True)
print("Age distribution at repair:")
print(ages_b.value_counts().reindex(labels))

# Fix rate by age bucket
age_df = repairs[(repairs["_age_at_repair"] >= 0) & (repairs["_age_at_repair"] <= 100)].copy()
age_df["age_b"] = pd.cut(age_df["_age_at_repair"], bins=bins, labels=labels, right=False, include_lowest=True)
print("Fix rate by age bucket:")
print(age_df.groupby("age_b", observed=True)["_outcome"].apply(lambda s: 100*(s=="fixed").sum()/len(s)).round(2))

# --- ana_11: Repairability score distribution and outcome correlation ---
print("=== ana_11 ===")
rep = pd.to_numeric(repairs["repairability"], errors="coerce")
print(f"Non-missing repairability: {rep.notna().sum():,} ({100*rep.notna().sum()/total:.2f}%)")
print(f"Mean: {rep.mean():.2f}, Median: {rep.median()}")
print("Score distribution (1-10):")
sd = rep.value_counts().sort_index()
print(sd)
# By outcome
repairs["_repairability"] = rep
print("Mean score by outcome:")
print(repairs.groupby("_outcome")["_repairability"].mean().round(2))
# Fix rate by score bucket
score_df = repairs[repairs["_repairability"].notna()].copy()
score_df["score_int"] = score_df["_repairability"].astype(int)
print("Fix rate by score:")
fr_by_score = score_df.groupby("score_int")["_outcome"].apply(lambda s: 100*(s=="fixed").sum()/len(s)).round(2)
print(fr_by_score)

# --- ana_12: Top brands by volume and fix rate ---
print("=== ana_12 ===")
br_grp = repairs.groupby("brand")["_outcome"].value_counts().unstack(fill_value=0)
br_grp["total"] = br_grp.sum(axis=1)
br_grp["fix_rate"] = 100 * br_grp.get("fixed", 0) / br_grp["total"]
big_br = br_grp[br_grp["total"] >= 300].sort_values("total", ascending=False)
print(f"Brands with >=300 visits: {len(big_br)}")
print(big_br.head(20)[["total", "fix_rate"]].round(2))
print("Best fix rates among >=300 visits:")
print(big_br.sort_values("fix_rate", ascending=False).head(10)[["total", "fix_rate"]].round(2))
print("Worst fix rates among >=300 visits:")
print(big_br.sort_values("fix_rate", ascending=True).head(10)[["total", "fix_rate"]].round(2))

# Save aug
repairs.to_pickle("/tmp/repairs_aug.pkl")
print("Saved /tmp/repairs_aug.pkl")
