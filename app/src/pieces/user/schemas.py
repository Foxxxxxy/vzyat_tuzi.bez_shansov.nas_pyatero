from enum import Enum

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


class UserOutputSchema(BaseModel):
    id: int
    level: int

    email: str
    name: str
    last_name: str
    organisation_name: str
    inn: str
    web_site: str

    class Config:
        orm_mode = True
