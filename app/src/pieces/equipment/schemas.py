from pydantic import BaseModel


class EquipmentCreationSchema(BaseModel):
    name: str
    average_price_dollar: float