from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
import json

from app.websocket.connection_manager import manager
from app.db import SessionDep
from app.schemas.chat_schemas import CreateMensaje, ReadMensaje, ConversationSummary
from app.crud.chat_crud import (
    create_mensaje, 
    get_chat_history, 
    get_user_conversations,
    mark_messages_as_read
)
from app.crud.user_crud import get_user

router = APIRouter(prefix="/chat", tags=["Chat"])

templates = Jinja2Templates("app/templates")

@router.get("/{sender_id}/{receiver_id}", response_class=HTMLResponse)
async def chat_conversation(
    request: Request, 
    receiver_id: int, 
    session: SessionDep,
    sender_id: int
):

    receiver = get_user(receiver_id, session)
    if not receiver:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    sender = get_user(sender_id, session)
    if not sender:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if sender_id == receiver_id:
        raise HTTPException(status_code=400, detail="No puedes chatear contigo mismo, triste mente :(")
    
    return templates.TemplateResponse("chat/chat.html", {
        "request": request,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "receiver_name": receiver.name,
        "sender_name": sender.name
    })

@router.get("/conversations/{user_id}", response_model=List[ConversationSummary])
def get_conversations_endpoint(user_id: int, session: SessionDep):
    """Obtiene la lista de conversaciones del usuario"""
    return get_user_conversations(user_id, session)

@router.get("/history/{user1_id}/{user2_id}", response_model=List[ReadMensaje])
def get_history_endpoint(user1_id: int, user2_id: int, session: SessionDep):
    """Obtiene el historial de mensajes entre dos usuarios"""
    return get_chat_history(user1_id, user2_id, session)

@router.post("/mark-read/{user_id}/{other_user_id}")
def mark_read_endpoint(user_id: int, other_user_id: int, session: SessionDep):
    """Marca todos los mensajes de other_user_id como leídos"""
    count = mark_messages_as_read(user_id, other_user_id, session)
    return {"marked_as_read": count}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, session: SessionDep):
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                # Esperar JSON con formato: {"receiver_id": int, "content": str}
                message_data = json.loads(data)
                receiver_id = message_data.get("receiver_id")
                content = message_data.get("content")
                
                if not receiver_id or not content:
                    await websocket.send_text(json.dumps({
                        "error": "Formato inválido. Se requiere receiver_id y content"
                    }))
                    continue
                
                # Persistir mensaje
                mensaje_data = CreateMensaje(
                    contenido=content,
                    sender_id=user_id,
                    receiver_id=receiver_id
                )
                db_mensaje = create_mensaje(mensaje_data, session)
                
                # Preparar respuesta con el mensaje completo
                message_response = {
                    "id": db_mensaje.id,
                    "sender_id": user_id,
                    "receiver_id": receiver_id,
                    "content": content,
                    "timestamp": db_mensaje.timestamp.isoformat(),
                    "read": db_mensaje.read
                }
                
                # Enviar al remitente (confirmación)
                await websocket.send_text(json.dumps(message_response))
                
                # Enviar al receptor si está conectado
                await manager.send_personal(receiver_id, json.dumps(message_response))
                
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "error": "Formato JSON inválido"
                }))
            except ValueError as e:
                await websocket.send_text(json.dumps({
                    "error": f"Error en los datos: {str(e)}"
                }))

    except WebSocketDisconnect:
        manager.disconnect(user_id)