from datetime import datetime
import uuid

from sqlalchemy import Column, LargeBinary, ForeignKey, UUID, TIMESTAMP, String

from person.models import Base

class Auth(Base):
    def __init__(self,
                 id: uuid.UUID,
                 user_id: uuid.UUID,
                 password: bytes,
                 salt: bytes):
        self.id = id
        self.user_id = user_id
        self.password = password
        self.salt = salt

    __tablename__ = 'auth'
    id = Column(UUID, primary_key=True)
    user_id = Column(ForeignKey('person.person_id', ondelete='cascade'), nullable=False)
    password = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)


class RefreshToken(Base):
    def __init__(self,
                 id: uuid.UUID=None,
                 user_id: uuid.UUID=None,
                 user_agent: str=None,
                 exp: datetime=None,
                 last_use: datetime=None):
        self.id = id if id else uuid.uuid4()
        self.user_id = user_id
        self.user_agent = user_agent
        self.exp = exp
        self.last_use = last_use


    __tablename__ = 'refresh_token'
    id = Column(UUID, primary_key=True)
    user_id = Column(ForeignKey('person.person_id', ondelete='cascade'), nullable=False)
    user_agent = Column(String, nullable=False)
    exp = Column(TIMESTAMP, nullable=False)
    last_use = Column(TIMESTAMP)
