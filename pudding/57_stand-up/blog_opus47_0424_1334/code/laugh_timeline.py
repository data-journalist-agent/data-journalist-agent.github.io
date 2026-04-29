"""Per-minute laughter timeline — find the laughter climax."""
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/57_stand-up")
cap = pd.read_csv(DATA_DIR / "ali-wong--captions.csv")

# Per-minute bins
cap["minute"] = cap["timeStart"] // 60
by_min = cap.groupby("minute")["laugh"].sum().reset_index()
by_min.columns = ["minute", "laugh_s"]

# --- ana_07: Laughter timeline (per minute) ---
print("=== ana_07 ===")
print("Laugh seconds per minute across the 59-minute special:")
for _, r in by_min.iterrows():
    bar = "#" * int(r["laugh_s"])
    print(f"  min {int(r['minute']):2d}: {r['laugh_s']:5.2f}s {bar}")

# --- ana_08: Peak 60s rolling window (laughter climax) ---
print("=== ana_08 ===")
runtime = int(cap["timeStop"].max()) + 1
laugh_per_sec = np.zeros(runtime)
for _, r in cap.iterrows():
    laugh_per_sec[int(r["timeStart"])] += r["laugh"]
rolling = np.convolve(laugh_per_sec, np.ones(60), mode="same")
top_idx = np.argsort(rolling)[::-1]
seen = set()
top_windows = []
for idx in top_idx:
    # Cluster peaks within 30s of an already-seen one
    if any(abs(idx - s) < 30 for s in seen):
        continue
    seen.add(int(idx))
    top_windows.append((int(idx), float(rolling[idx])))
    if len(top_windows) >= 5:
        break

print(f"Top 5 laughter peaks (60s rolling window):")
for t, val in top_windows:
    print(f"  t={t}s ({t//60}:{t%60:02d}) - {val:.1f}s laughter in 60s window")
print(f"Overall peak: t={top_windows[0][0]}s "
      f"({top_windows[0][0]//60}:{top_windows[0][0]%60:02d}) with "
      f"{top_windows[0][1]:.1f}s of laughter in a single minute")
