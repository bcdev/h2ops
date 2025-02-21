# PLEASE DELETE ME AFTER YOU ARE DONE UNDERSTANDING!!

import numpy as np


def example_postprocess(predictions: np.ndarray):
    """
    Postprocess model predictions - works for both single and batch predictions

    Args:
        predictions: Model output of shape (batch_size, num_classes) or (1, num_classes)
                    for a single prediction

    Returns:
        For single prediction: single class index
        For batch: array of class indices
    """
    print("Postprocess called!")

    # Get predicted class indices
    predicted_classes = np.argmax(predictions, axis=1)

    # If it's a single prediction, return the scalar value
    if len(predicted_classes) == 1:
        return predicted_classes[0]

    # Otherwise return the array of predictions
    return predicted_classes


if __name__ == "__main__":
    # single pred
    data = np.random.rand(1, 10)
    postprocessed_results = example_postprocess(data)
    print("Before postprocessing", data)
    print("After postprocessing", postprocessed_results)

    # batch pred
    data = np.random.rand(4, 10)
    postprocessed_results = example_postprocess(data)
    print("Before postprocessing", data)
    print("After postprocessing", postprocessed_results)
