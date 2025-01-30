FROM quay.io/jupyter/base-notebook:python-3.12.8
USER root

COPY ../../environment.yml .

RUN conda env create -f environment.yml -n mlops
RUN conda env list

SHELL ["/bin/bash", "-c"]

RUN conda init bash

RUN echo "source activate mlops" >> ~/.bashrc

ENV CONDA_DEFAULT_ENV=mlops
ENV PATH="/opt/conda/envs/mlops/bin:$PATH"

RUN conda env list

RUN conda list

