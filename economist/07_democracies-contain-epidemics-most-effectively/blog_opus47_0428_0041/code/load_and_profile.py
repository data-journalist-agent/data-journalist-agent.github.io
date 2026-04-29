"""
Profile every CSV in the dataset folder.
Run from anywhere; we use absolute paths.
"""
import os
import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_pkg/economist/07_democracies-contain-epidemics-most-effectively"

files = [
    "mobility_change_by_type_regime_and_time.v1.2.csv",
    "Global_Mobility_Report.csv",
    "OxCGRT_20200525.csv",
    "democracy-v3.0.csv",
    "freedomhouse.csv",
    "p4v2016.csv",
    "emdat_full.csv",
    "maddison_project_gdppc.csv",
]

# --- ana_00: dataset profile ---
print("=== ana_00 ===")
for f in files:
    path = os.path.join(DATA_DIR, f)
    try:
        df = pd.read_csv(path, low_memory=False, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, low_memory=False, encoding="latin-1")
    print(f"{f}: rows={len(df)} cols={df.shape[1]}")
