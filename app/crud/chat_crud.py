from sqlmodel import Session, select, or_, and_, func
from typing import List
from datetime import datetime

from app.models.mensaje import Mensaje
from app.models.usuario import Usuario
from app.schemas.chat_schemas import CreateMensaje, ConversationSummary

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
        ).order_by(Mensaje.timestamp)
    ).all()

def get_user_conversations(user_id: int, session: Session) -> List[ConversationSummary]:
    """
    Obtiene la lista de conversaciones de un usuario con resumen.
    """
    # Obtener todos los usuarios con los que ha chateado
    conversations = []
    
    # Query para obtener usuarios únicos con los que ha intercambiado mensajes
    stmt = select(Mensaje).where(
        or_(Mensaje.sender_id == user_id, Mensaje.receiver_id == user_id)
    )
    messages = session.exec(stmt).all()
    
    # Agrupar por usuario
    user_ids = set()
    for msg in messages:
        other_user_id = msg.receiver_id if msg.sender_id == user_id else msg.sender_id
        user_ids.add(other_user_id)
    
    # Crear resumen para cada conversación
    for other_user_id in user_ids:
        user = session.get(Usuario, other_user_id)
        if not user:
            continue
            
        # Obtener último mensaje
        last_msg_stmt = select(Mensaje).where(
            or_(
                and_(Mensaje.sender_id == user_id, Mensaje.receiver_id == other_user_id),
                and_(Mensaje.sender_id == other_user_id, Mensaje.receiver_id == user_id)
            )
        ).order_by(Mensaje.timestamp.desc()).limit(1)
        
        last_msg = session.exec(last_msg_stmt).first()
        
        # Contar mensajes no leídos
        unread_count = session.exec(
            select(func.count(Mensaje.id)).where(
                and_(
                    Mensaje.receiver_id == user_id,
                    Mensaje.sender_id == other_user_id,
                    Mensaje.read == False
                )
            )
        ).one()
        
        conversations.append(ConversationSummary(
            user_id=user.id,
            user_name=user.nombre,
            user_role=user.role.value,
            last_message=last_msg.contenido if last_msg else None,
            last_message_time=last_msg.timestamp if last_msg else None,
            unread_count=unread_count
        ))
    
    # Ordenar por último mensaje (más reciente primero)
    conversations.sort(key=lambda x: x.last_message_time or datetime.min, reverse=True)
    
    return conversations

def mark_messages_as_read(user_id: int, other_user_id: int, session: Session) -> int:
    """
    Marca todos los mensajes de other_user_id a user_id como leídos.
    Retorna el número de mensajes marcados.
    """
    stmt = select(Mensaje).where(
        and_(
            Mensaje.sender_id == other_user_id,
            Mensaje.receiver_id == user_id,
            Mensaje.read == False
        )
    )
    messages = session.exec(stmt).all()
    
    count = 0
    for msg in messages:
        msg.read = True
        count += 1
    
    session.commit()
    return count

def get_unread_count(user_id: int, other_user_id: int, session: Session) -> int:
    """
    Obtiene el número de mensajes no leídos de other_user_id para user_id.
    """
    return session.exec(
        select(func.count(Mensaje.id)).where(
            and_(
                Mensaje.sender_id == other_user_id,
                Mensaje.receiver_id == user_id,
                Mensaje.read == False
            )
        )
    ).one()
