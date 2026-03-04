from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base

class MeasurementType(Base):
    """Тип средства измерения"""
    __tablename__ = "Type_Instrument_Measurement"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    name_company = Column("Name_Company", String, nullable=False)
    batch_number = Column("Batch_Number", String, nullable=False)
    
    # Связи
    instruments = relationship("MeasurementInstrument", back_populates="type")
    
    def __repr__(self):
        return f"<MeasurementType {self.name_company} {self.batch_number}>"