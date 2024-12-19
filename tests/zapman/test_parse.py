import pytest

from zapman import __version__
from zapman._parse import ZapFile, construct_call_args  # noqa: PLC2701


@pytest.mark.parametrize(
    ("zapfile", "expected"),
    [
        (
            ZapFile(get="https://lukin.be"),
            ["zapman", "--print=HBhbm", "GET", "https://lukin.be", f"User-Agent: Zapman/{__version__}"],
        ),
        (
            ZapFile(get="https://lukin.be", download=True),
            ["zapman", "--print=HBhbm", "--download", "GET", "https://lukin.be", f"User-Agent: Zapman/{__version__}"],
        ),
        (
            ZapFile(get="https://lukin.be", headers={"X-Foo": "bar"}),
            ["zapman", "--print=HBhbm", "GET", "https://lukin.be", f"User-Agent: Zapman/{__version__}", "X-Foo: bar"],
        ),
        (
            ZapFile(get="https://lukin.be", headers={"user-agent": "Eddie Vedder"}),
            ["zapman", "--print=HBhbm", "GET", "https://lukin.be", "user-agent: Eddie Vedder"],
        ),
        (
            ZapFile(get="https://lukin.be", params={"foo": "bar"}),
            ["zapman", "--print=HBhbm", "GET", "https://lukin.be", f"User-Agent: Zapman/{__version__}", "foo==bar"],
        ),
        (
            ZapFile(get="https://lukin.be", body_json={"foo": "bar"}),
            [
                "zapman",
                "--print=HBhbm",
                "--json",
                "--raw",
                '{"foo": "bar"}',
                "GET",
                "https://lukin.be",
                f"User-Agent: Zapman/{__version__}",
            ],
        ),
        (
            ZapFile(get="https://lukin.be", body_form={"foo": "bar"}),
            [
                "zapman",
                "--print=HBhbm",
                "--form",
                "GET",
                "https://lukin.be",
                f"User-Agent: Zapman/{__version__}",
                "foo=bar",
            ],
        ),
        (
            ZapFile(get="https://lukin.be", cookies={"foo": "bar"}),
            [
                "zapman",
                "--print=HBhbm",
                "GET",
                "https://lukin.be",
                f"User-Agent: Zapman/{__version__}",
                "Cookie:foo=bar",
            ],
        ),
        (
            ZapFile(get="https://lukin.be", verify=False),
            [
                "zapman",
                "--print=HBhbm",
                "--verify",
                "no",
                "GET",
                "https://lukin.be",
                f"User-Agent: Zapman/{__version__}",
            ],
        ),
    ],
)
def test_get(zapfile: ZapFile, expected: list[str]) -> None:
    assert construct_call_args(zapfile, {}) == expected


@pytest.mark.parametrize(
    ("zapfile", "expected"),
    [
        (ZapFile(get="https://lukin.be"), "Cookie:foo=bar"),
        (ZapFile(get="https://lukin.be", cookies={"foo": "McFly"}), "Cookie:foo=McFly"),
        (ZapFile(get="https://lukin.be", cookies={"bar": "Tannen"}), "Cookie:foo=bar;bar=Tannen"),
    ],
)
def test_get_with_existing_cookies(zapfile: ZapFile, expected: str) -> None:
    cookies = {"foo": "bar"}
    base_args = [
        "zapman",
        "--print=HBhbm",
        "GET",
        "https://lukin.be",
        f"User-Agent: Zapman/{__version__}",
    ]
    assert construct_call_args(zapfile, cookies) == [*base_args, expected]


@pytest.mark.parametrize(
    ("zapfile", "expected"),
    [
        (
            ZapFile(post="https://lukin.be"),
            ["zapman", "--print=HBhbm", "POST", "https://lukin.be", f"User-Agent: Zapman/{__version__}"],
        ),
        (
            ZapFile(post="https://lukin.be", body_form={"foo": "bar"}),
            [
                "zapman",
                "--print=HBhbm",
                "--form",
                "POST",
                "https://lukin.be",
                f"User-Agent: Zapman/{__version__}",
                "foo=bar",
            ],
        ),
        (
            ZapFile(post="https://lukin.be", body_json={"foo": "bar"}),
            [
                "zapman",
                "--print=HBhbm",
                "--json",
                "--raw",
                '{"foo": "bar"}',
                "POST",
                "https://lukin.be",
                f"User-Agent: Zapman/{__version__}",
            ],
        ),
        (
            ZapFile(post="https://lukin.be", body_raw='{"foo":"bar"}'),
            [
                "zapman",
                "--print=HBhbm",
                "--json",
                "--raw",
                '{"foo":"bar"}',
                "POST",
                "https://lukin.be",
                f"User-Agent: Zapman/{__version__}",
            ],
        ),
        (
            ZapFile(post="https://lukin.be", body_raw=' {"foo": "bar"} '),
            [
                "zapman",
                "--print=HBhbm",
                "--json",
                "--raw",
                ' {"foo": "bar"} ',
                "POST",
                "https://lukin.be",
                f"User-Agent: Zapman/{__version__}",
            ],
        ),
        (
            ZapFile(post="https://lukin.be", body_raw=" Whatever "),
            [
                "zapman",
                "--print=HBhbm",
                "--json",
                "--raw",
                " Whatever ",
                "POST",
                "https://lukin.be",
                f"User-Agent: Zapman/{__version__}",
            ],
        ),
    ],
)
def test_post(zapfile: ZapFile, expected: list[str]) -> None:
    assert construct_call_args(zapfile, {}) == expected
