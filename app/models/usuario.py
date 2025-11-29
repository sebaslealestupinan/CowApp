
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Role(Enum):
    Veterinario = "Veterinario"
    Ganadero= "Ganadero"

class Telefono(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    numero: str

    user_id: int = Field(foreign_key="usuario.id")
    user: "Usuario" = Relationship(back_populates="telefonos")

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    email: str = Field(unique=True, index=True)
    password: str
    status: bool
    role: Role = Field(description="tipo de usuario", default=Role.Ganadero)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    telefonos: Optional[List[Telefono]] = Relationship(back_populates="user")
    animales: Optional[List["Animal"]] = Relationship(back_populates="propietario")
    reportes: Optional[List["Tratamiento"]] = Relationship(back_populates="veterinario")

    sent_messages: Optional[List["Mensaje"]] = Relationship(back_populates="sender", sa_relationship_kwargs={"foreign_keys": "[Mensaje.sender_id]"})
    received_messages: Optional[List["Mensaje"]] = Relationship(back_populates="receiver", sa_relationship_kwargs={"foreign_keys": "[Mensaje.receiver_id]"})

