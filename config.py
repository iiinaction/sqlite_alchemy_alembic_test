import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DATABASE_SQLITE: ClassVar[str] = 'sqlite+aiosqlite:///data/db.sqlite3'
    model_config = SettingsConfigDict(
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self): 
        return "sqlite+aiosqlite:///data/db.sqlite3"

settings = Settings()