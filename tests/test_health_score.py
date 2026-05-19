import pandas as pd
from src.ratios import calculate_ratios


def test_roa_positive():
    df = pd.DataFrame({
        "assets": [1000], "loans": [500], "liabilities": [800],
        "deposits": [400], "equity": [200], "net_income": [100],
        "number": [1], "bank_name": ["Test Bank"], "year": [2023]
    })
    result = calculate_ratios(df)
    assert result["ROA"].iloc[0] > 0


def test_roa_negative():
    df = pd.DataFrame({
        "assets": [1000], "loans": [500], "liabilities": [800],
        "deposits": [400], "equity": [200], "net_income": [-50],
        "number": [1], "bank_name": ["Test Bank"], "year": [2023]
    })
    result = calculate_ratios(df)
    assert result["ROA"].iloc[0] < 0


def test_ear_between_zero_and_one():
    df = pd.DataFrame({
        "assets": [1000], "loans": [500], "liabilities": [800],
        "deposits": [400], "equity": [200], "net_income": [50],
        "number": [1], "bank_name": ["Test Bank"], "year": [2023]
    })
    result = calculate_ratios(df)
    assert 0 < result["EAR"].iloc[0] < 1