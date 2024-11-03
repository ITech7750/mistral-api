from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Инициализация модели и токенизатора
try:
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
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

        inputs = tokenizer.encode(input_text, return_tensors="pt")
        attention_mask = torch.ones_like(inputs)

        with torch.no_grad():
            outputs = model.generate(
                inputs,
                attention_mask=attention_mask,
                max_length=50,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                pad_token_id=tokenizer.eos_token_id
            )
        
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"response": generated_text})

    except Exception as e:
        return jsonify({"error": f"Ошибка: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
