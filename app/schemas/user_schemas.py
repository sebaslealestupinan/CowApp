from sqlmodel import SQLModel, Field
from typing import List, Optional
from pydantic import EmailStr
from app.models.usuario import Role
from fastapi import Form

class CreateUser(SQLModel):

    name: str = Field( min_length=2,
        description="Nombre completo del veterinario, minimo dos letras."
    )
    email: EmailStr = Field(
        description="Dirección de correo electrónico única y válida."
    )
    role: Role = Field(description="Solo se tienen dos opciones: ser ganadero o veterinario",
                     default = Role.Ganadero)
    password: str = Field(min_length=5)

    status: bool = True

    telefonos: List[str] = Field(
        default=[],
        description="Lista de números de teléfono asociados al veterinario."
    )



class UpdateUser(SQLModel):
    name: Optional[str] = Field(
        min_length=2,
        default=None,
        description="Nombre completo del veterinario."
    )

    email: Optional[EmailStr] = Field(
        default=None,
        description="Dirección de correo electrónico única y válida."
    )

    password: Optional[str] = Field(

        default=None,
        description="Nueva contraseña (si se desea cambiar)."
    )

    telefonos: Optional[List[str]] = Field(
        gt= 10, 
        le=11,
        default=None,
        description="Lista opcional de números de teléfono nuevos."
    )

class ReadUser(SQLModel):

    name: str
    email: str

    class TelefonoRead(SQLModel):
        id: int
        numero: str

    telefonos: List[TelefonoRead]

    class Config:
        from_attributes = True