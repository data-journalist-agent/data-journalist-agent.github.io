"""Find the funniest individual lines and bits — what actually gets the biggest laugh."""
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/57_stand-up")
cap = pd.read_csv(DATA_DIR / "ali-wong--captions.csv")

# --- ana_12: Top 10 loudest single captions ---
print("=== ana_12 ===")
top10 = cap.nlargest(10, "laugh")[["timeStart", "caption", "laugh", "group"]].copy()
for _, r in top10.iterrows():
    ts = int(r["timeStart"])
    print(f"  t={ts}s ({ts//60}:{ts%60:02d}) laugh={r['laugh']}s "
          f"group={r['group']}: {r['caption'].strip()!r}")

# --- ana_13: Top 10 funniest bits (by total laugh per bit) ---
print("=== ana_13 ===")
bits = cap.groupby("group").agg(
    laugh_s=("laugh", "sum"),
    n_lines=("laugh", "size"),
    start=("timeStart", "min"),
    end=("timeStop", "max"),
).reset_index()
bits["dur_s"] = bits["end"] - bits["start"]
bits["laugh_per_min"] = bits["laugh_s"] / (bits["dur_s"] / 60)
bits = bits[bits["dur_s"] > 0]
top_bits = bits.nlargest(10, "laugh_s")
print("Bits with the most total laughter:")
print(top_bits[["group", "start", "dur_s", "n_lines",
                "laugh_s", "laugh_per_min"]].to_string(index=False))

# --- ana_14: Setup-to-punchline ratio ---
print("=== ana_14 ===")
silent = int((cap["laugh"] == 0).sum())
total = len(cap)
print(f"Lines with zero laughter: {silent} of {total} ({100*silent/total:.1f}%)")
print(f"Lines that landed a laugh: {total - silent} "
      f"({100*(total-silent)/total:.1f}%)")
print(f"Implied setup-to-payoff ratio: {silent/(total-silent):.2f} : 1")
