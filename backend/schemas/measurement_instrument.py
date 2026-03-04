from typing import Optional
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class MeasurementInstrumentBase(BaseModel):
    """
    Базовая схема средства измерения
    """
    serial_number: str = Field(..., description="Серийный номер", min_length=1, max_length=100)
    date_admission: date = Field(..., description="Дата поступления")
    id_type_instrument: int = Field(..., description="ID типа средства измерения", gt=0)


class MeasurementInstrumentCreate(MeasurementInstrumentBase):
    """
    Схема для создания средства измерения
    """
    model_config = ConfigDict(from_attributes=True)


class MeasurementInstrumentUpdate(BaseModel):
    """
    Схема для обновления средства измерения
    """
    serial_number: Optional[str] = Field(None, description="Серийный номер", min_length=1, max_length=100)
    date_admission: Optional[date] = Field(None, description="Дата поступления")
    id_type_instrument: Optional[int] = Field(None, description="ID типа средства измерения", gt=0)

    model_config = ConfigDict(from_attributes=True)


class MeasurementInstrumentRead(MeasurementInstrumentBase):
    """
    Схема для чтения средства измерения
    """
    id: int = Field(..., description="ID средства измерения")

    model_config = ConfigDict(from_attributes=True)


class MeasurementInstrumentWithType(MeasurementInstrumentRead):
    """
    Средство измерения с информацией о типе
    """
    type_name: str = Field(..., description="Название типа")
    type_company: str = Field(..., description="Компания-производитель")


class MeasurementInstrumentWithVerifications(MeasurementInstrumentRead):
    """
    Средство измерения с информацией о последней поверке
    """
    last_verification_date: Optional[date] = Field(None, description="Дата последней поверки")
    last_verification_result: Optional[str] = Field(None, description="Результат последней поверки")
    valid_until: Optional[date] = Field(None, description="Действителен до")