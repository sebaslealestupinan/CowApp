const chatConfig = window.CHAT_CONFIG;
const senderId = chatConfig.senderId;
const receiverId = chatConfig.receiverId;

const messagesDiv = document.getElementById("message-list");
const input = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");

let ws = null;

function connectWS() {
    ws = new WebSocket(chatConfig.wsUrl);

    ws.onopen = () => {
        console.log("WS conectado");
        loadHistory();
    };

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);

        // Verificar si el mensaje pertenece a esta conversación
        const esConversacionActual =
            (msg.sender_id === senderId && msg.receiver_id === receiverId) ||
            (msg.sender_id === receiverId && msg.receiver_id === senderId);

        if (esConversacionActual) {
            appendMessage(msg);
        }
    };

    ws.onclose = () => {
        console.warn("WS desconectado. Reintentando...");
        setTimeout(connectWS, 2000);
    };
}

connectWS();

async function loadHistory() {
    try {
        const response = await fetch(`/chat/history/${senderId}/${receiverId}`);
        const messages = await response.json();

        // Limpiar mensajes anteriores por si acaso
        messagesDiv.innerHTML = '';

        messages.forEach(appendMessage);
    } catch (error) {
        console.error("Error cargando historial:", error);
    }
}

function appendMessage(msg) {
    const div = document.createElement("div");

    const enviado = msg.sender_id === senderId;
    div.className = `message-bubble ${enviado ? "message-sent" : "message-received"}`;

    const date = new Date(msg.timestamp || Date.now());
    const time = date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    // Icono de doble check para mensajes enviados (simulado por ahora)
    const checkIcon = enviado ? `
        <span class="message-check" style="color: #53bdeb; margin-left: 3px;">
            <svg viewBox="0 0 16 15" width="16" height="15" class=""><path fill="currentColor" d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.879a.32.32 0 0 1-.484.033l-.358-.325a.319.319 0 0 0-.484.032l-.378.483a.418.418 0 0 0 .036.541l1.32 1.266c.143.14.361.125.484-.033l6.272-7.655a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.879a.32.32 0 0 1-.484.033L1.891 7.769a.366.366 0 0 0-.515.006l-.423.433a.364.364 0 0 0 .006.514l3.258 3.185c.143.14.361.125.484-.033l6.272-7.655a.365.365 0 0 0-.063-.51z"></path></svg>
        </span>
    ` : '';

    div.innerHTML = `
        <div>${msg.content || msg.contenido}</div>
        <div class="message-time">
            ${time}
            ${checkIcon}
        </div>
    `;

    messagesDiv.appendChild(div);
    scrollToBottom();
}

function scrollToBottom() {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// ------- Enviar mensaje -------
function sendMessage() {
    const content = input.value.trim();
    if (!content) return;

    ws.send(JSON.stringify({
        receiver_id: receiverId,
        content: content
    }));

    input.value = "";
    input.style.height = 'auto'; // Reset height
}

sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-resize textarea
input.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if (this.value === '') {
        this.style.height = '40px';
    }
});