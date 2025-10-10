FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=0

# Установка зависимостей Python
COPY Pipfile Pipfile.lock /app/
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile --system

# Копируем весь проект
COPY . /app/

# Установка Node.js и npm (если не установлены в образе)
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Переходим в папку с фронтендом и устанавливаем npm-зависимости
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Возвращаемся в корень приложения
WORKDIR /shopapp/templates/shopapp

# Запуск Gunicorn для Django
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]


