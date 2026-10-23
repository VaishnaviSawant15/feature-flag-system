from fastapi import FastAPI

from app.config import settings
from app.routers import health

app = FastAPI(title=settings.app_name, debug=settings.debug, version="0.1.0")

app.include_router(health.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": f"{settings.app_name} is running", "docs": "/docs"}
