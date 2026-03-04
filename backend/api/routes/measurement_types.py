from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.measurement_type import MeasurementType
from models.measurement_instrument import MeasurementInstrument
from schemas.measurement_type import MeasurementTypeRead, MeasurementTypeCreate, MeasurementTypeUpdate

router = APIRouter(prefix="/measurement-types", tags=["Типы средств измерения"])


@router.get("/", response_model=List[MeasurementTypeRead])
def get_measurement_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Любой авторизованный
    skip: int = 0,
    limit: int = 100
):
    """
    Получить список всех типов средств измерения
    """
    types = db.query(MeasurementType).offset(skip).limit(limit).all()
    return types


@router.get("/{type_id}", response_model=MeasurementTypeRead)
def get_measurement_type(
    type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Любой авторизованный
):
    """
    Получить тип средства измерения по ID
    """
    type_obj = db.query(MeasurementType).filter(MeasurementType.id == type_id).first()
    if not type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип не найден"
        )
    return type_obj


@router.post("/", response_model=MeasurementTypeRead, status_code=status.HTTP_201_CREATED)
def create_measurement_type(
    type_data: MeasurementTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Создать новый тип средства измерения (только для администратора)
    """
    # Проверка на уникальность комбинации компании и номера партии
    existing = db.query(MeasurementType).filter(
        MeasurementType.name_company == type_data.name_company,
        MeasurementType.batch_number == type_data.batch_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тип с такой компанией и номером партии уже существует"
        )
    
    db_type = MeasurementType(
        name_company=type_data.name_company,
        batch_number=type_data.batch_number
    )
    
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    
    return db_type


@router.put("/{type_id}", response_model=MeasurementTypeRead)
def update_measurement_type(
    type_id: int,
    type_data: MeasurementTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Обновить тип средства измерения (только для администратора)
    """
    type_obj = db.query(MeasurementType).filter(MeasurementType.id == type_id).first()
    if not type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип не найден"
        )
    
    # Проверка на уникальность, если меняются поля
    if (type_data.name_company or type_data.batch_number):
        existing = db.query(MeasurementType).filter(
            MeasurementType.name_company == type_data.name_company or type_obj.name_company,
            MeasurementType.batch_number == type_data.batch_number or type_obj.batch_number,
            MeasurementType.id != type_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Тип с такой компанией и номером партии уже существует"
            )
    
    update_data = type_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(type_obj, field, value)
    
    db.commit()
    db.refresh(type_obj)
    
    return type_obj


@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement_type(
    type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Удалить тип средства измерения (только для администратора)
    """
    type_obj = db.query(MeasurementType).filter(MeasurementType.id == type_id).first()
    if not type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип не найден"
        )
    
    # Проверка на связанные средства измерения
    if type_obj.instruments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить тип, к которому привязаны средства измерения"
        )
    
    db.delete(type_obj)
    db.commit()
    
    return None


@router.get("/{type_id}/instruments", response_model=List[dict])
def get_instruments_by_type(
    type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить все средства измерения данного типа
    """
    type_obj = db.query(MeasurementType).filter(MeasurementType.id == type_id).first()
    if not type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип не найден"
        )
    
    instruments = db.query(MeasurementInstrument).filter(
        MeasurementInstrument.id_type_instrument == type_id
    ).all()
    
    return instruments