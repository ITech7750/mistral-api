from flask import Flask, request, jsonify
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
import gc

# Загрузите токен из .env или переменной окружения
load_dotenv()
hf_token = os.getenv("HUGGINGFACE_TOKEN", "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")

app = Flask(__name__)

# Имя модели
model_name = "mistralai/Mistral-7B-v0.1"

# Проверка доступности CUDA
device = "cuda" if torch.cuda.is_available() else "cpu"

# Загрузка токенизатора
tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)

# Загрузка модели с оптимизацией под float16, если доступен CUDA
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto" if device == "cuda" else None,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    token=hf_token
)

# Перемещение модели на нужное устройство
model.to(device)

# API для генерации текста
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    max_length = data.get("max_length", 50)  # Ограничим длину вывода для экономии памяти

    # Подготовка ввода для модели
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Очистка кэша GPU и сборка мусора для освобождения памяти
    if device == "cuda":
        torch.cuda.empty_cache()
        gc.collect()

    # Генерация текста с моделью
    with torch.no_grad():  # Отключаем автодифференцирование для экономии памяти
        outputs = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

    # Декодирование и возврат результата
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
