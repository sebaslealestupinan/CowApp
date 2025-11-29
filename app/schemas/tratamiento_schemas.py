from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class CreateTratamiento(SQLModel):
    fecha_inicio: str = Field(description="Fecha de inicio del tratamiento")
    fecha_fin: str = Field(description="Fecha de fin del tratamiento")
    estado: str = Field(description="Estado del tratamiento (e.g., Activo, Finalizado)")
    nombre_tratamiento: str = Field(description="Nombre del tratamiento")
    diagnostico: str = Field(description="Diagnóstico del animal")
    medicamento: Optional[str] = Field(default=None, description="Medicamento administrado")
    dosis: Optional[float] = Field(default=None, description="Dosis del medicamento")
    veterinario_id: int = Field(description="ID del veterinario responsable")
    animal_id: int = Field(description="ID del animal tratado")

class UpdateTratamiento(SQLModel):
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    estado: Optional[str] = None
    nombre_tratamiento: Optional[str] = None
    diagnostico: Optional[str] = None
    medicamento: Optional[str] = None
    dosis: Optional[float] = None
    veterinario_id: Optional[int] = None
    animal_id: Optional[int] = None

class ReadTratamiento(SQLModel):
    id: int
    fecha_inicio: str
    fecha_fin: str
    estado: str
    nombre_tratamiento: str
    diagnostico: str
    medicamento: Optional[str]
    dosis: Optional[float]
    veterinario_id: int
    animal_id: int
    created_at: datetime
