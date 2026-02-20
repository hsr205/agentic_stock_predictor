from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: str = Field(..., description="API key for Alpaca Markets Connection")
    api_secret_key: str = Field(..., description="API secret key for Alpaca Markets Connection")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
