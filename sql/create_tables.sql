CREATE TABLE IF NOT EXISTS banks (
    id SERIAL PRIMARY KEY,
    number FLOAT,
    bank_name TEXT,
    assets FLOAT,
    loans FLOAT,
    liabilities FLOAT,
    deposits FLOAT,
    equity FLOAT,
    net_income FLOAT,
    year INT,
    ROA FLOAT,
    ROE FLOAT,
    LDR FLOAT,
    EAR FLOAT
);