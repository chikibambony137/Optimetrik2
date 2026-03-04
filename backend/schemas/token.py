from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Схема токена"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Данные из токена"""
    user_id: Optional[int] = None
    username: Optional[str] = None