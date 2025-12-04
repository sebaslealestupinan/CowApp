from fastapi import APIRouter, status, HTTPException, Query, UploadFile, File, Form
from typing import List, Optional

from app.db import SessionDep
from app.schemas.user_schemas import CreateUser, UpdateUser
from app.models.usuario import Usuario
from app.crud.user_crud import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    get_user_by_email
)
from app.service_and_config.cloudinary import upload_to_cloudinary

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(data: CreateUser, session: SessionDep):
    if get_user_by_email(data.email, session):
        raise HTTPException(status_code=400, detail="El email ya está registrado.")
    return create_user(data, session)


@router.get("/", response_model=List[Usuario])
def read_users_endpoint(session: SessionDep, role: Optional[str] = Query(None, description="Filtrar por rol"), search: Optional[str] = Query(None, description="Buscar por nombre")):
    return get_users(session, role, search)


@router.get("/{user_id}", response_model=Usuario)
def read_user_endpoint(user_id: int, session: SessionDep):
    user = get_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put("/{user_id}", response_model=Usuario)
async def update_user_endpoint(
    user_id: int,
    session: SessionDep,
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    number_phone: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    imag = None
    if image:
        upload_result = await upload_to_cloudinary(image)
        imag = upload_result["url"]

    # Filter out None values to avoid overwriting existing data with None
    update_dict = {}
    if name is not None:
        update_dict["name"] = name
    if email is not None:
        update_dict["email"] = email
    if password is not None:
        update_dict["password"] = password
    if number_phone is not None:
        update_dict["number_phone"] = number_phone
    if imag is not None:
        update_dict["imag"] = imag

    update_data = UpdateUser(**update_dict)
    
    updated_user = update_user(user_id, update_data, session)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, session: SessionDep):
    success = delete_user(user_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None
