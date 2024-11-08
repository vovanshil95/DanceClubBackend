from pydantic import BaseModel

from utils import BaseResponse
from config import DEFAULT_PHONE

from typing import List
import uuid

class NewUser(BaseModel):
    name: str=None
    surname: str
    patronimic: str
    age: int
    phone: str=DEFAULT_PHONE
    password: str
    picture: str


class Person(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    patronimic: str
    age: int
    phone: str
    picture: str | None


class PersonResponse(BaseResponse):
    data: Person


class PersonsResponse(BaseResponse):
    persons: List[Person]