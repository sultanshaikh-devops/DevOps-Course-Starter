FROM buildpack-deps:buster
ENV POETRY_HOME="/opt/poetry"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y curl python3-pip
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN poetry --version
RUN poetry install
EXPOSE 5000
CMD poetry run gunicorn --bind 0.0.0.0:5000 'todo_app.app:create_app()' --daemon --error-logfile gunicorn_daemon.log

