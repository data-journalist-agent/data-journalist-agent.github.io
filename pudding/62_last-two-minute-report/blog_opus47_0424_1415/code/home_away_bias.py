"""Home vs away team bias analysis."""
import pandas as pd

df = pd.read_parquet('/tmp/l2m_clean.parquet')

# For each call, who benefited / was hurt?
# disadvantaged_team = team that was hurt by the decision
# committing_team = team that committed (or would have committed) the foul

# Flag home/away role
def team_is_home(row, team_col):
    return row[team_col] == row['home']

df['dis_is_home'] = df.apply(lambda r: r['disadvantaged_team'] == r['home'], axis=1)
df['com_is_home'] = df.apply(lambda r: r['committing_team'] == r['home'], axis=1)

# --- ana_08: who gets disadvantaged more — home or away? (by review_decision type) ---
print("=== ana_08 ===")
# For IC (incorrect calls — wrongful whistle), the disadvantaged party is the team unfairly called against
# For INC (incorrect non-calls — missed whistle), the disadvantaged party is the team that deserved a foul called for them
# So in both error types: a "disadvantaged = home" means the home team got hurt by the error

errors = df[df['review_decision'].isin(['IC', 'INC'])].copy()
errors = errors.dropna(subset=['disadvantaged_team'])
errors_home_hurt = (errors['disadvantaged_team'] == errors['home']).sum()
errors_away_hurt = (errors['disadvantaged_team'] == errors['away']).sum()
total_errors = errors_home_hurt + errors_away_hurt
print(f"Total errors with known disadvantaged team: {total_errors}")
print(f"Home team hurt by error:  {errors_home_hurt} ({errors_home_hurt/total_errors*100:.2f}%)")
print(f"Away team hurt by error:  {errors_away_hurt} ({errors_away_hurt/total_errors*100:.2f}%)")
print(f"Delta (away - home): {errors_away_hurt - errors_home_hurt} extra errors hurting away teams")

# Split by error type
for etype in ['IC', 'INC']:
    sub = errors[errors['review_decision'] == etype]
    home_hurt = (sub['disadvantaged_team'] == sub['home']).sum()
    away_hurt = (sub['disadvantaged_team'] == sub['away']).sum()
    tot = home_hurt + away_hurt
    print(f"\n{etype}: total={tot}")
    print(f"  home hurt: {home_hurt} ({home_hurt/tot*100:.2f}%)")
    print(f"  away hurt: {away_hurt} ({away_hurt/tot*100:.2f}%)")
# end ana_08

# --- ana_09: correct calls — no bias expected ---
print("\n=== ana_09 ===")
correct = df[df['review_decision'].isin(['CC', 'CNC'])].copy()
correct = correct.dropna(subset=['disadvantaged_team'])
home_dis_correct = (correct['disadvantaged_team'] == correct['home']).sum()
away_dis_correct = (correct['disadvantaged_team'] == correct['away']).sum()
tot = home_dis_correct + away_dis_correct
print(f"Correct decisions where disadvantaged team known: {tot}")
print(f"  home 'disadvantaged': {home_dis_correct} ({home_dis_correct/tot*100:.2f}%)")
print(f"  away 'disadvantaged': {away_dis_correct} ({away_dis_correct/tot*100:.2f}%)")
print("\n(For reference — baseline split of disadvantaged-team occurrences in correct calls.)")
# end ana_09
