# todo здесь будет тяжелая логика с pdf
from fastapi import Depends
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.pieces.calculation.models import RequestModel
from app.src.pieces.calculation.pdf.PdfCreator import PdfCreator
from app.src.pieces.calculation.schemas import CalculationCreateFormSchema, EquipmentCalculationResponseSchema, \
    CalculationPreparedDataSchema
from app.src.pieces.district.models import DistrictModel
from app.src.pieces.equipment.models import EquipmentModel

RUBS_FOR_DOLLAR = 71


def make_pdf():
    return 'pdf'


def join_request_with_model(request_list, model_class, schema_class, update_strategy, db: Session):
    request_list.sort(key=lambda x: x.id)
    model_list: list[model_class] = db.query(model_class).filter(
        model_class.id.in_([eq.id for eq in request_list])).order_by(model_class.id)
    responses = [
        schema_class(
            **update_strategy(equipment_request, equipment_model)
            # equipment=equipment_model,
            # amount=equipment_request.amount,
            # total_expenses=equipment_model.average_price_dollar * RUBS_FOR_DOLLAR * equipment_request.amount,
        )
        for equipment_request, equipment_model
        in zip(request_list, model_list)
    ]
    return responses


def handle_calculation(form: CalculationCreateFormSchema, db: Session = Depends(get_db)):
    calculation_prepared_data = dict()

    district_model: DistrictModel = db.query(DistrictModel).filter(DistrictModel.id == form.district_id).first()
    calculation_prepared_data['district'] = district_model.name

    # rent
    calculation_prepared_data['total_rent_expenses'] = form.land_area_size * district_model.average_price_per_m2_rub

    # equipment
    equipments = join_request_with_model \
        (
             form.equipment, EquipmentModel, EquipmentCalculationResponseSchema,
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


def download_calculation(req_id: int, db: Session = Depends(get_db)):
    db_request: RequestModel = db.query(RequestModel).filter(RequestModel.id == req_id).first()
    request = CalculationCreateFormSchema(request_dict=db_request.__dict__, db=db)

    response = handle_calculation(request, db)
    pdf_creator = PdfCreator(response, req_id)

    return pdf_creator.get_output_pdf_filename()
