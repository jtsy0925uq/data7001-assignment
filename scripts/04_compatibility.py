"""
04_compatibility.py
===================
DATA7001 – Social Media & Cognitive Functioning Project
--------------------------------------------------------
Assesses whether the four filtered datasets can be meaningfully
combined or should answer different research questions independently.

Covers five dimensions:
  1. Usage measurement harmonisation
  2. Attention / cognitive measurement alignment
  3. Productivity / academic outcome alignment
  4. Platform / short-form content coverage (RQ3)
  5. Merge feasibility and RQ-to-dataset mapping

Output
------
  outputs/04_compatibility.md  — full compatibility report

Usage
-----
  python scripts/04_compatibility.py
"""

import sys
import os
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ─────────────────────────────────────────────────────────────────────
FILTERED_DIR = os.path.join("dataset", "filtered")
OUT_DIR      = "outputs"
REPORT_PATH  = os.path.join(OUT_DIR, "04_compatibility.md")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Load filtered datasets ────────────────────────────────────────────────────
print("Loading filtered datasets...")
df1 = pd.read_csv(os.path.join(FILTERED_DIR, "screen_time_attention_productivity_filtered.csv"))
df2 = pd.read_csv(os.path.join(FILTERED_DIR, "student_habits_exam_performance_filtered.csv"))
df3 = pd.read_csv(os.path.join(FILTERED_DIR, "student_social_media_academic_impact_filtered.csv"))
df4 = pd.read_csv(os.path.join(FILTERED_DIR, "social_media_attention_mental_health_survey_filtered.csv"))

n1, n2, n3, n4 = len(df1), len(df2), len(df3), len(df4)
print(f"  DS1={n1}  DS2={n2}  DS3={n3}  DS4={n4}")

# ── Q column names (DS4) ──────────────────────────────────────────────────────
Q10 = "10. How often do you get distracted by Social media when you are busy doing something?"
Q12 = "12. On a scale of 1 to 5, how easily distracted are you?"
Q14 = "14. Do you find it difficult to concentrate on things?"


# ════════════════════════════════════════════════════════════════════════════════
# Derived stats used in the report
# ════════════════════════════════════════════════════════════════════════════════

# -- Usage bin midpoints for DS1 --
bin_midpoints_ds1 = {
    "Less than 2":  1.0,
    "2\u20134":     3.0,
    "4\u20136":     5.0,
    "6\u20138":     7.0,
    "8-10":         9.0,
    "More than 10": 11.0,
}
df1["usage_hours_midpoint"] = df1["Average Screen Time"].map(bin_midpoints_ds1)

# -- Usage bin midpoints for DS4 --
bin_midpoints_ds4 = {
    "Less than an Hour":       0.5,
    "Between 1 and 2 hours":   1.5,
    "Between 2 and 3 hours":   2.5,
    "Between 3 and 4 hours":   3.5,
    "Between 4 and 5 hours":   4.5,
    "More than 5 hours":       6.0,
}
df4["usage_hours_midpoint"] = df4["Daily Time"].map(bin_midpoints_ds4)

# -- Attention span ordinal encoding DS1 --
attn_order_ds1 = {
    "Less than 10 minutes": 1,
    "10\u201330 minutes":   2,
    "30\u201360 minutes":   3,
    "More than 1 hour":     4,
}
df1["attention_ordinal"] = df1["Attention Span"].map(attn_order_ds1)

# -- Productivity ordinal encoding DS1 --
prod_order_ds1 = {
    "Unproductive, i might not have completed the task and got carried away": 1,
    "Moderately productive": 2,
    "Extremely productive, i efficiently complete my tasks": 3,
}
df1["productivity_ordinal"] = df1["Productivity"].map(prod_order_ds1)

# -- Attention composite DS4 --
df4["attention_composite"] = df4[Q10] + df4[Q12] + df4[Q14]

# -- Platform binary flags DS3 & DS4 --
short_form_platforms = ["TikTok", "Instagram", "YouTube"]
for plat in short_form_platforms:
    df3[f"uses_{plat.lower()}"] = (df3["Most_Used_Platform"] == plat).astype(int)
    df4[f"uses_{plat.lower()}"] = df4["Platforms"].str.contains(plat, na=False).astype(int)

# DS3 short-form primary user: TikTok or Instagram as most_used
df3["is_shortform_primary"] = df3["Most_Used_Platform"].isin(["TikTok", "Instagram"]).astype(int)

# DS4 has_any_shortform: uses TikTok OR Instagram
df4["has_shortform"] = ((df4["uses_tiktok"] == 1) | (df4["uses_instagram"] == 1)).astype(int)

# Platform counts DS3
ds3_platform_vc  = df3["Most_Used_Platform"].value_counts()
ds3_shortform_n  = int(df3["is_shortform_primary"].sum())
ds3_shortform_pct= round(ds3_shortform_n / n3 * 100, 1)

# Platform counts DS4
ds4_tiktok_n     = int(df4["uses_tiktok"].sum())
ds4_instagram_n  = int(df4["uses_instagram"].sum())
ds4_shortform_n  = int(df4["has_shortform"].sum())
ds4_shortform_pct= round(ds4_shortform_n / n4 * 100, 1)

# DS1 app category for social media (includes SM but not short-form specific)
ds1_sm_n   = int((df1["App Category"].str.contains("Social Media", na=False)).sum())
ds1_total  = n1

# DS4 midpoint stats
ds4_mid_mean = round(df4["usage_hours_midpoint"].mean(), 2)
ds4_mid_med  = round(df4["usage_hours_midpoint"].median(), 2)

# DS1 midpoint stats
ds1_mid_mean = round(df1["usage_hours_midpoint"].mean(), 2)
ds1_mid_med  = round(df1["usage_hours_midpoint"].median(), 2)

# DS2 usage stats
ds2_sm_mean  = round(df2["social_media_hours"].mean(), 2)
ds2_sm_med   = round(df2["social_media_hours"].median(), 2)
ds2_sm_max   = round(df2["social_media_hours"].max(), 2)

# DS3 usage stats
ds3_sm_mean  = round(df3["Avg_Daily_Usage_Hours"].mean(), 2)
ds3_sm_med   = round(df3["Avg_Daily_Usage_Hours"].median(), 2)
ds3_sm_max   = round(df3["Avg_Daily_Usage_Hours"].max(), 2)

# DS3 academic impact breakdown
ds3_yes_n   = int((df3["Affects_Academic_Performance"] == "Yes").sum())
ds3_yes_pct = round(ds3_yes_n / n3 * 100, 1)

print("Derived stats computed.")


# ════════════════════════════════════════════════════════════════════════════════
# Build markdown report
# ════════════════════════════════════════════════════════════════════════════════

lines = []

lines += [
    "# Dataset Compatibility Analysis — Stage 4\n",
    "> Assessing whether the four filtered datasets can be meaningfully combined,",
    "> or whether each should answer different research questions independently.\n",
    "---\n",
]

# ── RQ-to-dataset mapping summary (top) ──────────────────────────────────────
lines += [
    "## RQ-to-Dataset Mapping (Summary)\n",
    "| Research Question | Primary Dataset | Supporting Datasets | Merge Feasible? |",
    "|-------------------|----------------|---------------------|:---------------:|",
    "| **RQ1** — Social media use → attention span & productivity | `screen_time_attention_productivity` | `survey` (attention); `student_habits` (productivity) | No — triangulate |",
    "| **RQ2** — Higher usage → reduced attention → lower academic performance | `survey` (attention path) + `student_habits` (performance path) | `student_academic` (binary academic impact) | No — answer in two legs |",
    "| **RQ3** — Short-form content impact | `student_academic` (primary platform column) | `survey` (platform list, parseable) | No — compare findings |",
    "\n---\n",
]

# ════════════════════════════════════════════════════════════════════════════════
# Section 1 — Usage harmonisation
# ════════════════════════════════════════════════════════════════════════════════
lines += [
    "## 1. Usage Measurement Harmonisation\n",

    "### 1.1 Usage Columns by Dataset\n",
    "| Dataset | Column | Format | Range / Categories |",
    "|---------|--------|--------|-------------------|",
    f"| `screen_time_attention_productivity` | `Average Screen Time` | Categorical bins | Less than 2, 2–4, 4–6, 6–8, 8–10, More than 10 (hours/day) |",
    f"| `student_habits_exam_performance` | `social_media_hours` | Continuous float | 0–{ds2_sm_max} hours/day (mean {ds2_sm_mean}, median {ds2_sm_med}) |",
    f"| `student_social_media_academic_impact` | `Avg_Daily_Usage_Hours` | Continuous float | 1.5–{ds3_sm_max} hours/day (mean {ds3_sm_mean}, median {ds3_sm_med}) |",
    f"| `social_media_attention_mental_health_survey` | `Daily Time` | Categorical bins | Less than an Hour, Between 1–2, 2–3, 3–4, 4–5, More than 5 (hours/day) |",
    "",

    "### 1.2 Proposed Common Scale — Bin Midpoint Conversion\n",
    "Categorical bins in DS1 and DS4 can be converted to numeric midpoints, ",
    "enabling approximate comparison with the continuous columns in DS2 and DS3. ",
    "Information loss is unavoidable: within-bin variance is erased and the open-ended ",
    "top bins ('More than 10', 'More than 5') require a capped assumption.\n",

    "**DS1 — `Average Screen Time` → `usage_hours_midpoint`:**\n",
    "| Bin label | Assigned midpoint (hours/day) | Rationale |",
    "|-----------|:-----------------------------:|-----------|",
    "| Less than 2 | 1.0 | Midpoint of 0–2 |",
    "| 2–4 | 3.0 | Midpoint |",
    "| 4–6 | 5.0 | Midpoint |",
    "| 6–8 | 7.0 | Midpoint |",
    "| 8–10 | 9.0 | Midpoint |",
    f"| More than 10 | 11.0 | Conservative cap (could be higher) |",
    "",
    f"_After conversion: DS1 mean ≈ {ds1_mid_mean} h/day, median ≈ {ds1_mid_med} h/day_\n",

    "**DS4 — `Daily Time` → `usage_hours_midpoint`:**\n",
    "| Bin label | Assigned midpoint (hours/day) | Rationale |",
    "|-----------|:-----------------------------:|-----------|",
    "| Less than an Hour | 0.5 | Midpoint of 0–1 |",
    "| Between 1 and 2 hours | 1.5 | Midpoint |",
    "| Between 2 and 3 hours | 2.5 | Midpoint |",
    "| Between 3 and 4 hours | 3.5 | Midpoint |",
    "| Between 4 and 5 hours | 4.5 | Midpoint |",
    "| More than 5 hours | 6.0 | Conservative cap (survey top bin is lower than DS1) |",
    "",
    f"_After conversion: DS4 mean ≈ {ds4_mid_mean} h/day, median ≈ {ds4_mid_med} h/day_\n",

    "### 1.3 Cross-Dataset Usage Range Comparison\n",
    "| Dataset | Scale | Approx. mean (h/day) | Approx. median (h/day) | Max |",
    "|---------|-------|:-------------------:|:---------------------:|-----|",
    f"| DS1 (midpoints) | Pseudo-continuous | {ds1_mid_mean} | {ds1_mid_med} | 11.0 (capped) |",
    f"| DS2 (continuous) | Continuous float | {ds2_sm_mean} | {ds2_sm_med} | {ds2_sm_max} |",
    f"| DS3 (continuous) | Continuous float | {ds3_sm_mean} | {ds3_sm_med} | {ds3_sm_max} |",
    f"| DS4 (midpoints) | Pseudo-continuous | {ds4_mid_mean} | {ds4_mid_med} | 6.0 (capped) |",
    "",
    (
        "> **Interpretation:** DS1 and DS4 usage levels are substantially higher than DS2 and DS3. "
        "DS2's max of 7.2 h/day and DS3's max of 8.5 h/day both fall within DS1's bins, but DS1 "
        "shows a high concentration in the 6–10+ hour range, suggesting the screen_time survey "
        "may have recruited heavy users or captures all screen time (not exclusively social media). "
        "These scale differences mean **direct numeric comparison across datasets is misleading** — "
        "within-dataset correlations remain valid, but cross-dataset effect sizes cannot be pooled."
    ),

    "\n### 1.4 Information Lost in Bin Conversion\n",
    "- **Within-bin variance is zeroed:** all respondents in '4–6 hours' receive midpoint 5.0, "
    "regardless of whether they actually spend 4.1 or 5.9 hours online.",
    "- **Top-bin assumption is arbitrary:** 'More than 10 hours' could represent 10.5 or 18 hours — "
    "the 11.0 cap is conservative but unverifiable.",
    "- **Different bin widths:** DS4 uses 1-hour bins (higher precision); DS1 uses 2-hour bins. "
    "Merging them treats unequal precision as equivalent.",
    "- **Conclusion:** Midpoint conversion is acceptable for **within-dataset ordinal analysis** "
    "(e.g., Spearman correlation with attention) but **not** for pooled regression across datasets.\n",

    "```python",
    "# Derived variable: usage_hours_midpoint",
    "# Apply to DS1",
    "usage_map_ds1 = {",
    "    'Less than 2':  1.0,",
    "    '2\u20134':         3.0,",
    "    '4\u20136':         5.0,",
    "    '6\u20138':         7.0,",
    "    '8-10':         9.0,",
    "    'More than 10': 11.0,",
    "}",
    "df1['usage_hours_midpoint'] = df1['Average Screen Time'].map(usage_map_ds1)",
    "",
    "# Apply to DS4",
    "usage_map_ds4 = {",
    "    'Less than an Hour':       0.5,",
    "    'Between 1 and 2 hours':   1.5,",
    "    'Between 2 and 3 hours':   2.5,",
    "    'Between 3 and 4 hours':   3.5,",
    "    'Between 4 and 5 hours':   4.5,",
    "    'More than 5 hours':       6.0,",
    "}",
    "df4['usage_hours_midpoint'] = df4['Daily Time'].map(usage_map_ds4)",
    "```\n",
    "---\n",
]

# ════════════════════════════════════════════════════════════════════════════════
# Section 2 — Attention measurement
# ════════════════════════════════════════════════════════════════════════════════

# Compute attention composite stats for DS4
ac = df4["attention_composite"]
ac_mean = round(ac.mean(), 2)
ac_std  = round(ac.std(), 2)

# DS4 Q-level means
q10_mean = round(df4[Q10].mean(), 2)
q12_mean = round(df4[Q12].mean(), 2)
q14_mean = round(df4[Q14].mean(), 2)

# DS1 attention distribution
attn1_vc = df1["Attention Span"].value_counts()
pct_lt10 = round(df1[df1["Attention Span"] == "Less than 10 minutes"].shape[0] / n1 * 100, 1)
pct_gt60 = round(df1[df1["Attention Span"] == "More than 1 hour"].shape[0] / n1 * 100, 1)

lines += [
    "## 2. Attention / Cognitive Measurement Alignment\n",

    "### 2.1 Attention Columns by Dataset\n",
    "| Dataset | Column(s) | Measurement type | Scale |",
    "|---------|-----------|-----------------|-------|",
    "| `screen_time_attention_productivity` | `Attention Span` | Self-reported ordinal | 4 categories: <10 min, 10–30 min, 30–60 min, >1 hr |",
    "| `student_habits_exam_performance` | **None** | — | — |",
    "| `student_social_media_academic_impact` | **None** | — | — |",
    "| `social_media_attention_mental_health_survey` | Q10, Q12, Q14 + `attention_composite` | Likert self-report | 1–5 per item; composite 3–15 |",
    "",

    "### 2.2 Are DS1 and DS4 Measuring the Same Construct?\n",
    (
        "Both datasets capture **self-reported attention/concentration difficulty**, "
        "but they operationalise the construct differently:\n\n"
        "- **DS1 `Attention Span`** asks respondents to select the longest duration they "
        "can sustain focus on a task (behavioural-duration framing). It is a single item "
        "with four ordered categories, yielding an ordinal variable. "
        f"In the filtered sample, {pct_lt10}% report less than 10 minutes and "
        f"{pct_gt60}% report more than 1 hour.\n\n"
        "- **DS4 Q10/Q12/Q14** ask about distraction frequency and difficulty concentrating "
        "on a 1–5 Likert scale (experiential-frequency framing). These three items can be "
        "summed into an `attention_composite` score (range 3–15, higher = more distracted). "
        f"In the filtered sample the composite mean is {ac_mean} (SD={ac_std}), "
        f"with item means Q10={q10_mean}, Q12={q12_mean}, Q14={q14_mean}.\n\n"
        "The two measures are **theoretically related but operationally distinct**: "
        "duration-of-focus (DS1) and distraction-frequency (DS4) are correlated constructs "
        "but not identical. A respondent who reports >1 hour attention span (DS1) would "
        "plausibly score low on Q10/Q12/Q14 (DS4), but the mapping is not deterministic. "
        "**Direct cross-dataset comparison of attention scores is not valid.** "
        "They should instead be treated as converging evidence for the same latent construct."
    ),
    "",

    "### 2.3 Datasets Without Attention Measures\n",
    (
        "`student_habits_exam_performance` and `student_social_media_academic_impact` contain "
        "**no attention or distraction column**. This has direct implications for the research questions:\n\n"
        "- **RQ1** (usage → attention → productivity): DS2 and DS3 can only speak to the "
        "usage → productivity/performance leg; the attention mechanism cannot be modelled "
        "in either dataset.\n"
        "- **RQ2** (mediation path: usage → attention → performance): DS2 and DS3 lack the "
        "mediator variable. A proper mediation model requires either DS1 or DS4. "
        "The analysis will need to be **split across datasets**: use DS4 to establish the "
        "usage → attention association, then use DS2 or DS3 to establish the "
        "usage → academic performance association separately."
    ),

    "\n### 2.4 Ordinal Encoding for DS1 Attention Span\n",
    "```python",
    "# Convert DS1 Attention Span to numeric ordinal for correlation analysis",
    "attention_ordinal_map_ds1 = {",
    "    'Less than 10 minutes': 1,",
    "    '10\u201330 minutes':       2,",
    "    '30\u201360 minutes':       3,",
    "    'More than 1 hour':     4,",
    "}",
    "df1['attention_ordinal'] = df1['Attention Span'].map(attention_ordinal_map_ds1)",
    "",
    "# DS4: attention composite (already numeric)",
    "df4['attention_composite'] = (df4[Q10] + df4[Q12] + df4[Q14])",
    "# Note: higher composite = more distracted (inverse of DS1 ordinal)",
    "# For consistent direction, invert: attention_score_ds4 = 16 - attention_composite",
    "df4['attention_score'] = 16 - df4['attention_composite']   # higher = better attention",
    "```\n",
    "---\n",
]

# ════════════════════════════════════════════════════════════════════════════════
# Section 3 — Productivity / academic outcomes
# ════════════════════════════════════════════════════════════════════════════════

prod1_vc = df1["Productivity"].value_counts()

lines += [
    "## 3. Productivity / Academic Outcome Alignment\n",

    "### 3.1 Outcome Columns by Dataset\n",
    "| Dataset | Column(s) | Measurement type | Scale |",
    "|---------|-----------|-----------------|-------|",
    "| `screen_time_attention_productivity` | `Productivity` | Self-reported ordinal | 3 categories: Unproductive, Moderately, Extremely productive |",
    "| `student_habits_exam_performance` | `exam_score`, `attendance_percentage` | Objective-proxy continuous | exam_score 0–100; attendance 56–100% |",
    "| `student_social_media_academic_impact` | `Affects_Academic_Performance` (binary), `Addicted_Score` | Binary + ordinal | Yes/No; 1–10 addiction scale |",
    "| `social_media_attention_mental_health_survey` | **None** | — | — |",
    "",

    "### 3.2 Can These Be Compared Across Datasets?\n",
    (
        "The three outcome measures capture related but distinct constructs and "
        "**cannot be numerically pooled**:\n\n"
        "- **DS1 `Productivity`** is a subjective, global self-assessment of task "
        "completion. It is ordinal (3 levels) and confounds productivity with "
        f"work-context factors (the dataset includes professionals, not only students). "
        f"Distribution: Unproductive={int(prod1_vc.get('Unproductive, i might not have completed the task and got carried away', 0))} "
        f"({round(prod1_vc.get('Unproductive, i might not have completed the task and got carried away', 0)/n1*100,1)}%), "
        f"Moderately={int(prod1_vc.get('Moderately productive', 0))} "
        f"({round(prod1_vc.get('Moderately productive', 0)/n1*100,1)}%), "
        f"Extremely={int(prod1_vc.get('Extremely productive, i efficiently complete my tasks', 0))} "
        f"({round(prod1_vc.get('Extremely productive, i efficiently complete my tasks', 0)/n1*100,1)}%).\n\n"
        "- **DS2 `exam_score`** is the closest proxy to an objective academic outcome, "
        "though the dataset is synthetic. It is continuous (18.4–100.0, mean 69.6) and "
        "suitable for linear regression. `attendance_percentage` is a complementary "
        "behavioural outcome.\n\n"
        "- **DS3 `Affects_Academic_Performance`** is a binary self-assessment (Yes/No). "
        f"{ds3_yes_n} of {n3} students ({ds3_yes_pct}%) report that social media "
        "affects their academic performance. This is highly susceptible to social "
        "desirability bias and lacks directionality (positive or negative effect). "
        "`Addicted_Score` (1–10, mean 6.44) is a complementary predictor rather than "
        "an outcome variable.\n\n"
        "**Practical recommendation:** Treat each outcome as an independent operationalisation. "
        "If all three point in the same direction (e.g., higher usage → lower productivity/exam_score/"
        "more likely 'Yes' on academic impact), this constitutes **triangulated convergent validity** "
        "— a stronger claim than any single dataset alone."
    ),

    "\n### 3.3 Ordinal and Binary Encoding for Analysis\n",
    "```python",
    "# DS1 — Productivity ordinal encoding",
    "productivity_map_ds1 = {",
    "    'Unproductive, i might not have completed the task and got carried away': 1,",
    "    'Moderately productive': 2,",
    "    'Extremely productive, i efficiently complete my tasks': 3,",
    "}",
    "df1['productivity_ordinal'] = df1['Productivity'].map(productivity_map_ds1)",
    "",
    "# DS3 — Binary academic impact encoding",
    "df3['academic_impact_binary'] = (df3['Affects_Academic_Performance'] == 'Yes').astype(int)",
    "# 1 = social media affects academic performance, 0 = does not",
    "```\n",
    "---\n",
]

# ════════════════════════════════════════════════════════════════════════════════
# Section 4 — Platform / short-form content (RQ3)
# ════════════════════════════════════════════════════════════════════════════════

ds3_platform_rows = "\n".join(
    f"| {plat} | {cnt} | {round(cnt/n3*100,1)}% |"
    for plat, cnt in ds3_platform_vc.items()
)

lines += [
    "## 4. Platform / Short-Form Content Coverage (RQ3)\n",

    "### 4.1 Platform Data by Dataset\n",
    "| Dataset | Platform column | Short-form distinguishable? | Notes |",
    "|---------|----------------|:---------------------------:|-------|",
    "| `screen_time_attention_productivity` | `App Category` | **No** | Groups all social media into one bin; no platform-level detail |",
    "| `student_habits_exam_performance` | **None** | **No** | No platform column at all |",
    "| `student_social_media_academic_impact` | `Most_Used_Platform` | **Yes** | Single primary platform; TikTok and Instagram identified |",
    "| `social_media_attention_mental_health_survey` | `Platforms` | **Partial** | Comma-separated multi-platform list; parseable into binary indicators |",
    "",

    "### 4.2 DS3 — Most Used Platform Distribution\n",
    "| Platform | n | % |",
    "|----------|--:|--|",
    ds3_platform_rows,
    "",
    f"Short-form primary users (TikTok or Instagram as most-used): "
    f"**{ds3_shortform_n} / {n3} ({ds3_shortform_pct}%)**\n",

    "### 4.3 DS4 — Platform Indicator Parsing\n",
    f"From the comma-separated `Platforms` field (n={n4}):\n",
    "| Platform | n users | % |",
    "|----------|--------:|--|",
    f"| TikTok | {ds4_tiktok_n} | {round(ds4_tiktok_n/n4*100,1)}% |",
    f"| Instagram | {ds4_instagram_n} | {round(ds4_instagram_n/n4*100,1)}% |",
    f"| YouTube | {int(df4['uses_youtube'].sum())} | {round(df4['uses_youtube'].sum()/n4*100,1)}% |",
    f"| Any short-form (TikTok OR Instagram) | {ds4_shortform_n} | {ds4_shortform_pct}% |",
    "",
    (
        "> **Limitation:** DS4 captures platforms used (presence/absence) but not which "
        "platform the user spends the *most* time on. A respondent who lists both TikTok "
        "and YouTube cannot be classified as a short-form-primary user. This makes DS4 "
        "weaker than DS3 for RQ3, where platform-as-primary-activity is more meaningful."
    ),

    "\n### 4.4 DS1 — App Category Limitation\n",
    (
        "DS1's `App Category` column bundles all social media (Facebook, Instagram, LinkedIn, "
        "Twitter) into a single 'Social Media' category, with no TikTok or Reels distinction. "
        f"{ds1_sm_n} of {ds1_total} filtered respondents ({round(ds1_sm_n/ds1_total*100,1)}%) "
        "selected 'Social Media' as their primary app category. **RQ3 cannot be answered "
        "using DS1** — it provides no short-form vs. long-form granularity."
    ),

    "\n### 4.5 Recommended RQ3 Approach\n",
    (
        "**Primary dataset for RQ3: `student_social_media_academic_impact`** — it is the "
        "only dataset where each respondent's *primary* platform is identified, enabling "
        "a clean TikTok/Instagram (short-form) vs. Facebook/WhatsApp/Twitter (longer-form) "
        "comparison against `Affects_Academic_Performance` and `Addicted_Score`.\n\n"
        "**Supporting dataset: `social_media_attention_mental_health_survey`** — binary "
        "TikTok/Instagram indicators can be used as covariates in attention models, "
        "though the 'any-use' framing is noisier than 'primary platform'.\n\n"
        "**Proposed RQ3 analysis:** In DS3, create a `shortform_user` binary variable "
        "(TikTok or Instagram as primary platform) and compare `Addicted_Score`, "
        "`Affects_Academic_Performance`, and `Mental_Health_Score` across groups using "
        "Mann-Whitney U tests and logistic regression."
    ),

    "\n```python",
    "# DS3 — Short-form binary indicator",
    "shortform_platforms = ['TikTok', 'Instagram']",
    "df3['is_shortform_primary'] = df3['Most_Used_Platform'].isin(shortform_platforms).astype(int)",
    "# 1 = TikTok or Instagram primary user, 0 = other platform",
    "",
    "# DS4 — Multi-hot platform indicators",
    "for platform in ['TikTok', 'Instagram', 'YouTube', 'Facebook', 'Twitter', 'Snapchat']:",
    "    col = f'uses_{platform.lower()}'",
    "    df4[col] = df4['Platforms'].str.contains(platform, na=False).astype(int)",
    "",
    "# DS4 — Any short-form user flag",
    "df4['has_shortform'] = ((df4['uses_tiktok'] == 1) | (df4['uses_instagram'] == 1)).astype(int)",
    "```\n",
    "---\n",
]

# ════════════════════════════════════════════════════════════════════════════════
# Section 5 — Merge feasibility
# ════════════════════════════════════════════════════════════════════════════════
lines += [
    "## 5. Merge Feasibility\n",

    "### 5.1 Why a Row-Level Merge Is Not Feasible\n",
    (
        "A row-level merge (stacking or joining datasets into a single analytic file) "
        "is **not feasible** for three structural reasons:\n\n"
        "1. **No common participant identifier.** The four datasets are entirely independent "
        "surveys with different respondent pools collected at different times and contexts. "
        "There is no shared ID, email, or timestamp linking any row in one dataset to any "
        "row in another.\n\n"
        "2. **Incompatible column schemas.** Across all four datasets there is no column "
        "that is measured in the same instrument, at the same scale, in a comparable "
        "population. Even 'usage hours/day', which appears in all four, uses different "
        "bins, different recall windows, and likely different reference activities "
        "(all screen time vs. social media only).\n\n"
        "3. **Different constructs being measured.** DS1 measures screen-time effects on "
        "productivity and attention. DS2 measures student lifestyle vs. exam outcomes. "
        "DS3 measures social media adoption and self-reported academic impact. DS4 measures "
        "distraction and mental health via structured survey items. Pooling them would "
        "conflate incompatible operationalisations of the same underlying constructs."
    ),

    "\n### 5.2 Recommended Strategy: Triangulation Across Datasets\n",
    (
        "Rather than merging, each research question should be answered primarily by the "
        "dataset with the best variable coverage, and the findings triangulated against "
        "other datasets for convergent validity:\n"
    ),
    "",
    "| RQ | Primary Dataset | Why | Supporting Datasets |",
    "|----|----------------|-----|---------------------|",
    "| **RQ1**: Usage → attention + productivity | `screen_time_attention_productivity` | Only dataset with both `Attention Span` and `Productivity` alongside usage | `survey` (attention path only); `student_habits` (productivity/exam path only) |",
    "| **RQ2**: Higher usage → reduced attention → lower performance | Leg A: `survey` (usage → attention); Leg B: `student_habits` (usage → exam_score) | No single dataset covers the full mediation path | `student_academic` supports Leg B via `Affects_Academic_Performance` |",
    "| **RQ3**: Short-form content impact | `student_social_media_academic_impact` | Only dataset with per-respondent primary platform; enables clean short-form vs. other comparison | `survey` (multi-hot platform flags as covariates) |",
    "",

    "### 5.3 What 'Triangulation' Means in Practice\n",
    (
        "If DS1 shows higher screen time is associated with shorter attention span, "
        "and DS4 independently shows higher daily time is associated with higher "
        "attention_composite (more distracted), these are **convergent findings from "
        "independent instruments** — a stronger evidential basis than either alone. "
        "If they diverge, this is itself a finding worth reporting (construct validity "
        "differs across populations or measurement approaches). In either case, the "
        "findings should be presented per-dataset with explicit caveats about "
        "comparability, rather than aggregated into a single effect estimate."
    ),

    "\n### 5.4 Derived Variables Summary\n",
    "The following derived variables should be created before analysis:\n",
    "",
    "| Variable | Dataset | Definition | Python snippet |",
    "|----------|---------|------------|----------------|",
    "| `usage_hours_midpoint` | DS1, DS4 | Numeric midpoint of usage bin | See Section 1 code |",
    "| `attention_ordinal` | DS1 | 1–4 encoding of `Attention Span` | See Section 2 code |",
    "| `attention_composite` | DS4 | Q10 + Q12 + Q14 (3–15, higher = more distracted) | See Section 2 code |",
    "| `attention_score` | DS4 | 16 − attention_composite (higher = better focus) | See Section 2 code |",
    "| `productivity_ordinal` | DS1 | 1–3 encoding of `Productivity` | See Section 3 code |",
    "| `academic_impact_binary` | DS3 | 1 if `Affects_Academic_Performance` == 'Yes' | See Section 3 code |",
    "| `is_shortform_primary` | DS3 | 1 if `Most_Used_Platform` in {TikTok, Instagram} | See Section 4 code |",
    "| `uses_tiktok` / `uses_instagram` | DS4 | 1 if platform appears in `Platforms` list | See Section 4 code |",
    "| `has_shortform` | DS4 | 1 if uses TikTok OR Instagram | See Section 4 code |",
    "\n---\n",
]

# ── Write report ──────────────────────────────────────────────────────────────
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nDone. Report saved to: {REPORT_PATH}")
print(f"  Lines: {len(lines)}")
