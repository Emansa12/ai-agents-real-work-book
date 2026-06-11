"""Load and validate application settings from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

DEFAULT_MODEL_NAME = "gpt-4o-mini"

PLACEHOLDER_VALUES = {
    "OPENAI_API_KEY": "your_openai_api_key_here",
    "SERPER_API_KEY": "your_serper_api_key_here",
}


class ConfigError(Exception):
    """Raised when required configuration is missing or invalid."""


class Settings(BaseModel):
    openai_api_key: str
    serper_api_key: str
    model_name: str = DEFAULT_MODEL_NAME


def _is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return not value.strip()


def _validate_required_key(name: str, value: str | None) -> None:
    if _is_missing(value):
        raise ConfigError(
            f"Missing required environment variable: {name}. "
            f"Copy .env.example to .env and set a valid {name}."
        )
    placeholder = PLACEHOLDER_VALUES.get(name)
    if placeholder and value.strip() == placeholder:
        raise ConfigError(
            f"Invalid {name}: placeholder value detected. "
            f"Set a real API key in your .env file."
        )


def load_settings(dotenv_path: Path | None = None) -> Settings:
    """Load settings from `.env` and environment. Fail fast if API keys are missing."""
    if dotenv_path is not None:
        load_dotenv(dotenv_path)
    else:
        load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    model_name = os.getenv("MODEL_NAME")

    _validate_required_key("OPENAI_API_KEY", openai_key)
    _validate_required_key("SERPER_API_KEY", serper_key)

    if _is_missing(model_name):
        model_name = DEFAULT_MODEL_NAME

    return Settings(
        openai_api_key=openai_key.strip(),
        serper_api_key=serper_key.strip(),
        model_name=model_name.strip(),
    )
