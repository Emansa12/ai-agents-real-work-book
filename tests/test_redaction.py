"""Tests for secret redaction helpers."""

from src.redaction import REDACTED, redact_secrets


def test_redact_openai_style_key() -> None:
    text = "Authentication failed for sk-abc123"
    result = redact_secrets(text)

    assert "sk-abc123" not in result
    assert REDACTED in result


def test_redact_explicit_secrets() -> None:
    secret = "my-secret-api-value"
    text = f"Request failed with key {secret}"

    result = redact_secrets(text, secrets=[secret])

    assert secret not in result
    assert REDACTED in result


def test_redact_without_secrets_list() -> None:
    text = "token sk-proj-abc123xyz"

    result = redact_secrets(text)

    assert "sk-proj-abc123xyz" not in result
    assert REDACTED in result
