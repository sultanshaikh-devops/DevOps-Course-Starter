FROM python:3.9-slim-buster AS base

#Set envrioment variables 
ENV POETRY_HOME="/opt/poetry"
ENV PATH="/usr/local/python3/bin:$POETRY_HOME/bin:$PATH"

#Update the system and install additional package
RUN apt-get update && apt-get install -y curl wget
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

#Set working directory
WORKDIR /app

#copy poetry *.toml files
COPY poetry.lock /app
COPY poetry.toml /app
COPY pyproject.toml /app
RUN poetry config virtualenvs.create false

#Test Stage
FROM base as test
RUN apt-get install -y firefox-esr
RUN poetry install
ENV FLASK_DEBUG=0
ENV GECKODRIVER_VERSION 0.29.1
ENV MOZ_HEADLESS=1
RUN wget --no-verbose -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz  \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf geckodriver.tar.gz \
  && rm geckodriver.tar.gz \
  && chmod 755 /opt/geckodriver \
  && ln -fs /opt/geckodriver /usr/bin/geckodriver

EXPOSE 5000
ENTRYPOINT poetry run watchmedo shell-command -c='poetry run pytest' -p='*.py;*.html;*.txt' -D -R -w --debug-force-polling '/app'