import base64
import hmac
import string
import uuid
import random
import re
from typing import Tuple

from fastapi import HTTPException, Header
from pydantic import BaseModel

from config import SHA_KEY, SALT


class AccessTokenPayload(BaseModel):
    id: uuid.UUID
    name: str | None
    phone: str
    exp: int
    super_user: bool


async def check_user_agent():
    return 'AndroidUser'


def encrypt(string: str | bytes) -> bytes:
    return hmac.new(SHA_KEY, string.encode() if isinstance(string, str) else string, 'sha256').digest()


def generate_salted_password(password: str | bytes) -> Tuple[bytes, bytes]:
    password = password.encode() if isinstance(password, str) else password
    dynamic_salt = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation)
                           for i in range(64)).encode()
    return encrypt(password + dynamic_salt + SALT), dynamic_salt


def get_salted_password(password: str | bytes, dynamic_salt: bytes):
    password = password.encode() if isinstance(password, str) else password
    return encrypt(password + dynamic_salt + SALT)


def base64_encode(content: str | bytes) -> str:
    if isinstance(content, str):
        content = content.encode()
    return base64.urlsafe_b64encode(content).decode()


def base64_decode(content: str) -> bytes:
    return base64.urlsafe_b64decode(content)


def validate_phone(phone):
    pattern = re.compile(r'^\+79\d{9}$')
    return bool(pattern.match(phone))


def validate_password(password):
    pattern = re.compile(r'^(?=.*\d)(?=.*[a-zA-Zа-яА-Я]).{8,}$')
    return bool(pattern.match(password))