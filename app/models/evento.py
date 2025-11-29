from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from  datetime import datetime

from app.models.tratamiento import Tratamiento


class Evento(SQLModel, table= True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tratamiento_id: Optional[int] = Field(default=None, foreign_key="tratamiento.id", index=True)
    tratamiento: Optional["Tratamiento"] = Relationship(back_populates="eventos")

    fecha: datetime = Field(default_factory=datetime.now)
    estado: str

    tipo: str
    observaciones: str
    responsable: str