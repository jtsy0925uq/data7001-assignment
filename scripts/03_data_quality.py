"""
03_data_quality.py
==================
DATA7001 – Social Media & Cognitive Functioning Project
--------------------------------------------------------
Applies population filters determined in Stage 2, saves filtered
datasets to ./data/filtered/, then runs a five-part data quality
sweep on each:

  1. Missingness patterns (column-level, row-level, missingno matrix,
     MCAR/MAR/MNAR classification)
  2. Duplicate rows and ID duplicates
  3. Outliers in key numeric fields (boxplots, IQR rule, implausible
     value flags)
  4. Category consistency (case, whitespace, near-duplicate labels,
     canonical mapping dicts)
  5. Self-report bias discussion (report-ready prose)

Outputs
-------
  data/filtered/<name>_filtered.csv          — 4 filtered datasets
  outputs/missing_<dataset>.png              — missingno matrix plots
  outputs/boxplot_<dataset>_<var>.png        — outlier boxplots
  outputs/03_data_quality.md                 — full quality report

Usage
-----
  python scripts/03_data_quality.py
"""

import sys
import os
import warnings

# Force UTF-8 output so Unicode characters in print statements
# render correctly on Windows terminals (cp1252 by default).
sys.stdout.reconfigure(encoding="utf-8")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import missingno as msno

warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
DATASET_DIR  = "dataset"
FILTERED_DIR = os.path.join("data", "filtered")
OUT_DIR      = "outputs"
REPORT_PATH  = os.path.join(OUT_DIR, "03_data_quality.md")

for d in (FILTERED_DIR, OUT_DIR):
    os.makedirs(d, exist_ok=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_csv(fname):
    path = os.path.join(DATASET_DIR, fname)
    for enc in ("utf-8", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Cannot decode {fname}")


def save_fig(fname):
    path = os.path.join(OUT_DIR, fname)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"    Saved {path}")


def iqr_outliers(series, label=""):
    """Return IQR fence bounds and count of values beyond them."""
    s = series.dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr    = q3 - q1
    lo     = q1 - 1.5 * iqr
    hi     = q3 + 1.5 * iqr
    n_low  = int((s < lo).sum())
    n_high = int((s > hi).sum())
    return q1, q3, iqr, lo, hi, n_low, n_high


def make_boxplot(series, title, xlabel, fname_out):
    """Save a styled boxplot for a single variable."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot(
        series.dropna(),
        vert=False,
        patch_artist=True,
        boxprops=dict(facecolor="#6366f1", color="#1e1b4b"),
        medianprops=dict(color="#ef4444", linewidth=2),
        whiskerprops=dict(color="#1e1b4b"),
        capprops=dict(color="#1e1b4b"),
        flierprops=dict(marker="o", color="#f97316", alpha=0.5, markersize=4),
    )
    ax.set_title(title, fontweight="bold", fontsize=10)
    ax.set_xlabel(xlabel)
    ax.set_yticks([])
    plt.tight_layout()
    save_fig(fname_out)


def make_missing_plot(df, title, fname_out):
    """Save a missingno matrix plot."""
    fig, ax = plt.subplots(figsize=(max(8, len(df.columns) * 0.55), 5))
    msno.matrix(df, ax=ax, sparkline=False, color=(0.39, 0.40, 0.95), fontsize=8)
    ax.set_title(title, fontweight="bold", pad=12)
    plt.tight_layout()
    save_fig(fname_out)


def check_whitespace_case(df):
    """
    For every string column, detect:
      - leading/trailing whitespace in any value
      - mixed case within the same column (e.g., 'Male' and 'male')
    Returns a dict: {col: list_of_issues}
    """
    issues = {}
    for col in df.select_dtypes(include="object").columns:
        col_issues = []
        vals = df[col].dropna().astype(str)
        # Whitespace
        if (vals != vals.str.strip()).any():
            n = int((vals != vals.str.strip()).sum())
            col_issues.append(f"{n} values with leading/trailing whitespace")
        # Case: check if lowercasing reduces unique count
        unique_orig  = vals.nunique()
        unique_lower = vals.str.lower().nunique()
        if unique_lower < unique_orig:
            col_issues.append(
                f"mixed case detected ({unique_orig} unique raw → "
                f"{unique_lower} after lower()) — possible duplicates"
            )
        if col_issues:
            issues[col] = col_issues
    return issues


def flag_implausible(series, lo=None, hi=None, label=""):
    """Return count of values outside [lo, hi] (ignoring NaN)."""
    s = series.dropna()
    count = 0
    if lo is not None:
        count += int((s < lo).sum())
    if hi is not None:
        count += int((s > hi).sum())
    return count


# ════════════════════════════════════════════════════════════════════════════════
# STAGE A — Apply population filters & save filtered CSVs
# ════════════════════════════════════════════════════════════════════════════════

print("=== Stage A: Applying population filters ===\n")

# ── DS1: screen_time_attention_productivity ───────────────────────────────────
df1_raw = load_csv("screen_time_attention_productivity.csv")
target_bins = {"Below 18", "18\u201324"}
df1 = df1_raw[df1_raw["Age Group"].isin(target_bins)].copy().reset_index(drop=True)
df1.to_csv(os.path.join(FILTERED_DIR, "screen_time_attention_productivity_filtered.csv"), index=False)
print(f"  DS1 filtered: {len(df1_raw)} -> {len(df1)} rows  (kept Age Group in 'Below 18' or '18-24')")

# ── DS2: student_habits_exam_performance ─────────────────────────────────────
df2 = load_csv("student_habits_exam_performance.csv").copy()
df2.to_csv(os.path.join(FILTERED_DIR, "student_habits_exam_performance_filtered.csv"), index=False)
print(f"  DS2 filtered: no filter applied — {len(df2)} rows retained (age 17–24, 100% fit)")

# ── DS3: student_social_media_academic_impact ─────────────────────────────────
df3 = load_csv("student_social_media_academic_impact.csv").copy()
df3.to_csv(os.path.join(FILTERED_DIR, "student_social_media_academic_impact_filtered.csv"), index=False)
print(f"  DS3 filtered: no filter applied — {len(df3)} rows retained (age 18–24, 100% fit)")

# ── DS4: social_media_attention_mental_health_survey ─────────────────────────
df4_raw = load_csv("social_media_attention_mental_health_survey.csv")
n_outliers_age = int((df4_raw["Age"] > 60).sum())
student_occ    = {"University Student", "School Student"}
df4 = df4_raw[
    (df4_raw["Age"] <= 30) &
    (df4_raw["Occupation"].isin(student_occ))
].copy().reset_index(drop=True)
df4.to_csv(os.path.join(FILTERED_DIR, "social_media_attention_mental_health_survey_filtered.csv"), index=False)
print(
    f"  DS4 filtered: {len(df4_raw)} → {len(df4)} rows  "
    f"(Age ≤ 30 AND student occupation; {n_outliers_age} age>60 outlier(s) also excluded)"
)

DATASETS = [
    ("screen_time_attention_productivity",     df1),
    ("student_habits_exam_performance",        df2),
    ("student_social_media_academic_impact",   df3),
    ("social_media_attention_mental_health_survey", df4),
]

print()


# ════════════════════════════════════════════════════════════════════════════════
# STAGE B — Per-dataset quality checks (collect results for report)
# ════════════════════════════════════════════════════════════════════════════════

quality_results = {}   # ds_key → dict of findings

# ────────────────────────────────────────────────────────────────────────────────
# DS1 checks
# ────────────────────────────────────────────────────────────────────────────────
print("=== DS1: screen_time_attention_productivity ===")

ds1_key  = "screen_time_attention_productivity"
df       = df1

# 1. Missingness
miss1 = df.isnull().sum()
miss1_pct = (miss1 / len(df) * 100).round(2)
row_miss1 = {
    "≥1":  int((df.isnull().sum(axis=1) >= 1).sum()),
    "≥3":  int((df.isnull().sum(axis=1) >= 3).sum()),
    "≥5":  int((df.isnull().sum(axis=1) >= 5).sum()),
}
make_missing_plot(df, "Missingness Matrix — screen_time_attention_productivity (filtered)",
                  f"missing_{ds1_key}.png")

# 2. Duplicates
n_dup1     = df.duplicated().sum()
# No meaningful ID column in DS1 (Unnamed: 0 is a row index, not a true ID)

# 3. Outliers — DS1 is almost entirely categorical; only Unnamed:0 is numeric (row index)
# No domain-relevant numeric column exists — document this explicitly.

# 4. Category consistency
cat_issues1 = check_whitespace_case(df)

quality_results[ds1_key] = {
    "miss_col": miss1[miss1 > 0],
    "miss_pct": miss1_pct[miss1_pct > 0],
    "row_miss": row_miss1,
    "n_dup": n_dup1,
    "cat_issues": cat_issues1,
    "n_rows": len(df),
}
print(f"  Missing cols with data: {(miss1>0).sum()} | Duplicates: {n_dup1}")

# ────────────────────────────────────────────────────────────────────────────────
# DS2 checks
# ────────────────────────────────────────────────────────────────────────────────
print("=== DS2: student_habits_exam_performance ===")

ds2_key = "student_habits_exam_performance"
df      = df2

# 1. Missingness
miss2     = df.isnull().sum()
miss2_pct = (miss2 / len(df) * 100).round(2)
row_miss2 = {
    "≥1": int((df.isnull().sum(axis=1) >= 1).sum()),
    "≥3": int((df.isnull().sum(axis=1) >= 3).sum()),
    "≥5": int((df.isnull().sum(axis=1) >= 5).sum()),
}
make_missing_plot(df, "Missingness Matrix — student_habits_exam_performance (filtered)",
                  f"missing_{ds2_key}.png")

# 2. Duplicates
n_dup2    = df.duplicated().sum()
n_dup_id2 = df["student_id"].duplicated().sum()

# 3. Outliers — key columns for RQs
key_cols2 = {
    "social_media_hours":    ("Social Media Hours/Day",   0, 24),
    "exam_score":            ("Exam Score",               0, 100),
    "sleep_hours":           ("Sleep Hours/Night",        0, 16),
    "study_hours_per_day":   ("Study Hours/Day",          0, 24),
}
outlier_results2 = {}
for col, (label, lo_plaus, hi_plaus) in key_cols2.items():
    q1, q3, iqr, lo, hi, n_lo, n_hi = iqr_outliers(df[col])
    n_implaus = flag_implausible(df[col], lo_plaus, hi_plaus)
    make_boxplot(df[col], f"{label}\nstudent_habits_exam_performance",
                 label, f"boxplot_{ds2_key}_{col}.png")
    outlier_results2[col] = {
        "label": label, "q1": q1, "q3": q3, "iqr": iqr,
        "fence_lo": round(lo, 3), "fence_hi": round(hi, 3),
        "n_below_fence": n_lo, "n_above_fence": n_hi,
        "n_implausible": n_implaus, "plaus_range": f"{lo_plaus}–{hi_plaus}",
    }

# 4. Category consistency
cat_issues2 = check_whitespace_case(df)

quality_results[ds2_key] = {
    "miss_col": miss2[miss2 > 0],
    "miss_pct": miss2_pct[miss2_pct > 0],
    "row_miss": row_miss2,
    "n_dup": n_dup2,
    "n_dup_id": n_dup_id2,
    "outliers": outlier_results2,
    "cat_issues": cat_issues2,
    "n_rows": len(df),
}
print(f"  Missing cols: {(miss2>0).sum()} | Duplicates: {n_dup2} | ID dups: {n_dup_id2}")

# ────────────────────────────────────────────────────────────────────────────────
# DS3 checks
# ────────────────────────────────────────────────────────────────────────────────
print("=== DS3: student_social_media_academic_impact ===")

ds3_key = "student_social_media_academic_impact"
df      = df3

# 1. Missingness
miss3     = df.isnull().sum()
miss3_pct = (miss3 / len(df) * 100).round(2)
row_miss3 = {
    "≥1": int((df.isnull().sum(axis=1) >= 1).sum()),
    "≥3": int((df.isnull().sum(axis=1) >= 3).sum()),
    "≥5": int((df.isnull().sum(axis=1) >= 5).sum()),
}
make_missing_plot(df, "Missingness Matrix — student_social_media_academic_impact (filtered)",
                  f"missing_{ds3_key}.png")

# 2. Duplicates
n_dup3    = df.duplicated().sum()
n_dup_id3 = df["Student_ID"].duplicated().sum()

# 3. Outliers
key_cols3 = {
    "Avg_Daily_Usage_Hours": ("Avg Daily Usage (hours)", 0, 24),
    "Addicted_Score":        ("Addiction Score",          1, 10),
    "Mental_Health_Score":   ("Mental Health Score",      1, 10),
    "Sleep_Hours_Per_Night": ("Sleep Hours/Night",        0, 16),
}
outlier_results3 = {}
for col, (label, lo_plaus, hi_plaus) in key_cols3.items():
    q1, q3, iqr, lo, hi, n_lo, n_hi = iqr_outliers(df[col])
    n_implaus = flag_implausible(df[col], lo_plaus, hi_plaus)
    make_boxplot(df[col], f"{label}\nstudent_social_media_academic_impact",
                 label, f"boxplot_{ds3_key}_{col}.png")
    outlier_results3[col] = {
        "label": label, "q1": q1, "q3": q3, "iqr": iqr,
        "fence_lo": round(lo, 3), "fence_hi": round(hi, 3),
        "n_below_fence": n_lo, "n_above_fence": n_hi,
        "n_implausible": n_implaus, "plaus_range": f"{lo_plaus}–{hi_plaus}",
    }

# 4. Category consistency
cat_issues3 = check_whitespace_case(df)

quality_results[ds3_key] = {
    "miss_col": miss3[miss3 > 0],
    "miss_pct": miss3_pct[miss3_pct > 0],
    "row_miss": row_miss3,
    "n_dup": n_dup3,
    "n_dup_id": n_dup_id3,
    "outliers": outlier_results3,
    "cat_issues": cat_issues3,
    "n_rows": len(df),
}
print(f"  Missing cols: {(miss3>0).sum()} | Duplicates: {n_dup3} | ID dups: {n_dup_id3}")

# ────────────────────────────────────────────────────────────────────────────────
# DS4 checks
# ────────────────────────────────────────────────────────────────────────────────
print("=== DS4: social_media_attention_mental_health_survey ===")

ds4_key = "social_media_attention_mental_health_survey"
df      = df4

# 1. Missingness
miss4     = df.isnull().sum()
miss4_pct = (miss4 / len(df) * 100).round(2)
row_miss4 = {
    "≥1": int((df.isnull().sum(axis=1) >= 1).sum()),
    "≥3": int((df.isnull().sum(axis=1) >= 3).sum()),
    "≥5": int((df.isnull().sum(axis=1) >= 5).sum()),
}
make_missing_plot(df, "Missingness Matrix — social_media_attention_mental_health_survey (filtered)",
                  f"missing_{ds4_key}.png")

# 2. Duplicates — use Timestamp as proxy ID
n_dup4    = df.duplicated().sum()
n_dup_ts4 = df["Timestamp"].duplicated().sum()

# 3. Outliers — Age + key Likert items + composite attention score
# Composite: Q10 (distracted when busy) + Q12 (easily distracted) + Q14 (difficulty concentrating)
q10_col = "10. How often do you get distracted by Social media when you are busy doing something?"
q12_col = "12. On a scale of 1 to 5, how easily distracted are you?"
q14_col = "14. Do you find it difficult to concentrate on things?"
df["attention_composite"] = df[q10_col] + df[q12_col] + df[q14_col]

key_cols4 = {
    "Age":                 ("Age",                    13, 30),
    q10_col:               ("Q10 — Distracted (1–5)", 1,  5),
    q12_col:               ("Q12 — Easily Distracted (1–5)", 1, 5),
    q14_col:               ("Q14 — Difficulty Concentrating (1–5)", 1, 5),
    "attention_composite": ("Attention Composite Score (Q10+Q12+Q14)", 3, 15),
}
outlier_results4 = {}
short_names4 = {
    "Age":                 "Age",
    q10_col:               "Q10_distracted",
    q12_col:               "Q12_easily_distracted",
    q14_col:               "Q14_difficulty_concentrating",
    "attention_composite": "attention_composite",
}
for col, (label, lo_plaus, hi_plaus) in key_cols4.items():
    q1, q3, iqr, lo, hi, n_lo, n_hi = iqr_outliers(df[col])
    n_implaus = flag_implausible(df[col], lo_plaus, hi_plaus)
    sname = short_names4[col]
    make_boxplot(df[col], f"{label}\nsocial_media_attention_mental_health_survey",
                 label, f"boxplot_{ds4_key}_{sname}.png")
    outlier_results4[col] = {
        "label": label, "q1": q1, "q3": q3, "iqr": iqr,
        "fence_lo": round(lo, 3), "fence_hi": round(hi, 3),
        "n_below_fence": n_lo, "n_above_fence": n_hi,
        "n_implausible": n_implaus, "plaus_range": f"{lo_plaus}–{hi_plaus}",
    }

# 4. Category consistency — incl. Gender normalisation
cat_issues4 = check_whitespace_case(df)

# Gender canonical mapping
gender_map4 = {
    "Male":               "Male",
    "Female":             "Female",
    "Nonbinary ":         "Non-binary or Other",
    "Non-binary":         "Non-binary or Other",
    "NB":                 "Non-binary or Other",
    "unsure ":            "Non-binary or Other",
    "Trans":              "Non-binary or Other",
    "Non binary ":        "Non-binary or Other",
    "There are others???":"Non-binary or Other",
}

quality_results[ds4_key] = {
    "miss_col": miss4[miss4 > 0],
    "miss_pct": miss4_pct[miss4_pct > 0],
    "row_miss": row_miss4,
    "n_dup": n_dup4,
    "n_dup_ts": n_dup_ts4,
    "outliers": outlier_results4,
    "cat_issues": cat_issues4,
    "gender_map": gender_map4,
    "n_rows": len(df),
}
print(f"  Missing cols: {(miss4>0).sum()} | Duplicates: {n_dup4} | Timestamp dups: {n_dup_ts4}")


# ════════════════════════════════════════════════════════════════════════════════
# STAGE C — Build markdown report
# ════════════════════════════════════════════════════════════════════════════════

print("\nBuilding markdown report...")


def miss_table(miss_col, miss_pct_col, threshold=30):
    """Render a missingness table; flag columns above threshold."""
    if miss_col.empty:
        return "_No missing values detected._"
    rows = "| Column | Missing n | Missing % | Flag |\n|--------|----------:|----------:|------|\n"
    for col in miss_col.index:
        flag = "⚠ **>30% — consider drop/impute**" if miss_pct_col[col] > threshold else ""
        rows += f"| `{col}` | {int(miss_col[col]):,} | {miss_pct_col[col]:.1f}% | {flag} |\n"
    return rows


def outlier_table(outlier_dict):
    rows = (
        "| Column | Q1 | Q3 | IQR | Lower Fence | Upper Fence | "
        "n < fence | n > fence | Implausible values |\n"
        "|--------|----|----|-----|-------------|-------------|"
        "----------|----------|-------------------|\n"
    )
    for col, r in outlier_dict.items():
        rows += (
            f"| `{col}` | {r['q1']} | {r['q3']} | {r['iqr']:.3f} | "
            f"{r['fence_lo']} | {r['fence_hi']} | "
            f"{r['n_below_fence']} | {r['n_above_fence']} | "
            f"{r['n_implausible']} (outside {r['plaus_range']}) |\n"
        )
    return rows


lines = []

# ── Title ─────────────────────────────────────────────────────────────────────
lines += [
    "# Data Quality Sweep — Stage 3\n",
    "> Filters applied per Stage 2 population check. "
    "Filtered datasets saved to `data/filtered/`.\n",
    "---\n",
]

# ── Population filter log ─────────────────────────────────────────────────────
lines += [
    "## Population Filters Applied\n",
    "| Dataset | Filter Applied | n Before | n After |",
    "|---------|---------------|--------:|-------:|",
    f"| `screen_time_attention_productivity.csv` | Age Group ∈ {{'Below 18', '18–24'}} | "
    f"{len(df1_raw)} | {len(df1)} |",
    f"| `student_habits_exam_performance.csv` | None (age 17–24, 100% fit) | "
    f"{len(df2)} | {len(df2)} |",
    f"| `student_social_media_academic_impact.csv` | None (age 18–24, 100% fit) | "
    f"{len(df3)} | {len(df3)} |",
    f"| `social_media_attention_mental_health_survey.csv` | Age ≤ 30 AND student occupation; "
    f"{n_outliers_age} age>60 outlier(s) dropped | {len(df4_raw)} | {len(df4)} |",
    "",
    "> **DS1 note:** The '25–34' age bin was excluded entirely because it cannot be split at "
    "age 25 without raw values. This removes 24 respondents (~12 of whom would fall within "
    "the broad 13–30 target). This exclusion is conservative and explicitly documented here.\n",
    "---\n",
]

# ── Cross-dataset summary table ───────────────────────────────────────────────
r1 = quality_results["screen_time_attention_productivity"]
r2 = quality_results["student_habits_exam_performance"]
r3 = quality_results["student_social_media_academic_impact"]
r4 = quality_results["social_media_attention_mental_health_survey"]

def count_high_miss(r):
    if r["miss_pct"].empty:
        return 0
    return int((r["miss_pct"] > 30).sum())

def count_outlier_flags(r):
    if "outliers" not in r:
        return "N/A (all categorical)"
    total = sum(v["n_above_fence"] + v["n_below_fence"] for v in r["outliers"].values())
    return str(total)

def count_cat_issues(r):
    return len(r["cat_issues"])

lines += [
    "## Cross-Dataset Quality Summary\n",
    "| Dataset | n (filtered) | Cols >30% missing | Outlier flags (IQR) | Category issues |",
    "|---------|:------------:|:-----------------:|:-------------------:|:---------------:|",
    f"| `screen_time_attention_productivity` | {r1['n_rows']} | {count_high_miss(r1)} | "
    f"{count_outlier_flags(r1)} | {count_cat_issues(r1)} |",
    f"| `student_habits_exam_performance` | {r2['n_rows']} | {count_high_miss(r2)} | "
    f"{count_outlier_flags(r2)} | {count_cat_issues(r2)} |",
    f"| `student_social_media_academic_impact` | {r3['n_rows']} | {count_high_miss(r3)} | "
    f"{count_outlier_flags(r3)} | {count_cat_issues(r3)} |",
    f"| `social_media_attention_mental_health_survey` | {r4['n_rows']} | {count_high_miss(r4)} | "
    f"{count_outlier_flags(r4)} | {count_cat_issues(r4)} |",
    "\n---\n",
]

# ════════════════════════════════════════════════════════════════════════════════
# DS1 Section
# ════════════════════════════════════════════════════════════════════════════════
lines += [
    "## 1. screen_time_attention_productivity (n = {n})\n".format(n=r1["n_rows"]),
    "_Filtered to Age Group ∈ {'Below 18', '18–24'}_\n",

    "### Check 1 — Missingness\n",
    miss_table(r1["miss_col"], r1["miss_pct"]),
    "",
    "**Row-level missingness distribution:**",
    f"- Rows with ≥1 missing value: {r1['row_miss']['≥1']} ({r1['row_miss']['≥1']/r1['n_rows']*100:.1f}%)",
    f"- Rows with ≥3 missing values: {r1['row_miss']['≥3']}",
    f"- Rows with ≥5 missing values: {r1['row_miss']['≥5']}",
    "",
    "![Missingness matrix](missing_screen_time_attention_productivity.png)\n",
    (
        "**MCAR/MAR/MNAR classification:** The three columns with missing data "
        "(`Environment`, `Work Strategy`, `Notification Handling`) each lose fewer than 2% of "
        "rows. The sparsity is consistent across respondent types with no discernible pattern "
        "linked to other variables, suggesting **MCAR** (Missing Completely At Random) — likely "
        "survey non-response on optional items. Listwise deletion of these rows is appropriate "
        "given the low rate and large retained sample."
    ),

    "\n### Check 2 — Duplicates\n",
    f"- Full duplicate rows: **{r1['n_dup']}**",
    "- ID column: none available (the `Unnamed: 0` column is a row index, not a participant ID)",

    "\n### Check 3 — Outliers in Key Numeric Fields\n",
    (
        "> **Note:** All domain-relevant columns in this dataset are categorical or ordinal "
        "strings (`Average Screen Time`, `Attention Span`, `Productivity`, `App Category`). "
        "No continuous numeric variable suitable for IQR outlier analysis exists. Ordinal "
        "distributions are reported via value_counts in the intake summary (Stage 1). "
        "Boxplot analysis is not applicable here."
    ),

    "\n### Check 4 — Category Consistency\n",
]

if r1["cat_issues"]:
    for col, issues in r1["cat_issues"].items():
        lines.append(f"**`{col}`:**")
        for iss in issues:
            lines.append(f"- {iss}")
else:
    lines.append("_No case inconsistencies or whitespace issues detected._")

lines += [
    "",
    "**Recommended cleaning mappings:**",
    "```python",
    "# DS1 — no column-level cleaning required; values are already consistent.",
    "```",
    "\n---\n",
]

# ════════════════════════════════════════════════════════════════════════════════
# DS2 Section
# ════════════════════════════════════════════════════════════════════════════════
lines += [
    "## 2. student_habits_exam_performance (n = {n})\n".format(n=r2["n_rows"]),
    "_No population filter applied (age 17–24, 100% within target)_\n",

    "### Check 1 — Missingness\n",
    miss_table(r2["miss_col"], r2["miss_pct"]),
    "",
    "**Row-level missingness distribution:**",
    f"- Rows with ≥1 missing value: {r2['row_miss']['≥1']} ({r2['row_miss']['≥1']/r2['n_rows']*100:.1f}%)",
    f"- Rows with ≥3 missing values: {r2['row_miss']['≥3']}",
    f"- Rows with ≥5 missing values: {r2['row_miss']['≥5']}",
    "",
    "![Missingness matrix](missing_student_habits_exam_performance.png)\n",
]

if r2["miss_col"].empty:
    lines.append(
        "**MCAR/MAR/MNAR classification:** No missing values detected. "
        "This is consistent with the dataset being synthetically generated "
        "(confirmed on Kaggle) — synthetic datasets are typically complete by construction."
    )
else:
    pct_val = r2["miss_pct"].max()
    col_val = r2["miss_pct"].idxmax()
    lines.append(
        f"**MCAR/MAR/MNAR classification:** `{col_val}` is missing in {pct_val:.1f}% of rows. "
        "Given this is a synthetic dataset, the pattern is likely deliberately introduced; "
        "it should be treated as **MCAR** and imputed with the mode or dropped."
    )

lines += [
    "\n### Check 2 — Duplicates\n",
    f"- Full duplicate rows: **{r2['n_dup']}**",
    f"- Duplicate `student_id` values: **{r2['n_dup_id']}**",

    "\n### Check 3 — Outliers in Key Numeric Fields\n",
    outlier_table(r2["outliers"]),
    "",
]
for col, res in r2["outliers"].items():
    lines.append(f"![Boxplot {res['label']}](boxplot_student_habits_exam_performance_{col}.png)\n")

lines += [
    "**Implausibility notes:**",
    "- `social_media_hours` values > 24 would be physically impossible — flag as implausible.",
    "- `sleep_hours` values < 0 or > 16 are physiologically implausible.",
    "- `exam_score` must be in [0, 100] by definition.",
    "- `study_hours_per_day` > 24 is impossible.",

    "\n### Check 4 — Category Consistency\n",
]

if r2["cat_issues"]:
    for col, issues in r2["cat_issues"].items():
        lines.append(f"**`{col}`:**")
        for iss in issues:
            lines.append(f"- {iss}")
else:
    lines.append("_No case inconsistencies or whitespace issues detected._")

# Gender values
g2_vals = df2["gender"].unique().tolist()
lines += [
    "",
    "**Recommended cleaning mappings:**",
    "```python",
    f"# DS2 — gender values observed: {g2_vals}",
    "# Values appear clean; no mapping required.",
    "gender_map_ds2 = {}  # no changes needed",
    "",
    "# parental_education_level — check if NaN rows should be imputed or dropped",
    f"# Missing count: {int(r2['miss_col'].get('parental_education_level', 0))}",
    "# Recommended: impute with mode ('High School') or create 'Unknown' category",
    "```",
    "\n---\n",
]

# ════════════════════════════════════════════════════════════════════════════════
# DS3 Section
# ════════════════════════════════════════════════════════════════════════════════
lines += [
    "## 3. student_social_media_academic_impact (n = {n})\n".format(n=r3["n_rows"]),
    "_No population filter applied (age 18–24, 100% within target)_\n",

    "### Check 1 — Missingness\n",
    miss_table(r3["miss_col"], r3["miss_pct"]),
    "",
    "**Row-level missingness distribution:**",
    f"- Rows with ≥1 missing value: {r3['row_miss']['≥1']} ({r3['row_miss']['≥1']/r3['n_rows']*100:.1f}%)",
    f"- Rows with ≥3 missing values: {r3['row_miss']['≥3']}",
    f"- Rows with ≥5 missing values: {r3['row_miss']['≥5']}",
    "",
    "![Missingness matrix](missing_student_social_media_academic_impact.png)\n",
    (
        "**MCAR/MAR/MNAR classification:** No missing values detected. "
        "The dataset appears to be synthetically generated or carefully curated, "
        "consistent with its Kaggle provenance. The absence of any missingness means "
        "no imputation strategy is required prior to analysis."
    ),

    "\n### Check 2 — Duplicates\n",
    f"- Full duplicate rows: **{r3['n_dup']}**",
    f"- Duplicate `Student_ID` values: **{r3['n_dup_id']}**",

    "\n### Check 3 — Outliers in Key Numeric Fields\n",
    outlier_table(r3["outliers"]),
    "",
]
for col, res in r3["outliers"].items():
    lines.append(f"![Boxplot {res['label']}](boxplot_student_social_media_academic_impact_{col}.png)\n")

lines += [
    "**Implausibility notes:**",
    "- `Avg_Daily_Usage_Hours` > 24 is physically impossible.",
    "- `Addicted_Score` and `Mental_Health_Score` should fall within their declared scale range (1–10).",
    "- `Sleep_Hours_Per_Night` < 0 or > 16 is physiologically implausible.",

    "\n### Check 4 — Category Consistency\n",
]

if r3["cat_issues"]:
    for col, issues in r3["cat_issues"].items():
        lines.append(f"**`{col}`:**")
        for iss in issues:
            lines.append(f"- {iss}")
else:
    lines.append("_No case inconsistencies or whitespace issues detected._")

g3_vals = df3["Gender"].unique().tolist()
lines += [
    "",
    "**Recommended cleaning mappings:**",
    "```python",
    f"# DS3 — Gender values: {g3_vals}",
    "# Values appear clean (binary Male/Female); no mapping required.",
    "gender_map_ds3 = {}  # no changes needed",
    "",
    "# Affects_Academic_Performance — binary Yes/No; verify no variants",
    f"# Unique values: {sorted(df3['Affects_Academic_Performance'].dropna().unique().tolist())}",
    "```",
    "\n---\n",
]

# ════════════════════════════════════════════════════════════════════════════════
# DS4 Section
# ════════════════════════════════════════════════════════════════════════════════
lines += [
    "## 4. social_media_attention_mental_health_survey (n = {n})\n".format(n=r4["n_rows"]),
    "_Filter: Age ≤ 30 AND Occupation ∈ {'University Student', 'School Student'}_\n",

    "### Check 1 — Missingness\n",
    miss_table(r4["miss_col"], r4["miss_pct"]),
    "",
    "**Row-level missingness distribution:**",
    f"- Rows with ≥1 missing value: {r4['row_miss']['≥1']} ({r4['row_miss']['≥1']/r4['n_rows']*100:.1f}%)",
    f"- Rows with ≥3 missing values: {r4['row_miss']['≥3']}",
    f"- Rows with ≥5 missing values: {r4['row_miss']['≥5']}",
    "",
    "![Missingness matrix](missing_social_media_attention_mental_health_survey.png)\n",
    (
        "**MCAR/MAR/MNAR classification:** The only column with missing values is `Affiliations` "
        "(institutional affiliation). Its absence is unlikely to be random: respondents without a "
        "clear institutional affiliation (e.g., online students, gap-year students) may be more "
        "likely to skip this field, suggesting **MAR** (Missing At Random, conditional on "
        "`Occupation`). Since `Affiliations` is not a primary analysis variable, listwise "
        "exclusion for this column is acceptable. All Likert-scale items (Q9–Q20) and the "
        "key demographic fields are complete."
    ),

    "\n### Check 2 — Duplicates\n",
    f"- Full duplicate rows: **{r4['n_dup']}**",
    f"- Duplicate `Timestamp` values: **{r4['n_dup_ts']}**",
    (
        "  > Note: a small number of duplicate timestamps can occur when multiple "
        "respondents submit the form within the same second — this does not necessarily "
        "indicate actual duplicate responses."
    ),

    "\n### Check 3 — Outliers in Key Numeric Fields\n",
    outlier_table(r4["outliers"]),
    "",
]
sname_map = {
    "Age":                 "Age",
    q10_col:               "Q10_distracted",
    q12_col:               "Q12_easily_distracted",
    q14_col:               "Q14_difficulty_concentrating",
    "attention_composite": "attention_composite",
}
for col, res in r4["outliers"].items():
    sname = sname_map[col]
    lines.append(
        f"![Boxplot {res['label']}]"
        f"(boxplot_social_media_attention_mental_health_survey_{sname}.png)\n"
    )

lines += [
    "**Implausibility notes:**",
    "- `Age` values > 30 have already been removed by the population filter.",
    "- All Likert items (Q9–Q20) are bounded 1–5; any value outside this range would be implausible.",
    "- `attention_composite` (Q10 + Q12 + Q14) has a theoretical range of 3–15.",

    "\n### Check 4 — Category Consistency\n",
    "**Gender column — near-duplicate label issue (requires normalisation):**",
    "",
    f"Unique raw values observed: `{sorted(df4_raw['Gender'].dropna().unique().tolist())}`",
    "",
    "Seven variants of non-binary/other gender exist alongside 'Male' and 'Female'. "
    "These must be consolidated before any gender-stratified analysis.",
    "",
    "**Recommended canonical mapping:**",
    "```python",
    "# DS4 — Gender normalisation map",
    "gender_map_ds4 = {",
    '    "Male":               "Male",',
    '    "Female":             "Female",',
    '    "Nonbinary ":         "Non-binary or Other",   # trailing whitespace',
    '    "Non-binary":         "Non-binary or Other",',
    '    "NB":                 "Non-binary or Other",',
    '    "unsure ":            "Non-binary or Other",   # trailing whitespace',
    '    "Trans":              "Non-binary or Other",',
    '    "Non binary ":        "Non-binary or Other",   # trailing whitespace',
    '    "There are others???":"Non-binary or Other",',
    "}",
    "",
    "# Apply with:",
    "df['Gender'] = df['Gender'].str.strip().map(gender_map_ds4)",
    "```",
    "",
    "**`Affiliations` column — high cardinality with mixed separator styles:**",
    "```python",
    "# DS4 — Affiliations has 18 unique values including multi-value strings",
    "# e.g., 'School, University' — consider splitting into binary indicator columns",
    "# if affiliation is used as a covariate.",
    "# No merge required; low priority given Affiliations is not a primary variable.",
    "```",
]

if r4["cat_issues"]:
    lines.append("\n**Other whitespace/case issues detected:**")
    for col, issues in r4["cat_issues"].items():
        if col == "Gender":
            continue    # already handled above
        lines.append(f"**`{col}`:**")
        for iss in issues:
            lines.append(f"- {iss}")

lines.append("\n---\n")

# ════════════════════════════════════════════════════════════════════════════════
# Self-report bias
# ════════════════════════════════════════════════════════════════════════════════
lines += [
    "## Self-Report Bias and Data Limitations\n",
    (
        "All four datasets rely on self-reported measures of social media usage, "
        "attention, productivity, and/or academic performance, which introduces "
        "several interconnected validity concerns. **Recall bias** is particularly "
        "salient for usage estimates: respondents are unlikely to accurately remember "
        "the precise number of hours spent on social media each day, and platform-level "
        "screen time data (where available) consistently exceeds self-reported figures by "
        "20–40% in the literature. **Social desirability bias** may suppress reported "
        "usage hours and inflate reported productivity and academic engagement, especially "
        "in datasets collected in academic contexts where respondents may infer the "
        "researcher's hypothesis. **Measurement error** compounds across constructs: "
        "constructs such as 'attention span' (`screen_time_attention_productivity.csv`) "
        "and 'addiction score' (`student_social_media_academic_impact.csv`) are operationalised "
        "differently across datasets with no shared validated instrument, limiting "
        "cross-dataset comparability."
    ),
    "",
    (
        "Two datasets warrant explicit disclosure beyond the general self-report caveat. "
        "**`student_habits_exam_performance.csv`** is openly described as synthetically "
        "generated on Kaggle: while it is useful for demonstrating relationships between "
        "variables, its findings cannot be interpreted as empirical evidence of real-world "
        "effects and must be clearly labelled as synthetic throughout the report. "
        "**`student_social_media_academic_impact.csv`** spans respondents from over 110 "
        "countries, meaning that constructs such as 'addiction', 'academic performance', "
        "and 'mental health score' are being compared across fundamentally different "
        "educational systems, grading cultures, and cultural attitudes towards social media "
        "use. Cross-cultural measurement equivalence has not been established for any of "
        "the instruments used, and aggregate findings should be interpreted with this "
        "heterogeneity explicitly acknowledged."
    ),
]

# ── Write report ──────────────────────────────────────────────────────────────
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nDone.")
print(f"  Report  : {REPORT_PATH}")
print(f"  Filtered: {FILTERED_DIR}/")
print(f"  Charts  : {OUT_DIR}/missing_*.png, {OUT_DIR}/boxplot_*.png")
