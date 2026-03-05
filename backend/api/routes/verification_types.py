from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.verification_type import VerificationType
from models.user import User
from schemas.verification_type import VerificationTypeRead, VerificationTypeCreate

router = APIRouter(prefix="/verification-types", tags=["Типы поверок"])


@router.get("/", response_model=List[VerificationTypeRead])
def get_verification_types(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Получить список всех типов поверок
    """
    types = db.query(VerificationType).all()
    return types


@router.get("/{type_id}", response_model=VerificationTypeRead)
def get_verification_type(
    type_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Получить тип поверки по ID
    """
    type_obj = db.query(VerificationType).filter(VerificationType.id == type_id).first()
    if not type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип поверки не найден"
        )
    return type_obj


@router.post("/", response_model=VerificationTypeRead, status_code=status.HTTP_201_CREATED)
def create_verification_type(
    type_data: VerificationTypeCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Создать новый тип поверки (только для администратора)
    """
    # Проверка уникальности названия
    existing = db.query(VerificationType).filter(
        VerificationType.type_name == type_data.type_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тип поверки с таким названием уже существует"
        )
    
    db_type = VerificationType(type_name=type_data.type_name)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    
    return db_type