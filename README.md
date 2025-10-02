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


# 💰 Personal Finance ETL & Visualization

This project demonstrates a full ETL pipeline for personal finance data.  
Data is extracted from a **Mock API**, transformed with additional fields, loaded into **PostgreSQL**, and visualized with **Power BI** dashboards.

---

## 🔹 4. Visualization (Power BI)

### 📊 Power BI Dashboard Strategy

#### 📌 Page 1 – Overview
- **Cards:** Total Income, Total Expenses, Net Balance  
- **Line Chart:** Income vs Expense trend  
- **Pie Chart:** Category-wise expense breakdown  

#### 📌 Page 2 – Trends & Comparison
- **Column Chart:** Monthly Income vs Expenses  
- **Stacked Chart:** Category spend over months  
- **Slicers:** Year, Month, Transaction Type, Merchant  

![page1](https://github.com/user-attachments/assets/8fa709ee-5b2f-4900-906d-6158a8683166)
![part2](https://github.com/user-attachments/assets/07e999bc-49a8-469d-af23-0cb95f6e978b)
---

### 🗄️ Database Schema

#### 1️⃣ accounts table
```sql
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

#### 2️⃣ merchants table
CREATE TABLE merchants (
    merchant_id SERIAL PRIMARY KEY,
    merchant_name VARCHAR(255) NOT NULL,
    category VARCHAR(100)
);
#### 3️⃣ transactions table
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

#### 4️⃣ (Optional) users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
🔗 Relation: accounts.user_id → users.user_id

## 🛠️ How This Fits in ETL

✨ The pipeline works in **four stages**:

**🔹 Extract →** Fetch JSON data from the Mock API  
**🔹 Transform →** Clean data & add derived fields (`year`, `month`, `transaction_type`)  
**🔹 Load →** Insert the processed data into PostgreSQL schema  
**🔹 Visualize →** Build interactive Power BI dashboards for financial insights  

---

### 🔄 ETL Flow Diagram

```mermaid
flowchart LR
    A[📥 Extract<br/>Mock API] --> B[🧹 Transform<br/>Clean & Enrich Data]
    B --> C[🗄️ Load<br/>PostgreSQL Database]
    C --> D[📊 Visualize<br/>Power BI Dashboards]


