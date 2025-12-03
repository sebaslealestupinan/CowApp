from sqlmodel import Session, select
from typing import List, Optional

from app.models.tratamiento import Tratamiento
from app.schemas.tratamiento_schemas import CreateTratamiento, UpdateTratamiento

from datetime import datetime, timedelta
from app.models.evento import Evento

def create_tratamiento(data: CreateTratamiento, session: Session) -> Tratamiento:
    """
    Crea un nuevo tratamiento y genera eventos diarios automáticos.
    """
    db_tratamiento = Tratamiento.model_validate(data)
    session.add(db_tratamiento)
    session.commit()
    session.refresh(db_tratamiento)

    # Generar eventos diarios
    try:
        start_date = datetime.strptime(db_tratamiento.fecha_inicio, "%Y-%m-%d")
        end_date = datetime.strptime(db_tratamiento.fecha_fin, "%Y-%m-%d")
        
        current_date = start_date
        while current_date <= end_date:
            evento = Evento(
                tratamiento_id=db_tratamiento.id,
                fecha=current_date,
                estado="Pendiente",
                tipo="Seguimiento Diario",
                observaciones=f"Seguimiento programado para el día {current_date.strftime('%Y-%m-%d')}",
                responsable="Veterinario" 
            )
            session.add(evento)
            current_date += timedelta(days=1)
        
        session.commit()
    except ValueError:
        # Manejar caso donde las fechas no tengan el formato correcto
        pass

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
