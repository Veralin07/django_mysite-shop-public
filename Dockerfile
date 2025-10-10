FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=0

COPY Pipfile Pipfile.lock /app/

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile --system

COPY . /app/

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]

