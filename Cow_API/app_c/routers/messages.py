from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app_c import models, schemas, services
from app_c.database import get_session

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=schemas.MessageRead)
def send_message(message_in: schemas.MessageCreate, session: Session = Depends(get_session)):
    return services.send_message(session, message_in)

@router.get("/", response_model=List[schemas.MessageRead])
def inbox(recipient_id: int = None, session: Session = Depends(get_session)):
    if not recipient_id:
        raise HTTPException(status_code=400, detail="recipient_id es requerido para listar la bandeja")
    return services.list_messages_for_user(session, recipient_id)

@router.get("/{message_id}", response_model=schemas.MessageRead)
def read_message(message_id: int, session: Session = Depends(get_session)):
    return services.get_message(session, message_id)

@router.put("/{message_id}", response_model=schemas.MessageRead)
def mark_read(message_id: int, update: schemas.MessageUpdate, session: Session = Depends(get_session)):
    return services.mark_message_read(session, message_id, read=update.read if update.read is not None else True)

@router.delete("/{message_id}")
def delete_message(message_id: int, session: Session = Depends(get_session)):
    msg = services.get_message(session, message_id)
    session.delete(msg)
    session.commit()
    return {"200": True}