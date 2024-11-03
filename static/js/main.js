async function generateText() {
    const inputText = document.getElementById("user-input").value;
    const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText })
    });
    const data = await response.json();
    document.getElementById("response").innerText = data.response;
}