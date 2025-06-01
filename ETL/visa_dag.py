from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from visa_etl_logic import main

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 5, 31),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="visa_full_pipeline",
    default_args=default_args,
    description="ETL pipeline for visa data",
    schedule_interval='@daily',
    catchup=False,
    tags=["visa", "etl"],
)

etl_task = PythonOperator(
    task_id="etl_task",
    python_callable=main,
    dag=dag,
)

etl_task
