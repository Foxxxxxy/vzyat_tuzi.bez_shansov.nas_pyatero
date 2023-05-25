import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.src.database.common import get_db

from app.src.pieces.industry.schemas import IndustrySchema, IndustryCreationSchema
from app.src.pieces.industry import service as industry_service
from app.src.pieces.user.models import UserModel
from app.src.security import auth_user, auth_admin

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = Path(script_dir).resolve().parents[0]
excel_template_filename = f"{parent_dir}/excel/excel_templates/industry_template.xlsx"

router = APIRouter(
    prefix="/industry",
    tags=["industry"],
)


@router.get("/excel-template", response_class=FileResponse)
async def get_excel_template():
    headers = {'Content-Disposition': 'attachment; filename="template.xlsx"'}
    return FileResponse(path=excel_template_filename, filename=f"template.xlsx", headers=headers)


@router.post("/excel")
async def post_excel(file: UploadFile, refresh: bool = False, db: Session = Depends(get_db)):
    await industry_service.upload_industry_excel_to_db(file, refresh, db)


@router.get("/suggestions", response_model=list[IndustrySchema])
async def get_industries_suggestions(subtext: str = '', skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return industry_service.get_industry_suggestions(db, subtext, skip, limit)


@router.get("/{id}", response_model=IndustrySchema)
async def get_industry(id: int, db: Session = Depends(get_db)):
    result = industry_service.get_industry_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such industry")
    return result


@router.get("/", response_model=list[IndustrySchema])
async def get_industries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = industry_service.get_industries(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such industry")
    return result


@router.post("/", response_model=IndustrySchema)
async def add_industry(schema: IndustryCreationSchema,
                       db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    return industry_service.add_industry(db, schema)


@router.put("/{id}", response_model=IndustrySchema)
async def update_industry(id: int, schema: IndustryCreationSchema,
                          db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    return industry_service.update_industry(db, id, schema)


@router.delete("/{id}", response_model=IndustrySchema)
async def delete_industry(id: int, db: Session = Depends(get_db),
                          user: UserModel = Depends(auth_admin)):
    return industry_service.delete_industry(db, id)
