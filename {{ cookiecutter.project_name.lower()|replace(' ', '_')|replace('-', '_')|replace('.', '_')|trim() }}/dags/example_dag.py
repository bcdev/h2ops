from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    "start_date": days_ago(0),
    "retries": 1,
}


def add_your_first_task():
    print("First Task Completed")


def add_your_second_task():
    print("Second Task Completed")


with DAG(
    "your_dag_id",
    default_args=default_args,
    schedule_interval=None,
    tags=["your_dag_tags"],
) as dag:

    first_task = PythonOperator(
        task_id="first_task",
        python_callable=add_your_first_task,
        dag=dag,
    )

    second_task = PythonOperator(
        task_id="second_task",
        python_callable=add_your_second_task,
        dag=dag,
    )

    first_task >> second_task
