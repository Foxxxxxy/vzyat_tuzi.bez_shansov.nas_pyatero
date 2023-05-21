from pydantic import BaseModel


class CurrencyCreationSchema(BaseModel):
    name: str
    value: float
