{{ cookiecutter.project_name }}

## Getting Started with MLOps

Now that you have created a project using the template provided, please follow
the steps below to start your ML journey.

1. Create and activate mamba environment.
You can update the `environment.yml` to include your libraries, or you can 
update them later as well.
```bash
  mamba env create
  mamba activate <your-env-name>
```

If you have created an environment using the steps above, and would like to 
update the mamba env after adding new libraries in `environment.yml`, do this:
```bash
  mamba env update
```

3. Start the services:
```bash
  chmod +x mlops-run.sh
```
```bash
  ./mlops-run.sh -b
```
The following flags exist which could alter the behaviour of the way the framework 
runs, but the user should not worry about it or change them if not needed.
```commandline
-c -> to build docker images without cache
-j -> to change the port of jupyter lab instance running; defaults to 8895
-v -> to delete attached volumes when shutting down
-b -> to build the docker images before starting the containers
```

When you run this for the first time, make sure you use the `-b` flag as it builds
the images for the first time as shown above.
Next time when you start it again, you start it without the flag as it saves 
time by not building the same images again:
```bash
  ./mlops-run.sh
```

4. Stopping the services:

You should stop these container services when you're done working 
with your project, need to free up system resources, or want to apply some updates.
To gracefully stop the services, run this in the terminal where you started them:
```bash
  ctrl + C
```

### Accessing the services

Wait for the services to start (usually take 2-3 mins, might take longer if you start it without cache)

- Airflow UI: http://localhost:8080
  - Login Details:
    - username: `admin`
    - password: `admin`
- MLflow UI: http://localhost:5000
- JupyterLab: Opens up JupyterLab automatically at port 8895
- Minio (Local S3): http://localhost:9000
  - Login Details:
    - username: `minio`
    - password: `minio123`


### Development Workflow

1. In the JupyterLab that was opened up in your browser, navigate to the 
`notebooks` folder and create notebooks where you can experiment with your 
data, models and log metrics, params and artifacts to MLFlow. 
There are some example notebooks provided in the `examples` 
directory tp help you get started. If you chose MinIO as your local S3, use it 
to mimic API calls to real S3 to make sure all works when this goes into 
production.
2. Once you have your logic ready for the data ingestion, preprocessing and 
training, refactor it to production code in the `src/` directory.
3. Create tests in the `tests/` directory to test your data preprocessing 
methods and data schema etc. Make them green.
4. Create a new dag in the `dags` folder using the `example_dag.py` template provided.
**NOTE**: This will be simplified in the future.
5. Now you can see your DAG in the [Airflow UI](http://localhost:8080). 
You can trigger by clicking the 
`Trigger DAG ▶️` button. You can now view the logs of
your dag's execution and its status.
6. If you chose [MinIO](http://localhost:9000) (recommended) during the project 
initialization for MLFLow artifact storage, you can view them in the MinIO UI to
check if everything was generated correctly.
7. While the model is training, you can track the model experiments on the 
[MLFlow UI](http://localhost:5000).


### Deployment workflow

Once you have a model trained, you can deploy it locally either as
container or serve it directly from MinIO S3.
We recommend to deploy it as a container as this makes sure that it has its 
own environment for serving.

#### Deploying Model as a Container locally

Since we have been working with docker containers so far, all the environment 
variables have been set for them, but now as we need to deploy them,
we would need to export a few variables so that MLFLow has access to them and 
can pull the required models from MinIO S3.

```bash
  export MLFLOW_TRACKING_URI=http://127.0.0.1:5000 
  export MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:9000 
  export AWS_ACCESS_KEY_ID=mini
  export AWS_SECRET_ACCESS_KEY=minio12
```

Once we have this variables exported, find out the `run_id` of the model you 
want to deploy from the MLFlow UI and run the following command:

```bash
  mlflow models build-docker -m runs:/<run-id>/model -n <name-of-your-container> --enable-mlserver
```

After this finishes, you can run the docker container by:

```bash
  docker run -p 5002:8080 <name-of-your-container> 
```

Now you have an endpoint ready at `127.0.0.1:5002`.

Have a look at `notebooks/examples/mlflow_docker_inference.ipynb` for an 
example on how to get predictions


####  Deploying local inference server

Prerequisites

- [Pyenv](https://github.com/pyenv/pyenv-installer)
- Make sure standard libraries in linux are upto date.
  ```
  sudo apt-get update
  sudo apt-get install -y build-essential
  sudo apt-get install --reinstall libffi-dev
  ```
- Run these commands to export the AWS (Local Minio server running)
  ```bash
   export AWS_ACCESS_KEY_ID=minio 
   export AWS_SECRET_ACCESS_KEY=minio123
   export MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:9000
  ```
- Now we are ready for local inference server. Run this after replacing the required stuff
    ```bash
    mlflow models serve -m s3://mlflow/0/<run_id>/artifacts/<model_name> -h 0.0.0.0 -p 3333
    ```
- We can now run inference against this server on the `/invocations` endpoint,
- run `local_inference.py` after changing your input data.

