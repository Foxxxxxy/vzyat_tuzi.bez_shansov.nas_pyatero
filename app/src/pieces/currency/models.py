from sqlalchemy import Column, Integer, String, Float

from app.src.database.database import Base


class CurrencyModel(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    value = Column(Float)

