from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from person.models import Person
from person.schemas import Person as PersonSchema, PersonsResponse
from database import get_async_session
from auth.routers import get_access_token
from auth.utils import AccessTokenPayload


router = APIRouter(prefix='/person',
                   tags=['person'])


def person_convert(person_data: Person) -> PersonSchema:
    return PersonSchema(
        id=person_data.person_id,
        name=person_data.person_name,
        surname=person_data.person_surname,
        patronimic=person_data.person_patronimic,
        age=person_data.person_age,
        phone=person_data.person_phone,
        picture=person_data.picture
    )

@router.get('/all')
async def add_person(access_token: AccessTokenPayload=Depends(get_access_token),
                     session: AsyncSession=Depends(get_async_session)) -> PersonsResponse:

    # if not access_token.super_user:
    #     raise HTTPException(status_code=403, detail='forbidden')

    persons = (await session.execute(select(Person))).scalars().all()
    persons = [person_convert(person) for person in persons]

    return PersonsResponse(persons=persons)
