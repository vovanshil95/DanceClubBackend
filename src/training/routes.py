from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from trainer.schemas import TrainerResponse

from training.models import Training
from training_sign.models import TrainingSign
from trainer.models import  Trainer
from direction.models import Direction
from training.schemas import TrainingsResponse, TrainingResponse
from training.schemas import Training as TrainingSchema
from training.schemas import NewTraining


from database import get_async_session
from utils import BaseResponse
from auth.utils import AccessTokenPayload
from auth.routers import get_access_token 


import datetime
import time
import uuid


router = APIRouter(prefix='/training',
                   tags=['training'])


def training_convert(training_data: Training, signs: int, trainer_name, trainer_description, directionName, directionDescription) -> TrainingSchema:
    return TrainingSchema(
        id=training_data.training_id,
        name=directionName,
        description=directionDescription,
        date=int(time.mktime(training_data.training_date.timetuple())),
        status=training_data.training_status,
        space=training_data.training_space,
        freeSpace=max(0, training_data.training_space - signs),
        price = training_data.training_price,
        trainerName = trainer_name,
        trainerDescriptions=trainer_description
    )


def training_back_convert(training_schema: TrainingSchema) -> Training:
    return Training(
        training_id=training_schema.id,
        trainer_id=training_schema.name,
        training_description = training_schema.description,
        training_date=datetime.datetime.fromtimestamp(training_schema.date),
        training_status=training_schema.status,
        training_space=training_schema.space,
        training_price=training_schema.price,
        trainer_id=training_schema.trainerId
    )


@router.get('/all')
async def get_future_trainings(session: AsyncSession=Depends(get_async_session)) -> TrainingsResponse:

    query = (
        select(Training,
               func.count(TrainingSign.person_id).label('training_sings'),
               Trainer.trainer_name,
               Trainer.trainer_description,
               Direction.direction_name,
               Direction.direction_description)
        .outerjoin(TrainingSign, Training.training_id == TrainingSign.training_id)
        .outherjoin(Trainer, Training.trainer_id == Trainer.trainer_id)
        .outherjoin(Direction, Training.direction_id == Direction.trainer_id)
        .where(Training.training_date > datetime.datetime.now())
        .group_by(Training.training_id)
        .order_by(Training.training_date)
    )

    trainings_data = (await session.execute(query)).all()

    return TrainingsResponse(trainings=[training_convert(tr, signs, tName, tDescription, dName, dDescription) 
                                        for tr, signs, tName, tDescription, dName, dDescription in trainings_data])


@router.get('/signed')
async def get_signed_trainings(access_token: AccessTokenPayload=Depends(get_access_token),
                               session: AsyncSession=Depends(get_async_session)) -> TrainingsResponse:

    query = (
        select(Training,
               func.count(TrainingSign.person_id).label('training_sings'),
               Trainer.trainer_name,
               Trainer.trainer_description,
               Direction.direction_name,
               Direction.direction_description)
        .outerjoin(TrainingSign, Training.training_id == TrainingSign.training_id)
        .outherjoin(Trainer, Training.trainer_id == Trainer.trainer_id)
        .outherjoin(Direction, Training.direction_id == Direction.trainer_id)
        .where(Training.training_date > datetime.datetime.now())
        .group_by(Training.training_id)
        .order_by(Training.training_date)
    )

    trainings_data = (await session.execute(query)).all()
    training_ids = (await session.execute(select(TrainingSign.training_id)
                                         .where(TrainingSign.person_id == access_token.id))).scalars().all()
    

    return TrainingsResponse(trainings=[training_convert(tr, signs, tName, tDescription, dName, dDescription) 
                                        for tr, signs, tName, tDescription, dName, dDescription 
                                        in trainings_data if tr.training_id in training_ids])


@router.post('/add')
async def add_training(training: NewTraining,
                       access_token: AccessTokenPayload=Depends(get_access_token),
                       session: AsyncSession=Depends(get_async_session)) -> TrainingResponse:

    training_id = uuid.uuid4()

    training_date_raw = training.date
    training.date = datetime.datetime.fromtimestamp(training.date)

    session.add(Training(
        *([training_id] + list(training.dict().values()))
    ))
    await session.commit()

    training.date = training_date_raw
    
    training = training.dict()
    training.update({'id': training_id, 'freeSpace': training['space']})
    return TrainingResponse(training=TrainingSchema(**training))
