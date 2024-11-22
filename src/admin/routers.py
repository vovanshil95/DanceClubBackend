from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter(prefix='/admin',
                   tags=['admin'])


async def stream():
    with open('./output.log', 'rb') as file:
        while True:
            chunk = file.read(8192)
            if not chunk:
                break
            yield chunk


@router.get("/logs")
async def get_logs():
    return StreamingResponse(stream(), media_type="application/octet-stream", 
        headers={"Content-Disposition": f"attachment; filename=output.log"})
