# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем и очищаем зависимости системы
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Обновляем pip, setuptools и wheel для совместимости
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Устанавливаем зависимости Python, включая правильный пакет для dotenv
RUN pip install --no-cache-dir torch transformers flask python-dotenv

# Создаем директорию для приложения и устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Задаем переменную окружения для Flask
ENV FLASK_APP=app.py

# Устанавливаем токен Hugging Face как аргумент сборки
ARG HF_TOKEN
ENV HUGGINGFACE_TOKEN=$HF_TOKEN

# Запускаем приложение
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
