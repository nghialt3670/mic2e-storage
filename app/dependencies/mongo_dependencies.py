from fastapi import Request
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorGridFSBucket,
)


def get_client(request: Request) -> AsyncIOMotorClient:
    return request.app.state.client


def get_db(request: Request) -> AsyncIOMotorDatabase:
    return request.app.state.db


def get_bucket(request: Request) -> AsyncIOMotorGridFSBucket:
    return request.app.state.bucket
