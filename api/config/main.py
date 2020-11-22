import yaml
import os

from loguru import logger


from api.config.schemas import Settings

settings_file = 'debug-settings.yaml'

if os.environ.get('PRODUCTION'):
    settings_file = 'production-settings.yaml'

with open(f'api/config/{settings_file}') as f:
    logger.debug(f'reading settings file {settings_file}')
    settings = yaml.safe_load(f)


def get_api_settings() -> Settings:
    logger.debug('making settings')
    config = {}
    for k, v in settings.items():
        config.update(v)
    origins = config['origins'].split(',')
    config['origins'] = [origin.strip() for origin in origins]
    config = Settings(**config)
    return config


main_config = get_api_settings()
