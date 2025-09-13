let fitbotCategory = "";

async function handleOption(option) {
    const response = await fetch("/fitbot", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: option, category: fitbotCategory })
    });
    const data = await response.json();
    const chat = document.getElementById("fitbot-chat");
    const optionsDiv = document.getElementById("fitbot-options");

    if (option !== "start") chat.innerHTML += `<div class="user-message">${option}</div>`;
    chat.innerHTML += `<div class="bot-message">${data.response}</div>`;

    fitbotCategory = data.category;
    optionsDiv.innerHTML = "";

    if (data.options && data.options.length > 0) {
        data.options.forEach(opt => {
            const btn = document.createElement("button");
            btn.textContent = opt;
            btn.classList.add("option-btn");
            btn.onclick = () => handleOption(opt);
            optionsDiv.appendChild(btn);
        });
    }

    chat.scrollTop = chat.scrollHeight;
}

document.addEventListener("DOMContentLoaded", () => {
    handleOption("start");
});
