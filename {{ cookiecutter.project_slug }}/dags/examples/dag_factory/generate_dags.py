import os
from pathlib import Path
from airflow import DAG
import dagfactory

BASE_DIR = Path(__file__).resolve().parent
config_file = BASE_DIR / "pipeline-config.yml"
print(f"Loading config file from: {config_file}")

if not config_file.exists():
    raise FileNotFoundError(f"Config file not found: {config_file}")


def print_xcom(ti):
    bash_output = ti.xcom_pull(task_ids="task_1")  # Pull from task_1
    print(f"Bash Output: {bash_output}")


dag_factory = dagfactory.DagFactory(str(config_file))

dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())

with DAG("basic_example_dag") as dag:
    task_4 = dag.get_task("task_4")
    task_4.python_callable = print_xcom
