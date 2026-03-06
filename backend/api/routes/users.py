from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.user import User
from schemas.user import (
    UserRead,
    UserCreate,
    UserUpdate
)
from core.security import get_password_hash, verify_password

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Получить информацию о текущем авторизованном пользователе
    """
    # Логируем для отладки
    auth_header = request.headers.get("authorization")
    print(f"=== /users/me called ===")
    print(f"Auth header: {auth_header}")
    print(f"Current user: {current_user.login if current_user else 'None'}")
    
    return current_user


@router.get("/", response_model=List[UserRead])
async def get_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Получить список всех пользователей (только для администраторов)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Получить пользователя по ID (только для администраторов)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Создать нового пользователя (только для администраторов)
    """
    # Проверка уникальности логина
    existing_user = db.query(User).filter(User.login == user_data.login).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует"
        )
    
    # Создание пользователя
    db_user = User(
        surname=user_data.surname,
        name=user_data.name,
        patronymic=getattr(user_data, 'patronymic', None),
        admin_role=getattr(user_data, 'admin_role', False),
        hashed_password=get_password_hash(user_data.password),
        login=user_data.login,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Обновить данные пользователя (только для администраторов)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Проверка логина на уникальность
    if user_data.login and user_data.login != user.login:
        existing = db.query(User).filter(User.login == user_data.login).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким логином уже существует"
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
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Удалить пользователя (только для администраторов)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Нельзя удалить самого себя
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить свою учетную запись"
        )
    
    db.delete(user)
    db.commit()
    
    return None


@router.post("/change-password")
async def change_password(
    password_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Смена пароля пользователя
    """
    # Проверяем текущий пароль
    if not verify_password(password_data['current_password'], current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный текущий пароль"
        )
    
    # Проверяем сложность нового пароля
    new_password = password_data['new_password']
    if len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль должен содержать минимум 6 символов"
        )
    
    # Хешируем и сохраняем новый пароль
    current_user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Пароль успешно изменен"}