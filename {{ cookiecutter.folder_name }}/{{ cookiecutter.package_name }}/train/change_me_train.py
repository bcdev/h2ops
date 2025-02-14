# Hi, I am Model Training Script Template.
# Please update me in the required places.
# You can run me as is to see how everything works.
# There are some instructions below that tell you how to use mlflow
# in-conjunction with your code to track your experiments.
# Once you are comfortable, please delete all these comments including me.


def load_data(path_to_data: str):
    """
    Function to load the preprocessed dataset.

    Args:
        path_to_data (str): The path to the preprocessed data file.

    Returns:
        The loaded preprocessed data.
    """
    print(f"Loading preprocessed data from {file_path}")
    # TODO: Implement actual data loading logic
    data = ...
    return data


class Trainer:
    def __init__(self, model, train_data, test_data, hyperparams, trained_model_path):
        self.model = model
        self.train_data = train_data
        self.test_data = test_data
        self.hyperparams = hyperparams
        self.trained_model_path = trained_model_path

    def train(self):
        """
        Function to train a machine learning model.
        Returns:
            The trained machine learning model.
        """
        print("Training model...")
        # TODO: Implement model training logic with mlflow logging
        # self.model.fit(self.train_data) or something like that using
        # self.hyperparams
        trained_model = ...
        print("Evaluating model...")
        # TODO: Implement model evaluation logic
        print("Evaluation metrics: ...")
        # TODO: Save model # save model to self.trained_model_path
        print("Model training and evaluation complete!")
        return trained_model

    def train_and_evaluate(self, file_path: str):
        """
        General training and evaluation pipeline.

        Args:
            file_path (str): The path to the preprocessed data.
        """
        data = self.load_data(file_path)
        model = self.train_model(data)
        self.evaluate_model(model, data)
        print("Model training and evaluation complete!")


if __name__ == "__main__":
    # Modify this path to point to the preprocessed data file
    file_path = "path/to/your/processed_data.file"
    train_data, test_data = load_data(file_path)
    from {{ cookiecutter.package_name }}.models.change_me_model import get_model
    model = get_model()
    hyperparams = {}
    trained_model_path = "path/to/save/your/model"
    trainer = Trainer(model, train_data, test_data, hyperparams,
                   trained_model_path)
    trainer.train()

    # ------------------------------------------------------
    # HOW TO USE MLFlow FOR EXPERIMENT TRACKING
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
                
                # For logging custom models, define them as shown in 
                # change_me_model_pipeline.py and then you can log models 
                # like this:
                mlflow.pyfunc.log_model(CustomModel(model), path)

    # 4. View your experiment runs
        Go to http://127.0.0.1:5000 to view your experiments
    """
