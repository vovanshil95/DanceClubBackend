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
import logging



router = APIRouter(prefix='/training',
                   tags=['training'])


def training_convert(training_data: Training,
                     signs: int,
                     trainer_name: str,
                     trainer_description: str,
                     directionName: str,
                     directionDescription: str) -> TrainingSchema:
    return TrainingSchema(
        id=training_data.training_id,
        name=directionName,
        description=directionDescription,
        date=int(time.mktime(training_data.training_date.timetuple())),
        status=training_data.training_status,
        space=training_data.training_space,
        freeSpace=max(0, training_data.training_space - signs),
        price = training_data.training_price,
        trainerId=training_data.trainer_id,
        trainerName = trainer_name,
        trainerDescriptions=trainer_description
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
        .outerjoin(Trainer, Training.trainer_id == Trainer.trainer_id)
        .outerjoin(Direction, Training.direction_id == Direction.direction_id)
        .where(Training.training_date > datetime.datetime.now())
        .group_by(Training.training_id, Trainer.trainer_name, Trainer.trainer_description, Direction.direction_name, Direction.direction_description) 
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
        .outerjoin(Trainer, Training.trainer_id == Trainer.trainer_id)
        .outerjoin(Direction, Training.direction_id == Direction.direction_id)
        .where(Training.training_date > datetime.datetime.now())
        .group_by(Training.training_id, Trainer.trainer_name, Trainer.trainer_description, Direction.direction_name, Direction.direction_description) 
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
    
    trainer_id = (await session.execute(select(Trainer.trainer_id)
                                   .where(Trainer.trainer_name == training.trainerName))).scalar()


    if trainer_id is None:
        trainer_id = uuid.uuid4()
        session.add(Trainer(trainer_id=trainer_id,
                            trainer_name=training.trainerName,
                            trainer_description=training.trainerDescriptions))
        await session.commit()
        
        
    direction_id = (await session.execute(select(Direction.direction_id)
                                   .where(Direction.direction_name == training.name))).scalar()
    if direction_id is None:
        direction_id = uuid.uuid4()
        session.add(Direction(direction_id=direction_id,
                              direction_name=training.name,
                              direction_description=training.description))
        await session.commit()

    training_date_raw = training.date
    training.date = datetime.datetime.fromtimestamp(training.date)
    
    session.add(Training(training_id=training_id,
                         trainer_id=trainer_id,
                         direction_id=direction_id,
                         training_date=training.date,
                         training_status=training.status,
                         training_space=training.space,
                         training_price=training.price))

    await session.commit()
    

    training.date = training_date_raw
    
    training = training.dict()
    training.update({'id': training_id, 'freeSpace': training['space']})
    return TrainingResponse(training=TrainingSchema(**training))
