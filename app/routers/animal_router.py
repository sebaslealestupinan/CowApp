from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.db import SessionDep
from app.schemas.animal_schemas import CreateAnimal, ReadAnimal, UpdateAnimal
from app.crud.animal_crud import (
    create_animal,
    get_animal,
    get_animals_by_owner,
    update_animal,
    delete_animal
)
from app.crud.user_crud import get_user # Added this import for the new endpoint

# Assuming 'router' is defined elsewhere, e.g., router = APIRouter()
router = APIRouter()
@router.post("/", response_model=ReadAnimal, status_code=status.HTTP_201_CREATED)
def create_animal_endpoint(animal: CreateAnimal, session: SessionDep):
    # Verify owner exists and has Ganadero role
    owner = get_user(animal.propietario_id, session)
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    if owner.role.value != "Ganadero":
        raise HTTPException(status_code=403, detail="Solo usuarios con rol Ganadero pueden crear animales")
    return create_animal(animal, session)

@router.get("/ganadero/{ganadero_id}", response_model=List[ReadAnimal])
def read_animales_by_ganadero_endpoint(ganadero_id: int, session: SessionDep):
    return get_animals_by_owner(ganadero_id, session)

@router.put("/{animal_id}", response_model=ReadAnimal)
def update_animal_endpoint(animal_id: int, animal_update: UpdateAnimal, session: SessionDep):
    animal = update_animal(animal_id, animal_update, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return animal

@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal_endpoint(animal_id: int, session: SessionDep):
    success = delete_animal(animal_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return None