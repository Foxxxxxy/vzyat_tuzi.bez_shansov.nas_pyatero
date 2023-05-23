from enum import Enum

from sqlalchemy import Column, Integer, String, Float

from app.src.database.database import Base


class BuildingModel(Base):
    __tablename__ = 'building'

    id = Column(Integer, primary_key=True, index=True)
    average_price_rub = Column(Float)
    name = Column(String, unique=True)
