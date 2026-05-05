"""


  Source A — student_productivity_distraction_dataset_20000.csv (20,000 rows)
             Columns include: social_media_hours, focus_score, final_grade,
             study_hours_per_day, sleep_hours, attendance_percentage, etc.

  Source B — student_habits_exam_performance_filtered.csv (1,000 rows)
             Columns include: social_media_hours, exam_score, study_hours_per_day,
             sleep_hours, attendance_percentage, mental_health_rating, etc.

"""

import sys
import os
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

# ── File paths ────────────────────────────────────────────────────────────────
PATH_PRODUCTIVITY = os.path.join(
    "dataset", "filtered", "student_productivity_distraction_dataset_20000.csv"
)
PATH_HABITS = os.path.join(
    "dataset", "filtered", "student_habits_exam_performance_filtered.csv"
)
PATH_OUTPUT = os.path.join("dataset", "master_student_dataset.csv")

# Columns where negative values are physically impossible
HOURS_COLUMNS       = ["study_hours_per_day", "social_media_hours", "sleep_hours"]
PERCENTAGE_COLUMNS  = ["attendance_percentage"]


# ── Section 1: Load Data ──────────────────────────────────────────────────────

def load_datasets():
    """Load both CSVs and print their shapes and column names for verification."""
    print("=" * 60)
    print("SECTION 1 — Loading datasets")
    print("=" * 60)

    df_prod = pd.read_csv(PATH_PRODUCTIVITY)
    df_hab  = pd.read_csv(PATH_HABITS)

    print(f"\n[Source A] student_productivity_distraction_dataset_20000.csv")
    print(f"  Shape   : {df_prod.shape[0]:,} rows × {df_prod.shape[1]} columns")
    print(f"  Columns : {list(df_prod.columns)}")

    print(f"\n[Source B] student_habits_exam_performance_filtered.csv")
    print(f"  Shape   : {df_hab.shape[0]:,} rows × {df_hab.shape[1]} columns")
    print(f"  Columns : {list(df_hab.columns)}")

    return df_prod, df_hab


# ── Section 2: Harmonise Schemas ─────────────────────────────────────────────

def harmonise(df_prod, df_hab):
    """
    Align both datasets to a shared schema:
      - Rename grade/score columns to 'academic_score'.
      - Standardise student_id to string.
      - Add a 'source' label column.
      - Keep only the columns shared by both datasets.
    Returns the two harmonised DataFrames.
    """
    print("\n" + "=" * 60)
    print("SECTION 2 — Harmonising schemas")
    print("=" * 60)

    # -- 2a. Rename grade columns to a common name --------------------------
    df_prod = df_prod.rename(columns={"final_grade": "academic_score"})
    df_hab  = df_hab.rename(columns={"exam_score":   "academic_score"})
    print("\n[2a] Renamed 'final_grade' → 'academic_score' (Source A)")
    print("     Renamed 'exam_score'   → 'academic_score' (Source B)")

    # -- 2b. Standardise student_id to string --------------------------------
    # Source A: integer IDs (1, 2, 3 …)  → "1", "2", "3"
    # Source B: string IDs ("S1000" …)   → kept as-is (already strings)
    df_prod["student_id"] = df_prod["student_id"].astype(str)
    df_hab["student_id"]  = df_hab["student_id"].astype(str)
    print("\n[2b] Standardised student_id to string in both datasets")
    print(f"     Source A sample IDs : {df_prod['student_id'].head(3).tolist()}")
    print(f"     Source B sample IDs : {df_hab['student_id'].head(3).tolist()}")

    # -- 2c. Add source label ------------------------------------------------
    df_prod = df_prod.copy()
    df_hab  = df_hab.copy()
    df_prod["source"] = "productivity"
    df_hab["source"]  = "habits"
    print("\n[2c] Added 'source' column")
    print("     Source A → 'productivity'")
    print("     Source B → 'habits'")

    # -- 2d. Find shared columns (including 'source') -------------------------
    shared_cols = sorted(set(df_prod.columns) & set(df_hab.columns))

    # Always ensure student_id and source come first for readability
    ordered_cols = ["student_id", "source"] + [
        c for c in shared_cols if c not in ("student_id", "source")
    ]

    # Dropped columns per dataset
    dropped_prod = [c for c in df_prod.columns if c not in shared_cols]
    dropped_hab  = [c for c in df_hab.columns  if c not in shared_cols]

    print(f"\n[2d] Shared columns ({len(ordered_cols)}): {ordered_cols}")
    print(f"\n     Dropped from Source A ({len(dropped_prod)}): {dropped_prod}")
    print(f"     Dropped from Source B ({len(dropped_hab)}):  {dropped_hab}")
    print("\n     NOTE: Dropped columns can be re-added later if needed.")

    df_prod_clean = df_prod[ordered_cols]
    df_hab_clean  = df_hab[ordered_cols]

    return df_prod_clean, df_hab_clean


# ── Section 3: Merge ──────────────────────────────────────────────────────────

def merge(df_prod_clean, df_hab_clean):
    """Concatenate both harmonised DataFrames vertically."""
    print("\n" + "=" * 60)
    print("SECTION 3 — Merging datasets")
    print("=" * 60)

    merged = pd.concat([df_prod_clean, df_hab_clean], ignore_index=True)

    print(f"\n  Source A rows   : {len(df_prod_clean):,}")
    print(f"  Source B rows   : {len(df_hab_clean):,}")
    print(f"  Merged rows     : {len(merged):,}")
    print(f"  Merged columns  : {list(merged.columns)}")

    # Sanity check: source breakdown
    vc = merged["source"].value_counts()
    print(f"\n  Row counts by source:")
    for src, cnt in vc.items():
        print(f"    {src}: {cnt:,} rows ({cnt/len(merged)*100:.1f}%)")

    return merged


# ── Section 4: Data Quality Checks ───────────────────────────────────────────

def quality_check(merged):
    """
    Run basic data quality checks on the merged dataset:
      - Shape, dtypes, missing value counts.
      - Flag negative values in hours columns.
      - Flag attendance_percentage outside 0–100.
    """
    print("\n" + "=" * 60)
    print("SECTION 4 — Data quality checks on merged dataset")
    print("=" * 60)

    # -- Shape ---------------------------------------------------------------
    print(f"\n  Shape: {merged.shape[0]:,} rows × {merged.shape[1]} columns")

    # -- Dtypes --------------------------------------------------------------
    print("\n  Column dtypes:")
    for col, dtype in merged.dtypes.items():
        print(f"    {col:<30} {dtype}")

    # -- Missing values -------------------------------------------------------
    miss = merged.isnull().sum()
    miss_pct = (miss / len(merged) * 100).round(2)
    print("\n  Missing values per column:")
    any_missing = False
    for col in merged.columns:
        if miss[col] > 0:
            print(f"    ⚠  {col:<28} {miss[col]:>6,} missing ({miss_pct[col]:.1f}%)")
            any_missing = True
    if not any_missing:
        print("    ✓  No missing values detected.")

    # -- Negative values in hours columns ------------------------------------
    print("\n  Negative-value check (hours columns):")
    any_negative = False
    for col in HOURS_COLUMNS:
        if col in merged.columns:
            n_neg = int((merged[col].dropna() < 0).sum())
            if n_neg > 0:
                print(f"    ⚠  {col}: {n_neg} negative value(s) — investigate before analysis.")
                any_negative = True
    if not any_negative:
        print("    ✓  No negative values detected in hours columns.")

    # -- Percentage columns outside 0–100 ------------------------------------
    print("\n  Range check (percentage columns must be 0–100):")
    any_oob = False
    for col in PERCENTAGE_COLUMNS:
        if col in merged.columns:
            n_oob = int(((merged[col].dropna() < 0) | (merged[col].dropna() > 100)).sum())
            if n_oob > 0:
                print(f"    ⚠  {col}: {n_oob} value(s) outside [0, 100].")
                any_oob = True
    if not any_oob:
        print("    ✓  All percentage values within valid range.")

    # -- Academic score range ------------------------------------------------
    if "academic_score" in merged.columns:
        lo = merged["academic_score"].min()
        hi = merged["academic_score"].max()
        print(f"\n  academic_score range: {lo:.2f} – {hi:.2f}")
        n_oob = int(((merged["academic_score"].dropna() < 0) |
                     (merged["academic_score"].dropna() > 100)).sum())
        if n_oob > 0:
            print(f"    ⚠  {n_oob} academic_score value(s) outside [0, 100].")
        else:
            print("    ✓  All academic_score values within [0, 100].")

    # -- Quick descriptive stats on numeric columns --------------------------
    print("\n  Descriptive statistics (numeric columns):")
    print(merged.select_dtypes(include="number").describe().round(2).to_string())


# ── Section 5: Save ───────────────────────────────────────────────────────────

def save(merged):
    """Save the merged dataset to CSV."""
    print("\n" + "=" * 60)
    print("SECTION 5 — Saving merged dataset")
    print("=" * 60)

    merged.to_csv(PATH_OUTPUT, index=False)
    print(f"\n  Saved to : {PATH_OUTPUT}")
    print(f"  Rows     : {len(merged):,}")
    print(f"  Columns  : {list(merged.columns)}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    df_prod, df_hab             = load_datasets()
    df_prod_clean, df_hab_clean = harmonise(df_prod, df_hab)
    merged                      = merge(df_prod_clean, df_hab_clean)
    quality_check(merged)
    save(merged)
    print("\n✓ Done.")
