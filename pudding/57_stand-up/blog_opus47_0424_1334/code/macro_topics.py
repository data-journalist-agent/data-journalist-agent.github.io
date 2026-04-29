"""Analyze the six top-level (level=1) macro topics — duration and laugh intensity."""
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/57_stand-up")
cap = pd.read_csv(DATA_DIR / "ali-wong--captions.csv")
top = pd.read_csv(DATA_DIR / "ali-wong--topics.csv")

# Level-1 topics: take min timeStart and max topicEnd per unique group
lvl1 = (
    top[top["level"] == 1]
    .groupby("group")
    .agg(start=("timeStart", "min"), end=("topicEnd", "max"))
    .reset_index()
    .sort_values("start")
)
lvl1["duration_s"] = lvl1["end"] - lvl1["start"]


def macro_for(t: int) -> str:
    """Return the level-1 macro topic that contains timestamp t (seconds)."""
    for _, r in lvl1.iterrows():
        if r["start"] <= t < r["end"]:
            return r["group"]
    return "outside"


cap["macro"] = cap["timeStart"].apply(macro_for)

agg = cap.groupby("macro").agg(laugh_s=("laugh", "sum"),
                                n_lines=("laugh", "size")).reset_index()
agg = agg.merge(lvl1[["group", "duration_s"]].rename(columns={"group": "macro"}),
                on="macro", how="left")
agg["laugh_pct"] = 100 * agg["laugh_s"] / agg["duration_s"]
agg["laugh_per_min"] = agg["laugh_s"] / (agg["duration_s"] / 60)
agg = agg.sort_values("laugh_per_min", ascending=False)

# --- ana_03: Macro-topic runtime breakdown ---
print("=== ana_03 ===")
print("Level-1 topic durations (sorted by start):")
for _, r in lvl1.iterrows():
    print(f"  {r['group']}: {r['start']}s - {r['end']}s "
          f"= {r['duration_s']}s ({r['duration_s']/60:.2f} min)")
print(f"  total spanned: {lvl1['duration_s'].sum()}s")

# --- ana_04: Laugh intensity per macro topic ---
print("=== ana_04 ===")
print(agg[["macro", "duration_s", "n_lines", "laugh_s",
          "laugh_pct", "laugh_per_min"]].to_string(index=False))
