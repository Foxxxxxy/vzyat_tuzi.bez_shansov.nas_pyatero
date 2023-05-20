from pydantic import BaseModel


class PatentCreationSchema(BaseModel):
    name: str
    percent_rate: float
    income_rub: float
    price: float


class PatentSchema(PatentCreationSchema):
    id: int

    class Config:
        orm_mode = True
