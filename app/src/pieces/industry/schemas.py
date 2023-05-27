from pydantic import BaseModel


class IndustryCreationSchema(BaseModel):
    name: str
    avg_salary: float


class IndustrySchema(IndustryCreationSchema):
    id: int

    class Config:
        orm_mode = True
