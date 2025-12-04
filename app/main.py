from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from app.db import create_data_base
from starlette.middleware.sessions import SessionMiddleware
from app.routers import (user_router, chat_router, 
    animal_router, tratamiento_router, eventos_router, auth_router, views_router)
from app.service_and_config.cloudinary import MIDDLEWARE

import httpx
import asyncio

ping_url = "https://cowapp-yafm.onrender.com/"
minuts = 14

@asynccontextmanager
async def lifespan(app: FastAPI):
    #async def keep_awake():
    #    while True:
    #        try:
    #            async with httpx.AsyncClient() as client:
    #                await client.get(ping_url, timeout=10)
    #                print("Deeeeeeees pieeeeeertaaaaaaaa.")
    #        except Exception as e:
    #            print("y se durmio pero esto fue el culpable:", e)
    #        await asyncio.sleep(minuts * 60)
    
    #asyncio.create_task(keep_awake())
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

app.add_middleware(
    SessionMiddleware,
    secret_key=MIDDLEWARE
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("paginaPrincipal.html", {"request": request})


app.include_router(views_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(chat_router.router)
app.include_router(animal_router.router)
app.include_router(tratamiento_router.router)
app.include_router(eventos_router.router)