import datetime
import uuid

from sqlalchemy import Column, UUID, TIMESTAMP, Integer, ForeignKey
from direction.models import Base
from trainer.models import Base

class Training(Base):
    def __init__(self,
                 training_id: uuid.UUID,
                 trainer_id: str,
                 direction_id: str,
                 training_date: datetime.datetime,
                 training_status: int,
                 training_space: int,
                 training_price: int):
        self.training_id = training_id
        self.direction_id = direction_id
        self.training_date = training_date
        self.training_status = training_status
        self.training_space = training_space
        self.training_price = training_price
        self.trainer_id = trainer_id

    __tablename__ = 'training'
    training_id = Column(UUID, primary_key=True)
    trainer_id = Column(ForeignKey('trainer.trainer_id', ondelete='cascade'), nullable=False, primary_key=False)
    direction_id = Column(ForeignKey('direction.direction_id', ondelete='cascade'), nullable=False, primary_key=False)
    training_date = Column(TIMESTAMP)
    training_status = Column(Integer)
    training_space = Column(Integer)
    training_price = Column(Integer)
