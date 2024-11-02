# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir torch transformers flask dotenv

# Создаем директорию для приложения
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Задаем переменную окружения для Flask
ENV FLASK_APP=app.py

# Устанавливаем токен Hugging Face
ARG HF_TOKEN
ENV HUGGINGFACE_TOKEN=$HF_TOKEN

# Запускаем приложение
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
