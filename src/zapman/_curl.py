import json
from urllib.parse import quote

from orval import kebab_case

from zapman._parse import ZapFile


def format_curl(zap_file: ZapFile, existing_cookies: dict[str, str]) -> str:  # noqa: PLR0914
    method, url = zap_file.method_and_url

    headers = zap_file.headers or {}
    headers_str = [f"--header '{key}: {value}'" for key, value in headers.items()]
    params_str = [
        f"{key}={quote(value) if isinstance(value, str) else value}" for key, value in (zap_file.params or {}).items()
    ]
    if params_str:
        url += "?" + "&".join(params_str)

    zap_cookies = zap_file.cookies or {}
    cookies_merged = {k: v for k, v in {**existing_cookies, **zap_cookies}.items() if v is not None}
    cookie_str = f"--cookie '{'; '.join([f'{k}={v}' for k, v in cookies_merged.items()])}'" if cookies_merged else ""

    body, body_str, body_type = zap_file.body_and_type
    if body_type == "json":
        body_json_str = json.dumps(zap_file.body_json) if body else body_str
        headers_str.append("--header 'Content-Type: application/json'")
        body_part = f"--data '{body_json_str}'"
    elif body_type == "raw":
        body_part = f"--data-raw '{body_str}'"
    elif body_type == "form":
        body_form_str = "&".join([f"{key}={value}" for key, value in (body or {}).items()])
        body_part = f"--data '{body_form_str}'"
    else:
        body_part = ""

    verify_part = "" if zap_file.verify else "--insecure"
    # TODO: properly compute the output file name & extension based on content-type
    download_part = f"-o {kebab_case(url)}.json" if zap_file.download else ""
    print_headers = " -i" if not zap_file.download else ""

    final = [f"curl{print_headers} -X {method} '{url}'"]
    if headers_str:
        final.extend(headers_str)
    if cookie_str:
        final.append(cookie_str)
    if body_part:
        final.append(body_part)
    if verify_part:
        final.append(verify_part)
    if download_part:
        final.append(download_part)

    return " \\\n".join(final).strip()
