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