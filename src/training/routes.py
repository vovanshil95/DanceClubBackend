from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from training.models import Training
from training_sign.models import TrainingSign
from person.models import Person
from training.schemas import TrainingsResponse
from training.schemas import Training as TrainingSchema
from database import get_async_session

import datetime
import time
import uuid


router = APIRouter(prefix='/training',
                   tags=['training'])


def training_convert(training_data: list) -> TrainingSchema:
    return TrainingSchema(
        id=training_data.training_id,
        name=training_data.training_name,
        description=training_data.training_description,
        date= int(time.mktime(training_data.training_date.timetuple())),
        status=training_data.training_status,
        space=training_data.training_space,
        freeSpace=training_data.training_free_space
    )

@router.get('/all')
async def get_future_trainings(session: AsyncSession=Depends(get_async_session)) -> TrainingsResponse:

    traings_data = (await session.execute(select(Training)
                    .where(Training.training_date > datetime.datetime.now()))).scalars().all()
    
    return TrainingsResponse(trainings=[training_convert(t) for t in traings_data])


@router.get('/signed')
async def get_signed_trainings(person_id: uuid.UUID, session: AsyncSession=Depends(get_async_session)  ) -> TrainingsResponse:

    traings_data = (await session.execute(select(Training)
                    .join(TrainingSign)
                    .where(and_(Training.training_date > datetime.datetime.now(),
                                TrainingSign.person_id == person_id)))).scalars().all()

    return TrainingsResponse(trainings=[training_convert(t) for t in traings_data])
