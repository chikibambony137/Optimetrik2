from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ResultBase(BaseModel):
    """
    Базовая схема результата поверки
    """
    result_name: str = Field(..., description="Название результата", min_length=1, max_length=100)


class ResultCreate(ResultBase):
    """
    Схема для создания результата
    """
    model_config = ConfigDict(from_attributes=True)


class ResultRead(ResultBase):
    """
    Схема для чтения результата
    """
    id: int = Field(..., description="ID результата")

    model_config = ConfigDict(from_attributes=True)