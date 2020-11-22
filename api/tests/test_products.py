import pytest

from loguru import logger

test_url = "products"

product_json = {
    'id': 4,
    'name': 'Test name',
    'description': 'test desc',
    'parameters': {
        'brand': 'test brand',
        'ram_size': 4,
        'screen_size': 6,
        'color': 'black',
        'operating_system': 'Android'
    }
}

product_json_2 = {
    'id': 1,
    'name': 'Test name',
    'description': 'test desc',
    'parameters': {
        'brand': 'test brand',
        'ram_size': 4,
        'screen_size': 6,
        'color': 'black',
        'operating_system': 'Android'
    }
}


@pytest.mark.parametrize('product_id, status', [(1, 200), (2, 200), (4, 404)])
@pytest.mark.usefixtures('insert_products_in_mongo')
def test_get_product_by_id(client, product_id, status):
    response = client.get(test_url + '/' + str(product_id))
    logger.debug(response.content)
    assert response.status_code == status


@pytest.mark.usefixtures('insert_products_in_mongo')
@pytest.mark.parametrize('product, status', [(product_json, 201), (product_json_2, 409), ({}, 422)])
def test_create_product(client, product, status):
    response = client.post(test_url, json=product)
    assert response.status_code == status


@pytest.mark.usefixtures('insert_products_in_mongo')
@pytest.mark.parametrize('product_id, status', [(1, 204), (4, 404)])
def test_delete_product(client, product_id, status):
    response = client.delete(test_url + '?product_id=' + str(product_id))
    logger.debug(response.content)
    assert response.status_code == status


queries = [
    ('?name=sam', 200, 1),
    ('?name=Samsung', 200, 1),
    ('?name=samsung', 200, 1),
    ('?name=a', 200, 3),
    ('?color=black', 200, 1),
    ('?color=green', 404, 0),
    ('?brand=xiaomi', 200, 1),
    ('?brand=siemens', 404, 0),
    ('?ram_size=4', 200, 2),
    ('?ram_size=16', 404, 0),
    ('?screen_size=5', 200, 1),
    ('?screen_size=7.7', 200, 1),
    ('?screen_size=16', 404, 0),
    ('?operating_system=android', 200, 2),
    ('?operating_system=ios', 404, 0),
    ('?ram_size=4&color=blue', 200, 1),
    ('?ram_size=4&color=green', 404, 1),
    ('?ram_size=4&screen_size=6', 200, 1),
    ('?color=black&name=x', 200, 1),
    ('?color=black&name=x&skip=100', 404, 1),
]


@pytest.mark.usefixtures('insert_products_in_mongo')
@pytest.mark.parametrize('query, status, count', queries)
def test_get_filtered(client, query, status, count):
    response = client.get(test_url + query)
    logger.debug(response.json())
    assert response.status_code == status
    if status != 404:
        assert len(response.json()['products']) == count


next_queries = [
    ('?name=a&length=1', 200, True),
    ('?name=Nokia', 200, False),
    ('?name=Nokia&length=51', 400, False),
]


@pytest.mark.usefixtures('insert_products_in_mongo')
@pytest.mark.parametrize('query, status, next_url', next_queries)
def test_next_filtered(client, query, status, next_url):
    response = client.get(test_url + query)
    logger.debug(response.json())
    assert response.status_code == status
    if status != 400:
        assert bool(response.json()['next']) == next_url
