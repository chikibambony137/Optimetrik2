from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from core.database import SessionLocal
from core.config import settings
from models.user import User

# Схема аутентификации - ТОЧНО УКАЖИТЕ ПРАВИЛЬНЫЙ URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_db() -> Generator:
    """
    Зависимость для получения сессии базы данных
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
    print(f"=== get_current_user called ===")
    print(f"Token received: {token[:20] if token else 'None'}...")
    
    if not token:
        print("No token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не предоставлен токен авторизации",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Декодируем JWT токен
        print(f"Decoding token with secret: {settings.SECRET_KEY[:5]}...")
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        print(f"Payload: {payload}")
        
        user_id = payload.get("sub")
        print(f"User ID from token: {user_id}")
        
        if user_id is None:
            print("No user_id in payload")
            raise credentials_exception
            
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception
    
    # Получаем пользователя из БД
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        print(f"User with id {user_id} not found in database")
        raise credentials_exception
    
    print(f"User found: {user.login}, admin_role: {user.admin_role}")
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Проверка, что пользователь - администратор
    """
    if not current_user.admin_role:
        print(f"User {current_user.login} is not admin")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуются права администратора"
        )
    
    return current_user


async def get_current_user_optional(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Optional[User]:
    """
    Получить текущего пользователя или None, если не авторизован
    """
    if not token:
        return None
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except JWTError:
        return None