import datetime
import uuid

from sqlalchemy import Column, String, UUID, TIMESTAMP, BOOLEAN, LargeBinary, ForeignKey
from database import Base
class Person(Base):
    def __init__(self,
                 person_id: uuid.UUID,
                 person_name: str,
                 person_surname: str,
                 person_patronimic: str,
                 person_birth_date: datetime.datetime,
                 person_phone: str,
                 super_user: bool):
        self.person_id = person_id
        self.person_name = person_name
        self.person_surname = person_surname
        self.person_patronimic = person_patronimic
        self.person_birth_date = person_birth_date
        self.person_phone = person_phone
        self.super_user = super_user

    __tablename__ = 'person'
    person_id = Column(UUID, primary_key=True)
    person_name = Column(String)
    person_surname = Column(String)
    person_patronimic = Column(String)
    person_birth_date = Column(TIMESTAMP)
    person_phone = Column(String)
    super_user = Column(BOOLEAN)


class Picture(Base):
    def __init__(self,
                 user_id: uuid.UUID,
                 data: bytes):
        self.user_id = user_id
        self.data = data

    __tablename__ = 'profile_picture'

    user_id = Column(ForeignKey('person.person_id', ondelete='cascade'), primary_key=True)
    data = Column(LargeBinary, nullable=False)
