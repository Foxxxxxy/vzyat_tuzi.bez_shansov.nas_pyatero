from sqlalchemy.orm import Session

from app.src.config import DATA_FOLDER_PATH
from app.src.pieces.building.models import BuildingModel
from app.src.pieces.building.schemas import BuildingCreationSchema
import os
from typing import Union

from openpyxl import load_workbook
from sqlalchemy.orm import Session

from app.src.pieces.building.schemas import BuildingCreationSchema


def get_building_by_id(db: Session, user_id: int) -> BuildingModel:
    return db.query(BuildingModel).filter(BuildingModel.id == user_id).first()


def get_buildings(db: Session, skip: int = 0, limit: int = 100) -> list[BuildingModel]:
    return db.query(BuildingModel).offset(skip).limit(limit).all()


def get_building_suggestions(db: Session, subtext: str = '', skip: int = 0, limit: int = 100) -> list[BuildingModel]:
    if subtext == '':
        return get_buildings(db, skip, limit)
    return db.query(BuildingModel).filter(BuildingModel.name.contains(subtext)).offset(skip).limit(limit).all()


def create_building(equipment: BuildingCreationSchema, db: Session) -> BuildingModel:
    equipment = BuildingModel(**equipment.dict())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


def parse_buildings(filename: str, db: Session, only_first: Union[int, None] = None):
    if only_first is not None:
        only_first += 2

    file_path = os.path.join(DATA_FOLDER_PATH, filename)
    workbook = load_workbook(file_path, data_only=True)
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, max_row=only_first, max_col=5, values_only=True):
        if row[2] is None or row[2] == '-':
            continue
        schema = BuildingCreationSchema(name=row[1], average_price_rub=float(row[2]))
        res = create_building(schema, db)
        #print('eq created')
        #print(res.average_price_dollar)
        #print(res.name)
        #print(res.id)
