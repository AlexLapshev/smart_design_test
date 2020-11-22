from typing import List

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from api.services.products.schemas import ProductSchema
from api.services.products.utils import ProductSerializer


class ProductCRUD:

    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_collection = mongo_client.smart_design_mongo.products

    async def get_product_by_id(self, product_id: int) -> ProductSchema:
        logger.debug(f'getting product by id: {product_id}')
        if product := await self.mongo_collection.find_one({'_id': product_id}):
            product = ProductSerializer(product).replace_id_key()
            return ProductSchema(**product)

    async def get_filtered_products(self, filters: dict, skip: int = 0,
                                    length: int = 10) -> List[ProductSchema]:
        logger.debug(f'getting filtered products filtered: {filters}')
        products = await self.mongo_collection.find(filters).skip(skip=skip).to_list(length=length)
        products = [ProductSerializer(product).replace_id_key() for product in products]
        return [ProductSchema(**product) for product in products]

    async def create_product(self, product: ProductSchema) -> bool:
        logger.debug(f'creating product: {product.dict()}')
        try:
            await self.mongo_collection.insert_one({
                '_id': product.id,
                'name': product.name,
                'description': product.description,
                'parameters': product.parameters.dict()
            })
        except DuplicateKeyError:
            return False
        return True

    async def delete_product(self, product_id) -> bool:
        result = await self.mongo_collection.delete_one({'_id': product_id})
        if result.deleted_count != 0:
            return True

    async def count_products(self, filters) -> int:
        logger.debug('counting products')
        return await self.mongo_collection.count_documents(filters)
