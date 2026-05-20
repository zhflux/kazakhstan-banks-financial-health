import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Kazakhstan Banks", layout="wide")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")


@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "banks_with_ratios.csv"))
    df_score = pd.read_csv(os.path.join(DATA_DIR, "banks_health_score.csv"))
    df["bank_name"] = df["bank_name"].str.replace('"', '').str.strip()
    df_score["bank_name"] = df_score["bank_name"].str.replace('"', '').str.strip()
    return df, df_score


df, df_score = load_data()

page = st.sidebar.selectbox("Page", [
    "Executive Overview",
    "Bank Comparison",
    "Risk Analysis",
    "Health Score Explorer",
    "Time Series"
])

# ── PAGE 1 ──────────────────────────────────────────────────────────────────
if page == "Executive Overview":
    st.title("Executive Overview")

    total_assets = df[df["year"] == df["year"].max()]["assets"].sum()
    avg_roa = df["ROA"].mean()
    avg_roe = df[df["ROE"] < 100]["ROE"].mean()
    strongest = df_score.groupby("bank_name")["health_score"].mean().idxmax()
    weakest = df_score.groupby("bank_name")["health_score"].mean().idxmin()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Assets", f"{total_assets/1e9:.0f}B KZT")
    c2.metric("Avg ROA", f"{avg_roa:.2%}")
    c3.metric("Avg ROE", f"{avg_roe:.2%}")
    c4.metric("Strongest Bank", strongest.split('"')[1] if '"' in strongest else strongest)
    c5.metric("Weakest Bank", weakest.split('"')[1] if '"' in weakest else weakest)

    st.subheader("Sector Asset Growth")
    sector = df.groupby("year")["assets"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(sector["year"], sector["assets"] / 1e12, color="#2196F3")
    ax.set_ylabel("Total Assets (trillion KZT)")
    ax.set_xlabel("Year")
    st.pyplot(fig)

    st.subheader("Profitability Trends (avg ROA by year)")
    roa_trend = df.groupby("year")["ROA"].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(roa_trend["year"], roa_trend["ROA"], marker="o", color="#4CAF50")
    ax2.set_ylabel("Avg ROA")
    st.pyplot(fig2)

# ── PAGE 2 ──────────────────────────────────────────────────────────────────
elif page == "Bank Comparison":
    st.title("Bank Comparison")

    banks = sorted(df["bank_name"].unique())
    selected = st.multiselect("Select banks (2-3)", banks, default=banks[:3])

    if len(selected) < 2:
        st.warning("Select at least 2 banks")
    else:
        df_sel = df[df["bank_name"].isin(selected)]
        metrics = ["ROA", "ROE", "LDR", "EAR"]

        for metric in metrics:
            fig, ax = plt.subplots(figsize=(10, 3))
            for bank in selected:
                d = df_sel[df_sel["bank_name"] == bank]
                ax.plot(d["year"], d[metric], marker="o", label=bank)
            ax.set_title(metric)
            ax.legend(fontsize=8)
            st.pyplot(fig)

# ── PAGE 3 ──────────────────────────────────────────────────────────────────
elif page == "Risk Analysis":
    st.title("Risk Analysis")

    year = st.selectbox("Year", sorted(df["year"].unique(), reverse=True))
    df_y = df[df["year"] == year].copy()

    st.subheader(f"Unprofitable Banks ({year})")
    if df_y[df_y["ROA"] < 0].empty:
        st.success("No unprofitable banks in this year")
    st.dataframe(
        df_y[df_y["ROA"] < 0][["bank_name", "ROA", "ROE", "net_income"]]
        .sort_values("ROA").reset_index(drop=True)
    )

    st.subheader("Risky LDR (> 2.0)")
    st.dataframe(
        df_y[(df_y["LDR"] > 2) & (df_y["LDR"] < 10)][["bank_name", "LDR", "loans", "deposits"]]
        .sort_values("LDR", ascending=False).reset_index(drop=True)
    )

    st.subheader("Low Capital (EAR < 0.08)")
    st.dataframe(
        df_y[df_y["EAR"] < 0.08][["bank_name", "EAR", "equity", "assets"]]
        .sort_values("EAR").reset_index(drop=True)
    )

# ── PAGE 4 ──────────────────────────────────────────────────────────────────
elif page == "Health Score Explorer":
    st.title("Health Score Explorer")

    year = st.selectbox("Year", sorted(df_score["year"].unique(), reverse=True))
    category = st.selectbox("Category", ["All", "Strong", "Moderate", "Weak"])

    df_f = df_score[df_score["year"] == year]
    if category != "All":
        df_f = df_f[df_f["category"] == category]

    df_f = df_f.sort_values("health_score", ascending=False).reset_index(drop=True)
    st.dataframe(df_f[["bank_name", "health_score", "category", "ROA", "ROE", "LDR", "EAR"]])

    st.subheader("Score Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = df_f["category"].map({"Strong": "#4CAF50", "Moderate": "#FF9800", "Weak": "#f44336"})
    ax.barh(df_f["bank_name"], df_f["health_score"], color=colors)
    ax.axvline(0.35, color="red", linestyle="--", alpha=0.5)
    ax.axvline(0.60, color="green", linestyle="--", alpha=0.5)
    st.pyplot(fig)

# ── PAGE 5 ──────────────────────────────────────────────────────────────────
elif page == "Time Series":
    st.title("Time Series Analysis")

    banks = sorted(df["bank_name"].unique())
    bank = st.selectbox("Select bank", banks)
    df_b = df[df["bank_name"] == bank].sort_values("year")

    metrics = ["assets", "ROA", "ROE", "LDR"]
    for metric in metrics:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(df_b["year"], df_b[metric], marker="o", color="#2196F3")
        ax.set_title(f"{metric} — {bank}")
        st.pyplot(fig)