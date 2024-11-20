from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

import uuid

from auth.utils import AccessTokenPayload
from auth.routers import get_access_token
from database import get_async_session
from trainer.models import Picture
from utils import BaseResponse, PictureResponse
from utils import Picture as PictureSchema


router = APIRouter(prefix='/trainer',
                   tags=['trainer'])


@router.get('/picture')
async def get_picture(trainer_id: uuid.UUID,
                      access_token: AccessTokenPayload=Depends(get_access_token),
                      session: AsyncSession=Depends(get_async_session)) -> PictureResponse:
    picture = await session.get(Picture, trainer_id)
    if picture is None:
        return PictureResponse(image=None)
    return PictureResponse(image=picture.data)


@router.put('/picture')
async def add_picture(trainer_id: uuid.UUID,
                      picture: PictureSchema,
                      access_token: AccessTokenPayload=Depends(get_access_token),
                      session: AsyncSession=Depends(get_async_session)) -> BaseResponse:
    
    if len((await session.execute(select(Picture.trainer_id).where(Picture.trainer_id == trainer_id))).all()) > 0:
        stmt = update(Picture).where(Picture.trainer_id == trainer_id).values({'data': picture.image})
        session.not_awaited.append(session.execute(stmt))
    else:
        session.add(Picture(trainer_id=trainer_id, data=picture.image))

    return BaseResponse()
