import pandas as pd


def calculate_roa(df: pd.DataFrame) -> pd.Series:
    return df["net_income"] / df["assets"]


def calculate_roe(df: pd.DataFrame) -> pd.Series:
    return df["net_income"] / df["equity"]


def calculate_ldr(df: pd.DataFrame) -> pd.Series:
    return df["loans"] / df["deposits"]


def calculate_ear(df: pd.DataFrame) -> pd.Series:
    return df["equity"] / df["assets"]


def calculate_all_ratios(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ROA"] = calculate_roa(df)
    df["ROE"] = calculate_roe(df)
    df["LDR"] = calculate_ldr(df)
    df["EAR"] = calculate_ear(df)
    return df