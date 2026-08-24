"""Enterprise Configuration Management (12-Factor App pattern)."""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""

    app_name: str = "DaRT Automation Service"
    app_version: str = "1.0.0"
    apm_id: str = "AD00001234"
    track: str = "HDX"
    environment: str = os.getenv("ENVIRONMENT", "dev")
    port: int = int(os.getenv("PORT", "8080"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    api_prefix: str = "/api/v1"
    enable_detailed_errors: bool = os.getenv("ENVIRONMENT", "dev") != "prod"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()