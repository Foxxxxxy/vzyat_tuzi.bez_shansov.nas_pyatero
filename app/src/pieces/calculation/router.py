import os
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.src.common import round_floats
from app.src.database.common import get_db
from app.src.pieces.calculation import service
from app.src.pieces.calculation.models import RequestModel
from app.src.pieces.calculation.schemas import CalculationCreateFormSchema, CalculationPreparedDataSchema, \
    EquipmentCalculationResponseSchema, CalculationCreateRequestSchema
from app.src.pieces.calculation.service import join_request_with_model
from app.src.pieces.district.models import DistrictModel
from app.src.pieces.equipment.models import EquipmentModel
from app.src.pieces.calculation.pdf.PdfCreator import PdfCreator
from app.src.pieces.calculation.schemas import CalculationCreateFormSchema, CalculationPreparedDataSchema
from app.src.pieces.user.models import UserModel
from app.src.pieces.user.schemas import EUserLevel
from app.src.security import auth_user, maybe_auth_user, auth_admin
from app.src.pieces.calculation import service as calculation_service

script_dir = os.path.dirname(os.path.realpath(__file__))

router = APIRouter(
    prefix="/calculation",
    tags=["calculation"],
)


@router.get("/{id}", response_model=CalculationCreateRequestSchema)
async def get_calculation_request(id: int, db: Session = Depends(get_db), user: UserModel = Depends(auth_user)):
    result = calculation_service.get_calculation_request_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No request with such id!")

    if user.level == EUserLevel.admin:
        return result

    if result.user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This is anonymus request!")

    if result.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not the owner of this request!")

    return result


@router.get("/", response_model=list[CalculationCreateRequestSchema])
async def get_calculation_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    result = calculation_service.get_calculation_requests(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No requests!")
    return result


@router.post("/create", response_model=CalculationPreparedDataSchema)
async def create_calculation(form: CalculationCreateFormSchema, db: Session = Depends(get_db), user: Union[UserModel, None] = Depends(maybe_auth_user)):
    result = service.handle_calculation(form, db, user)
    round_floats(result)
    return result


@router.get("/{req_id}/download-pdf", response_class=FileResponse)
async def download_calculated_report(req_id: int, db: Session = Depends(get_db), user: UserModel = Depends(auth_user)):
    pdf_filename = service.download_calculation(req_id, db)
    headers = {'Content-Disposition': 'attachment; filename="out.pdf"'}
    return FileResponse(path=pdf_filename, filename=f"out.pdf", headers=headers)

