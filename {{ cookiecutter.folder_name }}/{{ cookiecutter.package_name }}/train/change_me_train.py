# Hi, I am Model Training Script Template.
# Please update me in the required places.
# You can run me as is to see how everything works.
# There are some instructions below that tell you how to use mlflow
# in-conjunction with your code to track your experiments.
# Once you are comfortable, please delete all these comments including me.

from typing import TYPE_CHECKING

import mlflow

from {{ cookiecutter.package_name }}.model_pipeline.change_me_model_pipeline import ModelPipelineModel

# This is to make sure that Airflow or its dependencies are not added to the
# environment of the Mlflow model as it is not required and might also bring
# issues related to packages. Better to avoid them. Please use the following
# syntax to use the TaskInstance for accessing xcom values.
if TYPE_CHECKING:
    from airflow.models import TaskInstance

def load_data(path_to_data: str):
    """
    Function to load the preprocessed dataset.

    Args:
        path_to_data (str): The path to the preprocessed data file.

    Returns:
        The loaded preprocessed data.
    """
    print(f"Loading preprocessed data from {path_to_data}")
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
        # TODO: Implement model training logic with mlflow logging (use
        #  autologging)
        print("Evaluating model...")
        # TODO: Implement model evaluation logic
        print("Saving model...")
        # TODO: Save model # save model to self.trained_model_path
        # example custom model saving
        # Here we log our custom model that we created.
        # It is important that we pass the code_paths argument which
        # contains your package as mlflow needs to find the code that
        # it needs to run.
        # Please make sure that none of the __init__.py files are
        # completely empty as this creates some issues with
        # mlflow logging. You can literally just add a # to the
        # __init__ file. This is needed because while serializing
        # the files, empty files have 0 bytes of content and that
        # creates issues with the urllib3 upload to S3 (this
        # happens inside MLFlow)
        artifact_path = "..."
        mlflow.pyfunc.log_model(
            python_model=ModelPipelineModel(self.model),
            artifact_path=artifact_path,
            # Code paths are required basically to package your
            # code along withe model if you have a custom model
            # that for e.g. might need a preprocessing script.
            # See here for more details:
            # https://mlflow.org/docs/latest/model/dependencies.html#id12
            code_paths=["{{ cookiecutter.package_name }}"],
            # sometimes when you deploy and run your model
            # inference, you might get errors like Module Not
            # found, for those cases, you can specify the
            # libraries that your code needs. For e.g.,
            # in preprocess script, if you need boto3, you need to
            # specify it here.
            # You can also specify conda env instead of pip if
            # needed.
            # This is just an example, if you do not need boto3, feel free to
            # remove it.
            # See here for more details:
            # https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html#mlflow.pyfunc.log_model
            extra_pip_requirements=["boto3==1.36.21"]
        )
        print("Model training and evaluation complete!")


def train(ti: "TaskInstance"=None):
    # Example xcom pull.
    # Consider the previous task in Airflow was preprocess which pushed the
    # path to xcom, we can pull it like this:
    # Note we use ml.preprocess if ml is the task_group name, else we just
    # use preprocess as the task_ids

    # preprocessed_path = ti.xcom_pull(task_ids="ml.preprocess",
    #                                  key="path")


    # Modify this path to point to the preprocessed data file
    file_path = "path/to/your/processed_data.file"
    train_data, test_data = load_data(file_path)
    from {{cookiecutter.package_name}}.models.change_me_model import get_model
    model = get_model()
    hyperparams = {}
    trained_model_path = "path/to/save/your/model"
    trainer = Trainer(model, train_data, test_data, hyperparams,
                      trained_model_path)
    trainer.train()

if __name__ == "__main__":
    train()


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
        # You can also use mlflow.autolog() along with the usual logging to log
        # parameters or text or images that autolog does not log automatically
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
