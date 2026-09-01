from fastapi import FastAPI

from app.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
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
