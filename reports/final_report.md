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

## Business Interpretations

**Halyk Bank — Dominant but Efficiency-Challenged**
Despite commanding the largest balance sheet in Kazakhstan, Halyk Bank's ROA of 3.9%
trails smaller peers like Kaspi (7.1%) and Citibank (7.5%). This suggests that scale
does not translate into proportional profitability — a pattern common in state-adjacent
universal banks where loan book growth outpaces margin improvement.

**Kaspi Bank — Profitability Leader with Concentration Risk**
Kaspi's ROE of 66% reflects exceptional capital efficiency driven by its fintech-embedded
lending model. However, its LDR of 0.91 and relatively thin equity base raise questions
about resilience in a credit stress scenario. High ROE without proportional capital
growth may indicate increasing leverage dependency.

**Shinhan, ICBC — High Growth, Unverified Sustainability**
Shinhan Bank's 478% asset growth between 2023 and 2026 is extraordinary. Rapid balance
sheet expansion unsupported by proportional capital growth may increase exposure to
liquidity and credit risk. Without visibility into loan quality, this growth trajectory
warrants close monitoring.

**Bereke Bank — Recovery Story with Residual Uncertainty**
Bereke Bank posted a ROA of -7.6% in 2023 following restructuring. Its recovery to
positive territory by 2024 is encouraging, but its Financial Health Score remains
volatile under Monte Carlo simulation — meaning its ranking is highly sensitive to
how profitability versus capital adequacy is weighted. This reflects genuine analytical
uncertainty, not a data artifact.

**Sector-Wide Capital Adequacy Concern**
No bank in the dataset achieved a Health Score above 0.60 (Strong category). The
sector-wide average EAR of approximately 11% suggests limited capital buffers relative
to asset bases. In a rising rate or credit deterioration environment, banks with EAR
below 8% face meaningful solvency pressure.

## Risk Implications

- **Liquidity risk:** Banks with LDR above 2.0 fund loans through interbank markets
  rather than stable customer deposits. This creates refinancing vulnerability in
  tightening credit conditions.

- **Capital adequacy risk:** Several institutions maintain EAR below 8%, providing
  minimal loss-absorption capacity. Regulatory minimum in Kazakhstan is 7.5% (Tier 1),
  leaving little buffer.

- **Concentration risk:** The top 3 banks (Halyk, Kaspi, CenterCredit) hold over 60%
  of sector assets. Distress in any of these would have systemic implications.

- **Model risk:** Financial Health Score rankings shift materially under Monte Carlo
  weight simulation. Any composite scoring model should be treated as directional,
  not definitive.

### Conclusions
The Kazakhstan banking sector shows steady asset growth across all major banks.
Kaspi Bank remains the profitability leader. Small foreign-owned banks show
high efficiency ratios due to their niche business models. The sector has
largely recovered from the 2023 losses seen in Bereke and VTB.

### Limitations
- Data covers only 4 periods (2023-2026)
- Financial Health Score weights are subjective
- This is not an official rating or investment recommendation