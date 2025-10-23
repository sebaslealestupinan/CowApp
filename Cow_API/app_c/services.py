from sqlmodel import Session, select
from fastapi import HTTPException, status

from app_c import models, schemas
from app_c.models import DeletedUser
import datetime


def create_user(session: Session, user_in: schemas.UserCreate) -> models.User:
    statement = select(models.User).where(models.User.phone_number == user_in.phone_number)
    existing = session.exec(statement).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Número de teléfono ya registrado")

    user = models.User(**user_in.model_dump(exclude_unset=True))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(session: Session, user_id: int):
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

def get_user_for(session: Session, full_name: str):
    statement = select(models.User).where(models.User.full_name == full_name)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    return result

def update_user(session: Session, user_id: int, user_in: schemas.UserUpdate):
    user = get_user(session, user_id)
    for key, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int):
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    deleted_user = DeletedUser(
            original_user_id=user.id,
            phone_number=user.phone_number,
            full_name=user.full_name,
            password=user.password,
            role=user.role,
            deleted_at=datetime.utcnow()
    )

    session.add(deleted_user)
    session.delete(user)
    session.commit()

    return {"ok": True}

def create_animal(session: Session, animal_in: schemas.AnimalCreate):
    if animal_in.owner_id is not None:
        owner = session.get(models.User, animal_in.owner_id)
        if not owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propietario no encontrado")

    animal = models.Animal(**animal_in.model_dump(exclude_unset=True))
    session.add(animal)
    session.commit()
    session.refresh(animal)
    return animal

def get_animal(session: Session, animal_id: int):
    animal = session.get(models.Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado")
    return animal

def list_animals_by_owner(session: Session, owner_id: int):
    return session.exec(select(models.Animal).where(models.Animal.owner_id == owner_id)).all()

def update_animal(session: Session, animal_id: int, animal_in: schemas.AnimalUpdate):
    animal = get_animal(session, animal_id)
    for key, value in animal_in.model_dump(exclude_unset=True).items():
        setattr(animal, key, value)
    session.add(animal)
    session.commit()
    session.refresh(animal)
    return animal

def delete_animal(session: Session, animal_id: int):
    animal = get_animal(session, animal_id)
    session.delete(animal)
    session.commit()
    return {"ok": True}

def create_health_record(session: Session, hr_in: schemas.HealthRecordCreate):
    animal = session.get(models.Animal, hr_in.animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado")

    if hr_in.vet_id:
        vet = session.get(models.User, hr_in.vet_id)
        if not vet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinario no encontrado")

    hr = models.HealthRecord(**hr_in.model_dump(exclude_unset=True))
    session.add(hr)
    session.commit()
    session.refresh(hr)
    return hr

def get_health_record(session: Session, hr_id: int):
    hr = session.get(models.HealthRecord, hr_id)
    if not hr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro sanitario no encontrado")
    return hr

def list_health_records_for_animal(session: Session, animal_id: int):
    return session.exec(
        select(models.HealthRecord)
        .where(models.HealthRecord.animal_id == animal_id)
        .order_by(models.HealthRecord.date.desc())
    ).all()

def update_health_record(session: Session, hr_id: int, hr_in: schemas.HealthRecordUpdate):
    hr = get_health_record(session, hr_id)
    for key, value in hr_in.model_dump(exclude_unset=True).items():
        setattr(hr, key, value)
    session.add(hr)
    session.commit()
    session.refresh(hr)
    return hr

def delete_health_record(session: Session, hr_id: int):
    hr = get_health_record(session, hr_id)
    session.delete(hr)
    session.commit()
    return {"ok": True}

def send_message(session: Session, message_in: schemas.MessageCreate):
    sender = session.get(models.User, message_in.sender_id)
    if not sender:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Remitente no encontrado")

    receiver = session.get(models.User, message_in.receiver_id)
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destinatario no encontrado")

    msg = models.Message(**message_in.model_dump(exclude_unset=True))
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg

def list_messages_for_user(session: Session, user_id: int):
    return session.exec(
        select(models.Message)
        .where(models.Message.receiver_id == user_id)
        .order_by(models.Message.created_at.desc())
    ).all()

def mark_message_read(session: Session, message_id: int, read: bool = True):
    msg = session.get(models.Message, message_id)
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado")
    msg.read = read
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg

def get_message(session: Session, message_id: int):
    msg = session.get(models.Message, message_id)
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado")
    return msg
