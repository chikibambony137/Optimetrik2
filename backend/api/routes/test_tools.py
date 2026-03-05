from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.test_tool import TestTool
from models.user import User
from schemas.test_tool import (
    TestToolRead, 
    TestToolCreate, 
    TestToolUpdate
)

router = APIRouter(prefix="/test-tools", tags=["Тестовые стенды"])


@router.get("/", response_model=List[TestToolRead])
def get_test_tools(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),  # Раскомментировал
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False
):
    """
    Получить список всех тестовых стендов
    Можно фильтровать только активные
    """
    query = db.query(TestTool)
    
    if active_only:
        query = query.filter(TestTool.active == True)
    
    tools = query.offset(skip).limit(limit).all()
    return tools


@router.get("/active", response_model=List[TestToolRead])
def get_active_test_tools(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)  # Раскомментировал
):
    """
    Получить только активные тестовые стенды
    """
    tools = db.query(TestTool).filter(TestTool.active == True).all()
    return tools


@router.get("/{tool_id}", response_model=TestToolRead)
def get_test_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)  # Раскомментировал
):
    """
    Получить тестовый стенд по ID
    """
    tool = db.query(TestTool).filter(TestTool.id == tool_id).first()
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тестовый стенд не найден"
        )
    return tool


@router.post("/", response_model=TestToolRead, status_code=status.HTTP_201_CREATED)
def create_test_tool(
    tool_data: TestToolCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Раскомментировал, только админ
):
    """
    Создать новый тестовый стенд (только для администратора)
    """
    # Проверка уникальности серийного номера
    existing = db.query(TestTool).filter(
        TestTool.serial_number == tool_data.serial_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тестовый стенд с таким серийным номером уже существует"
        )
    
    db_tool = TestTool(
        serial_number=tool_data.serial_number,
        active=tool_data.active
    )
    
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    
    return db_tool


@router.put("/{tool_id}", response_model=TestToolRead)
def update_test_tool(
    tool_id: int,
    tool_data: TestToolUpdate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Раскомментировал, только админ
):
    """
    Обновить тестовый стенд (только для администратора)
    """
    tool = db.query(TestTool).filter(TestTool.id == tool_id).first()
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тестовый стенд не найден"
        )
    
    # Проверка серийного номера на уникальность, если меняется
    if tool_data.serial_number and tool_data.serial_number != tool.serial_number:
        existing = db.query(TestTool).filter(
            TestTool.serial_number == tool_data.serial_number
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Тестовый стенд с таким серийным номером уже существует"
            )
    
    update_data = tool_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tool, field, value)
    
    db.commit()
    db.refresh(tool)
    
    return tool


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Раскомментировал, только админ
):
    """
    Удалить тестовый стенд (только для администратора)
    """
    tool = db.query(TestTool).filter(TestTool.id == tool_id).first()
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тестовый стенд не найден"
        )
    
    # Проверка на связанные TestToolVerification
    if tool.test_tool_verifications:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить стенд, который использовался в поверках"
        )
    
    db.delete(tool)
    db.commit()
    
    return None


@router.patch("/{tool_id}/toggle", response_model=TestToolRead)
def toggle_test_tool_active(
    tool_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Раскомментировал, только админ
):
    """
    Переключить статус активности стенда (только для администратора)
    """
    tool = db.query(TestTool).filter(TestTool.id == tool_id).first()
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тестовый стенд не найден"
        )
    
    tool.active = not tool.active
    db.commit()
    db.refresh(tool)
    
    return tool


@router.get("/{tool_id}/verifications", response_model=List[dict])
def get_tool_verifications(
    tool_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)  # Раскомментировал
):
    """
    Получить все поверки, проведенные на данном стенде
    """
    tool = db.query(TestTool).filter(TestTool.id == tool_id).first()
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тестовый стенд не найден"
        )
    
    result = db.execute(
        text("""
            SELECT 
                v."ID",
                v."Real_Date_Verification",
                i."Serial_Number" as instrument_serial,
                tv."Type_Name" as verification_type,
                rv."Result_Name" as result,
                u."Surname" || ' ' || u."Name" as metrologist
            FROM "Test_Tool_Verification" ttv
            JOIN "Verification" v ON ttv."ID_Verification" = v."ID"
            JOIN "Instrument_Measurement" i ON v."ID_Instrument" = i."ID"
            LEFT JOIN "Type_Verification" tv ON v."ID_Type" = tv."ID"
            LEFT JOIN "Result_Verification" rv ON v."ID_Result" = rv."ID"
            LEFT JOIN "User" u ON v."ID_Metrologist" = u."ID"
            WHERE ttv."ID_Test_Tool" = :tool_id
            ORDER BY v."Real_Date_Verification" DESC
        """),
        {"tool_id": tool_id}
    ).fetchall()
    
    return [dict(row._mapping) for row in result]


@router.get("/{tool_id}/stats", response_model=dict)
def get_tool_stats(
    tool_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Получить статистику использования стенда
    """
    tool = db.query(TestTool).filter(TestTool.id == tool_id).first()
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тестовый стенд не найден"
        )
    
    # Общее количество использований
    total = db.execute(
        text("SELECT COUNT(*) FROM \"Test_Tool_Verification\" WHERE \"ID_Test_Tool\" = :tool_id"),
        {"tool_id": tool_id}
    ).scalar()
    
    # Последнее использование
    last = db.execute(
        text("""
            SELECT v."Real_Date_Verification"
            FROM "Test_Tool_Verification" ttv
            JOIN "Verification" v ON ttv."ID_Verification" = v."ID"
            WHERE ttv."ID_Test_Tool" = :tool_id
            ORDER BY v."Real_Date_Verification" DESC
            LIMIT 1
        """),
        {"tool_id": tool_id}
    ).scalar()
    
    return {
        "tool_id": tool_id,
        "serial_number": tool.serial_number,
        "active": tool.active,
        "total_uses": total or 0,
        "last_used": last
    }