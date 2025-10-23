import os
from typing import ClassVar
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_DIR: ClassVar[str] = os.path.dirname(os.path.abspath(__file__))
    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"

    class Config:
        env_file = ".env"

settings = Settings()
