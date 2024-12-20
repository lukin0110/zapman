"""Zap environments."""


def env_default() -> dict[str, str]:
    """Provide default environment."""
    return {
        "endpoint": "https://httpbin.org",
    }


def env_pie() -> dict[str, str]:
    return {
        "endpoint": "https://pie.dev",
    }
