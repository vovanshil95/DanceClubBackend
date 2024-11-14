from sqlalchemy import Column, ForeignKey
from training.models import Base

class TrainingSign(Base):
    def __init__(self,
                 training_id: int,
                 person_id: int):
        self.training_id = training_id
        self.person_id = person_id

    __tablename__ = 'training_sign'
    training_id = Column(ForeignKey('training.training_id', ondelete='cascade'), nullable=False, primary_key=True)
    person_id = Column(ForeignKey('person.person_id', ondelete='cascade'), nullable=False, primary_key=True)