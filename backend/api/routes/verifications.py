from typing import List, Optional
from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, and_

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.verification import Verification
from models.user import User
from models.measurement_instrument import MeasurementInstrument
from models.reference_device import ReferenceDevice
from models.test_tool import TestTool
from models.testing_instrument import TestingInstrument
from models.test_tool_verification import TestToolVerification
from schemas.verification import (
    VerificationRead,
    VerificationCreate,
    VerificationUpdate,
    VerificationTestData,
    VerificationComplete,
    VerificationDetailRead,
    VerificationListRead,
    VerificationWithRelations
)

router = APIRouter(prefix="/verifications", tags=["Поверки"])


@router.get("/", response_model=List[VerificationListRead])
def get_verifications(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    instrument_id: Optional[int] = None,
    metrologist_id: Optional[int] = None
):
    """
    Получить список поверок с фильтрацией
    """
    query = db.execute(
        text("""
            SELECT 
                v."ID" as id,
                v."Planned_Date_Verification" as planned_date_verification,
                v."Real_Date_Verification" as real_date_verification,
                i."Serial_Number" as instrument_serial,
                rv."Result_Name" as result_name,
                tv."Type_Name" as type_name,
                u."Surname" || ' ' || u."Name" as metrologist_name,
                CASE WHEN v."Real_Date_Verification" IS NOT NULL THEN true ELSE false END as is_completed
            FROM "Verification" v
            JOIN "Instrument_Measurement" i ON v."ID_Instrument" = i."ID"
            LEFT JOIN "Result_Verification" rv ON v."ID_Result" = rv."ID"
            LEFT JOIN "Type_Verification" tv ON v."ID_Type" = tv."ID"
            LEFT JOIN "User" u ON v."ID_Metrologist" = u."ID"
            WHERE 1=1
                {completed_filter}
                {date_filter}
                {instrument_filter}
                {metrologist_filter}
            ORDER BY v."Planned_Date_Verification" DESC
            LIMIT :limit OFFSET :skip
        """.format(
            completed_filter="AND v.\"Real_Date_Verification\" IS NOT NULL" if completed is True else 
                           "AND v.\"Real_Date_Verification\" IS NULL" if completed is False else "",
            date_filter="AND v.\"Planned_Date_Verification\" BETWEEN :from_date AND :to_date" if from_date and to_date else "",
            instrument_filter="AND v.\"ID_Instrument\" = :instrument_id" if instrument_id else "",
            metrologist_filter="AND v.\"ID_Metrologist\" = :metrologist_id" if metrologist_id else ""
        )),
        {
            "skip": skip,
            "limit": limit,
            "from_date": from_date,
            "to_date": to_date,
            "instrument_id": instrument_id,
            "metrologist_id": metrologist_id
        }
    ).fetchall()
    
    return [dict(row._mapping) for row in query]


@router.get("/{verification_id}", response_model=VerificationDetailRead)
def get_verification(
    verification_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Получить детальную информацию о поверке по ID
    """
    # Основная информация о поверке
    verification = db.query(Verification).filter(Verification.id == verification_id).first()
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Поверка не найдена"
        )
    
    # Получаем расширенную информацию через SQL
    result = db.execute(
        text("""
            SELECT 
                v."ID" as id,
                v."Planned_Date_Verification" as planned_date_verification,
                v."Date_Receipt" as date_receipt,
                v."Temperature" as temperature,
                v."Pressure" as pressure,
                v."Wetness" as wetness,
                v."Complete_Electric_test" as complete_electric_test,
                v."Complete_Voltage_test" as complete_voltage_test,
                v."Complete_Isolation_test" as complete_isolation_test,
                v."ID_Result" as id_result,
                v."Real_Date_Verification" as real_date_verification,
                v."Valid_Until" as valid_until,
                v."ID_Type" as id_type,
                v."ID_Metrologist" as id_metrologist,
                v."ID_Instrument" as id_instrument,
                rv."Result_Name" as result_name,
                tv."Type_Name" as type_name,
                u."Surname" || ' ' || u."Name" || ' ' || COALESCE(u."Patronymic", '') as metrologist_name,
                i."Serial_Number" as instrument_serial
            FROM "Verification" v
            LEFT JOIN "Result_Verification" rv ON v."ID_Result" = rv."ID"
            LEFT JOIN "Type_Verification" tv ON v."ID_Type" = tv."ID"
            LEFT JOIN "User" u ON v."ID_Metrologist" = u."ID"
            JOIN "Instrument_Measurement" i ON v."ID_Instrument" = i."ID"
            WHERE v."ID" = :vid
        """),
        {"vid": verification_id}
    ).first()
    
    # Получаем использованные стенды
    test_tools = db.execute(
        text("""
            SELECT tb."ID", tb."Serial_Number", tb."Active"
            FROM "Test_Tool_Verification" ttv
            JOIN "Test_tool" tb ON ttv."ID_Test_Tool" = tb."ID"
            WHERE ttv."ID_Verification" = :vid
        """),
        {"vid": verification_id}
    ).fetchall()
    
    # Получаем использованные эталоны
    reference_devices = db.execute(
        text("""
            SELECT rd."ID", rd."Serial_Number", rd."Valid_For"
            FROM "Testing_Instrument" ti
            JOIN "Reference_Instrument_Measurement" rd ON ti."ID_Reference_Instrument" = rd."ID"
            WHERE ti."ID_Verification" = :vid
        """),
        {"vid": verification_id}
    ).fetchall()
    
    result_dict = dict(result._mapping)
    result_dict["test_tools"] = [dict(tb._mapping) for tb in test_tools]
    result_dict["reference_devices"] = [dict(rd._mapping) for rd in reference_devices]
    
    return result_dict


@router.post("/", response_model=VerificationRead, status_code=status.HTTP_201_CREATED)
def create_verification(
    verification_data: VerificationCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Создать новую поверку (только планируемая дата и дата поступления)
    """
    # Проверяем существование прибора
    instrument = db.query(MeasurementInstrument).filter(
        MeasurementInstrument.id == verification_data.id_instrument
    ).first()
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Средство измерения не найдено"
        )
    
    db_verification = Verification(
        planned_date_verification=verification_data.planned_date_verification,
        date_receipt=verification_data.date_receipt,
        id_instrument=verification_data.id_instrument,
        # Заполняем обязательные поля значениями по умолчанию
        temperature=0,  # или другое значение по умолчанию
        pressure=0,
        wetness=0,
        complete_electric_test=False,
        complete_voltage_test=False,
        complete_isolation_test=False,
        id_result=6,  # например, "Не завершено"
        real_date_verification=None,  # это поле может быть NULL
        valid_until=None,  # это поле может быть NULL
        id_type=1,  # значение по умолчанию
        id_metrologist=1  # значение по умолчанию или current_user.id
    )
    
    db.add(db_verification)
    db.commit()
    db.refresh(db_verification)
    
    return db_verification

@router.put("/{verification_id}/test-data", response_model=VerificationRead)
def fill_test_data(
    verification_id: int,
    test_data: VerificationTestData,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Заполнить данные тестирования для поверки
    """
    verification = db.query(Verification).filter(Verification.id == verification_id).first()
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Поверка не найдена"
        )
    
    # Проверяем, что поверка еще не завершена
    if verification.real_date_verification is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя изменить завершенную поверку"
        )
    
    # Проверяем валидность эталонов на текущую дату
    today = date.today()
    for ref_id in test_data.id_reference_devices:
        ref_device = db.query(ReferenceDevice).filter(
            ReferenceDevice.id == ref_id,
            ReferenceDevice.valid_for >= today
        ).first()
        if not ref_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Эталон с ID {ref_id} не валиден на текущую дату"
            )
    
    # Проверяем активность стендов
    for tool_id in test_data.id_test_tools:
        tool = db.query(TestTool).filter(
            TestTool.id == tool_id,
            TestTool.active == True
        ).first()
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Стенд с ID {tool_id} не активен"
            )
    
    # Обновляем данные поверки
    verification.temperature = test_data.temperature
    verification.pressure = test_data.pressure
    verification.wetness = test_data.wetness
    verification.complete_electric_test = test_data.complete_electric_test
    verification.complete_voltage_test = test_data.complete_voltage_test
    verification.complete_isolation_test = test_data.complete_isolation_test
    
    db.commit()
    
    # Добавляем связи со стендами
    for tool_id in test_data.id_test_tools:
        ttv = TestToolVerification(
            id_verification=verification_id,
            id_test_tool=tool_id
        )
        db.add(ttv)
    
    # Добавляем связи с эталонами
    for ref_id in test_data.id_reference_devices:
        ti = TestingInstrument(
            id_verification=verification_id,
            id_reference_instrument=ref_id
        )
        db.add(ti)
    
    db.commit()
    db.refresh(verification)
    
    return verification


@router.put("/{verification_id}/complete", response_model=VerificationRead)
def complete_verification(
    verification_id: int,
    complete_data: VerificationComplete,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Завершить поверку с автоматическим расчетом дат
    """
    verification = db.query(Verification).filter(Verification.id == verification_id).first()
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Поверка не найдена"
        )
    
    # Проверяем, что все тестовые данные заполнены
    if None in [
        verification.temperature,
        verification.pressure,
        verification.wetness,
        verification.complete_electric_test,
        verification.complete_voltage_test,
        verification.complete_isolation_test
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не все тестовые данные заполнены"
        )
    
    # Проверяем, что есть хотя бы один эталон и стенд
    has_refs = db.query(TestingInstrument).filter(
        TestingInstrument.id_verification == verification_id
    ).first()
    has_tools = db.query(TestToolVerification).filter(
        TestToolVerification.id_verification == verification_id
    ).first()
    
    if not has_refs or not has_tools:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Должны быть указаны эталоны и стенды"
        )
    
    # Рассчитываем даты
    today = date.today()
    
    # Срок действия в зависимости от типа поверки
    if complete_data.id_type == 1:  # Первичная (8 лет - 1 день)
        valid_until = today + timedelta(days=8*365 - 1)
    elif complete_data.id_type == 2:  # Периодическая (4 года - 1 день)
        valid_until = today + timedelta(days=4*365 - 1)
    else:  # Другие типы (по умолчанию 1 год)
        valid_until = today + timedelta(days=365)
    
    # Общий результат (успех если все тесты пройдены)
    all_tests_passed = (
        verification.complete_electric_test and
        verification.complete_voltage_test and
        verification.complete_isolation_test
    )
    
    verification.real_date_verification = today
    verification.valid_until = valid_until
    verification.id_type = complete_data.id_type
    verification.id_result = complete_data.id_result
    verification.id_metrologist = 1 ## current_user.id
    
    db.commit()
    db.refresh(verification)
    
    return verification


@router.delete("/{verification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_verification(
    verification_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Только админ
):
    """
    Удалить поверку (только для администратора)
    """
    verification = db.query(Verification).filter(Verification.id == verification_id).first()
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Поверка не найдена"
        )
    
    # Удаляем связанные записи
    db.execute(
        text("DELETE FROM \"Testing_Instrument\" WHERE \"ID_Verification\" = :vid"),
        {"vid": verification_id}
    )
    db.execute(
        text("DELETE FROM \"Test_Tool_Verification\" WHERE \"ID_Verification\" = :vid"),
        {"vid": verification_id}
    )
    
    db.delete(verification)
    db.commit()
    
    return None


@router.get("/stats/summary", response_model=dict)
def get_verification_stats(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
    year: Optional[int] = None
):
    """
    Получить статистику по поверкам
    """
    if not year:
        year = date.today().year
    
    result = db.execute(
        text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN "Real_Date_Verification" IS NOT NULL THEN 1 END) as completed,
                COUNT(CASE WHEN "Real_Date_Verification" IS NULL THEN 1 END) as pending,
                COUNT(CASE WHEN "ID_Result" = 1 THEN 1 END) as successful,
                COUNT(CASE WHEN "ID_Result" = 2 THEN 1 END) as failed
            FROM "Verification"
            WHERE EXTRACT(YEAR FROM "Planned_Date_Verification") = :year
        """),
        {"year": year}
    ).first()
    
    return dict(result._mapping)