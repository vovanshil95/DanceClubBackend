from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from training_sign.models import TrainingSign
from training_sign.schemas import TrainingSign as TrainingSignSchema
from utils import BaseResponse
from database import get_async_session


router = APIRouter(prefix='/sign',
                   tags=['training_sign'])


@router.post('/add')
async def sign(training_sign: TrainingSignSchema,
               session: AsyncSession=Depends(get_async_session)) -> BaseResponse:
    session.add(TrainingSign(training_sign.trainingId, training_sign.personId))
    await session.commit()
    
    return BaseResponse()
