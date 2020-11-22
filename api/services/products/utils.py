import copy

from loguru import logger

from api.config.main import main_config
from api.services.products.schemas import FiltersSchema


class FilterCreator:

    def __init__(self, filters: FiltersSchema):
        self.filters = filters

    def filter_dict(self) -> dict:
        copy_filters = copy.deepcopy(self.filters)
        created_filters = {}
        if self.filters.name:
            created_filters.update({'name': {'$regex': copy_filters.name, '$options': 'i'}})
            copy_filters.name = None
        string_filters = {'parameters.' + filter: {'$regex': f'^{value}', '$options': 'i'}
                          for filter, value in copy_filters.dict().items() if type(value) == str}
        float_filters = {'parameters.' + filter: value for filter, value in
                         copy_filters.dict().items() if type(value) == float}
        integer_filters = {'parameters.' + filter: value for filter, value in
                           copy_filters.dict().items() if type(value) == int}
        created_filters.update(float_filters)
        created_filters.update(string_filters)
        created_filters.update(integer_filters)
        logger.debug(f'filter dict created: {created_filters}')
        return created_filters


class QueryUrlCreator:

    @staticmethod
    def create_next_url(filters: FiltersSchema,
                        skip: int,
                        total_products: int,
                        length: int = 10) -> str or None:
        next_url = None
        if skip + length < total_products:
            query_string = '&'.join([f'{query_param}={value}'
                                     for query_param, value in filters.dict().items() if value])
            logger.debug(query_string)
            next_url = main_config.base_url + '/products?' + query_string + f'&skip={skip+length}' + f'&length={length}'
        return next_url


class ProductSerializer:
    def __init__(self, product: dict):
        self.product = product

    def replace_id_key(self):
        self.product['id'] = self.product.pop('_id')
        return self.product
