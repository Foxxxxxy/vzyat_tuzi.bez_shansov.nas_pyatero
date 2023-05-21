from fastapi import Depends
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.pieces.additional_service.models import AdditionalServiceModel
from app.src.pieces.additional_service.schemas import AdditionalServiceSchema
from app.src.pieces.calculation.models import LegalEntityType, RequestModel
from app.src.pieces.equipment.models import EquipmentModel
from app.src.pieces.equipment.schemas import EquipmentSchema


class EquipmentCalculationRequestSchema(BaseModel):
    id: int
    amount: int


class EquipmentCalculationResponseSchema(BaseModel):
    equipment: EquipmentSchema
    amount: int
    total_expenses: float


class AdditionalServiceCalculationRequestSchema(BaseModel):
    id: int


class AdditionalServiceCalculationResponseSchema(BaseModel):
    additional_service: AdditionalServiceSchema
    total_expenses: float


class CalculationCreateFormSchema(BaseModel):
    industry_id: int  # id сферы хоз деятельности todo таблица сфер хоз деятельности
    subindustry_id: Optional[int]

    district_id: int

    employee_amount: int  # количество рабочих, чел

    building_area_size: float  # площадь здания, м2
    land_area_size: float  # площадь земельного участка, м2

    equipment: list[EquipmentCalculationRequestSchema]
    additional_services: list[AdditionalServiceCalculationRequestSchema]

    legal_entity_type: LegalEntityType

    predicted_income_per_year_rub: float  # предполагаемый доход в год - для подсчета стоимости патента

    class Config:
        orm_mode = True

    def __init__(self, request_dict, db):
        equipment_ids = request_dict["equipment"]
        additional_services_ids = request_dict["additional_services"]

        equipment_models = db.query(EquipmentModel).filter(EquipmentModel.id.in_(equipment_ids))
        additional_services_models = db.query(AdditionalServiceModel).filter(AdditionalServiceModel.id.in_(additional_services_ids))

        equipment_schemas = [EquipmentSchema.from_orm(it) for it in equipment_models]
        equipment_calculation_request_schemas = [
            EquipmentCalculationRequestSchema(id=it.id, amount=amount) for it, amount in
            zip(equipment_schemas, request_dict["equipment_amounts"])
        ]
        additional_services_schemas = [AdditionalServiceSchema.from_orm(it) for it in additional_services_models]

        request_dict["equipment"] = equipment_calculation_request_schemas
        request_dict["additional_services"] = additional_services_schemas

        super().__init__(**request_dict)

    # todo
    # building = List[Building] список зданий и цены по их кв метру и их размер в кв м

    # todo
    # данные для рассчета бухгалтерского калькулятора

    # todo
    # иные потребности List[Потребность]


class CalculationPreparedDataSchema(BaseModel):
    # business info
    industry_name: str
    # subindustry_name: str
    district: str
    legal_entity_type: str

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

    # equipment
    equipments: list[EquipmentCalculationResponseSchema]
    total_equipments_expenses: float

    # additional services
    additional_services: list[AdditionalServiceCalculationResponseSchema]
    total_additional_services_expenses: float
