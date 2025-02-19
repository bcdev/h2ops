import numpy as np

from tensorflow.keras.datasets import mnist


def load_raw_data():
    return mnist.load_data()


def load_preprocessed_data(preprocessed_path: str):

    data = np.load(preprocessed_path)
    X_train, y_train = data["X_train"], data["y_train"]
    X_test, y_test = data["X_test"], data["y_test"]
    return (X_train, y_train), (X_test, y_test)
