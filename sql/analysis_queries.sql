-- 1. Топ-5 банков по активам в 2023
SELECT bank_name, assets
FROM banks
WHERE year = 2023
ORDER BY assets DESC
LIMIT 5;

-- 2. Топ банков по ROA в 2026
SELECT bank_name, ROA, ROE
FROM banks
WHERE year = 2026
ORDER BY ROA DESC
LIMIT 5;

-- 3. Банки с наибольшим ростом активов 2023 vs 2026
SELECT 
    b1.bank_name,
    b1.assets AS assets_2023,
    b2.assets AS assets_2026,
    ROUND(((b2.assets - b1.assets) / b1.assets * 100)::numeric, 2) AS growth_pct
FROM banks b1
JOIN banks b2 ON b1.bank_name = b2.bank_name
WHERE b1.year = 2023 AND b2.year = 2026
ORDER BY growth_pct DESC
LIMIT 5;

-- 4. Убыточные банки
SELECT bank_name, year, net_income, ROA
FROM banks
WHERE net_income < 0
ORDER BY net_income ASC;

-- year over year asset growth
SELECT
    bank_name,
    year,
    assets,
    LAG(assets) OVER (PARTITION BY bank_name ORDER BY year) AS prev_assets,
    ROUND((
        (assets - LAG(assets) OVER (PARTITION BY bank_name ORDER BY year))
        / LAG(assets) OVER (PARTITION BY bank_name ORDER BY year) * 100
    )::numeric, 2) AS yoy_growth_pct
FROM banks
ORDER BY bank_name, year;


-- rolling 2-year avg ROA
SELECT
    bank_name,
    year,
    ROA,
    ROUND(AVG(ROA) OVER (
        PARTITION BY bank_name
        ORDER BY year
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
    )::numeric, 4) AS rolling_avg_roa
FROM banks
ORDER BY bank_name, year;


-- rank banks by ROA within each year
SELECT
    bank_name,
    year,
    ROA,
    RANK() OVER (PARTITION BY year ORDER BY ROA DESC) AS roa_rank
FROM banks
ORDER BY year, roa_rank;


-- quartile buckets by assets
SELECT
    bank_name,
    year,
    assets,
    NTILE(4) OVER (PARTITION BY year ORDER BY assets DESC) AS asset_quartile
FROM banks
ORDER BY year, asset_quartile;


-- CTE: banks that were top 5 by ROA every year
WITH yearly_ranks AS (
    SELECT
        bank_name,
        year,
        ROA,
        RANK() OVER (PARTITION BY year ORDER BY ROA DESC) AS roa_rank
    FROM banks
),
consistently_top AS (
    SELECT
        bank_name,
        COUNT(*) AS years_in_top5
    FROM yearly_ranks
    WHERE roa_rank <= 5
    GROUP BY bank_name
)
SELECT *
FROM consistently_top
WHERE years_in_top5 = (SELECT COUNT(DISTINCT year) FROM banks)
ORDER BY bank_name;