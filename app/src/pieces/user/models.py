from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.src.database.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    hashed_password = Column(String)

    email = Column(String, unique=True, index=True)
    name = Column(String)
    last_name = Column(String)
    organisation_name = Column(String)
    inn = Column(String)  # todo validation
    web_site = Column(String)

    fathers_name = Column(String)
    industry_id = Column(Integer, ForeignKey("industry.id"), nullable=True)
    country = Column(String)
    city = Column(String)
    position = Column(String)

    industry = relationship("IndustryModel")
