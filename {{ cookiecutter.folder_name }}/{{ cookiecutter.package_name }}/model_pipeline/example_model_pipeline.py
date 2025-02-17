# Hi I am a Custom Python MLFlow model.
# Usually, when you log models in an mlflow experiment, you would use the
# log_model() from the ML python library that you are using to train your model.
# For e.g., if you use tensorflow, you would do something like
# mlflow.tensorflow.log_model(model)
# Now, this model can be registered and then be deployed using docker
# containers or locally. Then you can send requests with your input data to
# this model. But if you have to do some preprocessing and/or postprocessing
# steps before/after the prediction, you either have to create your own
# FastAPI or Flask server to do that or you can make use of MLFlow's custom
# python models as shown below.

# PLEASE DELETE ME AFTER YOU ARE DONE UNDERSTANDING!!

import mlflow.pyfunc


# To create your own custom model, extend this class: mlflow.pyfunc.PythonModel
class ModelPipelineModel(mlflow.pyfunc.PythonModel):
    """
    This is a custom MLflow model that handles:
    - Preprocessing
    - Inference
    - Postprocessing
    """
    def __init__(self, trained_model):
        self.model = trained_model

    def preprocess(self, input_data):
        from {{ cookiecutter.package_name }} import preprocess_single_image

        print("Preprocessing input data...")
        processed = preprocess_single_image(input_data)
        return processed

    def postprocess(self, predictions):
        from {{ cookiecutter.package_name }} import postprocess

        print("Postprocessing predictions...")
        postprocessed = postprocess(predictions)
        return postprocessed

    def predict(self, context, model_input):
        """
        Runs full pipeline: Preprocess -> Model Inference -> Postprocess.
        """
        print("Running full pipeline...")
        processed_input = self.preprocess(model_input)
        raw_predictions = self.model.predict(processed_input)
        return self.postprocess(raw_predictions)
