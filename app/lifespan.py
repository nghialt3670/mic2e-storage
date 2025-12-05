from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from app.env import MONGODB_URI


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = AsyncIOMotorClient(MONGODB_URI)
    app.state.db = app.state.client.get_database()
    app.state.bucket = AsyncIOMotorGridFSBucket(app.state.db)
    yield
    app.state.client.close()
