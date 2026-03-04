from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base

class ResultVerification(Base):
    """Результат поверки"""
    __tablename__ = "Result_Verification"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    result_name = Column("Result_Name", String, nullable=False)
    
    # Связи
    verifications = relationship("Verification", back_populates="result")
    
    def __repr__(self):
        return f"<ResultVerification {self.result_name}>"