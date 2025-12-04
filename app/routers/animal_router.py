from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from typing import List
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlmodel import select

from app.db import SessionDep
from app.schemas.animal_schemas import CreateAnimal, ReadAnimal, UpdateAnimal
from app.models.animal import Animal, Usuario
from app.crud.animal_crud import (
    create_animal,
    get_animal,
    get_animals_by_owner,
    update_animal,
    delete_animal
)
from app.crud.user_crud import get_user

router = APIRouter(prefix="/animales", tags=["Animales"])
templates = Jinja2Templates(directory="app/templates")

@router.post("/", response_model=ReadAnimal, status_code=status.HTTP_201_CREATED)
def create_animal_endpoint(animal: CreateAnimal, session: SessionDep):
    owner = get_user(animal.propietario_id, session)
    ganadero = session.exec(select(Usuario).where(Usuario.id == animal.propietario_id)).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    if ganadero.role != "Ganadero":
        raise HTTPException(status_code=403, detail="Solo usuarios con rol Ganadero pueden crear animales")
    return create_animal(animal, session)

@router.get("/", response_model=List[ReadAnimal])
def read_animals_endpoint(session: SessionDep):
    # For now return all, later filter by user
    return session.exec(select(Animal)).all()

# IMPORTANTE: Las rutas estáticas deben definirse ANTES de las rutas dinámicas
@router.get("/nuevo", response_class=HTMLResponse)
async def nuevo_animal(request: Request, user_id: int, session: SessionDep):
    user = session.get(Usuario, user_id)
    return templates.TemplateResponse("animales/nuevo.html", {"request": request, "user": user})

@router.get("/editar/{animal_id}", response_class=HTMLResponse)
async def editar_animal(request: Request, animal_id: int, session: SessionDep):
    animal = get_animal(animal_id, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    user = session.get(Usuario, animal.propietario_id)
    return templates.TemplateResponse("animales/editar.html", {"request": request, "animal": animal, "user": user})

@router.get("/ganadero/{ganadero_id}", response_model=List[ReadAnimal])
def read_animales_by_ganadero_endpoint(ganadero_id: int, session: SessionDep):
    return get_animals_by_owner(ganadero_id, session)

# Las rutas con parámetros dinámicos van DESPUÉS de las rutas estáticas
@router.get("/{animal_id}", response_model=ReadAnimal)
def read_animal_endpoint(animal_id: int, session: SessionDep):
    animal = get_animal(animal_id, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return animal

@router.put("/{animal_id}", response_model=ReadAnimal)
def update_animal_endpoint(animal_id: int, animal_update: UpdateAnimal, session: SessionDep):
    animal = update_animal(animal_id, animal_update, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return animal

@router.delete("/delete/{animal_id}/{ganadero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal_endpoint(animal_id: int, ganadero_id: int, session: SessionDep):
    success = delete_animal(animal_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    
    # Retornamos None con status 204 para compatibilidad con AJAX
    return None

