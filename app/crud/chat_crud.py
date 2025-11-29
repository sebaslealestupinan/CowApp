from sqlmodel import Session, select, or_, and_
from typing import List

from app.models.mensaje import Mensaje
from app.schemas.chat_schemas import CreateMensaje

def create_mensaje(data: CreateMensaje, session: Session) -> Mensaje:
    """
    Crea un nuevo mensaje.
    """
    db_mensaje = Mensaje.model_validate(data)
    session.add(db_mensaje)
    session.commit()
    session.refresh(db_mensaje)
    return db_mensaje

def get_chat_history(user1_id: int, user2_id: int, session: Session) -> List[Mensaje]:
    """
    Obtiene el historial de chat entre dos usuarios.
    """
    return session.exec(
        select(Mensaje).where(
            or_(
                and_(Mensaje.sender_id == user1_id, Mensaje.receiver_id == user2_id),
                and_(Mensaje.sender_id == user2_id, Mensaje.receiver_id == user1_id)
            )
        ).order_by(Mensaje.id)
    ).all()
