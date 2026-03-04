# from typing import List
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from api.dependencies import get_db, get_current_user
# from crud.measurement_instrument import crud_measurement_instrument
# from schemas.measurement_instrument import (
#     MeasurementInstrumentCreate, 
#     MeasurementInstrumentUpdate, 
#     MeasurementInstrumentInDB
# )
# from app.models.user import User

# router = APIRouter(prefix="/measurement_instruments", tags=["Средства измерения"])

# @router.get("/", response_model=List[MeasurementInstrumentInDB])
# def read_instruments(
#     db: Session = Depends(get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: User = Depends(get_current_user)
# ):
#     """Получить список всех средств измерения"""
#     instruments = crud_measurement_instrument.get_multi(db, skip=skip, limit=limit)
#     return instruments

# # ... остальные эндпоинты