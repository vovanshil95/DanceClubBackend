import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from training_sign.models import TrainingSign
from training_sign.schemas import TrainingSign as TrainingSignSchema
from utils import BaseResponse
from database import get_async_session
from auth.routers import get_access_token
from auth.utils import AccessTokenPayload


router = APIRouter(prefix='/sign',
                   tags=['training_sign'])


@router.post('/add')
async def sign(trainingId: uuid.UUID,
               user_token: AccessTokenPayload=Depends(get_access_token),
               session: AsyncSession=Depends(get_async_session)) -> BaseResponse:
    session.add(TrainingSign(training_id=trainingId,
                             person_id=user_token.id))
    await session.commit()
    
    return BaseResponse()
