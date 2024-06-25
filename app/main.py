from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from firebase_admin import credentials as firebase_credentials, initialize_app as init_firebase
from app.routers import patients
from app.settings import get_settings
from app.middleware import handle_uncaught_exceptions, handle_validation_error
from app.routers import auth
from app.models import initialize_mongodb
from app.logs import get_logger

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager# User routes

async def lifespan(app: FastAPI): # pylint: disable=unused-argument
    init_firebase(firebase_credentials.Certificate(settings.firebase_config))
    await initialize_mongodb()
    logger.info("Emails are %s", "enabled" if not settings.disable_email else "disabled")
    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan, root_path=settings.root_path)
app.middleware("http")(handle_uncaught_exceptions)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await handle_validation_error(request, exc)


# User routes
app.include_router(patients.router)

# Auth routes
app.include_router(auth.router)
