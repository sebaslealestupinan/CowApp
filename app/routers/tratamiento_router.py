from fastapi import APIRouter, HTTPException, status, Form, Request
from typing import List, Optional
from sqlmodel import select
from app.crud.user_crud import get_user
from app.db import SessionDep
from app.models.usuario import Usuario
from app.schemas.tratamiento_schemas import CreateTratamiento, ReadTratamiento, UpdateTratamiento
from app.crud.evento_crud import get_eventos_by_tratamiento
from app.crud.tratamiento_crud import (
    create_tratamiento,
    get_tratamiento,
    get_tratamientos_by_animal,
    delete_tratamiento,
    update_tratamiento
)
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.tratamiento import Tratamiento

router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])
templates = Jinja2Templates(directory="app/templates")

@router.post("/", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
def create_tratamiento_endpoint(request: Request, session: SessionDep, 
animal_id: int = Form(...),
nombre_tratamiento: str = Form(...),
diagnostico: str = Form(...),
medicamento: str = Form(None),
dosis: float = Form(None),
fecha_inicio: str = Form(...),
fecha_fin: str = Form(...),
estado: str = Form(...),
veterinario_id: int = Form(...)):

    tratamiento = CreateTratamiento(
        animal_id=animal_id,
        nombre_tratamiento=nombre_tratamiento,
        diagnostico=diagnostico,
        medicamento=medicamento,
        dosis=dosis,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado=estado,
        veterinario_id=veterinario_id
    )

    create_tratamiento(tratamiento, session)

    return RedirectResponse(
        url=f"/veterinario/{veterinario_id}?message=Tratamiento creado exitosamente",
        status_code=303
    )   

@router.get("/read/{tratamiento_id}", response_class=HTMLResponse, name="view_tratamiento_detalle")
async def view_tratamiento_detalle(request: Request, tratamiento_id: int, session: SessionDep):
    """Vista de detalle de tratamiento"""
    tratamiento = get_tratamiento(tratamiento_id, session)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    eventos = get_eventos_by_tratamiento(tratamiento_id, session)
    return templates.TemplateResponse("tratamientos/detalle.html", {"request": request, "tratamiento": tratamiento, "eventos": eventos})


@router.get("/all", response_class=HTMLResponse, name="view_tratamientos_lista")
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

@router.get("/{tratamiento_id}/evento/nuevo", response_class=HTMLResponse)
async def nuevo_evento_tratamiento(request: Request, tratamiento_id: int, session: SessionDep):
    """Vista para registrar un nuevo evento en un tratamiento"""
    tratamiento = get_tratamiento(tratamiento_id, session)
    if not tratamiento:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Tratamiento no encontrado"})
    return templates.TemplateResponse("tratamientos/evento.html", {"request": request, "tratamiento": tratamiento, "tratamiento_id": tratamiento_id})

@router.put("/update/{tratamiento_id}", response_model=ReadTratamiento)
def update_tratamiento_endpoint(tratamiento_id: int, tratamiento_update: UpdateTratamiento, session: SessionDep):
    tratamiento = update_tratamiento(tratamiento_id, tratamiento_update, session)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return tratamiento

@router.delete("/delete/{tratamiento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tratamiento_endpoint(tratamiento_id: int, session: SessionDep):
    success = delete_tratamiento(tratamiento_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return None
