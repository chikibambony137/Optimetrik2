from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TestToolBase(BaseModel):
    """
    Базовая схема тестового стенда
    """
    serial_number: str = Field(..., description="Серийный номер", min_length=1, max_length=100)
    active: bool = Field(True, description="Активен")


class TestToolCreate(TestToolBase):
    """
    Схема для создания стенда
    """
    model_config = ConfigDict(from_attributes=True)


class TestToolUpdate(BaseModel):
    """
    Схема для обновления стенда
    """
    serial_number: Optional[str] = Field(None, description="Серийный номер", min_length=1, max_length=100)
    active: Optional[bool] = Field(None, description="Активен")

    model_config = ConfigDict(from_attributes=True)


class TestToolRead(TestToolBase):
    """
    Схема для чтения стенда
    """
    id: int = Field(..., description="ID стенда")

    model_config = ConfigDict(from_attributes=True)


class TestToolWithUsage(TestToolRead):
    """
    Стенд с информацией об использовании
    """
    verifications_count: int = Field(0, description="Количество проведенных поверок")
    last_used: Optional[str] = Field(None, description="Дата последнего использования")