"""Tests for configuration loading and validation."""

import pytest

from src.config import DEFAULT_MODEL_NAME, ConfigError, load_settings


@pytest.fixture(autouse=True)
def _isolate_from_dotenv(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent local `.env` from overriding test environment variables."""
    monkeypatch.setattr("src.config.load_dotenv", lambda *args, **kwargs: False)


def test_config_fails_when_openai_key_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("SERPER_API_KEY", "test-serper-key")
    monkeypatch.delenv("MODEL_NAME", raising=False)

    with pytest.raises(ConfigError, match="OPENAI_API_KEY"):
        load_settings()


def test_config_fails_when_serper_key_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key")
    monkeypatch.delenv("SERPER_API_KEY", raising=False)
    monkeypatch.delenv("MODEL_NAME", raising=False)

    with pytest.raises(ConfigError, match="SERPER_API_KEY"):
        load_settings()


def test_config_fails_on_placeholder_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "your_openai_api_key_here")
    monkeypatch.setenv("SERPER_API_KEY", "your_serper_api_key_here")
    monkeypatch.delenv("MODEL_NAME", raising=False)

    with pytest.raises(ConfigError, match="OPENAI_API_KEY"):
        load_settings()


def test_config_succeeds_with_fake_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key-123")
    monkeypatch.setenv("SERPER_API_KEY", "serper-test-fake-key-456")
    monkeypatch.delenv("MODEL_NAME", raising=False)

    settings = load_settings()

    assert settings.openai_api_key == "sk-test-fake-key-123"
    assert settings.serper_api_key == "serper-test-fake-key-456"
    assert settings.model_name == DEFAULT_MODEL_NAME


def test_config_uses_model_name_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key")
    monkeypatch.setenv("SERPER_API_KEY", "serper-test-fake-key")
    monkeypatch.setenv("MODEL_NAME", "gpt-4o")

    settings = load_settings()

    assert settings.model_name == "gpt-4o"
