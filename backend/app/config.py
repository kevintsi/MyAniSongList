import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
