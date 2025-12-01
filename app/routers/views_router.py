from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/ganadero", response_class=HTMLResponse)
async def dashboard_ganadero(request: Request):
    return templates.TemplateResponse("dashboard/ganadero.html", {"request": request})

@router.get("/veterinario", response_class=HTMLResponse)
async def dashboard_veterinario(request: Request):
    return templates.TemplateResponse("dashboard/veterinario.html", {"request": request})
