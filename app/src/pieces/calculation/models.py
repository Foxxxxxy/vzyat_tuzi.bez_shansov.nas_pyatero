import enum

from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY, Enum
from sqlalchemy.orm import relationship

from app.src.database.database import Base

from app.src.pieces.industry.models import IndustryModel
from app.src.pieces.district.models import DistrictModel


class LegalEntityType(str, enum.Enum):
    OOO_AO = 'OOO_AO'
    IP = 'IP'


class RequestModel(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    industry_id = Column(Integer, ForeignKey("industry.id"))
    district_id = Column(Integer, ForeignKey("district.id"))
    employee_amount = Column(Integer)
    building_area_size = Column(Float)
    land_area_size = Column(Float)
    equipment = Column(ARRAY(Integer))
    equipment_amounts = Column(ARRAY(Integer))
    additional_services = Column(ARRAY(Integer))
    legal_entity_type = Column(Enum(LegalEntityType))
    predicted_income_per_year_rub = Column(Float)
    accounting_services_documents_amount = Column(Integer)

    industry = relationship("IndustryModel")
    district = relationship("DistrictModel")
