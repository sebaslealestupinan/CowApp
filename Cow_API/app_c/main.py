from fastapi import FastAPI
from contextlib import asynccontextmanager
from app_c.database import init_db
from app_c.routers import users, animals, health, messages

@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Iniciando base de datos...")
    init_db()
    print("Base de datos lista.")
    yield
    print("Cerrando aplicacion")



app = FastAPI(
    title="Cow API - Gestión Sanitaria Ganadera",
    version="0.0.3",
    description="API para digitalizar historiales veterinarios y comunicación.",
    lifespan=lifespan,
)

# registrar routers
app.include_router(users.router)
app.include_router(animals.router)
app.include_router(health.router)
app.include_router(messages.router)

@app.get("/")
def root():
    return {"app": "Cow API", "version": "0.2.0"}
