"""Export the canonical 949-color palette as a compact JSON for visualization
and write a small chart-ready palette CSV.
"""
import pandas as pd
import json
import colorsys

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/14_the-xkcd-color-survey-results'
color_ranks = pd.read_csv(f'{DATA_DIR}/color_ranks.csv')

def hex_to_hsv(h):
    h = h.lstrip('#')
    r,g,b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
    H,S,V = colorsys.rgb_to_hsv(r,g,b)
    return round(H*360,1), round(S,3), round(V,3)

color_ranks[['H','S','V']] = color_ranks['hex'].apply(lambda h: pd.Series(hex_to_hsv(h)))
color_ranks.to_csv('/tmp/palette_full.csv', index=False)

# --- ana_25: Hue distribution full palette ---
print("=== ana_25 ===")
out = color_ranks[['rank','color','hex','H','S','V']].head(100).to_dict(orient='records')
print(f"Top 100 exported. Total: {len(color_ranks)}")
print(json.dumps(out[:10], indent=2))
