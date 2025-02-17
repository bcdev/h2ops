import os

import numpy as np

from {{ cookiecutter.package_name }}.utils.utils import (
    get_s3_client,
)

def load_data(preprocessed_path, bucket_name):
    s3 = get_s3_client(
        endpoint_url=os.getenv("MLFLOW_S3_ENDPOINT_URL"),
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    local_path = "/tmp"
    local_file = f"{local_path}/{preprocessed_path.split("/")[-1]}"
    s3.download_file(bucket_name, preprocessed_path, local_file)

    data = np.load(local_file)
    X_train, y_train = data["X_train"], data["y_train"]
    X_test, y_test = data["X_test"], data["y_test"]
    return (X_train, y_train), (X_test, y_test), preprocessed_path

