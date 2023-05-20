from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.pieces.calculation.schemas import CalculationCreateFormSchema
from app.src.pieces.calculation.service import make_pdf

router = APIRouter(
    prefix="/calculation",
    tags=["calculation"],
)


# todo with response_model - спиздить способ выгрузки файла из лцт2022
@router.post("/create")  # , response_model=UserOutputSchema)
async def create_calculation(form: CalculationCreateFormSchema, db: Session = Depends(get_db)):
    return make_pdf()
