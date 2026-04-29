"""Load summary, daySummary, pvals; profile dataset and produce all findings."""
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path('/Users/forrest/Desktop/data2blog/data/04_country-radio-data')
SUMMARY = pd.read_csv(DATA_DIR / 'output' / 'summary.csv')
DAYSUM  = pd.read_csv(DATA_DIR / 'output' / 'daySummary.csv')
PVALS   = pd.read_csv(DATA_DIR / 'analysis' / 'pvals.csv')

# normalize columns
PVALS.columns = [c.strip() for c in PVALS.columns]

print("=== profile ===")
print(f"summary rows: {len(SUMMARY)}, cols: {SUMMARY.shape[1]}")
print(f"daySummary rows: {len(DAYSUM)}, cols: {DAYSUM.shape[1]}")
print(f"pvals rows: {len(PVALS)}")
print(f"unique cities: {SUMMARY['cityName'].nunique()}")
print(f"unique stations: {SUMMARY['stationName'].nunique()}")
print(f"unique owners: {SUMMARY['ownerName'].nunique()}")
print("owner counts:")
print(SUMMARY['ownerName'].value_counts().to_string())
print(f"date range: {DAYSUM['date'].min()} → {DAYSUM['date'].max()} ({DAYSUM['date'].nunique()} unique dates)")
print(f"total songs across stations: {SUMMARY['total_COUNT'].sum():,}")

# --- ana_01: Headline - back-to-back women vs men gap ---
print("\n=== ana_01 ===")
total_songs = SUMMARY['total_COUNT'].sum()
total_b2b_women = SUMMARY['b2bWomenSongs_COUNT'].sum()
total_b2b_men   = SUMMARY['b2bMenSongs_COUNT'].sum()
total_b2b_mixed = SUMMARY['b2bMixedGenderSongs_COUNT'].sum()
total_b2b_combined = SUMMARY['b2bCombinedGenderSongs_COUNT'].sum()
# total b2b pairs = sum across all categories (per station)
# instead, use b2b_men + b2b_women + b2b_mixed as approximation of all b2b pairs
# More accurately: sum of any consecutive same-category, but for headline use these three
total_b2b_any = total_b2b_women + total_b2b_men + total_b2b_mixed
print(f"Total songs: {total_songs:,}")
print(f"b2b women count: {total_b2b_women:,}")
print(f"b2b men count: {total_b2b_men:,}")
print(f"b2b mixed-gender count: {total_b2b_mixed:,}")
print(f"b2b women % of all songs: {100*total_b2b_women/total_songs:.2f}%")
print(f"b2b men % of all songs: {100*total_b2b_men/total_songs:.2f}%")
print(f"b2b women % of b2b pairs (women+men+mixed): {100*total_b2b_women/total_b2b_any:.2f}%")
print(f"b2b men % of b2b pairs (women+men+mixed): {100*total_b2b_men/total_b2b_any:.2f}%")
print(f"ratio men:women in b2b: {total_b2b_men/total_b2b_women:.1f}x")
# average per-station rates
mean_b2b_women_pct = SUMMARY['b2bWomenSongs_PERCENT'].mean()
mean_b2b_men_pct   = SUMMARY['b2bMenSongs_PERCENT'].mean()
print(f"mean station b2b women %: {mean_b2b_women_pct:.2f}%")
print(f"mean station b2b men %: {mean_b2b_men_pct:.2f}%")

# --- ana_02: Overall airplay share by gender ---
print("\n=== ana_02 ===")
total_only_women = SUMMARY['onlyWomenSongs_COUNT'].sum()
total_only_men   = SUMMARY['onlyMenSongs_COUNT'].sum()
total_only_mixed = SUMMARY['onlyMixedGenderSongs_COUNT'].sum()
print(f"women airplay share: {100*total_only_women/total_songs:.2f}%")
print(f"men airplay share: {100*total_only_men/total_songs:.2f}%")
print(f"mixed airplay share: {100*total_only_mixed/total_songs:.2f}%")
print(f"women count: {total_only_women:,}")
print(f"men count: {total_only_men:,}")
print(f"mixed count: {total_only_mixed:,}")

# --- ana_03: Station ranking by women's b2b % ---
print("\n=== ana_03 ===")
rank = SUMMARY[['cityName','stationName','ownerName','b2bWomenSongs_PERCENT',
                'b2bMenSongs_PERCENT','onlyWomenSongs_PERCENT','total_COUNT',
                'b2bWomenSongs_COUNT']].copy()
rank = rank.sort_values('b2bWomenSongs_PERCENT', ascending=False).reset_index(drop=True)
print("Station ranking by b2b women %:")
print(rank.to_string(index=False))

# --- ana_04: Daypart distribution of women's b2b plays ---
print("\n=== ana_04 ===")
# Sum across all stations
ovn = SUMMARY['b2bOVNwomenSongs_COUNT'].sum()
amd = SUMMARY['b2bAMDwomenSongs_COUNT'].sum()
mid = SUMMARY['b2bMIDwomenSongs_COUNT'].sum()
pmd = SUMMARY['b2bPMDwomenSongs_COUNT'].sum()
eve = SUMMARY['b2bEVEwomenSongs_COUNT'].sum()
total_dp = ovn + amd + mid + pmd + eve
print(f"b2b women OVN (12am-6am): {ovn} ({100*ovn/total_dp:.1f}%)")
print(f"b2b women AMD (6-10am):   {amd} ({100*amd/total_dp:.1f}%)")
print(f"b2b women MID (10-3pm):   {mid} ({100*mid/total_dp:.1f}%)")
print(f"b2b women PMD (3-7pm):    {pmd} ({100*pmd/total_dp:.1f}%)")
print(f"b2b women EVE (7pm-12am): {eve} ({100*eve/total_dp:.1f}%)")
print(f"OVN + EVE off-peak share: {100*(ovn+eve)/total_dp:.1f}%")
print(f"AMD + PMD drive-time share: {100*(amd+pmd)/total_dp:.1f}%")

# --- ana_05: Owner-level comparison ---
print("\n=== ana_05 ===")
own = SUMMARY.groupby('ownerName').agg(
    n_stations=('stationName','count'),
    total_songs=('total_COUNT','sum'),
    b2b_women=('b2bWomenSongs_COUNT','sum'),
    only_women=('onlyWomenSongs_COUNT','sum'),
    b2b_men=('b2bMenSongs_COUNT','sum'),
).reset_index()
own['women_airplay_pct'] = 100*own['only_women']/own['total_songs']
own['b2b_women_pct'] = 100*own['b2b_women']/own['total_songs']
own['b2b_men_pct'] = 100*own['b2b_men']/own['total_songs']
own = own.sort_values('b2b_women_pct')
print(own.to_string(index=False))

# --- ana_06: Coin-flip significance test (p-values) ---
print("\n=== ana_06 ===")
# pval == 0 means observed b2b women count <= ALL 1000 simulated counts
# Pudding flagged anything below the 95% range
sig = PVALS.copy()
n_sig_women = (sig['pval_women'] < 0.05).sum()
print(f"Stations with p<0.05 for women under-pairing: {n_sig_women} / {len(sig)}")
print(f"Stations with p==0 (observed below ALL 1000 sims): {(sig['pval_women']==0).sum()}")
sig_sorted = sig.sort_values(['pval_women','stationName']).reset_index(drop=True)
print("All stations p-values:")
print(sig_sorted.to_string(index=False))

# --- ana_07: Catalogue type - Gold/Recurrent/Current b2b women ---
print("\n=== ana_07 ===")
g = SUMMARY['b2bGwomenSongs_COUNT'].sum()
r = SUMMARY['b2bRwomenSongs_COUNT'].sum()
c = SUMMARY['b2bCwomenSongs_COUNT'].sum()
total_grc = g + r + c
print(f"b2b women Gold: {g} ({100*g/total_grc:.1f}%)")
print(f"b2b women Recurrent: {r} ({100*r/total_grc:.1f}%)")
print(f"b2b women Current: {c} ({100*c/total_grc:.1f}%)")

# --- ana_08: POC (artists of color) representation ---
print("\n=== ana_08 ===")
poc_men   = SUMMARY['onlyPOCMenSongs_COUNT'].sum()
poc_women = SUMMARY['onlyPOCWomenSongs_COUNT'].sum()
poc_mixed = SUMMARY['onlyPOCMixedSongs_COUNT'].sum()
poc_total = poc_men + poc_women + poc_mixed
b2b_poc_men   = SUMMARY['b2bPOCMenSongs_COUNT'].sum()
b2b_poc_women = SUMMARY['b2bPOCWomenSongs_COUNT'].sum()
b2b_poc_mixed = SUMMARY['b2bPOCMixedSongs_COUNT'].sum()
white_men   = SUMMARY['onlyWhiteMenSongs_COUNT'].sum()
white_women = SUMMARY['onlyWhiteWomenSongs_COUNT'].sum()
b2b_white_women = SUMMARY['b2bWhiteWomenSongs_COUNT'].sum()
print(f"POC overall airplay share: {100*poc_total/total_songs:.2f}%")
print(f"POC men airplay: {poc_men} ({100*poc_men/total_songs:.2f}%)")
print(f"POC women airplay: {poc_women} ({100*poc_women/total_songs:.4f}%)")
print(f"POC mixed airplay: {poc_mixed} ({100*poc_mixed/total_songs:.2f}%)")
print(f"b2b POC men: {b2b_poc_men} ({100*b2b_poc_men/total_songs:.4f}%)")
print(f"b2b POC women: {b2b_poc_women} ({100*b2b_poc_women/total_songs:.4f}%)")
print(f"b2b POC mixed: {b2b_poc_mixed} ({100*b2b_poc_mixed/total_songs:.4f}%)")
# Of total women airplay
print(f"white women / all women airplay: {100*white_women/total_only_women:.2f}%")
print(f"POC women / all women airplay: {100*poc_women/total_only_women:.2f}%")
print(f"white women b2b: {b2b_white_women}, POC women b2b: {b2b_poc_women}")

# --- ana_09: Variance across days ---
print("\n=== ana_09 ===")
day_pct = DAYSUM.groupby('date')['b2bWomenSongs_PERCENT'].agg(['mean','min','max','std']).reset_index()
print("Across all 19 dates, daily mean b2b women %:")
print(day_pct.to_string(index=False))
print(f"Best day mean: {day_pct['mean'].max():.2f}% on {day_pct.loc[day_pct['mean'].idxmax(),'date']}")
print(f"Worst day mean: {day_pct['mean'].min():.2f}% on {day_pct.loc[day_pct['mean'].idxmin(),'date']}")

# --- ana_10: Best vs worst station - extreme contrast ---
print("\n=== ana_10 ===")
best = rank.iloc[0]
worst = rank.iloc[-1]
print(f"BEST b2b-women: {best['cityName']} {best['stationName']} ({best['ownerName']}) {best['b2bWomenSongs_PERCENT']:.2f}%")
print(f"WORST b2b-women: {worst['cityName']} {worst['stationName']} ({worst['ownerName']}) {worst['b2bWomenSongs_PERCENT']:.4f}%")
print(f"Ratio: {best['b2bWomenSongs_PERCENT']/max(worst['b2bWomenSongs_PERCENT'],0.001):.0f}x")

# --- ana_11: Average gap (men b2b % minus women b2b %) per station ---
print("\n=== ana_11 ===")
gap = SUMMARY[['cityName','stationName','b2bWomenSongs_PERCENT','b2bMenSongs_PERCENT']].copy()
gap['gap'] = gap['b2bMenSongs_PERCENT'] - gap['b2bWomenSongs_PERCENT']
gap = gap.sort_values('gap', ascending=False)
print(gap.head(10).to_string(index=False))
print(f"\nMean station gap: {gap['gap'].mean():.2f}%")
print(f"Min gap: {gap['gap'].min():.2f}%")
print(f"Max gap: {gap['gap'].max():.2f}%")

# --- ana_12: Listening-experience reframe (per station 24-hr) ---
print("\n=== ana_12 ===")
# average per-station: in one day how many b2b women vs men do you hear
# total_count is over multiple days though, divide by 19 days approximate
days_sampled = DAYSUM['date'].nunique()
print(f"Days sampled: {days_sampled}")
exp = SUMMARY.copy()
exp['per_day_total']      = exp['total_COUNT'] / days_sampled
exp['per_day_b2b_women']  = exp['b2bWomenSongs_COUNT'] / days_sampled
exp['per_day_b2b_men']    = exp['b2bMenSongs_COUNT'] / days_sampled
print(f"Mean per-day b2b women per station: {exp['per_day_b2b_women'].mean():.2f}")
print(f"Mean per-day b2b men per station:   {exp['per_day_b2b_men'].mean():.2f}")
print(f"Mean per-day total songs per station: {exp['per_day_total'].mean():.1f}")

# Simple 24-hr listener experience (across all stations averaged)
total_b2b_w_per_day = total_b2b_women / days_sampled / len(SUMMARY)
total_b2b_m_per_day = total_b2b_men / days_sampled / len(SUMMARY)
print(f"In a single 24-hr listen at the average station: ~{total_b2b_w_per_day:.1f} b2b-women, ~{total_b2b_m_per_day:.0f} b2b-men")

# Save data tables
import json
out = {
    'rank_table': rank.to_dict('records'),
    'daypart': {'OVN':int(ovn),'AMD':int(amd),'MID':int(mid),'PMD':int(pmd),'EVE':int(eve)},
    'owner': own.to_dict('records'),
    'pvals': sig_sorted.to_dict('records'),
    'grc': {'Gold':int(g),'Recurrent':int(r),'Current':int(c)},
    'gap_top10': gap.head(10).to_dict('records'),
    'day_pct': day_pct.to_dict('records'),
}
print("\n=== meta done ===")
