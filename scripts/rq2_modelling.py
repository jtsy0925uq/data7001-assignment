"""
rq2_modelling.py
================
DATA7001 – Social Media & Cognitive Functioning Project
--------------------------------------------------------
Answers RQ2: "To what extent do student lifestyle habits predict
academic performance?"

Dataset : dataset/filtered/student_habits_exam_performance_filtered.csv
Target  : exam_score
Predictors:
  - social_media_hours   (usage variable of interest)
  - netflix_hours        (usage variable of interest)
  - study_hours_per_day  (control — general lifestyle)
  - sleep_hours          (control — general lifestyle)
  - attendance_percentage(control — general lifestyle)

Models:
  1. Multiple Linear Regression  (sklearn + statsmodels OLS for p-values)
  2. Random Forest Regressor

Outputs saved to ./outputs/:
  rq2_linear_residuals.png
  rq2_rf_importances.png
  rq2_actual_vs_predicted.png
  rq2_model_comparison.csv

Usage
-----
  python scripts/rq2_modelling.py
"""

import sys
import os

import numpy  as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection  import train_test_split
from sklearn.preprocessing    import StandardScaler
from sklearn.linear_model     import LinearRegression
from sklearn.ensemble         import RandomForestRegressor
from sklearn.metrics          import r2_score, mean_absolute_error, mean_squared_error

import statsmodels.api as sm

sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ─────────────────────────────────────────────────────────────────────
DATA_PATH  = os.path.join("dataset", "filtered",
                           "student_habits_exam_performance_filtered.csv")
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Column definitions ────────────────────────────────────────────────────────
TARGET     = "exam_score"
PREDICTORS = [
    "study_hours_per_day",    # control
    "sleep_hours",            # control
    "attendance_percentage",  # control
    "social_media_hours",     # usage variable of interest
    "netflix_hours",          # usage variable of interest
]


# ════════════════════════════════════════════════════════════════════════════════
# Section 1 — Load & Prepare Data
# ════════════════════════════════════════════════════════════════════════════════

def load_and_prepare(path):
    """
    Load the CSV, select relevant columns, report missing values,
    drop NaN rows, and return the feature matrix X and target vector y.
    """
    print("=" * 65)
    print("SECTION 1 — Load and prepare data")
    print("=" * 65)

    df = pd.read_csv(path)
    print(f"\nLoaded: {path}")
    print(f"  Full dataset shape : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\nFirst 3 rows (selected columns):")
    print(df[PREDICTORS + [TARGET]].head(3).to_string(index=False))

    # Select only the columns we need
    df_model = df[PREDICTORS + [TARGET]].copy()

    # Missing value check
    missing = df_model.isnull().sum()
    if missing.sum() == 0:
        print(f"\n  Missing values : none detected across all model columns")
    else:
        print(f"\n  Missing values detected — dropping affected rows:")
        for col, n in missing[missing > 0].items():
            print(f"    {col}: {n} missing")
        before = len(df_model)
        df_model = df_model.dropna()
        print(f"  Rows before drop: {before:,} → after drop: {len(df_model):,}")

    X = df_model[PREDICTORS]
    y = df_model[TARGET]
    print(f"\n  Features : {PREDICTORS}")
    print(f"  Target   : {TARGET}  (mean={y.mean():.2f}, std={y.std():.2f})")

    return X, y


# ════════════════════════════════════════════════════════════════════════════════
# Section 2 — Train/Test Split & Scaling
# ════════════════════════════════════════════════════════════════════════════════

def split_and_scale(X, y):
    """
    80/20 train/test split (random_state=42), then StandardScaler
    fit on train and applied to both train and test.
    Returns scaled arrays and the fitted scaler.
    """
    print("\n" + "=" * 65)
    print("SECTION 2 — Train/test split and scaling")
    print("=" * 65)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"\n  Train size : {len(X_train):,} rows (80%)")
    print(f"  Test size  : {len(X_test):,}  rows (20%)")

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)
    print(f"\n  StandardScaler fitted on training set and applied to both splits.")
    print(f"  Feature means (train): {np.round(scaler.mean_, 3)}")
    print(f"  Feature stds  (train): {np.round(scaler.scale_, 3)}")

    return X_train_sc, X_test_sc, y_train, y_test, scaler


# ════════════════════════════════════════════════════════════════════════════════
# Section 3 — Model 1: Multiple Linear Regression
# ════════════════════════════════════════════════════════════════════════════════

def run_linear_regression(X_train_sc, X_test_sc, y_train, y_test, X_full, y_full):
    """
    Fit sklearn LinearRegression for prediction metrics, then statsmodels OLS
    on the full (unscaled) dataset for interpretable p-values.
    Produces a residual plot.
    Returns y_pred_test for the comparison plot.
    """
    print("\n" + "=" * 65)
    print("SECTION 3 — Model 1: Multiple Linear Regression")
    print("=" * 65)

    # -- sklearn fit & evaluation -------------------------------------------
    lr = LinearRegression()
    lr.fit(X_train_sc, y_train)
    y_pred = lr.predict(X_test_sc)

    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\n  [sklearn] Coefficients (standardised predictors):")
    print(f"  {'Feature':<28} {'Coefficient':>12}")
    print("  " + "-" * 42)
    for feat, coef in zip(PREDICTORS, lr.coef_):
        print(f"  {feat:<28} {coef:>12.4f}")
    print(f"  {'Intercept':<28} {lr.intercept_:>12.4f}")

    print(f"\n  [sklearn] Test-set performance:")
    print(f"    R²   : {r2:.4f}")
    print(f"    MAE  : {mae:.4f}")
    print(f"    RMSE : {rmse:.4f}")

    # -- statsmodels OLS on full dataset (unscaled) for p-values -------------
    print("\n  [statsmodels] OLS on full dataset (unscaled, for p-values):")
    X_sm = sm.add_constant(X_full)   # adds intercept column
    ols  = sm.OLS(y_full, X_sm).fit()
    print(ols.summary())

    # -- Residual plot --------------------------------------------------------
    residuals = y_test.values - y_pred
    fig, ax   = plt.subplots(figsize=(7, 5))
    ax.scatter(y_pred, residuals, alpha=0.4, color="#6366f1", edgecolors="none", s=25)
    ax.axhline(0, color="#ef4444", linewidth=1.5, linestyle="--")
    ax.set_title("Linear Regression — Residuals vs Predicted", fontweight="bold")
    ax.set_xlabel("Predicted exam_score")
    ax.set_ylabel("Residual (actual − predicted)")
    ax.annotate(f"R² = {r2:.3f}  |  RMSE = {rmse:.3f}",
                xy=(0.02, 0.95), xycoords="axes fraction", fontsize=9,
                color="#374151")
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "rq2_linear_residuals.png")
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"\n  Residual plot saved → {out}")

    return y_pred, {"model": "Linear Regression", "R2": r2, "MAE": mae, "RMSE": rmse}


# ════════════════════════════════════════════════════════════════════════════════
# Section 4 — Model 2: Random Forest Regressor
# ════════════════════════════════════════════════════════════════════════════════

def run_random_forest(X_train_sc, X_test_sc, y_train, y_test):
    """
    Fit a Random Forest Regressor, evaluate on the test set, print ranked
    feature importances, and produce a horizontal bar chart.
    Returns y_pred_test for the comparison plot.
    """
    print("\n" + "=" * 65)
    print("SECTION 4 — Model 2: Random Forest Regressor")
    print("=" * 65)

    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train_sc, y_train)
    y_pred = rf.predict(X_test_sc)

    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"\n  Test-set performance:")
    print(f"    R²   : {r2:.4f}")
    print(f"    MAE  : {mae:.4f}")
    print(f"    RMSE : {rmse:.4f}")

    # -- Feature importances --------------------------------------------------
    importances = pd.Series(rf.feature_importances_, index=PREDICTORS)
    importances = importances.sort_values(ascending=False)

    print(f"\n  Feature importances (ranked):")
    print(f"  {'Feature':<28} {'Importance':>10}")
    print("  " + "-" * 40)
    for feat, imp in importances.items():
        print(f"  {feat:<28} {imp:>10.4f}")

    # -- Importance bar chart -------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 4))
    colors  = ["#6366f1" if i < 2 else "#94a3b8"
               for i in range(len(importances))]
    ax.barh(importances.index[::-1], importances.values[::-1],
            color=colors[::-1], edgecolor="#1e1b4b", linewidth=0.6)
    ax.set_title("Random Forest — Feature Importances", fontweight="bold")
    ax.set_xlabel("Importance score")
    ax.set_ylabel("")
    ax.annotate(f"R² = {r2:.3f}  |  RMSE = {rmse:.3f}",
                xy=(0.98, 0.03), xycoords="axes fraction", fontsize=9,
                ha="right", color="#374151")
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "rq2_rf_importances.png")
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"\n  Feature importance chart saved → {out}")

    return y_pred, {"model": "Random Forest", "R2": r2, "MAE": mae, "RMSE": rmse}


# ════════════════════════════════════════════════════════════════════════════════
# Section 5 — Model Comparison
# ════════════════════════════════════════════════════════════════════════════════

def compare_models(metrics_lr, metrics_rf):
    """
    Print a side-by-side comparison table and save it as a CSV.
    Returns the comparison DataFrame.
    """
    print("\n" + "=" * 65)
    print("SECTION 5 — Model comparison")
    print("=" * 65)

    comparison = pd.DataFrame([metrics_lr, metrics_rf]).set_index("model")
    comparison = comparison.round(4)

    print("\n  Side-by-side metrics (test set):")
    print(comparison.to_string())

    # Indicate which model wins on each metric
    print(f"\n  Best R²   : {comparison['R2'].idxmax()}  ({comparison['R2'].max():.4f})")
    print(f"  Best MAE  : {comparison['MAE'].idxmin()}  ({comparison['MAE'].min():.4f})")
    print(f"  Best RMSE : {comparison['RMSE'].idxmin()}  ({comparison['RMSE'].min():.4f})")

    out = os.path.join(OUTPUT_DIR, "rq2_model_comparison.csv")
    comparison.to_csv(out)
    print(f"\n  Comparison saved → {out}")

    return comparison


# ════════════════════════════════════════════════════════════════════════════════
# Section 6 — Actual vs Predicted Plots
# ════════════════════════════════════════════════════════════════════════════════

def plot_actual_vs_predicted(y_test, y_pred_lr, y_pred_rf, metrics_lr, metrics_rf):
    """
    Two-subplot figure: actual vs predicted for each model,
    with a diagonal reference line.
    """
    print("\n" + "=" * 65)
    print("SECTION 6 — Actual vs Predicted plots")
    print("=" * 65)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    diag      = [y_test.min(), y_test.max()]

    for ax, y_pred, metrics, colour in zip(
        axes,
        [y_pred_lr, y_pred_rf],
        [metrics_lr, metrics_rf],
        ["#6366f1", "#10b981"]
    ):
        ax.scatter(y_test, y_pred, alpha=0.35, s=18,
                   color=colour, edgecolors="none")
        ax.plot(diag, diag, color="#ef4444", linewidth=1.5,
                linestyle="--", label="Perfect prediction")
        ax.set_title(
            f"{metrics['model']}\nR² = {metrics['R2']:.3f}  |  "
            f"RMSE = {metrics['RMSE']:.3f}",
            fontweight="bold", fontsize=10
        )
        ax.set_xlabel("Actual exam_score")
        ax.set_ylabel("Predicted exam_score")
        ax.legend(fontsize=8)

    fig.suptitle("Actual vs Predicted — exam_score (test set)",
                 fontweight="bold", fontsize=12, y=1.02)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "rq2_actual_vs_predicted.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"\n  Actual vs Predicted plot saved → {out}")


# ════════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # 1. Load and prepare
    X, y = load_and_prepare(DATA_PATH)

    # 2. Split and scale
    X_train_sc, X_test_sc, y_train, y_test, scaler = split_and_scale(X, y)

    # 3. Linear Regression  (pass unscaled X for statsmodels OLS p-values)
    y_pred_lr, metrics_lr = run_linear_regression(
        X_train_sc, X_test_sc, y_train, y_test,
        X_full=X, y_full=y
    )

    # 4. Random Forest
    y_pred_rf, metrics_rf = run_random_forest(
        X_train_sc, X_test_sc, y_train, y_test
    )

    # 5. Compare
    compare_models(metrics_lr, metrics_rf)

    # 6. Actual vs Predicted
    plot_actual_vs_predicted(y_test, y_pred_lr, y_pred_rf, metrics_lr, metrics_rf)

    print("\n" + "=" * 65)
    print("All outputs saved to ./outputs/")
    print("=" * 65)
