from typing import ClassVar


class ZapError(BaseException):
    pass


class ZapTypeError(ZapError, TypeError):
    __attrs__: ClassVar = ["errors"]

    def __init__(self, errors: list[str]) -> None:
        super().__init__("Invalid zapfile")
        self.errors = errors

    def __str__(self) -> str:
        return f"Invalid zapfile\n🛠️  {'\n🛠️  '.join(self.errors)}"


class ZapKeyError(ZapError, LookupError):
    pass


class ZapValueError(ZapError, ValueError):
    pass


class ZapStoreError(ZapError):
    pass
