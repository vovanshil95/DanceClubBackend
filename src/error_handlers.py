from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler
import logging

LOG = logging.getLogger('main')
logging.basicConfig(level=logging.INFO)

async def http_val_err_handler(request, exception):
    LOG.info(f' 422 error to request with body: {exception.body},\n'
             f'Headers: {request.headers},\n'
             f'Method: {request.method},\n' 
             f'Errors: {exception.errors()}\n')

    return await request_validation_exception_handler(request, exception)


async def http_all_err_handler(request, exception):
    LOG.info(f' {exception.status_code} error\n'
             f'Headers: {request.headers},\n'
             f'Method: {request.method},\n' 
             f'Errors: {exception.detail}\n')

    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.detail}
    )
