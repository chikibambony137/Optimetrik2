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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def get_db() -> Generator:
    """
    Зависимость для получения сессии базы данных
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==== Если ты ИСПОЛЬЗУЕШЬ fastapi-users ====
# Раскомментируй эти строки и закомментируй ручные реализации выше

from core.users import current_user as fastapi_current_user
from core.users import current_superuser as fastapi_current_superuser
# 
# # Просто реэкспортируем зависимости из fastapi-users
get_current_user = fastapi_current_user
get_current_admin_user = fastapi_current_superuser
get_current_active_user = fastapi_current_user

# # ==== Если ты НЕ используешь fastapi-users ====
# async def get_current_user(
#     db: Session = Depends(get_db),
#     token: str = Depends(oauth2_scheme)
# ) -> User:
#     """
#     Получить текущего пользователя по JWT токену
#     """
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Не предоставлен токен авторизации",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Не удалось подтвердить учетные данные",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     try:
#         # Декодируем JWT токен
#         payload = jwt.decode(
#             token, 
#             settings.SECRET_KEY, 
#             algorithms=[settings.ALGORITHM]
#         )
#         user_id: int = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         token_data = TokenData(user_id=user_id)
#     except JWTError:
#         raise credentials_exception
    
#     # Получаем пользователя из БД
#     user = db.query(User).filter(User.id == token_data.user_id).first()
#     if user is None:
#         raise credentials_exception
    
#     return user


# async def get_current_active_user(
#     current_user: User = Depends(get_current_user)
# ) -> User:
#     """
#     Получить активного пользователя
#     """
#     if not current_user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail="Неактивный пользователь"
#         )
#     return current_user


# def get_current_admin_user(
#     current_user: User = Depends(get_current_active_user)
# ) -> User:
#     """
#     Проверка, что пользователь - администратор
#     """
#     # В зависимости от названия поля в модели
#     if hasattr(current_user, 'is_superuser') and not current_user.is_superuser:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Недостаточно прав. Требуются права администратора"
#         )
#     elif hasattr(current_user, 'admin_role') and not current_user.admin_role:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Недостаточно прав. Требуются права администратора"
#         )
    
#     return current_user





# # Опционально: зависимости для пагинации
# def get_pagination_params(
#     skip: int = 0, 
#     limit: int = 100
# ) -> dict:
#     """
#     Параметры пагинации
#     """
#     return {"skip": skip, "limit": limit}


# # Для опционального текущего пользователя (может быть None)
# async def get_current_user_optional(
#     db: Session = Depends(get_db),
#     token: str = Depends(oauth2_scheme)
# ) -> Optional[User]:
#     """
#     Получить текущего пользователя или None, если не авторизован
#     """
#     if not token:
#         return None
    
#     try:
#         payload = jwt.decode(
#             token, 
#             settings.SECRET_KEY, 
#             algorithms=[settings.ALGORITHM]
#         )
#         user_id: int = payload.get("sub")
#         if user_id is None:
#             return None
        
#         user = db.query(User).filter(User.id == user_id).first()
#         return user
#     except JWTError:
#         return None