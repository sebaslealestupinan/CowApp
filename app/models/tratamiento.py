from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

"""En esta tabla se guardan los diferentes tratamientos que puede llagar a tener un animal a lo 
largo de su vida productiva"""

class Tratamiento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_inicio: str
    fecha_fin: str

    estado: str = Field(index=True)
    nombre_tratamiento: str
    diagnostico: str

    medicamento: Optional[str] = None
    dosis: Optional[float] = None

    veterinario_id: int = Field(foreign_key="usuario.id")
    veterinario: Optional["Usuario"] = Relationship(back_populates="reportes")

    animal_id: int = Field(foreign_key="animal.id")
    animal: Optional["Animal"] = Relationship(back_populates="tratamientos")

    eventos: List["Evento"] = Relationship(back_populates="tratamiento")

    created_at: datetime = Field(default_factory=datetime.utcnow)