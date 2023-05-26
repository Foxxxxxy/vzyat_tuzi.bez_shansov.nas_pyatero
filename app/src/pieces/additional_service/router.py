import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.pieces.additional_service.schemas import AdditionalServiceSchema, AdditionalServiceCreationSchema

from app.src.pieces.additional_service import service as additional_services_service
from app.src.pieces.user.models import UserModel
from app.src.security import auth_user, auth_admin

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = Path(script_dir).resolve().parents[0]
excel_template_filename = f"{parent_dir}/excel/excel_templates/additional_service_template.xlsx"

router = APIRouter(
    prefix="/additional-service",
    tags=["additional-service"],
)


@router.get("/excel-template", response_class=FileResponse)
async def get_excel_template(user: UserModel = Depends(auth_admin)):
    headers = {'Content-Disposition': 'attachment; filename="template.xlsx"'}
    return FileResponse(path=excel_template_filename, filename=f"template.xlsx", headers=headers)


@router.post("/excel")
async def post_excel(file: UploadFile, refresh: bool = False, db: Session = Depends(get_db),
                     user: UserModel = Depends(auth_admin)):
    await additional_services_service.upload_additional_services_excel_to_db(file, refresh, db)


@router.get("/suggestions", response_model=list[AdditionalServiceSchema])
async def get_additional_services_suggestions(subtext: str = '', skip: int = 0, limit: int = 100,
                                              db: Session = Depends(get_db)):
    return additional_services_service.get_additional_service_suggestions(db, subtext, skip, limit)


@router.get("/{id}", response_model=AdditionalServiceSchema)
async def get_additional_service(id: int, db: Session = Depends(get_db)):
    result = additional_services_service.get_additional_service_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No additional_service with such id!")
    return result


@router.get("/", response_model=list[AdditionalServiceSchema])
async def get_additional_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = additional_services_service.get_additional_services(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No additional_service!")
    return result


@router.post("/", response_model=AdditionalServiceSchema)
async def add_additional_service(schema: AdditionalServiceCreationSchema,
                                 db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    return additional_services_service.add_additional_service(db, schema)


@router.put("/{id}", response_model=AdditionalServiceSchema)
async def update_additional_service(id: int, schema: AdditionalServiceCreationSchema,
                                    db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    return additional_services_service.update_additional_service(db, id, schema)


@router.delete("/{id}", response_model=AdditionalServiceSchema)
async def delete_additional_service(id: int,
                                    db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    return additional_services_service.delete_additional_service(db, id)
