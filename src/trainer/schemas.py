from pydantic import BaseModel

from utils import BaseResponse

from typing import List
import uuid

class NewTrainer(BaseModel):
    name: str=None
    description: str


class Trainer(BaseModel):
    id: uuid.UUID
    name: str
    description: str


class TrainerResponse(BaseResponse):
    data: Trainer


class TrainerResponse(BaseResponse):
    persons: List[Trainer]