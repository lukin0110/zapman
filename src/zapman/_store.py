import logging
from collections.abc import Iterator, MutableMapping
from contextvars import ContextVar
from copy import deepcopy
from functools import lru_cache
from typing import Any
from urllib.parse import urlparse

from zapman._exceptions import ZapKeyError, ZapStoreError
from zapman._io import load_cookies, load_environments, load_store

logger = logging.getLogger(__name__)


class EnvironmentStore(MutableMapping[str, Any]):
    def __init__(self, environment: str, *, env_data: dict[str, str], env_store: dict[str, Any]) -> None:
        self.__environment = environment
        self.__env_data = env_data
        self.__env_store = env_store
        self.__writes = 0

    def __str__(self) -> str:
        key_set = set(self.__env_data.keys()) | set(self.__env_store.keys())
        return "".join([
            "[env=",
            self.__environment,
            '] vars=["',
            '", "'.join(key_set),
            '"]',
            "\nUse 'zap --view-vars' to view all values",
        ])

    @property
    def environment(self) -> str:
        return self.__environment

    def __getitem__(
        self,
        key: str,
    ) -> Any:
        if key in self.__env_data:
            return self.__env_data[key]
        if key in self.__env_store:
            return self.__env_store[key]
        raise ZapKeyError(f"Zap key '{key}' does not exist", env=self.__environment)

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        if key in self.__env_data:
            msg = f"Can't store a key that is defined as an environment variable (key={key}, env={self.__environment})"
            raise ZapStoreError(msg)
        self.__env_store[key] = value
        self.__writes += 1

    def __delitem__(self, key: str) -> None:
        if key in self.__env_data:
            msg = f"Can't delete a key that is defined as an environment variable (key={key}, env={self.__environment})"
            raise ZapStoreError(msg)
        del self.__env_store[key]
        self.__writes += 1

    def __iter__(self) -> Iterator[Any]:
        merged = {
            **self.__env_store,
            **self.__env_data,
        }
        return merged.__iter__()

    def __len__(self) -> int:
        key_set = set(self.__env_data.keys()) | set(self.__env_store.keys())
        return len(key_set)

    def is_changed(self) -> bool:
        return self.__writes > 0

    def copy(self) -> dict[str, Any]:
        return deepcopy(self.__env_store)


@lru_cache
def _create_store(environment: str) -> EnvironmentStore:
    envs = load_environments()
    env_data = envs[environment]
    env_store = load_store(environment)
    return EnvironmentStore(environment, env_data=env_data, env_store=env_store)


class ContextStore(MutableMapping[str, Any]):
    """."""

    __ENVIRONMENT = ContextVar[str]("environment", default="default")

    @classmethod
    def get_store(cls, environment: str) -> EnvironmentStore:
        """."""
        cls.__ENVIRONMENT.set(environment)
        return _create_store(environment)

    def __store(self) -> EnvironmentStore:
        # Fetch selected environment from ContextVar
        environment = self.__ENVIRONMENT.get()
        return _create_store(environment)

    def __getitem__(self, key: str) -> Any:
        return self.__store().__getitem__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__store().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        self.__store().__delitem__(key)

    def __iter__(self) -> Iterator[Any]:
        return self.__store().__iter__()

    def __len__(self) -> int:
        return self.__store().__len__()

    def __str__(self) -> str:
        return self.__store().__str__()


class CookieStore(MutableMapping[str, Any]):
    def __init__(self, url: str, data: dict[str, Any]) -> None:
        parsed_url = urlparse(url)
        self.__host = parsed_url.netloc or url
        self.__data = data

    def __getitem__(self, key: str) -> Any:
        if key not in self.__data:
            raise ZapKeyError(f"Cookie '{key}' doesn't exist for host '{self.__host}'", env=None)
        return self.__data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        raise NotImplementedError("Setting cookies is not supported yet")

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError("Deleting cookies is not supported yet")

    def __iter__(self) -> Iterator[Any]:
        return self.__data.__iter__()

    def __len__(self) -> int:
        return self.__data.__len__()

    def __str__(self) -> str:
        return self.__data.__str__()


@lru_cache
def _create_cookies(url: str) -> CookieStore:
    cookies = load_cookies(url)
    return CookieStore(url, {c.name: c.value for c in cookies if c.value is not None})


class CookieStoreWrapper:
    def __getitem__(self, key: str) -> Any:
        return _create_cookies(key)
