from sqlalchemy.orm import Session

from app.src.config import DATA_FOLDER_PATH
from app.src.pieces.district.models import DistrictModel
from app.src.pieces.district.schemas import DistrictCreationSchema
import os

from openpyxl import load_workbook
from sqlalchemy.orm import Session


def create_district(district: DistrictCreationSchema, db: Session) -> DistrictModel:
    district = DistrictModel(**district.dict())
    db.add(district)
    db.commit()
    db.refresh(district)
    return district


def parse_district(filename: str, db: Session):

    file_path = os.path.join(DATA_FOLDER_PATH, filename)

    workbook = load_workbook(file_path, data_only=True)
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, max_row=9, max_col=4, values_only=True):
        schema = DistrictCreationSchema(name=row[1], average_price_per_m2_rub=float(row[2]))
        res = create_district(schema, db)
        print('eq created')
        print(res.average_price_per_m2_rub)
        print(res.name)
        print(res.id)
