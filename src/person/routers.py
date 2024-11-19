from fastapi import APIRouter, Depends, Body
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from person.models import Person, Picture
from person.schemas import Person as PersonSchema, PersonsResponse
from database import get_async_session
from auth.routers import get_access_token
from auth.utils import AccessTokenPayload
from utils import BaseResponse

import time

router = APIRouter(prefix='/person',
                   tags=['person'])


def person_convert(person_data: Person) -> PersonSchema:
    return PersonSchema(
        id=person_data.person_id,
        name=person_data.person_name,
        surname=person_data.person_surname,
        patronimic=person_data.person_patronimic,
        birth_date=int(time.mktime(person_data.person_birth_date.timetuple())),
        phone=person_data.person_phone,
    )

@router.get('/all')
async def add_person(access_token: AccessTokenPayload=Depends(get_access_token),
                     session: AsyncSession=Depends(get_async_session)) -> PersonsResponse:


    persons = (await session.execute(select(Person))).scalars().all()
    persons = [person_convert(person) for person in persons]

    return PersonsResponse(persons=persons)

@router.get('/picture')
async def get_picture(access_token: AccessTokenPayload=Depends(get_access_token),
                      session: AsyncSession=Depends(get_async_session)) -> bytes | None:
    picture = await session.get(Picture, access_token.id)
    if picture is None:
        return None
    return picture.data


@router.put('/picture')
async def get_picture(data: bytes = Body(...),
                      access_token: AccessTokenPayload=Depends(get_access_token),
                      session: AsyncSession=Depends(get_async_session)) -> BaseResponse:
    
    if len((await session.execute(select(Picture.user_id).where(Picture.user_id == access_token.id))).all()) > 0:
        stmt = update(Picture).where(Picture.user_id == access_token.id).values({'data': data})
        session.not_awaited.append(session.execute(stmt))
    else:
        session.add(Picture(user_id=access_token.id, data=data))

    return BaseResponse()
