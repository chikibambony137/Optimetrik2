from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, validator
import re


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    surname: str = Field(..., description="Фамилия", min_length=1, max_length=100)
    name: str = Field(..., description="Имя", min_length=1, max_length=100)
    patronymic: Optional[str] = Field(None, description="Отчество", max_length=100)
    login: str = Field(..., description="Логин", min_length=3, max_length=100)
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """Схема для создания пользователя администратором"""
    password: str = Field(..., description="Пароль", min_length=6, max_length=100)
    admin_role: bool = Field(False, description="Роль администратора")
    
    @validator('login')
    def validate_login(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Логин может содержать только буквы, цифры и подчеркивание')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль должен быть не менее 6 символов')
        return v


class UserRegister(BaseModel):
    """Схема для регистрации нового пользователя"""
    surname: str = Field(..., description="Фамилия", min_length=1, max_length=100)
    name: str = Field(..., description="Имя", min_length=1, max_length=100)
    patronymic: Optional[str] = Field(None, description="Отчество", max_length=100)
    login: str = Field(..., description="Логин", min_length=3, max_length=100)
    password: str = Field(..., description="Пароль", min_length=6, max_length=100)
    
    @validator('login')
    def validate_login(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Логин может содержать только буквы, цифры и подчеркивание')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль должен быть не менее 6 символов')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not any(c.isupper() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        return v


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    surname: Optional[str] = Field(None, description="Фамилия", min_length=1, max_length=100)
    name: Optional[str] = Field(None, description="Имя", min_length=1, max_length=100)
    patronymic: Optional[str] = Field(None, description="Отчество", max_length=100)
    login: Optional[str] = Field(None, description="Логин", min_length=3, max_length=100)
    password: Optional[str] = Field(None, description="Новый пароль", min_length=6, max_length=100)
    admin_role: Optional[bool] = Field(None, description="Роль администратора")
    
    @validator('login')
    def validate_login(cls, v):
        if v is not None and not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Логин может содержать только буквы, цифры и подчеркивание')
        return v
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Схема для входа"""
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")


class UserRead(BaseModel):
    """Схема для чтения пользователя"""
    id: int
    surname: str
    name: str
    patronymic: Optional[str] = None
    login: str
    admin_role: bool = False
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    """Ответ с данными пользователя (без пароля) - алиас для UserRead"""
    id: int
    surname: str
    name: str
    patronymic: Optional[str] = None
    login: str
    admin_role: bool = False
    
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Ответ с токеном"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse