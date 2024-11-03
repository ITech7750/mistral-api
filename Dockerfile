# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем зависимости системы
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Обновляем pip, setuptools и wheel для совместимости
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Устанавливаем зависимости Python и используем torch с CUDA, если предполагается работа с GPU
# (Замените torch на torch+cuXXX для GPU, например torch==2.0.1+cu117 для CUDA 11.7)
RUN pip install --no-cache-dir \
    torch transformers flask python-dotenv

# Создаем директорию для приложения и устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=app.py

# Задаем переменную окружения для токена Hugging Face
ARG HF_TOKEN
ENV HUGGINGFACE_TOKEN=$HF_TOKEN

# Устанавливаем переменную окружения для CUDA, чтобы уменьшить использование памяти (если используется GPU)
ENV TORCH_CUDNN_V8_API_ENABLED=1
ENV TORCH_CUDNN_V7_API_ENABLED=0

# Запускаем приложение
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
