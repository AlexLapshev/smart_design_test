from pydantic import BaseSettings
from typing import List


class SettingsDB(BaseSettings):
    mongo_url: str


class SettingsApp(BaseSettings):
    base_url: str
    origins: List[str]
    reload: bool = False
    host: str
    port: int
    workers: int


class Settings(SettingsDB, SettingsApp):
    pass



