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

@router.get("/views/animal", response_class=HTMLResponse, name="view_animal_detalle")
async def view_animal_detalle(request: Request, animal_id: int):
    """Vista de detalle de animal"""
    return templates.TemplateResponse("animales/detalle.html", {"request": request, "animal_id": animal_id})