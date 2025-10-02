import sys
import os

# Add the scripts folder to Python path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = "/home/parth/personal_finace_project"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
from scripts.transform import transform
from scripts.load import load_to_db


from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


URL = "https://68d9ff4590a75154f0db97c6.mockapi.io/personal_account"

default_args = {
    "owner": "parth",
    "depends_on_past": False,
    "email": ["parthsapar2@gmail.com"],  
    "email_on_failure": True,              # 👈 enable email alerts
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="personal_finance_etl",
    default_args=default_args,
    description="ETL pipeline for personal finance",
    schedule_interval="*/3 * * * *",  # 👈 every 3 minutes for testing
    # schedule_interval="@hourly",        # 👈 change here when moving to hourly
    start_date=datetime(2025, 9, 30),
    catchup=False,
    tags=["finance", "ETL"],
) as dag:

    def run_transform():
        return transform(URL)

    def run_load():
        load_to_db()

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=run_transform
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=run_load
    )

    transform_task >> load_task
