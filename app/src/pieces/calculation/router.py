from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.pieces.calculation.schemas import CalculationCreateFormSchema, CalculationPreparedDataSchema, \
    EquipmentCalculationResponseSchema
from app.src.pieces.calculation.service import make_pdf
from app.src.pieces.district.models import DistrictModel
from app.src.pieces.equipment.models import EquipmentModel

router = APIRouter(
    prefix="/calculation",
    tags=["calculation"],
)

RUBS_FOR_DOLLAR = 71


# todo with response_model - спиздить способ выгрузки файла из лцт2022
@router.post("/create")  # , response_model=UserOutputSchema)
async def create_calculation(form: CalculationCreateFormSchema, db: Session = Depends(get_db)):
    calculation_prepared_data = CalculationPreparedDataSchema()

    district_model: DistrictModel = db.query(DistrictModel).filter(DistrictModel.id == form.district_id).first()
    calculation_prepared_data.district = district_model.name

    # rent
    calculation_prepared_data.total_rent_expenses = form.land_area_size * district_model.average_price_rub

    # equipment
    form.equipment.sort(key=lambda x: x.id)
    equipment_models: list[EquipmentModel] = db.query(EquipmentModel).filter(EquipmentModel.id.in_([eq.equipment_type_id for eq in form.equipment])).order_by(EquipmentModel.id)
    equipment_responses = [
        EquipmentCalculationResponseSchema(
            equipment=equipment_model,
            amount=equipment_request.amount,
            total_expenses=equipment_model.average_price_dollar * RUBS_FOR_DOLLAR * equipment_request.amount,
        )
        for equipment_request, equipment_model
        in zip(form.equipment, equipment_models)
    ]
    calculation_prepared_data.equipments = equipment_responses




    industry_name: str
    subindustry_name: str
    legal_entity_type: str
    district: str

    # general
    total_expenses: float

    # employee
    employee_amount: int
    total_employee_expenses: float

    # rent
    building_area_size: float
    land_area_size: float
    total_rent_expenses: float

    # taxes
    predicted_income_per_year_rub: float
    total_taxes_expenses: float


