"""Analyze the three callbacks — the moments that retrieve earlier material."""
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/57_stand-up")
cap = pd.read_csv(DATA_DIR / "ali-wong--captions.csv")
top = pd.read_csv(DATA_DIR / "ali-wong--topics.csv")


def to_sec(t: str) -> int:
    parts = t.split(":")
    h, m, s = (parts if len(parts) == 3 else ["0", parts[0], parts[1]])
    return int(h) * 3600 + int(m) * 60 + int(s)


cb = top[top["callback"].notna()].copy()
cb["callback_s"] = cb["callback"].apply(to_sec)
cb["gap_s"] = cb["timeStart"] - cb["callback_s"]

# --- ana_09: The three callbacks ---
print("=== ana_09 ===")
print("All callbacks in the special:")
for _, r in cb.iterrows():
    print(f"  group {r['group']}: triggered at {r['timeStart']}s "
          f"({r['timeStart']//60}:{r['timeStart']%60:02d}), "
          f"references {r['callback']} (= {r['callback_s']}s) — "
          f"gap of {r['gap_s']}s ({r['gap_s']/60:.1f} min)")

# --- ana_10: Laugh intensity in 30s after each callback vs random baseline ---
print("=== ana_10 ===")


def window_laugh(t0: int, length: int = 30) -> float:
    return float(cap[(cap["timeStart"] >= t0) &
                     (cap["timeStart"] < t0 + length)]["laugh"].sum())


cb_times = cb["timeStart"].tolist()
cb_laughs = [window_laugh(t) for t in cb_times]
print(f"Callback window 30s laugh totals: {cb_laughs}")
print(f"Mean callback-window laughter: {np.mean(cb_laughs):.2f}s")

np.random.seed(42)
runtime = int(cap["timeStop"].max())
baseline_starts = np.random.randint(0, runtime - 30, 1000)
baseline_laughs = [window_laugh(int(t)) for t in baseline_starts]
print(f"Baseline (1000 random 30s windows) mean: {np.mean(baseline_laughs):.2f}s")
print(f"Baseline median: {np.median(baseline_laughs):.2f}s")
print(f"Callback windows beat the baseline by "
      f"{np.mean(cb_laughs) / np.mean(baseline_laughs):.2f}x")

# --- ana_11: Content of the callback bits (what they refer back to) ---
print("=== ana_11 ===")
for _, r in cb.iterrows():
    print(f"--- Callback '{r['group']}' at t={r['timeStart']}s ---")
    print(f"  Returns to an earlier moment at t={r['callback_s']}s:")
    src = cap[(cap["timeStart"] >= r["callback_s"] - 2) &
              (cap["timeStart"] <= r["callback_s"] + 5)][["timeStart", "caption", "group"]]
    for _, s in src.iterrows():
        print(f"    [{s['timeStart']}s | {s['group']}] {s['caption'].strip()}")
    print(f"  The callback bit itself:")
    dst = cap[(cap["timeStart"] >= r["timeStart"]) &
              (cap["timeStart"] < r["totalStop"])][["timeStart", "caption", "laugh"]]
    for _, s in dst.iterrows():
        print(f"    [{s['timeStart']}s | laugh={s['laugh']}] {s['caption'].strip()}")
