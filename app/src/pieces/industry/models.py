from sqlalchemy import Column, Integer, String

from app.src.database.database import Base


class IndustryModel(Base):
    __tablename__ = "industry"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
