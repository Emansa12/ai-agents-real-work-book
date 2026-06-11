"""Redact secret values from log messages and strings."""

import re

REDACTED = "***REDACTED***"

_SK_PATTERN = re.compile(r"sk-[a-zA-Z0-9_-]+")


def redact_secrets(text: str, secrets: list[str] | None = None) -> str:
    """Replace known secrets and common API-key patterns with a redacted marker."""
    result = text
    if secrets:
        for secret in secrets:
            if secret:
                result = result.replace(secret, REDACTED)
    return _SK_PATTERN.sub(REDACTED, result)
