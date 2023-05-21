from sqlalchemy.orm import Session

from app.src.config import DATA_FOLDER_PATH
from app.src.pieces.equipment.models import EquipmentModel
from app.src.pieces.equipment.schemas import EquipmentCreationSchema
import os

from openpyxl import load_workbook
from sqlalchemy.orm import Session

from app.src.pieces.equipment.schemas import EquipmentCreationSchema


def get_equipment_by_id(db: Session, user_id: int) -> EquipmentModel:
    return db.query(EquipmentModel).filter(EquipmentModel.id == user_id).first()


def get_equipments(db: Session, skip: int = 0, limit: int = 100) -> list[EquipmentModel]:
    return db.query(EquipmentModel).offset(skip).limit(limit).all()


def get_equipment_suggestions(db: Session, subtext: str = '', skip: int = 0, limit: int = 100) -> list[EquipmentModel]:
    if subtext == '':
        return get_equipments(db, skip, limit)
    return db.query(EquipmentModel).filter(EquipmentModel.name.contains(subtext)).offset(skip).limit(limit).all()


def create_equipment(equipment: EquipmentCreationSchema, db: Session) -> EquipmentModel:
    equipment = EquipmentModel(**equipment.dict())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


def parse_stanki(filename: str, db: Session):

    file_path = os.path.join(DATA_FOLDER_PATH, filename)

    workbook = load_workbook(file_path, data_only=True)
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, max_row=9, max_col=4, values_only=True):
        # todo - add try-except block and smart error count
        schema = EquipmentCreationSchema(name=row[1], average_price_dollar=float(row[2]))
        res = create_equipment(schema, db)
        #print('eq created')
        #print(res.average_price_dollar)
        #print(res.name)
        #print(res.id)
