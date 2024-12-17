import json
from dataclasses import dataclass
from types import ModuleType
from typing import Any, TypeVar

from zapman._exceptions import ZapTypeError, ZapValueError
from zapman._version import __version__

T = TypeVar("T")


@dataclass
class ZapFile:
    # HTTP methods
    get: str | None = None
    post: str | None = None
    put: str | None = None
    patch: str | None = None
    delete: str | None = None
    head: str | None = None
    connect: str | None = None
    options: str | None = None
    trace: str | None = None

    # Headers
    headers: dict[str, str] | None = None

    # Parameters
    params: dict[str, str] | None = None

    # Body
    body_form: dict[str, str] | None = None
    body_json: dict[str, str] | None = None
    body_raw: str | None = None

    # Cookies
    cookies: dict[str, str] | None = None

    # Download the resource
    download: bool = False

    # SSL
    verify: bool = True

    @property
    def method_and_url(self) -> tuple[str, str]:
        methods = {
            "GET": self.get,
            "POST": self.post,
            "PUT": self.put,
            "PATCH": self.patch,
            "DELETE": self.delete,
            "HEAD": self.head,
            "CONNECT": self.connect,
            "OPTIONS": self.options,
            "TRACE": self.trace,
        }
        found = [method for method, value in methods.items() if value is not None]
        if len(found) > 1:
            raise ZapValueError(f"Multiple HTTP methods '{found}' found in zapfile")
        for method, url in methods.items():
            if url:
                return method, url
        raise ZapValueError("No HTTP method found in zapfile")

    @property
    def body_and_type(self) -> tuple[dict[str, str], str, str]:
        body = [self.body_json, self.body_form, self.body_raw]
        found = [b for b in body if b is not None]
        if len(found) > 1:
            raise ZapValueError("Multiple bodies ['BODY_JSON', 'BODY_FORM', 'BODY_RAW'] found in zapfile")
        if self.body_form is not None:
            return self.body_form, "", "form"
        if self.body_json is not None:
            return self.body_json, "", "json"
        if self.body_raw is not None:
            return {}, self.body_raw, "raw"
        return {}, "", ""


def __extract_and_type_check(
    module: ModuleType,
    name: str,
    type_: type,
) -> tuple[Any, str | None]:
    value = getattr(module, name, None)
    if value is not None and not isinstance(value, type_):
        return value, f"{name} has an invalid type '{type(value).__name__}'. It must be of type '{type_.__name__}'."
    return value, None


def extract(module: ModuleType) -> ZapFile:
    mapping = {
        "get": ("GET", str),
        "post": ("POST", str),
        "put": ("PUT", str),
        "patch": ("PATCH", str),
        "delete": ("DELETE", str),
        "head": ("HEAD", str),
        "connect": ("CONNECT", str),
        "options": ("OPTIONS", str),
        "trace": ("TRACE", str),
        "headers": ("HEADERS", dict),
        "params": ("PARAMS", dict),
        "body_form": ("BODY_FORM", dict),
        "body_json": ("BODY_JSON", dict),
        "body_raw": ("BODY_RAW", str),
        "cookies": ("COOKIES", dict),
        "download": ("DOWNLOAD", bool),
        "verify": ("VERIFY", bool),
    }
    errors = []
    values = {}
    for key, (name, type_) in mapping.items():
        value, error = __extract_and_type_check(module, name, type_)
        if error is not None:
            errors.append(error)
        if type_ is bool and value is None:
            continue
        values[key] = value
    if errors:
        raise ZapTypeError(errors)
    return ZapFile(**values)


def construct_call_args(zap_file: ZapFile, existing_cookies: dict[str, str]) -> list[str]:  # noqa: PLR0914
    # Extract and validate
    method, url = zap_file.method_and_url

    # Construct headers, params & cookies
    headers = zap_file.headers or {}
    headers_str = [f"{key}: {value}" for key, value in headers.items()]
    params_str = [f"{key}=={value}" for key, value in (zap_file.params or {}).items()]
    zap_cookies = zap_file.cookies or {}
    cookies_merged = {**existing_cookies, **zap_cookies}
    if len(cookies_merged) > 0:
        cookie_str = f"Cookie:{';'.join([f'{k}={v}' for k, v in cookies_merged.items() if v is not None])}"
    else:
        cookie_str = ""
    base_args = ["zapman", "--print=HBhbm"]
    # base_args = ["zapman", "--verbose"]
    if not zap_file.verify:
        base_args.extend(["--verify", "no"])
    if zap_file.download:
        base_args.append("--download")
    header_keys = set(map(str.lower, headers.keys()))
    header_part = [f"User-Agent: Zapman/{__version__}"] if "user-agent" not in header_keys else []
    second_part = [*header_part, *headers_str, *params_str]
    last_part = [cookie_str] if cookie_str else []

    # Parsing the body for any HTTP method, it's up to the server to decide what to do
    body, body_str, body_type_ = zap_file.body_and_type
    if body_type_ == "json":
        body_json_str = json.dumps(zap_file.body_json) if body else body_str
        return [*base_args, "--json", "--raw", body_json_str, method, url, *second_part, *last_part]
    if body_type_ == "raw":
        # TODO: handle other content types, based on the Content-Type header
        # For now it's implicitly assuming JSON: Content-Type: application/json
        return [*base_args, "--json", "--raw", body_str, method, url, *second_part, *last_part]
    if body_type_ == "form":
        body_form_str = [f"{key}={value}" for key, value in (body or {}).items()]
        return [*base_args, "--form", method, url, *second_part, *body_form_str, *last_part]

    return [*base_args, method, url, *second_part, *last_part]
