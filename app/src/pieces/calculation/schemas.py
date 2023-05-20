from pydantic import BaseModel
from typing import Optional

from app.src.pieces.additional_service.schemas import AdditionalServiceSchema
from app.src.pieces.calculation.models import LegalEntityType
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


    # todo
    # building = List[Building] список зданий и цены по их кв метру и их размер в кв м


    # todo
    # данные для рассчета бухгалтерского калькулятора

    # todo
    # иные потребности List[Потребность]

class CalculationPreparedDataSchema(BaseModel):
    # business info
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

    # equipment
    equipments: list[EquipmentCalculationResponseSchema]
    total_equipments_expenses: float

    # additional services
    additional_services: list[AdditionalServiceCalculationResponseSchema]
    total_additional_services_expenses: float
