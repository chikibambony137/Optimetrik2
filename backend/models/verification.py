from sqlalchemy import Date, Numeric, Boolean, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Verification(Base):
    """Поверка"""
    __tablename__ = "Verification"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    planned_date_verification = Column("Planned_Date_Verification", Date, nullable=False)
    date_receipt = Column("Date_Receipt", Date, nullable=False)
    temperature = Column("Temperature", Numeric(5,2))
    pressure = Column("Pressure", Numeric(10,2))
    wetness = Column("Wetness", Numeric(5,2))
    complete_electric_test = Column("Complete_Electric_test", Boolean)
    complete_voltage_test = Column("Complete_Voltage_test", Boolean)
    complete_isolation_test = Column("Complete_Isolation_test", Boolean)
    id_result = Column("ID_Result", Integer, ForeignKey("Result_Verification.ID"))
    real_date_verification = Column("Real_Date_Verification", Date)
    valid_until = Column("Valid_Until", Date)
    id_type = Column("ID_Type", Integer, ForeignKey("Type_Verification.ID"))
    id_metrologist = Column("ID_Metrologist", Integer, ForeignKey("User.ID"))
    id_instrument = Column("ID_Instrument", Integer, ForeignKey("Instrument_Measurement.ID"))
    
    # Связи
    result = relationship("ResultVerification")
    type = relationship("VerificationType")
    metrologist = relationship("User", back_populates="verifications")
    instrument = relationship("MeasurementInstrument", back_populates="verifications")
    testing_instruments = relationship("TestingInstrument", back_populates="verification")
    test_tool_verifications = relationship("TestToolVerification", back_populates="verification")