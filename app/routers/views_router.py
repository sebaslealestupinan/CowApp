from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select, func
from app.db import get_session
from app.models.usuario import Usuario
from app.models.tratamiento import Tratamiento
from app.models.mensaje import Mensaje
from app.models.animal import Animal

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/ganadero/{id_user}", response_class=HTMLResponse)
async def dashboard_ganadero(request: Request, id_user: int):
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

@router.get("/veterinario/{id_user}", response_class=HTMLResponse)
async def dashboard_veterinario(request: Request, id_user: int, session: Session = Depends(get_session)):
    # Get Vet
    vet = session.get(Usuario, id_user)
    if not vet:
        # In a real app, handle 404 or redirect
        return HTMLResponse(content="Veterinario no encontrado", status_code=404)

    # Get Treatments (eager load animal and owner if needed, but simple access might work if session is active)
    # Using selectinload to ensure relationships are loaded
    from sqlalchemy.orm import selectinload
    statement = (
        select(Tratamiento)
        .where(Tratamiento.veterinario_id == id_user)
        .options(selectinload(Tratamiento.animal).selectinload(Animal.propietario))
    )
    tratamientos = session.exec(statement).all()

    # Get Notifications (Unread messages)
    statement_msgs = select(func.count(Mensaje.id)).where(Mensaje.receiver_id == id_user, Mensaje.read == False)
    notifications = session.exec(statement_msgs).one()

    return templates.TemplateResponse("dashboard/veterinario.html", {
        "request": request,
        "vet": vet,
        "tratamientos": tratamientos,
        "notifications": notifications
    })
