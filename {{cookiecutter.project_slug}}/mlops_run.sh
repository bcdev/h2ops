#!/bin/bash
mkdir -p mlflow_artifacts
mkdir -p logs
chmod 777 mlflow_artifacts
chmod 777 logs
docker compose up
