import os
import itertools

import mlflow
import numpy as np
from dotenv import load_dotenv

os.environ["KERAS_BACKEND"] = "tensorflow"
import keras

from src.utils.utils import get_s3_client, get_latest_data_path, get_or_create_experiment

load_dotenv()

s3 = get_s3_client(
    endpoint_url=os.getenv("MLFLOW_S3_ENDPOINT_URL"),
    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def train_mnist_autolog():

    bucket_name = "mnist-data"
    base_folder = "preprocessing"
    s3_path, filename = get_latest_data_path(
        s3, bucket_name=bucket_name, base_folder=base_folder
    )
    local_path = "/tmp"
    local_file = f"{local_path}/{filename}"
    s3.download_file(bucket_name, s3_path, local_file)

    data = np.load(local_file)
    X_train, y_train = data["X_train"], data["y_train"]
    X_test, y_test = data["X_test"], data["y_test"]

    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)

    mlflow.set_tracking_uri(os.getenv("J_MLFLOW_SERVER_URI"))
    experiment_id = get_or_create_experiment("MNIST_Hyperparameter_Search_autolog")
    mlflow.set_experiment(experiment_id=experiment_id)

    best_accuracy = 0
    best_model = None
    best_params = {}

    HYPERPARAM_GRID = {"epochs": [1, 2]}

    keys, values = zip(*HYPERPARAM_GRID.items())
    param_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
    mlflow.autolog()
    with mlflow.start_run(run_name="mnist-hyperparameter-tuning-parent"):
        for params in param_combinations:
            with mlflow.start_run(nested=True):
                mlflow.log_param(key="data_source", value=s3_path)
                model = keras.Sequential(
                    [
                        keras.layers.Conv2D(
                            32, (3, 3), activation="relu", input_shape=(28, 28, 1)
                        ),
                        keras.layers.MaxPooling2D((2, 2)),
                        keras.layers.Flatten(),
                        keras.layers.Dense(128, activation="relu"),
                        keras.layers.Dense(10, activation="softmax"),
                    ]
                )

                optimizer = keras.optimizers.Adam(learning_rate=0.001)
                model.compile(
                    optimizer=optimizer,
                    loss="categorical_crossentropy",
                    metrics=["accuracy"],
                )
                history = model.fit(
                    X_train,
                    y_train,
                    epochs=params["epochs"],
                    validation_data=(X_test, y_test),
                )

                val_acc = history.history["val_accuracy"][-1]

                if val_acc > best_accuracy:
                    best_accuracy = val_acc
                    best_model = model
                    best_params = params

            if best_model is not None:
                artifact_path = "mnist_model_autolog"
                mlflow.tensorflow.log_model(model, artifact_path)

                model_uri = mlflow.get_artifact_uri(artifact_path)

                print(f"Best model accuracy: {best_accuracy:.4f}")
                print("Best model params: ", best_params)
                print("Model stored at ", model_uri)
