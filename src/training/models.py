import datetime
import uuid

from sqlalchemy import Column, String, UUID, TIMESTAMP, Integer
from person.models import Base

class Training(Base):
    def __init__(self,
                 training_id: uuid.UUID,
                 training_name: str,
                 training_description: str,
                 training_date: datetime.datetime,
                 training_status: int,
                 training_space: int,
                 training_free_space: str):
        self.training_id = training_id
        self.training_name = training_name
        self.training_description = training_description
        self.training_date = training_date
        self.training_status = training_status
        self.training_space = training_space
        self.training_free_space = training_free_space

    __tablename__ = 'training'
    training_id = Column(UUID, primary_key=True)
    training_name = Column(String)
    training_description = Column(String)
    training_date = Column(TIMESTAMP)
    training_status = Column(Integer)
    training_space = Column(Integer)
    training_free_space = Column(String)