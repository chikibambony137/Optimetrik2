from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class TestToolVerification(Base):
    """Связь поверки и тестовых стендов"""
    __tablename__ = "Test_Tool_Verification"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    id_verification = Column("ID_Verification", Integer, ForeignKey("Verification.ID"), nullable=False)
    id_test_tool = Column("ID_Test_Tool", Integer, ForeignKey("Test_tool.ID"), nullable=False)
    
    # Связи
    verification = relationship("Verification", back_populates="test_tool_verifications")
    test_tool = relationship("TestTool", back_populates="test_tool_verifications")