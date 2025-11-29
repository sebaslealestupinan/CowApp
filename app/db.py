from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends

url_data_base= "sqlite:///dB.db"

engine = create_engine(url_data_base)

def create_data_base():
    from app.models.animal import Animal
    from app.models.usuario import Usuario, Telefono
    from app.models.mensaje import Mensaje
    from app.models.tratamiento import Tratamiento
    from app.models.evento import Evento
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep= Annotated[Session, Depends(get_session)]