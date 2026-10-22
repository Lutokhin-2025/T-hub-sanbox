FROM python:3.13-slim
WORKDIR /app
# Копирую файл зависимостей
COPY requirements.txt .
# Устанавливаею библиотеки
RUN pip install --no-cache-dir -r requirements.txt
# Копирую код проекта
COPY . .