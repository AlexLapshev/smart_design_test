from typing import Optional, List

from pydantic import BaseModel, PositiveFloat, PositiveInt


class ParametersSchema(BaseModel):
    color: str
    brand: str
    screen_size: PositiveFloat
    ram_size: PositiveInt
    operating_system: str


class ProductSchema(BaseModel):
    id: PositiveInt
    name: str
    description: str
    parameters: ParametersSchema


class FiltersSchema(BaseModel):
    name: Optional[str]
    ram_size: Optional[PositiveInt]
    screen_size: Optional[PositiveFloat]
    operating_system: Optional[str]
    brand: Optional[str]
    color: Optional[str]


class ProductsWithNextSchema(BaseModel):
    products: List[ProductSchema]
    next: Optional[str]
