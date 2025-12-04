from sqlmodel import Session, select
from typing import List, Optional

from app.models.evento import Evento
from app.schemas.evento_schemas import CreateEvento, UpdateEvento

def create_evento(data, session: Session) -> Evento:
    """
    Crea un nuevo evento.
    """
    db_evento = Evento.model_validate(data)
    session.add(db_evento)
    session.commit()
    session.refresh(db_evento)
    return db_evento

def get_evento(evento_id: int, session: Session) -> Optional[Evento]:
    """
    Obtiene un evento por su ID.
    """
    return session.get(Evento, evento_id)

def get_eventos_by_tratamiento(tratamiento_id: int, session: Session) -> List[Evento]:
    """
    Obtiene todos los eventos de un tratamiento específico.
    """
    return session.exec(select(Evento).where(Evento.tratamiento_id == tratamiento_id)).all()

def update_evento(evento_id: int, evento_update: UpdateEvento, session: Session) -> Optional[Evento]:
    """
    Actualiza los datos de un evento.
    """
    db_evento = session.get(Evento, evento_id)
    if not db_evento:
        return None

    update_data = evento_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_evento, key, value)
    
    session.add(db_evento)
    session.commit()
    session.refresh(db_evento)
    return db_evento

def delete_evento(evento_id: int, session: Session) -> bool:
    """
    Elimina un evento.
    """
    db_evento = session.get(Evento, evento_id)
    if not db_evento:
        return False
    
    session.delete(db_evento)
    session.commit()
    return True
