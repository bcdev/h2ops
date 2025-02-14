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

import mlflow.pyfunc


# To create your own custom model, extend this class: mlflow.pyfunc.PythonModel
class ModelPipelineModel(mlflow.pyfunc.PythonModel):
    def __init__(self, trained_model):
        """
        When you log your model using mlflow.pyfunc.log_model(
        ModelPipelineModel(model)), you can pass in your model, which is then
        uses as trained_model here.
        """
        self.model = trained_model

    def preprocess(self, input_data):
        """
        Change me!
        This currently just calls a preprocess_dummy() to show how to invoke
        preprocess functions from this model.
        Update this to use your preprocessing script that you have used for
        training and also want to use before running predictions on the input
        data.
        """
        print("Preprocessing input data...")
        return input_data

    def postprocess(self, predictions):
        """
        Change me! (if required)
        There could be some postprocessing that you would like to do after
        the predictions from the model. You can invoke or put them here.
        """
        print("Postprocessing predictions...")
        return predictions

    def predict(self, context, model_input):
        """
        Runs full pipeline: Preprocess -> Model Inference -> Postprocess.

        You can change this as well based on your requirements.
        """
        print("Running full pipeline...")
        processed_input = self.preprocess(model_input)
        raw_predictions = self.model.predict(processed_input)
        return self.postprocess(raw_predictions)
