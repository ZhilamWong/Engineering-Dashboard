from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    temperature = Column(Float, nullable=False)

class BatteryReading(Base):
    __tablename__ = "battery_readings"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    charge_percent = Column(Float, nullable=False)
    is_charging = Column(Boolean, nullable=False)