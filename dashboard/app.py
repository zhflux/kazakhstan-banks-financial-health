import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Путь к данным
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

# Заголовок
st.title("Financial Health of Kazakhstan Banks")
st.markdown("Анализ банков второго уровня РК на основе данных НБ РК")

# Фильтры
col1, col2 = st.columns(2)
with col1:
    year = st.selectbox("Год", sorted(df["year"].unique()))
with col2:
    metric = st.selectbox("Метрика", ["ROA", "ROE", "LDR", "EAR"])

# Таблица
st.subheader(f"Банки по {metric} в {year}")
df_filtered = df[df["year"] == year].sort_values(metric, ascending=False)
st.dataframe(df_filtered[["bank_name", "assets", "ROA", "ROE", "LDR", "EAR"]].reset_index(drop=True))

# График
st.subheader(f"График {metric} ({year})")
df_chart = df_filtered[df_filtered["LDR"] < 100].copy()
fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(data=df_chart, x=metric, y="bank_name", palette="Blues_r", ax=ax)
ax.set_title(f"{metric} по банкам ({year})")
st.pyplot(fig)

# Health Score
st.subheader("Financial Health Score (среднее 2023-2026)")
df_avg = df_score.groupby("bank_name")["health_score"].mean().sort_values(ascending=False).reset_index()
st.dataframe(df_avg)