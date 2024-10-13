from pydantic import BaseModel

import uuid

class TrainingSign(BaseModel):
    personId: uuid.UUID
    trainingId: uuid.UUID
