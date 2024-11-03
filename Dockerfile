FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

COPY . /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

ARG HF_TOKEN
ENV HUGGINGFACE_TOKEN=$HF_TOKEN

ENV TORCH_CUDNN_V8_API_ENABLED=1
ENV TORCH_CUDNN_V7_API_ENABLED=0

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
