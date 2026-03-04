from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class TestingInstrument(Base):
    """Связь поверки и эталонов"""
    __tablename__ = "Testing_Instrument"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    id_verification = Column("ID_Verification", Integer, ForeignKey("Verification.ID"), nullable=False)
    id_reference_instrument = Column("ID_Reference_Instrument", Integer, ForeignKey("Reference_Instrument_Measurement.ID"), nullable=False)
    
    # Связи
    verification = relationship("Verification", back_populates="testing_instruments")
    reference_device = relationship("ReferenceDevice", back_populates="testing_instruments")