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
    return templates.TemplateResponse("paginaPrincipal.html", {"request": request})

@router.get("/views/chat", response_class=HTMLResponse, name="view_chat")
async def view_chat(request: Request):
    """Pgaina de chat"""
    return templates.TemplateResponse("chat.html", {"request": request})