# Financial Health Analysis of Kazakhstan Banks

## Financial Health Score Methodology

The score is calculated as a weighted average of 4 normalized metrics:

| Metric | Weight | Description |
|--------|--------|-------------|
| ROA | 35% | Return on Assets — profitability relative to total assets |
| ROE | 35% | Return on Equity — profitability relative to equity |
| LDR | 15% | Loan-to-Deposit Ratio — closer to 1.0 is optimal |
| EAR | 15% | Equity-to-Assets Ratio — capital strength |

### Normalization
- ROA, ROE, EAR: Min-Max scaling to [0, 1]
- LDR: `1 - abs(LDR - 1) / max(LDR)` — penalizes deviation from 1.0

### Final Formula
Health Score = ROA_norm × 0.35 + ROE_norm × 0.35 + LDR_score × 0.15 + EAR_norm × 0.15

### Categories
| Score | Category |
|-------|----------|
| 0.0 — 0.35 | 🔴 Weak |
| 0.35 — 0.60 | 🟡 Moderate |
| 0.60 — 1.00 | 🟢 Strong |

## Final Report

### Key Findings

**1. Fastest growing banks (2023-2026)**
- Shinhan Bank Kazakhstan: +478% asset growth
- Industrial and Commercial Bank of China: +112%
- Bank CenterCredit: +97%

**2. Most profitable banks (ROA)**
- Kaspi Bank: ROA 7.1% — consistently the most profitable large bank
- Halyk Bank: ROA 3.9% — largest by assets, stable profitability

**3. Problematic banks in 2023**
- Bereke Bank: ROA -7.6% (loss)
- Bank VTB Kazakhstan: ROA -17.4% (loss)
- Both recovered by 2024-2025

**4. Financial Health Score ranking**
- Bereke Bank JSC (SB of Lesha Bank): 0.50 — Moderate
- Islamic bank Zaman-Bank: 0.48 — Moderate
- ICBC in Almaty: 0.46 — Moderate
- No bank reached "Strong" category (>0.6)

### Conclusions
The Kazakhstan banking sector shows steady asset growth across all major banks.
Kaspi Bank remains the profitability leader. Small foreign-owned banks show
high efficiency ratios due to their niche business models. The sector has
largely recovered from the 2023 losses seen in Bereke and VTB.

### Limitations
- Data covers only 4 periods (2023-2026)
- Financial Health Score weights are subjective
- This is not an official rating or investment recommendation