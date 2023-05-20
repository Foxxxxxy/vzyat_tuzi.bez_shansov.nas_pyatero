from enum import Enum

from sqlalchemy import Column, Integer, String, Float

from app.src.database.database import Base


class AdditionalServiceModel(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True, index=True)
    average_price_dollar = Column(Float)
    name = Column(String, unique=True)