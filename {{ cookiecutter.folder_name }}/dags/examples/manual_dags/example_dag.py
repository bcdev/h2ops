from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    "start_date": days_ago(0),
    "retries": 1,
}


def add_your_first_task(ti):
    ti.xcom_push(key="first_task_output", value="Some processed data")
    print("First Task Completed")


def add_your_second_task(ti):
    first_task_data = ti.xcom_pull(task_ids="first_task", key="first_task_output")
    print(f"Second Task Completed with {first_task_data}")


def third_task(my_param):
    print(f"Processing parameter: {my_param}")


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

    third_task = PythonOperator(
        task_id="third_task",
        python_callable=third_task,
        op_kwargs={"my_param": "test_value"},
        dag=dag,
    )

    bash_task = BashOperator(
        task_id="run_script",
        bash_command="python /opt/airflow/{{ cookiecutter.package_name }}/train/example_bash.py option1",
        dag=dag,
    )

    first_task >> second_task
    first_task >> third_task
    third_task >> bash_task
