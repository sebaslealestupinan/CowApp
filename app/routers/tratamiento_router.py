from fastapi import APIRouter, HTTPException, status
from typing import List

from app.db import SessionDep
from app.schemas.tratamiento_schemas import CreateTratamiento, ReadTratamiento, UpdateTratamiento
from app.crud.tratamiento_crud import (
    create_tratamiento,
    get_tratamiento,
    get_tratamientos_by_animal,
    delete_tratamiento,
    update_tratamiento
)

router = APIRouter()

@router.get("/animal/{animal_id}", response_model=List[ReadTratamiento])
def read_tratamientos_by_animal_endpoint(animal_id: int, session: SessionDep):
    return get_tratamientos_by_animal(animal_id, session)

@router.put("/{tratamiento_id}", response_model=ReadTratamiento)
def update_tratamiento_endpoint(tratamiento_id: int, tratamiento_update: UpdateTratamiento, session: SessionDep):
    tratamiento = update_tratamiento(tratamiento_id, tratamiento_update, session)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return tratamiento

@router.post("/", response_model=ReadTratamiento, status_code=status.HTTP_201_CREATED)
def create_tratamiento_endpoint(tratamiento: CreateTratamiento, session: SessionDep):
    # Verify veterinarian exists and has Veterinario role
    from app.crud.user_crud import get_user
    vet = get_user(tratamiento.veterinario_id, session)
    if not vet:
        raise HTTPException(status_code=404, detail="Veterinario no encontrado")
    if vet.role.value != "Veterinario":
        raise HTTPException(status_code=403, detail="Solo usuarios con rol Veterinario pueden crear tratamientos")
    return create_tratamiento(tratamiento, session)

@router.delete("/{tratamiento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tratamiento_endpoint(tratamiento_id: int, session: SessionDep):
    success = delete_tratamiento(tratamiento_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return None