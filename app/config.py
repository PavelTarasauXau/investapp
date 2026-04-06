# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # обязательное поле

    class Config:
        env_file = ".env"  # всё так же читает .env

settings = Settings()