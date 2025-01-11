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


def env_fastmock() -> dict[str, str]:
    return {
        "endpoint": "https://fastmock.lukin.be",
    }


def env_docker() -> dict[str, str]:
    return {
        # For Docker Desktop (altenatively use the host ip)
        "endpoint": "http://host.docker.internal:8001",
    }
