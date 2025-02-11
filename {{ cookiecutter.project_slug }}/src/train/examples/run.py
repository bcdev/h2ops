import os

import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import pandas as pd

def train(ti, my_param: str = None):
    '''
    The second argument `ti` is the Task Instance that Airflow passes it to the
    Python functions that the PythonOperator invokes.
    You can add this argument anywhere is your argument list.
    It provides a feature called `XCom` that means Cross-Communications which
    facilitates sharing small amounts of data from one task to another.
    See the usage below for ti.xcom_pull and to.xcom_push if you need to share
    the data to downstream tasks or get the task from upstream tasks
    respectively.
    '''
    print("Begin config")

    # You can pull the data from the xcom from Upstream tasks as follows:
    # If a task is not in a task group, just use the task_id, if not you can
    # specify the task id along with the task group shown below.
    # By default, airflow xcom uses return_value as the key. If you have
    # already passed some information via xcom using some other key, please
    # use that instead.
    pulled_data = ti.xcom_pull(task_ids="task_group_23.task_2",
                 key="return_value")

    print("Passed in Parameter:", my_param, pulled_data)
    X, y = load_iris(return_X_y=True)

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)

    mlflow.set_tracking_uri(os.getenv("MLFLOW_SERVER_URI"))
    print("end config")
    with mlflow.start_run():
        print("Begin logging")
        mlflow.log_param("model_type", "logistic_regression")
        mlflow.log_metric("test_accuracy", 0.95)
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="iris_model",
            registered_model_name="tiny_iris_classifier"
        )
        print("End logging")

    model = mlflow.pyfunc.load_model("models:/tiny_iris_classifier/latest")

    sample_data = pd.DataFrame([[5.1, 3.5, 1.4, 0.2]],
      columns=["sepal length (cm)", "sepal width (cm)", "petal length (cm)",
               "petal width (cm)"])

    prediction = model.predict(sample_data)
    print(prediction)
    mlflow.get_artifact_uri("iris_model")

    # You can push the data to xcom for the downstream tasks as follows.
    ti.xcom_push(key="train_output", value=mlflow.get_artifact_uri("iris_model"))

