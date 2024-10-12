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
    freeSpace: str

class TrainingsResponse(BaseResponse):
    trainings: list[Training]

# class NewTemplate(BaseModel):
#     templateId: uuid.UUID
#     title: str
#     newAnswers: list[NewAnswer]