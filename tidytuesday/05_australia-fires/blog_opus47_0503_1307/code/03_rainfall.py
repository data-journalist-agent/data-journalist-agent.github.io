"""Rainfall analysis — annual totals per city, with 2019 anomaly highlighted."""
import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/05_australia-fires"

rain = pd.read_csv(f"{DATA}/rainfall.csv", dtype={"month": str, "day": str})
rain["rainfall"] = pd.to_numeric(rain["rainfall"], errors="coerce")
rain = rain.dropna(subset=["rainfall", "year"])

# --- ana_04: 2019 annual rainfall vs long-term per-city averages ---
print("=== ana_04 ===")
yearly = rain.groupby(["city_name", "year"])["rainfall"].sum().reset_index()
yearly.columns = ["city_name", "year", "annual_mm"]
# Filter complete-ish years: keep only years where the station has >=300 daily rows
day_counts = rain.groupby(["city_name", "year"]).size().reset_index(name="n_days")
yearly = yearly.merge(day_counts, on=["city_name", "year"])
yearly = yearly[yearly["n_days"] >= 300]

avg = yearly.groupby("city_name")["annual_mm"].mean().round(0).rename("avg_annual_mm")
y2019 = yearly[yearly["year"] == 2019].set_index("city_name")["annual_mm"].rename("year_2019_mm")
table = pd.concat([avg, y2019], axis=1)
table["pct_of_avg"] = (table["year_2019_mm"] / table["avg_annual_mm"] * 100).round(0)
table = table.sort_values("pct_of_avg")
print(table.to_string())

# --- ana_05: 2019 ranked among each city's history (driest years on record) ---
print("=== ana_05 ===")
for c in sorted(yearly["city_name"].unique()):
    sub = yearly[yearly["city_name"] == c].sort_values("annual_mm").reset_index(drop=True)
    if (sub["year"] == 2019).any():
        rank_2019 = int(sub.index[sub["year"] == 2019][0]) + 1
        total_yrs = len(sub)
        driest = sub.iloc[0]
        print(f"{c}: 2019 rank = {rank_2019} of {total_yrs} ({rank_2019/total_yrs*100:.1f} pctl); driest year overall = {int(driest['year'])} at {driest['annual_mm']:.0f} mm")

# --- ana_06: monthly rainfall pattern in 2019 (deviation from climatology) ---
print("=== ana_06 ===")
rain["month_num"] = pd.to_numeric(rain["month"], errors="coerce")
clim = rain[rain["year"] < 2019].groupby(["city_name", "month_num"])["rainfall"].sum().reset_index()
clim_avg = clim.groupby(["city_name", "month_num"])["rainfall"].mean().reset_index()
# Better: use sum per (city, year, month) then average across years
mset = rain.groupby(["city_name", "year", "month_num"])["rainfall"].sum().reset_index()
clim_avg = mset[mset["year"] < 2019].groupby(["city_name", "month_num"])["rainfall"].mean().reset_index()
clim_avg.columns = ["city_name", "month_num", "avg_mm"]
y2019m = mset[mset["year"] == 2019].rename(columns={"rainfall": "y2019_mm"})
m = clim_avg.merge(y2019m[["city_name", "month_num", "y2019_mm"]], on=["city_name", "month_num"], how="left")
m["delta_mm"] = (m["y2019_mm"] - m["avg_mm"]).round(1)
print(m.to_string(index=False))

# --- ana_07: nationwide 2019 rainfall total vs long-term mean across all six cities pooled ---
print("=== ana_07 ===")
nat = yearly.groupby("year")["annual_mm"].mean().rename("avg_six_city_mm").reset_index()
print("recent years:")
print(nat.tail(10).to_string(index=False))
nat_2019 = nat[nat["year"] == 2019]["avg_six_city_mm"].iloc[0]
nat_avg = nat[nat["year"] < 2019]["avg_six_city_mm"].mean()
print(f"long-term mean (pre-2019): {nat_avg:.0f} mm; 2019: {nat_2019:.0f} mm; pct = {nat_2019/nat_avg*100:.0f}%")
