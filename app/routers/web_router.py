from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

# Setup templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/views/ganadero", response_class=HTMLResponse, name="view_ganadero")
async def view_ganadero(request: Request):
    """Vista del dashboard para ganaderos"""
    return templates.TemplateResponse("ganadero.html", {"request": request})

@router.get("/views/veterinario", response_class=HTMLResponse, name="view_veterinario")
async def view_veterinario(request: Request):
    """Vista del dashboard para veterinarios"""
    return templates.TemplateResponse("veterinario.html", {"request": request})

@router.get("/", response_class=HTMLResponse, name="view_home")
async def view_home(request: Request):
    """Página de inicio"""
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/views/chat", response_class=HTMLResponse, name="view_chat")
async def view_chat(request: Request):
    """Pgaina de chat"""
    return templates.TemplateResponse("chat/chat.html", {"request": request})

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

@router.get("/login", response_class=HTMLResponse, name="view_login")
async def view_login(request: Request):
    """Vista de inicio de sesión"""
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse, name="view_register")
async def view_register(request: Request):
    """Vista de registro"""
    return templates.TemplateResponse("auth/register.html", {"request": request})