import pandas as pd
import pytest
from src.ratios import calculate_ratios


def make_sample_df():
    return pd.DataFrame({
        "number": [1, 2],
        "bank_name": ["Bank A", "Bank B"],
        "assets": [1000, 2000],
        "loans": [500, 1200],
        "liabilities": [800, 1600],
        "deposits": [400, 800],
        "equity": [200, 400],
        "net_income": [50, -20],
        "year": [2023, 2023]
    })


def test_roa():
    df = calculate_ratios(make_sample_df())
    assert df["ROA"].iloc[0] == 50 / 1000
    assert df["ROA"].iloc[1] == -20 / 2000


def test_roe():
    df = calculate_ratios(make_sample_df())
    assert df["ROE"].iloc[0] == 50 / 200
    assert df["ROE"].iloc[1] == -20 / 400


def test_ldr():
    df = calculate_ratios(make_sample_df())
    assert df["LDR"].iloc[0] == 500 / 400
    assert df["LDR"].iloc[1] == 1200 / 800


def test_ear():
    df = calculate_ratios(make_sample_df())
    assert df["EAR"].iloc[0] == 200 / 1000
    assert df["EAR"].iloc[1] == 400 / 2000