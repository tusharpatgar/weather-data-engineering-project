FROM apache/airflow:2.8.1

USER root
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean

USER airflow
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/home/airflow/.local/bin:${PATH}"

COPY pyproject.toml uv.lock /opt/airflow/
WORKDIR /opt/airflow

RUN uv sync --frozen

