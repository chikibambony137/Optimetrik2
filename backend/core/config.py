from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # База данных
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/verification_db"
    
    # JWT
    SECRET_KEY: str = "dev-secret-key-for-development-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Настройки приложения
    PROJECT_NAME: str = "Verification Service"
    VERSION: str = "1.0.0"
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()