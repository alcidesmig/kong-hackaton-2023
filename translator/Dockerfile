FROM python:3.11 as dependencies

# System envs
ENV PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.2 \
  POETRY_HOME="/opt/poetry"

# Project Envs
ENV CACHE=True
ENV SERVER_PORT=25564
ENV LANGUAGE_AUTODETECT=True

# System deps
RUN python3 -m venv $POETRY_HOME
RUN $POETRY_HOME/bin/pip install poetry==${POETRY_VERSION}
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# Copy only requirements to cache them in docker layer
WORKDIR /api
COPY poetry.lock pyproject.toml /api/

# Project initialization
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi

# Creating folders, and files for a project
COPY . /api

ENTRYPOINT ["sh", "-c", "python3 main.py"]
