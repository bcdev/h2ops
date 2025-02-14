# Hi, I am Model Training Script Template.
# Please update me in the required places.
# You can run me as is to see how everything works.
# There are some instructions below that tell you how to use mlflow
# in-conjunction with your code to track your experiments.
# Once you are comfortable, please delete all these comments including me.


def load_data(file_path: str):
    """
    Function to load the preprocessed dataset.

    Args:
        file_path (str): The path to the preprocessed data file.

    Returns:
        The loaded preprocessed data.
    """
    print(f"Loading preprocessed data from {file_path}")
    # TODO: Implement actual data loading logic
    return None  # Replace with actual dataset


def prepare_data(data):
    """
    Function to prepare data for training by separating features (X) and target (y).

    Args:
        data: The preprocessed dataset.

    Returns:
        tuple: A tuple containing the features (X) and target (y).
    """
    print("Preparing data for training...")
    # TODO: Implement feature-target separation
    X, y = None, None  # Replace with actual values
    return X, y


def train_model(X, y):
    """
    Function to train a machine learning model.

    Args:
        X: The feature data.
        y: The target variable.

    Returns:
        The trained machine learning model.
    """
    print("Training model...")
    # TODO: Implement model training logic
    model = None  # Replace with actual model
    return model


def evaluate_model(model, X, y):
    """
    Function to evaluate the trained model's performance.

    Args:
        model: The trained machine learning model.
        X: The feature data.
        y: The target variable.
    """
    print("Evaluating model...")
    # TODO: Implement model evaluation logic
    print("Evaluation metrics: ...")  # Replace with actual evaluation


def train_and_evaluate(file_path: str):
    """
    General training and evaluation pipeline.

    Args:
        file_path (str): The path to the preprocessed data.
    """
    data = load_data(file_path)
    X, y = prepare_data(data)
    model = train_model(X, y)
    evaluate_model(model, X, y)
    print("Model training and evaluation complete!")


if __name__ == "__main__":
    # Modify this path to point to the preprocessed data file
    file_path = "path/to/your/processed_data.file"  # Update this with the actual path
    train_and_evaluate(file_path)

    # ------------------------------------------------------
    # HOW TO USE MLflow FOR EXPERIMENT TRACKING
    # ------------------------------------------------------

    """
    # 1. Import MLflow
    import mlflow

    # 2. Start an MLflow experiment (ensure the MLflow tracking server is running)
    mlflow.set_tracking_uri(os.getenv("J_MLFLOW_SERVER_URI"))
    experiment_id = get_or_create_experiment("your-experiment-name")
    mlflow.set_experiment("experiment_name")

    # 3. Start a parent run
    with mlflow.start_run(run_name="Parent_Run"):

        # Log general parameters (you would do this only when you dont want to 
        # Hyperparameter tuning). If you want to HPT, start a child run as shown
        # a few lines below.
        # (https://mlflow.org/docs/latest/python_api/mlflow.html?highlight=log_artifacts#mlflow.log_param)
        mlflow.log_param("learning_rate", 0.01)
        mlflow.log_param("batch_size", 32)

        # Log a local file or directory as an artifact (https://mlflow.org/docs/latest/python_api/mlflow.html?highlight=log_artifacts#mlflow.log_artifact)
        mlflow.log_artifact("path")
        
        # Log an image (https://mlflow.org/docs/latest/python_api/mlflow.html?highlight=log_artifacts#mlflow.log_image)
        mlflow.log_image(image: Union[numpy.ndarray, PIL.Image.Image, mlflow.Image])
        
        # Log a figure (https://mlflow.org/docs/latest/python_api/mlflow.html?highlight=log_artifacts#mlflow.log_figure)
        mlflow.log_figure(figure: Union[matplotlib.figure.Figure, plotly.graph_objects.Figure], artifact_file: str)
        
        # Log multiple parameters (https://mlflow.org/docs/latest/python_api/mlflow.html?highlight=log_artifacts#mlflow.log_params)
        mlflow.log_params(params: dict)
        
        # Log metrics (https://mlflow.org/docs/latest/python_api/mlflow.html?highlight=log_artifacts#mlflow.log_metrics)
        mlflow.log_metrics(metrics: dict)
        
        
        ########################################################################
        # Use mlflow.autolog() to log everything that mlflow can log 
        # automatically
        # (https://mlflow.org/docs/latest/python_api/mlflow.html?highlight=log_artifacts#mlflow.autolog)
        ########################################################################
        mlflow.autolog()

        # Start a child run for hyperparameter tuning
        for i, param_value in enumerate([0.001, 0.01, 0.1]):
            with mlflow.start_run(run_name=f"Child_Run_{i}", nested=True):

                
                # Train model with different hyperparameters
                model = train_model(X, y, learning_rate=param_value)

                # Log metrics, params, artifacts, images etc per run.
                accuracy = evaluate_model(model, X, y)
                
                # Log models based on the library you chose (if supported by 
                # mlflow)
                # Currently the following libraries are supported:
                # https://mlflow.org/docs/latest/search.html?q=log_model&check_keywords=yes&area=default
                mlflow.<flavor>.log_model(model, path)

    # 4. View your experiment runs
        Go to http://127.0.0.1:5000 to view your experiments
    """
