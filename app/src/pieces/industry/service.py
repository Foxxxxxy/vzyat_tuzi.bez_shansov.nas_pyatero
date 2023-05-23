from sqlalchemy.orm import Session

from app.src.config import DATA_FOLDER_PATH
from app.src.pieces.industry.models import IndustryModel
from app.src.pieces.industry.schemas import IndustryCreationSchema
import os
from typing import Union

from openpyxl import load_workbook
from sqlalchemy.orm import Session


def get_industry_by_id(db: Session, user_id: int) -> IndustryModel:
    return db.query(IndustryModel).filter(IndustryModel.id == user_id).first()


def get_industries(db: Session, skip: int = 0, limit: int = 100) -> list[IndustryModel]:
    return db.query(IndustryModel).offset(skip).limit(limit).all()


def get_industry_suggestions(db: Session, subtext: str = '', skip: int = 0, limit: int = 100) -> list[IndustryModel]:
    if subtext == '':
        return get_industries(db, skip, limit)
    return db.query(IndustryModel).filter(IndustryModel.name.contains(subtext)).offset(skip).limit(limit).all()


def create_industry(industry: IndustryCreationSchema, db: Session) -> IndustryModel:
    industry = IndustryModel(**industry.dict())
    db.add(industry)
    db.commit()
    db.refresh(industry)
    return industry


def parse_industry(filename: str, db: Session, only_first: Union[int, None] = None):
    if only_first is not None:
        only_first += 2

    file_path = os.path.join(DATA_FOLDER_PATH, filename)

    workbook = load_workbook(file_path, data_only=True)
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, max_row=only_first, max_col=6, values_only=True):
        if db.query(IndustryModel).filter(IndustryModel.name == row[1]).first():
            continue

        schema = IndustryCreationSchema(name=row[1])#, average_price_per_m2_rub=float(row[2]))
        res = create_industry(schema, db)
        #print(row[5])
        #print('eq created')
        #print(res.average_price_per_m2_rub)
        #print(res.name)
        #print(res.id)
