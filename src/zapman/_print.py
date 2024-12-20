import pickle  # noqa: S403
from datetime import datetime, timezone
from pathlib import Path

from rich import print as rprint


def print_cookies() -> None:
    """Print basic info of stored cookies.

    Basic quick and dirty approach.
    """
    cookie_files = (Path.cwd() / ".zap_cache" / "cookies").glob("*.pkl")
    results = []
    for cookie_file in cookie_files:
        with cookie_file.open("rb") as f:
            try:
                cookies = pickle.load(f)  # noqa: S301
                results.append(cookies)
            except (EOFError, FileNotFoundError):
                rprint(f"Failed to load cookies from '{cookie_file}'")

    for cookies in results:
        domain = cookies[0].domain if len(cookies) > 0 else None
        if domain:
            rprint(f"[bold green]Domain: {domain}[/bold green]")
        for cookie in cookies:
            expired_str = r"[bold red]\[EXPIRED][/bold red]" if cookie.is_expired() else ""
            rprint(f"[orange1]{cookie.name}[/orange1] {expired_str}")
            iso_date = datetime.fromtimestamp(cookie.expires, tz=timezone.utc).isoformat() if cookie.expires else "None"
            values = [
                ("value", cookie.value),
                ("domain", cookie.domain),
                ("path", cookie.path),
                ("expires", f"{cookie.expires} ({iso_date})"),
            ]
            for value in values:
                rprint(f"  [cyan]{value[0]}[/cyan]=[not bold grey78]{value[1]}[not bold grey78]")
            print()
        print()


def print_stores() -> None:
    """Print basic info of stored variables.

    Basic quick and dirty approach.
    """
    store_files = (Path.cwd() / ".zap_cache" / "stores").glob("*.pkl")
    results = []
    for store_file in store_files:
        with store_file.open("rb") as f:
            try:
                store_name = store_file.name.replace(".pkl", "")
                store = pickle.load(f)  # noqa: S301
                results.append((store_name, store))
            except (EOFError, FileNotFoundError):
                rprint(f"Failed to load store from '{store_file}'")

    for store in results:
        rprint(f"[bold green]Store: {store[0]}[/bold green]")
        for key, value in store[1].items():
            rprint(f"  [cyan]{key}[/cyan]=[not bold grey78]{value}[not bold grey78]")
        print()
