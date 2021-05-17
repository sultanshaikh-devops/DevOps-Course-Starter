#FROM buildpack-deps:buster
FROM python:3.9-slim-buster AS base

#Set envrioment variables 
ENV POETRY_HOME="/opt/poetry"
ENV PATH="/usr/local/python3/bin:$POETRY_HOME/bin:$PATH"

#Update the system and install additional package
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

#Set working directory
WORKDIR /app

#copy poetry *.toml files
COPY poetry.lock /app
COPY poetry.toml /app
COPY pyproject.toml /app

#Production Stage
FROM base as production
RUN poetry install --no-root --no-dev
COPY . /app
ENTRYPOINT ["./entrypoint.sh"]
EXPOSE 5000

#Development Stage
FROM base as development
RUN poetry install
ENV FLASK_DEBUG=1
ENTRYPOINT ["./entrypointdev.sh"]
EXPOSE 5000