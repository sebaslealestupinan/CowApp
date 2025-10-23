from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select

from app_c import models, schemas, services
from app_c.database import get_session

router = APIRouter(prefix="/animals", tags=["animals"])

@router.post("/", response_model=schemas.AnimalRead)
def create_animal(animal_in: schemas.AnimalCreate, session: Session = Depends(get_session)):
    if not animal_in.owner_id:
        raise HTTPException(status_code=400, detail="owner_id es requerido en esta versión sin autenticación")
    return services.create_animal(session, animal_in)

@router.get("/{animal_id}", response_model=schemas.AnimalRead)
def read_animal(animal_id: int, session: Session = Depends(get_session)):
    return services.get_animal(session, animal_id)

@router.get("/", response_model=List[schemas.AnimalRead])
def list_animals(owner_id: int = None, session: Session = Depends(get_session)):
    if owner_id:
        return services.list_animals_by_owner(session, owner_id)
    return session.exec(select(models.Animal)).all()

@router.put("/{animal_id}", response_model=schemas.AnimalRead)
def update_animal(animal_id: int, animal_in: schemas.AnimalUpdate, session: Session = Depends(get_session)):
    return services.update_animal(session, animal_id, animal_in)

@router.delete("/{animal_id}")
def delete_animal(animal_id: int, session: Session = Depends(get_session)):
    return services.delete_animal(session, animal_id)

