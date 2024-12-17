"""Zap environments."""


def env_default() -> dict[str, str]:
    """Provide default environment."""
    return {
        "endpoint": "https://httpbin.org",
    }
