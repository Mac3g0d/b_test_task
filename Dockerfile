FROM python:3.11

ENV PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1\
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.2
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /src
COPY poetry.lock pyproject.toml alembic.ini /src/
COPY /migrations /src/migrations

RUN poetry install -n
COPY src src

EXPOSE 8000
CMD poetry run alembic upgrade head && poetry run gunicorn -k uvicorn.workers.UvicornWorker -w 8 -b 0.0.0.0:8000 src.app:app
