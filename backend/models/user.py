from sqlalchemy import Boolean, String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    """Модель пользователя"""
    __tablename__ = "User"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    surname = Column("Surname", String(100), nullable=False)
    name = Column("Name", String(100), nullable=False)
    patronymic = Column("Patronymic", String(100), nullable=True)
    admin_role = Column("Admin_Role", Boolean, nullable=False, default=False)
    hashed_password = Column("Hashed_Password", String(100), nullable=False)
    login = Column("Login", String(100), nullable=False, unique=True)
    
    # Связи
    verifications = relationship("Verification", back_populates="metrologist")
    
    def __repr__(self):
        return f"<User {self.surname} {self.name}>"