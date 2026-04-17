"""
04_compatibility.py
Checks whether the 4 filtered datasets can be merged or should
answer different research questions independently. 
"""

import os
import pandas as pd

FILTERED_DIR = os.path.join("data", "filtered")
os.makedirs("outputs", exist_ok=True)

# load filtered datasets
print("Loading filtered datasets...")
ds = {}
for name in ["screen_time_attention_productivity",
             "student_habits_exam_performance",
             "student_social_media_academic_impact",
             "social_media_attention_mental_health_survey"]:
    path = os.path.join(FILTERED_DIR, f"{name}_filtered.csv")
    ds[name] = pd.read_csv(path)
    print(f"  {name}: {len(ds[name])} rows")

df1 = ds["screen_time_attention_productivity"]
df2 = ds["student_habits_exam_performance"]
df3 = ds["student_social_media_academic_impact"]
df4 = ds["social_media_attention_mental_health_survey"]

report = "# Dataset Compatibility Analysis — Stage 4\n\n"
report += "> Assessing whether the four filtered datasets can be combined or should answer different RQs independently.\n\n---\n\n"

# ---- 1. Usage measurement ----
report += "## 1. Usage Measurement Harmonisation\n\n"
report += "### How each dataset measures usage\n\n"
report += "| Dataset | Column | Format | Range |\n"
report += "|---------|--------|--------|-------|\n"
report += "| screen_time | `Average Screen Time` | Categorical bins | Less than 2 → More than 10 (hours/day) |\n"
report += "| student_habits | `social_media_hours` | Continuous float | 0–7.2 hours/day |\n"
report += "| student_academic | `Avg_Daily_Usage_Hours` | Continuous float | 1.5–8.5 hours/day |\n"
report += "| survey | `Daily Time` | Categorical bins | Less than an Hour → More than 5 hours |\n\n"

# midpoint conversion tables
report += "### Bin midpoint conversion\n\n"
report += "For the categorical datasets, we can convert bins to numeric midpoints for approximate analysis.\n\n"

report += "**DS1 — `Average Screen Time`:**\n\n"
report += "| Bin | Midpoint (h/day) |\n|-----|:----------------:|\n"
ds1_map = {"Less than 2": 1.0, "2–4": 3.0, "4–6": 5.0, "6–8": 7.0, "8-10": 9.0, "More than 10": 11.0}
for label, mid in ds1_map.items():
    report += f"| {label} | {mid} |\n"

report += "\n**DS4 — `Daily Time`:**\n\n"
report += "| Bin | Midpoint (h/day) |\n|-----|:----------------:|\n"
ds4_map = {
    "Less than an Hour": 0.5, "Between 1 and 2 hours": 1.5,
    "Between 2 and 3 hours": 2.5, "Between 3 and 4 hours": 3.5,
    "Between 4 and 5 hours": 4.5, "More than 5 hours": 6.0,
}
for label, mid in ds4_map.items():
    report += f"| {label} | {mid} |\n"

# compute converted means
df1_mid = df1["Average Screen Time"].map(ds1_map)
df4_mid = df4["Daily Time"].map(ds4_map)

report += f"\nAfter conversion: DS1 mean ≈ {df1_mid.mean():.2f} h/day | DS4 mean ≈ {df4_mid.mean():.2f} h/day\n\n"

report += "### Cross-dataset comparison\n\n"
report += "| Dataset | Mean (h/day) | Median (h/day) | Max |\n"
report += "|---------|:-----------:|:--------------:|-----|\n"
report += f"| DS1 (midpoints) | {df1_mid.mean():.2f} | {df1_mid.median():.1f} | 11.0 (capped) |\n"
report += f"| DS2 (continuous) | {df2['social_media_hours'].mean():.2f} | {df2['social_media_hours'].median():.1f} | {df2['social_media_hours'].max()} |\n"
report += f"| DS3 (continuous) | {df3['Avg_Daily_Usage_Hours'].mean():.2f} | {df3['Avg_Daily_Usage_Hours'].median():.1f} | {df3['Avg_Daily_Usage_Hours'].max()} |\n"
report += f"| DS4 (midpoints) | {df4_mid.mean():.2f} | {df4_mid.median():.1f} | 6.0 (capped) |\n\n"

report += "> **Key finding:** DS1 usage levels are much higher than the others — it may capture all screen time, not just social media. Direct numeric comparison across datasets is misleading. Within-dataset correlations are valid, but effect sizes should not be pooled.\n\n"

report += "### Information lost in bin conversion\n\n"
report += "- Within-bin variance is zeroed (everyone in '4–6 hours' gets 5.0)\n"
report += "- Top-bin cap is arbitrary ('More than 10' could be 10.5 or 18)\n"
report += "- DS1 uses 2-hour bins, DS4 uses 1-hour bins — unequal precision\n"
report += "- Acceptable for ordinal analysis (Spearman), not for pooled regression\n\n"

# python code
report += "```python\n"
report += "# Midpoint conversion code\n"
report += f"usage_map_ds1 = {ds1_map}\n"
report += "df1['usage_hours_midpoint'] = df1['Average Screen Time'].map(usage_map_ds1)\n\n"
report += f"usage_map_ds4 = {ds4_map}\n"
report += "df4['usage_hours_midpoint'] = df4['Daily Time'].map(usage_map_ds4)\n"
report += "```\n\n---\n\n"

# ---- 2. Attention measurement ----
report += "## 2. Attention / Cognitive Measurement\n\n"
report += "| Dataset | Column(s) | Type | Scale |\n"
report += "|---------|-----------|------|-------|\n"
report += "| screen_time | `Attention Span` | Ordinal | 4 categories: <10 min → >1 hr |\n"
report += "| student_habits | **None** | — | — |\n"
report += "| student_academic | **None** | — | — |\n"
report += "| survey | Q10, Q12, Q14 + `attention_composite` | Likert | 1–5 per item; composite 3–15 |\n\n"

report += "DS1 and DS4 both measure attention, but differently:\n"
report += "- DS1 asks about the *duration* you can sustain focus (behavioural framing)\n"
report += "- DS4 asks about *frequency* of distraction and concentration difficulty (experiential framing)\n\n"
report += "These are related constructs but not directly comparable across datasets. "
report += "Treat them as converging evidence for the same underlying concept.\n\n"

report += "DS2 and DS3 have **no attention measure**. This means RQ2's full chain "
report += "(usage → attention → performance) cannot be tested in a single dataset. "
report += "We answer it in two legs: Leg A (usage → attention) in DS4, Leg B (usage → grades) in DS2.\n\n"

# ordinal encoding
report += "```python\n"
report += "# Attention ordinal encoding for DS1\n"
report += "attention_map_ds1 = {\n"
report += "    'Less than 10 minutes': 1,\n"
report += "    '10–30 minutes': 2,\n"
report += "    '30–60 minutes': 3,\n"
report += "    'More than 1 hour': 4,\n"
report += "}\n"
report += "df1['attention_ordinal'] = df1['Attention Span'].map(attention_map_ds1)\n\n"
report += "# Attention composite for DS4 (already created in stage 3)\n"
report += "# attention_composite = Q10 + Q12 + Q14 (3-15, higher = more distracted)\n"
report += "# attention_score = 16 - attention_composite (higher = better focus)\n"
report += "```\n\n---\n\n"

# ---- 3. Productivity / academic measurement ----
report += "## 3. Productivity / Academic Measurement\n\n"
report += "| Dataset | Column | Type | Scale |\n"
report += "|---------|--------|------|-------|\n"
report += "| screen_time | `Productivity` | Ordinal | Unproductive / Moderate / Extremely productive |\n"
report += "| student_habits | `exam_score` | Continuous | 18.4–100 |\n"
report += "| student_academic | `Affects_Academic_Performance` | Binary | Yes/No |\n"
report += "| survey | **None** | — | — |\n\n"

report += "Three different operationalisations — can't merge them, but they each answer "
report += "a different angle of RQ2.\n\n"

report += "```python\n"
report += "# Productivity ordinal encoding for DS1\n"
report += "prod_map = {\n"
report += "    'Unproductive, i might not have completed the task and got carried away': 1,\n"
report += "    'Moderately productive': 2,\n"
report += "    'Extremely productive, i efficiently complete my tasks': 3,\n"
report += "}\n"
report += "df1['productivity_ordinal'] = df1['Productivity'].map(prod_map)\n\n"
report += "# Binary academic impact for DS3\n"
report += "df3['academic_impact_binary'] = (df3['Affects_Academic_Performance'] == 'Yes').astype(int)\n"
report += "```\n\n---\n\n"

# ---- 4. Platform / short-form ----
report += "## 4. Platform / Short-Form Content Coverage (RQ3)\n\n"
report += "| Dataset | Platform column | Short-form distinguishable? |\n"
report += "|---------|----------------|:--------------------------:|\n"
report += "| screen_time | `App Category` | **No** — all social media lumped together |\n"
report += "| student_habits | **None** | **No** |\n"
report += "| student_academic | `Most_Used_Platform` | **Yes** — TikTok, Instagram identified |\n"
report += "| survey | `Platforms` | **Partial** — comma-separated, parseable |\n\n"

# DS3 platform distribution
report += "### DS3 — Most Used Platform\n\n"
report += "| Platform | n | % |\n|----------|--:|--:|\n"
for val, cnt in df3["Most_Used_Platform"].value_counts().items():
    report += f"| {val} | {cnt} | {cnt/len(df3)*100:.1f}% |\n"

shortform_n = df3["Most_Used_Platform"].isin(["TikTok", "Instagram"]).sum()
report += f"\nShort-form primary users (TikTok or Instagram): **{shortform_n} / {len(df3)} ({shortform_n/len(df3)*100:.1f}%)**\n\n"

# DS4 platform parsing
report += "### DS4 — Platform Indicators (parsed from comma-separated list)\n\n"
platforms_to_check = ["TikTok", "Instagram", "YouTube", "Facebook", "Twitter", "Snapchat"]
report += "| Platform | n users | % |\n|----------|--------:|--:|\n"
for p in platforms_to_check:
    n = df4["Platforms"].str.contains(p, na=False).sum()
    report += f"| {p} | {n} | {n/len(df4)*100:.1f}% |\n"

any_sf = (df4["Platforms"].str.contains("TikTok", na=False) |
          df4["Platforms"].str.contains("Instagram", na=False)).sum()
report += f"| Any short-form (TikTok OR Instagram) | {any_sf} | {any_sf/len(df4)*100:.1f}% |\n\n"

report += "> **Limitation:** DS4 captures which platforms someone uses (presence/absence), not which one they spend the most time on. Noisier than DS3's single primary platform.\n\n"

report += "### Recommended RQ3 approach\n\n"
report += "Primary: DS3 — create binary `is_shortform_primary` (TikTok or Instagram as primary platform) "
report += "and compare `Addicted_Score`, `Affects_Academic_Performance` across groups.\n\n"
report += "Supporting: DS4 — binary TikTok/Instagram indicators as covariates in attention models.\n\n"

report += "```python\n"
report += "# Short-form indicator for DS3\n"
report += "df3['is_shortform_primary'] = df3['Most_Used_Platform'].isin(['TikTok', 'Instagram']).astype(int)\n\n"
report += "# Multi-hot platform indicators for DS4\n"
report += "for platform in ['TikTok', 'Instagram', 'YouTube', 'Facebook', 'Twitter', 'Snapchat']:\n"
report += "    df4[f'uses_{platform.lower()}'] = df4['Platforms'].str.contains(platform, na=False).astype(int)\n"
report += "df4['has_shortform'] = ((df4['uses_tiktok'] == 1) | (df4['uses_instagram'] == 1)).astype(int)\n"
report += "```\n\n---\n\n"

# ---- 5. Merge feasibility ----
report += "## 5. Merge Feasibility\n\n"
report += "### Why merging is not feasible\n\n"
report += "1. **No common participant identifier** — four independent surveys, different respondent pools\n"
report += "2. **Incompatible column schemas** — even 'usage hours' is measured in different bins/scales\n"
report += "3. **Different constructs** — DS1 measures screen time effects, DS2 measures lifestyle vs exam outcomes, "
report += "DS3 measures platform adoption and academic impact, DS4 measures distraction via Likert items\n\n"

report += "### Strategy: triangulation, not merging\n\n"
report += "Each RQ is answered by its best-fit dataset, with findings compared across datasets for convergent validity.\n\n"

report += "| RQ | Primary Dataset | Supporting |\n"
report += "|----|----------------|------------|\n"
report += "| RQ1: Usage → attention + productivity | screen_time | survey (attention); student_habits (productivity) |\n"
report += "| RQ2: Higher usage → reduced attention → lower performance | Leg A: survey (usage → attention); Leg B: student_habits (usage → exam_score) | student_academic (binary academic impact) |\n"
report += "| RQ3: Short-form content impact | student_academic (primary platform) | survey (platform indicators) |\n\n"

# derived variables summary
report += "### Derived variables to create\n\n"
report += "| Variable | Dataset | Definition |\n"
report += "|----------|---------|------------|\n"
report += "| `usage_hours_midpoint` | DS1, DS4 | Numeric midpoint of usage bin |\n"
report += "| `attention_ordinal` | DS1 | 1–4 encoding of Attention Span |\n"
report += "| `attention_composite` | DS4 | Q10 + Q12 + Q14 (3–15, higher = more distracted) |\n"
report += "| `attention_score` | DS4 | 16 − attention_composite (higher = better focus) |\n"
report += "| `productivity_ordinal` | DS1 | 1–3 encoding of Productivity |\n"
report += "| `academic_impact_binary` | DS3 | 1 if Affects_Academic_Performance == 'Yes' |\n"
report += "| `is_shortform_primary` | DS3 | 1 if Most_Used_Platform in {TikTok, Instagram} |\n"
report += "| `uses_tiktok`, `uses_instagram` | DS4 | 1 if platform in Platforms list |\n"
report += "| `has_shortform` | DS4 | 1 if uses TikTok OR Instagram |\n\n"

report += "---\n"

with open("outputs/04_compatibility.md", "w", encoding="utf-8") as f:
    f.write(report)

print("\nDone — saved to outputs/04_compatibility.md")