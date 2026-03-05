from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.reference_device import ReferenceDevice
from schemas.reference_device import (
    ReferenceDeviceRead, 
    ReferenceDeviceCreate, 
    ReferenceDeviceUpdate
)

router = APIRouter(prefix="/reference-devices", tags=["Эталонные средства измерения"])


@router.get("/", response_model=List[ReferenceDeviceRead])
def get_reference_devices(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),  # Любой авторизованный
    skip: int = 0,
    limit: int = 100,
    valid_only: bool = False
):
    """
    Получить список всех эталонных средств измерения
    Можно фильтровать только валидные на текущую дату
    """
    query = db.query(ReferenceDevice)
    
    if valid_only:
        today = date.today()
        query = query.filter(ReferenceDevice.valid_for >= today)
    
    devices = query.offset(skip).limit(limit).all()
    return devices

@router.get("/{device_id}", response_model=ReferenceDeviceRead)
def get_reference_device(
    device_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Получить эталон по ID
    """
    device = db.query(ReferenceDevice).filter(ReferenceDevice.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Эталон не найден"
        )
    return device


@router.post("/", response_model=ReferenceDeviceRead, status_code=status.HTTP_201_CREATED)
def create_reference_device(
    device_data: ReferenceDeviceCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Создать новый эталон (только для администратора)
    """
    # Проверка уникальности серийного номера
    existing = db.query(ReferenceDevice).filter(
        ReferenceDevice.serial_number == device_data.serial_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Эталон с таким серийным номером уже существует"
        )
    
    # Проверка дат
    if device_data.valid_for <= device_data.date_admission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Дата окончания срока должна быть позже даты поступления"
        )
    
    db_device = ReferenceDevice(
        serial_number=device_data.serial_number,
        date_admission=device_data.date_admission,
        valid_for=device_data.valid_for
    )
    
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    
    return db_device


@router.put("/{device_id}", response_model=ReferenceDeviceRead)
def update_reference_device(
    device_id: int,
    device_data: ReferenceDeviceUpdate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Обновить эталон (только для администратора)
    """
    device = db.query(ReferenceDevice).filter(ReferenceDevice.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Эталон не найден"
        )
    
    # Проверка серийного номера на уникальность, если меняется
    if device_data.serial_number and device_data.serial_number != device.serial_number:
        existing = db.query(ReferenceDevice).filter(
            ReferenceDevice.serial_number == device_data.serial_number
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Эталон с таким серийным номером уже существует"
            )
    
    update_data = device_data.model_dump(exclude_unset=True)
    
    # Проверка дат, если обе даты обновляются
    if "date_admission" in update_data and "valid_for" in update_data:
        if update_data["valid_for"] <= update_data["date_admission"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Дата окончания срока должна быть позже даты поступления"
            )
    
    for field, value in update_data.items():
        setattr(device, field, value)
    
    db.commit()
    db.refresh(device)
    
    return device


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reference_device(
    device_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Удалить эталон (только для администратора)
    """
    device = db.query(ReferenceDevice).filter(ReferenceDevice.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Эталон не найден"
        )
    
    # Проверка на связанные TestingInstrument
    if device.testing_instruments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить эталон, который использовался в поверках"
        )
    
    db.delete(device)
    db.commit()
    
    return None


@router.get("/{device_id}/usage", response_model=List[dict])
def get_device_usage(
    device_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Получить историю использования эталона в поверках
    """
    device = db.query(ReferenceDevice).filter(ReferenceDevice.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Эталон не найден"
        )
    
    result = db.execute(
        text("""
        SELECT 
            v."ID",
            v."Real_Date_Verification",
            i."Serial_Number" as instrument_serial,
            tv."Type_Name" as verification_type
        FROM "Testing_Instrument" ti
        JOIN "Verification" v ON ti."ID_Verification" = v."ID"
        JOIN "Instrument_Measurement" i ON v."ID_Instrument" = i."ID"
        LEFT JOIN "Type_Verification" tv ON v."ID_Type" = tv."ID"
        WHERE ti."ID_Reference_Instrument" = :device_id
        ORDER BY v."Real_Date_Verification" DESC
        """),
        {"device_id": device_id}
    ).fetchall()
    
    return [dict(row._mapping) for row in result]