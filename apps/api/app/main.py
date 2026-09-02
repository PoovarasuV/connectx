from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.phone_auth import router as phone_auth_router
from app.api.v1.profile import router as profile_router
from app.api.v1.preferences import router as preferences_router
from app.config import settings
from app.api.v1.interests import router as interests_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    users_router,
    prefix="/api/v1",
)

app.include_router(
    phone_auth_router,
    prefix="/api/v1",
)

app.include_router(
    profile_router,
    prefix="/api/v1",
)
app.include_router(
    preferences_router,
    prefix="/api/v1",
)

app.include_router(
    interests_router,
    prefix="/api/v1",
)
@app.get("/")
def root():
    return {
        "message": "ConnectX API is running",
        "environment": settings.app_env,
        "version": settings.app_version,
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": settings.app_env,
    }
