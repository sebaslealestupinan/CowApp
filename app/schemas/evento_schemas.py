from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class CreateEvento(SQLModel):
    tratamiento_id: int = Field(description="ID del tratamiento asociado")
    fecha: datetime = Field(default_factory=datetime.now, description="Fecha del evento")
    estado: str = Field(description="Estado del evento")
    tipo: str = Field(description="Tipo de evento")
    observaciones: str = Field(description="Observaciones del evento")
    responsable: str = Field(description="Responsable del evento")
    imagen: Optional[str] = Field(default=None, description="URL de la imagen del evento")

class UpdateEvento(SQLModel):
    tratamiento_id: Optional[int] = None
    fecha: Optional[datetime] = None
    estado: Optional[str] = None
    tipo: Optional[str] = None
    observaciones: Optional[str] = None
    responsable: Optional[str] = None

class ReadEvento(SQLModel):
    id: int
    tratamiento_id: int
    fecha: datetime
    estado: str
    imagen: Optional[str] = None
    tipo: str
    observaciones: str
    responsable: str
