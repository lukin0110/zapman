"""Response context."""

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any, cast

from requests import Response
from rich import print as rprint

from zapman._exceptions import ZapError


class _Base:
    """Wrapper around a requests.Response object."""

    def __init__(self, response: Response, content: bytes | None, output_file: Path | None) -> None:
        self.__response = response
        self.__content = content
        self.__output_file = output_file

    @property
    def status_code(self) -> int:
        return self.__response.status_code

    @property
    def content_type(self) -> str | None:
        return self.headers.get("Content-Type", None)

    @property
    def headers(self) -> dict[str, str]:
        return cast("dict[str, str]", self.__response.headers)

    @property
    def json(self) -> Any:
        msg = f"JSON response not available (content-type={self.content_type})"
        if self.__content is None:
            raise ZapError(msg)
        try:
            return json.loads(self.__content)
        except JSONDecodeError as e:
            raise ZapError(msg) from e

    @property
    def output_file(self) -> Path | None:
        return self.__output_file

    @property
    def text(self) -> str:
        return self.__response.text

    @property
    def cookies(self) -> dict[str, str]:
        return self.__response.cookies.get_dict()


class Test(_Base):
    pass


class After(_Base):
    def __init__(self, environment: str, response: Response, content: bytes | None, output_file: Path | None) -> None:
        super().__init__(response, content, output_file)
        self.__environment = environment

    def print(self, string: str) -> None:
        print(f"[env={self.__environment}] {string}")

    def happy(self, string: str) -> None:
        rprint(rf"[green]\[env={self.__environment}][/green] [not bold grey78]{string}[/not bold grey78]")

    def info(self, string: str) -> None:
        # https://rich.readthedocs.io/en/stable/appendix/colors.html
        # rprint(rf"[bold blue]\[env={self.__environment}][/bold blue] [blue]{string}[/blue]")
        rprint(rf"[blue]\[env={self.__environment}][/blue] [grey78]{string}[/grey78]")

    def error(self, string: str) -> None:
        rprint(rf"[red]\[env={self.__environment}] {string}[/red]")
