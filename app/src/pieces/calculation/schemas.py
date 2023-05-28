import datetime

from pydantic import BaseModel
from typing import Optional, Union

from app.src.pieces.additional_service.models import AdditionalServiceModel
from app.src.pieces.additional_service.schemas import AdditionalServiceSchema
from app.src.pieces.building.models import BuildingModel
from app.src.pieces.building.schemas import BuildingSchema
from app.src.pieces.calculation.models import LegalEntityType, RequestModel
from app.src.pieces.equipment.models import EquipmentModel
from app.src.pieces.equipment.schemas import EquipmentSchema


# equipment
class EquipmentCalculationRequestSchema(BaseModel):
    id: int
    amount: int


class EquipmentCalculationResponseSchema(BaseModel):
    equipment: EquipmentSchema
    amount: int
    total_expenses: float


# building
class BuildingCalculationRequestSchema(BaseModel):
    id: int
    area: int


class BuildingCalculationResponseSchema(BaseModel):
    building: BuildingSchema
    area: int
    total_expenses: float


# additional services
class AdditionalServiceCalculationRequestSchema(BaseModel):
    id: int


class AdditionalServiceCalculationResponseSchema(BaseModel):
    additional_service: AdditionalServiceSchema
    total_expenses: float


# additional needs
class AdditionalNeedCalculationSchema(BaseModel):
    name: str
    price: int


class CalculationCreateFormSchema(BaseModel):
    industry_id: int  # id сферы хоз деятельности todo таблица сфер хоз деятельности

    district_id: int

    employee_amount: int  # количество рабочих, чел

    building_area_size: float  # площадь здания, м2
    land_area_size: float  # площадь земельного участка, м2

    equipment: list[EquipmentCalculationRequestSchema]
    additional_services: list[AdditionalServiceCalculationRequestSchema] # todo
    buildings: list[BuildingCalculationRequestSchema]

    legal_entity_type: LegalEntityType

    predicted_income_per_year_rub: float  # предполагаемый доход в год - для подсчета стоимости патента

    accounting_services_documents_amount: int

    # todo
    # данные для рассчета бухгалтерского калькулятора

    additional_needs: list[AdditionalNeedCalculationSchema]

    def as_request_model_dict(self):
        result_dict = self.dict()

        result_dict['equipment_amounts'] = [el['amount'] for el in result_dict['equipment']]
        result_dict['equipment'] = [el['id'] for el in result_dict['equipment']]

        result_dict['building_areas'] = [el['area'] for el in result_dict['buildings']]
        result_dict['buildings'] = [el['id'] for el in result_dict['buildings']]

        result_dict['additional_services'] = [el['id'] for el in result_dict['additional_services']]

        result_dict["additional_needs_prices"] = [el["price"] for el in result_dict["additional_needs"]]
        result_dict["additional_needs"] = [el["name"] for el in result_dict["additional_needs"]]
        return result_dict


class CalculationCreateRequestSchema(CalculationCreateFormSchema):
    """
    orm wrapper for RequestModel
    """
    id: int  # RequestModel id
    user_id: Union[int, None]
    timestamp: datetime.datetime

    class Config:
        orm_mode = True

    @staticmethod
    def from_request_model(request_model: RequestModel, db):
        request_dict = request_model.__dict__
        request_dict["timestamp"] = request_model.timestamp
        equipment_ids = request_dict["equipment"]
        building_ids = request_dict["buildings"]
        additional_services_ids = request_dict["additional_services"]

        equipment_models = db.query(EquipmentModel).filter(EquipmentModel.id.in_(equipment_ids))
        building_models = db.query(BuildingModel).filter(BuildingModel.id.in_(building_ids))
        additional_services_models = db.query(AdditionalServiceModel).filter(AdditionalServiceModel.id.in_(additional_services_ids))

        equipment_schemas = [EquipmentSchema.from_orm(it) for it in equipment_models]
        equipment_calculation_request_schemas = [
            EquipmentCalculationRequestSchema(id=it.id, amount=amount) for it, amount in
            zip(equipment_schemas, request_dict["equipment_amounts"])
        ]

        building_schemas = [BuildingSchema.from_orm(it) for it in building_models]
        building_calculation_request_schemas = [
            BuildingCalculationRequestSchema(id=it.id, area=area) for it, area in
            zip(building_schemas, request_dict["building_areas"])
        ]

        additional_services_schemas = [AdditionalServiceSchema.from_orm(it) for it in additional_services_models]

        additional_needs_schemas = [
            AdditionalNeedCalculationSchema(name=name, price=price) for name, price in
            zip(request_dict["additional_needs"], request_dict["additional_needs_prices"])
        ]

        request_dict["equipment"] = equipment_calculation_request_schemas
        request_dict["buildings"] = building_calculation_request_schemas
        request_dict["additional_services"] = additional_services_schemas
        request_dict["additional_needs"] = additional_needs_schemas

        return CalculationCreateRequestSchema(**request_dict)


class CalculationPreparedDataSchema(BaseModel):
    # _techincal
    request_id: int


    # business info
    industry_name: str
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

    # accounting services
    accounting_services_documents_amount: int
    accounting_services_expenses: float

    # equipment
    equipments: list[EquipmentCalculationResponseSchema]
    total_equipments_expenses: float

    # buildings
    buildings: list[BuildingCalculationResponseSchema]
    total_buildings_expenses: float

    # additional services
    additional_services: list[AdditionalServiceCalculationResponseSchema]
    total_additional_services_expenses: float

    # additional needs
    additional_needs: list[AdditionalNeedCalculationSchema]
    total_additional_needs_expenses: float

    total_additional_expenses: float
