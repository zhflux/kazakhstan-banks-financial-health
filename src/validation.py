import pandas as pd
import numpy as np


def validate_assets(df):
    assert (df["assets"] > 0).all(), "Negative assets found"


def validate_financial_consistency(df, tolerance=0.15):
    df = df.copy()
    df["reconstructed"] = df["liabilities"] + df["equity"]
    df["diff_pct"] = abs(df["assets"] - df["reconstructed"]) / df["assets"]
    violations = df[df["diff_pct"] > tolerance]
    if len(violations) > 0:
        print(f"Warning: {len(violations)} rows where assets != liabilities + equity")
        print(violations[["bank_name", "year", "assets", "reconstructed", "diff_pct"]])
    return violations


def validate_ratios(df):
    issues = []
    if not (df["ROA"] < 1).all():
        issues.append("ROA > 1 found")
    if not (df["EAR"] >= 0).all():
        issues.append("Negative EAR found")
    if not (df["EAR"] <= 1).all():
        issues.append("EAR > 1 found")
    if issues:
        print("Ratio issues:", issues)
    else:
        print("All ratio checks passed")
    return issues


def missing_data_report(df, output_path="data/processed/missing_report.csv"):
    report = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isnull().sum().values,
        "missing_pct": (df.isnull().sum() / len(df) * 100).round(2).values,
        "dtype": df.dtypes.astype(str).values
    })
    report.to_csv(output_path, index=False)
    missing = report[report["missing_count"] > 0]
    print(f"Missing data report saved: {len(missing)} columns with missing values")
    return report


def run_all_validations(df):
    print("Running validations...")
    validate_assets(df)
    validate_financial_consistency(df)
    validate_ratios(df)
    missing_data_report(df)
    print("Done")