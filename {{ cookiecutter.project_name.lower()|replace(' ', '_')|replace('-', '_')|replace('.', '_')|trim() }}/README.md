{{ cookiecutter.project_name }}

## Project Development

### Prerequisites

- [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.8+

1. Start the services:
```bash
  chmod +x mlops_run.sh
```
```bash
  ./mlops_run.sh 
```
Use the following flags to modify the behaviour of the script
```commandline
-c -> to build docker images with/without cache; defaults to true; options [true, false]
-j -> to change the port of jupyter lab instance running; defaults to 8895
-v -> to shut down docker with/without deleting attached volumes; defaults to false; options [true, false]
```

1. Stopping the services
```bash
  ctrl + C
```

The following services are available as a part of the current MLOps framework

- Airflow UI: http://0.0.0.0:8080
- MLflow UI: http://localhost:5000
- JupyterLab: Opens up JupyterLab automatically at port 8895
{% if cookiecutter.use_minio == "yes" %}
- Minio (Local S3): http://localhost:9000
{% else %}
- This project now uses local artifact storage which you can find at 
  `/mlflow_artifacts` at the root of this project
{% endif %}
