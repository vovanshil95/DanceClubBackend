import uuid

from sqlalchemy import Column, String, UUID
from database import Base

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
