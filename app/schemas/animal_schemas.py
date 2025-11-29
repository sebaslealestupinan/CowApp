from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from app.utils.kind_animal import Kind

class CreateAnimal(SQLModel):
    tag_id: str = Field(description="Identificador único del animal (arete, chip, etc.)")
    nombre: Optional[str] = Field(default=None, description="Nombre del animal")
    especie: Kind = Field(default=Kind.Bovino, description="Especie del animal")
    raza: Optional[str] = Field(default=None, description="Raza del animal")
    sexo: Optional[str] = Field(default=None, description="Sexo del animal")
    fecha_nacimiento: Optional[datetime] = Field(default=None, description="Fecha de nacimiento")
    propietario_id: int = Field(description="ID del ganadero propietario")
    activo: bool = Field(default=True, description="Estado del animal")

class UpdateAnimal(SQLModel):
    tag_id: Optional[str] = None
    nombre: Optional[str] = None
    especie: Optional[Kind] = None
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    propietario_id: Optional[int] = None
    activo: Optional[bool] = None

class ReadAnimal(SQLModel):
    id: int
    tag_id: str
    nombre: Optional[str]
    especie: Kind
    raza: Optional[str]
    sexo: Optional[str]
    fecha_nacimiento: Optional[datetime]
    propietario_id: int
    activo: bool
    created_at: datetime
    updated_at: datetime
