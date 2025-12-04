from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from app.models.animal import Animal
from app.models.tratamiento import Tratamiento
from app.schemas.animal_schemas import CreateAnimal, UpdateAnimal

def create_animal(data: CreateAnimal, session: Session) -> Animal:
    """
    Crea un nuevo animal.
    """
    db_animal = Animal.model_validate(data)
    session.add(db_animal)
    session.commit()
    session.refresh(db_animal)
    return db_animal

def get_animal(animal_id: int, session: Session) -> Optional[Animal]:
    """
    Obtiene un animal por su ID.
    """
    return session.get(Animal, animal_id)

def get_animals_by_owner(owner_id: int, session: Session) -> List[Animal]:
    """
    Obtiene todos los animales de un propietario específico.
    """
    return session.exec(select(Animal).where(Animal.propietario_id == owner_id)).all()

def update_animal(animal_id: int, animal_update: UpdateAnimal, session: Session) -> Optional[Animal]:
    """
    Actualiza los datos de un animal.
    """
    db_animal = session.get(Animal, animal_id)
    if not db_animal:
        return None

    update_data = animal_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_animal, key, value)
    
    db_animal.updated_at = datetime.utcnow()
    
    session.add(db_animal)
    session.commit()
    session.refresh(db_animal)
    return db_animal

def delete_animal(animal_id: int, session: Session) -> bool:
    """
    Elimina un animal (o lo marca como inactivo si se prefiere soft delete, 
    pero aquí implementamos borrado físico para consistencia con el router anterior).
    """
    db_animal = session.get(Animal, animal_id)
    if not db_animal:
        return False
    
    session.delete(db_animal)
    session.commit()
    return True

def get_animal_with_tratamientos(animal_id: int, session: Session) -> Optional[Animal]:
    """
    Obtiene un animal por su ID con sus tratamientos.
    """
    data = {"animal": None, "tratamientos": None}

    animal = session.exec(select(Animal).where(Animal.id == animal_id)).first()
    if animal:
        data["animal"] = animal
    tratamientos = session.exec(select(Tratamiento).where(Tratamiento.animal_id == animal_id)).all()
    if tratamientos:
        data["tratamientos"] = tratamientos

    return data

