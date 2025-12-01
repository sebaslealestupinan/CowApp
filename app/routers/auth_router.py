from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.db import get_session
from app.crud.user_crud import create_user, get_user_by_email
from app.schemas.user_schemas import CreateUser

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse, name="view_login")
async def get_login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse, name="view_register")
async def get_register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def post_login(request: Request, email: str = Form(...), password: str = Form(...), role: str = Form(...), session: Session = Depends(get_session)):
    user = get_user_by_email(email, session)
    if not user or user.password != password:
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Credenciales inválidas"})
   
    if role.lower() == "ganadero":
        return RedirectResponse(url="/ganadero", status_code=status.HTTP_302_FOUND)
    elif role.lower() == "veterinario":
        return RedirectResponse(url="/veterinario", status_code=status.HTTP_302_FOUND)
    
# POST registration handling
@router.post("/register", response_class=HTMLResponse)
async def post_register(request: Request, nombre: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form(...), session: Session = Depends(get_session)):
    existing_user = get_user_by_email(email, session)
    if existing_user:
        return templates.TemplateResponse("auth/register.html", {"request": request, "error": "El email ya está registrado"})

    user_data = {
        "name": nombre,
        "email": email,
        "password": password,
        "role": role,
        "status": True,
        "telefonos": []
    }
    create_user(CreateUser(**user_data), session)

    if role.lower() == "ganadero":
        return RedirectResponse(url="/ganadero", status_code=status.HTTP_302_FOUND)
    elif role.lower() == "veterinario":
        return RedirectResponse(url="/veterinario", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)