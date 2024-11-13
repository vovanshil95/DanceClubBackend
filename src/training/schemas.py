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
    price: int
    trainerName: str
    trainerDescriptions: str


class NewTraining(BaseModel):
    directionId: uuid.UUID
    date: int
    status: int
    space: int
    price: int
    trainerId: uuid.UUID


class TrainingsResponse(BaseResponse):
    trainings: list[Training]


class TrainingResponse(BaseResponse):
    training: Training
