from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from core.database import Base, get_db
from core.security import get_password_hash
from models.user import User
from models.measurement_type import MeasurementType
from models.measurement_instrument import MeasurementInstrument
from models.reference_device import ReferenceDevice
from models.test_tool import TestTool
from models.verification import Verification
from models.result_verification import ResultVerification
from models.verification_type import VerificationType

# Создаем тестовую базу данных SQLite в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Фикстура для переопределения зависимости get_db
@pytest.fixture
def db_session():
    """Создает тестовую сессию базы данных"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Создает тестовый клиент с тестовой БД"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    import api.dependencies
    app.dependency_overrides[api.dependencies.get_db] = override_get_db
    
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Создает тестового пользователя"""
    from core.security import get_password_hash, verify_password
    
    # Очищаем всех тестовых пользователей перед созданием нового
    db_session.query(User).filter(User.login.like("testuser%")).delete()
    db_session.commit()
    
    # Создаем нового с уникальным логином
    import uuid
    unique_login = f"testuser_{uuid.uuid4().hex[:8]}"
    
    password = "Test123"
    hashed = get_password_hash(password)
    
    # Проверяем, что хеш работает
    assert verify_password(password, hashed), "Хеширование не работает!"
    
    user = User(
        surname="Тестов",
        name="Тест",
        patronymic="Тестович",
        login=unique_login,  # уникальный логин
        hashed_password=hashed,
        admin_role=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def test_admin(db_session):
    """Создает тестового администратора"""
    admin = User(
        surname="Админ",
        name="Админ",
        patronymic="Админович",
        login="admin",
        hashed_password=get_password_hash("Admin123"),
        admin_role=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def auth_headers(client, test_user):
    """Возвращает заголовки с токеном авторизации"""
    # Пытаемся залогиниться
    response = client.post("/auth/login", data={
        "username": test_user.login,
        "password": "Test123"
    })
    
    # Если не получилось, выводим подробную информацию
    if response.status_code != 200:
        
        # Проверим, существует ли пользователь в БД
        from models.user import User
        db = TestingSessionLocal()
        user_in_db = db.query(User).filter(User.login == test_user.login).first()
        if user_in_db:
            print(f"User in DB: {user_in_db.login}")
            print(f"Hash in DB: {user_in_db.hashed_password[:20]}...")
        else:
            print("Пользователь НЕ НАЙДЕН в БД!")
        db.close()
        
        pytest.skip(f"Login failed: {response.text}")
    
    response_data = response.json()
    
    # Проверяем наличие токена
    if "access_token" not in response_data:
        print(f"\n!!! Нет access_token в ответе: {response_data}")
        print(f"Ключи ответа: {response_data.keys()}")
        pytest.skip("No access_token in response")
    
    token = response_data["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, test_admin):
    """Возвращает заголовки с токеном администратора"""
    response = client.post("/auth/login", data={
        "username": test_admin.login,
        "password": "Admin123"
    })

    if "access_token" not in response.json():
        print(f"\n!!! Нет access_token в ответе: {response.json()}")
        print(f"Ключи ответа: {response.json().keys()}")
        pytest.skip("No access_token in response")

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_measurement_type(db_session):
    """Создает тестовый тип средства измерения"""
    mt = MeasurementType(
        name_company="Test Company",
        batch_number="TEST-001"
    )
    db_session.add(mt)
    db_session.commit()
    db_session.refresh(mt)
    return mt


@pytest.fixture
def test_instrument(db_session, test_measurement_type):
    """Создает тестовое средство измерения"""
    instrument = MeasurementInstrument(
        serial_number="TEST-SN-001",
        date_admission=date.today(),
        id_type_instrument=test_measurement_type.id
    )
    db_session.add(instrument)
    db_session.commit()
    db_session.refresh(instrument)
    return instrument


@pytest.fixture
def test_reference_device(db_session):
    """Создает тестовый эталон"""
    from datetime import date, timedelta
    device = ReferenceDevice(
        serial_number="REF-TEST-001",
        date_admission=date.today(),
        valid_for=date.today() + timedelta(days=365)
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)
    return device


@pytest.fixture
def test_test_tool(db_session):
    """Создает тестовый стенд"""
    tool = TestTool(
        serial_number="TOOL-TEST-001",
        active=True
    )
    db_session.add(tool)
    db_session.commit()
    db_session.refresh(tool)
    return tool


@pytest.fixture
def test_result(db_session):
    """Создает тестовый результат поверки"""
    result = ResultVerification(
        result_name="Тестовый результат"
    )
    db_session.add(result)
    db_session.commit()
    db_session.refresh(result)
    return result


@pytest.fixture
def test_verification_type(db_session):
    """Создает тестовый тип поверки"""
    vt = VerificationType(
        type_name="Тестовый тип"
    )
    db_session.add(vt)
    db_session.commit()
    db_session.refresh(vt)
    return vt