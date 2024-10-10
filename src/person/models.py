import uuid

from sqlalchemy import Column, String, UUID, TIMESTAMP, Float, Integer
from database import Base

class Person(Base):
    def __init__(self,
                 person_id: uuid.UUID,
                 person_name: str,
                 person_surname: str,
                 person_patronimic: str,
                 person_age: int,
                 person_phone: str):
        self.person_id = person_id
        self.person_name = person_name
        self.person_surname = person_surname
        self.person_patronimic = person_patronimic
        self.person_age = person_age
        self.person_phone = person_phone

    __tablename__ = 'person'
    person_id = Column(UUID, primary_key=True)
    person_name = Column(String)
    person_surname = Column(String)
    person_patronimic = Column(String)
    person_age = Column(Integer, autoincrement=False)
    person_phone = Column(String)