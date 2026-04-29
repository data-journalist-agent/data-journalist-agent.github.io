"""Load Ali Wong Baby Cobra dataset and compute dataset profile findings."""
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/57_stand-up")
cap = pd.read_csv(DATA_DIR / "ali-wong--captions.csv")
top = pd.read_csv(DATA_DIR / "ali-wong--topics.csv")

runtime_s = int(cap["timeStop"].max())
total_laugh_s = float(cap["laugh"].sum())
laugh_lines = int((cap["laugh"] > 0).sum())
max_laugh = float(cap["laugh"].max())
max_laugh_time = int(cap.loc[cap["laugh"].idxmax(), "timeStart"])
max_laugh_caption = cap.loc[cap["laugh"].idxmax(), "caption"].strip()

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"captions rows: {len(cap)} / columns: {len(cap.columns)}")
print(f"topics rows: {len(top)} / columns: {len(top.columns)}")
print(f"runtime: {runtime_s}s = {runtime_s/60:.1f} min")
print(f"total laugh seconds: {total_laugh_s}")
print(f"lines that triggered laughter: {laugh_lines} of {len(cap)} "
      f"({100*laugh_lines/len(cap):.1f}%)")
print(f"loudest single laugh: {max_laugh}s at t={max_laugh_time}s "
      f"({max_laugh_time//60}:{max_laugh_time%60:02d}) — caption: {max_laugh_caption!r}")

# --- ana_02: Laugh percentage vs benchmark ---
print("=== ana_02 ===")
laugh_pct = 100 * total_laugh_s / runtime_s
laugh_per_min = total_laugh_s / (runtime_s / 60)
print(f"Total laugh time: {total_laugh_s}s across {runtime_s}s runtime")
print(f"Laughter share of runtime: {laugh_pct:.1f}%")
print(f"Laugh seconds per performing minute: {laugh_per_min:.2f}s")
print(f"Headline-comedian benchmark: ~18s/min (30% share)")
print(f"Ali Wong vs benchmark: {'above' if laugh_per_min > 18 else 'below'} headline threshold")
