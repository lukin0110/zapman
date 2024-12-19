import logging
import pickle  # noqa: S403
from functools import lru_cache
from http.cookiejar import Cookie
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

from orval import kebab_case

from zapman._exceptions import ZapTypeError
from zapman._module import load_module

logger = logging.getLogger(__name__)


def __dir_path(dir_path: str) -> Path:
    path = Path.cwd() / ".zap_cache" / dir_path
    path.mkdir(parents=True, exist_ok=True)
    return path


def dump_cookies(url: str, cookies: list[Cookie]) -> Path:
    parsed_url = urlparse(url)
    path = __dir_path("cookies") / f"{kebab_case(parsed_url.netloc)}.pkl"
    with path.open("wb") as f:
        pickle.dump(cookies, f)
    logger.debug("Cookies dumped for %s", parsed_url.netloc)
    return path


def load_cookies(url: str) -> list[Cookie]:
    parsed_url = urlparse(url)
    try:
        path = __dir_path("cookies") / f"{kebab_case(parsed_url.netloc)}.pkl"
        if path.exists():
            with path.open("rb") as f:
                return cast("list[Cookie]", pickle.load(f))  # noqa: S301
    except (EOFError, FileNotFoundError):
        # TODO: lower to debug once lib is stable
        logger.exception("Failed to load cookies for '%s'", parsed_url.netloc)
    return []


def dump_store(environment: str, store: dict[str, Any]) -> Path:
    path = __dir_path("stores") / f"{kebab_case(environment)}.pkl"
    with path.open("wb") as f:
        pickle.dump(store, f)
    logger.debug("Store dumped to %s", path)
    return path


def load_store(environment: str) -> dict[str, Any]:
    try:
        path = __dir_path("stores") / f"{kebab_case(environment)}.pkl"
        if path.exists():
            with path.open("rb") as f:
                return cast("dict[str, Any]", pickle.load(f))  # noqa: S301
    except (EOFError, FileNotFoundError):
        # TODO: lower to debug once lib is stable
        logger.exception("Failed to load store for '%s'", environment)
    return {}


def __validate_env_dict(environment: str, data: Any) -> None:
    if not isinstance(data, dict):
        raise ZapTypeError([f"Environment definition '{environment}' must be a flat dictionary."])
    allowed_types = (int, float, str, bool)
    allowed = all(isinstance(value, allowed_types) for value in data.values())
    if not allowed:
        msg = f"Environment definition '{environment}' must only contain basic types (int, float, str, bool)."
        raise ZapTypeError([msg])


@lru_cache
def load_environments() -> dict[str, dict[str, str]]:
    zap_envs = Path.cwd() / "zapenvs.py"
    if not zap_envs.exists():
        logger.debug("No 'zapenvs.py' file found in current '%s' directory.", Path.cwd())
        return {"default": {}}
    module = load_module(str(zap_envs))
    keys = module.__dict__.keys()
    filtered = [k for k in keys if k.startswith("env_")]
    results = {}
    for key in filtered:
        func = getattr(module, key)
        data = func()
        __validate_env_dict(key, data)
        results[key.split("env_")[1]] = data
    if "default" not in results:
        results["default"] = {}
    return results
