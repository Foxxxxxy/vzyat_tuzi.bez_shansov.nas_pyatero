import os

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.pieces.calculation import service
from app.src.pieces.calculation.models import RequestModel
from app.src.pieces.calculation.schemas import CalculationCreateFormSchema, CalculationPreparedDataSchema, \
    EquipmentCalculationResponseSchema
from app.src.pieces.calculation.service import join_request_with_model
from app.src.pieces.district.models import DistrictModel
from app.src.pieces.equipment.models import EquipmentModel
from app.src.pieces.calculation.pdf.PdfCreator import PdfCreator
from app.src.pieces.calculation.schemas import CalculationCreateFormSchema, CalculationPreparedDataSchema

script_dir = os.path.dirname(os.path.realpath(__file__))

router = APIRouter(
    prefix="/calculation",
    tags=["calculation"],
)


# todo with response_model - спиздить способ выгрузки файла из лцт2022
@router.post("/create", response_model=CalculationPreparedDataSchema)
async def create_calculation(form: CalculationCreateFormSchema, db: Session = Depends(get_db)):
    return service.handle_calculation(form, db)


@router.get("/{req_id}/download-pdf", response_class=FileResponse)
async def download_calculated_report(req_id: int, db: Session = Depends(get_db)):
    pdf_filename = service.download_calculation(req_id, db)
    headers = {'Content-Disposition': 'attachment; filename="out.pdf"'}
    return FileResponse(path=pdf_filename, filename=f"out.pdf", headers=headers)

