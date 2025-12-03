from sqlmodel import SQLModel, Field
from typing import List, Optional
from pydantic import EmailStr
from fastapi import Form

class CreateUser(SQLModel):

    name: str = Field( min_length=2,
        description="Nombre completo del veterinario, minimo dos letras."
    )
    email: EmailStr = Field(
        description="Dirección de correo electrónico única y válida."
    )
    role: str = Field(description="Solo se tienen dos opciones: ser ganadero o veterinario",
                     default = "ganadero")
    password: str = Field(min_length=5)

    status: bool = True

    telefonos: str = Field(
        description="numero de telefono."
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

    telefonos: Optional[str] = Field(
        gt= 10, 
        le=11,
        default=None,
        description="telefono nuevo."
    )

class ReadUser(SQLModel):

    name: str
    email: str
    role: str
    status: bool
    telefonos: str

    class Config:
        from_attributes = True