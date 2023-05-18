from enum import Enum

from pydantic import BaseModel
from typing import Union, List, Optional
from .models import LegalEntityType

#fn shift f6


class MainInput(BaseModel):
    industry_id: int  # id сферы хоз деятельности (todo)
    subindustry_id: Optional[int]
    employee_amount: int # количество рабочих, чел


    building_area_size: float # площадь здания, м2
    land_area_size: float  # площадь земельного участка, м2

    equipment_id: int # оборудование

    legal_entity_type: LegalEntityType


    # todo
    # building = List[Building] список зданий и цены по их кв метру и их размер в кв м


    # todo
    # данные для рассчета бухгалтерского калькулятора

    predicted_income_per_year_rub: int  # предполагаемый доход в год - для подсчета стоимости патента

    # todo
    # иные потребности List[Потребность]

