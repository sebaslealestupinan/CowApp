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
async def dashboard_ganadero(request: Request, id_user: int, session: Session = Depends(get_session)):

    user = session.get(Usuario, id_user)
    
    
    return templates.TemplateResponse("ganadero.html", {
        "request": request,
        "user": user
    })

from datetime import date

@router.get("/veterinario/{id_user}", response_class=HTMLResponse)
async def dashboard_veterinario(request: Request, id_user: int, session: Session = Depends(get_session)):
    # Get Vet
    vet = session.get(Usuario, id_user)
    tratamientos = session.exec(select(Tratamiento).where(Tratamiento.veterinario_id == id_user, Tratamiento.estado == "activo")).all()
    notifications = session.exec(select(func.count(Mensaje.id)).where(Mensaje.receiver_id == id_user, Mensaje.read == False)).one()
    
    current_date = date.today().strftime("%Y-%m-%d")

    return templates.TemplateResponse("dashboard/veterinario.html", {
        "request": request,
        "user": vet,
        "tratamientos": tratamientos,
        "notifications": notifications,
        "current_date": current_date
    })

@router.get("/veterinario/{id_user}/tratamiento/nuevo", response_class=HTMLResponse)
async def nuevo_tratamiento_veterinario(request: Request, id_user: int, session: Session = Depends(get_session)):
    user = session.get(Usuario, id_user)
    return templates.TemplateResponse("tratamientos/nuevo.html", {"request": request, "user": user})

@router.get("/perfil/{user_id}", response_class=HTMLResponse)
async def view_perfil(request: Request, user_id: int, session: Session = Depends(get_session)):
    user = session.get(Usuario, user_id)
    return templates.TemplateResponse("dashboard/perfil.html", {"request": request, "user": user})
