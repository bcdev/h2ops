from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from src import train_mnist
from src import preprocess_and_store

default_args = {
    'start_date': days_ago(0),
    'retries': 1,
}

with DAG(
    'mnist_pipeline',
    default_args=default_args,
    schedule_interval=None,
    tags=['mnist']
) as dag:

    preprocess_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_and_store,
        dag=dag,
    )

    train_task = PythonOperator(
        task_id='hyperparameter_tuning',
        python_callable=train_mnist,
        dag=dag,
    )

    preprocess_task >> train_task