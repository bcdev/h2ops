# Hi, I am the python file that you need to update when you are ready to create
# the dags. This step is usually done
# when you have your code ready in your {{ cookiecutter.package_name }} package.

# NOTE: Please delete all these comments once you have understood how to use
# this python file to create your own dags.

# Some basics to understand the creation of Airflow DAGs
#
# Dags in airflow can triggered by defining the start_date and/or schedules (which can be manually triggered as well).
# For automatic triggers, defining the schedule is mandatory.
# For testing purposes, you can trigger them manually. If you would like to also manually trigger them for your workflow
# you can!
# But if you want your DAG to run periodically, setting the start_date and schedule is important.
# NOTE: By default, if you set a start_date in the past, Airflow will try to backfill all those runs. To avoid that,
# use catchup=False inside the dag definitions as you can see in the example dag definition below.
#
# `DAG` - Directed Acyclic Graphs -> collection of tasks with directional dependencies.
# `Pipeline/Workflow` -> Same as DAG. You can call your DAG a pipeline or workflow.
# `description` -> description for the DAG to be shown on the webserver
# `start_date` -> The timestamp from which the scheduler will attempt to backfill the dag runs. Recommended to keep it
#                 the date when you would run it for the first time and don't change it.
# `schedule` -> Defines the rules according to which DAG runs are scheduled. Can accept cron string, timedelta object,
#               Timetable, or list of Dataset objects. If this is not provided, the DAG will be set to the default
#               schedule timedelta(days=1).
# `catchup` -> Perform scheduler catchup by backfilling runs (or only run latest)
# `task_groups` -> Used to organize tasks into hierarchical groups in Graph view.
# `tasks` -> The actual tasks that needs to run. Airflow by default provides several operators to run various types of
#            tasks. For e.g., if you want to run a Bash operation, you can use the BashOperator, if you would like to
#            run Python, use the PythonOperator. When and if this goes to production, we will use KubermetesPodOperator,
#            but you dont have to worry about that now. Most likely for testing and running experiments locally, we
#            recommend using BashOperator and PythonOperator. We have provided some examples below on how to use them.
# `dependencies` -> This basically defines the flow of your DAG i.e. which task is dependent on which. Be careful to
#                   avoid cyclic dependencies as this is supposed to be an acyclic graph.


from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from {{ cookiecutter.package_name }} import preprocess, train

# Define default arguments
# Please change the start date as today (the day you will run this dag for the
# first time) and keep it static.
default_args = {
    "owner": "change_your_name_here",
    "start_date": datetime(2025, 2, 1),
}

# Create the DAG
# Keep `catchup` as false if you would not like to backfill the runs if the
# start_date is in the past.
# To learn more about cron expressions, see here: https://crontab.guru/.
with DAG(
    "change_your_dag_name_here_dag",
    default_args=default_args,
    description="change your description here",
    schedule_interval="0 0 * * *",
    catchup=False,
    tags=["python_dag"]
) as dag:

    # Define the bash task. If you would like to run bash scripts, use this
    # operator.
    # You can invoke the scripts that you have written in the scripts folder by using:
    # bash_command="${AIRFLOW_HOME}/scripts/your_script"
    change_task_1 = BashOperator(task_id="bash_demo", bash_command="echo 1")

    # Create task group
    with TaskGroup(group_id="change_task_group_23", tooltip="change your task group tooltip") as tg:

        # Define preprocess task. If you would like to run python scripts,
        # use this operator.
        # Please update the python_callable key here to point to your file in
        # your `{{ cookiecutter.package_name }}` package. It is currently set
        # to `preprocess` as an example which is imported above.
        # You can pass parameters as follows to your python callable, if required.
        # op_kwargs={"your_param": "your_value"},
        change_task_2 = PythonOperator(
            task_id="preprocess",
            python_callable=preprocess,  # Replace with your actual function
            # op_kwargs={"your_param": "your_value"}
        )

        # Define train task
        # If you would like to run python scripts, use this operator.
        # Please update the python_callable key here to point to your file in
        # your `{{ cookiecutter.package_name }}` package. It is currently set
        # to `train` as an example which is imported above.
        change_task_3 = PythonOperator(
            task_id="train",
            python_callable=train  # Replace with your actual function
        )

        # Set dependencies within the task group
        change_task_2 >> change_task_3

    # Set main DAG dependencies
    change_task_1 >> tg
