from loguru import logger

from api.services.products.schemas import FiltersSchema


class FilterCreator:

    def __init__(self, filters: FiltersSchema):
        self.filters = filters

    def filter_dict(self):
        created_filters = {}
        if self.filters.name:
            created_filters.update({'name': {'$regex': self.filters.name, '$options': 'i'}})
            self.filters.name = None
        string_filters = {'parameters.' + filter: {'$regex': f'^{value}', '$options': 'i'}
                          for filter, value in self.filters.dict().items() if type(value) == str}
        float_filters = {'parameters.' + filter: value for filter, value in
                         self.filters.dict().items() if type(value) == float}
        integer_filters = {'parameters.' + filter: value for filter, value in
                           self.filters.dict().items() if type(value) == int}
        created_filters.update(float_filters)
        created_filters.update(string_filters)
        created_filters.update(integer_filters)
        logger.debug(f'filter dict created: {created_filters}')
        return created_filters
