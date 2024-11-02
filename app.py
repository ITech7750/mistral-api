from flask import Flask, request, jsonify
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv

# Загрузите токен из .env или переменной окружения
load_dotenv()
#hf_token = os.getenv("HUGGINGFACE_TOKEN")
hf_token = "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"

app = Flask(__name__)

# Загрузите модель и токенизатор с использованием токена
model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", load_in_8bit=True, use_auth_token=hf_token)

# API для генерации текста
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    max_length = data.get("max_length", 100)

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"], max_length=max_length, temperature=0.7, top_p=0.9, do_sample=True
        )
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
