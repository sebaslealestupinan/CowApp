from sqlmodel import Session, select
from typing import List, Optional

from app.models.tratamiento import Tratamiento
from app.schemas.tratamiento_schemas import CreateTratamiento, UpdateTratamiento

def create_tratamiento(data: CreateTratamiento, session: Session) -> Tratamiento:
    """
    Crea un nuevo tratamiento.
    """
    db_tratamiento = Tratamiento.model_validate(data)
    session.add(db_tratamiento)
    session.commit()
    session.refresh(db_tratamiento)
    return db_tratamiento

def get_tratamiento(tratamiento_id: int, session: Session) -> Optional[Tratamiento]:
    """
    Obtiene un tratamiento por su ID.
    """
    return session.get(Tratamiento, tratamiento_id)

def get_tratamientos_by_animal(animal_id: int, session: Session) -> List[Tratamiento]:
    """
    Obtiene todos los tratamientos de un animal específico.
    """
    return session.exec(select(Tratamiento).where(Tratamiento.animal_id == animal_id)).all()

def update_tratamiento(tratamiento_id: int, tratamiento_update: UpdateTratamiento, session: Session) -> Optional[Tratamiento]:
    """
    Actualiza los datos de un tratamiento.
    """
    db_tratamiento = session.get(Tratamiento, tratamiento_id)
    if not db_tratamiento:
        return None

    update_data = tratamiento_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tratamiento, key, value)
    
    session.add(db_tratamiento)
    session.commit()
    session.refresh(db_tratamiento)
    return db_tratamiento

def delete_tratamiento(tratamiento_id: int, session: Session) -> bool:
    """
    Elimina un tratamiento.
    """
    db_tratamiento = session.get(Tratamiento, tratamiento_id)
    if not db_tratamiento:
        return False
    
    session.delete(db_tratamiento)
    session.commit()
    return True
