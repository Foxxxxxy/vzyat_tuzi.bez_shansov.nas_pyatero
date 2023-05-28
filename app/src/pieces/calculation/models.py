import enum

from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY, Enum, DateTime
from sqlalchemy.orm import relationship

from app.src.database.database import Base


class LegalEntityType(str, enum.Enum):
    OOO_AO = 'OOO_AO'
    IP = 'IP'


class RequestModel(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    industry_id = Column(Integer, ForeignKey("industry.id"))
    district_id = Column(Integer, ForeignKey("district.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    employee_amount = Column(Integer)
    building_area_size = Column(Float)
    land_area_size = Column(Float)

    equipment = Column(ARRAY(Integer))
    equipment_amounts = Column(ARRAY(Integer))

    buildings = Column(ARRAY(Integer))
    building_areas = Column(ARRAY(Integer))

    additional_services = Column(ARRAY(Integer))

    legal_entity_type = Column(Enum(LegalEntityType))
    predicted_income_per_year_rub = Column(Float)
    accounting_services_documents_amount = Column(Integer)

    additional_needs = Column(ARRAY(String))
    additional_needs_prices = Column(ARRAY(Integer))

    industry = relationship("IndustryModel")
    district = relationship("DistrictModel")
