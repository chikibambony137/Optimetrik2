from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base

class VerificationType(Base):
    """Тип поверки"""
    __tablename__ = "Type_Verification"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    type_name = Column("Type_Name", String(30), nullable=False)
    
    # Связи
    verifications = relationship("Verification", back_populates="type")
    
    def __repr__(self):
        return f"<VerificationType {self.type_name}>"