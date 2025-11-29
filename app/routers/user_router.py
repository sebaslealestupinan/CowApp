from fastapi import APIRouter, status, HTTPException, Query
from typing import List, Optional

from app.db import SessionDep
from app.schemas.user_schemas import CreateUser, UpdateUser
from app.models.usuario import Usuario, Role
from app.crud.user_crud import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    get_user_by_email
)

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(data: CreateUser, session: SessionDep):
    if get_user_by_email(data.email, session):
        raise HTTPException(status_code=400, detail="El email ya está registrado.")
    return create_user(data, session)


@router.get("/", response_model=List[Usuario])
def read_users_endpoint(session: SessionDep, role: Optional[Role] = Query(None, description="Filtrar por rol")):
    return get_users(session, role)


@router.get("/{user_id}", response_model=Usuario)
def read_user_endpoint(user_id: int, session: SessionDep):
    user = get_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put("/{user_id}", response_model=Usuario)
def update_user_endpoint(user_id: int, new_data: UpdateUser, session: SessionDep):
    updated_user = update_user(user_id, new_data, session)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, session: SessionDep):
    success = delete_user(user_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None
