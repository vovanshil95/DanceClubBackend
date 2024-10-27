import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from person.models import Person
from person.schemas import Person as PersonSchema 
from person.schemas import PersonResponse
    

async def get_profile(session: AsyncSession, user_id: uuid.UUID, user_agent: str) -> PersonResponse:
    person = await session.get(Person, user_id)

    return PersonResponse(
        data=PersonSchema(
            id=person.person_id,
            name=person.person_name,
            surname=person.person_surname,
            patronimic=person.person_patronimic,
            age=person.person_age,
            phone=person.person_phone
        )
    )
