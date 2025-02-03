FROM apache/airflow:2.10.4-python3.12

USER root
WORKDIR /opt/airflow

RUN apt-get update && apt-get install -y curl bzip2

RUN curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C /opt/

ENV PATH="/opt/bin:$PATH"
RUN micromamba --version

USER airflow
COPY ../../environment.yml .

RUN micromamba env create -f environment.yml
RUN micromamba env list

RUN micromamba shell init -s bash
