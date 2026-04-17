"""
03_data_quality.py
Applies population filters, then runs missingness, duplicate, outlier,
and category consistency checks on each filtered dataset.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    import missingno as msno
    HAS_MSNO = True
except ImportError:
    HAS_MSNO = False
    print("Warning: missingno not installed, skipping matrix plots")

DATASET_DIR = "dataset"
FILTERED_DIR = os.path.join("data", "filtered")
os.makedirs("outputs", exist_ok=True)
os.makedirs(FILTERED_DIR, exist_ok=True)


# ---- step 1: load and filter each dataset ----

def load_and_filter():
    """Load raw CSVs and apply the population filters from stage 2."""
    filtered = {}

    # DS1: screen time — keep only young age groups
    df1 = pd.read_csv(os.path.join(DATASET_DIR, "screen_time_attention_productivity.csv"))
    df1 = df1[df1["Age Group"].isin(["Below 18", "18–24"])].copy()
    filtered["screen_time_attention_productivity"] = df1

    # DS2: student habits — already 17-24, no filter needed
    df2 = pd.read_csv(os.path.join(DATASET_DIR, "student_habits_exam_performance.csv"))
    filtered["student_habits_exam_performance"] = df2

    # DS3: student academic impact — already 18-24, no filter needed
    df3 = pd.read_csv(os.path.join(DATASET_DIR, "student_social_media_academic_impact.csv"))
    filtered["student_social_media_academic_impact"] = df3

    # DS4: attention survey — age <= 30 AND student, drop age > 60 outliers
    df4 = pd.read_csv(os.path.join(DATASET_DIR, "social_media_attention_mental_health_survey.csv"))
    df4 = df4[df4["Age"] <= 60]  # drop obvious outliers first
    df4 = df4[
        (df4["Age"] <= 30) &
        (df4["Occupation"].isin(["University Student", "School Student"]))
    ].copy()
    filtered["social_media_attention_mental_health_survey"] = df4

    # save filtered versions
    for name, df in filtered.items():
        path = os.path.join(FILTERED_DIR, f"{name}_filtered.csv")
        df.to_csv(path, index=False)
        print(f"  Saved {name}: {len(df)} rows → {path}")

    return filtered


# ---- step 2: run quality checks ----

def check_missing(df, name, report):
    """Check missingness patterns and generate matrix plot."""
    report += "### Check 1 — Missingness\n\n"

    miss = df.isnull().sum()
    miss = miss[miss > 0]

    if len(miss) == 0:
        report += "_No missing values detected._\n\n"
    else:
        report += "| Column | Missing n | Missing % | Flag |\n"
        report += "|--------|----------:|----------:|------|\n"
        for col, cnt in miss.items():
            pct = round(cnt / len(df) * 100, 1)
            flag = "⚠️ >30%" if pct > 30 else ""
            report += f"| `{col}` | {cnt} | {pct}% | {flag} |\n"
        report += "\n"

    # row-level missingness
    row_miss = df.isnull().sum(axis=1)
    report += "**Row-level missingness distribution:**\n"
    report += f"- Rows with ≥1 missing value: {(row_miss >= 1).sum()} ({(row_miss >= 1).mean()*100:.1f}%)\n"
    report += f"- Rows with ≥3 missing values: {(row_miss >= 3).sum()}\n"
    report += f"- Rows with ≥5 missing values: {(row_miss >= 5).sum()}\n\n"

    # missingness matrix plot
    if HAS_MSNO:
        fig, ax = plt.subplots(figsize=(10, 4))
        msno.matrix(df, ax=ax, sparkline=False, fontsize=8)
        plt.title(f"Missingness Matrix — {name}", fontsize=10)
        plt.tight_layout()
        plt.savefig(f"outputs/missing_{name}.png", dpi=150)
        plt.close()
        report += f"![Missingness matrix](missing_{name}.png)\n\n"

    return report


def check_duplicates(df, name, report):
    """Check for duplicate rows and IDs."""
    report += "### Check 2 — Duplicates\n\n"
    report += f"- Full duplicate rows: **{df.duplicated().sum()}**\n"

    # check for ID columns
    id_candidates = [c for c in df.columns if "id" in c.lower() or c == "Timestamp"]
    for col in id_candidates:
        n_dup = df[col].duplicated().sum()
        report += f"- Duplicate `{col}` values: **{n_dup}**\n"
        if n_dup > 0 and col == "Timestamp":
            report += "  > Note: duplicate timestamps can occur when multiple respondents submit within the same second.\n"

    report += "\n"
    return report


def check_outliers(df, name, report, key_cols):
    """Check IQR-based outliers for specified numeric columns."""
    report += "### Check 3 — Outliers in Key Numeric Fields\n\n"

    # skip if no numeric key cols
    actual_cols = [c for c in key_cols if c in df.columns and df[c].dtype in ["int64", "float64"]]
    if not actual_cols:
        report += "> **Note:** All domain-relevant columns in this dataset are categorical. "
        report += "Boxplot analysis is not applicable.\n\n"
        return report

    report += "| Column | Q1 | Q3 | IQR | Lower Fence | Upper Fence | n < fence | n > fence | Implausible values |\n"
    report += "|--------|----|----|-----|-------------|-------------|----------|----------|-------------------|\n"

    for col in actual_cols:
        vals = df[col].dropna()
        q1 = vals.quantile(0.25)
        q3 = vals.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        n_low = int((vals < lower).sum())
        n_high = int((vals > upper).sum())

        # check for implausible values based on what the column represents
        implausible = 0
        if "hour" in col.lower() and (vals > 24).any():
            implausible = int((vals > 24).sum())
        if "sleep" in col.lower() and ((vals < 0) | (vals > 16)).any():
            implausible = int(((vals < 0) | (vals > 16)).sum())
        if "score" in col.lower() and "exam" in col.lower() and ((vals < 0) | (vals > 100)).any():
            implausible = int(((vals < 0) | (vals > 100)).sum())

        report += f"| `{col}` | {q1} | {q3} | {iqr:.3f} | {lower:.1f} | {upper:.1f} | {n_low} | {n_high} | {implausible} |\n"

        # boxplot
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.boxplot(vals, vert=False)
        ax.set_title(f"{col} — {name}")
        plt.tight_layout()
        safe_col = col.replace(" ", "_").replace(".", "").replace(",", "")[:40]
        plt.savefig(f"outputs/boxplot_{name}_{safe_col}.png", dpi=150)
        plt.close()

    report += "\n"
    return report


def check_categories(df, name, report):
    """Check for case issues, whitespace, and near-duplicate categories."""
    report += "### Check 4 — Category Consistency\n\n"
    issues_found = False

    cat_cols = df.select_dtypes(exclude="number").columns
    for col in cat_cols:
        vals = df[col].dropna().unique()

        # check whitespace
        stripped = [str(v).strip() for v in vals]
        if set(str(v) for v in vals) != set(stripped):
            report += f"**`{col}`**: trailing/leading whitespace detected\n\n"
            issues_found = True

        # check case variants
        lower_map = {}
        for v in vals:
            key = str(v).strip().lower()
            if key not in lower_map:
                lower_map[key] = []
            lower_map[key].append(str(v))
        for key, variants in lower_map.items():
            if len(variants) > 1:
                report += f"**`{col}`**: near-duplicate values: {variants}\n\n"
                issues_found = True

    if not issues_found:
        report += "_No case inconsistencies or whitespace issues detected._\n\n"

    return report


# ---- main ----

print("Loading and filtering datasets...")
filtered = load_and_filter()

# define which numeric columns to check outliers on, per dataset
outlier_cols = {
    "screen_time_attention_productivity": [],  # all categorical
    "student_habits_exam_performance": ["social_media_hours", "exam_score", "sleep_hours", "study_hours_per_day"],
    "student_social_media_academic_impact": ["Avg_Daily_Usage_Hours", "Addicted_Score", "Mental_Health_Score", "Sleep_Hours_Per_Night"],
    "social_media_attention_mental_health_survey": ["Age"],
}

# also check the Likert attention items for DS4
likert_cols = [c for c in filtered["social_media_attention_mental_health_survey"].columns if c.startswith("1")]
outlier_cols["social_media_attention_mental_health_survey"].extend(likert_cols[:3])  # Q10, Q12, Q14

# create attention composite for DS4
df4 = filtered["social_media_attention_mental_health_survey"]
q10 = [c for c in df4.columns if "distracted by Social media" in c]
q12 = [c for c in df4.columns if "easily distracted" in c]
q14 = [c for c in df4.columns if "difficult to concentrate" in c]
if q10 and q12 and q14:
    df4["attention_composite"] = df4[q10[0]] + df4[q12[0]] + df4[q14[0]]
    outlier_cols["social_media_attention_mental_health_survey"].append("attention_composite")

# build the report
report = "# Data Quality Sweep — Stage 3\n\n"
report += "> Filters applied per Stage 2 population check. Filtered datasets saved to `data/filtered/`.\n\n---\n\n"

# filter summary table
report += "## Population Filters Applied\n\n"
report += "| Dataset | Filter Applied | n Before | n After |\n"
report += "|---------|---------------|--------:|-------:|\n"
originals = {
    "screen_time_attention_productivity": 200,
    "student_habits_exam_performance": 1000,
    "student_social_media_academic_impact": 705,
    "social_media_attention_mental_health_survey": 481,
}
filter_desc = {
    "screen_time_attention_productivity": "Age Group ∈ {'Below 18', '18–24'}",
    "student_habits_exam_performance": "None (age 17–24, 100% fit)",
    "student_social_media_academic_impact": "None (age 18–24, 100% fit)",
    "social_media_attention_mental_health_survey": "Age ≤ 30 AND student occupation; age>60 outliers dropped",
}
for name, df in filtered.items():
    report += f"| `{name}` | {filter_desc[name]} | {originals[name]} | {len(df)} |\n"
report += "\n---\n\n"

# quality summary (we'll fill counts as we go)
quality_summary = {}

for name, df in filtered.items():
    print(f"\nRunning quality checks on {name}...")
    report += f"## {name} (n = {len(df):,})\n\n"

    report = check_missing(df, name, report)
    report = check_duplicates(df, name, report)
    report = check_outliers(df, name, report, outlier_cols.get(name, []))
    report = check_categories(df, name, report)

    report += "---\n\n"

# MCAR/MAR/MNAR notes — written manually since this requires judgment
report += "## Missingness Classification Notes\n\n"
report += "- **screen_time_attention_productivity:** 3 columns with <2% missing, no pattern linked to other variables → **MCAR**. Listwise deletion appropriate.\n"
report += "- **student_habits_exam_performance:** `parental_education_level` missing 9.1%. Synthetic dataset, pattern likely deliberate → **MCAR**. Not a primary variable, retain rows.\n"
report += "- **student_social_media_academic_impact:** No missing values.\n"
report += "- **social_media_attention_mental_health_survey:** `Affiliations` missing 5.0%, likely skipped by students without institutional affiliation → **MAR** (conditional on occupation). Primary Likert items complete.\n\n"

# self-report bias paragraph
report += "## Self-Report Bias and Data Limitations\n\n"
report += (
    "All four datasets rely on self-reported measures of social media usage, attention, "
    "productivity, and/or academic performance. This introduces recall bias (respondents "
    "are unlikely to accurately remember precise usage hours), social desirability bias "
    "(respondents may underreport usage and overreport productivity), and measurement error "
    "(constructs like 'attention span' and 'addiction score' are operationalised differently "
    "across datasets with no shared validated instrument).\n\n"
    "Two datasets warrant explicit disclosure. **`student_habits_exam_performance`** is openly "
    "described as synthetically generated on Kaggle — findings cannot be interpreted as empirical "
    "evidence and must be labelled as synthetic. **`student_social_media_academic_impact`** spans "
    "110 countries, meaning constructs like 'addiction' and 'academic performance' are compared "
    "across different educational systems and cultural contexts without established measurement "
    "equivalence.\n"
)

# gender mapping for DS4
report += "\n## Recommended Cleaning Mappings\n\n"
report += "```python\n"
report += "# Gender normalisation for the attention survey\n"
report += "gender_map = {\n"
report += '    "Male":               "Male",\n'
report += '    "Female":             "Female",\n'
report += '    "Nonbinary":          "Non-binary or Other",\n'
report += '    "Non-binary":         "Non-binary or Other",\n'
report += '    "NB":                 "Non-binary or Other",\n'
report += '    "unsure":             "Non-binary or Other",\n'
report += '    "Trans":              "Non-binary or Other",\n'
report += '    "Non binary":         "Non-binary or Other",\n'
report += '    "There are others???":"Non-binary or Other",\n'
report += "}\n"
report += "# apply: df['Gender'] = df['Gender'].str.strip().map(gender_map)\n"
report += "```\n"

with open("outputs/03_data_quality.md", "w", encoding="utf-8") as f:
    f.write(report)

print("\nDone — saved to outputs/03_data_quality.md")