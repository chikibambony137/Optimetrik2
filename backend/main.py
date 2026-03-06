from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.routes import *
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import get_db


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)

app.include_router(verifications.router)
app.include_router(test_tools.router)
app.include_router(reference_devices.router)
app.include_router(measurement_instruments.router)

app.include_router(measurement_types.router)
app.include_router(results.router)
app.include_router(verification_types.router)


@app.get("/")
def health_check(db: Session = Depends(get_db)):
    """
    Проверка работоспособности API и подключения к БД
    """
    try:
        # Пробуем выполнить запрос к БД
        db.execute(text("SELECT 1")).scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "✅ API и БД работают"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }