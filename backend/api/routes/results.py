from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.result_verification import ResultVerification
from models.user import User
from schemas.result import ResultRead, ResultCreate

router = APIRouter(prefix="/results", tags=["Результаты поверки"])


@router.get("/", response_model=List[ResultRead])
def get_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить список всех результатов поверки
    """
    results = db.query(ResultVerification).all()
    return results


@router.get("/{result_id}", response_model=ResultRead)
def get_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить результат по ID
    """
    result = db.query(ResultVerification).filter(ResultVerification.id == result_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Результат не найден"
        )
    return result


@router.post("/", response_model=ResultRead, status_code=status.HTTP_201_CREATED)
def create_result(
    result_data: ResultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Создать новый результат поверки (только для администратора)
    """
    # Проверка уникальности названия
    existing = db.query(ResultVerification).filter(
        ResultVerification.result_name == result_data.result_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Результат с таким названием уже существует"
        )
    
    db_result = ResultVerification(result_name=result_data.result_name)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    
    return db_result