# Dataset Compatibility Analysis — Stage 4

> Assessing whether the four filtered datasets can be meaningfully combined,
> or whether each should answer different research questions independently.

---

## RQ-to-Dataset Mapping (Summary)

| Research Question | Primary Dataset | Supporting Datasets | Merge Feasible? |
|-------------------|----------------|---------------------|:---------------:|
| **RQ1** — Social media use → attention span & productivity | `screen_time_attention_productivity` | `survey` (attention); `student_habits` (productivity) | No — triangulate |
| **RQ2** — Higher usage → reduced attention → lower academic performance | `survey` (attention path) + `student_habits` (performance path) | `student_academic` (binary academic impact) | No — answer in two legs |
| **RQ3** — Short-form content impact | `student_academic` (primary platform column) | `survey` (platform list, parseable) | No — compare findings |

---

## 1. Usage Measurement Harmonisation

### 1.1 Usage Columns by Dataset

| Dataset | Column | Format | Range / Categories |
|---------|--------|--------|-------------------|
| `screen_time_attention_productivity` | `Average Screen Time` | Categorical bins | Less than 2, 2–4, 4–6, 6–8, 8–10, More than 10 (hours/day) |
| `student_habits_exam_performance` | `social_media_hours` | Continuous float | 0–7.2 hours/day (mean 2.51, median 2.5) |
| `student_social_media_academic_impact` | `Avg_Daily_Usage_Hours` | Continuous float | 1.5–8.5 hours/day (mean 4.92, median 4.8) |
| `social_media_attention_mental_health_survey` | `Daily Time` | Categorical bins | Less than an Hour, Between 1–2, 2–3, 3–4, 4–5, More than 5 (hours/day) |

### 1.2 Proposed Common Scale — Bin Midpoint Conversion

Categorical bins in DS1 and DS4 can be converted to numeric midpoints, 
enabling approximate comparison with the continuous columns in DS2 and DS3. 
Information loss is unavoidable: within-bin variance is erased and the open-ended 
top bins ('More than 10', 'More than 5') require a capped assumption.

**DS1 — `Average Screen Time` → `usage_hours_midpoint`:**

| Bin label | Assigned midpoint (hours/day) | Rationale |
|-----------|:-----------------------------:|-----------|
| Less than 2 | 1.0 | Midpoint of 0–2 |
| 2–4 | 3.0 | Midpoint |
| 4–6 | 5.0 | Midpoint |
| 6–8 | 7.0 | Midpoint |
| 8–10 | 9.0 | Midpoint |
| More than 10 | 11.0 | Conservative cap (could be higher) |

_After conversion: DS1 mean ≈ 6.91 h/day, median ≈ 7.0 h/day_

**DS4 — `Daily Time` → `usage_hours_midpoint`:**

| Bin label | Assigned midpoint (hours/day) | Rationale |
|-----------|:-----------------------------:|-----------|
| Less than an Hour | 0.5 | Midpoint of 0–1 |
| Between 1 and 2 hours | 1.5 | Midpoint |
| Between 2 and 3 hours | 2.5 | Midpoint |
| Between 3 and 4 hours | 3.5 | Midpoint |
| Between 4 and 5 hours | 4.5 | Midpoint |
| More than 5 hours | 6.0 | Conservative cap (survey top bin is lower than DS1) |

_After conversion: DS4 mean ≈ 3.9 h/day, median ≈ 3.5 h/day_

### 1.3 Cross-Dataset Usage Range Comparison

| Dataset | Scale | Approx. mean (h/day) | Approx. median (h/day) | Max |
|---------|-------|:-------------------:|:---------------------:|-----|
| DS1 (midpoints) | Pseudo-continuous | 6.91 | 7.0 | 11.0 (capped) |
| DS2 (continuous) | Continuous float | 2.51 | 2.5 | 7.2 |
| DS3 (continuous) | Continuous float | 4.92 | 4.8 | 8.5 |
| DS4 (midpoints) | Pseudo-continuous | 3.9 | 3.5 | 6.0 (capped) |

> **Interpretation:** DS1 and DS4 usage levels are substantially higher than DS2 and DS3. DS2's max of 7.2 h/day and DS3's max of 8.5 h/day both fall within DS1's bins, but DS1 shows a high concentration in the 6–10+ hour range, suggesting the screen_time survey may have recruited heavy users or captures all screen time (not exclusively social media). These scale differences mean **direct numeric comparison across datasets is misleading** — within-dataset correlations remain valid, but cross-dataset effect sizes cannot be pooled.

### 1.4 Information Lost in Bin Conversion

- **Within-bin variance is zeroed:** all respondents in '4–6 hours' receive midpoint 5.0, regardless of whether they actually spend 4.1 or 5.9 hours online.
- **Top-bin assumption is arbitrary:** 'More than 10 hours' could represent 10.5 or 18 hours — the 11.0 cap is conservative but unverifiable.
- **Different bin widths:** DS4 uses 1-hour bins (higher precision); DS1 uses 2-hour bins. Merging them treats unequal precision as equivalent.
- **Conclusion:** Midpoint conversion is acceptable for **within-dataset ordinal analysis** (e.g., Spearman correlation with attention) but **not** for pooled regression across datasets.

```python
# Derived variable: usage_hours_midpoint
# Apply to DS1
usage_map_ds1 = {
    'Less than 2':  1.0,
    '2–4':         3.0,
    '4–6':         5.0,
    '6–8':         7.0,
    '8-10':         9.0,
    'More than 10': 11.0,
}
df1['usage_hours_midpoint'] = df1['Average Screen Time'].map(usage_map_ds1)

# Apply to DS4
usage_map_ds4 = {
    'Less than an Hour':       0.5,
    'Between 1 and 2 hours':   1.5,
    'Between 2 and 3 hours':   2.5,
    'Between 3 and 4 hours':   3.5,
    'Between 4 and 5 hours':   4.5,
    'More than 5 hours':       6.0,
}
df4['usage_hours_midpoint'] = df4['Daily Time'].map(usage_map_ds4)
```

---

## 2. Attention / Cognitive Measurement Alignment

### 2.1 Attention Columns by Dataset

| Dataset | Column(s) | Measurement type | Scale |
|---------|-----------|-----------------|-------|
| `screen_time_attention_productivity` | `Attention Span` | Self-reported ordinal | 4 categories: <10 min, 10–30 min, 30–60 min, >1 hr |
| `student_habits_exam_performance` | **None** | — | — |
| `student_social_media_academic_impact` | **None** | — | — |
| `social_media_attention_mental_health_survey` | Q10, Q12, Q14 + `attention_composite` | Likert self-report | 1–5 per item; composite 3–15 |

### 2.2 Are DS1 and DS4 Measuring the Same Construct?

Both datasets capture **self-reported attention/concentration difficulty**, but they operationalise the construct differently:

- **DS1 `Attention Span`** asks respondents to select the longest duration they can sustain focus on a task (behavioural-duration framing). It is a single item with four ordered categories, yielding an ordinal variable. In the filtered sample, 16.2% report less than 10 minutes and 23.8% report more than 1 hour.

- **DS4 Q10/Q12/Q14** ask about distraction frequency and difficulty concentrating on a 1–5 Likert scale (experiential-frequency framing). These three items can be summed into an `attention_composite` score (range 3–15, higher = more distracted). In the filtered sample the composite mean is 10.49 (SD=3.07), with item means Q10=3.51, Q12=3.5, Q14=3.47.

The two measures are **theoretically related but operationally distinct**: duration-of-focus (DS1) and distraction-frequency (DS4) are correlated constructs but not identical. A respondent who reports >1 hour attention span (DS1) would plausibly score low on Q10/Q12/Q14 (DS4), but the mapping is not deterministic. **Direct cross-dataset comparison of attention scores is not valid.** They should instead be treated as converging evidence for the same latent construct.

### 2.3 Datasets Without Attention Measures

`student_habits_exam_performance` and `student_social_media_academic_impact` contain **no attention or distraction column**. This has direct implications for the research questions:

- **RQ1** (usage → attention → productivity): DS2 and DS3 can only speak to the usage → productivity/performance leg; the attention mechanism cannot be modelled in either dataset.
- **RQ2** (mediation path: usage → attention → performance): DS2 and DS3 lack the mediator variable. A proper mediation model requires either DS1 or DS4. The analysis will need to be **split across datasets**: use DS4 to establish the usage → attention association, then use DS2 or DS3 to establish the usage → academic performance association separately.

### 2.4 Ordinal Encoding for DS1 Attention Span

```python
# Convert DS1 Attention Span to numeric ordinal for correlation analysis
attention_ordinal_map_ds1 = {
    'Less than 10 minutes': 1,
    '10–30 minutes':       2,
    '30–60 minutes':       3,
    'More than 1 hour':     4,
}
df1['attention_ordinal'] = df1['Attention Span'].map(attention_ordinal_map_ds1)

# DS4: attention composite (already numeric)
df4['attention_composite'] = (df4[Q10] + df4[Q12] + df4[Q14])
# Note: higher composite = more distracted (inverse of DS1 ordinal)
# For consistent direction, invert: attention_score_ds4 = 16 - attention_composite
df4['attention_score'] = 16 - df4['attention_composite']   # higher = better attention
```

---

## 3. Productivity / Academic Outcome Alignment

### 3.1 Outcome Columns by Dataset

| Dataset | Column(s) | Measurement type | Scale |
|---------|-----------|-----------------|-------|
| `screen_time_attention_productivity` | `Productivity` | Self-reported ordinal | 3 categories: Unproductive, Moderately, Extremely productive |
| `student_habits_exam_performance` | `exam_score`, `attendance_percentage` | Objective-proxy continuous | exam_score 0–100; attendance 56–100% |
| `student_social_media_academic_impact` | `Affects_Academic_Performance` (binary), `Addicted_Score` | Binary + ordinal | Yes/No; 1–10 addiction scale |
| `social_media_attention_mental_health_survey` | **None** | — | — |

### 3.2 Can These Be Compared Across Datasets?

The three outcome measures capture related but distinct constructs and **cannot be numerically pooled**:

- **DS1 `Productivity`** is a subjective, global self-assessment of task completion. It is ordinal (3 levels) and confounds productivity with work-context factors (the dataset includes professionals, not only students). Distribution: Unproductive=34 (21.2%), Moderately=89 (55.6%), Extremely=37 (23.1%).

- **DS2 `exam_score`** is the closest proxy to an objective academic outcome, though the dataset is synthetic. It is continuous (18.4–100.0, mean 69.6) and suitable for linear regression. `attendance_percentage` is a complementary behavioural outcome.

- **DS3 `Affects_Academic_Performance`** is a binary self-assessment (Yes/No). 453 of 705 students (64.3%) report that social media affects their academic performance. This is highly susceptible to social desirability bias and lacks directionality (positive or negative effect). `Addicted_Score` (1–10, mean 6.44) is a complementary predictor rather than an outcome variable.

**Practical recommendation:** Treat each outcome as an independent operationalisation. If all three point in the same direction (e.g., higher usage → lower productivity/exam_score/more likely 'Yes' on academic impact), this constitutes **triangulated convergent validity** — a stronger claim than any single dataset alone.

### 3.3 Ordinal and Binary Encoding for Analysis

```python
# DS1 — Productivity ordinal encoding
productivity_map_ds1 = {
    'Unproductive, i might not have completed the task and got carried away': 1,
    'Moderately productive': 2,
    'Extremely productive, i efficiently complete my tasks': 3,
}
df1['productivity_ordinal'] = df1['Productivity'].map(productivity_map_ds1)

# DS3 — Binary academic impact encoding
df3['academic_impact_binary'] = (df3['Affects_Academic_Performance'] == 'Yes').astype(int)
# 1 = social media affects academic performance, 0 = does not
```

---

## 4. Platform / Short-Form Content Coverage (RQ3)

### 4.1 Platform Data by Dataset

| Dataset | Platform column | Short-form distinguishable? | Notes |
|---------|----------------|:---------------------------:|-------|
| `screen_time_attention_productivity` | `App Category` | **No** | Groups all social media into one bin; no platform-level detail |
| `student_habits_exam_performance` | **None** | **No** | No platform column at all |
| `student_social_media_academic_impact` | `Most_Used_Platform` | **Yes** | Single primary platform; TikTok and Instagram identified |
| `social_media_attention_mental_health_survey` | `Platforms` | **Partial** | Comma-separated multi-platform list; parseable into binary indicators |

### 4.2 DS3 — Most Used Platform Distribution

| Platform | n | % |
|----------|--:|--|
| Instagram | 249 | 35.3% |
| TikTok | 154 | 21.8% |
| Facebook | 123 | 17.4% |
| WhatsApp | 54 | 7.7% |
| Twitter | 30 | 4.3% |
| LinkedIn | 21 | 3.0% |
| WeChat | 15 | 2.1% |
| Snapchat | 13 | 1.8% |
| LINE | 12 | 1.7% |
| KakaoTalk | 12 | 1.7% |
| VKontakte | 12 | 1.7% |
| YouTube | 10 | 1.4% |

Short-form primary users (TikTok or Instagram as most-used): **403 / 705 (57.2%)**

### 4.3 DS4 — Platform Indicator Parsing

From the comma-separated `Platforms` field (n=339):

| Platform | n users | % |
|----------|--------:|--|
| TikTok | 77 | 22.7% |
| Instagram | 279 | 82.3% |
| YouTube | 298 | 87.9% |
| Any short-form (TikTok OR Instagram) | 280 | 82.6% |

> **Limitation:** DS4 captures platforms used (presence/absence) but not which platform the user spends the *most* time on. A respondent who lists both TikTok and YouTube cannot be classified as a short-form-primary user. This makes DS4 weaker than DS3 for RQ3, where platform-as-primary-activity is more meaningful.

### 4.4 DS1 — App Category Limitation

DS1's `App Category` column bundles all social media (Facebook, Instagram, LinkedIn, Twitter) into a single 'Social Media' category, with no TikTok or Reels distinction. 90 of 160 filtered respondents (56.2%) selected 'Social Media' as their primary app category. **RQ3 cannot be answered using DS1** — it provides no short-form vs. long-form granularity.

### 4.5 Recommended RQ3 Approach

**Primary dataset for RQ3: `student_social_media_academic_impact`** — it is the only dataset where each respondent's *primary* platform is identified, enabling a clean TikTok/Instagram (short-form) vs. Facebook/WhatsApp/Twitter (longer-form) comparison against `Affects_Academic_Performance` and `Addicted_Score`.

**Supporting dataset: `social_media_attention_mental_health_survey`** — binary TikTok/Instagram indicators can be used as covariates in attention models, though the 'any-use' framing is noisier than 'primary platform'.

**Proposed RQ3 analysis:** In DS3, create a `shortform_user` binary variable (TikTok or Instagram as primary platform) and compare `Addicted_Score`, `Affects_Academic_Performance`, and `Mental_Health_Score` across groups using Mann-Whitney U tests and logistic regression.

```python
# DS3 — Short-form binary indicator
shortform_platforms = ['TikTok', 'Instagram']
df3['is_shortform_primary'] = df3['Most_Used_Platform'].isin(shortform_platforms).astype(int)
# 1 = TikTok or Instagram primary user, 0 = other platform

# DS4 — Multi-hot platform indicators
for platform in ['TikTok', 'Instagram', 'YouTube', 'Facebook', 'Twitter', 'Snapchat']:
    col = f'uses_{platform.lower()}'
    df4[col] = df4['Platforms'].str.contains(platform, na=False).astype(int)

# DS4 — Any short-form user flag
df4['has_shortform'] = ((df4['uses_tiktok'] == 1) | (df4['uses_instagram'] == 1)).astype(int)
```

---

## 5. Merge Feasibility

### 5.1 Why a Row-Level Merge Is Not Feasible

A row-level merge (stacking or joining datasets into a single analytic file) is **not feasible** for three structural reasons:

1. **No common participant identifier.** The four datasets are entirely independent surveys with different respondent pools collected at different times and contexts. There is no shared ID, email, or timestamp linking any row in one dataset to any row in another.

2. **Incompatible column schemas.** Across all four datasets there is no column that is measured in the same instrument, at the same scale, in a comparable population. Even 'usage hours/day', which appears in all four, uses different bins, different recall windows, and likely different reference activities (all screen time vs. social media only).

3. **Different constructs being measured.** DS1 measures screen-time effects on productivity and attention. DS2 measures student lifestyle vs. exam outcomes. DS3 measures social media adoption and self-reported academic impact. DS4 measures distraction and mental health via structured survey items. Pooling them would conflate incompatible operationalisations of the same underlying constructs.

### 5.2 Recommended Strategy: Triangulation Across Datasets

Rather than merging, each research question should be answered primarily by the dataset with the best variable coverage, and the findings triangulated against other datasets for convergent validity:


| RQ | Primary Dataset | Why | Supporting Datasets |
|----|----------------|-----|---------------------|
| **RQ1**: Usage → attention + productivity | `screen_time_attention_productivity` | Only dataset with both `Attention Span` and `Productivity` alongside usage | `survey` (attention path only); `student_habits` (productivity/exam path only) |
| **RQ2**: Higher usage → reduced attention → lower performance | Leg A: `survey` (usage → attention); Leg B: `student_habits` (usage → exam_score) | No single dataset covers the full mediation path | `student_academic` supports Leg B via `Affects_Academic_Performance` |
| **RQ3**: Short-form content impact | `student_social_media_academic_impact` | Only dataset with per-respondent primary platform; enables clean short-form vs. other comparison | `survey` (multi-hot platform flags as covariates) |

### 5.3 What 'Triangulation' Means in Practice

If DS1 shows higher screen time is associated with shorter attention span, and DS4 independently shows higher daily time is associated with higher attention_composite (more distracted), these are **convergent findings from independent instruments** — a stronger evidential basis than either alone. If they diverge, this is itself a finding worth reporting (construct validity differs across populations or measurement approaches). In either case, the findings should be presented per-dataset with explicit caveats about comparability, rather than aggregated into a single effect estimate.

### 5.4 Derived Variables Summary

The following derived variables should be created before analysis:


| Variable | Dataset | Definition | Python snippet |
|----------|---------|------------|----------------|
| `usage_hours_midpoint` | DS1, DS4 | Numeric midpoint of usage bin | See Section 1 code |
| `attention_ordinal` | DS1 | 1–4 encoding of `Attention Span` | See Section 2 code |
| `attention_composite` | DS4 | Q10 + Q12 + Q14 (3–15, higher = more distracted) | See Section 2 code |
| `attention_score` | DS4 | 16 − attention_composite (higher = better focus) | See Section 2 code |
| `productivity_ordinal` | DS1 | 1–3 encoding of `Productivity` | See Section 3 code |
| `academic_impact_binary` | DS3 | 1 if `Affects_Academic_Performance` == 'Yes' | See Section 3 code |
| `is_shortform_primary` | DS3 | 1 if `Most_Used_Platform` in {TikTok, Instagram} | See Section 4 code |
| `uses_tiktok` / `uses_instagram` | DS4 | 1 if platform appears in `Platforms` list | See Section 4 code |
| `has_shortform` | DS4 | 1 if uses TikTok OR Instagram | See Section 4 code |

---
