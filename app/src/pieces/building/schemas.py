from pydantic import BaseModel


class BuildingCreationSchema(BaseModel):
    name: str
    average_price_rub: float


class BuildingSchema(BuildingCreationSchema):
    id: int

    class Config:
        orm_mode = True
