import binascii
import uuid
from datetime import datetime, timedelta
import re

from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from config import REFRESH_TTL_DAYS, ACCESS_TTL_MINUTES
from database import get_async_session
from auth.schemas import Credentials, JwtTokens, UserSign, AccessTokenHeader, \
    RefreshTokenPayload, AccessTokenSchema, Passwords, PersonTokens
from auth.models import Auth, RefreshToken
from person.models import Person
from person.utils import get_profile
from person.schemas import NewUser
from person.schemas import Person as PersonSchema
from auth.utils import encrypt, base64_encode, AccessTokenPayload, base64_decode, check_user_agent, get_salted_password, \
    generate_salted_password
from utils import BaseResponse
from auth.utils import validate_phone, validate_password

router = APIRouter(prefix='/auth',
                   tags=['Auth'])

async def get_access_token(Authorization: str = Header(...)) -> AccessTokenPayload:
    base64_chars = r'[a-zA-Z0-9=_+-/]'
    pattern = re.compile(rf'^Bearer {base64_chars}+\.{base64_chars}+\.{base64_chars}+$')

    if pattern.match(Authorization) is None:
        raise HTTPException(status_code=401, detail='user is not authorized')
    header, payload, sign = Authorization.split('Bearer ')[1].split('.')
    try:
        decoded_sign = base64_decode(sign)
        decoded_payload = base64_decode(payload)
    except binascii.Error:
        raise HTTPException(status_code=498, detail='the access token is invalid')

    if not encrypt(header + '.' + payload) == decoded_sign:
        raise HTTPException(status_code=498, detail='the access token is invalid')

    user_token = AccessTokenPayload.parse_raw(decoded_payload)

    if int(datetime.utcnow().timestamp()) > user_token.exp:
        raise HTTPException(status_code=498, detail='the access token is invalid')

    return user_token

async def get_admin_token(user_token: AccessTokenPayload=Depends(get_access_token)) -> AccessTokenPayload:
    if user_token.role != 'admin':
        raise HTTPException(status_code=403, detail='User has to be admin')
    return user_token

async def get_refresh_token(Authorization: str = Header(...),
                            session: AsyncSession=Depends(get_async_session),
                            user_agent: str=Depends(check_user_agent)) -> RefreshToken:
    try:
        token=RefreshTokenPayload.parse_raw(base64_decode(Authorization.split('Bearer ')[1]))
    except (IndexError, ValueError, binascii.Error, ValidationError):
        raise HTTPException(status_code=498, detail='the refresh token is invalid')

    db_token = (await session.execute(select(RefreshToken)
                        .where(and_(RefreshToken.user_id == token.sub,
                                    RefreshToken.user_agent == user_agent)))).scalars().first()

    if db_token is None:
        raise HTTPException(status_code=404, detail='refresh token not found')
    if db_token.id != token.jti:
        await session.delete(db_token)
        await session.commit()
        raise HTTPException(status_code=401, detail='the refresh token has already been used')

    return db_token


async def check_new_user(request: Request,
                         new_user: NewUser,
                         user_agent: str=Depends(check_user_agent),
                         session: AsyncSession=Depends(get_async_session)) -> UserSign:

    same_user = (await session.execute(select(Person).where(Person.person_phone == new_user.phone))).scalar()
    if same_user:
        if new_user.phone is not None:
            raise HTTPException(detail='user with same phone already exists', status_code=409)

    return UserSign(ip=request.client.host, user_agent=user_agent)

def generate_access_token(user: Person) -> str:
    payload = AccessTokenPayload(id=user.person_id,
                                 name=user.person_name,
                                 phone=user.person_phone,
                                 exp=int((datetime.utcnow() + timedelta(minutes=ACCESS_TTL_MINUTES)).timestamp()),
                                 super_user=user.super_user)

    access_token = base64_encode(AccessTokenHeader().json()) + '.' + base64_encode(payload.json())
    signature = base64_encode(encrypt(access_token))
    signed_access_token = access_token + '.' + signature
    return signed_access_token

def get_new_tokens(user: Person,
                   user_agent: str,
                   session: AsyncSession) -> JwtTokens:

    refresh_token_id = uuid.uuid4()

    session.add(RefreshToken(id=refresh_token_id,
                             user_id=user.person_id,
                             user_agent=user_agent,
                             exp=datetime.utcnow() + timedelta(days=REFRESH_TTL_DAYS),
                             last_use=datetime.utcnow()))
    refresh_token = base64_encode(RefreshTokenPayload(jti=refresh_token_id, sub=user.person_id).json())

    tokens = JwtTokens(refreshToken=refresh_token,
                       accessToken=generate_access_token(user))
    return tokens


async def login(session: AsyncSession,
                phone: str,
                password: str,
                user_agent: str):
    user_auth = (await session.execute(select(Person, Auth)
                                  .join(Auth)
                                  .where(Person.person_phone == phone))).first()

    if user_auth is None:
        raise HTTPException(status_code=404, detail="user with same name doesn't exist")

    user, auth = user_auth

    if get_salted_password(password=password, dynamic_salt=auth.salt) != auth.password:
        raise HTTPException(status_code=401, detail='incorrect username and password')


    if token := (await session.execute(select(RefreshToken)
                        .where(and_(RefreshToken.user_id==user.person_id,
                                    RefreshToken.user_agent == user_agent)))).scalar():
        await session.delete(token)

    jwt_tokens = get_new_tokens(user, user_agent, session)

    return jwt_tokens


@router.post('/login', responses={200: {'model': JwtTokens},
                                       400: {'model': BaseResponse, 'description': 'error: User-Agent required'},
                                       401: {'model': BaseResponse, 'description': 'incorrect username and password'}})
async def login_route(credentials: Credentials,
                session: AsyncSession=Depends(get_async_session),
                user_agent: str=Depends(check_user_agent)) -> JwtTokens:
    
    jwt_tokens = await login(
        session=session,
        phone=credentials.phone,
        password=credentials.password,
        user_agent=user_agent
    )

    return jwt_tokens

@router.post('/logout', responses={200: {'model': BaseResponse},
                                        300: {'model': BaseResponse, 'description': 'user is blocked'},
                                        400: {'model': BaseResponse, 'description': 'error: User-Agent required'},
                                        401: {'model': BaseResponse, 'description': 'user is not authorized'},
                                        498: {'model': BaseResponse, 'description': 'the access token is invalid'}})
async def logout(user_token: AccessTokenPayload=Depends(get_access_token),
                 user_agent: str=Depends(check_user_agent),
                 session: AsyncSession=Depends(get_async_session)) -> BaseResponse:

    refresh_tokens = (await session.execute(select(RefreshToken)
                           .where(and_(RefreshToken.user_agent == user_agent,
                                       RefreshToken.user_id == user_token.id)))).all()
    if refresh_tokens == []:
        await session.execute(delete(RefreshToken).filter(RefreshToken.id == user_token.id))
        raise HTTPException(status_code=300, detail='user is blocked')

    await session.execute(delete(RefreshToken)
                          .where(and_(RefreshToken.user_agent == user_agent,
                                      RefreshToken.user_id == user_token.id)))

    return BaseResponse(message='status success, user logged out')

@router.post('/newTokens', responses={200: {'model': JwtTokens},
                                          401: {'model': BaseResponse, 'description': 'the refresh token has already been used'},
                                          404: {'model': BaseResponse, 'description': 'refresh token not found'},
                                          498: {'model': BaseResponse, 'description': 'the refresh token is invalid'}})
async def give_new_tokens(refresh_token: RefreshToken=Depends(get_refresh_token),
                          session: AsyncSession=Depends(get_async_session)) -> JwtTokens:

    user = await session.get(Person, refresh_token.user_id)
    await session.delete(refresh_token)

    new_tokens = get_new_tokens(user=user,
                                user_agent=refresh_token.user_agent,
                                session=session)

    return new_tokens

@router.post('/newAccessToken', responses={200: {'model': JwtTokens},
                                               401: {'model': BaseResponse, 'description': 'the refresh token has already been used'},
                                               403: {'model': BaseResponse, 'description': 'refresh token expired'},
                                               404: {'model': BaseResponse, 'description': 'refresh token not found'},
                                               498: {'model': BaseResponse, 'description': 'the refresh token is invalid'}})
async def get_new_access_token(refresh_token: RefreshToken=Depends(get_refresh_token),
                           session: AsyncSession=Depends(get_async_session)) -> AccessTokenSchema:
    if datetime.utcnow() > refresh_token.exp:
        raise HTTPException(status_code=403, detail='refresh token expired')


    user = await session.get(Person, refresh_token.user_id)

    refresh_token.last_use = datetime.utcnow()
    session.add(refresh_token)

    return AccessTokenSchema(access_token=generate_access_token(user))

@router.post('/changePassword', responses={200: {'model': PersonSchema},
                                                400: {'model': BaseResponse, 'description': 'error: User-Agent required'},
                                                401: {'model': BaseResponse, 'description': 'user is not authorized'},
                                                409: {'model': BaseResponse, 'description': 'Old password is incorrect'},
                                                498: {'model': BaseResponse, 'description': 'the access token is invalid'}})
async def change_password(passwords: Passwords,
                          user_agent: str=Depends(check_user_agent),
                          session: AsyncSession=Depends(get_async_session),
                          access_token: AccessTokenPayload=Depends(get_access_token)):

    auth = (await session.execute(select(Auth).where(Auth.user_id == access_token.id))).scalar()

    if auth.password != get_salted_password(password=passwords.oldPassword, dynamic_salt=auth.salt):
        raise HTTPException(status_code=409, detail='Old password is wrong')

    encrypted_password, salt = generate_salted_password(passwords.newPassword)

    auth.password = encrypted_password
    auth.salt = salt
    session.add(auth)

    return await get_profile(session, access_token.id, user_agent)

@router.post('/register', 
             responses={200: {'model': PersonTokens},
                        409: {'model': BaseResponse, 'description': 'user with same phone already exists'},
                        400: {'model': BaseResponse, 'description': 'incorrect phone number format'}})
async def register(new_user: NewUser,
                   user_sign: UserSign=Depends(check_new_user),
                   user_agent: str=Depends(check_user_agent),
                   session: AsyncSession=Depends(get_async_session)):
    
    if not validate_phone(new_user.phone):
        raise HTTPException(status_code=400, detail='incorrect phone number format')
    
    if not validate_password(new_user.password):
        raise HTTPException(status_code=400, detail='password should be at least 8 characters long and contain digits and letters')
    

    person_id = uuid.uuid4()
    auth_id = uuid.uuid4()
    encoded_password, salt = generate_salted_password(password=new_user.password)

    session.add(Person(person_id=person_id,
                       person_name=new_user.name,
                       person_surname=new_user.surname,
                       person_age=new_user.age,
                       person_patronimic=new_user.patronimic,
                       person_phone=new_user.phone,
                       super_user=False,
                       picture=new_user.picture))
    
    await session.commit()
    session.add(Auth(
        id=auth_id,
        user_id=person_id,
        password=encoded_password,
        salt=salt
    ))

    await session.commit()
    
    jwt_tokens = await login(
        session=session,
        phone=new_user.phone,
        password=new_user.password,
        user_agent=user_agent
    )

    return PersonTokens(
        person=PersonSchema(
            id=person_id,
            name=new_user.name,
            surname=new_user.surname,
            patronimic=new_user.patronimic,
            age=new_user.age,
            phone=new_user.phone
        ),
        tokens=jwt_tokens
    )
