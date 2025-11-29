from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Mensaje(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contenido: str

    sender_id: int = Field(foreign_key="usuario.id")
    receiver_id: int = Field(foreign_key="usuario.id")

    sender: "Usuario" = Relationship(back_populates="sent_messages", sa_relationship_kwargs={"foreign_keys": "[Mensaje.sender_id]"})
    receiver: "Usuario" = Relationship(back_populates="received_messages", sa_relationship_kwargs={"foreign_keys": "[Mensaje.receiver_id]"})
