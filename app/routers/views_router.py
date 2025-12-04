from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select, func
from app.db import get_session
from app.models.usuario import Usuario
from app.models.tratamiento import Tratamiento
from app.models.mensaje import Mensaje
from app.models.animal import Animal
from app.db import SessionDep
from app.crud.tratamiento_crud import get_tratamientos_by_animal
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

from app.models.evento import Evento

@router.get("/ganadero/{id_user}", response_class=HTMLResponse)
async def dashboard_ganadero(request: Request, id_user: int, session: Session = Depends(get_session)):

    user = session.get(Usuario, id_user)
    
    # Stats
    muertos_count = session.exec(select(func.count(Animal.id)).where(Animal.propietario_id == id_user, Animal.activo == False)).one()
    nacimientos_count = session.exec(select(func.count(Animal.id)).where(Animal.propietario_id == id_user, Animal.fecha_nacimiento != None)).one()
    total_animales = session.exec(select(func.count(Animal.id)).where(Animal.propietario_id == id_user, Animal.activo == True)).one()

    # Lists for display
    muertos = session.exec(select(Animal).where(Animal.propietario_id == id_user, Animal.activo == False)).all()
    nacimientos = session.exec(select(Animal).where(Animal.propietario_id == id_user, Animal.fecha_nacimiento != None)).all()
    all_animales = session.exec(select(Animal).where(Animal.propietario_id == id_user)).all()

    # Tratamientos con eventos pendientes
    tratamientos = session.exec(
        select(Tratamiento)
        .join(Animal)
        .join(Evento)
        .where(Animal.propietario_id == id_user)
        .where(Evento.estado == "Pendiente")
        .distinct()
    ).all()

    return templates.TemplateResponse("dashboard/ganadero.html", {
        "request": request,
        "user": user,
        "muertos_count": muertos_count,
        "nacimientos_count": nacimientos_count,
        "total_animales": total_animales,
        "muertos": muertos,
        "nacimientos": nacimientos,
        "all_animales": all_animales,
        "tratamientos": tratamientos
    })

from datetime import date

@router.get("/veterinario/{id_user}", response_class=HTMLResponse)
async def dashboard_veterinario(request: Request, id_user: int, session: Session = Depends(get_session)):
    
    alert = request.session.pop("alert", None)

    vet = session.get(Usuario, id_user)
    tratamientos = session.exec(select(Tratamiento).where(Tratamiento.veterinario_id == id_user, Tratamiento.estado == "activo")).all()
    notifications = session.exec(select(func.count(Mensaje.id)).where(Mensaje.receiver_id == id_user, Mensaje.read == False)).one()
    
    current_date = date.today().strftime("%Y-%m-%d")

    return templates.TemplateResponse("dashboard/veterinario.html", {
        "request": request,
        "user": vet,
        "tratamientos": tratamientos,
        "notifications": notifications,
        "current_date": current_date,
        "alert": alert
    })

@router.get("/veterinario/{id_user}/tratamiento/nuevo", response_class=HTMLResponse)
async def nuevo_tratamiento_veterinario(request: Request, id_user: int, session: Session = Depends(get_session)):
    user = session.get(Usuario, id_user)
    return templates.TemplateResponse("tratamientos/nuevo.html", {"request": request, "user": user})

@router.get("/perfil/{user_id}", response_class=HTMLResponse, tags=["Perfil"])
async def view_perfil(request: Request, user_id: int, session: Session = Depends(get_session)):
    user = session.get(Usuario, user_id)
    return templates.TemplateResponse("dashboard/perfil.html", {"request": request, "user": user})



@router.get("/views/animal", response_class=HTMLResponse, name="view_animal_detalle")
async def view_animal_detalle(request: Request, animal_id: int):
    """Vista de detalle de animal"""
    
    return templates.TemplateResponse("animales/detalle.html", {"request": request, "animal_id": animal_id})

@router.get("/views/animales/{ganadero_id}", response_class=HTMLResponse, name="view_animales")
async def view_animales(request: Request, ganadero_id: int, session: Session = Depends(get_session)):
    """Vista de lista de animales del ganadero"""
    animales = session.exec(select(Animal).where(Animal.propietario_id == ganadero_id)).all()
    ganadero = session.get(Usuario, ganadero_id)
    return templates.TemplateResponse("animales/lista.html", {
        "request": request, 
        "animales": animales,
        "user": ganadero
    })

@router.get("/views/tratamientos/{animal_id}", response_class=HTMLResponse, name="view_tratamientos_animal")
async def view_tratamientos_animal(request: Request, animal_id: int, session: SessionDep):
    tratamientos = get_tratamientos_by_animal(animal_id, session)
    return templates.TemplateResponse(
        "animales/detalle.html",
        {
            "request": request,
            "tratamientosList": tratamientos,
            "animal_id": animal_id
        }
    )
