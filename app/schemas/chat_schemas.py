from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class CreateMensaje(SQLModel):
    contenido: str = Field(description="Contenido del mensaje")
    sender_id: int = Field(description="ID del remitente")
    receiver_id: int = Field(description="ID del destinatario")

class ReadMensaje(SQLModel):
    id: int
    contenido: str
    sender_id: int
    receiver_id: int
    timestamp: datetime
    read: bool

class ConversationSummary(SQLModel):
    """Resumen de una conversación para mostrar en la lista de chats"""
    user_id: int
    user_name: str
    user_role: str
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None
    unread_count: int = 0
