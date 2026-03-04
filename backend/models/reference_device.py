from sqlalchemy import String, Date, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base

class ReferenceDevice(Base):
    """Эталонное средство измерения"""
    __tablename__ = "Reference_Instrument_Measurement"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    serial_number = Column("Serial_Number", String, nullable=False, unique=True)
    date_admission = Column("Date_Admission", Date, nullable=False)
    valid_for = Column("Valid_For", Date, nullable=False)
    
    # Связи
    testing_instruments = relationship("TestingInstrument", back_populates="reference_device")
    
    def __repr__(self):
        return f"<ReferenceDevice {self.serial_number}>"