from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List

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

router = APIRouter(tags=["Evento"], prefix="/eventos")

@router.post("/", response_model=ReadEvento, status_code=status.HTTP_201_CREATED)
def create_evento_endpoint(evento: CreateEvento, session: SessionDep):
    # Verify treatment exists
    tratamiento = session.get(Tratamiento, evento.tratamiento_id)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento asociado no encontrado")
        
    return create_evento(evento, session)

@router.get("/{evento_id}", response_model=ReadEvento)
def read_evento_endpoint(evento_id: int, session: SessionDep):
    evento = get_evento(evento_id, session)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento

@router.get("/tratamiento/{tratamiento_id}", response_model=List[ReadEvento])
def read_eventos_by_tratamiento_endpoint(tratamiento_id: int, session: SessionDep):
    return get_eventos_by_tratamiento(tratamiento_id, session)

@router.put("/{evento_id}", response_model=ReadEvento)
def update_evento_endpoint(evento_id: int, evento_update: UpdateEvento, session: SessionDep):
    evento = update_evento(evento_id, evento_update, session)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento

@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evento_endpoint(evento_id: int, session: SessionDep):
    success = delete_evento(evento_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return None