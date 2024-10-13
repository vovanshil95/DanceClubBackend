from pydantic import BaseModel
from utils import BaseResponse

from typing import List
import uuid

class Person(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    patronimic: str
    age: int
    phone: str


class PersonsResponse(BaseResponse):
    persons: List[Person]