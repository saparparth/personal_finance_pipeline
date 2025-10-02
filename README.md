# 💳 Personal Finance ETL & Dashboard Project  

An **end-to-end Data Engineering & Analytics pipeline** for tracking and analyzing personal finance.  

This project demonstrates how to:  

- 🔗 **Fetch** data from a Mock API (simulating bank transactions)  
- ⚙️ **ETL** the data into **PostgreSQL** using **Apache Airflow**  
- 📊 **Visualize & Analyze** the data with **Power BI**  

---

## 🚀 Tech Stack  

- **Data Source** → Mock API (REST)  
- **Orchestration** → Apache Airflow  
- **Database** → PostgreSQL (running inside WSL2)  
- **Visualization** → Power BI  
- **Programming** → Python (`requests`, `pandas`, `pyspark`)  

---

## 📂 Project Structure  

```bash
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
│   ├── raw/                     # Stores raw API responses
│   └── staging/                 # Stores processed data
│
├── powerbi/
│   └── finance_dashboard.pbix   # Power BI dashboard file
│
└── README.md


⚡ ETL Pipeline Flow
🔹 1. Extract (extract.py)

Fetch transaction data from Mock API using requests

Store raw JSON responses under data/raw/ with timestamped filenames

🔹 2. Transform (transform.py)

Clean & enrich raw data:

Convert date & createdAt → proper datetime

Derive new fields:

year, month

transaction_type → Income / Expense

🔹 3. Load (load.py)

Insert transformed data into PostgreSQL:

transactions(
  accountId, amount, category, date, merchant,
  transaction_type, year, month, createdAt
)

🔹 4. Visualization (Power BI)

Connect Power BI directly to PostgreSQL

Create interactive dashboards

📊 Power BI Dashboard Strategy
📌 Page 1 – Overview

Cards: Total Income, Total Expenses, Net Balance

Line Chart: Income vs Expense trend

Pie Chart: Category-wise expense breakdown

📌 Page 2 – Trends & Comparison

Column Chart: Monthly Income vs Expenses

Stacked Chart: Category spend over months

Slicers: Year, Month, Transaction Type, Merchant

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
    type VARCHAR(50),             -- deposit / withdrawal / payment / invoice
    transaction_type VARCHAR(50), -- Income / Expense
    category VARCHAR(100),
    description TEXT,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    year INT,
    month INT
);

4️⃣ (Optional) users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


🔗 Link: accounts.user_id → users.user_id

📊 Data Model (ERD)
erDiagram
    USERS ||--o{ ACCOUNTS : owns
    ACCOUNTS ||--o{ TRANSACTIONS : has
    TRANSACTIONS }o--|| MERCHANTS : "done at"


One user → many accounts

One account → many transactions

One transaction → linked to one merchant

🛠️ How This Fits in ETL

Extract → Get JSON from Mock API

Transform → Add derived fields (year, month, transaction_type)

Load → Insert into PostgreSQL schema

Visualize → Power BI dashboards for financial insights
