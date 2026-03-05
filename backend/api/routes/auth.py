from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt

from api.dependencies import get_db
from core.config import settings
from core.security import get_password_hash, verify_password
from models.user import User
from schemas.user import UserRegister, UserResponse, UserLogin, TokenResponse

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя
    """
    # Проверка уникальности логина
    existing_login = db.query(User).filter(User.login == user_data.login).first()
    if existing_login:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует"
        )
    
    # Создаем нового пользователя
    # По умолчанию обычный пользователь (не админ)
    db_user = User(
        surname=user_data.surname,
        name=user_data.name,
        patronymic=user_data.patronymic,
        login=user_data.login,
        hashed_password=get_password_hash(user_data.password),
        admin_role=False,  # обычный пользователь
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Вход в систему
    """
    # Ищем пользователя по логину
    user = db.query(User).filter(
        (User.login == form_data.username)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Проверяем пароль
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    # Создаем JWT токен
    access_token = create_access_token(
        data={"sub": str(user.id), "login": user.login}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


# @router.post("/login/json", response_model=TokenResponse)
# def login_json(
#     login_data: UserLogin,
#     db: Session = Depends(get_db)
# ):
#     """
#     Вход в систему (с JSON телом вместо form-data)
#     """
#     # Ищем пользователя по логину
#     user = db.query(User).filter(
#         (User.login == login_data.login)
#     ).first()
    
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Неверный логин или пароль"
#         )
    
#     if not verify_password(login_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Неверный логин или пароль"
#         )
    
#     access_token = create_access_token(
#         data={"sub": str(user.id), "login": user.login}
#     )
    
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "user": user
#     }


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Создание JWT токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.get("/verify-token", response_model=UserResponse)
def verify_token(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Проверить валидность токена и получить информацию о пользователе
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный токен"
            )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    return user