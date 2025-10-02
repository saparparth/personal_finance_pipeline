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
