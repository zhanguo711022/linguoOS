from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    provider: str = "mock"
    db_path: str = "linguoos/data/history.db"
    require_api_key: bool = False
    api_key: str = "dev-key-123"
    version: str = "1.0.0"
    debug: bool = False
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    azure_speech_key: str = Field(default="", alias="AZURE_SPEECH_KEY")
    azure_speech_region: str = "eastasia"

    model_config = SettingsConfigDict(
        env_prefix="LINGUO_",
        env_file=".env",
        extra="ignore",
        populate_by_name=True,
    )


settings = Settings()
