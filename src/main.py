from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from training.routes import router as training_router
from training_sign.routers import router as sign_router
from person.routers import router as person_router
from auth.routers import router as auth_router


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
app.include_router(auth_router)


def custom_openapi():
    openapi_schema = get_openapi(
        title='FastAPI',
        version='0.1.0',
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
