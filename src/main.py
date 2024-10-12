from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from training.routes import router as training_router
from training_sign.routers import router as sign_router

from config import ORIGINS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(training_router)
app.include_router(sign_router)
'a99ed1ea-49c9-4cf4-83a3-5ca4cfe3bf8f'






'4aeebe0d-60f0-4905-9e40-92d739f9a866'

'24353782-7249-4a64-beaa-445f5b39d076'