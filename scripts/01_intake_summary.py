"""
01_intake_summary.py
====================
DATA7001 – Social Media & Cognitive Functioning Project
--------------------------------------------------------
Loads each surviving dataset, produces a structured intake summary
including shape, dtypes, missing values, duplicates, descriptive
statistics, and categorical value counts.

For each dataset answers three relevance questions:
  - Does it measure social media USAGE?
  - Does it measure ATTENTION / concentration / distraction?
  - Does it measure PRODUCTIVITY / grades / academic performance?

Output
------
  outputs/01_intake_summary.md  — full markdown report

Usage
-----
  python scripts/01_intake_summary.py
"""

import os
import pandas as pd

# ── Paths ─────────────────────────────────────────────────────────────────────
DATASET_DIR = "dataset"
OUTPUT_PATH = os.path.join("outputs", "01_intake_summary.md")
os.makedirs("outputs", exist_ok=True)

# ── Datasets to process ───────────────────────────────────────────────────────
FILES = [
    "screen_time_attention_productivity.csv",
    "social_media_addiction_productivity.csv",
    "student_social_media_academic_impact.csv",
    "social_media_content_mental_fatigue.csv",
    "student_habits_exam_performance.csv",
    "social_media_attention_mental_health_survey.csv",
]

# ── Relevance annotations (manually assessed per column audit) ────────────────
# Y = Yes  |  N = No  |  P = Partial / Proxy
RELEVANCE = {
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


# ── Helper functions ──────────────────────────────────────────────────────────

def load_csv(fname):
    """Load a CSV, trying utf-8 then latin-1 encoding."""
    path = os.path.join(DATASET_DIR, fname)
    for enc in ("utf-8", "latin-1"):
        try:
            df = pd.read_csv(path, encoding=enc)
            return df, enc
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {fname} with utf-8 or latin-1.")


def section(title, content):
    """Return a markdown ### section block."""
    return f"\n### {title}\n\n{content}\n"


def build_missing_table(df):
    """Return a markdown table of columns with missing values, or a 'none' note."""
    miss_count = df.isnull().sum()
    miss_pct   = (miss_count / len(df) * 100).round(2)
    missing    = pd.DataFrame({"Missing Count": miss_count, "Missing %": miss_pct})
    missing    = missing[missing["Missing Count"] > 0]

    if missing.empty:
        return "_No missing values detected._"

    rows = "| Column | Missing Count | Missing % |\n|--------|:------------:|:---------:|\n"
    for col, row in missing.iterrows():
        rows += f"| `{col}` | {int(row['Missing Count']):,} | {row['Missing %']}% |\n"
    return rows


def build_categorical_section(df):
    """
    For columns with <= 15 unique values: full value_counts table.
    For columns with  > 15 unique values: unique count + 5 sample values.
    """
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()
    if not cat_cols:
        return "_No categorical columns._"

    parts = []
    for col in cat_cols:
        n_unique = df[col].nunique()
        if n_unique <= 15:
            vc = df[col].value_counts(dropna=False)
            tbl = f"**`{col}`** — {n_unique} unique values\n\n"
            tbl += "| Value | Count | % |\n|-------|------:|---:|\n"
            for val, cnt in vc.items():
                tbl += f"| {val} | {cnt:,} | {cnt / len(df) * 100:.1f}% |\n"
        else:
            samples = ", ".join(f"`{s}`" for s in df[col].dropna().unique()[:5])
            tbl = (
                f"**`{col}`** — {n_unique} unique values "
                f"_(>15, showing 5 samples)_\n\nSamples: {samples}\n"
            )
        parts.append(tbl)

    return "\n".join(parts)


def build_dataset_section(fname):
    """Build the full markdown section for one dataset."""
    df, enc = load_csv(fname)
    n_rows, n_cols = df.shape
    lines = []

    # Header
    lines.append(f"## {fname}\n")
    lines.append(f"_Encoding detected: {enc}_\n")
    lines.append(f"**Shape:** {n_rows:,} rows × {n_cols} columns\n")

    # Columns & dtypes
    col_table = "| Column | dtype |\n|--------|-------|\n"
    for col in df.columns:
        col_table += f"| `{col}` | `{df[col].dtype}` |\n"
    lines.append(section("Columns & Dtypes", col_table))

    # Missing values
    lines.append(section("Missing Values", build_missing_table(df)))

    # Duplicates
    dup = df.duplicated().sum()
    lines.append(f"**Duplicate rows:** {dup:,}\n")

    # First 3 rows
    lines.append(section("First 3 Rows", df.head(3).to_markdown(index=False)))

    # Numeric describe
    num_df = df.select_dtypes(include="number")
    if not num_df.empty:
        lines.append(section(
            "Numeric Summary — describe()",
            num_df.describe().round(3).to_markdown()
        ))

    # Categorical value counts
    lines.append(section("Categorical Columns", build_categorical_section(df)))

    # Relevance assessment
    rel = RELEVANCE[fname]
    rel_table = (
        "| Question | Answer | Justification |\n"
        "|----------|:------:|---------------|\n"
    )
    rel_table += f"| Measures social media **USAGE**? | **{rel['usage'][0]}** | {rel['usage'][1]} |\n"
    rel_table += f"| Measures **ATTENTION** / focus / distraction? | **{rel['attention'][0]}** | {rel['attention'][1]} |\n"
    rel_table += f"| Measures **PRODUCTIVITY** / grades / academic performance? | **{rel['performance'][0]}** | {rel['performance'][1]} |\n"
    lines.append(section("Relevance Assessment", rel_table))

    lines.append("---\n")
    return "\n".join(lines)


# ── Summary table ─────────────────────────────────────────────────────────────

def build_summary_table():
    header = (
        "# Social Media & Cognition — Dataset Intake Summary\n\n"
        "> **Y** = Yes | **N** = No | **P** = Partial / Proxy\n\n"
        "## Quick-Reference Relevance Table\n\n"
        "| Dataset | Measures Usage? | Measures Attention? | Measures Performance? |\n"
        "|---------|:--------------:|:------------------:|:--------------------:|\n"
    )
    for fname in FILES:
        rel = RELEVANCE[fname]
        header += (
            f"| `{fname}` "
            f"| **{rel['usage'][0]}** "
            f"| **{rel['attention'][0]}** "
            f"| **{rel['performance'][0]}** |\n"
        )
    header += "\n---\n\n"
    return header


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Building intake summary report...")
    report = build_summary_table()

    for fname in FILES:
        print(f"  Processing {fname}...")
        report += build_dataset_section(fname)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nDone. Report saved to: {OUTPUT_PATH}")
    print(f"Total size: {len(report):,} characters")


if __name__ == "__main__":
    main()
