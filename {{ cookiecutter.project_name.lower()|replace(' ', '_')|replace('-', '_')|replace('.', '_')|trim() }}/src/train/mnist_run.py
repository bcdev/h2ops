import itertools
import os
from datetime import datetime

import numpy as np

import mlflow
from dotenv import load_dotenv
from keras.src.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

from ..utils.utils import get_s3_client, get_latest_data_path, get_or_create_experiment

load_dotenv()

s3 = get_s3_client(
    endpoint_url=os.getenv("MLFLOW_S3_ENDPOINT_URL"),
    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def train_mnist():

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

    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)

    mlflow.set_tracking_uri(os.getenv("J_MLFLOW_SERVER_URI"))
    experiment_id = get_or_create_experiment("MNIST_Hyperparameter_Search")
    mlflow.set_experiment(experiment_id=experiment_id)

    best_accuracy = 0
    best_model = None
    best_params = {}

    HYPERPARAM_GRID = {"learning_rate": [0.001, 0.01], "epochs": [2, 4]}

    keys, values = zip(*HYPERPARAM_GRID.items())
    param_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]

    for params in param_combinations:
        with mlflow.start_run(nested=True):

            model = Sequential(
                [
                    Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
                    MaxPooling2D((2, 2)),
                    Flatten(),
                    Dense(128, activation="relu"),
                    Dense(10, activation="softmax"),
                ]
            )

            optimizer = Adam(learning_rate=params["learning_rate"])
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
            train_acc = history.history["accuracy"][-1]
            mlflow.log_metrics(
                {
                    "validation_accuracy": val_acc,
                    "training_accuracy": train_acc,
                    "validation_loss": history.history["val_loss"][-1],
                    "training_loss": history.history["loss"][-1],
                }
            )

            mlflow.log_param(key="data_source", value=s3_path)

            if val_acc > best_accuracy:
                best_accuracy = val_acc
                best_model = model
                best_params = params

    if best_model is not None:
        artifact_path = "mnist_model"
        mlflow.tensorflow.log_model(model, artifact_path)

        model_uri = mlflow.get_artifact_uri(artifact_path)

        print(f"Best model accuracy: {best_accuracy:.4f}")
        print(f"Best model params: {best_params}")
        print(f"Model stored at: {model_uri}")
