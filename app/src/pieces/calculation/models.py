from enum import Enum

from sqlalchemy import Column, Integer, String, Float

from app.src.database.database import Base


class LegalEntityType(str, Enum):
    OOO_AO = 'OOO_AO'
    IP = 'IP'

# todo - it will be a model that stores calculation results. It will have its own api like /calculation/{calculation_id}
# class CalculationModel(Base):
#     __tablename__ = "calculation"
#
#     id = Column(Integer, primary_key=True, index=True)
#     # foreign key user id
