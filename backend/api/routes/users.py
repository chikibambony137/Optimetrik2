from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.dependencies import get_db  # добавлен app.
from models.user import User         # добавлен app.
from schemas.user import (           # добавлен app.
    UserLogin, 
    UserRegister, 
    UserBase, 
    UserResponse,
    UserCreate,  # добавил недостающие схемы
    UserUpdate,
    UserRead
)
from core.security import get_password_hash  # добавлен импорт в начало

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/", response_model=List[UserRead])
def get_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Получить список всех пользователей
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить пользователя по ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Создать нового пользователя
    """
    # Проверка уникальности логина
    existing_user = db.query(User).filter(User.login == user_data.login).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует"
        )
    
    # Проверка уникальности email, если он есть
    if hasattr(user_data, 'email') and user_data.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )
    
    # Создание пользователя
    db_user = User(
        surname=user_data.surname,
        name=user_data.name,
        patronymic=getattr(user_data, 'patronymic', None),
        admin_role=getattr(user_data, 'admin_role', False),
        hashed_password=get_password_hash(user_data.password),
        login=user_data.login,
        email=getattr(user_data, 'email', None),
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить данные пользователя
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Проверка логина на уникальность (если меняется)
    if user_data.login and user_data.login != user.login:
        existing = db.query(User).filter(User.login == user_data.login).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким логином уже существует"
            )
    
    # Проверка email на уникальность (если меняется)
    if hasattr(user_data, 'email') and user_data.email and user_data.email != user.email:
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )
    
    # Обновление полей
    update_data = user_data.model_dump(exclude_unset=True)
    
    # Если есть пароль - хешируем
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить пользователя
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Проверка на связанные поверки
    if user.verifications:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить пользователя, у которого есть проведенные поверки"
        )
    
    db.delete(user)
    db.commit()
    
    return None


# # Добавим эндпоинт для регистрации (если нужен отдельно от create_user)
# @router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def register_user(
#     user_data: UserRegister,
#     db: Session = Depends(get_db)
# ):
#     """
#     Регистрация нового пользователя (публичный эндпоинт)
#     """
#     # Проверка уникальности логина
#     existing_user = db.query(User).filter(User.login == user_data.login).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Пользователь с таким логином уже существует"
#         )
    
#     # Проверка уникальности email
#     if user_data.email:
#         existing_email = db.query(User).filter(User.email == user_data.email).first()
#         if existing_email:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Пользователь с таким email уже существует"
#             )
    
#     # Создание пользователя (обычный пользователь, не админ)
#     db_user = User(
#         surname=user_data.surname,
#         name=user_data.name,
#         patronymic=user_data.patronymic,
#         login=user_data.login,
#         email=user_data.email,
#         hashed_password=get_password_hash(user_data.password),
#         admin_role=False,  # обычный пользователь
#         is_active=True
#     )
    
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
    
#     return db_user