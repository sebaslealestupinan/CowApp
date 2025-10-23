from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app_c import models, schemas, services
from app_c.database import get_session

router = APIRouter(prefix="/health", tags=["health"])

@router.post("/", response_model=schemas.HealthRecordRead)
def create_health_record(hr_in: schemas.HealthRecordCreate, session: Session = Depends(get_session)):
    return services.create_health_record(session, hr_in)

@router.get("/animal/{animal_id}", response_model=List[schemas.HealthRecordRead])
def list_records_for_animal(animal_id: int, session: Session = Depends(get_session)):
    return services.list_health_records_for_animal(session, animal_id)

@router.get("/{hr_id}", response_model=schemas.HealthRecordRead)
def get_record(hr_id: int, session: Session = Depends(get_session)):
    return services.get_health_record(session, hr_id)

@router.put("/{hr_id}", response_model=schemas.HealthRecordRead)
def update_record(hr_id: int, hr_in: schemas.HealthRecordUpdate, session: Session = Depends(get_session)):
    return services.update_health_record(session, hr_id, hr_in)

@router.delete("/{hr_id}")
def delete_record(hr_id: int, session: Session = Depends(get_session)):
    return services.delete_health_record(session, hr_id)