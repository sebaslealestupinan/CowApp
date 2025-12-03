from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from sqlmodel import select
from typing import Optional

from app.db import SessionDep
from app.models.tratamiento import Tratamiento
from app.crud.user_crud import get_user

router = APIRouter()

# Setup templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/views/animales", response_class=HTMLResponse, name="view_animales_lista")
async def view_animales_lista(request: Request):
    """Vista de lista de animales"""
    return templates.TemplateResponse("animales/lista.html", {"request": request})

@router.get("/views/animal/{animal_id}", response_class=HTMLResponse, name="view_animal_detalle")
async def view_animal_detalle(request: Request, animal_id: int):
    """Vista de detalle de animal"""
    return templates.TemplateResponse("animales/detalle.html", {"request": request, "animal_id": animal_id})

@router.get("/views/tratamientos", response_class=HTMLResponse, name="view_tratamientos_lista")
async def view_tratamientos_lista(
    request: Request, 
    session: SessionDep,
    animal_id: Optional[int] = None,
    veterinario_id: Optional[int] = None,
    user_id: Optional[int] = None
):
    """Vista de lista de tratamientos"""
    query = select(Tratamiento)
    if animal_id:
        query = query.where(Tratamiento.animal_id == animal_id)
    if veterinario_id:
        query = query.where(Tratamiento.veterinario_id == veterinario_id)
        
    tratamientos = session.exec(query).all()
    
    user = None
    if user_id:
        user = get_user(user_id, session)
    
    return templates.TemplateResponse("tratamientos/tratamientos.html", {
        "request": request, 
        "tratamientos": tratamientos,
        "user": user
    })

@router.get("/views/tratamientos/{tratamiento_id}", response_class=HTMLResponse, name="view_tratamiento_detalle")
async def view_tratamiento_detalle(request: Request, tratamiento_id: int):
    """Vista de detalle de tratamiento"""
    return templates.TemplateResponse("tratamientos/detalle.html", {"request": request, "tratamiento_id": tratamiento_id})

@router.get("/chat", response_class=HTMLResponse, name="chat")
async def chat(request: Request):
    """Vista de chat"""
    return templates.TemplateResponse("chat.html", {"request": request})