import copy
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse, Response

from api.databases.mongo.mongo_connection import get_mongo_client
from api.services.products.products_crud import ProductCRUD
from api.services.products.schemas import ProductSchema, FiltersSchema, ProductsWithNextSchema
from api.services.products.utils import FilterCreator, QueryUrlCreator

products = APIRouter()


@products.get('/{product_id}', response_model=ProductSchema)
async def one_product(product_id: int, mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)):
    if product := await ProductCRUD(mongo_client).get_product_by_id(product_id):
        return product
    else:
        raise HTTPException(status_code=404, detail='product not found')


@products.get('', response_model=ProductsWithNextSchema)
async def filtered_products(name: Optional[str] = None,
                            ram_size: Optional[int] = None,
                            screen_size: Optional[float] = None,
                            operating_system: Optional[str] = None,
                            brand: Optional[str] = None,
                            color: Optional[str] = None,
                            skip: Optional[int] = 0,
                            length: Optional[int] = 10,
                            mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)):
    if length > 50:
        raise HTTPException(status_code=400, detail='max length is 50')
    filters = FiltersSchema(name=name, ram_size=ram_size, screen_size=screen_size,
                            brand=brand, color=color, operating_system=operating_system)
    copy_filters = copy.deepcopy(filters)
    created_filters = FilterCreator(filters).filter_dict()
    if filtered_pr := await ProductCRUD(mongo_client).get_filtered_products(filters=created_filters, skip=skip,
                                                                            length=length):
        total_products = await ProductCRUD(mongo_client).count_products(created_filters)
        next_url = QueryUrlCreator.create_next_url(filters=copy_filters,
                                                   skip=skip,
                                                   length=length,
                                                   total_products=total_products)
        return ProductsWithNextSchema(products=filtered_pr, next=next_url)
    else:
        raise HTTPException(status_code=404, detail='product not found')


@products.post('')
async def create_product(product: ProductSchema, mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)):
    if await ProductCRUD(mongo_client).create_product(product):
        return JSONResponse(status_code=201, content={'result': 'product created'})
    raise HTTPException(status_code=409, detail='product with this id already exists')


@products.delete('')
async def delete_product(product_id: int, mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)):
    if await ProductCRUD(mongo_client).delete_product(product_id):
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail='product not found')
