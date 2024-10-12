import uuid

from sqlalchemy import Column, UUID, Integer
from training.models import Base

class Training_sign(Base):
    def __init__(self,
                 sign_id: uuid.UUID,
                 training_id: int,
                 person_id: int):
        self.sign_id = sign_id
        self.training_id = training_id
        self.person_id = person_id

    __tablename__ = 'training_sign'
    sign_id = Column(UUID, primary_key=True)
    training_id = Column(Integer)
    person_id = Column(Integer)