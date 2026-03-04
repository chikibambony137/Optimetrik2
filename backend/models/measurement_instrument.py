from sqlalchemy import String, Date, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class MeasurementInstrument(Base):
    """Средство измерения"""
    __tablename__ = "Instrument_Measurement"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    serial_number = Column("Serial_Number", String, nullable=False, unique=True)
    date_admission = Column("Date_Admission", Date, nullable=False)
    id_type_instrument = Column("ID_Type_Instrument", Integer, ForeignKey("Type_Instrument_Measurement.ID"), nullable=False)
    
    # Связи
    type = relationship("MeasurementType", back_populates="instruments")
    verifications = relationship("Verification", back_populates="instrument")
    
    def __repr__(self):
        return f"<MeasurementInstrument {self.serial_number}>"