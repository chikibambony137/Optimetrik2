from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date
from models.user import User

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.measurement_instrument import MeasurementInstrument
from models.measurement_type import MeasurementType
from schemas.measurement_instrument import (
    MeasurementInstrumentRead, 
    MeasurementInstrumentCreate, 
    MeasurementInstrumentUpdate
)

router = APIRouter(prefix="/measurement-instruments", tags=["Средства измерения"])


@router.get("/", response_model=List[MeasurementInstrumentRead])
def get_instruments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Любой авторизованный
    skip: int = 0,
    limit: int = 100,
    type_id: Optional[int] = None
):
    """
    Получить список всех средств измерения
    Можно фильтровать по типу
    """
    query = db.query(MeasurementInstrument)
    
    if type_id:
        query = query.filter(MeasurementInstrument.id_type_instrument == type_id)
    
    instruments = query.offset(skip).limit(limit).all()
    return instruments


@router.get("/{instrument_id}", response_model=MeasurementInstrumentRead)
def get_instrument(
    instrument_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Любой авторизованный
):
    """
    Получить средство измерения по ID
    """
    instrument = db.query(MeasurementInstrument).filter(
        MeasurementInstrument.id == instrument_id
    ).first()
    
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Средство измерения не найдено"
        )
    return instrument


@router.post("/", response_model=MeasurementInstrumentRead, status_code=status.HTTP_201_CREATED)
def create_instrument(
    instrument_data: MeasurementInstrumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Создать новое средство измерения (только для администратора)
    """
    # Проверка уникальности серийного номера
    existing = db.query(MeasurementInstrument).filter(
        MeasurementInstrument.serial_number == instrument_data.serial_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Средство измерения с таким серийным номером уже существует"
        )
    
    # Проверка существования типа
    type_obj = db.query(MeasurementType).filter(
        MeasurementType.id == instrument_data.id_type_instrument
    ).first()
    
    if not type_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Указанный тип не существует"
        )
    
    db_instrument = MeasurementInstrument(
        serial_number=instrument_data.serial_number,
        date_admission=instrument_data.date_admission,
        id_type_instrument=instrument_data.id_type_instrument
    )
    
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    
    return db_instrument


@router.put("/{instrument_id}", response_model=MeasurementInstrumentRead)
def update_instrument(
    instrument_id: int,
    instrument_data: MeasurementInstrumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Обновить средство измерения (только для администратора)
    """
    instrument = db.query(MeasurementInstrument).filter(
        MeasurementInstrument.id == instrument_id
    ).first()
    
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Средство измерения не найдено"
        )
    
    # Проверка серийного номера на уникальность, если меняется
    if instrument_data.serial_number and instrument_data.serial_number != instrument.serial_number:
        existing = db.query(MeasurementInstrument).filter(
            MeasurementInstrument.serial_number == instrument_data.serial_number
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Средство измерения с таким серийным номером уже существует"
            )
    
    # Проверка типа, если меняется
    if instrument_data.id_type_instrument:
        type_obj = db.query(MeasurementType).filter(
            MeasurementType.id == instrument_data.id_type_instrument
        ).first()
        
        if not type_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Указанный тип не существует"
            )
    
    update_data = instrument_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(instrument, field, value)
    
    db.commit()
    db.refresh(instrument)
    
    return instrument


@router.delete("/{instrument_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instrument(
    instrument_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Удалить средство измерения (только для администратора)
    """
    instrument = db.query(MeasurementInstrument).filter(
        MeasurementInstrument.id == instrument_id
    ).first()
    
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Средство измерения не найдено"
        )
    
    # Проверка на связанные поверки
    if instrument.verifications:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить средство измерения, у которого есть поверки"
        )
    
    db.delete(instrument)
    db.commit()
    
    return None


@router.get("/{instrument_id}/verifications", response_model=List[dict])
def get_instrument_verifications(
    instrument_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить историю поверок средства измерения
    """
    instrument = db.query(MeasurementInstrument).filter(
        MeasurementInstrument.id == instrument_id
    ).first()
    
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Средство измерения не найдено"
        )
    
    # Используем прямой SQL для сложного запроса
    result = db.execute(
        text("""
        SELECT 
            v."ID",
            v."Real_Date_Verification",
            v."Valid_Until",
            tv."Type_Name" as verification_type,
            rv."Result_Name" as result,
            u."Surname" || ' ' || u."Name" as metrologist
        FROM "Verification" v
        LEFT JOIN "Type_Verification" tv ON v."ID_Type" = tv."ID"
        LEFT JOIN "Result_Verification" rv ON v."ID_Result" = rv."ID"
        LEFT JOIN "User" u ON v."ID_Metrologist" = u."ID"
        WHERE v."ID_Instrument" = :instrument_id
        ORDER BY v."Real_Date_Verification" DESC
        """),
        {"instrument_id": instrument_id}
    ).fetchall()
    
    return [dict(row._mapping) for row in result]