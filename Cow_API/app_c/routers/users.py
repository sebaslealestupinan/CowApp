from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from typing import List

from app_c import models, schemas, services
from app_c.database import get_session
from app_c.models import DeletedUser

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[schemas.UserRead])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(models.User)).all()

@router.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, session: Session = Depends(get_session)):
    return services.create_user(session, user_in)

@router.get("/id/{user_id}", response_model=schemas.UserRead)
def get_user_id(user_id: int, session: Session = Depends(get_session)):
    return services.get_user(session, user_id)

@router.get("/name/{full_name}", response_model=schemas.UserRead)
def get_user_fullname(full_name: str, session: Session = Depends(get_session)):
    return services.get_user_for(session, full_name)

@router.put("/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, user_in: schemas.UserUpdate, session: Session = Depends(get_session)):
    return services.update_user(session, user_id, user_in)

@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    return services.DeleteUser(session, user_id)

@router.get("/history/deleted_users", response_model=List[DeletedUser])
def get_deleted_users(session: Session = Depends(get_session)):
    deleted_users = session.exec(select(DeletedUser)).all()
    return deleted_users