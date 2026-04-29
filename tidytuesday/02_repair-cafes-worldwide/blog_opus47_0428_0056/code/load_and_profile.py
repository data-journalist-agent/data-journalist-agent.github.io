"""Load and profile the Repair Cafes Worldwide TidyTuesday dataset.

Run from any directory; paths are absolute.
"""
import pandas as pd
import numpy as np

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/02_repair-cafes-worldwide"
repairs = pd.read_csv(f"{DATA_DIR}/repairs.csv", low_memory=False)
repairs_text = pd.read_csv(f"{DATA_DIR}/repairs_text.csv", low_memory=False)

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"repairs.csv rows: {len(repairs):,}")
print(f"repairs.csv cols: {len(repairs.columns)} -> {list(repairs.columns)}")
print(f"repairs_text.csv rows: {len(repairs_text):,}")
print(f"repairs_text.csv cols: {len(repairs_text.columns)} -> {list(repairs_text.columns)}")
print(f"Joined on repair_id (1:1 expected).")
repairs["repair_date"] = pd.to_datetime(repairs["repair_date"], errors="coerce")
print(f"Date range: {repairs['repair_date'].min().date()} to {repairs['repair_date'].max().date()}")
print(f"Unique repair_cafe_number: {repairs['repair_cafe_number'].nunique():,}")
print(f"Unique repair_cafe_name: {repairs['repair_cafe_name'].nunique():,}")
print(f"Unique countries: {repairs['country'].nunique()}")
print(f"Unique kind_of_product: {repairs['kind_of_product'].nunique():,}")
print(f"Unique category: {repairs['category'].nunique()}")
print(f"Unique brand: {repairs['brand'].nunique():,}")

# --- ana_02: Missingness per column ---
print("=== ana_02 ===")
def miss(df, name):
    rows = []
    for c in df.columns:
        n = df[c].isna().sum()
        rows.append((name, c, int(n), round(100 * n / len(df), 2)))
    return rows
all_miss = miss(repairs, "repairs") + miss(repairs_text, "repairs_text")
for r in all_miss:
    print(r)

# --- ana_03: Overall outcome distribution (repaired) ---
print("=== ana_03 ===")
out = repairs["repaired"].fillna("(missing)").value_counts(dropna=False)
total = len(repairs)
for k, v in out.items():
    print(f"{k}: {v:,} ({100*v/total:.2f}%)")
print(f"Total: {total:,}")
# Map for analysis
def std_outcome(x):
    if pd.isna(x): return "unknown"
    s = str(x).strip().lower()
    if s in {"yes", "fixed", "repaired"}: return "fixed"
    if s in {"no", "not repaired", "unrepaired"}: return "not_fixed"
    if "partial" in s or "half" in s or "end of life" in s: return "partial_or_eol"
    return s
repairs["_outcome"] = repairs["repaired"].apply(std_outcome)
print("Standardized:")
for k, v in repairs["_outcome"].value_counts().items():
    print(f"  {k}: {v:,} ({100*v/total:.2f}%)")
fix_rate = (repairs["_outcome"] == "fixed").sum() / ((repairs["_outcome"].isin(["fixed", "not_fixed", "partial_or_eol"])).sum())
print(f"Fix rate (fixed / fixed+not_fixed+partial): {100*fix_rate:.2f}%")

# Save standardized for downstream scripts
repairs.to_pickle("/tmp/repairs_clean.pkl")
repairs_text.to_pickle("/tmp/repairs_text_clean.pkl")
print("Saved /tmp/repairs_clean.pkl and /tmp/repairs_text_clean.pkl")
