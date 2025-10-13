FROM python:3.13-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false --local
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app/

RUN pip install --upgrade pip
RUN pip install gunicorn

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
