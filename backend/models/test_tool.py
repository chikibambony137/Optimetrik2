from sqlalchemy import Boolean, String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base

class TestTool(Base):
    """Тестовый стенд"""
    __tablename__ = "Test_tool"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    serial_number = Column("Serial_Number", String, nullable=False, unique=True)
    active = Column("Active", Boolean, nullable=False, default=True)
    
    # Связи
    test_tool_verifications = relationship("TestToolVerification", back_populates="test_tool")
    
    def __repr__(self):
        return f"<TestTool {self.serial_number}>"