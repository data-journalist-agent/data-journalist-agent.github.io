"""Geographic hotspots — intake density by lat/lon and zip-cluster guess."""
import pandas as pd
from pathlib import Path
import re

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/09_long-beach-animal-shelter/longbeach.csv')
df = pd.read_csv(DATA, low_memory=False)
for col in ['dob', 'intake_date', 'outcome_date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# --- ana_21: intake hotspots by ZIP (grep ZIP from crossing field) ---
print("=== ana_21 ===")
def zip_of(c):
    if pd.isna(c): return None
    m = re.search(r'\b(90\d{3})\b', str(c))
    if m: return m.group(1)
    return None
df['zip'] = df['crossing'].apply(zip_of)
zips = df['zip'].value_counts().head(15)
print(zips.to_string())
print()

# --- ana_22: lat/lon bbox + sample for map ---
print("=== ana_22 ===")
geo = df.dropna(subset=['latitude', 'longitude'])
geo = geo[(geo['latitude'] > 33.0) & (geo['latitude'] < 35.0) & (geo['longitude'] > -119) & (geo['longitude'] < -117)]
print(f"valid geo rows: {len(geo)} of {len(df)}")
print(f"lat range: {geo['latitude'].min():.4f} -> {geo['latitude'].max():.4f}")
print(f"lon range: {geo['longitude'].min():.4f} -> {geo['longitude'].max():.4f}")
print(f"lat median: {geo['latitude'].median():.4f}")
print(f"lon median: {geo['longitude'].median():.4f}")

# --- ana_23: hex bin counts (~0.005 deg resolution) for top intake heat blocks ---
print("=== ana_23 ===")
geo = geo.copy()
geo['lat_bin'] = (geo['latitude'] * 200).round() / 200
geo['lon_bin'] = (geo['longitude'] * 200).round() / 200
hot = geo.groupby(['lat_bin', 'lon_bin']).size().reset_index(name='count').sort_values('count', ascending=False).head(15)
print(hot.to_string(index=False))
