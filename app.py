from flask import Flask, render_template, jsonify, request
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)

# Загрузка модели и токенизатора
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Маршрут для главной страницы
@app.route("/")
def index():
    return render_template("index.html")

# Маршрут для общения с моделью
@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.get_json()
    input_text = data.get("text", "")
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": generated_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
