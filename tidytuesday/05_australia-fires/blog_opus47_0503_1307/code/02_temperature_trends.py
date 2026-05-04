"""Temperature trends — compare 2010s decade vs 1910-1940 baseline for each capital city.

Uses MAX temperatures only. Aggregates daily values into city-year means
for max temps, then computes decadal anomalies vs the 1910-1940 baseline.
"""
import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/05_australia-fires"

temp = pd.read_csv(f"{DATA}/temperature.csv")
temp["date"] = pd.to_datetime(temp["date"], errors="coerce")
temp = temp.dropna(subset=["date", "temperature"]).copy()
temp["year"] = temp["date"].dt.year
temp["city_name"] = temp["city_name"].str.title()

# Use only the six standard cities
CITIES = ["Brisbane", "Canberra", "Melbourne", "Perth", "Sydney"]
temp = temp[temp["city_name"].isin(CITIES)]

# --- ana_01: decadal mean max temperature by city ---
print("=== ana_01 ===")
tmax = temp[temp["temp_type"] == "max"].copy()
yearly = tmax.groupby(["city_name", "year"])["temperature"].mean().reset_index()

# Baseline 1910-1940, recent 2010-2019
base = yearly[(yearly["year"] >= 1910) & (yearly["year"] <= 1940)].groupby("city_name")["temperature"].mean()
recent = yearly[(yearly["year"] >= 2010) & (yearly["year"] <= 2019)].groupby("city_name")["temperature"].mean()
delta = (recent - base).round(2)
out = pd.DataFrame({"baseline_1910_1940_C": base.round(2), "recent_2010_2019_C": recent.round(2), "delta_C": delta})
out = out.sort_values("delta_C", ascending=False)
print(out.to_string())

# --- ana_02: yearly mean max temperature, all cities, full series for line chart ---
print("=== ana_02 ===")
yearly_all = tmax.groupby("year")["temperature"].mean().reset_index()
yearly_all.columns = ["year", "mean_max_C"]
yearly_all = yearly_all[yearly_all["year"] >= 1910]
print(f"first year: {yearly_all['year'].min()}  last year: {yearly_all['year'].max()}")
print(yearly_all.tail(10).to_string(index=False))
print(f"earliest 5y avg: {yearly_all.iloc[:5]['mean_max_C'].mean():.2f} C")
print(f"latest 5y avg:   {yearly_all.iloc[-5:]['mean_max_C'].mean():.2f} C")

# --- ana_03: per-city yearly mean max series, last 110y, for small multiples ---
print("=== ana_03 ===")
city_yearly = (
    tmax.groupby(["city_name", "year"])["temperature"].mean().reset_index().rename(columns={"temperature": "mean_max_C"})
)
city_yearly = city_yearly[(city_yearly["year"] >= 1910) & (city_yearly["year"] <= 2019)]
# Show the per-city deltas one more time with clean numbers.
for c in CITIES:
    sub = city_yearly[city_yearly["city_name"] == c].sort_values("year")
    if len(sub) > 0:
        first = sub.head(10)["mean_max_C"].mean()
        last = sub.tail(10)["mean_max_C"].mean()
        print(f"{c}: first 10y = {first:.2f}, last 10y = {last:.2f}, delta = {last - first:+.2f} C")

city_yearly.to_csv(f"{DATA.replace('data_preprint', 'data_preprint')}/_temp_city_yearly.csv", index=False)
