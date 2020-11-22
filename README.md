# Smart_design_test

## Production run

`docker-compose up` from directory _/smart_design_test_


## Development run

`pip install -r requirements.txt` from directory _/smart_design_test/api_

`docker-compose up` from directory _/smart_design_test/api/databases/mongo/_

`python -m api.main` from directory _/smart_design_test_

## API

GET `http://0.0.0.0:1984/api/v1/products/{product_id}` get product by id

GET `http://0.0.0.0:1984/api/v1/products` get all products or products by query parameters, return {products:[], next: string or null}, where next is next url if paginated 

`name` - string, case insensitive, searches containing value: _'Product, product, prod'_ returns all products with _'product'_ in name

`ram_size`: integer,

`screen_size`: float or integer

`operating_system`: string

`brand`: string

`color`: string

`skip`: integer, default = 0, needs to paginate responses, app returns products from starting with the value of `skip`  

`length`: integer, default = 10, max=50, app returns number of products, that specified in `length` parameter

POST `http://0.0.0.0:1984/api/v1/products` create product:
needs json

```
{
  "id": integer,
  "name": "string",
  "description": "string",
  "parameters": {
    "color": "string",
    "brand": "string",
    "screen_size": float or integer,
    "ram_size": integer,
    "operating_system": "string"
  }
}
```

DELETE `http://0.0.0.0:1984/api/v1/products` delete product: needs query_parameter `product_id`

## curl

###create product

`curl -X POST "http://0.0.0.0:1984/api/v1/products" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"id\":4,\"name\":\"Honor 8X\",\"description\":\"Honor 8X description\",\"parameters\":{\"color\":\"black\",\"brand\":\"Honor\",\"screen_size\":4.7,\"ram_size\":4,\"operating_system\":\"Android\"}}"`

###retrieve product

**by id**

`curl -X GET "http://0.0.0.0:1984/api/v1/products/4" -H  "accept: application/json"`

**all phones with 'honor' in name**

`curl -X GET "http://0.0.0.0:1984/api/v1/products?name=honor" -H  "accept: application/json"`

**all phones with 4.7 display**

`curl -X GET "http://0.0.0.0:1984/api/v1/products?name=honor&screen_size=4.7" -H  "accept: application/json"`

###delete product

`curl -X DELETE "http://0.0.0.0:1984/api/v1/products?product_id=4" -H  "accept: application/json"`

