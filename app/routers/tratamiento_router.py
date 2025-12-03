from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlmodel import select
from app.crud.user_crud import get_user
from app.db import SessionDep
from app.models.usuario import Usuario
from app.schemas.tratamiento_schemas import CreateTratamiento, ReadTratamiento, UpdateTratamiento
from app.crud.tratamiento_crud import (
    create_tratamiento,
    get_tratamiento,
    get_tratamientos_by_animal,
    delete_tratamiento,
    update_tratamiento
)
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi import Request
router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])

@router.post("/", response_model=ReadTratamiento, status_code=status.HTTP_201_CREATED)
def create_tratamiento_endpoint(request: Request, session: SessionDep, 
animal_id: int = Form(...),
nombre_tratamiento: str = Form(...),
diagnostico: str = Form(...),
medicamento: str = Form(None),
dosis: float = Form(None),
fecha_inicio: str = Form(...),
fecha_fin: str = Form(...),
estado: str = Form(...),
veterinario_id: int = Form(...)):

    tratamiento = CreateTratamiento(
        animal_id=animal_id,
        nombre_tratamiento=nombre_tratamiento,
        diagnostico=diagnostico,
        medicamento=medicamento,
        dosis=dosis,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado=estado,
        veterinario_id=veterinario_id
    )

    create_tratamiento(tratamiento, session)

    return RedirectResponse(url=f"/veterinario/{veterinario_id}", status_code=303)

@router.get("/animal/{animal_id}", response_model=List[ReadTratamiento])
def read_tratamientos_by_animal_endpoint(animal_id: int, session: SessionDep):
    return get_tratamientos_by_animal(animal_id, session)

@router.get("/{tratamiento_id}", response_model=ReadTratamiento)
def read_tratamiento_endpoint(tratamiento_id: int, session: SessionDep):
    tratamiento = get_tratamiento(tratamiento_id, session)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return tratamiento

@router.put("/{tratamiento_id}", response_model=ReadTratamiento)
def update_tratamiento_endpoint(tratamiento_id: int, tratamiento_update: UpdateTratamiento, session: SessionDep):
    tratamiento = update_tratamiento(tratamiento_id, tratamiento_update, session)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return tratamiento

@router.delete("/{tratamiento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tratamiento_endpoint(tratamiento_id: int, session: SessionDep):
    success = delete_tratamiento(tratamiento_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return None