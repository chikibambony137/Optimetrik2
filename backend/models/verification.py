from sqlalchemy import Date, Numeric, Boolean, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Verification(Base):
    """Поверка"""
    __tablename__ = "Verification"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    planned_date_verification = Column("Planned_Date_Verification", Date, nullable=False)
    date_receipt = Column("Date_Receipt", Date, nullable=False)
    temperature = Column("Temperature", Numeric(5,2), nullable=False)
    pressure = Column("Pressure", Numeric(10,2), nullable=False)
    wetness = Column("Wetness", Numeric(5,2), nullable=False)
    complete_electric_test = Column("Complete_Electric_test", Boolean, nullable=False)
    complete_voltage_test = Column("Complete_Voltage_test", Boolean, nullable=False)
    complete_isolation_test = Column("Complete_Isolation_test", Boolean, nullable=False)
    id_result = Column("ID_Result", Integer, ForeignKey("Result_Verification.ID"), nullable=False)
    real_date_verification = Column("Real_Date_Verification", Date, nullable=False)
    valid_until = Column("Valid_Until", Date, nullable=False)
    id_type = Column("ID_Type", Integer, ForeignKey("Type_Verification.ID"), nullable=False)
    id_metrologist = Column("ID_Metrologist", Integer, ForeignKey("User.ID"), nullable=False)
    id_instrument = Column("ID_Instrument", Integer, ForeignKey("Instrument_Measurement.ID"), nullable=False)
    
    # Связи
    result = relationship("ResultVerification")
    type = relationship("VerificationType")
    metrologist = relationship("User", back_populates="verifications")
    instrument = relationship("MeasurementInstrument", back_populates="verifications")
    testing_instruments = relationship("TestingInstrument", back_populates="verification")
    test_tool_verifications = relationship("TestToolVerification", back_populates="verification")