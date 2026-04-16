"""
02_population_check.py
======================
DATA7001 – Social Media & Cognitive Functioning Project
--------------------------------------------------------
Runs a population-fit check on the four surviving datasets to assess
how well each covers our target population: the 'younger generation'.

Two age definitions are tested:
  - Strict: ages 13–25 (adolescents and emerging adults)
  - Broad:  ages 13–30 (includes graduate students and early-career)

For each dataset the script:
  1. Identifies and reports the age column (numeric or categorical).
  2. Produces descriptive statistics / value counts for the age variable.
  3. Plots and saves an age distribution chart (histogram or bar chart).
  4. Reports sample sizes retained under each age filter.
  5. (Survey dataset only) produces a secondary student-status filter
     breakdown and a cross-tab of age bracket × occupation.
  6. Summarises other demographic variables (gender, academic level,
     country where available).

Outputs
-------
  outputs/02_population_check.md                              — full report
  outputs/age_dist_screen_time_attention_productivity.png     — bar chart
  outputs/age_dist_student_habits_exam_performance.png        — histogram
  outputs/age_dist_student_social_media_academic_impact.png   — histogram
  outputs/age_dist_social_media_attention_mental_health_survey.png — histogram

Usage
-----
  python scripts/02_population_check.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")                     # non-interactive backend for saving files
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ── Paths ─────────────────────────────────────────────────────────────────────
DATASET_DIR = "dataset"
OUT_DIR     = "outputs"
REPORT_PATH = os.path.join(OUT_DIR, "02_population_check.md")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Colour palette ────────────────────────────────────────────────────────────
C_ALL    = "#94a3b8"   # slate  — full-population bars (out of range)
C_STRICT = "#6366f1"   # indigo — strict 13-25 in-range bars
C_BROAD  = "#a78bfa"   # violet — broad 26-30 extension bars
C_EDGE   = "#1e1b4b"   # dark navy — bar edges

# ── Age filter bounds ─────────────────────────────────────────────────────────
STRICT_MIN, STRICT_MAX = 13, 25
BROAD_MIN,  BROAD_MAX  = 13, 30


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_csv(fname):
    """Load CSV with utf-8 fallback to latin-1."""
    path = os.path.join(DATASET_DIR, fname)
    for enc in ("utf-8", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Cannot decode {fname}")


def pct_str(n, total):
    """Return 'n (xx.x%)' formatted string."""
    return f"{n} ({n / total * 100:.1f}%)"


def colour_histogram_bars(patches, edges, strict_max, broad_max):
    """Colour histogram bars by whether they fall in strict, broad, or outside range."""
    for patch, left_edge in zip(patches, edges):
        bar_mid = left_edge + 0.5
        if STRICT_MIN <= bar_mid <= strict_max:
            patch.set_facecolor(C_STRICT)
        elif strict_max < bar_mid <= broad_max:
            patch.set_facecolor(C_BROAD)
        else:
            patch.set_facecolor(C_ALL)


def add_age_cutoff_legend(ax):
    """Add a consistent legend for the age histogram colour scheme."""
    ax.legend(
        handles=[
            Patch(color=C_STRICT, label=f"Strict {STRICT_MIN}–{STRICT_MAX}"),
            Patch(color=C_BROAD,  label=f"Broad {STRICT_MAX + 1}–{BROAD_MAX}"),
            Patch(color=C_ALL,    label="Outside target range"),
            plt.Line2D([0], [0], color="#ef4444", ls="--", lw=1.2, label=f"Cutoff {STRICT_MAX}"),
            plt.Line2D([0], [0], color="#f97316", ls="--", lw=1.2, label=f"Cutoff {BROAD_MAX}"),
        ],
        fontsize=8,
    )


def save_fig(filename):
    """Save current figure and close."""
    path = os.path.join(OUT_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved {path}")


# ── Per-dataset analysis functions ────────────────────────────────────────────

def analyse_screen_time(df):
    """
    DS1: screen_time_attention_productivity.csv
    Age column is categorical ('Age Group'), so filtering is approximate.
    """
    fname  = "screen_time_attention_productivity.csv"
    n_total = len(df)

    # Ordered age bins as they appear in the data
    ordered_bins = ["Below 18", "18\u201324", "25\u201334", "35\u201344", "45 and above"]
    vc = df["Age Group"].value_counts().reindex(ordered_bins, fill_value=0)

    # Bins that fall entirely within strict 13-25
    strict_bins = ["Below 18", "18\u201324"]
    n_strict    = int(df["Age Group"].isin(strict_bins).sum())
    n_broad     = n_strict   # 25-34 bin cannot be split; flagged as caveat
    n_2534_bin  = int(vc.get("25\u201334", 0))

    # ── Chart: bar chart (categorical age) ────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = [C_STRICT if b in strict_bins else C_ALL for b in vc.index]
    bars   = ax.bar(vc.index, vc.values, color=colors, edgecolor=C_EDGE, linewidth=0.8)
    ax.bar_label(
        bars,
        labels=[f"{v}\n({v / n_total * 100:.0f}%)" for v in vc.values],
        padding=4, fontsize=9
    )
    ax.set_title(
        "Age Group Distribution\nscreen_time_attention_productivity.csv",
        fontweight="bold"
    )
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Count")
    ax.set_ylim(0, vc.max() * 1.3)
    ax.legend(
        handles=[
            Patch(color=C_STRICT, label="Within strict 13–25"),
            Patch(color=C_ALL,    label="Outside target range"),
        ],
        fontsize=9,
    )
    plt.tight_layout()
    save_fig("age_dist_screen_time_attention_productivity.png")

    # ── Gender ────────────────────────────────────────────────────────────────
    gender = df["Gender"].value_counts(dropna=False)

    return fname, n_total, vc, n_strict, n_broad, n_2534_bin, gender


def analyse_student_habits(df):
    """
    DS2: student_habits_exam_performance.csv
    Numeric age column.
    """
    fname   = "student_habits_exam_performance.csv"
    age     = df["age"].dropna()
    n_total = len(df)

    n_strict = int(((age >= STRICT_MIN) & (age <= STRICT_MAX)).sum())
    n_broad  = int(((age >= BROAD_MIN)  & (age <= BROAD_MAX)).sum())
    desc     = age.describe().round(2)

    # ── Chart: histogram ──────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bins = np.arange(age.min() - 0.5, age.max() + 1.5, 1)
    _, edges, patches = ax.hist(age, bins=bins, edgecolor=C_EDGE, linewidth=0.6, color=C_ALL)
    colour_histogram_bars(patches, edges, STRICT_MAX, BROAD_MAX)
    ax.axvline(STRICT_MAX, color="#ef4444", ls="--", lw=1.2)
    ax.axvline(BROAD_MAX,  color="#f97316", ls="--", lw=1.2)
    ax.set_title(
        "Age Distribution\nstudent_habits_exam_performance.csv",
        fontweight="bold"
    )
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    add_age_cutoff_legend(ax)
    plt.tight_layout()
    save_fig("age_dist_student_habits_exam_performance.png")

    gender = df["gender"].value_counts(dropna=False)

    return fname, n_total, desc, n_strict, n_broad, gender


def analyse_student_impact(df):
    """
    DS3: student_social_media_academic_impact.csv
    Numeric age column (capital 'Age').
    """
    fname   = "student_social_media_academic_impact.csv"
    age     = df["Age"].dropna()
    n_total = len(df)

    n_strict = int(((age >= STRICT_MIN) & (age <= STRICT_MAX)).sum())
    n_broad  = int(((age >= BROAD_MIN)  & (age <= BROAD_MAX)).sum())
    desc     = age.describe().round(2)

    # ── Chart: histogram ──────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bins = np.arange(age.min() - 0.5, age.max() + 1.5, 1)
    _, edges, patches = ax.hist(age, bins=bins, edgecolor=C_EDGE, linewidth=0.6, color=C_ALL)
    colour_histogram_bars(patches, edges, STRICT_MAX, BROAD_MAX)
    ax.axvline(STRICT_MAX, color="#ef4444", ls="--", lw=1.2)
    ax.axvline(BROAD_MAX,  color="#f97316", ls="--", lw=1.2)
    ax.set_title(
        "Age Distribution\nstudent_social_media_academic_impact.csv",
        fontweight="bold"
    )
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    add_age_cutoff_legend(ax)
    plt.tight_layout()
    save_fig("age_dist_student_social_media_academic_impact.png")

    gender        = df["Gender"].value_counts(dropna=False)
    academic_lvl  = df["Academic_Level"].value_counts(dropna=False)
    top_countries = df["Country"].value_counts(dropna=False).head(10)

    return fname, n_total, desc, n_strict, n_broad, gender, academic_lvl, top_countries


def analyse_survey(df):
    """
    DS4: social_media_attention_mental_health_survey.csv
    Numeric float age; also performs student-status secondary filter
    and cross-tab of age bracket × occupation.
    """
    fname   = "social_media_attention_mental_health_survey.csv"
    age     = df["Age"].dropna()
    n_total = len(df)

    n_strict = int(((age >= STRICT_MIN) & (age <= STRICT_MAX)).sum())
    n_broad  = int(((age >= BROAD_MIN)  & (age <= BROAD_MAX)).sum())
    n_over60 = int((age > 60).sum())
    desc     = age.describe().round(2)

    # Student-status filter
    student_occupations = ["University Student", "School Student"]
    n_student = int(df["Occupation"].isin(student_occupations).sum())

    # Cross-tab: age bracket × occupation
    df_ct = df.copy()
    df_ct["age_bracket"] = pd.cut(
        df_ct["Age"],
        bins=[0, 17, 25, 30, 200],
        labels=["<=17", "18-25", "26-30", "31+"],
        right=True,
    )
    crosstab = pd.crosstab(df_ct["age_bracket"], df_ct["Occupation"], margins=True)

    # ── Chart: histogram (clip display at 80 to avoid outlier distorting axis) ──
    fig, ax = plt.subplots(figsize=(8, 4.5))
    age_clipped = age.clip(upper=80)
    bins = np.arange(max(0, age_clipped.min() - 0.5), age_clipped.max() + 1.5, 1)
    _, edges, patches = ax.hist(
        age_clipped, bins=bins, edgecolor=C_EDGE, linewidth=0.6, color=C_ALL
    )
    colour_histogram_bars(patches, edges, STRICT_MAX, BROAD_MAX)
    ax.axvline(STRICT_MAX, color="#ef4444", ls="--", lw=1.2)
    ax.axvline(BROAD_MAX,  color="#f97316", ls="--", lw=1.2)
    ax.set_title(
        "Age Distribution\nsocial_media_attention_mental_health_survey.csv\n"
        "(display clipped at 80; 3 respondents aged >60 exist in data)",
        fontweight="bold",
        fontsize=9,
    )
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    add_age_cutoff_legend(ax)
    plt.tight_layout()
    save_fig("age_dist_social_media_attention_mental_health_survey.png")

    gender     = df["Gender"].value_counts(dropna=False)
    occupation = df["Occupation"].value_counts(dropna=False)

    return (
        fname, n_total, desc, n_strict, n_broad,
        n_over60, n_student, crosstab, gender, occupation,
    )


# ── Markdown builder ──────────────────────────────────────────────────────────

def build_report(results_ds1, results_ds2, results_ds3, results_ds4):
    fname1, n1, vc1, n1s, n1b, n1_2534, g1 = results_ds1
    fname2, n2, desc2, n2s, n2b, g2        = results_ds2
    fname3, n3, desc3, n3s, n3b, g3, al3, cty3 = results_ds3
    (fname4, n4, desc4, n4s, n4b,
     n4_over60, n4_student, ct4, g4, occ4) = results_ds4

    lines = []

    # ── Title & legend key ────────────────────────────────────────────────────
    lines += [
        "# Population Check — Younger Generation Fit\n",
        "> **Target definitions:** Strict = ages 13–25 | Broad = ages 13–30\n",
        "---\n",
    ]

    # ── Summary table ─────────────────────────────────────────────────────────
    lines += [
        "## Summary Table\n",
        "| Dataset | Age Type | Age Range in Data | n Strict 13–25 | n Broad 13–30 | Notes |",
        "|---------|----------|:-----------------:|:--------------:|:-------------:|-------|",
        (
            f"| `{fname1}` | Categorical | Below 18 → 45 and above "
            f"| {pct_str(n1s, n1)} | ~{pct_str(n1s, n1)} "
            f"| '25–34' bin unsplittable; ~{int(n1_2534 * 0.5)} extra rows possible under broad |"
        ),
        (
            f"| `{fname2}` | Numeric | {int(desc2['min'])}–{int(desc2['max'])} "
            f"| {pct_str(n2s, n2)} | {pct_str(n2b, n2)} "
            f"| Tightest age range; entire dataset within target |"
        ),
        (
            f"| `{fname3}` | Numeric | {int(desc3['min'])}–{int(desc3['max'])} "
            f"| {pct_str(n3s, n3)} | {pct_str(n3b, n3)} "
            f"| Global student sample; `Academic_Level` available for secondary filter |"
        ),
        (
            f"| `{fname4}` | Numeric | {int(desc4['min'])}–{int(desc4['max'])} "
            f"| {pct_str(n4s, n4)} | {pct_str(n4b, n4)} "
            f"| Age-{int(desc4['max'])} outlier present; student-status filter yields {pct_str(n4_student, n4)} |"
        ),
        "\n---\n",
    ]

    # ── DS1 ───────────────────────────────────────────────────────────────────
    lines += [
        f"## 1. {fname1}\n",
        "**Age column:** `Age Group` (categorical ordinal, 5 bins)\n",
        "### Full Age Distribution\n",
        "| Age Group | Count | % |",
        "|-----------|------:|--:|",
    ]
    for grp, cnt in vc1.items():
        lines.append(f"| {grp} | {cnt} | {cnt / n1 * 100:.1f}% |")
    lines += [
        "",
        f"![Age group bar chart](age_dist_screen_time_attention_productivity.png)\n",
        "### Population Fit\n",
        "| Filter | Bins Included | n | % of Total |",
        "|--------|--------------|--:|:---------:|",
        f"| Strict 13–25 | 'Below 18' + '18–24' | {n1s} | {n1s / n1 * 100:.1f}% |",
        f"| Broad 13–30  | Same bins ('25–34' unsplittable) | {n1s} | {n1s / n1 * 100:.1f}% |",
        "",
        (
            f"> **Caveat:** The '25–34' bin contains {n1_2534} respondents spanning ages 25–34. "
            f"Assuming uniform distribution, approximately {int(n1_2534 * 0.5)} fall within 25–30, "
            f"raising estimated broad coverage to ~{(n1s + int(n1_2534 * 0.5)) / n1 * 100:.1f}%. "
            f"Exact filtering is not possible without raw age values."
        ),
        "\n### Other Demographics\n",
        "**Gender:**",
    ]
    for val, cnt in g1.items():
        lines.append(f"- {val}: {cnt} ({cnt / n1 * 100:.1f}%)")
    lines.append("\n---\n")

    # ── DS2 ───────────────────────────────────────────────────────────────────
    lines += [
        f"## 2. {fname2}\n",
        "**Age column:** `age` (numeric integer)\n",
        "### Full Age Distribution\n",
        "| Statistic | Value |",
        "|-----------|------:|",
    ]
    for label, key in [("Min", "min"), ("25th percentile", "25%"), ("Median", "50%"),
                       ("Mean", "mean"), ("75th percentile", "75%"), ("Max", "max")]:
        lines.append(f"| {label} | {desc2[key]} |")
    lines += [
        "",
        f"![Age histogram](age_dist_student_habits_exam_performance.png)\n",
        "### Population Fit\n",
        "| Filter | n | % of Total |",
        "|--------|--:|:---------:|",
        f"| Strict 13–25 | {n2s} | {n2s / n2 * 100:.1f}% |",
        f"| Broad 13–30  | {n2b} | {n2b / n2 * 100:.1f}% |",
        f"| Excluded (>30) | {n2 - n2b} | {(n2 - n2b) / n2 * 100:.1f}% |",
        "\n### Other Demographics\n",
        "**Gender:**",
    ]
    for val, cnt in g2.items():
        lines.append(f"- {val}: {cnt} ({cnt / n2 * 100:.1f}%)")
    lines.append("\n---\n")

    # ── DS3 ───────────────────────────────────────────────────────────────────
    lines += [
        f"## 3. {fname3}\n",
        "**Age column:** `Age` (numeric integer)\n",
        "### Full Age Distribution\n",
        "| Statistic | Value |",
        "|-----------|------:|",
    ]
    for label, key in [("Min", "min"), ("25th percentile", "25%"), ("Median", "50%"),
                       ("Mean", "mean"), ("75th percentile", "75%"), ("Max", "max")]:
        lines.append(f"| {label} | {desc3[key]} |")
    lines += [
        "",
        f"![Age histogram](age_dist_student_social_media_academic_impact.png)\n",
        "### Population Fit\n",
        "| Filter | n | % of Total |",
        "|--------|--:|:---------:|",
        f"| Strict 13–25 | {n3s} | {n3s / n3 * 100:.1f}% |",
        f"| Broad 13–30  | {n3b} | {n3b / n3 * 100:.1f}% |",
        f"| Excluded (>30) | {n3 - n3b} | {(n3 - n3b) / n3 * 100:.1f}% |",
        "\n### Other Demographics\n",
        "**Gender:**",
    ]
    for val, cnt in g3.items():
        lines.append(f"- {val}: {cnt} ({cnt / n3 * 100:.1f}%)")
    lines += ["", "**Academic Level:**"]
    for val, cnt in al3.items():
        lines.append(f"- {val}: {cnt} ({cnt / n3 * 100:.1f}%)")
    lines += ["", "**Top 10 Countries:**"]
    for val, cnt in cty3.items():
        lines.append(f"- {val}: {cnt} ({cnt / n3 * 100:.1f}%)")
    lines.append("\n---\n")

    # ── DS4 ───────────────────────────────────────────────────────────────────
    lines += [
        f"## 4. {fname4}\n",
        "**Age column:** `Age` (numeric float, collected via Google Form)\n",
        "### Full Age Distribution\n",
        "| Statistic | Value |",
        "|-----------|------:|",
    ]
    for label, key in [("Min", "min"), ("25th percentile", "25%"), ("Median", "50%"),
                       ("Mean", "mean"), ("75th percentile", "75%"), ("Max", "max")]:
        lines.append(f"| {label} | {desc4[key]} |")
    lines += [
        "",
        (
            f"> **Outlier flag:** Max age = {int(desc4['max'])} — likely a data entry error. "
            f"Only {n4_over60} respondent(s) aged above 60. "
            f"Recommend dropping or capping at 60 during the cleaning phase."
        ),
        "",
        f"![Age histogram](age_dist_social_media_attention_mental_health_survey.png)\n",
        "### Population Fit\n",
        "| Filter | n | % of Total |",
        "|--------|--:|:---------:|",
        f"| Strict 13–25 | {n4s} | {n4s / n4 * 100:.1f}% |",
        f"| Broad 13–30  | {n4b} | {n4b / n4 * 100:.1f}% |",
        f"| Excluded (>30) | {n4 - n4b} | {(n4 - n4b) / n4 * 100:.1f}% |",
        "\n### Secondary Filter: Student Status\n",
        "| Filter | n | % of Total |",
        "|--------|--:|:---------:|",
        f"| University Student OR School Student | {n4_student} | {n4_student / n4 * 100:.1f}% |",
        f"| Other occupations (Salaried Worker, Retired) | {n4 - n4_student} | {(n4 - n4_student) / n4 * 100:.1f}% |",
        "\n### Cross-tab: Age Bracket × Occupation\n",
        ct4.to_markdown(),
        "",
        (
            f"> **Interpretation:** The strict age filter (13–25) captures {n4s} rows ({n4s / n4 * 100:.1f}%), "
            f"while the student-status filter captures {n4_student} rows ({n4_student / n4 * 100:.1f}%). "
            f"The cross-tab above shows the overlap between age bracket and occupation — "
            f"the intersection of both filters provides the most conservative target-population subset."
        ),
        "\n### Other Demographics\n",
        "**Gender** _(raw — 7 non-binary label variants require normalisation before analysis)_**:**",
    ]
    for val, cnt in g4.items():
        lines.append(f"- {val}: {cnt} ({cnt / n4 * 100:.1f}%)")
    lines += ["", "**Occupation:**"]
    for val, cnt in occ4.items():
        lines.append(f"- {val}: {cnt} ({cnt / n4 * 100:.1f}%)")
    lines.append("\n---\n")

    # ── Conclusion ────────────────────────────────────────────────────────────
    lines += [
        "## Conclusion\n",
        (
            f"**`{fname2}`** has the tightest fit to the target population: "
            f"its age range ({int(desc2['min'])}–{int(desc2['max'])}) sits entirely within both the strict "
            f"and broad definitions ({n2b / n2 * 100:.1f}% coverage), and it provides a direct continuous "
            f"`exam_score` outcome variable. "
            f"**`{fname3}`** is a close second at {n3b / n3 * 100:.1f}% broad coverage, with an explicit "
            f"`Academic_Level` column enabling secondary filtering by study stage. "
            f"**`{fname4}`** achieves {n4b / n4 * 100:.1f}% broad coverage but may require additional "
            f"filtering by `Occupation` (University Student / School Student) to exclude salaried workers "
            f"and retired respondents who fall within the age range but outside the conceptual "
            f"younger-generation target; it remains the strongest dataset for direct attention and "
            f"distraction measures across all four surviving datasets. "
            f"**`{fname1}`** requires the most caution: categorical age bins prevent precise filtering, "
            f"and the '25–34' bin straddles both population definitions."
        ),
    ]

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Running population check...\n")

    print("  Loading and analysing DS1: screen_time_attention_productivity.csv")
    df1 = load_csv("screen_time_attention_productivity.csv")
    results_ds1 = analyse_screen_time(df1)

    print("  Loading and analysing DS2: student_habits_exam_performance.csv")
    df2 = load_csv("student_habits_exam_performance.csv")
    results_ds2 = analyse_student_habits(df2)

    print("  Loading and analysing DS3: student_social_media_academic_impact.csv")
    df3 = load_csv("student_social_media_academic_impact.csv")
    results_ds3 = analyse_student_impact(df3)

    print("  Loading and analysing DS4: social_media_attention_mental_health_survey.csv")
    df4 = load_csv("social_media_attention_mental_health_survey.csv")
    results_ds4 = analyse_survey(df4)

    print("\nBuilding markdown report...")
    report = build_report(results_ds1, results_ds2, results_ds3, results_ds4)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nDone.")
    print(f"  Report : {REPORT_PATH}")
    print(f"  Charts : {OUT_DIR}/age_dist_*.png")


if __name__ == "__main__":
    main()
