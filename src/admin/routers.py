from fastapi import APIRouter
from fastapi.responses import FileResponse



router = APIRouter(prefix='/amdin',
                   tags=['amdin'])


@router.get("/logs")
async def get_logs():
    return FileResponse('./output.log')
