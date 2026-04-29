"""Sepsis bundle (SEP_1) and stroke / opioid / cataract / colonoscopy measures."""
import pandas as pd
from pathlib import Path

DATA = Path('/Users/forrest/Desktop/data2blog/data_pkg/tidytuesday/12_timely-and-effective-care-by-us-state/care_state.csv')
df = pd.read_csv(DATA)


# --- ana_18: SEP_1 sepsis bundle ---
print("=== ana_18 ===")
sep = df[df.measure_id == 'SEP_1'].dropna(subset=['score']).copy()
print(f"reporting: {len(sep)}")
print(sep.score.describe().round(1))
sep_sorted = sep.sort_values('score', ascending=False)
print('top 5 SEP_1:')
print(sep_sorted[['state','score']].head(5).to_string(index=False))
print('bottom 5:')
print(sep_sorted[['state','score']].tail(5).to_string(index=False))

# --- ana_19: All process measures side by side (national medians, ranges) ---
print("\n=== ana_19 ===")
process_ids = [
    'SEP_1',
    'SEV_SEP_3HR', 'SEV_SEP_6HR',
    'SEP_SH_3HR', 'SEP_SH_6HR',
    'OP_22', 'OP_23',
    'OP_29', 'OP_31',
    'SAFE_USE_OF_OPIOIDS',
    'IMM_3', 'HCP_COVID_19',
]
labels = {
    'SEP_1': 'Sepsis bundle',
    'SEV_SEP_3HR': 'Severe sepsis 3-hr bundle',
    'SEV_SEP_6HR': 'Severe sepsis 6-hr bundle',
    'SEP_SH_3HR': 'Septic shock 3-hr bundle',
    'SEP_SH_6HR': 'Septic shock 6-hr bundle',
    'OP_22': 'Left ED before being seen',
    'OP_23': 'Stroke CT/MRI in 45 min',
    'OP_29': 'Colonoscopy follow-up rec',
    'OP_31': 'Cataract vision improved',
    'SAFE_USE_OF_OPIOIDS': 'Safe opioid co-prescribing',
    'IMM_3': 'HCW flu vaccination',
    'HCP_COVID_19': 'HCW COVID up-to-date',
}
direction = {  # higher_better=True or lower_better=False
    'SEP_1': True, 'SEV_SEP_3HR': True, 'SEV_SEP_6HR': True,
    'SEP_SH_3HR': True, 'SEP_SH_6HR': True,
    'OP_22': False, 'OP_23': True,
    'OP_29': True, 'OP_31': True,
    'SAFE_USE_OF_OPIOIDS': False,
    'IMM_3': True, 'HCP_COVID_19': True,
}
rows = []
for mid in process_ids:
    sub = df[df.measure_id == mid].dropna(subset=['score'])
    rows.append({
        'measure_id': mid,
        'label': labels[mid],
        'higher_better': direction[mid],
        'n': len(sub),
        'min': round(sub.score.min(), 1),
        'median': round(sub.score.median(), 1),
        'mean': round(sub.score.mean(), 1),
        'max': round(sub.score.max(), 1),
    })
out = pd.DataFrame(rows)
print(out.to_string(index=False))


# --- ana_20: SEP_1 vs HCP_COVID_19 correlation (process-care quality consistency check) ---
print("\n=== ana_20 ===")
sep_s = sep.set_index('state')['score']
covid = df[df.measure_id == 'HCP_COVID_19'].dropna(subset=['score'])
covid_s = covid.set_index('state')['score']
m = pd.concat({'sep1': sep_s, 'covid': covid_s}, axis=1).dropna()
print(f"Pearson r = {m['sep1'].corr(m['covid']):.3f} (n={len(m)})")


# --- ana_21: SAFE_USE_OF_OPIOIDS distribution ---
print("\n=== ana_21 ===")
op = df[df.measure_id == 'SAFE_USE_OF_OPIOIDS'].dropna(subset=['score']).copy()
print(f"reporting: {len(op)}, mean: {op.score.mean():.2f}%, median: {op.score.median():.2f}%")
print('top 5 (lower better — fewest concurrent opioid+benzo prescriptions):')
print(op.sort_values('score').head(5)[['state','score']].to_string(index=False))
print('bottom 5:')
print(op.sort_values('score', ascending=False).head(5)[['state','score']].to_string(index=False))


# --- ana_22: Five-group taxonomy (rows-per-group breakdown) ---
print("\n=== ana_22 ===")
groups = {
    'ED flow': ['OP_18b','OP_18b_LOW_MIN','OP_18b_MEDIUM_MIN','OP_18b_HIGH_MIN','OP_18b_VERY_HIGH_MIN',
                'OP_18c','OP_18c_LOW_MIN','OP_18c_MEDIUM_MIN','OP_18c_HIGH_MIN','OP_18c_VERY_HIGH_MIN',
                'OP_22','OP_23'],
    'Vaccination': ['HCP_COVID_19','IMM_3'],
    'Sepsis': ['SEP_1','SEV_SEP_3HR','SEV_SEP_6HR','SEP_SH_3HR','SEP_SH_6HR'],
    'Outpatient procedures': ['OP_29','OP_31'],
    'Pharmacy safety': ['SAFE_USE_OF_OPIOIDS'],
}
total_measures = 0
for g, mids in groups.items():
    print(f"  {g}: {len(mids)} measures")
    total_measures += len(mids)
print(f"  TOTAL: {total_measures} unique measure_ids")
