from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine
from app.errors import ConflictError, NotFoundError, ValidationError
from app.routers import (
    auth,
    health,
    roles,
    schedules,
    services,
    staff_members,
    users,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.get("/")
def root():
    return {
        "message": f"Bienvenido a {settings.PROJECT_NAME}",
        "docs": "http://localhost:8000/docs",
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = settings.API_V1_STR
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(health.router, prefix=f"{prefix}/health", tags=["Health"])
app.include_router(auth.router, prefix=f"{prefix}/auth", tags=["Auth"])
app.include_router(roles.router, prefix=f"{prefix}/roles", tags=["Roles"])
app.include_router(users.router, prefix=f"{prefix}/users", tags=["Users"])
app.include_router(services.router, prefix=f"{prefix}/services", tags=["Services"])
app.include_router(
    staff_members.router, prefix=f"{prefix}/staff-members", tags=["Staff"]
)
app.include_router(schedules.router, prefix=f"{prefix}/schedules", tags=["Schedules"])
