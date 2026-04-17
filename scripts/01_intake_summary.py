"""
01_intake_summary.py
Loads each dataset and produces a markdown intake report with
shape, types, missing values, duplicates, stats and relevance checks.
"""

import os
import pandas as pd

DATASET_DIR = "dataset"
OUTPUT = "outputs/01_intake_summary.md"
os.makedirs("outputs", exist_ok=True)

# datasets I want to check
files = [
    "screen_time_attention_productivity.csv",
    "social_media_addiction_productivity.csv",
    "student_social_media_academic_impact.csv",
    "social_media_content_mental_fatigue.csv",
    "student_habits_exam_performance.csv",
    "social_media_attention_mental_health_survey.csv",
]

# relevance answers - figured these out after looking at the columns
# format: (usage, attention, performance) each with (Y/N/P, justification)
relevance = {
    "screen_time_attention_productivity.csv": {
        "usage":       ("Y", "`avg_screen_time_hours`, `app_category`, `screen_time_period`"),
        "attention":   ("Y", "`attention_span_duration` directly captures concentration duration"),
        "performance": ("Y", "`productivity_level`, `work_strategy`, `uses_productivity_apps`"),
    },
    "social_media_addiction_productivity.csv": {
        "usage":       ("Y", "`daily_usage_minutes`, `posts_per_day`, `scroll_rate_per_minute`"),
        "attention":   ("N", "No direct attention/focus column; `fomo_score` is closest proxy"),
        "performance": ("Y", "`productivity_loss_score` explicitly measures productivity impact"),
    },
    "student_social_media_academic_impact.csv": {
        "usage":       ("Y", "`Avg_Daily_Usage_Hours`, `Most_Used_Platform`"),
        "attention":   ("N", "No attention/distraction column present"),
        "performance": ("Y", "`Affects_Academic_Performance` and `Addicted_Score` relate to grades"),
    },
    "social_media_content_mental_fatigue.csv": {
        "usage":       ("Y", "`daily_usage_minutes`, `platform`, `content_type`"),
        "attention":   ("P", "`mental_fatigue_level` is a proxy for cognitive load/distraction"),
        "performance": ("N", "No productivity or academic performance column present"),
    },
    "student_habits_exam_performance.csv": {
        "usage":       ("Y", "`social_media_hours` and `netflix_hours`"),
        "attention":   ("N", "No direct attention column; `study_hours_per_day` is a weak proxy"),
        "performance": ("Y", "`exam_score` and `attendance_percentage` are direct academic measures"),
    },
    "social_media_attention_mental_health_survey.csv": {
        "usage":       ("Y", "`Daily Time`, `Platforms`, and `Social Media Use` capture time and breadth of use"),
        "attention":   ("Y", "Q10 (distracted when busy), Q12 (easily distracted), Q14 (difficulty concentrating) are direct Likert-scale attention measures"),
        "performance": ("N", "No productivity or grades column; `Occupation` identifies students but captures no performance outcome"),
    },
}


def load(fname):
    """Try utf-8 first, fall back to latin-1."""
    path = os.path.join(DATASET_DIR, fname)
    try:
        return pd.read_csv(path, encoding="utf-8"), "utf-8"
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1"), "latin-1"


# --- build the summary table at the top ---
report = "# Social Media & Cognition — Dataset Intake Summary\n\n"
report += "> Generated automatically. **Y** = Yes | **N** = No | **P** = Partial / Proxy\n\n"
report += "## Quick-Reference Relevance Table\n\n"
report += "| Dataset | Measures Usage? | Measures Attention? | Measures Performance? |\n"
report += "|---------|:--------------:|:------------------:|:--------------------:|\n"

for f in files:
    r = relevance[f]
    report += f"| `{f}` | **{r['usage'][0]}** | **{r['attention'][0]}** | **{r['performance'][0]}** |\n"
report += "\n---\n\n"

# --- process each dataset ---
for fname in files:
    print(f"Processing {fname}...")
    df, enc = load(fname)

    report += f"## {fname}\n\n"
    report += f"_Encoding: {enc}_\n\n"
    report += f"**Shape:** {len(df):,} rows x {len(df.columns)} columns\n\n"

    # columns and dtypes
    report += "\n### Columns & Dtypes\n\n"
    report += "| Column | dtype |\n|--------|-------|\n"
    for col in df.columns:
        report += f"| `{col}` | {df[col].dtype} |\n"

    # missing values
    report += "\n\n### Missing Values\n\n"
    miss = df.isnull().sum()
    miss = miss[miss > 0]
    if len(miss) == 0:
        report += "_No missing values._\n"
    else:
        report += "| Column | Missing Count | Missing % |\n|--------|--------------|----------|\n"
        for col, cnt in miss.items():
            pct = round(cnt / len(df) * 100, 2)
            report += f"| `{col}` | {cnt} | {pct}% |\n"

    # duplicates
    report += f"\n\n**Duplicate rows:** {df.duplicated().sum()}\n"

    # first 3 rows
    report += "\n\n### First 3 Rows\n\n"
    report += df.head(3).to_markdown(index=False) + "\n"

    # numeric summary
    nums = df.select_dtypes(include="number")
    if not nums.empty:
        report += "\n\n### Numeric Summary (describe)\n\n"
        report += nums.describe().round(3).to_markdown() + "\n"

    # categorical columns
    cats = df.select_dtypes(exclude="number").columns
    if len(cats) > 0:
        report += "\n\n### Categorical Columns\n\n"
        for col in cats:
            nuniq = df[col].nunique()
            if nuniq <= 15:
                report += f"\n**`{col}`** — {nuniq} unique values\n\n"
                report += "| Value | Count | % |\n|-------|-------|---|\n"
                for val, cnt in df[col].value_counts(dropna=False).items():
                    report += f"| {val} | {cnt} | {cnt/len(df)*100:.1f}% |\n"
            else:
                samples = df[col].dropna().unique()[:5]
                sample_str = ", ".join(f"`{s}`" for s in samples)
                report += f"\n**`{col}`** — {nuniq} unique values. Sample: {sample_str}\n"

    # relevance assessment
    r = relevance[fname]
    report += "\n\n### Relevance Assessment\n\n"
    report += "| Question | Answer | Justification |\n|----------|--------|---------------|\n"
    report += f"| Measures social media **USAGE**? | **{r['usage'][0]}** | {r['usage'][1]} |\n"
    report += f"| Measures **ATTENTION** / focus / distraction? | **{r['attention'][0]}** | {r['attention'][1]} |\n"
    report += f"| Measures **PRODUCTIVITY** / grades / academic performance? | **{r['performance'][0]}** | {r['performance'][1]} |\n"

    report += "\n\n---\n"

# write it out
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(report)

print(f"\nDone — saved to {OUTPUT}")