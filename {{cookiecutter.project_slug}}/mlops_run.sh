#!/bin/bash

NO_CACHE=true
JUPYTER_PORT=8895
DELETE_VOLUME=false

while getopts "c:j:v:" opt; do
    case $opt in
        c) NO_CACHE="$OPTARG" ;;
        j) JUPYTER_PORT="$OPTARG" ;;
        v) DELETE_VOLUME="$OPTARG" ;;
        \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
    esac
done


cleanup() {
    echo "Shutting down services..."
    if [ "$DELETE_VOLUME" = true ]; then
      echo "Shutting down docker with deleting volumes"
      docker compose down -v
    else
      echo "Shutting down docker without deleting volumes"
      docker compose down
    fi
    echo "Cleanup complete"
}

trap cleanup EXIT INT TERM QUIT HUP

handle_error() {
    echo "Error: $1"
    exit 1
}

create_directory() {
    local dir_name=$1
    if [ ! -d "$dir_name" ]; then
        mkdir "$dir_name" || handle_error "Failed to create $dir_name directory"
        echo "Created directory: $dir_name"
    else
        echo "Directory $dir_name already exists"
    fi

    if chmod -R 777 "$dir_name" 2>/dev/null; then
        echo "Set permissions for $dir_name"
    else
        echo "Error: Could not set permissions for $dir_name."
    fi
}

check_port() {
    if lsof -Pi :"$1" -sTCP:LISTEN -t >/dev/null ; then
        handle_error "Port $1 is already in use. Please free up the port and try again."
    fi
}

echo "Setting up directories..."
create_directory "mlflow_artifacts"
create_directory "logs"

check_port "$JUPYTER_PORT"

echo "Starting Docker Compose services..."
if [ "$NO_CACHE" = true ]; then
  echo "Docker compose build without cache"
  docker compose build --no-cache || handle_error "Docker Compose build failed"
else
  echo "Docker compose build with cache"
  docker compose build || handle_error "Docker Compose build failed"
fi
docker compose up -d || handle_error "Docker Compose up failed"

echo "Starting Jupyter Lab..."
jupyter lab --ip=0.0.0.0 --port="$JUPYTER_PORT" &

wait