import os

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.src.database.common import get_db
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

RUBS_FOR_DOLLAR = 71


# todo with response_model - спиздить способ выгрузки файла из лцт2022
@router.post("/create")  # , response_model=UserOutputSchema)
async def create_calculation(form: CalculationCreateFormSchema, db: Session = Depends(get_db)):
    calculation_prepared_data = dict()

    district_model: DistrictModel = db.query(DistrictModel).filter(DistrictModel.id == form.district_id).first()
    calculation_prepared_data['district'] = district_model.name

    # rent
    calculation_prepared_data['total_rent_expenses'] = form.land_area_size * district_model.average_price_rub

    # equipment
    equipments = join_request_with_model(form.equipment, EquipmentModel, EquipmentCalculationResponseSchema,
                                         lambda equipment_request, equipment_model: {
                                             'equipment': equipment_model,
                                             'amount': equipment_request.amount,
                                             'total_expenses': equipment_model.average_price_dollar * RUBS_FOR_DOLLAR * equipment_request.amount,
                                         },
                                         db
                                         )

    calculation_prepared_data['equipments'] = equipments

    return CalculationPreparedDataSchema(
        # business info
        industry_name='',
        subindustry_name='',
        legal_entity_type='',
        district='',

        # general
        total_expenses=0.0,

        # employee
        employee_amount=0,
        total_employee_expenses=0.0,

        # rent
        building_area_size=0.0,
        land_area_size=0.0,
        total_rent_expenses=0.0,

        # taxes
        predicted_income_per_year_rub=0.0,
        total_taxes_expenses=0.0,

        # equipment
        equipments=equipments,
        total_equipments_expenses=0.0,

        # additional services
        additional_services=[],  # list[AdditionalServiceCalculationResponseSchema]
        total_additional_services_expenses=0.0,
    )

@router.get("/pdf/{calc_id}", response_class=FileResponse)
async def download_calculated_report(calc_id: int):
    report = CalculationPreparedDataSchema(
        industry_name="бизнес",
        legal_entity='OOO',
        district="Центральный район",
        employee_amount=5,
        total_employee_expenses="500",
        total_rent_expenses="100",
        total_taxes_expenses="100",
        total_equipments_expenses="100",
        total_expenses="800",

        subindustry_name="",
        legal_entity_type="",
        building_area_size=0,
        land_area_size=0,
        predicted_income_per_year_rub=0,
        equipments=[],
        additional_services=[],
        total_additional_services_expenses=0,
    )

    PdfCreator(report, calc_id)
    headers = {'Content-Disposition': 'attachment; filename="out.pdf"'}
    return FileResponse(path=f"{script_dir}/pdf/brochures/brochure{calc_id}.pdf", filename=f"out.pdf", headers=headers)
