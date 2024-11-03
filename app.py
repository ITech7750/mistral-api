from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
import os

# Установка токена аутентификации Hugging Face
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "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")

# Инициализация модели и токенизатора
try:
    # Используем более мощную модель Code Llama, передавая токен аутентификации
    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/CodeLlama-13b", 
        token=HUGGINGFACE_TOKEN  # Заменили use_auth_token на token
    )
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/CodeLlama-13b", 
        token=HUGGINGFACE_TOKEN  # Заменили use_auth_token на token
    )
    model.to("cuda" if torch.cuda.is_available() else "cpu")
except Exception as e:
    print(f"Ошибка при загрузке модели: {e}")
    model = None


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Server is running"}), 200

@app.route("/generate", methods=["POST"])
def generate_text():
    if model is None:
        return jsonify({"error": "Модель недоступна"}), 500

    try:
        data = request.get_json()
        input_text = data.get("text", "")

        if not input_text:
            return jsonify({"error": "Текст не может быть пустым"}), 400

        if len(input_text) > 500:
            return jsonify({"error": "Слишком длинный текст, ограничение 500 символов"}), 400

        # Подготовка данных для генерации
        inputs = tokenizer.encode(input_text, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
        attention_mask = torch.ones_like(inputs)

        with torch.no_grad():
            outputs = model.generate(
                inputs,
                attention_mask=attention_mask,
                max_length=200,
                num_return_sequences=1,
                temperature=0.2,
                top_k=50,
                top_p=0.95,
                no_repeat_ngram_size=3,
                pad_token_id=tokenizer.eos_token_id
            )
        
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Форматирование кода с сохранением отступов
        formatted_text = format_code(generated_text)
        
        return jsonify({"response": formatted_text})

    except Exception as e:
        return jsonify({"error": f"Ошибка: {e}"}), 500

def format_code(code: str) -> str:
    """Форматирует сгенерированный код для улучшения читабельности и сохранения отступов."""
    lines = code.strip().split("\n")
    formatted_lines = [line.rstrip() for line in lines if line.strip()]

    base_indent = len(re.match(r"^\s*", formatted_lines[0]).group(0))
    formatted_lines = [line[base_indent:] if len(line) >= base_indent else line for line in formatted_lines]

    return "\n".join(formatted_lines)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
