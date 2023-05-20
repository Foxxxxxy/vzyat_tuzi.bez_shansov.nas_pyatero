from pydantic import BaseModel


class IndustryCreationSchema(BaseModel):
    name: str


class IndustrySchema(IndustryCreationSchema):
    id: int
