from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class SensorReadings(Base):
    __tablename__ = "temperature_readings"

    id = Column(Integer, primary_key=True, nullable=False)
    room_location = Column(Text, nullable=False)
    window_start = Column(TIMESTAMP(timezone=True), nullable=False)
    window_end = Column(TIMESTAMP(timezone=True), nullable=False)
    avg_temperature = Column(DOUBLE_PRECISION, nullable=False)
