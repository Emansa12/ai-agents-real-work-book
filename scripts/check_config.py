"""Validate configuration and print safe status (no secret values)."""

import sys

from src.config import ConfigError, load_settings


def main() -> None:
    try:
        settings = load_settings()
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print("Config loaded successfully")
    print(f"Model name: {settings.model_name}")
    print("OPENAI_API_KEY: present")
    print("SERPER_API_KEY: present")


if __name__ == "__main__":
    main()
