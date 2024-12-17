import logging
import time
from dataclasses import dataclass
from pathlib import Path

from httpie.context import Environment
from httpie.core import raw_main
from requests import Response
from rich import print as rprint

from zapman._context import After, Test
from zapman._curl import format_curl
from zapman._exceptions import ZapError, ZapTypeError, ZapValueError
from zapman._io import dump_cookies, dump_store, load_cookies, load_environments
from zapman._module import load_module
from zapman._parse import construct_call_args, extract
from zapman._program import ZapProgramWrapper
from zapman._store import ContextStore

logger = logging.getLogger(__name__)


@dataclass
class RunArgs:
    environment: str
    file_path: str
    quiet: bool = False
    download: bool = False
    verbose: bool = False
    curl: bool = False


def __call(url: str, args: list[str]) -> tuple[Response, bytes | None, Path | None]:
    from httpie.cli.definition import parser  # noqa: PLC0415

    program = ZapProgramWrapper()
    raw_main(parser=parser, main_program=program, args=args, env=Environment())
    if program.response is None:
        raise ZapError(f"🤯 Failed to call '{url}'")
    return program.response, program.content, program.output_file


def __execute_zap(run_args: RunArgs) -> None:  # noqa: C901, PLR0912, PLR0914
    envs = load_environments()
    if run_args.environment not in envs:
        raise ZapValueError(f"Environment '{run_args.environment}' not found in 'zapenvs.py'")
    if not Path(run_args.file_path).exists():
        raise FileNotFoundError(f"Zapfile not found: {run_args.file_path}")

    env_store = ContextStore.get_store(run_args.environment)

    # Dynamically import the Python file
    module = load_module(run_args.file_path)

    zap_file = extract(module)
    _, url = zap_file.method_and_url

    # Load cookies from cache and clear expired cookie
    stored_cookies = load_cookies(url)
    time_now = time.time()
    cookies = [c for c in stored_cookies if not c.is_expired(int(time_now))]
    cookies_map = {c.name: c.value for c in cookies if c.value is not None}

    # Construct HTTPie call arguments
    call_args = construct_call_args(zap_file, cookies_map)
    if run_args.quiet:
        call_args.append("--quiet")
    if run_args.download:
        call_args.append("--download")
    logger.debug(call_args)

    if run_args.curl:
        print(format_curl(zap_file, cookies_map))
        return

    # Do HTTPie call, print and get the response
    response, content, output_file = __call(url, call_args)

    if len(response.cookies) > 0:
        # Overwrite existing cookies with new values, if any
        mapped = {
            **{c.name: c for c in cookies},
            **{c.name: c for c in response.cookies},
        }
        dump_cookies(response.url, [v for _, v in mapped.items()])

    # TODO: experimental and useless for now
    if hasattr(module, "test"):
        func = module.test
        if callable(func):
            func(Test(response, content, output_file))
        else:
            raise ZapTypeError(["'test' is not callable."])

    if hasattr(module, "after"):
        func = module.after
        if callable(func):
            func(After(run_args.environment, response, content, output_file))
        else:
            raise ZapTypeError(["'after' is not callable."])

    if env_store.is_changed():
        dump_store(run_args.environment, env_store.copy())


def execute(  # noqa: PLR0913
    environment: str,
    file_path: str,
    *,
    quiet: bool = False,
    download: bool = False,
    verbose: bool = False,
    curl: bool = False,
) -> None:
    """Execute a Zapfile (which is just a regular Python file).

    Parameters
    ----------
    environment : str
        The API environment to use.
    file_path : str
        The path to the Python file to execute.
    quiet : bool, optional
        Suppress output, by default False
    download : bool, optional
        Download the response body, by default False
    verbose : bool, optional
        Enable debug logging, by default False
    """
    try:
        is_dir = Path(file_path).is_dir()
        if is_dir:
            python_files = list(Path(file_path).glob("*.py"))
            python_files.sort()
            for pf in python_files:
                run_args = RunArgs(environment, str(pf), quiet=quiet, download=download, verbose=verbose, curl=curl)
                if not quiet:
                    rprint(f"[blue]Executing: {pf}[/blue]")
                __execute_zap(run_args)
                if not quiet:
                    rprint(f"[green]Executed: {pf}[/green]")
        else:
            run_args = RunArgs(environment, file_path, quiet=quiet, download=download, verbose=verbose, curl=curl)
            __execute_zap(run_args)
    except (ZapError, FileNotFoundError) as e:
        if not verbose:
            rprint(f"[not bold red]{e}[/not bold red]")
        else:
            raise
