import pandas as pd
import yaml
from sklearn.preprocessing import MinMaxScaler


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def calculate_health_score(df: pd.DataFrame, config_path: str = "config.yaml") -> pd.DataFrame:
    config = load_config(config_path)
    weights = config["weights"]
    thresholds = config["thresholds"]

    df = df[df["LDR"] < 100].copy()

    scaler = MinMaxScaler()
    df["ROA_norm"] = scaler.fit_transform(df[["ROA"]])
    df["ROE_norm"] = scaler.fit_transform(df[["ROE"]])
    df["EAR_norm"] = scaler.fit_transform(df[["EAR"]])
    df["LDR_score"] = 1 - abs(df["LDR"] - 1) / df["LDR"].max()

    df["health_score"] = (
        df["ROA_norm"] * weights["roa"] +
        df["ROE_norm"] * weights["roe"] +
        df["LDR_score"] * weights["ldr"] +
        df["EAR_norm"] * weights["ear"]
    )

    df["category"] = pd.cut(
        df["health_score"],
        bins=[0, thresholds["weak"], thresholds["moderate"], 1],
        labels=["Weak", "Moderate", "Strong"]
    )

    return df