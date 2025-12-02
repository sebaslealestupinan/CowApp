// Messaging Component JavaScript
class MessagingApp {
    constructor(userId) {
        this.userId = userId;
        this.currentChatUserId = null;
        this.ws = null;
        this.conversations = [];
        this.messages = {};
        
        this.init();
    }
    
    init() {
        this.connectWebSocket();
        this.loadConversations();
        this.setupEventListeners();
    }
    
    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/chat/ws/${this.userId}`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('WebSocket conectado');
        };
        
        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleIncomingMessage(message);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket desconectado. Reconectando...');
            setTimeout(() => this.connectWebSocket(), 3000);
        };
    }
    
    async loadConversations() {
        try {
            const response = await fetch(`/chat/conversations/${this.userId}`);
            this.conversations = await response.json();
            this.renderConversations();
        } catch (error) {
            console.error('Error cargando conversaciones:', error);
        }
    }
    
    renderConversations() {
        const container = document.getElementById('conversations-list');
        
        if (this.conversations.length === 0) {
            container.innerHTML = `
                <div class="empty-state" style="padding: 40px 20px; text-align: center;">
                    <i class="fas fa-comments" style="font-size: 2rem; color: #dbdbdb; margin-bottom: 12px;"></i>
                    <p style="color: #b5b5b5;">No hay conversaciones</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = this.conversations.map(conv => `
            <div class="conversation-item ${conv.user_id === this.currentChatUserId ? 'active' : ''}" 
                 data-user-id="${conv.user_id}"
                 onclick="messagingApp.openChat(${conv.user_id})">
                <div class="conversation-header">
                    <span class="conversation-name">${conv.user_name}</span>
                    ${conv.unread_count > 0 ? `<span class="unread-badge">${conv.unread_count}</span>` : ''}
                </div>
                <span class="conversation-role">${conv.user_role}</span>
                ${conv.last_message ? `
                    <div class="conversation-last-message">${conv.last_message}</div>
                    <div class="conversation-time">${this.formatTime(conv.last_message_time)}</div>
                ` : ''}
            </div>
        `).join('');
    }
    
    async openChat(userId) {
        this.currentChatUserId = userId;
        
        // Marcar como leído
        await this.markAsRead(userId);
        
        // Cargar historial
        await this.loadChatHistory(userId);
        
        // Actualizar UI
        this.renderConversations();
        this.renderChatArea();
    }
    
    async loadChatHistory(userId) {
        try {
            const response = await fetch(`/chat/history/${this.userId}/${userId}`);
            const messages = await response.json();
            this.messages[userId] = messages;
            this.renderMessages();
        } catch (error) {
            console.error('Error cargando historial:', error);
        }
    }
    
    renderChatArea() {
        const chatArea = document.getElementById('chat-area');
        const conversation = this.conversations.find(c => c.user_id === this.currentChatUserId);
        
        if (!conversation) {
            chatArea.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-comment-dots"></i>
                    <p>Selecciona una conversación para comenzar</p>
                </div>
            `;
            return;
        }
        
        chatArea.innerHTML = `
            <div class="chat-header">
                <h3>
                    ${conversation.user_name}
                    <span class="role-badge">${conversation.user_role}</span>
                </h3>
            </div>
            <div class="messages-container" id="messages-container"></div>
            <div class="message-input-area">
                <input type="text" id="message-input" placeholder="Escribe un mensaje..." />
                <button onclick="messagingApp.sendMessage()">
                    <i class="fas fa-paper-plane"></i> Enviar
                </button>
            </div>
        `;
        
        this.renderMessages();
        this.setupMessageInput();
    }
    
    renderMessages() {
        const container = document.getElementById('messages-container');
        if (!container || !this.currentChatUserId) return;
        
        const messages = this.messages[this.currentChatUserId] || [];
        
        container.innerHTML = messages.map(msg => {
            const isSent = msg.sender_id === this.userId;
            return `
                <div class="message-bubble ${isSent ? 'sent' : 'received'}">
                    <div>${msg.contenido}</div>
                    <div class="message-time">${this.formatTime(msg.timestamp)}</div>
                </div>
            `;
        }).join('');
        
        // Scroll al final
        container.scrollTop = container.scrollHeight;
    }
    
    setupMessageInput() {
        const input = document.getElementById('message-input');
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendMessage();
                }
            });
            input.focus();
        }
    }
    
    sendMessage() {
        const input = document.getElementById('message-input');
        const content = input.value.trim();
        
        if (!content || !this.currentChatUserId) return;
        
        const messageData = {
            receiver_id: this.currentChatUserId,
            content: content
        };
        
        this.ws.send(JSON.stringify(messageData));
        input.value = '';
    }
    
    handleIncomingMessage(message) {
        if (message.error) {
            console.error('Error del servidor:', message.error);
            return;
        }
        
        // Determinar el usuario de la conversación
        const otherUserId = message.sender_id === this.userId ? message.receiver_id : message.sender_id;
        
        // Agregar mensaje al historial
        if (!this.messages[otherUserId]) {
            this.messages[otherUserId] = [];
        }
        
        // Evitar duplicados
        if (!this.messages[otherUserId].find(m => m.id === message.id)) {
            this.messages[otherUserId].push({
                id: message.id,
                contenido: message.content,
                sender_id: message.sender_id,
                receiver_id: message.receiver_id,
                timestamp: message.timestamp,
                read: message.read
            });
        }
        
        // Si es el chat actual, renderizar
        if (otherUserId === this.currentChatUserId) {
            this.renderMessages();
        }
        
        // Recargar conversaciones para actualizar contador
        this.loadConversations();
    }
    
    async markAsRead(userId) {
        try {
            await fetch(`/chat/mark-read/${this.userId}/${userId}`, {
                method: 'POST'
            });
        } catch (error) {
            console.error('Error marcando como leído:', error);
        }
    }
    
    formatTime(timestamp) {
        if (!timestamp) return '';
        
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return 'Ahora';
        if (diffMins < 60) return `Hace ${diffMins}m`;
        
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) return `Hace ${diffHours}h`;
        
        const diffDays = Math.floor(diffHours / 24);
        if (diffDays < 7) return `Hace ${diffDays}d`;
        
        return date.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
    }
    
    setupEventListeners() {
        // Recargar conversaciones cada 30 segundos
        setInterval(() => {
            if (document.visibilityState === 'visible') {
                this.loadConversations();
            }
        }, 30000);
    }
}

// Variable global para acceder desde el HTML
let messagingApp;
