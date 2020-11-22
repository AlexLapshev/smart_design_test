import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config.main import main_config
from api.databases.mongo.mongo_connection import create_mongo_client
from api.services.products.router import products


def create_app():
    app = FastAPI(debug=True)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=main_config.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(products, prefix='/api/v1/products', tags=['products'])
    app.router.add_event_handler("startup", create_startup_hook(app))
    return app


def create_startup_hook(app: FastAPI):
    async def startup_hook() -> None:
        app.state.mongo_client = await create_mongo_client()
    return startup_hook


app = create_app()


if __name__ == "__main__":
    uvicorn.run('api.main:app', host=main_config.host, port=main_config.port,
                reload=main_config.reload, workers=main_config.workers)
