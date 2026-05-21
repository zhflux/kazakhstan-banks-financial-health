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
    "Time Series",
    "Advanced Analysis",
    "Data Quality"
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

    st.subheader("Key Interpretations")

    st.info("""
    **Halyk Bank** dominates by assets but trails smaller peers in ROA (3.9% vs Kaspi's 7.1%).
    Scale does not translate into proportional profitability — a pattern common in universal banks
    where loan book growth outpaces margin improvement.
    """)

    st.warning("""
    **Shinhan Bank** grew 478% between 2023–2026. Rapid balance sheet expansion unsupported
    by proportional capital growth may increase exposure to liquidity and credit risk.
    """)

    st.error("""
    **Sector-wide:** No bank reached Strong category (Health Score > 0.60). Average EAR of ~11%
    suggests limited capital buffers. In a credit deterioration scenario, banks with EAR below 8%
    face meaningful solvency pressure.
    """)

    st.success("""
    **Bereke Bank** recovered from ROA -7.6% in 2023 to positive territory by 2024.
    However, its ranking remains volatile under Monte Carlo simulation — reflecting genuine
    analytical uncertainty.
    """)

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

# ── PAGE 6 ──────────────────────────────────────────────────────────────────
elif page == "Advanced Analysis":
    st.title("Advanced Analysis")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Correlation", "Clustering", "Sensitivity", "Outliers", "Forecasting"
    ])

    with tab1:
        df_corr = df[df["LDR"] < 10].copy()
        df_corr = df_corr[df_corr["ROE"] < 10]
        corr = df_corr[["ROA", "ROE", "LDR", "EAR", "assets", "net_income"]].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
        st.pyplot(fig)

    with tab2:
        year = st.selectbox("Year", sorted(df["year"].unique(), reverse=True))
        df_c = df[df["year"] == year][["bank_name", "ROA", "ROE", "LDR", "EAR"]].dropna()
        df_c = df_c[df_c["ROE"] < 100]
        df_c = df_c[df_c["LDR"] < 100]
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
        scaler = StandardScaler()
        X = scaler.fit_transform(df_c[["ROA", "ROE", "LDR", "EAR"]])
        df_c["segment"] = KMeans(n_clusters=3, random_state=42).fit_predict(X)
        df_c["segment"] = df_c["segment"].map({0: "Stable", 1: "Aggressive", 2: "Risky"})
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        colors = {"Stable": "#4CAF50", "Aggressive": "#2196F3", "Risky": "#f44336"}
        for seg, group in df_c.groupby("segment"):
            ax2.scatter(group["ROA"], group["ROE"], label=seg, color=colors[seg], s=100)
            for _, row in group.iterrows():
                ax2.annotate(row["bank_name"][:15], (row["ROA"], row["ROE"]), fontsize=7)
        ax2.set_xlabel("ROA")
        ax2.set_ylabel("ROE")
        ax2.legend()
        st.pyplot(fig2)

    with tab3:
        import numpy as np
        from sklearn.preprocessing import MinMaxScaler

        def score_with_weights(data, w):
            d = data[data["LDR"] < 10].copy()
            sc = MinMaxScaler()
            d["ROA_n"] = sc.fit_transform(d[["ROA"]])
            d["ROE_n"] = sc.fit_transform(d[["ROE"]])
            d["EAR_n"] = sc.fit_transform(d[["EAR"]])
            d["LDR_s"] = 1 - abs(d["LDR"] - 1) / d["LDR"].max()
            d["score"] = d["ROA_n"]*w[0] + d["ROE_n"]*w[1] + d["LDR_s"]*w[2] + d["EAR_n"]*w[3]
            return d.groupby("bank_name")["score"].mean()

        np.random.seed(42)
        results = []
        for _ in range(500):
            w = np.random.dirichlet([1, 1, 1, 1])
            results.append(score_with_weights(df, w))

        mc = pd.DataFrame(results)
        mean_score = mc.mean().sort_values(ascending=False)
        std_score = mc.std().sort_values(ascending=False)

        fig3, axes = plt.subplots(1, 2, figsize=(14, 6))
        mean_score.head(10).plot(kind="barh", ax=axes[0], color="#2196F3")
        axes[0].set_title("Top 10 by avg score")
        axes[0].invert_yaxis()
        std_score.head(10).plot(kind="barh", ax=axes[1], color="#f44336")
        axes[1].set_title("Most volatile rankings")
        axes[1].invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig3)

    with tab4:
        from scipy import stats
        df_out = df[df["ROA"] < 0.5].copy()
        df_out["ROA_z"] = stats.zscore(df_out["ROA"])
        df_out["assets_z"] = stats.zscore(df_out["assets"])
        outliers = df_out[(df_out["ROA_z"].abs() > 2) | (df_out["assets_z"].abs() > 2)]
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.scatter(df_out["ROA"], df_out["assets"]/1e9, alpha=0.5, label="normal")
        ax4.scatter(outliers["ROA"], outliers["assets"]/1e9, color="red", s=100, label="outlier")
        for _, row in outliers.iterrows():
            ax4.annotate(row["bank_name"][:15], (row["ROA"], row["assets"]/1e9), fontsize=7)
        ax4.set_xlabel("ROA")
        ax4.set_ylabel("Assets (B KZT)")
        ax4.legend()
        st.pyplot(fig4)

    with tab5:
        from sklearn.linear_model import LinearRegression
        search_terms = ["Halyk", "Kaspi", "CenterCredit"]
        fig5, axes = plt.subplots(1, 3, figsize=(15, 5))
        for i, term in enumerate(search_terms):
            d = df[df["bank_name"].str.contains(term)].sort_values("year")
            X = d["year"].values.reshape(-1, 1)
            y = d["assets"].values
            model = LinearRegression()
            model.fit(X, y)
            forecast = model.predict(np.array([2027, 2028]).reshape(-1, 1))
            axes[i].plot(d["year"], d["assets"]/1e9, marker="o", label="actual")
            axes[i].plot([2027, 2028], forecast/1e9, marker="o", linestyle="--", color="red", label="forecast")
            axes[i].set_title(term)
            axes[i].set_ylabel("Assets (B KZT)")
            axes[i].legend(fontsize=8)
        plt.suptitle("Asset Growth Forecast")
        plt.tight_layout()
        st.pyplot(fig5)

elif page == "Data Quality":
    st.title("Data Quality Report")

    from scipy import stats

    col1, col2, col3 = st.columns(3)
    col1.metric("Total rows", len(df))
    col2.metric("Banks", df["bank_name"].nunique())
    col3.metric("Years covered", df["year"].nunique())

    st.subheader("Missing Values")
    missing = pd.DataFrame({
        "column": df.columns,
        "missing": df.isnull().sum().values,
        "pct": (df.isnull().sum() / len(df) * 100).round(2).values
    })
    missing = missing[missing["missing"] > 0]
    if missing.empty:
        st.success("No missing values found")
    else:
        st.dataframe(missing)

    st.subheader("Financial Consistency (assets ≈ liabilities + equity)")
    df_check = df.copy()
    df_check["reconstructed"] = df_check["liabilities"] + df_check["equity"]
    df_check["diff_pct"] = (abs(df_check["assets"] - df_check["reconstructed"]) / df_check["assets"] * 100).round(2)
    violations = df_check[df_check["diff_pct"] > 15][["bank_name", "year", "assets", "reconstructed", "diff_pct"]]
    st.warning(f"{len(violations)} rows with inconsistency > 15%")
    st.dataframe(violations.reset_index(drop=True))

    st.subheader("Ratio Sanity Check")
    checks = {
        "ROA < 1": int((df["ROA"] < 1).sum()),
        "EAR between 0 and 1": int(((df["EAR"] >= 0) & (df["EAR"] <= 1)).sum()),
        "Assets > 0": int((df["assets"] > 0).sum()),
    }
    for check, count in checks.items():
        if count == len(df):
            st.success(f"{check}: ✅ all {count} rows pass")
        else:
            st.error(f"{check}: ❌ only {count}/{len(df)} rows pass")
