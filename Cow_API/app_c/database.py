from sqlmodel import create_engine, SQLModel, Session
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

def init_db():
    from app_c import models
    SQLModel.metadata.create_all(engine)
    print("Base de datos creada exitosamente")

def get_session():
    with Session(engine) as session:
        yield session


