"""Properties of the 954 named colors: hue distribution, basic-color
membership, name structure (compound names, modifiers).
"""
import pandas as pd
import numpy as np
import colorsys
import re
from collections import Counter

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/14_the-xkcd-color-survey-results'
color_ranks = pd.read_csv(f'{DATA_DIR}/color_ranks.csv')

def hex_to_hsv(h):
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    H, S, V = colorsys.rgb_to_hsv(r, g, b)
    return H * 360, S, V

color_ranks[['H', 'S', 'V']] = color_ranks['hex'].apply(lambda h: pd.Series(hex_to_hsv(h)))

# --- ana_05: Top 30 colors ---
print("=== ana_05 ===")
top30 = color_ranks.head(30)[['rank', 'color', 'hex']]
print(top30.to_string(index=False))

# --- ana_06: Hue distribution of 954 colors ---
print("=== ana_06 ===")
# bucket by hue (15-degree bins). Treat low-saturation (S<0.1) as 'achromatic'.
def hue_bucket(row):
    if row['S'] < 0.1:
        return 'achromatic (gray/white/black)'
    h = row['H']
    if h < 15 or h >= 345: return 'red (0-15, 345-360)'
    if h < 45: return 'orange (15-45)'
    if h < 75: return 'yellow (45-75)'
    if h < 105: return 'yellow-green (75-105)'
    if h < 165: return 'green (105-165)'
    if h < 195: return 'cyan/teal (165-195)'
    if h < 255: return 'blue (195-255)'
    if h < 285: return 'purple (255-285)'
    if h < 315: return 'magenta (285-315)'
    return 'pink (315-345)'

color_ranks['hue_bucket'] = color_ranks.apply(hue_bucket, axis=1)
hue_counts = color_ranks['hue_bucket'].value_counts()
print(hue_counts)
print(f"\nTotal: {len(color_ranks)}")

# --- ana_07: Basic color terms presence in 954 ---
print("=== ana_07 ===")
basics = ['red','orange','yellow','green','blue','purple','pink','brown','black','white','grey','gray']
basic_in = {b: int((color_ranks['color'] == b).any()) for b in basics}
basic_rank = {b: int(color_ranks[color_ranks['color'] == b]['rank'].min()) if (color_ranks['color'] == b).any() else None for b in basics}
print("basic | present | rank")
for b in basics:
    print(f"{b:8s} | {basic_in[b]} | {basic_rank[b]}")

# Names containing each basic root
basic_root_counts = {}
for b in basics:
    pat = re.compile(r'\b' + b + r'\b|' + b + r'(?:y|ish)?')
    basic_root_counts[b] = int(color_ranks['color'].str.contains(pat, regex=True).sum())
print("\nNames CONTAINING each basic root word:")
for b, c in sorted(basic_root_counts.items(), key=lambda kv: -kv[1]):
    print(f"  {b:8s}: {c}")

# --- ana_08: Compound name structure / modifiers ---
print("=== ana_08 ===")
# A name is "compound" if it has a space or hyphen
color_ranks['n_words'] = color_ranks['color'].str.replace('-', ' ').str.split().str.len()
word_counts = color_ranks['n_words'].value_counts().sort_index()
print("Words per name (1 = single word, 2 = e.g. 'dusty teal'):")
print(word_counts)
print(f"% multi-word: {(color_ranks['n_words'] > 1).mean()*100:.2f}%")

# Most productive modifiers (first word in a multi-word name, or pre/suffix)
multi = color_ranks[color_ranks['n_words'] > 1].copy()
multi['first_word'] = multi['color'].str.replace('-', ' ').str.split().str[0]
multi['last_word'] = multi['color'].str.replace('-', ' ').str.split().str[-1]
print("\nTop 15 first words (modifiers):")
print(multi['first_word'].value_counts().head(15))
print("\nTop 15 last words (heads):")
print(multi['last_word'].value_counts().head(15))

# Suffix -ish, -y
ish = color_ranks['color'].str.endswith('ish').sum()
y = (color_ranks['color'].str.endswith('y') & ~color_ranks['color'].str.contains(' ')).sum()
print(f"\nNames ending in -ish: {ish}")
print(f"Single-word names ending in -y (e.g. 'dusty'): {y}")

# --- ana_09: Achromatic colors and grayscale spectrum ---
print("=== ana_09 ===")
achr = color_ranks[color_ranks['hue_bucket'] == 'achromatic (gray/white/black)'].sort_values('V')
print(f"Achromatic count: {len(achr)}")
print(achr[['color','rank','hex','V']].to_string(index=False))
