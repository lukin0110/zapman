from pathlib import Path
from typing import ClassVar


class ZapError(BaseException):
    pass


class ZapTypeError(ZapError, TypeError):
    __attrs__: ClassVar = ["errors"]

    def __init__(self, errors: list[str]) -> None:
        super().__init__("Invalid zapfile")
        self.errors = errors

    def __str__(self) -> str:
        error_str = "\n 🛠️  ".join(self.errors)
        return f"Invalid zapfile:\n\n 🛠️  {error_str}"


class ZapKeyError(ZapError, LookupError):
    def __init__(self, message: str, *, env: str | None = None) -> None:
        super().__init__(message)
        self.__env = env

    def __str__(self) -> str:
        if not self.__env:
            return str(self.args[0])
        errors = [str(self.args[0]), ":\n", "\n 🌍 Selected environment: "]
        env_file = Path.cwd() / "zapenvs.py"
        if not env_file.exists():
            errors.append(f"\n 🛠️  Key not found in environment file ('{env_file}' not found)")
        errors.append("\n 🛠️  Key not found in local storage")
        return "".join(errors)


class ZapValueError(ZapError, ValueError):
    pass


class ZapStoreError(ZapError):
    pass
