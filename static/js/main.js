// static/js/main.js

document.addEventListener("DOMContentLoaded", function() {
    const generateButton = document.getElementById("generateButton");
    const inputText = document.getElementById("inputText");
    const responseText = document.getElementById("responseText");
    const responseContainer = document.getElementById("response");
    const loadingMessage = document.getElementById("loadingMessage");
    const languageSelect = document.getElementById("languageSelect");

    generateButton.addEventListener("click", function() {
        const text = inputText.value.trim();
        const selectedLanguage = languageSelect.value;  // Получение выбранного языка

        // Проверка на пустой или слишком длинный текст
        if (text.length === 0) {
            responseText.textContent = "Введите текст.";
            responseContainer.style.display = "block";
            return;
        }

        if (text.length > 500) {
            responseText.textContent = "Текст слишком длинный. Максимум 500 символов.";
            responseContainer.style.display = "block";
            return;
        }

        responseContainer.style.display = "none";
        loadingMessage.style.display = "block";

        // Отправка запроса на генерацию
        fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => {
            loadingMessage.style.display = "none";
            if (!response.ok) throw new Error("Ошибка: " + response.statusText);
            return response.json();
        })
        .then(data => {
            if (data.error) {
                responseText.textContent = "Ошибка: " + data.error;
            } else {
                // Применение выбранного языка для подсветки
                responseText.className = `language-${selectedLanguage}`;
                responseText.textContent = data.response;
                Prism.highlightElement(responseText); // Вызов подсветки синтаксиса
            }
            responseContainer.style.display = "block";
        })
        .catch(error => {
            responseText.textContent = error.message || "Неизвестная ошибка";
            responseContainer.style.display = "block";
            loadingMessage.style.display = "none";
        });
    });
});
