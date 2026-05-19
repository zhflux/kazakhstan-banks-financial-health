# Financial Health Analysis of Kazakhstan Banks

## Project Overview
This project analyzes the financial health of Kazakhstan's second-tier banks using publicly available financial data from the National Bank of Kazakhstan (NBK).

## Current Status
- [x] Project structure created
- [x] Data source identified (NBK)
- [x] Raw NBK Excel files added (2023-2026)
- [x] Data loading and cleaning notebook
- [x] Financial ratios calculated (ROA, ROE, LDR, EAR)
- [x] Financial Health Score completed
- [x] SQL analysis queries added
- [x] Streamlit dashboard completed
- [x] Final report completed

## Tools Used
Python, Pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebook, PostgreSQL, Streamlit

## Key Findings
- Shinhan Bank: fastest growth +478% (2023-2026)
- Kaspi Bank: most profitable (ROA 7.1%)
- Bereke Bank & VTB: losses in 2023, recovered by 2024

## Data Source
National Bank of Kazakhstan: https://nationalbank.kz/en/news/banks-performance

## Dashboard Preview

![Dashboard](reports/screenshot_1.png)
![ROA Chart](reports/screenshot_2.png)
![Health Score](reports/screenshot_3.png)

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/zhflux/kazakhstan-banks-financial-health.git
cd kazakhstan-banks-financial-health
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NBK Excel files from:

https://nationalbank.kz/en/news/banks-performance

Put them in `data/raw/` named as `nbk_2023_capital_assets.xls` etc.

4. Run notebooks in order:
```bash
notebooks/01_data_loading_and_cleaning.ipynb
notebooks/02_financial_ratios.ipynb
notebooks/03_health_score.ipynb
```

5. Run the dashboard:
```bash
cd dashboard
streamlit run app.py
```

6. (Optional) Load data into PostgreSQL:
```bash
psql -d kazakhstan_banks -f sql/create_tables.sql
psql -d kazakhstan_banks -c "\copy banks(...) FROM 'data/processed/banks_with_ratios.csv' CSV HEADER"
```