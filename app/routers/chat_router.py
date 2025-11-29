from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List

from app.websocket.connection_manager import manager
from app.db import SessionDep
from app.schemas.chat_schemas import CreateMensaje, ReadMensaje
from app.crud.chat_crud import create_mensaje, get_chat_history

router = APIRouter(prefix="/chat", tags=["Chat"])

templates = Jinja2Templates("app/templates")

@router.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        "chat/chat.html",
        {"request": request}
    )

@router.get("/history/{user1_id}/{user2_id}", response_model=List[ReadMensaje])
def get_history_endpoint(user1_id: int, user2_id: int, session: SessionDep):
    return get_chat_history(user1_id, user2_id, session)

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, session: SessionDep):
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Assuming data format: "receiver_id:message_content" for simplicity in this basic implementation
            # In a real app, you'd send JSON
            try:
                receiver_id_str, content = data.split(":", 1)
                receiver_id = int(receiver_id_str)
                
                # Persist message
                mensaje_data = CreateMensaje(
                    contenido=content,
                    sender_id=user_id,
                    receiver_id=receiver_id
                )
                create_mensaje(mensaje_data, session)
                
                # Send to receiver if connected
                await manager.send_personal(receiver_id, f"Usuario {user_id}: {content}")
                
            except ValueError:
                # Fallback to broadcast or error handling if format is wrong
                await manager.broadcast(f"Usuario {user_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(user_id)