"""Player-level advantage and disadvantage analysis."""
import pandas as pd

df = pd.read_parquet('/tmp/l2m_clean.parquet')

# For each player we compute:
#   disadvantaged_count: appearances as disadvantaged_player (the player who was hurt)
#   committing_count: appearances as committing_player (fouler)
# Error-specific:
#   disadvantaged_by_error (IC or INC): player got a raw deal
#   advantaged_by_error (IC/INC committed by them but not penalized, or a wrong call on opponent)

dis = df['disadvantaged_player'].value_counts()
com = df['committing_player'].value_counts()

# For errors only
errs = df[df['review_decision'].isin(['IC', 'INC'])].copy()
# In an IC (wrong whistle): committing player was wrongly penalized, disadvantaged player got a wrong benefit
# In an INC (missed whistle): committing player got away with it (advantaged), disadvantaged player got hurt
# We care about the disadvantaged side — who loses from referee errors?

dis_err = errs['disadvantaged_player'].value_counts()
com_err = errs['committing_player'].value_counts()

# --- ana_10: players most often flagged as disadvantaged (by errors) ---
print("=== ana_10 ===")
# Require at least 100 L2M appearances total to avoid small-sample noise
total_appear = dis.add(com, fill_value=0)
high_volume = total_appear[total_appear >= 100].index.tolist()

net = pd.DataFrame({
    'total_apps': total_appear,
    'disadvantaged_err': dis_err,
    'committed_err': com_err,
}).loc[high_volume].fillna(0)
net['net_disadvantage'] = net['disadvantaged_err'] - net['committed_err']
net = net.sort_values('net_disadvantage', ascending=False)

print("TOP 15 players with most net-disadvantage from L2M errors (disadvantaged_err - committed_err):")
print(f"{'player':25s} {'apps':>5s} {'dis_err':>8s} {'com_err':>8s} {'net':>5s}")
for player, row in net.head(15).iterrows():
    print(f"{player:25s} {int(row['total_apps']):5d} {int(row['disadvantaged_err']):8d} {int(row['committed_err']):8d} {int(row['net_disadvantage']):5d}")

print("\nBOTTOM 15 (net-advantaged — they commit more errors than they're hurt by):")
for player, row in net.tail(15).iterrows():
    print(f"{player:25s} {int(row['total_apps']):5d} {int(row['disadvantaged_err']):8d} {int(row['committed_err']):8d} {int(row['net_disadvantage']):5d}")
# end ana_10

# --- ana_11: most frequently appearing players in L2M ---
print("\n=== ana_11 ===")
print("Top 15 players by total L2M appearances:")
top_apps = total_appear.sort_values(ascending=False).head(15)
for p, v in top_apps.items():
    print(f"  {p:25s} {int(v):5d}")
# end ana_11
