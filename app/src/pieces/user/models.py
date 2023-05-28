from sqlalchemy import Column, Integer, String

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
