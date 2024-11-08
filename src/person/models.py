import uuid

from sqlalchemy import Column, String, UUID, Integer, BOOLEAN
from database import Base

class Person(Base):
    def __init__(self,
                 person_id: uuid.UUID,
                 person_name: str,
                 person_surname: str,
                 person_patronimic: str,
                 person_age: int,
                 person_phone: str,
                 super_user: bool,
                 picture: str):
        self.person_id = person_id
        self.person_name = person_name
        self.person_surname = person_surname
        self.person_patronimic = person_patronimic
        self.person_age = person_age
        self.person_phone = person_phone
        self.super_user = super_user
        self.picture = picture

    __tablename__ = 'person'
    person_id = Column(UUID, primary_key=True)
    person_name = Column(String)
    person_surname = Column(String)
    person_patronimic = Column(String)
    person_age = Column(Integer)
    person_phone = Column(String)
    super_user = Column(BOOLEAN)
    picture = Column(String)
