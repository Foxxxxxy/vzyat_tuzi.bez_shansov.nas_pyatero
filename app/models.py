from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()


class LegalEntityType(str, Enum):
    OOO_AO = 'OOO_AO'
    IP = 'IP'


# class Industry(Base):
#     __tablename__ = "industry"
#
#     id =
#
# class SubIndustry(Base):
#     __tablename__ = "industry"
#
#     id =
#     industry_id foreign key
#
# class District(Base):
#     __tablename__ = "district"
#     id =
#     price_per_meter = # rub?
#     # foreign key Region
#
# # future
# # class Region(Base):
# #   id =
#
# class Equipment(Base):
#     __tablename__ = "equipment"
#
#     id =
#     name =
#     average_price_dollar =
#     #average_price_rub =  #  count inplace