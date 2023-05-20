from pydantic import BaseModel


class AdditionalServiceCreationSchema(BaseModel):
    name: str
    average_price_dollar: float


class AdditionalServiceSchema(AdditionalServiceCreationSchema):
    id: int

    class Config:
        orm_mode = True

