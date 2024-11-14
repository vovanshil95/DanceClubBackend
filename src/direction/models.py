import uuid

from sqlalchemy import Column, String, UUID
from auth.models import Base

class Direction(Base):
    def __init__(self,
                 direction_id: uuid.UUID,
                 direction_name: str,
                 direction_description: str):
        
        self.direction_id = direction_id
        self.direction_name = direction_name
        self.direction_description = direction_description

    __tablename__ = 'direction'
    direction_id = Column(UUID, primary_key=True)
    direction_name = Column(String)
    direction_description = Column(String)