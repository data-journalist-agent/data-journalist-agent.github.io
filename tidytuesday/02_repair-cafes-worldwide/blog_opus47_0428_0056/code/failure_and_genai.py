"""Failure-reason taxonomy + GenAI vs YouTube as repair info source."""
import pandas as pd
import numpy as np
import re

repairs = pd.read_pickle("/tmp/repairs_aug.pkl")
text = pd.read_pickle("/tmp/repairs_text_clean.pkl")
joined = repairs.merge(text, on="repair_id", how="left")
total = len(joined)

# --- ana_13: Failure reasons taxonomy (multi-label list) ---
print("=== ana_13 ===")
not_fixed = joined[joined["_outcome"].isin(["not_fixed", "partial_or_eol"])]
print(f"Rows where not fully fixed: {len(not_fixed):,}")
print(f"With non-null failure_reasons: {not_fixed['failure_reasons'].notna().sum():,}")
# Reasons are comma-separated lists
all_reasons = []
for raw in not_fixed["failure_reasons"].dropna():
    parts = [p.strip() for p in str(raw).split(",")]
    for p in parts:
        if p and p.lower() != "na":
            all_reasons.append(p)
reason_counts = pd.Series(all_reasons).value_counts()
print(f"Total reason mentions: {len(all_reasons):,}")
print(f"Unique reason strings: {reason_counts.size}")
print("Top failure reasons:")
print(reason_counts.head(20))
# Pct of failed repairs that mention each reason
denom = not_fixed["failure_reasons"].notna().sum()
print("As % of failed/partial reports with non-null reason:")
top_pct = (reason_counts.head(15) / denom * 100).round(2)
print(top_pct)

# --- ana_14: GenAI vs YouTube as info source ---
print("=== ana_14 ===")
# Combine repair_info_source + repair_info_url + repair_method (sometimes mentioned there)
def text_blob(row):
    parts = []
    for c in ["repair_info_source", "repair_info_url", "repair_method", "suggestions"]:
        v = row.get(c)
        if isinstance(v, str):
            parts.append(v.lower())
    return " ".join(parts)

joined["_info_blob"] = joined.apply(text_blob, axis=1)

# Keyword buckets
genai_kw = re.compile(r"\b(chatgpt|gpt|openai|gemini|bard|claude|copilot|genai|gen ai|generative ai|llm|bing chat|perplexity)\b")
youtube_kw = re.compile(r"\byoutube|youtu\.be\b")
manual_kw = re.compile(r"\bmanual|user guide|instruction|datasheet|service manual|handleiding|manuel|bedienungsanleitung\b")
forum_kw = re.compile(r"\bforum|reddit|stackexchange|community\b")
ifixit_kw = re.compile(r"ifixit")
google_kw = re.compile(r"\bgoogle|search engine|web search\b")
own_kw = re.compile(r"own knowledge|experience|colleague|team|expertise")

joined["src_genai"] = joined["_info_blob"].str.contains(genai_kw, na=False, regex=True)
joined["src_youtube"] = joined["_info_blob"].str.contains(youtube_kw, na=False, regex=True)
joined["src_manual"] = joined["_info_blob"].str.contains(manual_kw, na=False, regex=True)
joined["src_forum"] = joined["_info_blob"].str.contains(forum_kw, na=False, regex=True)
joined["src_ifixit"] = joined["_info_blob"].str.contains(ifixit_kw, na=False, regex=True)
joined["src_google"] = joined["_info_blob"].str.contains(google_kw, na=False, regex=True)

# Filter rows where ANY info-source field has content
has_source = (joined["repair_info_source"].notna() | joined["repair_info_url"].notna())
print(f"Rows with any info source field: {has_source.sum():,}")

# Aggregate counts overall
print("Overall mention counts:")
for k in ["src_youtube", "src_manual", "src_genai", "src_forum", "src_ifixit", "src_google"]:
    print(f"  {k}: {joined[k].sum():,}")

# By year — focus on 2022 onwards (ChatGPT launched Nov 2022)
joined["year"] = joined["year"].fillna(0).astype(int)
yrs = sorted(joined["year"].unique())
print("By year — counts:")
yr_table = []
for y in yrs:
    if y < 2018 or y > 2026: continue
    sub = joined[joined["year"] == y]
    n = len(sub)
    yt = sub["src_youtube"].sum()
    ai = sub["src_genai"].sum()
    mn = sub["src_manual"].sum()
    yr_table.append((y, n, int(yt), int(ai), int(mn)))
    print(f"  {y}: rows={n:,} youtube={yt} genai={ai} manual={mn}")

# Examples of GenAI mentions
ex = joined[joined["src_genai"]].head(10)[["year", "repair_info_source", "repair_info_url", "repair_method"]]
print("Sample GenAI mentions:")
for _, r in ex.iterrows():
    print(f"  {r['year']} | source={r['repair_info_source']} | url={r['repair_info_url']}")

# --- ana_15: used_repair_info distribution ---
print("=== ana_15 ===")
ur = joined["used_repair_info"].fillna("(missing)").str.lower().str.strip()
print(ur.value_counts())

# --- ana_16: Failure reason vs category cross-tab — top 5 categories x top 5 reasons ---
print("=== ana_16 ===")
top_cats = joined["category"].value_counts().head(6).index.tolist()
top_reasons = reason_counts.head(8).index.tolist()
def in_reasons(raw, target):
    if not isinstance(raw, str): return False
    parts = [p.strip() for p in raw.split(",")]
    return target in parts
crosstab = []
for cat in top_cats:
    nf_cat = joined[(joined["category"] == cat) & joined["_outcome"].isin(["not_fixed", "partial_or_eol"])]
    n_cat = len(nf_cat)
    row = {"category": cat, "failed_total": n_cat}
    for r in top_reasons:
        cnt = nf_cat["failure_reasons"].apply(lambda x: in_reasons(x, r)).sum()
        row[r] = int(cnt)
        row[r + "_pct"] = round(100 * cnt / n_cat, 2) if n_cat else 0
    crosstab.append(row)
ctdf = pd.DataFrame(crosstab)
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
print(ctdf)

# Save
joined.to_pickle("/tmp/joined.pkl")

# --- ana_17: cumulative successful repairs and CO2 estimate ---
print("=== ana_17 ===")
fixed_total = (repairs["_outcome"] == "fixed").sum()
print(f"Total successful repairs in dataset: {fixed_total:,}")
# Restart Project headline figure: ~24 kg CO2e per fixed electrical/electronic item (class-weighted)
# Source: detective det_10. Apply ONLY to electrical/electronic categories.
elec_cats = ["Household appliances electric", "Display and sound equipment", "Tools electric",
             "Computer equipment / phones", "Toys electric", "Clocks / alarm clocks"]
elec_fixed = repairs[(repairs["_outcome"] == "fixed") & (repairs["category"].isin(elec_cats))].shape[0]
print(f"Electrical/electronic successful repairs: {elec_fixed:,}")
print(f"CO2e avoided estimate (24 kg/repair): {elec_fixed * 24 / 1000:.1f} tonnes")
print(f"CO2e avoided estimate range (10-40 kg/repair): {elec_fixed*10/1000:.1f}-{elec_fixed*40/1000:.1f} tonnes")
