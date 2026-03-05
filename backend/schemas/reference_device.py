from typing import Optional
from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ReferenceDeviceBase(BaseModel):
    """
    Базовая схема эталонного средства измерения
    """
    serial_number: str = Field(..., description="Серийный номер", min_length=1, max_length=100)
    date_admission: date = Field(..., description="Дата поступления")
    valid_for: date = Field(..., description="Действителен до")


class ReferenceDeviceCreate(ReferenceDeviceBase):
    """
    Схема для создания эталона
    """
    @model_validator(mode='after')
    def validate_dates(self):
        """Проверка, что дата окончания позже даты поступления"""
        if self.valid_for <= self.date_admission:
            raise ValueError('Дата окончания срока должна быть позже даты поступления')
        return self

    model_config = ConfigDict(from_attributes=True)


class ReferenceDeviceUpdate(BaseModel):
    """
    Схема для обновления эталона
    """
    serial_number: Optional[str] = Field(None, description="Серийный номер", min_length=1, max_length=100)
    date_admission: Optional[date] = Field(None, description="Дата поступления")
    valid_for: Optional[date] = Field(None, description="Действителен до")

    @model_validator(mode='after')
    def validate_dates(self):
        """Проверка, что дата окончания позже даты поступления (если обе даты указаны)"""
        if self.date_admission and self.valid_for and self.valid_for <= self.date_admission:
            raise ValueError('Дата окончания срока должна быть позже даты поступления')
        return self

    model_config = ConfigDict(from_attributes=True)


class ReferenceDeviceRead(ReferenceDeviceBase):
    """
    Схема для чтения эталона
    """
    id: int = Field(..., description="ID эталона")
    is_valid: Optional[bool] = Field(None, description="Валиден на текущую дату")

    model_config = ConfigDict(from_attributes=True)


class ReferenceDeviceWithUsage(ReferenceDeviceRead):
    """
    Эталон с информацией об использовании
    """
    usage_count: int = Field(0, description="Количество использований в поверках")
    last_used: Optional[date] = Field(None, description="Дата последнего использования")