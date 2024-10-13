from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from training.models import Training
from training_sign.models import TrainingSign
from training.schemas import TrainingsResponse
from training.schemas import Training as TrainingSchema
from database import get_async_session
from utils import BaseResponse

import datetime
import time
import uuid


router = APIRouter(prefix='/training',
                   tags=['training'])


def training_convert(training_data: Training) -> TrainingSchema:
    return TrainingSchema(
        id=training_data.training_id,
        name=training_data.training_name,
        description=training_data.training_description,
        date=int(time.mktime(training_data.training_date.timetuple())),
        status=training_data.training_status,
        space=training_data.training_space,
        freeSpace=training_data.training_free_space
    )


def training_back_convert(training_schema: TrainingSchema) -> Training:
    return Training(
        training_id=training_schema.id,
        training_name=training_schema.name,
        training_description = training_schema.description,
        training_date=datetime.datetime.fromtimestamp(training_schema.date),
        training_status=training_schema.status,
        training_space=training_schema.space,
        training_free_space=training_schema.freeSpace,
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


@router.post('/add')
async def add_training(training: TrainingSchema, session: AsyncSession=Depends(get_async_session)) -> BaseResponse:

    session.add(training_back_convert(training))
    await session.commit()

    return BaseResponse()
