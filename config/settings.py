"""Configuration management."""

from enum import Enum
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BrowserType(str, Enum):
    """Supported browser types."""
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    base_url: str = Field(default="https://www.saucedemo.com")
    browser: BrowserType = Field(default=BrowserType.CHROMIUM)
    headless: bool = Field(default=True)
    slow_mo: int = Field(default=0)
    viewport_width: int = Field(default=1920)
    viewport_height: int = Field(default=1080)
    default_timeout: int = Field(default=30000)
    navigation_timeout: int = Field(default=60000)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()