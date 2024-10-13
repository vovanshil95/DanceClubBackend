from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from person.models import Person
from person.schemas import Person as PersonSchema, PersonsResponse
from database import get_async_session
from utils import BaseResponse


router = APIRouter(prefix='/person',
                   tags=['person'])


def person_convert(person_data: Person) -> PersonSchema:
    return PersonSchema(
        id=person_data.person_id,
        name=person_data.person_name,
        surname=person_data.person_surname,
        patronimic=person_data.person_patronimic,
        age=person_data.person_age,
        phone=person_data.person_phone
    )


def person_back_convert(person_shema: PersonSchema) -> Person:
    return Person(
        person_id=person_shema.id,
        person_name=person_shema.name,
        person_surname=person_shema.surname,
        person_patronimic=person_shema.patronimic,
        person_age=person_shema.age,
        person_phone=person_shema.phone
    )


@router.post('/add')
async def add_person(person: PersonSchema, session: AsyncSession=Depends(get_async_session)  ) -> BaseResponse:

    session.add(person_back_convert(person))
    await session.commit()

    return BaseResponse()


@router.get('/all')
async def add_person(session: AsyncSession=Depends(get_async_session)  ) -> PersonsResponse:

    persons = (await session.execute(select(Person))).scalars().all()
    persons = [person_convert(person) for person in persons]

    return PersonsResponse(persons=persons)