"""Bloc voting and reciprocity analysis from eurovision-votes.csv."""
import pandas as pd
import numpy as np

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/14_eurovision"
votes = pd.read_csv(f"{DATA_DIR}/eurovision-votes.csv")

# Restrict to grand finals (semi_final == 'f' means final). Use final scores only.
final_votes = votes[votes.semi_final == "f"].copy()
# Remove self-votes (which appear with duplicate=='x' in the data when emitted)
final_votes = final_votes[final_votes.from_country != final_votes.to_country].copy()

# --- ana_07: Top 12-point recipients all-time ---
print("=== ana_07 ===")
twelves = final_votes[final_votes.points == 12]
top12 = twelves.to_country.value_counts().head(15)
print(top12.to_string())
print(f"unique recipients of 12-points: {twelves.to_country.nunique()}")
print(f"total 12-point allocations in finals: {len(twelves)}")

# --- ana_08: Greece <-> Cyprus, Turkey -> Germany etc bilateral pairs ---
print("=== ana_08 ===")
# count of times A gives 12 points to B
pair = (
    final_votes.groupby(["from_country", "to_country"])
    .agg(twelves=("points", lambda s: (s == 12).sum()),
         opportunities=("points", "count"),
         total_points=("points", "sum"))
    .reset_index()
)
pair["twelve_rate_pct"] = (pair["twelves"] / pair["opportunities"] * 100).round(1)
# top 20 most reliable 12-point pairs (need at least 5 opportunities)
top_pairs = pair[pair.opportunities >= 5].sort_values("twelves", ascending=False).head(25)
print(top_pairs.to_string(index=False))

# --- ana_09: Reciprocal 12-point pairs (mutual gifting) ---
print("=== ana_09 ===")
# build a frame of (A,B) -> twelves(A->B), invert and merge
twelve_to = pair.set_index(["from_country", "to_country"]).twelves
recip = []
seen = set()
for (a, b), n_ab in twelve_to.items():
    if (b, a) in seen:
        continue
    n_ba = twelve_to.get((b, a), 0)
    if n_ab >= 3 and n_ba >= 3:
        recip.append((a, b, int(n_ab), int(n_ba), int(n_ab) + int(n_ba)))
    seen.add((a, b))
recip_df = pd.DataFrame(recip, columns=["country_a", "country_b", "a_to_b_12s", "b_to_a_12s", "total"]).sort_values("total", ascending=False)
print(recip_df.head(20).to_string(index=False))

# --- ana_10: Mean points awarded between bloc neighbors ---
print("=== ana_10 ===")
NORDIC = {"Sweden", "Norway", "Denmark", "Finland", "Iceland"}
EX_YUGO = {"Croatia", "Slovenia", "North Macedonia", "Macedonia", "F.Y.R. Macedonia",
           "Bosnia & Herzegovina", "Serbia", "Montenegro", "Yugoslavia",
           "Serbia & Montenegro"}
EX_SOVIET = {"Russia", "Ukraine", "Belarus", "Estonia", "Latvia", "Lithuania",
             "Moldova", "Armenia", "Azerbaijan", "Georgia"}
GREEK_PAIR = {"Greece", "Cyprus"}
BLOCS = {"Nordic": NORDIC, "Ex-Yugoslav": EX_YUGO, "Ex-Soviet": EX_SOVIET, "Greek-Cypriot": GREEK_PAIR}

def label_bloc(c):
    for name, members in BLOCS.items():
        if c in members:
            return name
    return None

final_votes["from_bloc"] = final_votes.from_country.map(label_bloc)
final_votes["to_bloc"] = final_votes.to_country.map(label_bloc)
final_votes["same_bloc"] = (
    (final_votes.from_bloc == final_votes.to_bloc)
    & final_votes.from_bloc.notna()
)
in_bloc = final_votes[final_votes.same_bloc].points.mean()
out_bloc = final_votes[~final_votes.same_bloc].points.mean()
print(f"in-bloc mean points: {in_bloc:.3f}")
print(f"out-of-bloc mean points: {out_bloc:.3f}")
print(f"ratio in/out: {in_bloc/out_bloc:.2f}")

# Per-bloc breakdown
rows = []
for name, members in BLOCS.items():
    sub = final_votes[(final_votes.from_country.isin(members)) & (final_votes.to_country.isin(members))]
    out_sub = final_votes[(final_votes.from_country.isin(members)) & (~final_votes.to_country.isin(members))]
    if len(sub) and len(out_sub):
        rows.append((name, len(members), sub.points.mean(), out_sub.points.mean(), len(sub), len(out_sub)))
print("Per-bloc:")
print(pd.DataFrame(rows, columns=["bloc", "size", "in_mean_pts", "out_mean_pts", "in_n", "out_n"]).to_string(index=False))

# --- ana_11: Pre-2009 vs post-2009 bloc-voting magnitude ---
print("=== ana_11 ===")
final_votes["era"] = np.where(final_votes.year < 2009, "pre-2009 reform", "post-2009 reform")
g = final_votes.groupby(["era", "same_bloc"]).points.mean().unstack()
print(g.to_string())

# --- ana_12: Greece <-> Cyprus 12-point streak per year ---
print("=== ana_12 ===")
gc = final_votes[
    ((final_votes.from_country == "Greece") & (final_votes.to_country == "Cyprus")) |
    ((final_votes.from_country == "Cyprus") & (final_votes.to_country == "Greece"))
]
yearly = gc.groupby(["year", "from_country"]).points.first().unstack(fill_value=None)
print(yearly.to_string())
both12 = ((yearly.get("Greece") == 12) & (yearly.get("Cyprus") == 12)).sum()
yrs_both = ((yearly.get("Greece").notna()) & (yearly.get("Cyprus").notna())).sum()
print(f"Years both competed in final and traded points: {yrs_both}")
print(f"Years both gave each other 12: {both12}")
