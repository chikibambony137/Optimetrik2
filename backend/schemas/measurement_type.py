from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class MeasurementTypeBase(BaseModel):
    """
    Базовая схема типа средства измерения
    """
    name_company: str = Field(..., description="Название компании", min_length=1, max_length=200)
    batch_number: str = Field(..., description="Номер партии", min_length=1, max_length=100)


class MeasurementTypeCreate(MeasurementTypeBase):
    """
    Схема для создания типа
    """
    model_config = ConfigDict(from_attributes=True)


class MeasurementTypeUpdate(BaseModel):
    """
    Схема для обновления типа
    """
    name_company: Optional[str] = Field(None, description="Название компании", min_length=1, max_length=200)
    batch_number: Optional[str] = Field(None, description="Номер партии", min_length=1, max_length=100)

    model_config = ConfigDict(from_attributes=True)


class MeasurementTypeRead(MeasurementTypeBase):
    """
    Схема для чтения типа
    """
    id: int = Field(..., description="ID типа")

    model_config = ConfigDict(from_attributes=True)


class MeasurementTypeWithInstruments(MeasurementTypeRead):
    """
    Тип с количеством средств измерения
    """
    instruments_count: int = Field(0, description="Количество средств измерения данного типа")