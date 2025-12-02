from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/ganadero", response_class=HTMLResponse)
async def dashboard_ganadero(request: Request):
    # Datos por defecto para usuarios nuevos o sin datos
    datos_default = {
        "id_finca": "N/A",
        "total_animales": 0,
        "en_tratamiento": 0,
        "proximo_parto_fecha": "Sin datos",
        "mensajes_sin_leer": 0,
        "produccion_labels": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
        "produccion_valores": [0, 0, 0, 0, 0, 0, 0],
        "salud_sanos": 0,
        "salud_tratamiento": 0,
        "salud_criticos": 0,
        "eventos_recientes": []
    }
    
    return templates.TemplateResponse("dashboard/ganadero.html", {
        "request": request,
        "datos": datos_default
    })

@router.get("/veterinario", response_class=HTMLResponse)
async def dashboard_veterinario(request: Request):
    return templates.TemplateResponse("dashboard/veterinario.html", {"request": request})
