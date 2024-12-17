from types import ModuleType
from typing import Any

import pytest

from zapman._parse import extract  # noqa: PLC2701


class MockModuleType(ModuleType):
    GET: str
    POST: str
    BODY_JSON: dict[str, Any]


@pytest.fixture
def module_get() -> MockModuleType:
    module = MockModuleType("mock_module")
    module.GET = "https://lukin.be"
    return module


@pytest.fixture
def module_post() -> MockModuleType:
    module = MockModuleType("mock_module")
    module.POST = "https://lukin.be"
    module.BODY_JSON = {"foo": "bar"}
    return module


def test_extract_get(module_get: ModuleType) -> None:
    zapfile = extract(module_get)
    assert zapfile.method_and_url == ("GET", "https://lukin.be")
    assert zapfile.body_and_type == ({}, "", "")


def test_extract_post(module_post: ModuleType) -> None:
    zapfile = extract(module_post)
    assert zapfile.method_and_url == ("POST", "https://lukin.be")
    assert zapfile.body_and_type == ({"foo": "bar"}, "", "json")
