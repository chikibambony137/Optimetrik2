from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from decimal import Decimal


class VerificationBase(BaseModel):
    """
    Базовая схема поверки
    """
    planned_date_verification: date = Field(..., description="Планируемая дата поверки")
    date_receipt: date = Field(..., description="Дата поступления прибора")
    id_instrument: int = Field(..., description="ID средства измерения", gt=0)


class VerificationCreate(VerificationBase):
    """
    Схема для создания новой поверки (только планируемая дата и дата поступления)
    """
    @model_validator(mode='after')
    def validate_dates(self):
        """Проверка, что дата поступления не позже планируемой даты"""
        if self.date_receipt > self.planned_date_verification:
            raise ValueError('Дата поступления не может быть позже планируемой даты поверки')
        return self

    model_config = ConfigDict(from_attributes=True)


class VerificationTestData(BaseModel):
    """
    Схема для заполнения тестовых данных
    """
    temperature: Decimal = Field(..., description="Температура", ge=-50, le=100, decimal_places=2)
    pressure: Decimal = Field(..., description="Давление", ge=500, le=1200, decimal_places=2)
    wetness: Decimal = Field(..., description="Влажность", ge=0, le=100, decimal_places=2)
    complete_electric_test: bool = Field(..., description="Тест по току пройден")
    complete_voltage_test: bool = Field(..., description="Тест по напряжению пройден")
    complete_isolation_test: bool = Field(..., description="Тест изоляции пройден")
    id_test_tools: List[int] = Field(..., description="ID использованных стендов", min_length=1)
    id_reference_devices: List[int] = Field(..., description="ID использованных эталонов", min_length=1)


class VerificationComplete(BaseModel):
    """
    Схема для завершения поверки
    """
    id_result: int = Field(..., description="ID результата поверки", gt=0)
    id_type: int = Field(..., description="ID типа поверки", gt=0)


class VerificationUpdate(BaseModel):
    """
    Схема для обновления поверки (частичное обновление)
    """
    planned_date_verification: Optional[date] = Field(None, description="Планируемая дата поверки")
    date_receipt: Optional[date] = Field(None, description="Дата поступления прибора")
    temperature: Optional[Decimal] = Field(None, description="Температура", ge=-50, le=100, decimal_places=2)
    pressure: Optional[Decimal] = Field(None, description="Давление", ge=500, le=1200, decimal_places=2)
    wetness: Optional[Decimal] = Field(None, description="Влажность", ge=0, le=100, decimal_places=2)
    complete_electric_test: Optional[bool] = Field(None, description="Тест по току пройден")
    complete_voltage_test: Optional[bool] = Field(None, description="Тест по напряжению пройден")
    complete_isolation_test: Optional[bool] = Field(None, description="Тест изоляции пройден")
    id_result: Optional[int] = Field(None, description="ID результата поверки", gt=0)
    real_date_verification: Optional[date] = Field(None, description="Фактическая дата поверки")
    valid_until: Optional[date] = Field(None, description="Действителен до")
    id_type: Optional[int] = Field(None, description="ID типа поверки", gt=0)
    id_metrologist: Optional[int] = Field(None, description="ID метролога", gt=0)

    model_config = ConfigDict(from_attributes=True)


class VerificationRead(BaseModel):
    """
    Схема для чтения поверки
    """
    id: int = Field(..., description="ID поверки")
    planned_date_verification: date = Field(..., description="Планируемая дата поверки")
    date_receipt: date = Field(..., description="Дата поступления")
    temperature: Optional[Decimal] = Field(None, description="Температура")
    pressure: Optional[Decimal] = Field(None, description="Давление")
    wetness: Optional[Decimal] = Field(None, description="Влажность")
    complete_electric_test: Optional[bool] = Field(None, description="Тест по току")
    complete_voltage_test: Optional[bool] = Field(None, description="Тест по напряжению")
    complete_isolation_test: Optional[bool] = Field(None, description="Тест изоляции")
    id_result: Optional[int] = Field(None, description="ID результата")
    real_date_verification: Optional[date] = Field(None, description="Фактическая дата")
    valid_until: Optional[date] = Field(None, description="Действителен до")
    id_type: Optional[int] = Field(None, description="ID типа поверки")
    id_metrologist: Optional[int] = Field(None, description="ID метролога")
    id_instrument: int = Field(..., description="ID средства измерения")
    
    # Вычисляемые поля
    is_completed: bool = Field(False, description="Завершена ли поверка")
    is_success: Optional[bool] = Field(None, description="Успешна ли поверка")

    model_config = ConfigDict(from_attributes=True)


class VerificationDetailRead(VerificationRead):
    """
    Детальная информация о поверке с расшифровкой ID
    """
    result_name: Optional[str] = Field(None, description="Название результата")
    type_name: Optional[str] = Field(None, description="Название типа поверки")
    metrologist_name: Optional[str] = Field(None, description="ФИО метролога")
    instrument_serial: str = Field(..., description="Серийный номер прибора")
    test_tools: List[dict] = Field([], description="Использованные стенды")
    reference_devices: List[dict] = Field([], description="Использованные эталоны")


class VerificationListRead(BaseModel):
    """
    Краткая информация для списка поверок
    """
    id: int
    planned_date_verification: date
    real_date_verification: Optional[date]
    instrument_serial: str
    result_name: Optional[str]
    type_name: Optional[str]
    metrologist_name: Optional[str]
    is_completed: bool


class VerificationWithRelations(VerificationRead):
    """
    Поверка со связанными объектами
    """
    test_tools_ids: List[int] = Field([], description="ID использованных стендов")
    reference_devices_ids: List[int] = Field([], description="ID использованных эталонов")