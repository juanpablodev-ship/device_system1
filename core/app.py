from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import settings
from core.database import engine, Base
from core.exceptions import AppException
from api.v1.router import api_router
from core.middleware import RequestTimingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


application = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
)

application.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])
application.add_middleware(RequestTimingMiddleware)


@application.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message, "code": exc.error_code})


application.include_router(api_router, prefix="/api/v1")


@application.get("/ping", tags=["System"])
def pong():
    return {"reply": "pong", "version": settings.API_VERSION}
