from fastapi import FastAPI

from app.lifespan import lifespan
from app.routes.file_routes import router as file_router

app = FastAPI(lifespan=lifespan)
app.include_router(file_router)
