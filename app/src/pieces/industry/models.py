from sqlalchemy import Column, Integer, String, Float

from app.src.database.database import Base


class IndustryModel(Base):
    __tablename__ = "industry"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    avg_salary = Column(Float)
