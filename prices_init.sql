CREATE TABLE defaultdb.stu_schema.cmc_prices (
	id UUID NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol STRING NOT NULL,
    name STRING NOT NULL,
    price FLOAT NOT NULL,
    volume_24h FLOAT,
    volume_change_24h FLOAT,
    percent_change_1h FLOAT,
    percent_change_24h FLOAT,
    percent_change_7d FLOAT,
    percent_change_30d FLOAT,
    market_cap FLOAT,
    market_cap_dominance FLOAT,
    fully_diluted_market_cap FLOAT,
    cmc_rank INT,
    price_last_updated TIMESTAMP,
	is_active BOOL,
	is_fiat BOOL,
    circulating_supply FLOAT,
    total_supply FLOAT,
    max_supply FLOAT,
    num_market_pairs INT
);