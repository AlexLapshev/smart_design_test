import asyncio

import motor.motor_asyncio
import pytest

from fastapi.testclient import TestClient
from loguru import logger


from api.tests.data.data_for_testing import products

mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://smart_design_user:123456@0.0.0.0:27017/smart_design_mongo')
mongo_collection = mongo_client.smart_design_mongo.products


@pytest.fixture(scope="session")
def client():
    from api.main import app
    with TestClient(app, base_url='http://0.0.0.0:1984/api/v1/') as client:
        yield client


def _remove_from_mongo():
    logger.debug('removing from mongo')
    asyncio.get_event_loop().run_until_complete(mongo_collection.delete_many({}))


@pytest.fixture(scope='function')
def insert_products_in_mongo():
    logger.debug('inserting products in mongo')
    asyncio.get_event_loop().run_until_complete(mongo_collection.insert_many(products))
    yield
    _remove_from_mongo()


@pytest.fixture(scope="session", autouse=True)
def main():
    logger.debug('starting tests')
    yield
    _remove_from_mongo()
