from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from core.database import SessionLocal
from core.config import settings
from models.user import User
from schemas.token import TokenData

# Схема аутентификации (где искать токен)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db() -> Generator:
    """
    Зависимость для получения сессии базы данных
    Используется в каждом запросе, требует закрытия
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Получить текущего пользователя по JWT токену
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Декодируем JWT токен
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    # Получаем пользователя из БД
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Получить активного пользователя (проверка is_active)
    Если в вашей модели User нет поля is_active, можно убрать или заменить
    """
    # Если у вас есть поле is_active, раскомментируйте:
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Проверка, что пользователь - администратор
    """
    if not current_user.admin_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуются права администратора"
        )
    return current_user


# Для обратной совместимости (если где-то используется get_current_user)
get_current_user_from_token = get_current_user


# Опционально: зависимости для пагинации
def get_pagination_params(
    skip: int = 0, 
    limit: int = 100
) -> dict:
    """
    Параметры пагинации
    """
    return {"skip": skip, "limit": limit}