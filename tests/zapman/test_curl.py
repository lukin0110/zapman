import pytest

from zapman._curl import format_curl  # noqa: PLC2701
from zapman._parse import ZapFile  # noqa: PLC2701


# def format_curl(zap_file: ZapFile, existing_cookies: dict[str, str]) -> str:
@pytest.mark.parametrize(
    ("zapfile", "expected"),
    [
        (
            ZapFile(get="https://lukin.be"),
            "curl -i -X GET 'https://lukin.be'",
        ),
        (
            ZapFile(get="https://lukin.be", download=True),
            "curl -X GET 'https://lukin.be' \\\n-o https-lukin-be.json",
        ),
        (
            ZapFile(get="https://lukin.be", headers={"X-Foo": "bar"}),
            "curl -i -X GET 'https://lukin.be' \\\n--header 'X-Foo: bar'",
        ),
        (
            ZapFile(get="https://lukin.be", headers={"user-agent": "Eddie Vedder"}),
            "curl -i -X GET 'https://lukin.be' \\\n--header 'user-agent: Eddie Vedder'",
        ),
        (
            ZapFile(get="https://lukin.be", params={"foo": "bar"}),
            "curl -i -X GET 'https://lukin.be?foo=bar'",
        ),
        (
            ZapFile(get="https://lukin.be", body_json={"foo": "bar"}),
            "curl -i -X GET 'https://lukin.be' \\\n--header 'Content-Type: application/json' \\\n--data '{\"foo\": \"bar\"}'",
        ),
        (
            ZapFile(get="https://lukin.be", body_form={"foo": "bar"}),
            "curl -i -X GET 'https://lukin.be' \\\n--data 'foo=bar'",
        ),
        (
            ZapFile(get="https://lukin.be", cookies={"foo": "bar"}),
            "curl -i -X GET 'https://lukin.be' \\\n--cookie 'foo=bar'",
        ),
        (
            ZapFile(get="https://lukin.be", verify=False),
            "curl -i -X GET 'https://lukin.be' \\\n--insecure",
        ),
    ],
)
def test_format(zapfile: ZapFile, expected: str) -> None:
    assert format_curl(zapfile, {}) == expected
