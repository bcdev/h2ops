FROM apache/airflow:2.10.4-python3.12

USER root
WORKDIR /opt/airflow

RUN echo "deb http://deb.debian.org/debian testing main" >> /etc/apt/sources.list

# Install newer libstdc++6
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    bzip2 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C /opt/

ENV PATH="/opt/bin:$PATH"
RUN micromamba --version

USER airflow
COPY ../../environment.yml .

RUN micromamba env create -f environment.yml
RUN micromamba env list

RUN micromamba shell init -s bash
