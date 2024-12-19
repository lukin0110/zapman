import argparse
import logging
import sys
from pathlib import Path

from zapman._print import print_cookies, print_stores
from zapman._version import __version__
from zapman._zap import execute

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main() -> None:  # noqa: PLR0911,C901
    # Handle shortcut `zapx`
    invocation_name = Path(sys.argv[0]).name
    if invocation_name == "zapx":
        sys.argv.insert(1, "run")

    parser = argparse.ArgumentParser(
        prog="zap",
        description="A Python tool for API testing and development in your terminal.",
    )
    subparser = parser.add_subparsers(
        title="commands",
        dest="command",
    )
    run = subparser.add_parser(
        "run",
        help="🚀 run a Zapfile",
        description="Provide a Zapfile to invoke with `zapx <zapfile>.py` or `zap run <zapfile>.py`.",
    )
    run.add_argument("-e", "--env", type=str, help="🌐 API environment to use (default=default)", default="default")
    run.add_argument("-d", "--download", action="store_true", help="💾 download the response body")
    run.add_argument("-q", "--quiet", action="store_true", help="🤫 suppress output")
    run.add_argument("-v", "--verbose", action="store_true", help="🐞 enable debug logging", default=False)
    run.add_argument("--curl", action="store_true", help="🌊 print the curl command")
    run.add_argument("path", type=str, help="🐍 the Zapfile to execute", nargs="?", default=None)
    curl = subparser.add_parser("curl", help="🌊 print curl command")
    curl.add_argument("-e", "--env", type=str, help="🌐 API environment to use (default=default)", default="default")
    curl.add_argument("path", type=str, help="🐍 the Zapfile to print the curl command")
    subparser.add_parser("cookies", help="🍪 view stored cookies")
    subparser.add_parser("vars", help="📋 view stored variables")
    subparser.add_parser("version", help="🔖 show version")
    args = parser.parse_args()

    quiet_ = getattr(args, "quiet", False)
    verbose_ = getattr(args, "verbose", False)

    if quiet_ and verbose_:
        print("Cannot use both --quiet and --verbose")
        return
    if verbose_:
        logging.basicConfig(level=logging.DEBUG, force=True)
    elif quiet_:
        logging.disable(logging.CRITICAL)
    if args.command == "cookies":
        print_cookies()
        return
    if args.command == "vars":
        print_stores()
        return
    if args.command == "version":
        print(f"Zapman {__version__}")
        return
    if args.command == "curl":
        environment = args.env
        path_target = Path.cwd() / args.path
        execute(
            environment=environment,
            file_path=str(path_target),
            quiet=True,
            download=False,
            verbose=False,
            curl=True,
        )
        return
    if args.command == "run":
        if args.path is None:
            run.print_help()
            return
        environment = args.env
        path_cwd = Path.cwd()
        path_target = path_cwd / args.path
        logger.debug("Selected: env=%s, path=%s", environment, path_target)
        execute(
            environment=environment,
            file_path=str(path_target),
            quiet=quiet_,
            download=args.download,
            verbose=verbose_,
            curl=False,
        )
        return

    parser.print_help()
