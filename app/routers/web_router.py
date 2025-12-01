from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

# Setup templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
@router.get("/views/animales", response_class=HTMLResponse, name="view_animales_lista")
async def view_animales_lista(request: Request):
    """Vista de lista de animales"""
    return templates.TemplateResponse("animales/lista.html", {"request": request})

@router.get("/views/animales/{animal_id}", response_class=HTMLResponse, name="view_animal_detalle")
async def view_animal_detalle(request: Request, animal_id: int):
    """Vista de detalle de animal"""
    return templates.TemplateResponse("animales/detalle.html", {"request": request, "animal_id": animal_id})

@router.get("/views/tratamientos/{tratamiento_id}", response_class=HTMLResponse, name="view_tratamiento_detalle")
async def view_tratamiento_detalle(request: Request, tratamiento_id: int):
    """Vista de detalle de tratamiento"""
    return templates.TemplateResponse("tratamientos/detalle.html", {"request": request, "tratamiento_id": tratamiento_id})

@router.get("/views/visitas", response_class=HTMLResponse, name="view_visitas")
async def view_visitas(request: Request):
    """Vista de solicitudes de visitas"""
    return templates.TemplateResponse("visitas/solicitudes.html", {"request": request})