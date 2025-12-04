from fastapi import APIRouter, HTTPException, status, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import List, Optional
from datetime import datetime

from app.db import SessionDep
from app.schemas.evento_schemas import CreateEvento, ReadEvento, UpdateEvento
from app.crud.evento_crud import (
    create_evento,
    get_evento,
    get_eventos_by_tratamiento,
    update_evento,
    delete_evento
)
from app.models.tratamiento import Tratamiento
from app.service_and_config.cloudinary import upload_to_cloudinary

router = APIRouter(tags=["Evento"], prefix="/eventos")

@router.post("/", response_model=ReadEvento, status_code=status.HTTP_201_CREATED)
async def create_evento_endpoint(
    session: SessionDep,
    tratamiento_id: int = Form(...),
    fecha: str = Form(default=None),
    estado: str = Form(...),
    tipo: str = Form(...),
    observaciones: str = Form(...),
    responsable: str = Form(...),
    imagen: UploadFile = File(None)
):
    # Verify treatment exists
    tratamiento = session.get(Tratamiento, tratamiento_id)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento asociado no encontrado")
    
    # Handle date parsing if provided, otherwise default to now
    fecha_dt = datetime.now()
    if fecha:
        try:
            fecha_dt = datetime.fromisoformat(fecha)
        except ValueError:
            pass # Keep default now if parsing fails

    image_url = None
    if imagen and imagen.filename:
        try:
            upload_result = await upload_to_cloudinary(imagen)
            image_url = upload_result.get("url")
        except Exception as e:
            print(f"Error uploading image: {e}")
            # Optionally handle error, but for now we proceed without image or log it

    evento = CreateEvento(
        tratamiento_id=tratamiento_id,
        fecha=fecha_dt,
        estado=estado,
        tipo=tipo,
        observaciones=observaciones,
        responsable=responsable,
        imagen=image_url
    )
        
    create_evento(evento, session)

    return RedirectResponse(url=f"/tratamientos/read/{tratamiento.id}", status_code=status.HTTP_302_FOUND)

@router.get("/detalle/{evento_id}", response_model=ReadEvento)
def read_evento_endpoint(evento_id: int, session: SessionDep):
    evento = get_evento(evento_id, session)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento

@router.put("/update/{evento_id}", response_model=ReadEvento)
def update_evento_endpoint(evento_id: int, evento_update: UpdateEvento, session: SessionDep):
    evento = update_evento(evento_id, evento_update, session)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento