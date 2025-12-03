from fastapi import APIRouter, Request, Form, Depends, status, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.db import get_session
from app.crud.user_crud import create_user, get_user_by_email
from app.schemas.user_schemas import CreateUser
from typing import Optional
from app.service_and_config.cloudinary import upload_to_cloudinary
from app.models.usuario import Usuario

router = APIRouter()


templates = Jinja2Templates(directory="app/templates")

def redirec(role: str, usuario: Usuario):
    routes = {
        "ganadero": f"/ganadero/{usuario.id}",
        "veterinario": f"/veterinario/{usuario.id}",
    }
    url = routes.get(role.lower())
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.get("/login", response_class=HTMLResponse, name="view_login")
async def get_login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse, name="view_register")
async def get_register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def post_login(request: Request, email: str = Form(...), password: str = Form(...), 
role: str = Form(...), session: Session = Depends(get_session)):
    user = get_user_by_email(email, session)
    if not user or user.password != password:
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Credenciales inválidas"})
   
    return redirec(role, user)
    
@router.post("/register", response_class=HTMLResponse)
async def post_register(request: Request, name: str = Form(...), email: str = Form(...), 
password: str = Form(...), number_phone: str = Form(...), image: Optional[UploadFile] = File(None), role: str = Form(...), 
session: Session = Depends(get_session)):
    existing_user = get_user_by_email(email, session)
    if existing_user:
        return templates.TemplateResponse("auth/register.html", {"request": request, "error": "El email ya está registrado"})

    img_url = None
    if image:
        try:
            data_completed = await upload_to_cloudinary(image)
            img_url = data_completed["url"]
        except Exception as e:
            return templates.TemplateResponse("auth/register.html", {"request": request, "error": str(e)})

    user_data = {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "status": True,
        "number_phone": number_phone,
        "imag": img_url
    }

    user = Usuario.model_validate(user_data)   
    session.add(user)
    session.commit()
    session.refresh(user)

    return redirec(role, user)