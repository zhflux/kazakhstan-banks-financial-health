CREATE TABLE IF NOT EXISTS banks (
    id SERIAL PRIMARY KEY,
    number NUMERIC,
    bank_name TEXT,
    assets NUMERIC,
    loans NUMERIC,
    liabilities NUMERIC,
    deposits NUMERIC,
    equity NUMERIC,
    net_income NUMERIC,
    year INT,
    ROA NUMERIC,
    ROE NUMERIC,
    LDR NUMERIC,
    EAR NUMERIC
);