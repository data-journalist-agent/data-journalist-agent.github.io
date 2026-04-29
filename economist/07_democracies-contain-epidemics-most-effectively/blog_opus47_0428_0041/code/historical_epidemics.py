"""
Historical EM-DAT check: do democracies suffer fewer epidemic deaths per outbreak,
controlling roughly for income via Maddison terciles?
We use the Boix-Miller-Rosato classification at the epidemic's start year.
"""
import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_pkg/economist/07_democracies-contain-epidemics-most-effectively"

emdat = pd.read_csv(f"{DATA_DIR}/emdat_full.csv", encoding="latin-1", low_memory=False)
bmr = pd.read_csv(f"{DATA_DIR}/democracy-v3.0.csv", low_memory=False)

# Restrict to epidemics
ep = emdat[emdat["Disaster Type"] == "Epidemic"].copy()
ep = ep[ep["Total Deaths"].notna() & ep["Year"].notna()]
ep["Year"] = ep["Year"].astype(int)
ep = ep[ep["Year"] >= 1960]

# Join democracy classification at year of outbreak
bmr_small = bmr[["abbreviation", "year", "democracy"]].rename(
    columns={"abbreviation": "ISO"}
)
ep = ep.merge(bmr_small, left_on=["ISO", "Year"], right_on=["ISO", "year"], how="left")
ep["regime"] = ep["democracy"].map({1: "Democracies", 0: "Non-Democracies"})

# --- ana_10: epidemic count and total deaths, by regime, since 1960 ---
print("=== ana_10 ===")
agg = (
    ep.dropna(subset=["regime"])
    .groupby("regime")
    .agg(
        epidemics=("Total Deaths", "size"),
        total_deaths=("Total Deaths", "sum"),
        median_deaths=("Total Deaths", "median"),
        mean_deaths=("Total Deaths", "mean"),
    )
    .round(1)
)
print(agg)

# --- ana_11: median deaths per outbreak, by regime + decade ---
print("=== ana_11 ===")
ep["decade"] = (ep["Year"] // 10 * 10).astype(int)
dec = (
    ep.dropna(subset=["regime"])
    .groupby(["decade", "regime"])["Total Deaths"]
    .median()
    .unstack()
    .round(1)
)
print(dec)

# --- ana_12: epidemic types most common in each regime ---
print("=== ana_12 ===")
typ = (
    ep.dropna(subset=["regime"])
    .groupby(["regime", "Disaster Subtype"])
    .size()
    .unstack(fill_value=0)
)
typ["total"] = typ.sum(axis=1)
print(typ.T.sort_values(typ.index[0], ascending=False).head(15))

# --- ana_13: countries with most recorded epidemics ---
print("=== ana_13 ===")
top = (
    ep.dropna(subset=["regime"])
    .groupby(["Country", "regime"])["Total Deaths"]
    .agg(["size", "sum"])
    .sort_values("size", ascending=False)
    .head(15)
)
print(top)
