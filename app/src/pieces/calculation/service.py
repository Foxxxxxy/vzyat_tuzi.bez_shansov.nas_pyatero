# todo здесь будет тяжелая логика с pdf
from fastapi import Depends
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.pieces.additional_service.models import AdditionalServiceModel
from app.src.pieces.building.models import BuildingModel
from app.src.pieces.calculation.models import RequestModel
from app.src.pieces.calculation.pdf.PdfCreator import PdfCreator
from app.src.pieces.calculation.schemas import CalculationCreateFormSchema, EquipmentCalculationResponseSchema, \
    CalculationPreparedDataSchema, AdditionalServiceCalculationResponseSchema, CalculationCreateRequestSchema, \
    BuildingCalculationResponseSchema
from app.src.pieces.currency.currency import Currency
from app.src.pieces.district.models import DistrictModel
from app.src.pieces.equipment.models import EquipmentModel
from app.src.pieces.industry.models import IndustryModel

RUBS_FOR_DOLLAR = 71


def get_rubs_for_dollar(db: Session):
    return Currency.get_currency("RUB", db)


def make_pdf():
    return 'pdf'


def get_model_instance_by_id(model_class, form, form_id_field: str, db: Session):
    model: model_class = db.query(model_class).filter(
        model_class.id == getattr(form, form_id_field)
    ).first()
    return model


def calculate_accounting_services_expenses(accounting_services_documents_amount: int) -> float:
    return accounting_services_documents_amount * 1000.0  # todo


def join_request_with_model(request_list, model_class, schema_class, update_strategy, db: Session):
    request_list.sort(key=lambda x: x.id)
    model_list: list[model_class] = db.query(model_class).filter(
        model_class.id.in_([eq.id for eq in request_list])).order_by(model_class.id)
    responses = [
        schema_class(
            **update_strategy(equipment_request, equipment_model)
        )
        for equipment_request, equipment_model
        in zip(request_list, model_list)
    ]
    return responses


def create_request(request: CalculationCreateFormSchema, db: Session) -> RequestModel:
    request = RequestModel(**request.as_request_model_dict())
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def _handle_calculation(form: CalculationCreateRequestSchema, db: Session) -> CalculationPreparedDataSchema:
    calculation_prepared_data = dict()
    calculation_prepared_data['request_id'] = form.id

    # industry
    industry_model = get_model_instance_by_id(IndustryModel, form, "industry_id", db)

    calculation_prepared_data["industry_name"] = industry_model.name

    # district
    district_model = get_model_instance_by_id(DistrictModel, form, "district_id", db)

    calculation_prepared_data['district'] = district_model.name

    # legal entity type
    legal_entity_type = form.legal_entity_type

    calculation_prepared_data["legal_entity_type"] = legal_entity_type.name

    # employee
    employee_amount = form.employee_amount

    calculation_prepared_data["employee_amount"] = employee_amount
    calculation_prepared_data["total_employee_expenses"] = 0.0

    # rent
    building_area_size = form.building_area_size
    land_area_size = form.land_area_size

    calculation_prepared_data["building_area_size"] = building_area_size
    calculation_prepared_data["land_area_size"] = land_area_size
    total_area = building_area_size + land_area_size
    calculation_prepared_data['total_rent_expenses'] = total_area * district_model.average_price_per_m2_rub

    # taxes
    predicted_income_per_year_rub = form.predicted_income_per_year_rub

    calculation_prepared_data["predicted_income_per_year_rub"] = predicted_income_per_year_rub
    calculation_prepared_data["total_taxes_expenses"] = predicted_income_per_year_rub * 0.06

    # accounting services # todo add these fields to pdf
    accounting_services_documents_amount = form.accounting_services_documents_amount

    calculation_prepared_data["accounting_services_documents_amount"] = accounting_services_documents_amount
    calculation_prepared_data["accounting_services_expenses"] = calculate_accounting_services_expenses(accounting_services_documents_amount)

    # equipment
    equipments = join_request_with_model(
        form.equipment, EquipmentModel, EquipmentCalculationResponseSchema,
        lambda equipment_request, equipment_model: {
            'equipment': equipment_model,
            'amount': equipment_request.amount,
            'total_expenses': equipment_model.average_price_dollar * RUBS_FOR_DOLLAR * equipment_request.amount,
        },
        db
    )
    calculation_prepared_data['equipments'] = equipments
    calculation_prepared_data["total_equipments_expenses"] = \
        sum(it.total_expenses for it in equipments)


    # buildings
    buildings = join_request_with_model(
        form.buildings, BuildingModel, BuildingCalculationResponseSchema,
        lambda building_request, building_model: {
            'building': building_model,
            'area': building_request.area,
            'total_expenses': building_model.average_price_rub * building_request.area,
        },
        db
    )
    calculation_prepared_data['buildings'] = buildings
    calculation_prepared_data["total_buildings_expenses"] = \
        sum(it.total_expenses for it in buildings)

    # additional services
    additional_services = join_request_with_model(
        form.additional_services, AdditionalServiceModel, AdditionalServiceCalculationResponseSchema,
        lambda additional_service_request, additional_service_model: {
            'additional_service': additional_service_model,
            'total_expenses': additional_service_model.average_price_dollar * RUBS_FOR_DOLLAR
        },
        db
    )

    calculation_prepared_data['additional_services'] = additional_services
    calculation_prepared_data["total_additional_services_expenses"] = \
        sum(it.total_expenses for it in additional_services)

    calculation_prepared_data["total_expenses"] = 0.0

    return CalculationPreparedDataSchema(**calculation_prepared_data)


def handle_calculation(form: CalculationCreateFormSchema, db: Session) -> CalculationPreparedDataSchema:
    # save request to db
    request_model = create_request(form, db)
    # todo - better make converter from CalculationCreateFormSchema to CalculationCreateRequestSchema
    calculation_create_request_schema = CalculationCreateRequestSchema.from_request_model(request_model, db)
    return _handle_calculation(calculation_create_request_schema, db)


def download_calculation(req_id: int, db: Session):
    db_request: RequestModel = db.query(RequestModel).filter(RequestModel.id == req_id).first()
    request = CalculationCreateRequestSchema.from_request_model(request_model=db_request, db=db)

    response = _handle_calculation(request, db)
    pdf_creator = PdfCreator(response, req_id)

    return pdf_creator.get_output_pdf_filename()
