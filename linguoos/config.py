from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    provider: str = "mock"
    db_path: str = "linguoos/data/history.db"
    require_api_key: bool = False
    api_key: str = "dev-key-123"
    version: str = "1.0.0"
    debug: bool = False

    model_config = SettingsConfigDict(env_prefix="LINGUO_", env_file=".env")


settings = Settings()
