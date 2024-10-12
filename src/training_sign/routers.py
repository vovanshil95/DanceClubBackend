from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from training_sign.models import TrainingSign
from utils import BaseResponse
from database import get_async_session

import uuid


router = APIRouter(prefix='/sign',
                   tags=['training_sign'])


@router.get('/add')
async def sign(person_id: uuid.UUID,
               training_id: uuid.UUID,
               session: AsyncSession=Depends(get_async_session)  ) -> BaseResponse:
    session.add(TrainingSign(training_id, person_id))
    await session.commit()
    
    return BaseResponse()
