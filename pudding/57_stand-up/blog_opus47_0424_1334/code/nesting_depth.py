"""Measure how deeply the routine nests topics — the screenplay-like hierarchy."""
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/57_stand-up")
top = pd.read_csv(DATA_DIR / "ali-wong--topics.csv")

# --- ana_05: Distribution of nesting depth ---
print("=== ana_05 ===")
depth = top["level"].value_counts().sort_index()
for lvl, n in depth.items():
    print(f"  level {lvl}: {n} topic segments")
print(f"  total segments: {len(top)}")
print(f"  max depth reached: {top['level'].max()}")

# --- ana_06: Average bit duration by depth ---
print("=== ana_06 ===")
# Duration = topicEnd - timeStart for each row
top["dur_s"] = top["topicEnd"] - top["timeStart"]
dur = top.groupby("level")["dur_s"].agg(["mean", "median", "min", "max", "count"])
print(dur.to_string())
