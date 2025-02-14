# Hi I am a Preprocessing Script Template
# Please update me in the required places.
# You can run me as is to see how everything works.
# Once you are comfortable, please delete all these comments including me.


def load_data(file_path: str):
    """
    Function to load the dataset.

    Args:
        file_path (str): The path to the dataset file.

    Returns:
        The loaded dataset (modify this return as needed).
    """
    print(f"Loading data from {file_path}")
    # TODO: Implement actual data loading logic
    return None  # Replace with actual dataset


def clean_data(data):
    """
    Function to clean the dataset.

    Args:
        data: The raw dataset.

    Returns:
        The cleaned dataset.
    """
    print("Cleaning data...")
    # TODO: Implement data cleaning logic
    return data  # Modify this as needed


def feature_engineering(data):
    """
    Function to create or modify features in the dataset.

    Args:
        data: The cleaned dataset.

    Returns:
        The dataset with new features.
    """
    print("Performing feature engineering...")
    # TODO: Implement feature engineering logic
    return data  # Modify this as needed


def save_data(data, path):
    """
    Function to create or modify features in the dataset.

    Args:
        data: The cleaned dataset.

    Returns:
        The dataset with new features.
    """
    print("Saving data...")
    # TODO: Implement saving your data to S3 MinIO if you choose MinIO as
    #  your storage backend else save it locally in the data folder.
    print("Saving data successful.")


def preprocess(file_path: str):
    """
    General preprocessing pipeline. Includes loading, cleaning, and feature engineering.

    Args:
        file_path (str): The path to the data file.

    Returns:
        The preprocessed dataset.
    """
    data = load_data(file_path)
    data = clean_data(data)
    data = feature_engineering(data)
    path = "path/to/store/your/preprocessed/file"
    save_data(data, path)

    print("Preprocessing complete!")
    return path


if __name__ == "__main__":
    # Modify the file path here to the location of your data file
    file_path = "path/to/your/data.file"  # Update this path
    processed_data = preprocess(file_path)
