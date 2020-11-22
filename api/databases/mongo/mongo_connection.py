import motor
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from api.config.main import main_config


def _get_mongo_client(request: Request) -> AsyncIOMotorClient:
    return request.app.state.mongo_client


async def get_mongo_client(mongo_client: AsyncIOMotorClient = Depends(_get_mongo_client)):
    return mongo_client


async def create_mongo_client():
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(main_config.mongo_url)
    return mongo_client
