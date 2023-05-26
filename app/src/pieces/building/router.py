import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.src.database.common import get_db

from app.src.pieces.building.schemas import BuildingSchema, BuildingCreationSchema
from app.src.pieces.building import service as building_service
from app.src.pieces.user.models import UserModel

from app.src.security import auth_user, auth_admin

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = Path(script_dir).resolve().parents[0]
excel_template_filename = f"{parent_dir}/excel/excel_templates/building_template.xlsx"

router = APIRouter(
    prefix="/building",
    tags=["building"],
)


@router.get("/excel-template", response_class=FileResponse)
async def get_excel_template(user: UserModel = Depends(auth_admin)):
    headers = {'Content-Disposition': 'attachment; filename="template.xlsx"'}
    return FileResponse(path=excel_template_filename, filename=f"template.xlsx", headers=headers)


@router.post("/excel")
async def post_excel(file: UploadFile, refresh: bool = False, db: Session = Depends(get_db),
                     user: UserModel = Depends(auth_admin)):
    await building_service.upload_building_excel_to_db(file, refresh, db)


@router.get("/suggestions", response_model=list[BuildingSchema])
async def get_buildings_suggestions(subtext: str = '', skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return building_service.get_building_suggestions(db, subtext, skip, limit)


@router.get("/{id}", response_model=BuildingSchema)
async def get_building(id: int, db: Session = Depends(get_db)):
    result = building_service.get_building_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such building")
    return result


@router.get("/", response_model=list[BuildingSchema])
async def get_buildings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = building_service.get_buildings(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such building")
    return result


@router.post("/", response_model=BuildingSchema)
async def add_building(schema: BuildingCreationSchema, db: Session = Depends(get_db),
                       user: UserModel = Depends(auth_admin)):
    return building_service.add_building(db, schema)


@router.put("/{id}", response_model=BuildingSchema)
async def update_building(id: int, schema: BuildingCreationSchema,
                          db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    return building_service.update_building(db, id, schema)


@router.delete("/{id}", response_model=BuildingSchema)
async def delete_building(id: int, db: Session = Depends(get_db),
                          user: UserModel = Depends(auth_admin)):
    return building_service.delete_building(db, id)
