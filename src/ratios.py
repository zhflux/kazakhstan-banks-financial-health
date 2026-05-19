import pandas as pd

def calculate_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate financial ratios for each bank."""
    df = df.copy()
    df["ROA"] = df["net_income"] / df["assets"]
    df["ROE"] = df["net_income"] / df["equity"]
    df["LDR"] = df["loans"] / df["deposits"]
    df["EAR"] = df["equity"] / df["assets"]
    return df