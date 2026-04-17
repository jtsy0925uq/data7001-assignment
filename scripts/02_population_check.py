"""
02_population_check.py
Checks whether each dataset fits our target population (younger generation, 13-30).
Produces age distributions, histograms, and a cross-tab for the survey dataset.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATASET_DIR = "dataset"
os.makedirs("outputs", exist_ok=True)

# only the 4 surviving datasets
datasets = {
    "screen_time_attention_productivity.csv": {
        "age_col": "Age Group",
        "age_type": "categorical",
    },
    "student_habits_exam_performance.csv": {
        "age_col": "age",
        "age_type": "numeric",
    },
    "student_social_media_academic_impact.csv": {
        "age_col": "Age",
        "age_type": "numeric",
    },
    "social_media_attention_mental_health_survey.csv": {
        "age_col": "Age",
        "age_type": "numeric",
    },
}

report = "# Population Check — Younger Generation Fit\n\n"
report += "> **Target definitions:** Strict = ages 13–25 | Broad = ages 13–30\n\n---\n\n"

# we'll collect summary rows as we go
summary_rows = []

for fname, info in datasets.items():
    print(f"Checking {fname}...")
    df = pd.read_csv(os.path.join(DATASET_DIR, fname))
    age_col = info["age_col"]
    age_type = info["age_type"]
    short_name = fname.replace(".csv", "")

    report += f"## {short_name}\n\n"
    report += f"**Age column:** `{age_col}` ({age_type})\n\n"

    if age_type == "categorical":
        # bar chart for categorical age
        vc = df[age_col].value_counts()
        report += "### Full Age Distribution\n\n"
        report += "| Age Group | Count | % |\n|-----------|------:|--:|\n"
        for val, cnt in vc.items():
            report += f"| {val} | {cnt} | {cnt/len(df)*100:.1f}% |\n"

        fig, ax = plt.subplots(figsize=(8, 4))
        vc.plot(kind="bar", ax=ax, color="#5b9bd5")
        ax.set_title(f"Age Distribution — {short_name}")
        ax.set_ylabel("Count")
        plt.tight_layout()
        plt.savefig(f"outputs/age_dist_{short_name}.png", dpi=150)
        plt.close()

        # strict = Below 18 + 18-24
        strict_bins = ["Below 18", "18–24"]
        n_strict = df[df[age_col].isin(strict_bins)].shape[0]
        n_total = len(df)

        report += f"\n### Population Fit\n\n"
        report += "| Filter | Bins Included | n | % of Total |\n"
        report += "|--------|--------------|--:|:---------:|\n"
        report += f"| Strict 13–25 | 'Below 18' + '18–24' | {n_strict} | {n_strict/n_total*100:.1f}% |\n"
        report += f"| Broad 13–30  | Same bins ('25–34' unsplittable) | {n_strict} | {n_strict/n_total*100:.1f}% |\n"
        report += "\n> **Caveat:** The '25–34' bin contains 24 respondents spanning ages 25–34. "
        report += "Assuming uniform distribution, approximately 12 fall within 25–30, raising estimated "
        report += "broad coverage to ~86.0%. Exact filtering is not possible without raw age values.\n"

        summary_rows.append([f"`{fname}`", "Categorical", "Below 18 → 45+",
                            f"{n_strict} ({n_strict/n_total*100:.1f}%)",
                            f"~{n_strict} ({n_strict/n_total*100:.1f}%)",
                            "'25–34' bin unsplittable"])

    else:
        # numeric age — histogram + stats
        ages = df[age_col].dropna()
        stats = ages.describe()
        report += "### Full Age Distribution\n\n"
        report += "| Statistic | Value |\n|-----------|------:|\n"
        for s in ["min", "25%", "50%", "mean", "75%", "max"]:
            label = s if s != "50%" else "Median"
            if s == "mean":
                label = "Mean"
            elif s == "25%":
                label = "25th percentile"
            elif s == "75%":
                label = "75th percentile"
            elif s == "min":
                label = "Min"
            elif s == "max":
                label = "Max"
            report += f"| {label} | {stats[s]:.1f} |\n"

        # check for outliers
        if ages.max() > 60:
            report += f"\n> **Outlier flag:** Max age = {int(ages.max())} — likely data entry error. "
            report += f"Only {(ages > 60).sum()} respondent(s) aged above 60. "
            report += "Recommend dropping or capping at 60 during the cleaning phase.\n"

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(ages, bins=20, color="#5b9bd5", edgecolor="white")
        ax.set_title(f"Age Distribution — {short_name}")
        ax.set_xlabel("Age")
        ax.set_ylabel("Count")
        plt.tight_layout()
        plt.savefig(f"outputs/age_dist_{short_name}.png", dpi=150)
        plt.close()

        # population fit counts
        n_total = len(df)
        n_strict = int(((ages >= 13) & (ages <= 25)).sum())
        n_broad = int(((ages >= 13) & (ages <= 30)).sum())
        n_excluded = n_total - n_broad

        report += "\n### Population Fit\n\n"
        report += "| Filter | n | % of Total |\n|--------|--:|:---------:|\n"
        report += f"| Strict 13–25 | {n_strict} | {n_strict/n_total*100:.1f}% |\n"
        report += f"| Broad 13–30  | {n_broad} | {n_broad/n_total*100:.1f}% |\n"
        report += f"| Excluded (>30) | {n_excluded} | {n_excluded/n_total*100:.1f}% |\n"

        summary_rows.append([f"`{fname}`", "Numeric",
                            f"{int(ages.min())}–{int(ages.max())}",
                            f"{n_strict} ({n_strict/n_total*100:.1f}%)",
                            f"{n_broad} ({n_broad/n_total*100:.1f}%)",
                            ""])

    # special handling for the survey dataset — student status cross-tab
    if "survey" in fname:
        occ_col = "Occupation"
        student_mask = df[occ_col].isin(["University Student", "School Student"])
        n_students = student_mask.sum()

        report += "\n### Secondary Filter: Student Status\n\n"
        report += "| Filter | n | % of Total |\n|--------|--:|:---------:|\n"
        report += f"| University Student OR School Student | {n_students} | {n_students/n_total*100:.1f}% |\n"
        report += f"| Other occupations (Salaried Worker, Retired) | {n_total - n_students} | {(n_total-n_students)/n_total*100:.1f}% |\n"

        # cross-tab age bracket x occupation
        df["age_bracket"] = pd.cut(
            df[age_col],
            bins=[0, 17, 25, 30, 200],
            labels=["<=17", "18-25", "26-30", "31+"]
        )
        xtab = pd.crosstab(df["age_bracket"], df[occ_col], margins=True, margins_name="All")
        report += "\n### Cross-tab: Age Bracket × Occupation\n\n"
        report += xtab.to_markdown() + "\n"

        # update the summary note
        summary_rows[-1][-1] = f"Age-{int(ages.max())} outlier present; student-status filter yields {n_students} ({n_students/n_total*100:.1f}%)"

    # demographics
    report += "\n### Other Demographics\n\n"
    if "Gender" in df.columns or "gender" in df.columns:
        gcol = "Gender" if "Gender" in df.columns else "gender"
        report += f"**Gender:**\n"
        for val, cnt in df[gcol].value_counts().items():
            report += f"- {val}: {cnt} ({cnt/n_total*100:.1f}%)\n"

    if "Academic_Level" in df.columns:
        report += f"\n**Academic Level:**\n"
        for val, cnt in df["Academic_Level"].value_counts().items():
            report += f"- {val}: {cnt} ({cnt/n_total*100:.1f}%)\n"

    if "Country" in df.columns:
        report += f"\n**Top 10 Countries:**\n"
        for val, cnt in df["Country"].value_counts().head(10).items():
            report += f"- {val}: {cnt} ({cnt/n_total*100:.1f}%)\n"

    if "Occupation" in df.columns:
        report += f"\n**Occupation:**\n"
        for val, cnt in df["Occupation"].value_counts().items():
            report += f"- {val}: {cnt} ({cnt/n_total*100:.1f}%)\n"

    report += "\n---\n\n"

# insert summary table at the top (after the header)
summary_table = "## Summary Table\n\n"
summary_table += "| Dataset | Age Type | Age Range in Data | n Strict 13–25 | n Broad 13–30 | Notes |\n"
summary_table += "|---------|----------|:-----------------:|:--------------:|:-------------:|-------|\n"
for row in summary_rows:
    summary_table += "| " + " | ".join(row) + " |\n"
summary_table += "\n---\n\n"

# stick it right after the header
header_end = report.index("---\n\n") + len("---\n\n")
report = report[:header_end] + summary_table + report[header_end:]

# conclusion
report += "## Conclusion\n\n"
report += (
    "**`student_habits_exam_performance.csv`** has the tightest fit to the target population: "
    "its age range (17–24) sits entirely within both the strict and broad definitions (100.0% coverage), "
    "and it provides a direct continuous `exam_score` outcome variable. "
    "**`student_social_media_academic_impact.csv`** is a close second at 100.0% broad coverage, "
    "with an explicit `Academic_Level` column enabling secondary filtering by study stage. "
    "**`social_media_attention_mental_health_survey.csv`** achieves 81.5% broad coverage but may require "
    "additional filtering by `Occupation` (University Student / School Student) to exclude salaried workers "
    "and retired respondents who fall within the age range but outside the conceptual younger-generation target; "
    "it remains the strongest dataset for direct attention and distraction measures across all four surviving datasets. "
    "**`screen_time_attention_productivity.csv`** requires the most caution: categorical age bins prevent "
    "precise filtering, and the '25–34' bin straddles both population definitions.\n"
)

with open("outputs/02_population_check.md", "w", encoding="utf-8") as f:
    f.write(report)

print("Done — saved to outputs/02_population_check.md")