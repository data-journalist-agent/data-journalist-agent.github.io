"""Load both tables, print dataset profile + per-column null/cardinality."""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/07_the-history-of-himalayan-mountaineering-expedition"

exped = pd.read_csv(os.path.join(DATA_DIR, "exped_tidy.csv"), low_memory=False, encoding="latin-1")
peaks = pd.read_csv(os.path.join(DATA_DIR, "peaks_tidy.csv"), low_memory=False, encoding="latin-1")

# --- ana_00: Dataset profile ---
print("=== ana_00 ===")
print(f"exped rows={len(exped)}, cols={exped.shape[1]}")
print(f"peaks rows={len(peaks)}, cols={peaks.shape[1]}")
print("YEAR range:", sorted(exped["YEAR"].unique()))
print("seasons:", exped["SEASON_FACTOR"].value_counts().to_dict())
print("hosts:", exped["HOST_FACTOR"].value_counts().to_dict())
print("peaks PSTATUS:", peaks["PSTATUS_FACTOR"].value_counts().to_dict())
print("expeditions per year:", exped["YEAR"].value_counts().sort_index().to_dict())
