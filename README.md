# MLOps Project Cookiecutter Template

A comprehensive cookiecutter template for machine learning projects
incorporating MLOps practices using `Airflow`, `MLFlow`, and `JupyterLab`.

## Overview

This template provides a standardized project structure for ML initiatives at BC,
integrating essential MLOps tools:
- **Apache Airflow**: For orchestrating ML pipelines and workflows
- **MLflow**: For experiment tracking and model registry
- **JupyterLab**: For interactive development and experimentation

## Project Structure

```
├── .github/            # GitHub Actions workflows
├── dags/               # Airflow DAG definitions
├── notebooks/          # JupyterLab notebooks
├── src/
│   ├── train/          # Model training
│   ├── preprocess/     # Feature engineering
│   ├── postprocess/    # Postprocess model output
│   └── utils/          # Utility functions
├── tests/              # Unit and integration tests
├── mlflow-artifacts/   # MLflow artifacts
├── mlops_run.sh        # Shell script to start MLOps services locally
├── docker-compose.yml  # Docker compose that spins up all services locally for MLOps
├── pipeline-config.yml # Configure your airflow DAGs
└── dockerfiles/        # Dockerfiles and compose files
```

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.8+
- [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html#install-cookiecutter)

### Installation

1. Generate the project from template:
```bash
  cookiecutter https://github.com/bcdev/cookiecutter-mlops
```

1.1

When prompted for input, enter the details requested. For e.g.

Add image of cookiecutter creation

2. Start the services:
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

3. Stopping the services
```bash
  ctrl + C
```

### Accessing Services

Wait for the services to start (usually take 2-3 mins, might take longer the first time)

- Airflow UI: http://localhost:8080
- MLflow UI: http://localhost:5000
- JupyterLab: http://localhost:8895

## Usage


### Development Workflow

1. Develop and experiment in JupyterLab
2. Refactor production code into the `src/` directory
3. Create tests in the `tests/` directory
4. Update CI/CD pipelines using the provided GitHub Actions workflows (if required)

### Creating ML Pipelines

1. Define your data processing and model training steps in the `src/` directory
2. Create Airflow DAGs in `dags/` to orchestrate your pipeline
3. Track experiments using MLflow in your training scripts:


## Configuration


## Acknowledgments

- [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [Apache Airflow](https://airflow.apache.org/)
- [MLflow](https://mlflow.org/)
- [JupyterLab](https://jupyterlab.readthedocs.io/)