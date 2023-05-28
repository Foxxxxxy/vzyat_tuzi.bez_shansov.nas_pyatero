from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EUserLevel(int, Enum):
    user = 1
    moderator = 2
    admin = 3


# todo from typing import Optional сделать поля Optional
class SignUpSchema(BaseModel):
    password: str
    level: EUserLevel

    email: str
    name: str
    last_name: str
    organisation_name: str
    inn: str
    web_site: str

    fathers_name: str
    industry_id: Optional[int] = None
    country: str
    city: str
    position: str


class UserOutputSchema(BaseModel):
    id: int
    level: int

    email: str
    name: str
    last_name: str
    organisation_name: str
    inn: str
    web_site: str

    fathers_name: str
    industry_id: Optional[int] = None
    country: str
    city: str
    position: str

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    level: Optional[int] = None

    email: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    organisation_name: Optional[str] = None
    inn: Optional[str] = None
    web_site: Optional[str] = None

    fathers_name: Optional[str] = None
    industry_id: Optional[int] = None
    country: Optional[str] = None
    city: Optional[str] = None
    position: Optional[str] = None
