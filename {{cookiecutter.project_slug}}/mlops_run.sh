#!/bin/bash

mkdir -p mlflow_artifacts
mkdir -p logs

chmod -R 777 mlflow_artifacts
chmod -R 777 logs

jupyter lab --ip=0.0.0.0 --port=8893 > logs/jupyter.log 2>&1 &
jupyter_pid=$!
docker compose build
docker compose up

