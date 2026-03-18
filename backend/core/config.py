from pydantic_settings import BaseSettings
from pydantic import ConfigDict

import os
from dotenv import load_dotenv

# Загружаем .env файл (на всякий случай, но Docker уже передаст переменные)
load_dotenv()

class Settings(BaseSettings):
    # База данных
    # DB_USER: str = os.getenv("DB_USER", "postgres")
    # DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    # DB_NAME: str = os.getenv("DB_NAME", "mydb")
    # DB_HOST: str = os.getenv("DB_HOST", "localhost")
    # DB_PORT: str = os.getenv("DB_PORT", "5432")

    # @property
    # def DATABASE_URL(self) -> str:
    #     return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Настройки приложения
    PROJECT_NAME: str = "Optimetrik"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "API для сервиса поверки средств измерений"
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()