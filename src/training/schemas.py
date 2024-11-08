import uuid

from pydantic import BaseModel

from utils import BaseResponse


class Training(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    date: int
    status: int
    space: int
    freeSpace: int


class NewTraining(BaseModel):
    name: str
    description: str
    date: int
    status: int
    space: int


class TrainingsResponse(BaseResponse):
    trainings: list[Training]


class TrainingResponse(BaseResponse):
    training: Training
