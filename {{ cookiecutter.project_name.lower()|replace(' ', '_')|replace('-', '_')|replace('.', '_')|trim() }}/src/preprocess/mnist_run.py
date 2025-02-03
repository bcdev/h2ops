import os
import numpy as np

from datetime import datetime
from dotenv import load_dotenv
from tensorflow.keras.datasets import mnist

from ..utils.utils import get_s3_client

load_dotenv()

s3 = get_s3_client(
    endpoint_url=os.getenv("J_MLFLOW_S3_ENDPOINT_URL"),
    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)


def preprocess_and_store():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0
    X_train = np.expand_dims(X_train, axis=-1)
    X_test = np.expand_dims(X_test, axis=-1)

    local_path = f"/tmp/mnist_processed_{timestamp}.npz"
    np.savez_compressed(local_path,
                        X_train=X_train, y_train=y_train,
                        X_test=X_test, y_test=y_test)

    bucket_name = "mnist-data"
    object_path = f"preprocessing/{timestamp}/mnist_processed.npz"

    try:
        s3.head_bucket(Bucket=bucket_name)
    except:
        print(f"Bucket: {bucket_name} does not exist, creating one now!")
        s3.create_bucket(Bucket=bucket_name)

    s3.upload_file(local_path, bucket_name, object_path)

    os.remove(local_path)
    print(f"Preprocessed data stored to MinIO: {object_path}")