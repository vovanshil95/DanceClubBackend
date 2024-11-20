import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from training_sign.models import TrainingSign
from training.models import Training
from training_sign.schemas import TrainingSign as TrainingSignSchema
from utils import BaseResponse
from database import get_async_session
from auth.routers import get_access_token
from auth.utils import AccessTokenPayload


router = APIRouter(prefix='/sign',
                   tags=['training_sign'])


@router.post('/add', responses={200: {'model': BaseResponse, 'description': 'Successful Response'}
                                403: {'model': BaseResponse, 'description': 'user is not authorized'},
                                409: {'model': BaseResponse, 'description': 'user already signed to training'},
                                404: {'model': BaseResponse, 'description': 'training doesnt exist'},
                                400: {'model': BaseResponse, 'description': 'training has no free space'}})
async def sign(trainingId: uuid.UUID,
               user_token: AccessTokenPayload=Depends(get_access_token),
               session: AsyncSession=Depends(get_async_session)) -> BaseResponse:
    
    trainig = await session.get(Training, trainingId)

    if trainig is None:
        raise HTTPException(status_code=404, detail='training doesnt exist')

    sign = await session.get(TrainingSign, (trainingId, user_token.id))

    if sign is not None:
        raise HTTPException(status_code=409, detail='user already signed to training')
    
    signs = (await session.execute(select(func.count())
            .where(TrainingSign.training_id == trainingId))).scalar()
    
    if signs >= trainig.training_space:
        raise HTTPException(400, detail='training has no free space')

    session.add(TrainingSign(training_id=trainingId,
                             person_id=user_token.id))
    await session.commit()
    
    return BaseResponse()
