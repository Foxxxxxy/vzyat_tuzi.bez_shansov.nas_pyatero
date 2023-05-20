from sqlalchemy import Column, Integer, String, Float

from app.src.database.database import Base


class DistrictModel(Base):
    __tablename__ = 'district'

    id = Column(Integer, primary_key=True, index=True)
    average_price_rub = Column(Float)
    name = Column(String, unique=True)