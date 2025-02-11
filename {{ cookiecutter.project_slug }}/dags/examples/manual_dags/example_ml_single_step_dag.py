from airflow import DAG
from airflow.operators.python import PythonOperator

from airflow.utils.dates import days_ago

from src import train

with DAG(
    dag_id="test_ml_python_operator",
    start_date=days_ago(0),
) as dag:
    train = PythonOperator(task_id="train", python_callable=train, dag=dag)
