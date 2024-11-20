import uuid

from sqlalchemy import Column, String, UUID, LargeBinary, ForeignKey
from direction.models import Base

class Trainer(Base):
    def __init__(self,
                 trainer_id: uuid.UUID,
                 trainer_name: str,
                 trainer_description: str):
    
        self.trainer_id = trainer_id
        self.trainer_name = trainer_name
        self.trainer_description = trainer_description

    __tablename__ = 'trainer'
    trainer_id = Column(UUID, primary_key=True)
    trainer_name = Column(String)
    trainer_description = Column(String)


class Picture(Base):
    def __init__(self,
                 trainer_id: uuid.UUID,
                 data: bytes):
        self.trainer_id = trainer_id
        self.data = data

    __tablename__ = 'trainer_picture'

    trainer_id = Column(ForeignKey('trainer.trainer_id', ondelete='cascade'), primary_key=True)
    data = Column(LargeBinary, nullable=False)
