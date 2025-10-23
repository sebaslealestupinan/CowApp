from typing import Optional
from datetime import datetime
from pydantic import constr
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    phone_number: constr(min_length=7, max_length=15)
    full_name: Optional[str] = None
    password: constr(min_length=6)
    role: Optional[str] = "ganadero"

class UserRead(SQLModel):
    id: int
    phone_number: str
    full_name: Optional[str] = None
    role: str

class UserUpdate(SQLModel):
    phone_number: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[constr(min_length=1)] = None
    role: Optional[str] = None

class DeleteUser(SQLModel):
    id: int
    phone_number: str
    full_name: Optional[str] = None
    role: Optional[str] = None

class AnimalCreate(SQLModel):
    name: str
    breed: Optional[str] = None
    age_months: Optional[int] = None
    weight_kg: Optional[float] = None
    owner_id: Optional[int] = None

class AnimalRead(SQLModel):
    id: int
    name: str
    breed: Optional[str]
    age_months: Optional[int]
    weight_kg: Optional[float]
    owner_id: Optional[int]
    created_at: datetime

class AnimalUpdate(SQLModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age_months: Optional[int] = None
    weight_kg: Optional[float] = None

class HealthRecordCreate(SQLModel):
    animal_id: int
    vet_id: Optional[int] = None
    date: Optional[datetime] = None
    reason: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    vaccinations: Optional[str] = None
    notes: Optional[str] = None

class HealthRecordRead(SQLModel):
    id: int
    animal_id: int
    vet_id: Optional[int]
    date: datetime
    reason: Optional[str]
    diagnosis: Optional[str]
    treatment: Optional[str]
    vaccinations: Optional[str]
    notes: Optional[str]

class HealthRecordUpdate(SQLModel):
    reason: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    vaccinations: Optional[str] = None
    notes: Optional[str] = None

class MessageCreate(SQLModel):
    sender_id: int
    receiver_id: int
    matter: Optional[str] = None
    body: str

class MessageRead(SQLModel):
    id: int
    sender_id: int
    receiver_id: int
    matter: Optional[str]
    body: str
    created_at: datetime
    read: bool

class MessageUpdate(SQLModel):
    read: Optional[bool] = None
