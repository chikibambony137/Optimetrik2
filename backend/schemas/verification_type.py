from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class VerificationTypeBase(BaseModel):
    """
    Базовая схема типа поверки
    """
    type_name: str = Field(..., description="Название типа поверки", min_length=1, max_length=30)


class VerificationTypeCreate(VerificationTypeBase):
    """
    Схема для создания типа поверки
    """
    model_config = ConfigDict(from_attributes=True)


class VerificationTypeRead(VerificationTypeBase):
    """
    Схема для чтения типа поверки
    """
    id: int = Field(..., description="ID типа поверки")

    model_config = ConfigDict(from_attributes=True)