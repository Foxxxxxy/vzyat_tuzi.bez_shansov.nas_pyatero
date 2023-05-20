from pydantic import BaseModel
from typing import Optional

from app.src.pieces.calculation.models import LegalEntityType


class CalculationCreateFormSchema(BaseModel):
    industry_id: int  # id сферы хоз деятельности todo таблица сфер хоз деятельности
    subindustry_id: Optional[int]
    employee_amount: int  # количество рабочих, чел

    building_area_size: float  # площадь здания, м2
    land_area_size: float  # площадь земельного участка, м2

    equipment_id: int  # оборудование todo таблица оборудования

    legal_entity_type: LegalEntityType

    predicted_income_per_year_rub: int  # предполагаемый доход в год - для подсчета стоимости патента


    # todo
    # building = List[Building] список зданий и цены по их кв метру и их размер в кв м


    # todo
    # данные для рассчета бухгалтерского калькулятора

    # todo
    # иные потребности List[Потребность]
