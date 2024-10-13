from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from training.routes import router as training_router
from training_sign.routers import router as sign_router
from person.routers import router as person_router


from config import ORIGINS

app = FastAPI(title='DanceClub API',
              description='here is backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(training_router)
app.include_router(sign_router)
app.include_router(person_router)
