# Data Description

## Source
National Bank of Kazakhstan (NBK)
https://nationalbank.kz/en/news/banks-performance

Section: Statistics → Performance of financial sector → Banking sector → Financial performance
Table: "Information about owned capital, liabilities and assets"

## Raw Files
| File | Period |
|------|--------|
| nbk_2023_capital_assets.xls | January 2023 |
| nbk_2024_capital_assets.xls | January 2024 |
| nbk_2025_capital_assets.xls | January 2025 |
| nbk_2026_capital_assets.xls | January 2026 |

## Processed Files

### banks_financial_health_clean.csv
Raw data cleaned and combined across all years.

| Column | Description | Unit |
|--------|-------------|------|
| number | Bank rank by assets | — |
| bank_name | Full legal name of the bank | — |
| assets | Total assets | KZT |
| loans | Total loan portfolio | KZT |
| liabilities | Total liabilities | KZT |
| deposits | Total deposits | KZT |
| equity | Total equity / capital | KZT |
| net_income | Net profit or loss | KZT |
| year | Reporting year | — |

### banks_with_ratios.csv
Same as above with calculated financial ratios.

| Column | Description | Formula |
|--------|-------------|---------|
| ROA | Return on Assets | net_income / assets |
| ROE | Return on Equity | net_income / equity |
| LDR | Loan-to-Deposit Ratio | loans / deposits |
| EAR | Equity-to-Assets Ratio | equity / assets |

### banks_health_score.csv
Financial Health Score and category for each bank per year.

| Column | Description |
|--------|-------------|
| health_score | Weighted score from 0 to 1 |
| category | Weak / Moderate / Strong |

## Notes
- All monetary values are in Kazakhstani Tenge (KZT)
- Data represents unconsolidated statements of second-tier banks
- Citibank Kazakhstan excluded from some analyses due to anomalous LDR