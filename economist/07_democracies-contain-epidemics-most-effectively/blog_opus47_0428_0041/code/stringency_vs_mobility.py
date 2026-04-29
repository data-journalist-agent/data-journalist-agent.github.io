"""
Stringency (intent) vs mobility change (behaviour), by regime type.
Joins:
  OxCGRT (StringencyIndex, daily, country)  +  Global_Mobility_Report (workplaces % change, daily, country)
  +  Boix-Miller-Rosato democracy classification (most recent year per country)
April 2020 only (peak lockdown month).
"""
import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_pkg/economist/07_democracies-contain-epidemics-most-effectively"

# 1. Stringency: country-level mean for April 2020
ox = pd.read_csv(f"{DATA_DIR}/OxCGRT_20200525.csv", low_memory=False)
ox["Date"] = pd.to_datetime(ox["Date"], format="%Y%m%d")
ox_apr = ox[(ox["Date"].dt.year == 2020) & (ox["Date"].dt.month == 4)].copy()
ox_country = (
    ox_apr.groupby(["CountryCode", "CountryName"])["StringencyIndex"]
    .mean().round(1).reset_index()
    .rename(columns={"StringencyIndex": "stringency_apr"})
)

# 2. Mobility: country-level mean workplaces % change for April 2020
mob = pd.read_csv(f"{DATA_DIR}/Global_Mobility_Report.csv", low_memory=False)
mob["date"] = pd.to_datetime(mob["date"])
# country-level rows have empty sub_region_1
mob_country_rows = mob[mob["sub_region_1"].isna() & mob["sub_region_2"].isna()]
mob_apr = mob_country_rows[
    (mob_country_rows["date"].dt.year == 2020)
    & (mob_country_rows["date"].dt.month == 4)
].copy()
mob_country = (
    mob_apr.groupby("country_region_code")["workplaces_percent_change_from_baseline"]
    .mean().round(1).reset_index()
    .rename(columns={
        "country_region_code": "iso2",
        "workplaces_percent_change_from_baseline": "workplaces_apr",
    })
)

# 3. Democracy classification: most recent BMR year per country
bmr = pd.read_csv(f"{DATA_DIR}/democracy-v3.0.csv")
bmr_latest = bmr.sort_values("year").groupby("abbreviation", as_index=False).tail(1)
bmr_latest = bmr_latest[["abbreviation", "country", "democracy"]].rename(
    columns={"abbreviation": "iso3", "country": "country_bmr"}
)

# We need to join ISO2 (mobility) with ISO3 (BMR & OxCGRT). OxCGRT has CountryCode (ISO3).
# Build an iso2->iso3 lookup using OxCGRT (which has both CountryCode=ISO3 and CountryName);
# pull a sample per country.
# Simpler: join on country name via a small mapping using the mobility file's country name.

# Build iso2 -> name from mobility, then merge with OxCGRT by name? Easier path: use OxCGRT-only mobility?
# OxCGRT also has ConfirmedCases etc but no mobility. We rely on Google Mobility for mobility.
# Build a small iso2->iso3 map from a static lookup of countries present in BMR:
iso2_to_iso3 = {
    "US": "USA", "GB": "GBR", "FR": "FRA", "DE": "DEU", "IT": "ITA", "ES": "ESP",
    "JP": "JPN", "KR": "KOR", "CA": "CAN", "AU": "AUS", "NZ": "NZL", "IN": "IND",
    "BR": "BRA", "MX": "MEX", "ZA": "ZAF", "RU": "RUS", "CN": "CHN", "TR": "TUR",
    "ID": "IDN", "TH": "THA", "VN": "VNM", "PH": "PHL", "MY": "MYS", "SG": "SGP",
    "PT": "PRT", "NL": "NLD", "BE": "BEL", "SE": "SWE", "NO": "NOR", "DK": "DNK",
    "FI": "FIN", "IE": "IRL", "PL": "POL", "CZ": "CZE", "HU": "HUN", "RO": "ROU",
    "GR": "GRC", "AT": "AUT", "CH": "CHE", "AR": "ARG", "CL": "CHL", "CO": "COL",
    "PE": "PER", "EC": "ECU", "VE": "VEN", "BO": "BOL", "UY": "URY", "PY": "PRY",
    "EG": "EGY", "MA": "MAR", "DZ": "DZA", "TN": "TUN", "SA": "SAU", "AE": "ARE",
    "IL": "ISR", "JO": "JOR", "LB": "LBN", "QA": "QAT", "KW": "KWT", "BH": "BHR",
    "OM": "OMN", "IR": "IRN", "IQ": "IRQ", "PK": "PAK", "BD": "BGD", "LK": "LKA",
    "NP": "NPL", "MM": "MMR", "KH": "KHM", "LA": "LAO", "TW": "TWN", "HK": "HKG",
    "MO": "MAC", "MN": "MNG", "KZ": "KAZ", "UZ": "UZB", "KG": "KGZ", "TJ": "TJK",
    "TM": "TKM", "AZ": "AZE", "AM": "ARM", "GE": "GEO", "UA": "UKR", "BY": "BLR",
    "MD": "MDA", "RS": "SRB", "HR": "HRV", "SI": "SVN", "SK": "SVK", "BG": "BGR",
    "BA": "BIH", "MK": "MKD", "AL": "ALB", "ME": "MNE", "XK": "XKX", "CY": "CYP",
    "MT": "MLT", "EE": "EST", "LV": "LVA", "LT": "LTU", "IS": "ISL", "LU": "LUX",
    "NG": "NGA", "KE": "KEN", "ET": "ETH", "GH": "GHA", "CI": "CIV", "SN": "SEN",
    "CM": "CMR", "UG": "UGA", "TZ": "TZA", "ZM": "ZMB", "ZW": "ZWE", "MZ": "MOZ",
    "AO": "AGO", "RW": "RWA", "BW": "BWA", "NA": "NAM", "MW": "MWI", "MG": "MDG",
    "MU": "MUS", "RE": "REU", "BJ": "BEN", "BF": "BFA", "ML": "MLI", "NE": "NER",
    "CG": "COG", "CD": "COD", "GA": "GAB", "GN": "GIN", "TG": "TGO", "LR": "LBR",
    "SL": "SLE", "SO": "SOM", "DJ": "DJI", "ER": "ERI", "SS": "SSD", "SD": "SDN",
    "LY": "LBY", "YE": "YEM", "AF": "AFG", "BT": "BTN", "BN": "BRN", "DO": "DOM",
    "PR": "PRI", "GT": "GTM", "HN": "HND", "SV": "SLV", "NI": "NIC", "CR": "CRI",
    "PA": "PAN", "CU": "CUB", "JM": "JAM", "HT": "HTI", "BS": "BHS", "TT": "TTO",
    "BB": "BRB", "FJ": "FJI", "PG": "PNG", "MV": "MDV", "RW": "RWA",
}
mob_country["iso3"] = mob_country["iso2"].map(iso2_to_iso3)
mob_country = mob_country.dropna(subset=["iso3"])

merged = mob_country.merge(
    ox_country, left_on="iso3", right_on="CountryCode", how="inner"
).merge(bmr_latest, on="iso3", how="inner")

merged["regime"] = merged["democracy"].map({1: "Democracies", 0: "Non-Democracies"})
merged = merged[["iso3", "CountryName", "regime", "stringency_apr", "workplaces_apr"]]

# --- ana_07: stringency vs mobility, all merged countries ---
print("=== ana_07 ===")
print(f"countries merged: {len(merged)}")
print(f"democracies n = {(merged['regime']=='Democracies').sum()}")
print(f"non-democracies n = {(merged['regime']=='Non-Democracies').sum()}")
summary = merged.groupby("regime")[["stringency_apr", "workplaces_apr"]].mean().round(1)
print(summary)

# --- ana_08: at the SAME stringency level, do democracies move less? ---
print("=== ana_08 ===")
# Bin stringency: low (<60), mid (60-80), high (>=80)
def band(x):
    if x < 60: return "Low (<60)"
    if x < 80: return "Mid (60–80)"
    return "High (>=80)"
merged["stringency_band"] = merged["stringency_apr"].apply(band)
band_table = (
    merged.groupby(["stringency_band", "regime"])["workplaces_apr"].mean().round(1).unstack()
)
band_n = merged.groupby(["stringency_band", "regime"]).size().unstack()
print(band_table)
print("counts:")
print(band_n)

# --- ana_09: scatter rows for chart (one row per country) ---
print("=== ana_09 ===")
scatter = merged[["iso3", "CountryName", "regime", "stringency_apr", "workplaces_apr"]].copy()
scatter = scatter.sort_values(["regime", "iso3"])
print(scatter.head(40).to_string(index=False))
print(f"... ({len(scatter)} rows)")

# Save scatter for downstream packing into analyst.json
scatter.to_csv(
    "/Users/forrest/Desktop/data2blog/project/economist/07_democracies-contain-epidemics-most-effectively/blog_opus47_0428_0041/code/_scatter.csv",
    index=False,
)
