from os import path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=path.join(path.dirname(__file__), "..", ".env"),
        env_file_encoding='utf-8'
    )

    client_id: str
    client_secret: str
    session_secret_key: str
    db_url: str


stg = Settings()
# фикс родаков тут + пост на логауте с 303