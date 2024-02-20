USE stock_db;

DROP TABLE IF EXISTS ticker;
DROP TABLE IF EXISTS global_fs;
DROP TABLE IF EXISTS global_price;

CREATE TABLE IF NOT EXISTS ticker (
    Name VARCHAR(50) NOT NULL,
    Symbol VARCHAR(30),
    Exchange VARCHAR(30),
    Sector VARCHAR(40),
    `Market Cap` VARCHAR(10),
    Country VARCHAR(20),    
    Date DATE,
    PRIMARY KEY(Symbol, Country, Date)
);

CREATE TABLE IF NOT EXISTS global_price (
    Date DATE,
    High DOUBLE,
    Low DOUBLE,
    Open DOUBLE,
    Close DOUBLE,
    Volume DOUBLE,
    `Adj Close` DOUBLE,
    Ticker VARCHAR(20),
    PRIMARY KEY(Date, Ticker)
);

CREATE TABLE IF NOT EXISTS global_fs (
    Ticker VARCHAR(20),        
    Date DATE,
    Account VARCHAR(100),
    Value DOUBLE,
    Freq VARCHAR(1),
    PRIMARY KEY(Ticker, Date, Account, Freq)
);
