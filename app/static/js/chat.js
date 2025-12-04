// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {

    const chatConfig = window.CHAT_CONFIG;

    // Validar configuración
    if (!chatConfig) {
        console.error("Error: CHAT_CONFIG no está definido");
        return;
    }

    console.log("Chat Config:", chatConfig);

    const senderId = chatConfig.senderId;
    const receiverId = chatConfig.receiverId;

    const messagesDiv = document.getElementById("message-list");
    const input = document.getElementById("message-input");
    const sendBtn = document.getElementById("send-btn");

    let ws = null;

    function connectWS() {
        console.log("Intentando conectar WebSocket a:", chatConfig.wsUrl);

        try {
            ws = new WebSocket(chatConfig.wsUrl);
        } catch (error) {
            console.error("Error creando WebSocket:", error);
            return;
        }

        ws.onopen = () => {
            console.log("✅ WebSocket conectado!");
            loadHistory();
        };

        ws.onmessage = (event) => {
            console.log("Mensaje recibido:", event.data);
            const msg = JSON.parse(event.data);

            // Si hay error, mostrarlo
            if (msg.error) {
                console.error("Error del servidor:", msg.error);
                return;
            }

            // Verificar si el mensaje pertenece a esta conversación
            const esConversacionActual =
                (msg.sender_id === senderId && msg.receiver_id === receiverId) ||
                (msg.sender_id === receiverId && msg.receiver_id === senderId);

            if (esConversacionActual) {
                appendMessage(msg);
            }
        };

        ws.onerror = (error) => {
            console.error("❌ Error en WebSocket:", error);
        };

        ws.onclose = (event) => {
            console.warn("WebSocket cerrado. Código:", event.code, "Razón:", event.reason);
            setTimeout(connectWS, 3000);
        };
    }

    async function loadHistory() {
        try {
            console.log(`Cargando historial: /chat/history/${senderId}/${receiverId}`);
            const response = await fetch(`/chat/history/${senderId}/${receiverId}`);
            const messages = await response.json();
            console.log("Historial cargado:", messages.length, "mensajes");

            messagesDiv.innerHTML = '';
            messages.forEach(appendMessage);
            scrollToBottom();
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

        const checkIcon = enviado ? `
            <span class="message-check">
                <svg viewBox="0 0 16 15" width="16" height="15"><path fill="currentColor" d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.879a.32.32 0 0 1-.484.033l-.358-.325a.319.319 0 0 0-.484.032l-.378.483a.418.418 0 0 0 .036.541l1.32 1.266c.143.14.361.125.484-.033l6.272-7.655a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.879a.32.32 0 0 1-.484.033L1.891 7.769a.366.366 0 0 0-.515.006l-.423.433a.364.364 0 0 0 .006.514l3.258 3.185c.143.14.361.125.484-.033l6.272-7.655a.365.365 0 0 0-.063-.51z"></path></svg>
            </span>
        ` : '';

        div.innerHTML = `
            <div class="message-text">${msg.content || msg.contenido}</div>
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

    function sendMessage() {
        const content = input.value.trim();
        if (!content) return;

        if (!ws || ws.readyState !== WebSocket.OPEN) {
            console.error("WebSocket no está conectado");
            alert("No hay conexión. Reintentando...");
            connectWS();
            return;
        }

        console.log("Enviando mensaje:", content);
        ws.send(JSON.stringify({
            receiver_id: receiverId,
            content: content
        }));

        input.value = "";
        input.style.height = 'auto';
    }

    // Event listeners
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
        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
    });

    // Iniciar conexión
    connectWS();
});