from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from app.models.usuario import Usuario
from app.utils.kind_animal import Kind


class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    imagen: Optional[str] = None
    tag_id: str = Field(index=True)
    nombre: Optional[str] = None
    especie: Kind = Field(description="Kind of the animal", default=Kind.Bovino)
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None

    propietario_id: int = Field(foreign_key="usuario.id")
    propietario: Optional["Usuario"] = Relationship(back_populates="animales")


    tratamientos: List["Tratamiento"] = Relationship(back_populates="animal")

    activo: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)