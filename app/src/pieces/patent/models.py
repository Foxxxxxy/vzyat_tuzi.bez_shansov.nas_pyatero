from sqlalchemy import Column, Integer, String, Float

from app.src.database.database import Base


class PatentModel(Base):
    __tablename__ = 'patent'

    id = Column(Integer, primary_key=True, index=True)
    percent_rate = Column(Float)
    income_rub = Column(Float)
    name = Column(String, unique=True)
    price = Column(Float)
