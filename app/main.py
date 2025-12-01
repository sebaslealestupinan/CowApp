from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from app.db import create_data_base

# Import routers directly to avoid circular imports
from app.routers import (user_router, chat_router, web_router, 
    animal_router, tratamiento_router, eventos_router, auth_router, views_router)

# en esta funcion se inicializa la base de datos, con todas las tablas en ella
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando base de datos COW...")
    create_data_base()
    print("Db lista.")
    yield
    print("Apagando servidor COW...")

app = FastAPI(
    title="COW 0.1.0",
    description="Gestión ganadera y comunicacion veterinaria.",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("paginaPrincipal.html", {"request": request})

# Routers - web_router debe ir ANTES de veterinario_router para evitar conflictos de rutas

app.include_router(views_router.router)
app.include_router(auth_router.router)
app.include_router(web_router.router)
app.include_router(user_router.router)
app.include_router(chat_router.router)
app.include_router(animal_router.router)
app.include_router(tratamiento_router.router)
app.include_router(eventos_router.router)
