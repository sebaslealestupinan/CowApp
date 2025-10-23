from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str = Field(index=True, nullable=False, unique=True)
    full_name: Optional[str] = None
    password: str
    role: str = Field(default="ganadero")

    animals: List["Animal"] = Relationship(back_populates="owner")
    sent_messages: List["Message"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "Message.sender_id"}
    )
    received_messages: List["Message"] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs={"foreign_keys": "Message.receiver_id"}
    )
class DeletedUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_user_id: int = Field(nullable=False)
    phone_number: str
    full_name: Optional[str] = None
    password: str
    role: str
    deleted_at: datetime = Field(default_factory=datetime.utcnow)

class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    breed: Optional[str] = None
    age_months: Optional[int] = None
    weight_kg: Optional[float] = None
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional[User] = Relationship(back_populates="animals")
    health_records: List["HealthRecord"] = Relationship(back_populates="animal")

class HealthRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    vet_id: Optional[int] = Field(default=None, foreign_key="user.id")
    date: datetime = Field(default_factory=datetime.utcnow)
    reason: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    vaccinations: Optional[str] = None
    notes: Optional[str] = None

    animal: Optional[Animal] = Relationship(back_populates="health_records")
    veterinarian: Optional[User] = Relationship()

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="user.id")
    receiver_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    matter: Optional[str] = None
    body: str
    read: bool = Field(default=False)

    sender: Optional[User] = Relationship(
        back_populates="sent_messages",
        sa_relationship_kwargs={"foreign_keys": "Message.sender_id"}
    )
    receiver: Optional[User] = Relationship(
        back_populates="received_messages",
        sa_relationship_kwargs={"foreign_keys": "Message.receiver_id"}
    )