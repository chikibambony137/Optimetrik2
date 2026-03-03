from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/measurement_instruments",
    tags=["Средства измерения"]
)


@router.get("/")
def get_instruments(

):
    """
    Получить список всех средств измерения
    """
    return 'ok'

