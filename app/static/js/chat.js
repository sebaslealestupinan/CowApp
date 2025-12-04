document.addEventListener('DOMContentLoaded', function() {
    
    const chatConfig = window.CHAT_CONFIG;
    if (!chatConfig) return;
    
    const senderId = chatConfig.senderId;
    const receiverId = chatConfig.receiverId;

    const messagesDiv = document.getElementById("message-list");
    const input = document.getElementById("message-input");
    const sendBtn = document.getElementById("send-btn");
    const attachBtn = document.getElementById("attach-btn");
    const imageInput = document.getElementById("image-input");
    const typingIndicator = document.getElementById("typing-indicator");
    const statusText = document.getElementById("status-text");

    let ws = null;
    let typingTimeout = null;
    let isTyping = false;

    // --- WebSocket ---

    function connectWS() {
        ws = new WebSocket(chatConfig.wsUrl);

        ws.onopen = () => {
            console.log("✅ WebSocket conectado");
            loadHistory();
        };

        ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);

            if (msg.type === "typing") {
                handleTyping(msg.sender_id);
                return;
            }

            if (msg.error) {
                console.error("Error:", msg.error);
                return;
            }

            // Verificar conversación
            const esConversacionActual =
                (msg.sender_id === senderId && msg.receiver_id === receiverId) ||
                (msg.sender_id === receiverId && msg.receiver_id === senderId);

            if (esConversacionActual) {
                appendMessage(msg);
            }
        };

        ws.onclose = () => {
            console.warn("WS desconectado. Reintentando...");
            setTimeout(connectWS, 3000);
        };
    }

    // --- Funciones Core ---

    async function loadHistory() {
        try {
            const response = await fetch(`/chat/history/${senderId}/${receiverId}`);
            const messages = await response.json();
            messagesDiv.innerHTML = '';
            messages.forEach(appendMessage);
            scrollToBottom();
        } catch (error) {
            console.error("Error historial:", error);
        }
    }

    function appendMessage(msg) {
        const div = document.createElement("div");
        const enviado = msg.sender_id === senderId;
        div.className = `message-bubble ${enviado ? "message-sent" : "message-received"}`;

        const date = new Date(msg.timestamp || Date.now());
        const time = date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

        // Detectar si es imagen
        const content = msg.content || msg.contenido;
        let messageContent = `<div class="message-text">${content}</div>`;

        if (isImageUrl(content)) {
            messageContent = `
                <div class="message-image">
                    <img src="${content}" alt="Imagen enviada" onclick="window.open(this.src, '_blank')">
                </div>
            `;
        }

        const checkIcon = enviado ? `
            <span class="message-check">
                <svg viewBox="0 0 16 15" width="16" height="15"><path fill="currentColor" d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.879a.32.32 0 0 1-.484.033l-.358-.325a.319.319 0 0 0-.484.032l-.378.483a.418.418 0 0 0 .036.541l1.32 1.266c.143.14.361.125.484-.033l6.272-7.655a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.879a.32.32 0 0 1-.484.033L1.891 7.769a.366.366 0 0 0-.515.006l-.423.433a.364.364 0 0 0 .006.514l3.258 3.185c.143.14.361.125.484-.033l6.272-7.655a.365.365 0 0 0-.063-.51z"></path></svg>
            </span>
        ` : '';

        div.innerHTML = `
            ${messageContent}
            <div class="message-time">
                ${time}
                ${checkIcon}
            </div>
        `;

        messagesDiv.appendChild(div);
        scrollToBottom();
    }

    function isImageUrl(url) {
        if (!url) return false;
        return (url.match(/\.(jpeg|jpg|gif|png|webp)$/i) != null) || url.includes('cloudinary.com');
    }

    function scrollToBottom() {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    // --- Enviar Mensajes ---

    function sendMessage() {
        const content = input.value.trim();
        if (!content) return;

        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                receiver_id: receiverId,
                content: content,
                type: "text"
            }));
            input.value = "";
            input.style.height = 'auto';
        } else {
            alert("Conexión perdida. Reintentando...");
            connectWS();
        }
    }

    // --- Imágenes ---

    attachBtn.addEventListener('click', () => imageInput.click());

    imageInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        // Mostrar loading o algo visual podría ser bueno aquí
        attachBtn.disabled = true;
        attachBtn.style.opacity = "0.5";

        try {
            const response = await fetch('/chat/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Error subiendo imagen');

            const data = await response.json();
            
            // Enviar URL como mensaje
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    receiver_id: receiverId,
                    content: data.url,
                    type: "text" // Lo tratamos como texto para persistencia simple
                }));
            }

        } catch (error) {
            console.error(error);
            alert("Error al enviar imagen");
        } finally {
            attachBtn.disabled = false;
            attachBtn.style.opacity = "1";
            imageInput.value = ''; // Reset
        }
    });

    // --- Typing Indicator ---

    input.addEventListener('input', () => {
        // Auto resize
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 100) + 'px';

        // Send typing event
        if (!isTyping) {
            isTyping = true;
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    receiver_id: receiverId,
                    type: "typing"
                }));
            }
            // Reset flag after 2s to allow sending again
            setTimeout(() => isTyping = false, 2000);
        }
    });

    function handleTyping(senderId) {
        if (senderId !== receiverId) return; // Solo si es el otro usuario

        statusText.style.display = 'none';
        typingIndicator.style.display = 'block';

        if (typingTimeout) clearTimeout(typingTimeout);

        typingTimeout = setTimeout(() => {
            typingIndicator.style.display = 'none';
            statusText.style.display = 'block';
        }, 3000);
    }

    // --- Event Listeners ---

    sendBtn.addEventListener("click", sendMessage);

    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Iniciar
    connectWS();
});