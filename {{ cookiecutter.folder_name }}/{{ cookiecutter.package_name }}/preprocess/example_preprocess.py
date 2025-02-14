# PLEASE DELETE ME AFTER YOU ARE DONE UNDERSTANDING!!

import os
import numpy as np

from datetime import datetime

from botocore.exceptions import ClientError
from dotenv import load_dotenv
from tensorflow.keras.datasets import mnist

from {{ cookiecutter.package_name }}.utils.utils import get_s3_client

load_dotenv()

s3 = get_s3_client(
    endpoint_url=os.getenv("MLFLOW_S3_ENDPOINT_URL"),
    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def load_data():
    return mnist.load_data()


def feature_engineering(X_train, X_test):
    X_train = X_train.astype("float32") / 255.0
    X_test = X_test.astype("float32") / 255.0
    X_train = np.expand_dims(X_train, axis=-1)
    X_test = np.expand_dims(X_test, axis=-1)

    return X_train, X_test, X_train, X_test


def save_data(X_train, y_train, X_test, y_test, path, timestamp):
    np.savez_compressed(
        path, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test
    )

    bucket_name = "mnist-data"
    object_path = f"preprocessing/{timestamp}/mnist_processed.npz"

    try:
        s3.head_bucket(Bucket=bucket_name)
    except (NameError, ClientError):
        print(f"Bucket: {bucket_name} does not exist, creating one now!")
        s3.create_bucket(Bucket=bucket_name)

    s3.upload_file(path, bucket_name, object_path)

    os.remove(path)
    print(f"Preprocessed data stored to MinIO: {object_path}")


def preprocess():
    (X_train, y_train), (X_test, y_test) = load_data()
    data = feature_engineering(X_train, X_test)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = f"/tmp/mnist_processed_{timestamp}.npz"
    save_data(data, path, timestamp)

    print("Preprocessing complete!")
    return path


def preprocess_dummy():
    # You should define your preprocess method that does the same pre-processing
    # as done before training so that the pipeline does the same before the
    # model's inference.
    # Keep in mind that this preprocess_method should be able to handle both
    # batch and single input data.
    # You can of course have a single preprocess for both training and
    # inference.
    print("Dummy preprocess called!")


if __name__ == "__main__":
    preprocess()
