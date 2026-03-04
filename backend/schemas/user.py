from typing import Optional
from pydantic import BaseModel, ConfigDict


# Базовая схема
class UserBase(BaseModel):
    surname: str
    name: str
    patronymic: Optional[str] = None
    admin_role: bool = False
    login: str


# Схема для создания
class UserCreate(UserBase):
    password: str  # Пароль отдельно, не хранится в базе как есть
    
    model_config = ConfigDict(from_attributes=True)


# Схема для обновления
class UserUpdate(BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    patronymic: Optional[str] = None
    admin_role: Optional[bool] = None
    login: Optional[str] = None
    password: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# Схема для ответа (без пароля!)
class UserRead(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)