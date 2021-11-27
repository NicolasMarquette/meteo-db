"""Security settings."""

import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Create the config settings."""
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8


settings = Settings()
