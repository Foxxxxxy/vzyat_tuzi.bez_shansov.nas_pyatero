from pydantic import BaseModel


class DistrictCreationSchema(BaseModel):
    name: str
    average_price_per_m2_rub: float


class DistrictSchema(DistrictCreationSchema):
    id: int
