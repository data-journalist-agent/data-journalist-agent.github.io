"""Main analyses for the Himalayan blog. Each finding section produces ana_xx markers and reproducible numbers."""
import pandas as pd
import numpy as np
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/07_the-history-of-himalayan-mountaineering-expedition"
exped = pd.read_csv(os.path.join(DATA_DIR, "exped_tidy.csv"), low_memory=False, encoding="latin-1")
peaks = pd.read_csv(os.path.join(DATA_DIR, "peaks_tidy.csv"), low_memory=False, encoding="latin-1")

# Add a peak-name lookup so we can join exped to peaks_tidy
peak_lookup = peaks.set_index("PEAKID")[["PKNAME", "HEIGHTM", "HIMAL_FACTOR", "REGION_FACTOR"]].to_dict("index")
def look(peakid, key):
    info = peak_lookup.get(peakid, {})
    return info.get(key, None)
exped["PEAK_NAME"] = exped["PEAKID"].apply(lambda x: look(x, "PKNAME"))
exped["PEAK_HEIGHTM"] = exped["PEAKID"].apply(lambda x: look(x, "HEIGHTM"))
exped["PEAK_HIMAL"] = exped["PEAKID"].apply(lambda x: look(x, "HIMAL_FACTOR"))
exped["PEAK_REGION"] = exped["PEAKID"].apply(lambda x: look(x, "REGION_FACTOR"))

# Define success: TERMREASON 1,2,3 = success
exped["IS_SUCCESS"] = exped["TERMREASON"].isin([1, 2, 3])
exped["TOTAL_DEATHS"] = exped["MDEATHS"].fillna(0) + exped["HDEATHS"].fillna(0)

# --- ana_01: Year-over-year expedition volume (post-COVID rebound) ---
print("=== ana_01 ===")
year_counts = exped["YEAR"].value_counts().sort_index()
print(year_counts.to_string())
print(f"2020 -> 2022 multiplier: {year_counts[2022]/year_counts[2020]:.1f}x")
print(f"2024 (partial year): {year_counts[2024]} expeditions")

# --- ana_02: Top peaks by expedition count, 2020-2024 ---
print("\n=== ana_02 ===")
peak_counts = exped.groupby("PEAK_NAME").size().sort_values(ascending=False).head(20)
print(peak_counts.to_string())
print(f"Total expeditions: {len(exped)}")
print(f"Everest share: {peak_counts.get('Everest', 0)/len(exped)*100:.1f}%")
top3_share = peak_counts.head(3).sum() / len(exped) * 100
print(f"Top-3 peaks share of all expeditions: {top3_share:.1f}%")

# --- ana_03: Success rate by peak (top peaks with >= 10 expeditions) ---
print("\n=== ana_03 ===")
g = exped.groupby("PEAK_NAME").agg(n=("IS_SUCCESS", "size"), success=("IS_SUCCESS", "sum"))
g["rate"] = g["success"] / g["n"] * 100
g = g[g["n"] >= 10].sort_values("rate", ascending=False)
print(g.to_string())

# --- ana_04: Termination reason distribution ---
print("\n=== ana_04 ===")
term = exped["TERMREASON_FACTOR"].value_counts()
term_pct = (term / term.sum() * 100).round(2)
combined = pd.DataFrame({"count": term, "pct": term_pct}).sort_values("count", ascending=False)
print(combined.to_string())

# --- ana_05: Failure-only termination reasons (excludes successes) ---
print("\n=== ana_05 ===")
fail = exped[~exped["IS_SUCCESS"]]["TERMREASON_FACTOR"].value_counts()
fail_pct = (fail / fail.sum() * 100).round(2)
combined_fail = pd.DataFrame({"count": fail, "pct": fail_pct}).sort_values("count", ascending=False)
print(combined_fail.to_string())
print(f"Total failures: {len(exped)-int(exped['IS_SUCCESS'].sum())}")
print(f"Bad weather: {fail.get('Bad weather (storms, high winds)',0)} ({fail_pct.get('Bad weather (storms, high winds)',0)}%)")
print(f"Route too difficult: {fail.get('Route technically too difficult, lack of experience, strength, or motivation',0)} ({fail_pct.get('Route technically too difficult, lack of experience, strength, or motivation',0)}%)")

# --- ana_06: Oxygen use vs success ---
print("\n=== ana_06 ===")
o2_success = exped.groupby("O2USED")["IS_SUCCESS"].agg(["size", "sum", "mean"])
o2_success["pct"] = (o2_success["mean"] * 100).round(2)
print(o2_success.to_string())

o2_used = exped[exped["O2USED"] == True]
o2_not  = exped[exped["O2USED"] == False]
print(f"\nO2 used: n={len(o2_used)} success={o2_used['IS_SUCCESS'].mean()*100:.1f}%")
print(f"O2 not used: n={len(o2_not)} success={o2_not['IS_SUCCESS'].mean()*100:.1f}%")

# --- ana_07: Death rate by oxygen use ---
print("\n=== ana_07 ===")
o2_deaths = exped.groupby("O2USED")["TOTAL_DEATHS"].agg(["size", "sum", "mean"])
print(o2_deaths.to_string())
o2_used_dr = (exped[exped["O2USED"]==True]["TOTAL_DEATHS"]>0).mean()*100
o2_not_dr  = (exped[exped["O2USED"]==False]["TOTAL_DEATHS"]>0).mean()*100
print(f"\nFatal-expedition rate, O2 used: {o2_used_dr:.2f}%")
print(f"Fatal-expedition rate, no O2: {o2_not_dr:.2f}%")

# --- ana_08: Hired-personnel vs no-hired-personnel deaths ---
print("\n=== ana_08 ===")
hired = exped.groupby("NOHIRED").agg(
    n=("IS_SUCCESS", "size"),
    member_deaths=("MDEATHS", "sum"),
    hired_deaths=("HDEATHS", "sum"),
    success_rate=("IS_SUCCESS", "mean"),
    members=("TOTMEMBERS", "sum"),
    hired=("TOTHIRED", "sum"),
)
print(hired.to_string())

with_hired = exped[exped["NOHIRED"]==False]
no_hired = exped[exped["NOHIRED"]==True]
print(f"\nWith hired: n={len(with_hired)}, member_deaths={int(with_hired['MDEATHS'].sum())}, hired_deaths={int(with_hired['HDEATHS'].sum())}")
print(f"           success_rate={with_hired['IS_SUCCESS'].mean()*100:.1f}%")
print(f"           total members={int(with_hired['TOTMEMBERS'].sum())}, total hired={int(with_hired['TOTHIRED'].sum())}")
print(f"No hired: n={len(no_hired)}, member_deaths={int(no_hired['MDEATHS'].sum())}, hired_deaths={int(no_hired['HDEATHS'].sum())}")
print(f"           success_rate={no_hired['IS_SUCCESS'].mean()*100:.1f}%")
print(f"           total members={int(no_hired['TOTMEMBERS'].sum())}")

# --- ana_09: Sherpa fatality share (HDEATHS vs MDEATHS) ---
print("\n=== ana_09 ===")
total_m = int(exped["MDEATHS"].sum())
total_h = int(exped["HDEATHS"].sum())
total_mem = int(exped["TOTMEMBERS"].sum())
total_hired = int(exped["TOTHIRED"].sum())
print(f"Member deaths: {total_m}")
print(f"Hired (Sherpa) deaths: {total_h}")
print(f"Total deaths: {total_m+total_h}")
print(f"Hired share of deaths: {total_h/(total_m+total_h)*100:.1f}%")
print(f"Member-death rate per person: {total_m/total_mem*1000:.2f} per 1000")
print(f"Hired-death rate per person: {total_h/total_hired*1000:.2f} per 1000")
print(f"Total members: {total_mem}, total hired: {total_hired}")

# --- ana_10: Seasonality ---
print("\n=== ana_10 ===")
season_total = exped["SEASON_FACTOR"].value_counts()
season_pct = (season_total / season_total.sum() * 100).round(2)
season_success = exped.groupby("SEASON_FACTOR")["IS_SUCCESS"].agg(["size", "mean"])
season_success["pct"] = (season_success["mean"] * 100).round(2)
print("Counts:", season_total.to_dict())
print("Pct:", season_pct.to_dict())
print("\nSuccess by season:")
print(season_success.to_string())

# --- ana_11: Eight-thousanders summary ---
print("\n=== ana_11 ===")
EIGHT_K = ["Everest", "Kangchenjunga", "Lhotse", "Makalu", "Cho Oyu", "Dhaulagiri I", "Manaslu", "Annapurna I"]
sub = exped[exped["PEAK_NAME"].isin(EIGHT_K)].copy()
print(f"Eight-thousander expeditions in slice: {len(sub)} ({len(sub)/len(exped)*100:.1f}% of all)")
g8 = sub.groupby("PEAK_NAME").agg(
    n=("IS_SUCCESS", "size"),
    success=("IS_SUCCESS", "sum"),
    member_deaths=("MDEATHS", "sum"),
    hired_deaths=("HDEATHS", "sum"),
    total_members=("TOTMEMBERS", "sum"),
    total_hired=("TOTHIRED", "sum"),
)
g8["success_rate"] = (g8["success"] / g8["n"] * 100).round(2)
g8["death_rate_per1000"] = ((g8["member_deaths"] + g8["hired_deaths"]) / (g8["total_members"] + g8["total_hired"]) * 1000).round(2)
g8["height_m"] = g8.index.map(lambda p: peaks.set_index("PKNAME").loc[p, "HEIGHTM"] if p in peaks["PKNAME"].values else None)
g8 = g8.sort_values("height_m", ascending=False)
print(g8.to_string())

# --- ana_12: Top nationalities ---
print("\n=== ana_12 ===")
nation = exped["NATION"].value_counts().head(15)
nation_pct = (nation / len(exped) * 100).round(2)
print(pd.DataFrame({"count": nation, "pct": nation_pct}).to_string())
print(f"Distinct nationalities: {exped['NATION'].nunique()}")

# --- ana_13: Disputed and claimed flags ---
print("\n=== ana_13 ===")
print(f"Total expeditions: {len(exped)}")
print(f"CLAIMED=TRUE (success claimed): {int(exped['CLAIMED'].sum())}")
print(f"DISPUTED=TRUE: {int(exped['DISPUTED'].sum())}")
print(f"Disputed share of claimed: {int(exped['DISPUTED'].sum())/max(1,int(exped['CLAIMED'].sum()))*100:.1f}%")

# --- ana_14: Average summit days, total days, by 8000er status ---
print("\n=== ana_14 ===")
exped["IS_8000"] = exped["PEAK_HEIGHTM"] >= 8000
overall = exped["TOTDAYS"].dropna()
exp8000 = exped[exped["IS_8000"]]["TOTDAYS"].dropna()
expsmall = exped[~exped["IS_8000"]]["TOTDAYS"].dropna()
print(f"Avg total days, all expeditions: {overall.mean():.1f} (n={len(overall)})")
print(f"Avg total days, 8000ers: {exp8000.mean():.1f} (n={len(exp8000)})")
print(f"Avg total days, sub-8000m: {expsmall.mean():.1f} (n={len(expsmall)})")
print(f"Median total days, 8000ers: {exp8000.median():.0f}")
print(f"Median total days, sub-8000: {expsmall.median():.0f}")

# --- ana_15: Peak-height distribution and unclimbed peaks ---
print("\n=== ana_15 ===")
heights = peaks["HEIGHTM"].dropna()
print(f"Total peaks listed: {len(peaks)}")
print(f"Climbed: {(peaks['PSTATUS_FACTOR']=='Climbed').sum()}")
print(f"Unclimbed: {(peaks['PSTATUS_FACTOR']=='Unclimbed').sum()}")
print(f"Median height: {heights.median():.0f} m")
print(f"Max height: {heights.max():.0f} m ({peaks.loc[peaks['HEIGHTM'].idxmax(),'PKNAME']})")
unclimbed = peaks[peaks["PSTATUS_FACTOR"]=="Unclimbed"]
print(f"\nUnclimbed range: {unclimbed['HEIGHTM'].min()}-{unclimbed['HEIGHTM'].max()} m, median {unclimbed['HEIGHTM'].median():.0f} m")
print(f"Unclimbed by range:")
print(unclimbed["HIMAL_FACTOR"].value_counts().head(10).to_string())

# --- ana_16: Camps and rope length on 8000ers ---
print("\n=== ana_16 ===")
print(f"Avg camps, 8000ers: {exped[exped['IS_8000']]['CAMPS'].mean():.2f}")
print(f"Avg camps, sub-8000: {exped[~exped['IS_8000']]['CAMPS'].mean():.2f}")
print(f"Avg rope (m), 8000ers: {exped[exped['IS_8000']]['ROPE'].mean():.0f}")
print(f"Avg rope (m), sub-8000: {exped[~exped['IS_8000']]['ROPE'].mean():.0f}")

# --- ana_17: Failure mix on Annapurna I, Dhaulagiri I, Everest ---
print("\n=== ana_17 ===")
for peak in ["Everest", "Annapurna I", "Dhaulagiri I", "Manaslu", "Cho Oyu"]:
    s = exped[exped["PEAK_NAME"]==peak]
    if len(s)==0:
        continue
    succ = s["IS_SUCCESS"].mean()*100
    deaths = int(s["MDEATHS"].sum() + s["HDEATHS"].sum())
    n = len(s)
    print(f"{peak}: n={n}, success={succ:.1f}%, deaths={deaths}")

# --- ana_18: Year x success rate trend ---
print("\n=== ana_18 ===")
year_succ = exped.groupby("YEAR").agg(n=("IS_SUCCESS","size"), succ=("IS_SUCCESS","mean"))
year_succ["pct"] = (year_succ["succ"]*100).round(2)
print(year_succ.to_string())

# --- ana_19: Approach (caravan) length distribution top 10 ---
print("\n=== ana_19 ===")
appr = exped["APPROACH"].value_counts().head(10)
print(appr.to_string())

# --- ana_20: Per-1000-climber death rate by peak (8000ers, sorted) ---
print("\n=== ana_20 ===")
print(g8[["n","total_members","total_hired","member_deaths","hired_deaths","death_rate_per1000","success_rate"]].sort_values("death_rate_per1000", ascending=False).to_string())
