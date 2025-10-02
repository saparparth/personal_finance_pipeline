# personal_finance_pipeline
💳 Personal Finance ETL & Dashboard Project

This project demonstrates an end-to-end ETL pipeline that:

Fetches data from a Mock API (simulating bank transactions).

Extracts, Transforms, and Loads (ETL) the data into PostgreSQL using Apache Airflow.

Connects PostgreSQL to Power BI for interactive dashboards and reporting.

🚀 Tech Stack

Data Source: Mock API (REST)

ETL Orchestration: Apache Airflow

Database: PostgreSQL (running inside WSL2)

Analytics / Visualization: Power BI

Programming: Python (requests, pandas, pyspark for transformations)

📂 Project Structure
personal_finance_project/
│
├── airflow/
│   ├── dags/
│   │   └── etl_pipeline.py      # Main Airflow DAG
│   ├── scripts/
│   │   ├── extract.py           # Fetch data from Mock API
│   │   ├── transform.py         # Clean and enrich data
│   │   └── load.py              # Load into PostgreSQL
│
├── data/
│   └── raw/                     # Stores raw API responses
     └── staging                 # stores proccesed data 
│
├── powerbi/
│   └── finance_dashboard.pbix   # Power BI dashboard file
│
└── README.md

⚡ ETL Pipeline Flow
🔹 1. Extract  

Script: extract.py

Fetches transaction data from Mock API using requests.

Stores raw JSON responses with timestamped filenames under data/raw/.

🔹 2. Transform

Script: transform.py

Cleans and enriches transaction data:

Converts date & createdAt to proper datetime format.

Derives new fields:

year, month

transaction_type (Income/Expense based on type or amount).

🔹 3. Load

Script: load.py

Loads transformed data into PostgreSQL table:

transactions(accountId, amount, category, date, merchant, transaction_type, year, month, createdAt)

🔹 4. Visualization

Power BI connects directly to PostgreSQL.

Dashboards created for:

Overview (KPIs: Total Income, Total Expense, Net Balance)

Category Spend Breakdown

Merchant Rankings

Cashflow Trends (Monthly Income vs Expenses)

Detailed Drill-Down Transactions

📊 Power BI Report Strategy

Page 1 – Overview

Cards: Total Income, Total Expenses, Net Balance

Line chart: Income vs Expense trend

Pie chart: Category-wise expense breakdown

Page 2 – Trends & Comparison

Column chart: Monthly Income vs Expenses

Stacked chart: Category spend over months

Slicers: Year, Month, Transaction Type, Merchant

![page1](https://github.com/user-attachments/assets/afe28dc0-3c56-4512-ba70-139965a8da87)
![part2](https://github.com/user-attachments/assets/f9fbd105-9701-459f-b38b-97811f7edad5)


🗄️ Database Schema
1️⃣ accounts table
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

2️⃣ merchants table
CREATE TABLE merchants (
    merchant_id SERIAL PRIMARY KEY,
    merchant_name VARCHAR(255) NOT NULL,
    category VARCHAR(100)
);

3️⃣ transactions table
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(account_id),
    merchant_id INT REFERENCES merchants(merchant_id),
    amount NUMERIC(12,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    type VARCHAR(50),  -- deposit / withdrawal / payment / invoice
    transaction_type VARCHAR(50),  -- Income / Expense
    category VARCHAR(100),
    description TEXT,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    year INT,
    month INT
);

4️⃣ (Optional) users table (if multiple account holders)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


Then link accounts.user_id → users.user_id.

📊 Data Model (ERD)
users (1) --- (M) accounts (1) --- (M) transactions (M) --- (1) merchants


One user can have multiple accounts.

One account can have multiple transactions.

Each transaction can be linked to one merchant.

How This Fits in ETL

Extract → Mock API gives JSON of transactions.

Transform → Enrich fields (year, month, transaction_type).

Load → Write into PostgreSQL using above schema.
