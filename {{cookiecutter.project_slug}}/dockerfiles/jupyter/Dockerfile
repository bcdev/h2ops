FROM quay.io/jupyter/base-notebook:python-3.12.8
USER root
RUN apt-get update
COPY ../../requirements.txt .
RUN pip install -r requirements.txt