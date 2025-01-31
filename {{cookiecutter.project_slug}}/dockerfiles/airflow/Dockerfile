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

#SHELL ["/bin/bash", "-c"]
RUN micromamba shell init -s bash
#RUN echo "source activate mlops" >> ~/.bashrc
#
#ENV CONDA_DEFAULT_ENV=mlops
#
#RUN micromamba env list
#
#RUN micromamba list
#COPY ../../entrypoint.sh entrypoint.sh
#RUN echo '#!/bin/bash' > entrypoint.sh && \
#    echo 'eval "$(micromamba shell hook --shell=bash)"' >> entrypoint.sh && \
#    echo 'micromamba activate mlops' >> entrypoint.sh && \
#    echo 'exec "$@"' >> entrypoint.sh
#RUN chmod +x entrypoint.sh
#ENTRYPOINT ["./entrypoint.sh"]
