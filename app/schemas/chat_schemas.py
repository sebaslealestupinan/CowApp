from sqlmodel import SQLModel, Field
from typing import Optional

class CreateMensaje(SQLModel):
    contenido: str = Field(description="Contenido del mensaje")
    sender_id: int = Field(description="ID del remitente")
    receiver_id: int = Field(description="ID del destinatario")

class ReadMensaje(SQLModel):
    id: int
    contenido: str
    sender_id: int
    receiver_id: int
