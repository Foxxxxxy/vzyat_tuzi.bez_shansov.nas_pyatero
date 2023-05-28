import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.src.database.common import get_db

from app.src.pieces.district import service as district_service
from app.src.pieces.district.schemas import DistrictSchema, DistrictCreationSchema
from app.src.pieces.user.models import UserModel
from app.src.security import auth_user, auth_admin

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = Path(script_dir).resolve().parents[0]
excel_template_filename = f"{parent_dir}/excel/excel_templates/district_template.xlsx"

router = APIRouter(
    prefix="/district",
    tags=["district"],
)


@router.get("/excel-template", response_class=FileResponse)
async def get_excel_template(user: UserModel = Depends(auth_admin)):
    headers = {'Content-Disposition': 'attachment; filename="template.xlsx"'}
    return FileResponse(path=excel_template_filename, filename=f"template.xlsx", headers=headers)


@router.post("/excel")
async def post_excel(file: UploadFile, refresh: bool = False, db: Session = Depends(get_db),
                     user: UserModel = Depends(auth_admin)):
    await district_service.upload_district_excel_to_db(file, refresh, db)


@router.get("/suggestions", response_model=list[DistrictSchema])
async def get_districts_suggestions(subtext: str = '', skip: int = 0, limit: int = 100,
                                    db: Session = Depends(get_db)):
    return district_service.get_district_suggestions(db, subtext, skip, limit)


@router.get("/{id}", response_model=DistrictSchema)
async def get_district(id: int, db: Session = Depends(get_db)):
    result = district_service.get_district_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No district with such id!")
    return result


@router.get("/", response_model=list[DistrictSchema])
async def get_districts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = district_service.get_districts(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No districts!")
    return result


@router.post("/", response_model=DistrictSchema)
async def add_district(schema: DistrictCreationSchema, db: Session = Depends(get_db),
                       user: UserModel = Depends(auth_admin)):
    try:
        return district_service.add_district(db, schema)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Район с таким именем уже существует!")


@router.put("/{id}", response_model=DistrictSchema)
async def update_district(id: int, schema: DistrictCreationSchema,
                          db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    return district_service.update_district(db, id, schema)


@router.delete("/{id}", response_model=DistrictSchema)
async def delete_district(id: int, db: Session = Depends(get_db),
                          user: UserModel = Depends(auth_admin)):
    return district_service.delete_district(db, id)
