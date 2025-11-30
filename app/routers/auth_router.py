from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db import get_session
from app.crud.user_crud import create_user, get_user_by_email
from passlib.context import CryptContext
from app.schemas.user_schemas import CreateUser

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# GET routes to render forms
@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

# POST login handling
@router.post("/login", response_class=HTMLResponse)
async def post_login(request: Request, email: str = Form(...), password: str = Form(...), role: str = Form(...), session: Session = Depends(get_session)):
    user = get_user_by_email(email, session)
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Credenciales inválidas"})
    # Redirect based on role
    if role.lower() == "ganadero":
        return RedirectResponse(url="/views/ganadero", status_code=status.HTTP_302_FOUND)
    elif role.lower() == "veterinario":
        return RedirectResponse(url="/views/veterinario", status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Rol desconocido"})

# POST registration handling
@router.post("/register", response_class=HTMLResponse)
async def post_register(request: Request, nombre: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form(...), session: Session = Depends(get_session)):
    existing_user = get_user_by_email(email, session)
    if existing_user:
        return templates.TemplateResponse("auth/register.html", {"request": request, "error": "El email ya está registrado"})
    hashed_password = get_password_hash(password)
    user_data = {
        "name": nombre,
        "email": email,
        "password": hashed_password,
        "role": role,
        "status": True,
        "telefonos": []
    }
    create_user(CreateUser(**user_data), session)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
