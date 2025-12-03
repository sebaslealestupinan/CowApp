
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: Optional[str]
    email: str = Field(unique=True, index=True)
    password: str
    status: bool
    role: str = Field(description="tipo de usuario", default="Ganadero")
    imag: Optional[str] = Field(default=None, description="User image url")
    number_phone: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    animales: Optional[List["Animal"]] = Relationship(back_populates="propietario")
    reportes: Optional[List["Tratamiento"]] = Relationship(back_populates="veterinario")

    sent_messages: Optional[List["Mensaje"]] = Relationship(back_populates="sender", sa_relationship_kwargs={"foreign_keys": "[Mensaje.sender_id]"})
    received_messages: Optional[List["Mensaje"]] = Relationship(back_populates="receiver", sa_relationship_kwargs={"foreign_keys": "[Mensaje.receiver_id]"})

