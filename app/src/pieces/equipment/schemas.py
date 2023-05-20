from pydantic import BaseModel


class EquipmentCreationSchema(BaseModel):
    name: str
    average_price_dollar: float

class EquipmentSchema(EquipmentCreationSchema):
    id: int





#1. - класс оборудования - EquipmentSchema
# ткацкий станок
#2. - запрос пользователя list[EquipmentCalculationRequest]
# ткацкий станок - 5, токарный станок - 7
#3. - результат по каждому классу list[EquipmentCalculationResponse]
# ткацкий станок - 5, всего 500 р, токарный станок - 7, 400

class EquipmentExpensesInfo


class EquipmentCac